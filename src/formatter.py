from statistics import mean, stdev

from planner import min_to_time


def print_itinerary(
    itinerary: list[list[dict]],
    travel_matrix,
) -> None:
    total_cost = 0.0
    total_score = 0.0
    total_attractions = 0
    total_travel = 0.0

    for day_idx, day_plan in enumerate(itinerary, start=1):
        print(f"\n{'='*60}")
        print(f"  DAY {day_idx}")
        print(f"{'='*60}")

        if not day_plan:
            print("  (rest day - no visits scheduled)")
            continue

        prev_loc = "hotel"
        for step, visit in enumerate(day_plan, start=1):
            aid = visit["attraction_id"]

            travel_min = travel_matrix.loc[prev_loc, aid]
            total_travel += travel_min

            print(f"\n  [{step}] {visit['name']}")
            print(f"      Category     : {visit['category']}")
            print(f"      Travel there : {travel_min:.0f} min")
            if visit["wait"] > 0:
                print(f"      Wait         : {visit['wait']:.0f} min"
                      f" (arrives before opening)")
            print(f"      Visit window : {min_to_time(int(visit['visit_start']))}"
                  f" - {min_to_time(int(visit['visit_end']))}"
                  f"  ({visit['duration']} min)")
            print(f"      Cost         : ${visit['cost']:.0f}")
            print(f"      Score        : {visit['priority_score']}")

            total_cost += visit["cost"]
            total_score += visit["priority_score"]
            total_attractions += 1
            prev_loc = aid

        last_aid = day_plan[-1]["attraction_id"]
        return_travel = travel_matrix.loc[last_aid, "hotel"]
        total_travel += return_travel
        return_by = day_plan[-1]["visit_end"] + return_travel
        print(f"\n  Return to hotel : {min_to_time(int(return_by))}"
              f"  (travel {return_travel:.0f} min)")

    print(f"\n{'='*60}")
    print(f"  TRIP SUMMARY")
    print(f"{'='*60}")
    print(f"  Attractions visited : {total_attractions}")
    print(f"  Total cost          : ${total_cost:.0f}")
    print(f"  Total satisfaction  : {total_score:.1f}")
    print(f"  Total travel time   : {total_travel:.0f} min")

    categories = set(v["category"] for day in itinerary for v in day)
    print(f"  Categories covered  : {len(categories)}"
          f"  ({', '.join(sorted(categories))})")

    visits_per_day = [len(day) for day in itinerary]
    print(f"  Visits per day      : {visits_per_day}")
    if len(visits_per_day) > 1 and mean(visits_per_day) > 0:
        bal = 1.0 - stdev(visits_per_day) / mean(visits_per_day)
        print(f"  Daily balance       : {max(bal, 0):.2f}  (1.0 = perfect)")
    print()
