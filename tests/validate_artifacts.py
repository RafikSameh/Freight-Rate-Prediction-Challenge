import csv
import json
import math
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ArtifactContractTests(unittest.TestCase):
    def test_executed_notebook_records_leakage_safe_tuning(self):
        path = ROOT / "notebook.ipynb"
        self.assertTrue(path.is_file(), "notebook.ipynb was not created")
        with path.open(encoding="utf-8") as handle:
            notebook = json.load(handle)

        code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
        self.assertTrue(code_cells, "notebook contains no executable cells")
        self.assertTrue(
            all(cell.get("execution_count") is not None for cell in code_cells),
            "notebook must be executed from top to bottom",
        )

        error_outputs = [
            output
            for cell in code_cells
            for output in cell.get("outputs", [])
            if output.get("output_type") == "error"
        ]
        self.assertEqual(error_outputs, [], "executed notebook contains an error")

        stream_text = "\n".join(
            "".join(output.get("text", []))
            for cell in code_cells
            for output in cell.get("outputs", [])
            if output.get("output_type") == "stream"
        )
        self.assertIn("Rolling tuning candidates evaluated:", stream_text)
        self.assertIn("Chronological folds verified: 3", stream_text)
        self.assertIn("Final gate fits used early stopping: False", stream_text)
        self.assertIn("Frozen rolling iterations:", stream_text)
        self.assertIn("Final holdout promotion:", stream_text)

    def test_validation_predictions(self):
        path = ROOT / "validation_predictions.csv"
        self.assertTrue(path.is_file(), "validation_predictions.csv was not created")
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            self.assertEqual(reader.fieldnames, ["load_id", "predicted_rate"])
        self.assertEqual(len(rows), 12_000)
        expected = {f"TE-{number:06d}" for number in range(1, 12_001)}
        self.assertEqual({row["load_id"] for row in rows}, expected)
        rates = [float(row["predicted_rate"]) for row in rows]
        self.assertTrue(all(math.isfinite(value) and value > 0 for value in rates))

    def test_december_predictions(self):
        path = ROOT / "data" / "december_chart_inputs.csv"
        self.assertTrue(path.is_file(), "December predictions were not created")
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            expected_columns = ["pickup", "delivery", "distance", "equipment", "weight", "date", "predicted_rate"]
            self.assertEqual(reader.fieldnames, expected_columns)
        self.assertEqual(len(rows), 31)
        dates = {(date(2025, 12, 1) + timedelta(days=i)).isoformat() for i in range(31)}
        self.assertEqual({row["date"] for row in rows}, dates)
        self.assertTrue(all(row["pickup"] == "Lexington" and row["delivery"] == "Fort Wayne" for row in rows))
        self.assertTrue(all(float(row["distance"]) == 360 and float(row["weight"]) == 32_000 for row in rows))
        self.assertTrue(all(row["equipment"] == "Dry Van" for row in rows))
        rates = [float(row["predicted_rate"]) for row in rows]
        self.assertTrue(all(math.isfinite(value) and value > 0 for value in rates))


if __name__ == "__main__":
    unittest.main()
