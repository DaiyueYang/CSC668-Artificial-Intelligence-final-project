from dataclasses import dataclass

import pandas as pd


def time_to_min(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m


def min_to_time(m: int) -> str:
    return f"{m // 60:02d}:{m % 60:02d}"


REASON_OVER_BUDGET = "over_budget"
REASON_TOO_MUCH_WAITING = "too_much_waiting"
REASON_CLOSED_BEFORE_VISIT_END = "closed_before_visit_end"
REASON_CANNOT_RETURN_TO_HOTEL = "cannot_return_to_hotel"

ALL_REASONS = (
    REASON_OVER_BUDGET,
    REASON_TOO_MUCH_WAITING,
    REASON_CLOSED_BEFORE_VISIT_END,
    REASON_CANNOT_RETURN_TO_HOTEL,
)


@dataclass(frozen=True)
class TripConstraints:
    budget: float
    num_days: int
    day_start: str = "09:00"
    day_end: str = "21:00"
    max_wait_minutes: int = 120

    @property
    def day_start_min(self) -> int:
        return time_to_min(self.day_start)

    @property
    def day_end_min(self) -> int:
        return time_to_min(self.day_end)


@dataclass
class FeasibilityResult:
    feasible: bool
    reason: str | None = None
    travel: float = 0.0
    arrive: float = 0.0
    visit_start: float = 0.0
    visit_end: float = 0.0
    wait: float = 0.0


def check_feasibility(
    current_time: int,
    current_loc,
    attraction: pd.Series,
    travel_matrix: pd.DataFrame,
    remaining_budget: float,
    constraints: TripConstraints,
) -> FeasibilityResult:
    if attraction["cost"] > remaining_budget:
        return FeasibilityResult(feasible=False, reason=REASON_OVER_BUDGET)

    aid = attraction["attraction_id"]
    travel = travel_matrix.loc[current_loc, aid]
    arrive = current_time + travel

    open_min = time_to_min(attraction["opening_time"])
    close_min = time_to_min(attraction["closing_time"])

    visit_start = max(arrive, open_min)
    wait = visit_start - arrive

    if wait > constraints.max_wait_minutes:
        return FeasibilityResult(feasible=False, reason=REASON_TOO_MUCH_WAITING)

    visit_end = visit_start + attraction["visit_duration"]

    if visit_end > close_min:
        return FeasibilityResult(
            feasible=False, reason=REASON_CLOSED_BEFORE_VISIT_END,
        )

    return_travel = travel_matrix.loc[aid, "hotel"]
    if visit_end + return_travel > constraints.day_end_min:
        return FeasibilityResult(
            feasible=False, reason=REASON_CANNOT_RETURN_TO_HOTEL,
        )

    return FeasibilityResult(
        feasible=True,
        travel=round(float(travel), 1),
        arrive=round(float(arrive), 1),
        visit_start=round(float(visit_start), 1),
        visit_end=round(float(visit_end), 1),
        wait=round(float(wait), 1),
    )


def _normalize(values: list[float]) -> list[float]:
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.5] * len(values)
    return [(v - lo) / (hi - lo) for v in values]


def score_candidates(candidates: list[dict]) -> list[dict]:
    if not candidates:
        return []

    for c in candidates:
        hours = (c["travel"] + c["wait"] + c["duration"]) / 60
        c["time_eff"] = c["priority_score"] / max(hours, 0.1)
        c["cost_eff"] = c["priority_score"] / max(c["cost"], 1.0)

    raw_n = _normalize([c["priority_score"] for c in candidates])
    te_n = _normalize([c["time_eff"] for c in candidates])
    ce_n = _normalize([c["cost_eff"] for c in candidates])

    for i, c in enumerate(candidates):
        c["composite_score"] = (
            0.40 * raw_n[i]
            + 0.35 * te_n[i]
            + 0.25 * ce_n[i]
        )

    candidates.sort(
        key=lambda c: (-c["composite_score"],
                       -c["priority_score"],
                       c["travel"]),
    )
    return candidates


def plan_itinerary(
    attractions: pd.DataFrame,
    travel_matrix: pd.DataFrame,
    budget: float = 200.0,
    num_days: int = 3,
    day_start: str = "09:00",
    day_end: str = "21:00",
    max_wait_minutes: int = 120,
) -> list[list[dict]]:
    constraints = TripConstraints(
        budget=budget,
        num_days=num_days,
        day_start=day_start,
        day_end=day_end,
        max_wait_minutes=max_wait_minutes,
    )

    remaining_budget = constraints.budget
    visited: set[int] = set()
    itinerary: list[list[dict]] = []

    for _ in range(constraints.num_days):
        daily_plan: list[dict] = []
        current_time = constraints.day_start_min
        current_loc = "hotel"

        while True:
            candidates: list[dict] = []
            for _, row in attractions.iterrows():
                aid = row["attraction_id"]
                if aid in visited:
                    continue

                result = check_feasibility(
                    current_time, current_loc, row,
                    travel_matrix, remaining_budget, constraints,
                )
                if not result.feasible:
                    continue

                candidates.append({
                    "attraction_id": aid,
                    "name": row["name"],
                    "category": row["category"],
                    "cost": row["cost"],
                    "duration": row["visit_duration"],
                    "priority_score": row["priority_score"],
                    "travel": result.travel,
                    "arrive": result.arrive,
                    "visit_start": result.visit_start,
                    "visit_end": result.visit_end,
                    "wait": result.wait,
                })

            candidates = score_candidates(candidates)
            if not candidates:
                break

            best = candidates[0]
            daily_plan.append(best)

            visited.add(best["attraction_id"])
            current_time = best["visit_end"]
            current_loc = best["attraction_id"]
            remaining_budget -= best["cost"]

        itinerary.append(daily_plan)

    return itinerary


@dataclass
class _BeamState:
    days_done: tuple
    current_day_plan: tuple
    current_day: int
    current_time: int
    current_loc: object
    visited: frozenset
    remaining_budget: float
    score: float = 0.0


def _make_visit(row: pd.Series, result: FeasibilityResult) -> dict:
    return {
        "attraction_id": row["attraction_id"],
        "name": row["name"],
        "category": row["category"],
        "cost": row["cost"],
        "duration": row["visit_duration"],
        "priority_score": row["priority_score"],
        "travel": result.travel,
        "arrive": result.arrive,
        "visit_start": result.visit_start,
        "visit_end": result.visit_end,
        "wait": result.wait,
    }


def _score_state(
    state: _BeamState,
    constraints: TripConstraints,
    travel_matrix: pd.DataFrame,
    num_categories: int = 6,
) -> float:
    all_visits = [v for day in state.days_done for v in day] + list(state.current_day_plan)
    if not all_visits:
        return 0.0

    total_satisfaction = sum(v["priority_score"] for v in all_visits)
    num_attractions = len(all_visits)
    total_visit = sum(v["duration"] for v in all_visits)

    total_travel = 0.0
    for day in state.days_done:
        if not day:
            continue
        prev = "hotel"
        for v in day:
            total_travel += float(travel_matrix.loc[prev, v["attraction_id"]])
            prev = v["attraction_id"]
        total_travel += float(travel_matrix.loc[day[-1]["attraction_id"], "hotel"])
    if state.current_day_plan:
        prev = "hotel"
        for v in state.current_day_plan:
            total_travel += float(travel_matrix.loc[prev, v["attraction_id"]])
            prev = v["attraction_id"]

    active_time = total_visit + total_travel
    travel_efficiency = total_visit / active_time if active_time > 0 else 0.0

    diversity = len({v["category"] for v in all_visits}) / num_categories

    return (
        1.0 * total_satisfaction
        + 2.0 * num_attractions
        + 3.0 * travel_efficiency
        + 8.0 * diversity
        + 0.15 * state.remaining_budget
    )


def _expand_state(
    state: _BeamState,
    attractions: pd.DataFrame,
    travel_matrix: pd.DataFrame,
    constraints: TripConstraints,
) -> list[_BeamState]:
    if state.current_day >= constraints.num_days:
        return []

    successors: list[_BeamState] = []
    for _, row in attractions.iterrows():
        aid = row["attraction_id"]
        if aid in state.visited:
            continue
        result = check_feasibility(
            state.current_time, state.current_loc, row,
            travel_matrix, state.remaining_budget, constraints,
        )
        if not result.feasible:
            continue
        visit = _make_visit(row, result)
        new_state = _BeamState(
            days_done=state.days_done,
            current_day_plan=state.current_day_plan + (visit,),
            current_day=state.current_day,
            current_time=int(round(result.visit_end)),
            current_loc=aid,
            visited=state.visited | {aid},
            remaining_budget=state.remaining_budget - float(row["cost"]),
        )
        new_state.score = _score_state(new_state, constraints, travel_matrix)
        successors.append(new_state)

    if successors:
        return successors

    end_day = _BeamState(
        days_done=state.days_done + (state.current_day_plan,),
        current_day_plan=(),
        current_day=state.current_day + 1,
        current_time=constraints.day_start_min,
        current_loc="hotel",
        visited=state.visited,
        remaining_budget=state.remaining_budget,
    )
    end_day.score = _score_state(end_day, constraints, travel_matrix)
    return [end_day]


def plan_itinerary_beam_search(
    attractions: pd.DataFrame,
    travel_matrix: pd.DataFrame,
    budget: float = 200.0,
    num_days: int = 3,
    day_start: str = "09:00",
    day_end: str = "21:00",
    max_wait_minutes: int = 120,
    beam_width: int = 5,
) -> list[list[dict]]:
    constraints = TripConstraints(
        budget=budget,
        num_days=num_days,
        day_start=day_start,
        day_end=day_end,
        max_wait_minutes=max_wait_minutes,
    )

    start = _BeamState(
        days_done=(),
        current_day_plan=(),
        current_day=0,
        current_time=constraints.day_start_min,
        current_loc="hotel",
        visited=frozenset(),
        remaining_budget=float(constraints.budget),
    )
    beam: list[_BeamState] = [start]

    while True:
        frontier: list[_BeamState] = []
        any_extended = False
        for state in beam:
            successors = _expand_state(state, attractions, travel_matrix, constraints)
            if successors:
                any_extended = True
                frontier.extend(successors)
            else:
                frontier.append(state)
        if not any_extended:
            break
        frontier.sort(key=lambda s: s.score, reverse=True)
        beam = frontier[:beam_width]

    best = max(beam, key=lambda s: s.score)

    final_days: list[list[dict]] = [list(day) for day in best.days_done]
    if best.current_day_plan:
        final_days.append(list(best.current_day_plan))
    while len(final_days) < constraints.num_days:
        final_days.append([])
    return final_days
