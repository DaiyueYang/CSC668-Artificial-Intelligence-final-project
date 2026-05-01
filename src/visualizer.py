import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_CSV = os.path.join(REPO_ROOT, "outputs", "experiment_results.csv")
CHARTS_DIR = os.path.join(REPO_ROOT, "outputs", "charts")

SCENARIO_ORDER = ["easy", "standard", "tight_budget", "tight_time", "large_problem"]
PLANNER_ORDER = ["greedy", "beam_search"]
PLANNER_COLORS = {
    "greedy":      "#7e7e7e",
    "beam_search": "#1f77b4",
}


def _ensure_dirs() -> None:
    os.makedirs(CHARTS_DIR, exist_ok=True)


def load_results(csv_path: str = RESULTS_CSV) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Results CSV not found at {csv_path!r}. "
            f"Run `python src/main.py --run-experiments` first."
        )
    df = pd.read_csv(csv_path)
    df["scenario"] = pd.Categorical(
        df["scenario"], categories=SCENARIO_ORDER, ordered=True,
    )
    df["planner"] = pd.Categorical(
        df["planner"], categories=PLANNER_ORDER, ordered=True,
    )
    return df.sort_values(["scenario", "planner"]).reset_index(drop=True)


def _grouped_bar(
    df: pd.DataFrame,
    metric: str,
    ylabel: str,
    title: str,
    filename: str,
    value_format: str = "{:.1f}",
    log_y: bool = False,
) -> str:
    pivot = df.pivot(index="scenario", columns="planner", values=metric)
    pivot = pivot.reindex(SCENARIO_ORDER)[PLANNER_ORDER]

    n_scen = len(pivot.index)
    n_plan = len(pivot.columns)
    bar_width = 0.38
    x_positions = list(range(n_scen))

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for i, planner in enumerate(pivot.columns):
        offsets = [x + (i - (n_plan - 1) / 2) * bar_width for x in x_positions]
        values = pivot[planner].values
        bars = ax.bar(
            offsets, values, bar_width,
            label=planner,
            color=PLANNER_COLORS.get(planner),
            edgecolor="white",
        )
        for bar, v in zip(bars, values):
            if pd.isna(v):
                continue
            ax.annotate(
                value_format.format(v),
                xy=(bar.get_x() + bar.get_width() / 2, v),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center", va="bottom",
                fontsize=8,
            )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(pivot.index, rotation=15)
    ax.set_xlabel("Scenario")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if log_y:
        ax.set_yscale("log")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)

    y_top = ax.get_ylim()[1]
    if log_y:
        ax.set_ylim(top=y_top * 4)
    else:
        ax.set_ylim(0, y_top * 1.18)

    ax.legend(title="Planner", loc="upper left")
    fig.tight_layout()

    out_path = os.path.join(CHARTS_DIR, filename)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def chart_satisfaction(df: pd.DataFrame) -> str:
    return _grouped_bar(
        df, "total_satisfaction",
        ylabel="Total satisfaction (sum of priority scores)",
        title="Total satisfaction by scenario and planner",
        filename="satisfaction.png",
        value_format="{:.1f}",
    )


def chart_attractions(df: pd.DataFrame) -> str:
    return _grouped_bar(
        df, "attractions_visited",
        ylabel="Attractions visited",
        title="Attractions visited by scenario and planner",
        filename="attractions.png",
        value_format="{:.0f}",
    )


def chart_runtime(df: pd.DataFrame) -> str:
    return _grouped_bar(
        df, "runtime_seconds",
        ylabel="Runtime (seconds, log scale)",
        title="Planner runtime by scenario",
        filename="runtime.png",
        value_format="{:.3f}",
        log_y=True,
    )


def chart_travel_ratio(df: pd.DataFrame) -> str:
    return _grouped_bar(
        df, "travel_ratio",
        ylabel="Travel ratio  (travel time / active time)",
        title="Travel ratio by scenario and planner",
        filename="travel_ratio.png",
        value_format="{:.3f}",
    )


def generate_all_charts(csv_path: str = RESULTS_CSV) -> list[str]:
    _ensure_dirs()
    df = load_results(csv_path)
    paths = [
        chart_satisfaction(df),
        chart_attractions(df),
        chart_runtime(df),
        chart_travel_ratio(df),
    ]
    return paths


if __name__ == "__main__":
    generate_all_charts()
