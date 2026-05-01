import argparse
import os
import time

from data_generator import (
    generate_attractions,
    generate_travel_time_matrix,
    save_dataset,
)
from planner import (
    TripConstraints,
    plan_itinerary,
    plan_itinerary_beam_search,
)
from formatter import print_itinerary
from evaluator import evaluate_itinerary, print_evaluation, validate_itinerary
from experiment_runner import run_experiments
from scenarios import SCENARIOS, Scenario, all_scenarios, get_scenario

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data")


USAGE_EXAMPLES = """\
examples:
  python src/main.py
      Run the default: scenario=standard, algorithm=beam_search.

  python src/main.py --scenario standard --algorithm beam_search
      Run a single scenario with a specific algorithm.

  python src/main.py --scenario all --algorithm greedy
      Run every scenario with greedy; print a comparison table in the terminal.

  python src/main.py --run-experiments
      Run every scenario under both algorithms; write CSV, Markdown
      itineraries, and charts to outputs/.

  python src/main.py --make-charts
      Regenerate charts from outputs/experiment_results.csv (no re-run).

  python src/main.py --scenario standard --seed 7
      Override the scenario's random seed."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Constrained travel itinerary planner.",
        epilog=USAGE_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--scenario",
        default="standard",
        choices=list(SCENARIOS.keys()) + ["all"],
        help="Which evaluation scenario to run (default: standard). "
             "Use 'all' to print a comparison table across every scenario.",
    )
    parser.add_argument(
        "--algorithm",
        choices=["greedy", "beam_search"],
        default="beam_search",
        help="Planning algorithm for single-scenario mode (default: beam_search). "
             "Ignored by --run-experiments, which always runs both.",
    )
    parser.add_argument(
        "--beam-width",
        type=int,
        default=None,
        help="Override the scenario's beam_width (beam_search only).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Override the scenario's random seed. Applies to every scenario "
             "when combined with --run-experiments.",
    )
    parser.add_argument(
        "--run-experiments",
        action="store_true",
        help="Run every scenario under both algorithms; write CSV, Markdown "
             "itineraries, and charts to outputs/. Ignores --scenario and "
             "--algorithm.",
    )
    parser.add_argument(
        "--make-charts",
        action="store_true",
        help="Regenerate charts from outputs/experiment_results.csv (no re-run). "
             "Requires --run-experiments to have been run before.",
    )
    parser.add_argument(
        "--show-itinerary",
        action="store_true",
        help="Print the detailed per-day itinerary for a single scenario run.",
    )
    return parser.parse_args()


def _run_one(
    scenario: Scenario,
    algorithm: str,
    beam_width_override: int | None,
    seed_override: int | None,
    verbose: bool,
    show_itinerary: bool = False,
) -> dict:
    seed = seed_override if seed_override is not None else scenario.seed
    attractions = generate_attractions(
        n=scenario.num_attractions, seed=seed,
    )
    travel_matrix = generate_travel_time_matrix(attractions)
    constraints = TripConstraints(
        budget=scenario.budget,
        num_days=scenario.num_days,
        day_start=scenario.day_start,
        day_end=scenario.day_end,
    )

    beam_width = (beam_width_override if beam_width_override is not None
                  else scenario.beam_width)

    if verbose:
        save_dataset(
            attractions, travel_matrix,
            data_dir=os.path.join(DATA_DIR, scenario.name),
        )
        print(f"Scenario: {scenario.name} | Algorithm: {algorithm}"
              + (f" | beam_width={beam_width}" if algorithm == "beam_search" else ""))
        print(f"Attractions: {scenario.num_attractions} | Budget: ${scenario.budget:.0f} "
              f"| Days: {scenario.num_days} | Window: {scenario.day_start}-{scenario.day_end}")

    start = time.perf_counter()
    if algorithm == "greedy":
        itinerary = plan_itinerary(
            attractions, travel_matrix,
            budget=constraints.budget,
            num_days=constraints.num_days,
            day_start=constraints.day_start,
            day_end=constraints.day_end,
        )
    else:
        itinerary = plan_itinerary_beam_search(
            attractions, travel_matrix,
            budget=constraints.budget,
            num_days=constraints.num_days,
            day_start=constraints.day_start,
            day_end=constraints.day_end,
            beam_width=beam_width,
        )
    elapsed = time.perf_counter() - start

    metrics = evaluate_itinerary(
        itinerary, attractions, travel_matrix,
        constraints, runtime_seconds=elapsed,
    )

    if verbose:
        if show_itinerary:
            print_itinerary(itinerary, travel_matrix)
        _, violations = validate_itinerary(
            itinerary, attractions, travel_matrix, constraints,
        )
        print_evaluation(metrics, violations)

    return metrics


def _print_comparison(
    rows: list[tuple[Scenario, dict]],
    algorithm: str,
) -> None:
    headers = ("scenario", "N", "days", "budget", "visits", "cost",
               "satisf.", "travel", "diverse", "balance", "feas", "runtime_s")
    widths = (14, 4, 5, 7, 7, 7, 8, 7, 8, 8, 5, 10)

    def fmt_row(vals):
        return "  " + "  ".join(f"{v:<{w}}" for v, w in zip(vals, widths))

    print(f"\n{'=' * 118}")
    print(f"  Cross-scenario comparison  (algorithm = {algorithm})")
    print(f"{'=' * 118}")
    print(fmt_row(headers))
    print("  " + "-" * 116)
    for scenario, m in rows:
        vals = (
            scenario.name,
            scenario.num_attractions,
            scenario.num_days,
            f"${scenario.budget:.0f}",
            m["attractions_visited"],
            f"${m['total_cost']:.0f}",
            f"{m['total_satisfaction']:.1f}",
            f"{m['total_travel_minutes']:.0f}",
            f"{m['category_diversity']:.2f}",
            f"{m['daily_balance']:.2f}",
            "OK" if m["feasible"] else f"x{m['num_violations']}",
            f"{m['runtime_seconds']:.3f}" if m.get("runtime_seconds") is not None else "-",
        )
        print(fmt_row(vals))
    print()


def main():
    args = parse_args()

    if args.run_experiments:
        run_experiments(
            beam_width_override=args.beam_width,
            seed_override=args.seed,
        )
        return

    if args.make_charts:
        from visualizer import generate_all_charts
        generate_all_charts()
        return

    if args.scenario == "all":
        rows: list[tuple[Scenario, dict]] = []
        for scenario in all_scenarios():
            metrics = _run_one(
                scenario, args.algorithm, args.beam_width, args.seed,
                verbose=False,
                show_itinerary=False,
            )
            rows.append((scenario, metrics))
        _print_comparison(rows, args.algorithm)
    else:
        scenario = get_scenario(args.scenario)
        _run_one(
            scenario, args.algorithm, args.beam_width, args.seed,
            verbose=True,
            show_itinerary=args.show_itinerary,
        )


if __name__ == "__main__":
    main()
