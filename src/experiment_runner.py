import os
import time
from datetime import datetime

import pandas as pd

from data_generator import generate_attractions, generate_travel_time_matrix
from planner import (
    TripConstraints,
    plan_itinerary,
    plan_itinerary_beam_search,
)
from evaluator import evaluate_itinerary, validate_itinerary
from scenarios import Scenario, all_scenarios


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(REPO_ROOT, "outputs")
ITINERARIES_DIR = os.path.join(OUTPUTS_DIR, "itineraries")
RESULTS_CSV = os.path.join(OUTPUTS_DIR, "experiment_results.csv")

RESULT_COLUMNS = [
    "scenario", "planner", "beam_width",
    "num_attractions", "num_days", "budget", "day_start", "day_end",
    "feasible", "num_violations",
    "attractions_visited", "total_cost", "remaining_budget",
    "total_satisfaction", "total_visit_minutes", "total_travel_minutes",
    "travel_ratio", "category_diversity", "daily_balance",
    "runtime_seconds",
]


def _ensure_dirs() -> None:
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    os.makedirs(ITINERARIES_DIR, exist_ok=True)


def _min_to_time(m: float) -> str:
    m_int = int(round(m))
    return f"{m_int // 60:02d}:{m_int % 60:02d}"


def _render_markdown(
    scenario: Scenario,
    planner: str,
    beam_width: int | None,
    itinerary: list[list[dict]],
    travel_matrix: pd.DataFrame,
    metrics: dict,
    violations: list[dict],
) -> str:
    lines: list[str] = []
    lines.append(f"# Itinerary: {scenario.name} / {planner}")
    lines.append("")
    lines.append(f"_Generated {datetime.now().isoformat(timespec='seconds')}_")
    lines.append("")

    lines.append("## Scenario")
    lines.append(f"- **{scenario.name}**: {scenario.description}")
    lines.append(f"- N attractions: {scenario.num_attractions} (seed {scenario.seed})")
    lines.append(f"- Budget: ${scenario.budget:.0f}")
    lines.append(f"- Days: {scenario.num_days}")
    lines.append(f"- Daily window: {scenario.day_start} - {scenario.day_end}")
    bw_suffix = f" (beam_width={beam_width})" if planner == "beam_search" else ""
    lines.append(f"- Planner: {planner}{bw_suffix}")
    lines.append("")

    lines.append("## Metrics")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    feas = "OK" if metrics["feasible"] else f"FAILED ({metrics['num_violations']})"
    lines.append(f"| Feasibility | {feas} |")
    lines.append(f"| Attractions visited | {metrics['attractions_visited']} |")
    lines.append(f"| Total cost | ${metrics['total_cost']:.2f} |")
    lines.append(f"| Remaining budget | ${metrics['remaining_budget']:.2f} |")
    lines.append(f"| Total satisfaction | {metrics['total_satisfaction']} |")
    lines.append(f"| Total visit minutes | {metrics['total_visit_minutes']} |")
    lines.append(f"| Total travel minutes | {metrics['total_travel_minutes']} |")
    lines.append(f"| Travel ratio | {metrics['travel_ratio']} |")
    lines.append(f"| Category diversity | {metrics['category_diversity']} |")
    lines.append(f"| Daily balance | {metrics['daily_balance']} |")
    if metrics.get("runtime_seconds") is not None:
        lines.append(f"| Runtime (seconds) | {metrics['runtime_seconds']} |")
    lines.append("")

    for day_idx, day_plan in enumerate(itinerary, start=1):
        lines.append(f"## Day {day_idx}")
        if not day_plan:
            lines.append("_(rest day - no visits scheduled)_")
            lines.append("")
            continue

        lines.append("| # | Window | Name | Category | Cost | Score |")
        lines.append("|---|---|---|---|---|---|")
        for step, v in enumerate(day_plan, start=1):
            window = f"{_min_to_time(v['visit_start'])} - {_min_to_time(v['visit_end'])}"
            lines.append(
                f"| {step} | {window} | {v['name']} | {v['category']} "
                f"| ${v['cost']:.0f} | {v['priority_score']} |"
            )

        last_aid = day_plan[-1]["attraction_id"]
        return_travel = float(travel_matrix.loc[last_aid, "hotel"])
        return_at = day_plan[-1]["visit_end"] + return_travel
        lines.append("")
        lines.append(f"_Return to hotel at {_min_to_time(return_at)} "
                     f"(travel {return_travel:.0f} min)._")
        lines.append("")

    if violations:
        lines.append("## Violations")
        for v in violations:
            day = f"day {v['day'] + 1}" if v["day"] >= 0 else "trip"
            step = f"step {v['step'] + 1}" if v["step"] >= 0 else ""
            aid = f"aid={v['attraction_id']}" if v["attraction_id"] is not None else ""
            tag = " ".join(b for b in (day, step, aid) if b)
            lines.append(f"- **{tag}** {v['reason']}: {v['detail']}")
        lines.append("")

    return "\n".join(lines)


def _itinerary_filename(scenario_name: str, planner: str) -> str:
    return f"{scenario_name}_{planner}.md"


def run_one(
    scenario: Scenario,
    planner: str,
    beam_width_override: int | None = None,
    seed_override: int | None = None,
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
    effective_beam = (beam_width_override
                      if beam_width_override is not None
                      else scenario.beam_width)

    start = time.perf_counter()
    if planner == "greedy":
        itinerary = plan_itinerary(
            attractions, travel_matrix,
            budget=constraints.budget,
            num_days=constraints.num_days,
            day_start=constraints.day_start,
            day_end=constraints.day_end,
        )
    elif planner == "beam_search":
        itinerary = plan_itinerary_beam_search(
            attractions, travel_matrix,
            budget=constraints.budget,
            num_days=constraints.num_days,
            day_start=constraints.day_start,
            day_end=constraints.day_end,
            beam_width=effective_beam,
        )
    else:
        raise ValueError(f"Unknown planner {planner!r}")
    elapsed = time.perf_counter() - start

    metrics = evaluate_itinerary(
        itinerary, attractions, travel_matrix,
        constraints, runtime_seconds=elapsed,
    )
    _, violations = validate_itinerary(
        itinerary, attractions, travel_matrix, constraints,
    )

    md = _render_markdown(
        scenario, planner,
        beam_width=effective_beam if planner == "beam_search" else None,
        itinerary=itinerary, travel_matrix=travel_matrix,
        metrics=metrics, violations=violations,
    )
    md_path = os.path.join(ITINERARIES_DIR,
                           _itinerary_filename(scenario.name, planner))
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    return {
        "scenario": scenario.name,
        "planner": planner,
        "beam_width": effective_beam if planner == "beam_search" else "",
        "num_attractions": scenario.num_attractions,
        "num_days": scenario.num_days,
        "budget": scenario.budget,
        "day_start": scenario.day_start,
        "day_end": scenario.day_end,
        **{k: metrics[k] for k in (
            "feasible", "num_violations",
            "attractions_visited", "total_cost", "remaining_budget",
            "total_satisfaction", "total_visit_minutes", "total_travel_minutes",
            "travel_ratio", "category_diversity", "daily_balance",
            "runtime_seconds",
        )},
    }


def run_experiments(
    planners: tuple[str, ...] = ("greedy", "beam_search"),
    beam_width_override: int | None = None,
    seed_override: int | None = None,
    make_charts: bool = True,
) -> pd.DataFrame:
    _ensure_dirs()
    rows: list[dict] = []
    for scenario in all_scenarios():
        for planner in planners:
            row = run_one(scenario, planner, beam_width_override, seed_override)
            rows.append(row)

    df = pd.DataFrame(rows, columns=RESULT_COLUMNS)
    df.to_csv(RESULTS_CSV, index=False)

    if make_charts:
        from visualizer import generate_all_charts
        generate_all_charts(RESULTS_CSV)

    return df


if __name__ == "__main__":
    run_experiments()
