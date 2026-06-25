from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.csv_compare_tool import compare_csv_files, format_report, save_report


class CsvCompareTests(unittest.TestCase):
    def test_compare_csv_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            first = tmp / "first.csv"
            second = tmp / "second.csv"

            first.write_text(
                "id,name,score\n1,Alice,10\n2,Bob,20\n3,Chris,30\n",
                encoding="utf-8",
            )
            second.write_text(
                "id,name,score\n1,Alice,10\n2,Bob,25\n4,Dora,40\n",
                encoding="utf-8",
            )

            report = compare_csv_files(first, second)
            text = format_report(report, first, second)
            output = tmp / "report.txt"
            save_report(output, text)

            self.assertEqual(len(report.only_first), 1)
            self.assertEqual(len(report.only_second), 1)
            self.assertEqual(len(report.changed), 1)
            self.assertIn("Row key column: id", text)
            self.assertIn("score: first=20 | second=25", text)
            self.assertTrue(output.exists())


if __name__ == "__main__":
    unittest.main()
