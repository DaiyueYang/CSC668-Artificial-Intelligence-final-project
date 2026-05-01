from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    name: str
    description: str
    num_attractions: int
    seed: int
    budget: float
    num_days: int
    day_start: str
    day_end: str
    beam_width: int = 5


SCENARIOS: dict[str, Scenario] = {
    "easy": Scenario(
        name="easy",
        description="Larger budget, longer day window, fewer attractions.",
        num_attractions=20,
        seed=42,
        budget=400.0,
        num_days=3,
        day_start="08:00",
        day_end="22:00",
        beam_width=5,
    ),
    "standard": Scenario(
        name="standard",
        description="Reference case: 30 attractions, $200, 09:00-21:00 x 3 days.",
        num_attractions=30,
        seed=42,
        budget=200.0,
        num_days=3,
        day_start="09:00",
        day_end="21:00",
        beam_width=5,
    ),
    "tight_budget": Scenario(
        name="tight_budget",
        description="Low budget - forces the planner toward cheap attractions.",
        num_attractions=30,
        seed=42,
        budget=80.0,
        num_days=3,
        day_start="09:00",
        day_end="21:00",
        beam_width=5,
    ),
    "tight_time": Scenario(
        name="tight_time",
        description="Short daily window 10:00-17:00 - time is the binding constraint.",
        num_attractions=30,
        seed=42,
        budget=200.0,
        num_days=3,
        day_start="10:00",
        day_end="17:00",
        beam_width=5,
    ),
    "large_problem": Scenario(
        name="large_problem",
        description="Scaled up: 50 attractions, 5 days - tests scalability.",
        num_attractions=50,
        seed=42,
        budget=400.0,
        num_days=5,
        day_start="09:00",
        day_end="21:00",
        beam_width=10,
    ),
}


def get_scenario(name: str) -> Scenario:
    try:
        return SCENARIOS[name]
    except KeyError:
        valid = ", ".join(sorted(SCENARIOS))
        raise KeyError(f"Unknown scenario {name!r}. Valid: {valid}") from None


def all_scenarios() -> list[Scenario]:
    return list(SCENARIOS.values())
