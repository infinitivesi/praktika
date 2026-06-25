# Sports Results Tracker (Variant 28)

Console utility for tracking sports results with data persistence in JSON.

## Implemented functionality

- Save results with fields: sport type, date, numeric result, unit.
- View all saved results.
- View dynamics for selected sport (difference between consecutive records).
- View best result for selected sport.
- Generate random test results.
- Delete an unnecessary result.
- Robust handling of invalid user input (wrong menu option, invalid date, non-numeric result, empty fields).
- Startup screen includes technical specification and a text use case diagram.

## Project structure

- `main.py` - entry point and CLI menu.
- `src/storage.py` - load/save data to `data/results.json`.
- `src/tracker.py` - core operations for records, dynamics, and best result.

## Run

```bash
python main.py
```

## Data file

Records are stored in:

- `data/results.json`

The file is created automatically on first save.

## Testing

Таблиця тест-кейсів і фактичні результати збережені у [TEST_CASES.md](TEST_CASES.md).
Також додано автоматизовані тести у [tests/test_tracker.py](tests/test_tracker.py).
