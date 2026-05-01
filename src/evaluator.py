from statistics import mean, stdev

import pandas as pd

from planner import TripConstraints, time_to_min


VIOLATION_OVER_BUDGET = "over_budget"
VIOLATION_TOO_MUCH_WAITING = "too_much_waiting"
VIOLATION_CLOSED_BEFORE_VISIT_END = "closed_before_visit_end"
VIOLATION_CANNOT_RETURN_TO_HOTEL = "cannot_return_to_hotel"
VIOLATION_DOUBLE_VISIT = "double_visit"
VIOLATION_TOO_MANY_DAYS = "too_many_days"
VIOLATION_UNKNOWN_ATTRACTION = "unknown_attraction"

NUM_CATEGORIES = 6

_EPS = 1e-9


def validate_itinerary(
    itinerary: list[list[dict]],
    attractions: pd.DataFrame,
    travel_matrix: pd.DataFrame,
    constraints: TripConstraints,
) -> tuple[bool, list[dict]]:
    violations: list[dict] = []

    if len(itinerary) > constraints.num_days:
        violations.append({
            "day": -1, "step": -1, "attraction_id": None,
            "reason": VIOLATION_TOO_MANY_DAYS,
            "detail": f"{len(itinerary)} days planned, "
                      f"{constraints.num_days} allowed",
        })

    by_id = attractions.set_index("attraction_id")
    visited_global: set = set()
    remaining_budget = float(constraints.budget)

    for day_idx, day_plan in enumerate(itinerary):
        current_time: float = float(constraints.day_start_min)
        current_loc = "hotel"

        for step, visit in enumerate(day_plan):
            aid = visit["attraction_id"]

            if aid not in by_id.index:
                violations.append({
                    "day": day_idx, "step": step, "attraction_id": aid,
                    "reason": VIOLATION_UNKNOWN_ATTRACTION,
                    "detail": "attraction id not in dataset",
                })
                continue
            if aid in visited_global:
                violations.append({
                    "day": day_idx, "step": step, "attraction_id": aid,
                    "reason": VIOLATION_DOUBLE_VISIT,
                    "detail": "visited on an earlier day",
                })
            visited_global.add(aid)

            row = by_id.loc[aid]
            cost = float(row["cost"])
            if cost > remaining_budget + _EPS:
                violations.append({
                    "day": day_idx, "step": step, "attraction_id": aid,
                    "reason": VIOLATION_OVER_BUDGET,
                    "detail": f"cost={cost}, remaining={remaining_budget:.2f}",
                })
            remaining_budget -= cost

            travel = float(travel_matrix.loc[current_loc, aid])
            arrive = current_time + travel
            open_min = time_to_min(str(row["opening_time"]))
            close_min = time_to_min(str(row["closing_time"]))
            visit_start = max(arrive, open_min)
            wait = visit_start - arrive

            if wait > constraints.max_wait_minutes + _EPS:
                violations.append({
                    "day": day_idx, "step": step, "attraction_id": aid,
                    "reason": VIOLATION_TOO_MUCH_WAITING,
                    "detail": f"wait={wait:.1f}min, "
                              f"max={constraints.max_wait_minutes}",
                })

            visit_end = visit_start + float(row["visit_duration"])
            if visit_end > close_min + _EPS:
                violations.append({
                    "day": day_idx, "step": step, "attraction_id": aid,
                    "reason": VIOLATION_CLOSED_BEFORE_VISIT_END,
                    "detail": f"visit_end={visit_end:.1f}, "
                              f"closes_at={close_min}",
                })

            current_time = visit_end
            current_loc = aid

        if day_plan:
            return_travel = float(travel_matrix.loc[current_loc, "hotel"])
            if current_time + return_travel > constraints.day_end_min + _EPS:
                violations.append({
                    "day": day_idx, "step": len(day_plan) - 1,
                    "attraction_id": day_plan[-1]["attraction_id"],
                    "reason": VIOLATION_CANNOT_RETURN_TO_HOTEL,
                    "detail": (f"back_at_hotel={current_time + return_travel:.1f}, "
                               f"day_end={constraints.day_end_min}"),
                })

    return (len(violations) == 0), violations


def evaluate_itinerary(
    itinerary: list[list[dict]],
    attractions: pd.DataFrame,
    travel_matrix: pd.DataFrame,
    constraints: TripConstraints,
    runtime_seconds: float | None = None,
) -> dict:
    is_feasible, violations = validate_itinerary(
        itinerary, attractions, travel_matrix, constraints,
    )

    total_cost = 0.0
    total_satisfaction = 0.0
    total_travel = 0.0
    total_visit = 0.0
    categories: set = set()

    for day_plan in itinerary:
        prev_loc = "hotel"
        for visit in day_plan:
            aid = visit["attraction_id"]
            total_travel += float(travel_matrix.loc[prev_loc, aid])
            total_visit += float(visit["duration"])
            total_cost += float(visit["cost"])
            total_satisfaction += float(visit["priority_score"])
            categories.add(visit["category"])
            prev_loc = aid
        if day_plan:
            total_travel += float(
                travel_matrix.loc[day_plan[-1]["attraction_id"], "hotel"]
            )

    num_attractions = sum(len(d) for d in itinerary)
    active_time = total_travel + total_visit
    travel_ratio = total_travel / active_time if active_time > 0 else 0.0
    diversity = len(categories) / NUM_CATEGORIES

    visits_per_day = [len(d) for d in itinerary]
    if len(visits_per_day) > 1 and mean(visits_per_day) > 0:
        balance = max(1.0 - stdev(visits_per_day) / mean(visits_per_day), 0.0)
    else:
        balance = 1.0

    return {
        "feasible": bool(is_feasible),
        "num_violations": len(violations),
        "attractions_visited": num_attractions,
        "total_cost": round(total_cost, 2),
        "remaining_budget": round(float(constraints.budget) - total_cost, 2),
        "total_satisfaction": round(total_satisfaction, 1),
        "total_visit_minutes": round(total_visit, 1),
        "total_travel_minutes": round(total_travel, 1),
        "travel_ratio": round(travel_ratio, 3),
        "category_diversity": round(diversity, 2),
        "daily_balance": round(balance, 2),
        "runtime_seconds": (round(runtime_seconds, 4)
                            if runtime_seconds is not None else None),
    }


def print_evaluation(metrics: dict, violations: list[dict] | None = None) -> None:
    print("Evaluation:")
    if metrics["feasible"]:
        print(f"  Feasibility          : OK")
    else:
        print(f"  Feasibility          : FAILED "
              f"({metrics['num_violations']} violation(s))")
    print(f"  Attractions visited  : {metrics['attractions_visited']}")
    print(f"  Total cost           : ${metrics['total_cost']:.2f}")
    print(f"  Remaining budget     : ${metrics['remaining_budget']:.2f}")
    print(f"  Total satisfaction   : {metrics['total_satisfaction']}")
    print(f"  Total visit minutes  : {metrics['total_visit_minutes']}")
    print(f"  Total travel minutes : {metrics['total_travel_minutes']}")
    print(f"  Travel ratio         : {metrics['travel_ratio']}")
    print(f"  Category diversity   : {metrics['category_diversity']}")
    print(f"  Daily balance        : {metrics['daily_balance']}")
    if metrics["runtime_seconds"] is not None:
        print(f"  Runtime (seconds)    : {metrics['runtime_seconds']}")

    if violations:
        print("  Violations:")
        for v in violations:
            day_label = f"day {v['day'] + 1}" if v["day"] >= 0 else "trip-level"
            step_label = f"step {v['step'] + 1}" if v["step"] >= 0 else ""
            aid_label = f"aid={v['attraction_id']}" if v["attraction_id"] is not None else ""
            bits = [b for b in (day_label, step_label, aid_label) if b]
            print(f"    {' '.join(bits)}  {v['reason']}: {v['detail']}")
