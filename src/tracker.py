from __future__ import annotations

from datetime import date
from typing import Any


def add_record(
    records: list[dict[str, Any]],
    sport: str,
    result_date: date,
    value: float,
    unit: str,
) -> dict[str, Any]:
    record = {
        "sport": sport.strip(),
        "date": result_date.isoformat(),
        "value": value,
        "unit": unit.strip(),
    }
    records.append(record)
    return record


def list_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(records, key=lambda x: (x.get("sport", ""), x.get("date", "")))


def sport_dynamics(records: list[dict[str, Any]], sport: str) -> list[dict[str, Any]]:
    sport_clean = sport.strip().lower()
    filtered = [
        r
        for r in records
        if isinstance(r.get("sport"), str) and r["sport"].strip().lower() == sport_clean
    ]

    filtered.sort(key=lambda x: x.get("date", ""))

    result: list[dict[str, Any]] = []
    prev_value: float | None = None

    for item in filtered:
        current_value = float(item.get("value", 0))
        delta = None if prev_value is None else current_value - prev_value
        result.append({"record": item, "delta": delta})
        prev_value = current_value

    return result


def best_result(records: list[dict[str, Any]], sport: str) -> dict[str, Any] | None:
    sport_clean = sport.strip().lower()
    filtered = [
        r
        for r in records
        if isinstance(r.get("sport"), str) and r["sport"].strip().lower() == sport_clean
    ]

    if not filtered:
        return None

    return max(filtered, key=lambda x: float(x.get("value", 0)))
