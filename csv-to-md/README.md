# CSV to Markdown Table Converter

A Python script that converts CSV files into properly formatted markdown tables.

## Features

- Interactive prompts for easy usage
- Handles CSV files with or without header rows
- Automatic default column naming (C1, C2, C3, etc.) when no header is present
- Completion summary showing conversion statistics
- Automatic output file naming (same base name as input with `.md` extension)

## Requirements

- Python 3.x
- No external dependencies (uses standard library only)

## Usage

### Interactive Mode

Run the script without arguments and follow the prompts:

```bash
python3 csv-to-md.py
```

You'll be prompted to:
1. Enter the path to your CSV file
2. Specify whether the CSV contains a header row (y/n)

### Command Line Mode

Provide the CSV file path as an argument:

```bash
python3 csv-to-md.py path/to/your-file.csv
```

You'll still be prompted whether the file contains a header row.

## Examples

### With Header Row

Input CSV (`data.csv`):
```
Name,Age,City
Alice,30,New York
Bob,25,London
```

Command:
```bash
python3 csv-to-md.py data.csv
# Answer 'y' when asked about header row
```

Output (`data.md`):
```markdown
| Name | Age | City |
| --- | --- | --- |
| Alice | 30 | New York |
| Bob | 25 | London |
```

Summary:
```
Columns converted: 3
Rows converted: 2
Destination file: data.md
```

### Without Header Row

Input CSV (`data.csv`):
```
Alice,30,New York
Bob,25,London
```

Command:
```bash
python3 csv-to-md.py data.csv
# Answer 'n' when asked about header row
```

Output (`data.md`):
```markdown
| C1 | C2 | C3 |
| --- | --- | --- |
| Alice | 30 | New York |
| Bob | 25 | London |
```

Summary:
```
Columns converted: 3
Rows converted: 2
Destination file: data.md
```

## Output

- The markdown file is created in the same directory as the input CSV
- Output filename: `<input-basename>.md`
- The script displays a summary upon completion showing:
  - Number of columns converted
  - Number of data rows converted
  - Full path to the destination file

## Notes

- The script automatically handles rows with varying column counts by padding with empty cells
- UTF-8 encoding is used for both input and output files
- Existing markdown files with the same name will be overwritten
