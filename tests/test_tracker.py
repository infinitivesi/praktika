from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from src.storage import load_records, save_records
from src.tracker import add_record, best_result, list_records, sport_dynamics


class TrackerTests(unittest.TestCase):
    def test_add_and_list_records(self) -> None:
        records: list[dict] = []
        add_record(records, "Біг", date(2026, 6, 1), 12.5, "сек")
        add_record(records, "Плавання", date(2026, 6, 2), 45.0, "сек")

        ordered = list_records(records)
        self.assertEqual(ordered[0]["sport"], "Біг")
        self.assertEqual(ordered[1]["sport"], "Плавання")

    def test_best_result(self) -> None:
        records: list[dict] = []
        add_record(records, "Жим лежачи", date(2026, 6, 1), 80, "кг")
        add_record(records, "Жим лежачи", date(2026, 6, 2), 95, "кг")

        record = best_result(records, "Жим лежачи")
        self.assertIsNotNone(record)
        self.assertEqual(record["value"], 95)

    def test_sport_dynamics(self) -> None:
        records: list[dict] = []
        add_record(records, "Підтягування", date(2026, 6, 1), 10, "рази")
        add_record(records, "Підтягування", date(2026, 6, 2), 12, "рази")

        dynamics = sport_dynamics(records, "Підтягування")
        self.assertEqual(len(dynamics), 2)
        self.assertIsNone(dynamics[0]["delta"])
        self.assertEqual(dynamics[1]["delta"], 2)

    def test_storage_roundtrip(self) -> None:
        records = [{"sport": "Біг", "date": "2026-06-01", "value": 12.5, "unit": "сек"}]
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "results.json"
            save_records(file_path, records)
            loaded = load_records(file_path)

        self.assertEqual(loaded, records)


if __name__ == "__main__":
    unittest.main()
