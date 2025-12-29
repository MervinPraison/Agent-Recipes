# AI CSV Cleaner

Clean CSV files by removing duplicates, fixing nulls, and standardizing formats.

## Usage
```bash
praison run ai-csv-cleaner data.csv
praison run ai-csv-cleaner data.csv --drop-duplicates --fill-nulls mean
```

## Output
- `cleaned.csv` - Cleaned data
- `cleaning-report.json` - Changes made
