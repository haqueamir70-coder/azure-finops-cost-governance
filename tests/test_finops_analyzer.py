import json
import tempfile
import unittest
from pathlib import Path

from scripts.finops_analyzer import aggregate, analyze, load_cost_data, render_markdown


class FinOpsAnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"date": "2026-10-01", "subscription": "sub-a", "service": "Compute", "owner": "team-a", "cost": 60},
            {"date": "2026-10-02", "subscription": "sub-a", "service": "Storage", "owner": "team-a", "cost": 25},
            {"date": "2026-10-02", "subscription": "sub-b", "service": "Compute", "owner": "team-b", "cost": 15},
        ]

    def test_aggregate_sorts_by_cost_descending(self):
        self.assertEqual(aggregate(self.records, "service"), {"Compute": 75.0, "Storage": 25.0})

    def test_budget_below_threshold(self):
        result = analyze(self.records, budget=200, threshold=80)
        self.assertEqual(result["status"], "WITHIN_THRESHOLD")
        self.assertEqual(result["total_cost"], 100.0)
        self.assertEqual(result["budget_utilization_pct"], 50.0)

    def test_threshold_reached(self):
        # 100 spend against a 125 budget is exactly 80%, below the budget cap.
        self.assertEqual(analyze(self.records, 125, 80)["status"], "THRESHOLD_REACHED")

    def test_over_budget(self):
        self.assertEqual(analyze(self.records, 90, 80)["status"], "OVER_BUDGET")

    def test_budget_not_configured(self):
        self.assertEqual(analyze(self.records, 0, 80)["status"], "BUDGET_NOT_CONFIGURED")

    def test_empty_data_is_valid(self):
        result = analyze([], 100, 80)
        self.assertEqual(result["record_count"], 0)
        self.assertEqual(result["status"], "WITHIN_THRESHOLD")

    def test_input_validation(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "cost.json"
            path.write_text(json.dumps({"currency": "USD", "records": [
                {"date": "2026-10-01", "subscription": "s", "service": "x", "owner": "o", "cost": -1}
            ]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "cannot be negative"):
                load_cost_data(path)

    def test_markdown_mentions_limitations(self):
        report = analyze(self.records, 100, 80)
        content = render_markdown(report, "USD")
        self.assertIn("Current cost", content)
        self.assertIn("not savings estimates", content.lower())


if __name__ == "__main__":
    unittest.main()
