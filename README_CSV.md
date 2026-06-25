# CSV Comparison Tool

Console utility for comparing two CSV files with the same structure.

## Features

- Reads two CSV files with identical headers.
- Uses the first column as the row key.
- Finds rows that exist only in the first file.
- Finds rows that exist only in the second file.
- Finds changed rows for matching keys.
- Prints a detailed report to the console.
- Saves the report to a text file.

## Run

```bash
python csv_compare.py first.csv second.csv -o report.txt
```

## Notes

- CSV files must use the same column structure.
- The comparison uses all columns as the row key.
- Text output is saved in UTF-8 encoding.
