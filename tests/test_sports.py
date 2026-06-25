from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from src.storage import load_records, save_records
from src.tracker import add_record, best_result, sport_dynamics


class SportsTests(unittest.TestCase):
    def test_save_and_load_records(self) -> None:
        records: list[dict] = []

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "test_results.json"
            add_record(records, "Біг", date(2026, 6, 25), 12.34, "сек")
            save_records(file_path, records)

            loaded = load_records(file_path)

            self.assertEqual(loaded, records)

    def test_best_result_by_sport(self) -> None:
        records: list[dict] = []

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "test_results.json"
            add_record(records, "Жим лежачи", date(2026, 6, 24), 80, "кг")
            add_record(records, "Жим лежачи", date(2026, 6, 25), 95, "кг")
            save_records(file_path, records)

            loaded = load_records(file_path)
            record = best_result(loaded, "Жим лежачи")

            self.assertIsNotNone(record)
            self.assertEqual(record["value"], 95)

    def test_sport_dynamics(self) -> None:
        records: list[dict] = []

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "test_results.json"
            add_record(records, "Підтягування", date(2026, 6, 23), 10, "рази")
            add_record(records, "Підтягування", date(2026, 6, 24), 12, "рази")
            save_records(file_path, records)

            loaded = load_records(file_path)
            dynamics = sport_dynamics(loaded, "Підтягування")

            self.assertEqual(len(dynamics), 2)
            self.assertIsNone(dynamics[0]["delta"])
            self.assertEqual(dynamics[1]["delta"], 2)


if __name__ == "__main__":
    unittest.main()