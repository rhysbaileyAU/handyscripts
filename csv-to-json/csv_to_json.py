#!/usr/bin/env python3
"""
CSV to JSON Converter

Converts a CSV file to JSON format with a specified column as the key.
Each row becomes a dictionary entry where the key column value maps to
a dictionary of all other columns.

Usage:
    python csv_to_json.py <input_csv> <output_json> <key_column>

Example:
    python csv_to_json.py data.csv output.json "DEVICE NAME"
    python csv_to_json.py data.csv output.json SERIAL
"""

import csv
import json
import sys
from pathlib import Path


def csv_to_json(input_file, output_file, key_column):
    """
    Convert CSV to JSON with specified key column.

    Args:
        input_file: Path to input CSV file
        output_file: Path to output JSON file
        key_column: Column name to use as the key in the JSON object
    """
    result = {}

    try:
        with open(input_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Verify key column exists
            if reader.fieldnames and key_column not in reader.fieldnames:
                print(f"Error: Column '{key_column}' not found in CSV.")
                print(f"Available columns: {', '.join(reader.fieldnames)}")
                sys.exit(1)

            for row in reader:
                # Extract the key value
                key_value = row.get(key_column)

                if not key_value:
                    print(f"Warning: Skipping row with empty key value")
                    continue

                # Create dictionary with all other columns
                row_dict = {k: v for k, v in row.items() if k != key_column}

                # Check for duplicate keys
                if key_value in result:
                    print(f"Warning: Duplicate key '{key_value}' found. Overwriting previous entry.")

                result[key_value] = row_dict

        # Write JSON output
        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(result, jsonfile, indent=2, ensure_ascii=False)

        print(f"Success! Converted {len(result)} rows from {input_file} to {output_file}")
        print(f"Using '{key_column}' as key column")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    input_csv = sys.argv[1]
    output_json = sys.argv[2]
    key_column = sys.argv[3]

    csv_to_json(input_csv, output_json, key_column)


if __name__ == "__main__":
    main()
