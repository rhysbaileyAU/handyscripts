#!/usr/bin/env python3
"""
CSV Column Trimmer

Removes columns from a CSV file where all rows contain empty values.
Creates a new file with '-trimmed' appended to the original filename.

Usage:
    python trim_csv.py <input_file.csv>
"""

import csv
import sys
import os
from pathlib import Path


def generate_output_filename(input_path):
    """
    Generate output filename by appending '-trimmed' before the extension.

    Args:
        input_path: Path to input CSV file

    Returns:
        Path to output CSV file

    Examples:
        'data.csv' -> 'data-trimmed.csv'
        'path/to/file.csv' -> 'path/to/file-trimmed.csv'
        'data.backup.csv' -> 'data.backup-trimmed.csv'
    """
    path = Path(input_path)
    stem = path.stem
    suffix = path.suffix
    parent = path.parent

    output_name = f"{stem}-trimmed{suffix}"
    return parent / output_name


def identify_empty_columns(rows):
    """
    Identify column indices where all values are empty strings.

    Args:
        rows: List of rows (including header), where each row is a list of values

    Returns:
        Set of column indices that are completely empty (in data rows, not header)
    """
    if len(rows) < 2:  # Need at least header + 1 data row
        return set()

    num_columns = len(rows[0])
    empty_columns = set(range(num_columns))

    # Check only data rows (skip header at index 0) for non-empty values
    for row in rows[1:]:
        for col_idx in list(empty_columns):
            if col_idx < len(row) and row[col_idx] != '':
                empty_columns.discard(col_idx)

        # Early exit if no columns are empty
        if not empty_columns:
            break

    return empty_columns


def trim_csv(input_file, output_file):
    """
    Remove empty columns from CSV file.

    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file

    Returns:
        Tuple of (original_column_count, trimmed_column_count, removed_count)
    """
    # Read entire CSV into memory
    rows = []
    with open(input_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        raise ValueError("CSV file is empty")

    original_column_count = len(rows[0]) if rows else 0

    # Identify empty columns
    empty_columns = identify_empty_columns(rows)

    # Create list of column indices to keep
    columns_to_keep = [i for i in range(original_column_count) if i not in empty_columns]

    # Write trimmed CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in rows:
            trimmed_row = [row[i] for i in columns_to_keep if i < len(row)]
            writer.writerow(trimmed_row)

    trimmed_column_count = len(columns_to_keep)
    removed_count = len(empty_columns)

    return original_column_count, trimmed_column_count, removed_count


def main():
    """Main entry point for the script."""
    if len(sys.argv) != 2:
        print("Usage: python trim_csv.py <input_file.csv>")
        print("\nRemoves columns where all rows contain empty values.")
        print("Creates a new file with '-trimmed' appended to the filename.")
        sys.exit(1)

    input_file = sys.argv[1]

    # Validate input file exists
    if not os.path.isfile(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    # Generate output filename
    output_file = generate_output_filename(input_file)

    try:
        # Process the CSV
        original_count, trimmed_count, removed_count = trim_csv(input_file, output_file)

        # Report results
        print(f"CSV trimming complete!")
        print(f"  Input file:  {input_file}")
        print(f"  Output file: {output_file}")
        print(f"  Original columns: {original_count}")
        print(f"  Trimmed columns:  {trimmed_count}")
        print(f"  Removed columns:  {removed_count}")

        if removed_count == 0:
            print("\nNo empty columns found - all columns retained.")

    except FileNotFoundError:
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied accessing files")
        sys.exit(1)
    except csv.Error as e:
        print(f"Error: Invalid CSV format: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
