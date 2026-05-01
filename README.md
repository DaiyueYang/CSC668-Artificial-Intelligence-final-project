# Constrained Travel Itinerary Planner

An AI-based constrained travel itinerary planner that produces multi-day trip plans under budget, time, opening-hour, and travel-time constraints. The project uses synthetic data generated programmatically, and the core planning logic was implemented specifically for this project.

## Requirements

-   Python 3.10+
-   `numpy`
-   `pandas`
-   `matplotlib`

Install with:

``` bash
pip install -r requirements.txt
```

## Quick Start

``` bash
python src/main.py
python src/main.py --show-itinerary
python src/main.py --run-experiments
python src/main.py --make-charts
```

## Full CLI

Run `python src/main.py --help` for the complete reference.

| Flag | Default | Description |
|----|----|----|
| `--scenario NAME` | `standard` | One of `easy`, `standard`, `tight_budget`, `tight_time`, `large_problem`, or `all`. |
| `--algorithm NAME` | `beam_search` | One of `greedy` or `beam_search`. |
| `--beam-width N` | scenario default | Override beam width for `beam_search`. |
| `--seed N` | scenario default | Override the scenario random seed. |
| `--run-experiments` | off | Run every scenario x every algorithm and write CSV, Markdown, and charts. |
| `--make-charts` | off | Re-render charts from `outputs/experiment_results.csv`. |
| `--show-itinerary` | off | Print the detailed per-day itinerary for a single run. |

Example commands:

``` bash
python src/main.py --scenario standard --algorithm beam_search
python src/main.py --scenario all --algorithm greedy
python src/main.py --scenario standard --seed 7
python src/main.py --scenario large_problem --beam-width 20
```

## Project Structure

``` text
README.md                   Project overview
final_report.md             Links to both report versions
final_report_en.md          English final report
final_report_zh.md          Chinese final report
requirements.txt            Python dependencies
src/
  main.py                   CLI entry point
  data_generator.py         Synthetic attractions and travel matrix
  scenarios.py              Five predefined experiment presets
  planner.py                TripConstraints, greedy planner, beam search
  evaluator.py              validate_itinerary and evaluate_itinerary
  formatter.py              Optional per-day itinerary printer
  visualizer.py             matplotlib charts
  experiment_runner.py      Scenario x algorithm sweep
tests/
  test_smoke.py             Smoke tests
data/                       Per-scenario attractions and travel matrix CSVs
outputs/
  experiment_results.csv    One row per scenario and algorithm
  itineraries/              10 readable Markdown itineraries
  charts/                   4 matplotlib PNG charts
final project docs/         Early design notes
```

## Scenarios

| Scenario        |   N | Days | Budget | Window      | Beam | Design intent           |
|-----------------|----:|-----:|-------:|-------------|-----:|-------------------------|
| `easy`          |  20 |    3 |  \$400 | 08:00-22:00 |    5 | Loose constraints       |
| `standard`      |  30 |    3 |  \$200 | 09:00-21:00 |    5 | Reference case          |
| `tight_budget`  |  30 |    3 |   \$80 | 09:00-21:00 |    5 | Budget is binding       |
| `tight_time`    |  30 |    3 |  \$200 | 10:00-17:00 |    5 | Daily window is binding |
| `large_problem` |  50 |    5 |  \$400 | 09:00-21:00 |   10 | Scalability test        |

Defined in [`src/scenarios.py`](src/scenarios.py). All scenarios use `seed=42` unless overridden with `--seed`.

## Running Tests

``` bash
python -m unittest discover -s tests -v
```

Smoke tests cover synthetic data generation, the four feasibility reason codes, planner output shape, evaluator keys, and end-to-end feasibility.

## Outputs

After `python src/main.py --run-experiments`:

-   [`outputs/experiment_results.csv`](outputs/experiment_results.csv): 10 rows, one for each scenario and algorithm combination.
-   [`outputs/itineraries/`](outputs/itineraries/): 10 Markdown files with per-day itinerary breakdowns.
-   [`outputs/charts/`](outputs/charts/): 4 PNG charts for satisfaction, attraction count, runtime, and travel ratio.

All output directories are created automatically if they do not exist.
