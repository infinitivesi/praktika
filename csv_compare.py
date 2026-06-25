from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from src.csv_compare_tool import compare_csv_files, format_report, save_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Інструмент порівняння CSV-файлів з формуванням звіту."
    )
    parser.add_argument("first_csv", help="Шлях до першого CSV-файлу")
    parser.add_argument("second_csv", help="Шлях до другого CSV-файлу")
    parser.add_argument(
        "-o",
        "--output",
        default="csv_diff_report.txt",
        help="Файл, у який буде збережено звіт",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    first_csv = Path(args.first_csv)
    second_csv = Path(args.second_csv)
    output_path = Path(args.output)

    report = compare_csv_files(first_csv, second_csv)
    text = format_report(report, first_csv, second_csv)
    print(text)
    save_report(output_path, text)
    print(f"\nЗвіт збережено у: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
