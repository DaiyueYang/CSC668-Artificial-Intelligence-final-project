import os
import sys
import unittest

SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from data_generator import generate_attractions, generate_travel_time_matrix
from planner import (
    TripConstraints,
    check_feasibility,
    plan_itinerary,
    plan_itinerary_beam_search,
    time_to_min,
    REASON_OVER_BUDGET,
    REASON_TOO_MUCH_WAITING,
    REASON_CLOSED_BEFORE_VISIT_END,
    REASON_CANNOT_RETURN_TO_HOTEL,
)
from evaluator import validate_itinerary, evaluate_itinerary
from scenarios import get_scenario


EXPECTED_COLUMNS = [
    "attraction_id", "name", "category", "x", "y",
    "cost", "visit_duration", "opening_time", "closing_time", "priority_score",
]


class TestDataGeneration(unittest.TestCase):
    def test_attractions_have_expected_columns(self):
        df = generate_attractions(n=15, seed=1)
        self.assertEqual(list(df.columns), EXPECTED_COLUMNS)
        self.assertEqual(len(df), 15)

    def test_attractions_are_reproducible(self):
        a = generate_attractions(n=10, seed=42)
        b = generate_attractions(n=10, seed=42)
        self.assertTrue(a.equals(b))

    def test_travel_matrix_is_symmetric_with_hotel(self):
        attractions = generate_attractions(n=8, seed=42)
        m = generate_travel_time_matrix(attractions)
        self.assertEqual(m.shape, (9, 9))
        self.assertEqual(m.index[0], "hotel")
        self.assertEqual(m.columns[0], "hotel")
        self.assertTrue((m.values == m.values.T).all())
        for i in range(len(m)):
            self.assertEqual(m.iloc[i, i], 0.0)


class TestFeasibility(unittest.TestCase):
    def setUp(self):
        self.attractions = generate_attractions(n=30, seed=42)
        self.travel = generate_travel_time_matrix(self.attractions)
        self.constraints = TripConstraints(budget=200, num_days=3)

    def test_over_budget(self):
        row = self.attractions.iloc[0]
        r = check_feasibility(
            time_to_min("09:00"), "hotel", row,
            self.travel, remaining_budget=5, constraints=self.constraints,
        )
        self.assertFalse(r.feasible)
        self.assertEqual(r.reason, REASON_OVER_BUDGET)

    def test_too_much_waiting(self):
        row = self.attractions.iloc[0]
        r = check_feasibility(
            time_to_min("05:00"), "hotel", row,
            self.travel, remaining_budget=200, constraints=self.constraints,
        )
        self.assertFalse(r.feasible)
        self.assertEqual(r.reason, REASON_TOO_MUCH_WAITING)

    def test_closed_before_visit_end(self):
        row = self.attractions.iloc[25]
        r = check_feasibility(
            time_to_min("15:50"), "hotel", row,
            self.travel, remaining_budget=200, constraints=self.constraints,
        )
        self.assertFalse(r.feasible)
        self.assertEqual(r.reason, REASON_CLOSED_BEFORE_VISIT_END)

    def test_cannot_return_to_hotel(self):
        row = self.attractions.iloc[0]
        r = check_feasibility(
            time_to_min("17:30"), "hotel", row,
            self.travel, remaining_budget=200, constraints=self.constraints,
        )
        self.assertFalse(r.feasible)
        self.assertEqual(r.reason, REASON_CANNOT_RETURN_TO_HOTEL)

    def test_feasible_candidate_has_timing(self):
        row = self.attractions.iloc[15]
        r = check_feasibility(
            time_to_min("09:00"), "hotel", row,
            self.travel, remaining_budget=200, constraints=self.constraints,
        )
        self.assertTrue(r.feasible)
        self.assertGreater(r.visit_end, r.visit_start)


class TestPlanners(unittest.TestCase):
    def _run(self, plan_fn, **extra):
        scen = get_scenario("standard")
        attractions = generate_attractions(n=scen.num_attractions, seed=scen.seed)
        travel = generate_travel_time_matrix(attractions)
        constraints = TripConstraints(
            budget=scen.budget, num_days=scen.num_days,
            day_start=scen.day_start, day_end=scen.day_end,
        )
        itinerary = plan_fn(
            attractions, travel,
            budget=scen.budget, num_days=scen.num_days,
            day_start=scen.day_start, day_end=scen.day_end,
            **extra,
        )
        return itinerary, attractions, travel, constraints

    def test_greedy_output_shape_and_feasibility(self):
        itinerary, a, t, c = self._run(plan_itinerary)
        self.assertIsInstance(itinerary, list)
        self.assertEqual(len(itinerary), c.num_days)
        for day in itinerary:
            self.assertIsInstance(day, list)
            for visit in day:
                for key in ("attraction_id", "name", "category", "cost",
                            "duration", "priority_score",
                            "travel", "arrive", "visit_start", "visit_end", "wait"):
                    self.assertIn(key, visit)
        is_feasible, violations = validate_itinerary(itinerary, a, t, c)
        self.assertTrue(is_feasible, f"greedy produced violations: {violations}")

    def test_beam_output_shape_and_feasibility(self):
        itinerary, a, t, c = self._run(plan_itinerary_beam_search, beam_width=5)
        self.assertEqual(len(itinerary), c.num_days)
        is_feasible, violations = validate_itinerary(itinerary, a, t, c)
        self.assertTrue(is_feasible, f"beam produced violations: {violations}")

    def test_evaluate_has_required_metrics(self):
        itinerary, a, t, c = self._run(plan_itinerary_beam_search, beam_width=5)
        m = evaluate_itinerary(itinerary, a, t, c, runtime_seconds=0.1)
        for key in ("feasible", "num_violations", "attractions_visited",
                    "total_cost", "remaining_budget", "total_satisfaction",
                    "total_visit_minutes", "total_travel_minutes",
                    "travel_ratio", "category_diversity", "daily_balance",
                    "runtime_seconds"):
            self.assertIn(key, m)
        self.assertTrue(m["feasible"])


if __name__ == "__main__":
    unittest.main()
