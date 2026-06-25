from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class CsvDiffReport:
    headers: list[str]
    key_column: str
    only_first: list[dict[str, str]]
    only_second: list[dict[str, str]]
    changed: list[dict[str, Any]]


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames or []
        rows = [dict(row) for row in reader]
    return headers, rows


def row_key(row: dict[str, str], key_column: str) -> str:
    return row.get(key_column, "").strip()


def compare_csv_files(first_csv: Path, second_csv: Path) -> CsvDiffReport:
    headers_first, rows_first = read_csv_rows(first_csv)
    headers_second, rows_second = read_csv_rows(second_csv)

    if not headers_first or not headers_second:
        raise ValueError("CSV-файли повинні містити заголовки.")
    if headers_first != headers_second:
        raise ValueError("CSV-файли повинні мати однакову структуру (однакові заголовки).")

    headers = headers_first
    key_column = headers[0]

    index_first: dict[str, dict[str, str]] = {}
    for row in rows_first:
        key = row_key(row, key_column)
        if not key:
            raise ValueError(f"Порожнє значення ключа у першому файлі для колонки '{key_column}'.")
        if key in index_first:
            raise ValueError(f"Дубльований ключ '{key}' у першому файлі.")
        index_first[key] = row

    index_second: dict[str, dict[str, str]] = {}
    for row in rows_second:
        key = row_key(row, key_column)
        if not key:
            raise ValueError(f"Порожнє значення ключа у другому файлі для колонки '{key_column}'.")
        if key in index_second:
            raise ValueError(f"Дубльований ключ '{key}' у другому файлі.")
        index_second[key] = row

    only_first = [row for key, row in index_first.items() if key not in index_second]
    only_second = [row for key, row in index_second.items() if key not in index_first]

    changed: list[dict[str, Any]] = []
    common_keys = [key for key in index_first if key in index_second]
    for key in common_keys:
        row_a = index_first[key]
        row_b = index_second[key]
        differences = {
            column: {"first": row_a.get(column, ""), "second": row_b.get(column, "")}
            for column in headers[1:]
            if row_a.get(column, "") != row_b.get(column, "")
        }
        if differences:
            changed.append({"key": key, "differences": differences})

    return CsvDiffReport(
        headers=headers,
        key_column=key_column,
        only_first=only_first,
        only_second=only_second,
        changed=changed,
    )


def format_row(row: dict[str, str], headers: list[str]) -> str:
    return " | ".join(f"{header}={row.get(header, '')}" for header in headers)


def format_report(report: CsvDiffReport, first_csv: Path, second_csv: Path) -> str:
    lines: list[str] = []
    lines.append("CSV COMPARISON REPORT")
    lines.append(f"First file:  {first_csv}")
    lines.append(f"Second file: {second_csv}")
    lines.append(f"Columns: {', '.join(report.headers)}")
    lines.append(f"Row key column: {report.key_column}")
    lines.append("")
    lines.append(f"Only in first file: {len(report.only_first)}")
    for row in report.only_first:
        lines.append(f"  + {format_row(row, report.headers)}")
    lines.append("")
    lines.append(f"Only in second file: {len(report.only_second)}")
    for row in report.only_second:
        lines.append(f"  - {format_row(row, report.headers)}")
    lines.append("")
    lines.append(f"Changed rows: {len(report.changed)}")
    for item in report.changed:
        lines.append(f"  * Key: {item['key']}")
        for column, values in item["differences"].items():
            lines.append(f"      {column}: first={values['first']} | second={values['second']}")
    return "\n".join(lines)


def save_report(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
