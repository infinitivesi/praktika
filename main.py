from __future__ import annotations

import os
import random
from datetime import datetime
from datetime import timedelta
from pathlib import Path

from src.storage import load_records, save_records
from src.tracker import add_record, best_result, list_records, sport_dynamics

DATA_FILE = Path("data") / "results.json"
DEFAULT_SPORTS = [
    "Біг 100м",
    "Підтягування",
    "Присідання",
    "Велосипед",
    "Жим лежачи",
    "Плавання",
    "Планка",
    "Стрибки на скакалці",
]


def setup_console() -> None:
    if os.name == "nt":
        os.system("chcp 65001 > nul")


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pause() -> None:
    input("\nНатисніть Enter, щоб продовжити...")


def print_header(title: str) -> None:
    print("=" * 62)
    print(title.center(62))
    print("=" * 62)


def print_table_border(sport_width: int, result_width: int) -> None:
    print(f"+----+{'-' * (sport_width + 2)}+------------+{'-' * (result_width + 2)}+")


def print_results_table(records: list[dict], title: str, include_index: bool = False) -> None:
    print_header(title)
    if not records:
        print("Поки що немає жодного запису.")
        return

    sport_width = min(
        max(len("Вид спорту"), max(len(str(record.get("sport", ""))) for record in records)),
        24,
    )
    result_width = min(
        max(
            len("Результат"),
            max(len(f"{record.get('value', '')} {record.get('unit', '')}") for record in records),
        ),
        14,
    )

    print(f"Записів: {len(records)}")
    print_table_border(sport_width, result_width)
    print(f"| №  | {'Вид спорту':<{sport_width}} | Дата       | {'Результат':<{result_width}} |")
    print(f"+----+{'-' * (sport_width + 2)}+------------+{'-' * (result_width + 2)}+")
    for index, record in enumerate(records, start=1):
        number = f"{index:>2}" if include_index else "  "
        sport = str(record.get("sport", "?"))[:sport_width]
        date_value = str(record.get("date", "?"))[:10]
        result_value = f"{record.get('value', '?')} {record.get('unit', '')}"[:result_width]
        print(
            f"| {number} | {sport:<{sport_width}} | {date_value:<10} | {result_value:>{result_width}} |"
        )
    print(f"+----+{'-' * (sport_width + 2)}+------------+{'-' * (result_width + 2)}+")


def show_intro() -> None:
    clear_screen()
    print_header("ІНФОРМАЦІЯ ПРО ПРОГРАМУ")
    print("Технічне завдання:")
    print("- Програма веде облік спортивних результатів користувача.")
    print("- Реалізовані функції:")
    print("  1) додавання результату;")
    print("  2) перегляд усіх результатів;")
    print("  3) перегляд динаміки за видом спорту;")
    print("  4) пошук найкращого результату;")
    print("  5) генерація випадкових тестових результатів.")
    print("  6) видалення непотрібного результату.")
    print("  7) видалення всіх результатів одразу.")
    print("- Дані зберігаються у форматі JSON у файлі data/results.json.")
    print()
    print("Use case діаграма:")
    print("           +-----------------------------+")
    print("           |     Трекер результатів      |")
    print("           +-----------------------------+")
    print("Користувач --> (Додати результат)")
    print("Користувач --> (Переглянути всі результати)")
    print("Користувач --> (Переглянути динаміку)")
    print("Користувач --> (Показати найкращий результат)")
    print("Користувач --> (Згенерувати випадкові результати)")
    print("Користувач --> (Видалити результат)")
    print("Користувач --> (Видалити всі результати)")
    print("Програма була створена Шавиріном Ярославом, група ІПЗ-21")
    pause()


def read_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Поле не може бути порожнім. Спробуйте ще раз.")


def read_date(prompt: str):
    while True:
        raw = input(prompt).strip()
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            print("Невірний формат дати. Використовуйте YYYY-MM-DD.")


def read_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            print("Результат має бути числом. Спробуйте ще раз.")


def read_int_in_range(prompt: str, min_value: int, max_value: int) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Потрібно ввести ціле число.")
            continue

        if min_value <= value <= max_value:
            return value

        print(f"Введіть число від {min_value} до {max_value}.")


def get_available_sports(records: list[dict]) -> list[str]:
    sports = {
        str(record.get("sport", "")).strip()
        for record in records
        if str(record.get("sport", "")).strip()
    }
    combined = sorted(sports.union(DEFAULT_SPORTS), key=lambda item: item.lower())
    return combined


def choose_sport(records: list[dict], prompt: str) -> str:
    available_sports = get_available_sports(records)
    if not available_sports:
        return read_non_empty("Введіть вид спорту вручну: ")

    while True:
        clear_screen()
        print_header("ДОСТУПНІ ВИДИ СПОРТУ")
        for index, sport in enumerate(available_sports, start=1):
            print(f"{index}. {sport}")
        print("0. Ввести назву вручну")
        print("-" * 62)

        choice = read_int_in_range(prompt, 0, max(1, len(available_sports)))
        if choice == 0:
            return read_non_empty("Введіть вид спорту вручну: ")

        return available_sports[choice - 1]


def print_record(record: dict) -> None:
    print(
        f"{record.get('sport', '?'):<20} | {record.get('date', '?'):<10} | "
        f"{record.get('value', '?'):>8} {record.get('unit', '')}"
    )


def show_menu() -> None:
    print_header("ТРЕКЕР СПОРТИВНИХ РЕЗУЛЬТАТІВ")
    print("1. Додати результат")
    print("2. Переглянути всі результати")
    print("3. Переглянути динаміку за видом спорту")
    print("4. Показати найкращий результат")
    print("5. Згенерувати випадкові результати")
    print("6. Видалити результат")
    print("7. Видалити усі результати")
    print("8. Вихід")
    print("-" * 62)


def generate_random_results(records: list[dict], count: int) -> list[dict]:
    sports = [
        {"sport": "Біг 100м", "unit": "сек", "low": 10.0, "high": 18.5, "mode": 12.8},
        {"sport": "Підтягування", "unit": "рази", "low": 3.0, "high": 35.0, "mode": 14.0},
        {"sport": "Присідання", "unit": "рази", "low": 10.0, "high": 120.0, "mode": 55.0},
        {"sport": "Велосипед", "unit": "км", "low": 5.0, "high": 120.0, "mode": 42.0},
        {"sport": "Жим лежачи", "unit": "кг", "low": 20.0, "high": 180.0, "mode": 90.0},
        {"sport": "Плавання 50м", "unit": "сек", "low": 25.0, "high": 120.0, "mode": 48.0},
        {"sport": "Планка", "unit": "сек", "low": 20.0, "high": 600.0, "mode": 180.0},
        {"sport": "Стрибки на скакалці", "unit": "рази", "low": 20.0, "high": 400.0, "mode": 160.0},
        {"sport": "Стрибки вперед", "unit": "м", "low": 20.0, "high": 400.0, "mode": 160.0},
        {"sport": "Віджимання", "unit": "рази", "low": 5.0, "high": 60.0, "mode": 25.0},
    ]

    created: list[dict] = []
    today = datetime.now().date()
    for _ in range(count):
        profile = random.choice(sports)
        days_ago = random.randint(0, 120)
        random_date = today - timedelta(days=days_ago)
        value = random.triangular(
            float(profile["low"]),
            float(profile["high"]),
            float(profile["mode"]),
        )
        if profile["unit"] == "рази":
            value = int(round(value))
        else:
            value = round(value, 2)

        created.append(add_record(records, profile["sport"], random_date, value, profile["unit"]))

    return created


def delete_result(records: list[dict]) -> bool:
    sorted_records = list_records(records)
    clear_screen()
    print_results_table(sorted_records, "ВИДАЛЕННЯ РЕЗУЛЬТАТУ", include_index=True)
    if not sorted_records:
        pause()
        return False

    print("0. Скасувати")
    print("-" * 62)
    choice = read_int_in_range(f"Оберіть номер запису для видалення (0-{len(sorted_records)}): ", 0, len(sorted_records))
    if choice == 0:
        print("Видалення скасовано.")
        pause()
        return False

    record_to_delete = sorted_records[choice - 1]
    records.remove(record_to_delete)
    save_records(DATA_FILE, records)
    print("Запис видалено успішно.")
    pause()
    return True


def delete_all_results(records: list[dict]) -> bool:
    clear_screen()
    print_header("ПОВНЕ ОЧИЩЕННЯ РЕЗУЛЬТАТІВ")
    if not records:
        print("Список уже порожній.")
        pause()
        return False

    print(f"У списку зараз {len(records)} записів.")
    confirmation = read_non_empty("Введіть ТАК, щоб видалити всі результати: ").strip().lower()
    if confirmation not in {"так", "так."}:
        print("Очищення скасовано.")
        pause()
        return False

    records.clear()
    save_records(DATA_FILE, records)
    print("Усі результати видалено.")
    pause()
    return True


def main() -> None:
    setup_console()
    records = load_records(DATA_FILE)
    show_intro()

    while True:
        clear_screen()
        show_menu()
        choice = input("Оберіть дію (1-8): ").strip()

        if choice == "1":
            clear_screen()
            print_header("ДОДАВАННЯ РЕЗУЛЬТАТУ")
            sport = read_non_empty("Вид спорту: ")
            result_date = read_date("Дата (YYYY-MM-DD): ")
            value = read_float("Результат (число): ")
            unit = read_non_empty("Одиниця виміру (сек, км, кг, рази...): ")

            record = add_record(records, sport, result_date, value, unit)
            save_records(DATA_FILE, records)
            print("\nЗапис успішно збережено:")
            print_record(record)
            pause()

        elif choice == "2":
            clear_screen()
            sorted_records = list_records(records)
            print_results_table(sorted_records, "УСІ РЕЗУЛЬТАТИ")
            pause()

        elif choice == "3":
            clear_screen()
            print_header("ДИНАМІКА РЕЗУЛЬТАТІВ")
            sport = choose_sport(records, "Оберіть номер виду спорту: ")
            dynamics = sport_dynamics(records, sport)
            if not dynamics:
                print("Для цього виду спорту записів не знайдено.")
                pause()
                continue

            print(f"\nДинаміка для: {sport}")
            print("-" * 62)
            for item in dynamics:
                record = item["record"]
                delta = item["delta"]
                print_record(record)
                if delta is None:
                    print("  Зміна: н/д (перший запис)")
                else:
                    sign = "+" if delta >= 0 else ""
                    print(f"  Зміна: {sign}{delta} {record.get('unit', '')}")
            pause()

        elif choice == "4":
            clear_screen()
            print_header("НАЙКРАЩИЙ РЕЗУЛЬТАТ")
            sport = choose_sport(records, "Оберіть номер виду спорту: ")
            record = best_result(records, sport)
            if record is None:
                print("Для цього виду спорту записів не знайдено.")
            else:
                print("Найкращий результат:")
                print_record(record)
            pause()

        elif choice == "5":
            clear_screen()
            print_header("ГЕНЕРАЦІЯ ВИПАДКОВИХ РЕЗУЛЬТАТІВ")
            count = read_int_in_range("Скільки записів згенерувати (1-15): ", 1, 15)
            created = generate_random_results(records, count)
            save_records(DATA_FILE, records)
            print(f"\nЗгенеровано записів: {len(created)}")
            print("Останні згенеровані записи:")
            print("-" * 62)
            for record in created[-5:]:
                print_record(record)
            pause()

        elif choice == "6":
            delete_result(records)

        elif choice == "7":
            delete_all_results(records)

        elif choice == "8":
            clear_screen()
            print("Дякуємо за використання трекера. До зустрічі!")
            return

        else:
            print("Невідома команда. Введіть число від 1 до 8.")
            pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nРоботу перервано користувачем.")
