#!/usr/bin/env python3
"""
CSV to Markdown Table Converter

Converts a CSV file to a markdown table format with optional header row handling.
"""

import csv
import sys
import os


def convert_csv_to_markdown(csv_file_path, has_header):
    """
    Convert a CSV file to a markdown table.

    Args:
        csv_file_path: Path to the input CSV file
        has_header: Boolean indicating if CSV has a header row

    Returns:
        tuple: (markdown_string, num_columns, num_rows)
    """
    rows = []

    # Read the CSV file
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    if not rows:
        return "", 0, 0

    # Determine number of columns
    num_columns = max(len(row) for row in rows) if rows else 0
    num_rows = len(rows)

    # Pad rows to ensure consistent column count
    for row in rows:
        while len(row) < num_columns:
            row.append('')

    markdown_lines = []

    if has_header:
        # Use first row as header
        header = rows[0]
        data_rows = rows[1:]
        num_data_rows = len(data_rows)
    else:
        # Create default header
        header = [f'C{i+1}' for i in range(num_columns)]
        data_rows = rows
        num_data_rows = len(data_rows)

    # Build markdown table
    # Header row
    markdown_lines.append('| ' + ' | '.join(header) + ' |')

    # Separator row
    markdown_lines.append('| ' + ' | '.join(['---'] * num_columns) + ' |')

    # Data rows
    for row in data_rows:
        markdown_lines.append('| ' + ' | '.join(row) + ' |')

    return '\n'.join(markdown_lines), num_columns, num_data_rows


def main():
    # Get CSV file path
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = input("Enter the path to the CSV file: ").strip()

    # Validate file exists
    if not os.path.isfile(csv_file):
        print(f"Error: File '{csv_file}' not found.")
        sys.exit(1)

    # Ask if CSV has header row
    while True:
        response = input("Does the CSV file contain a header row? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            has_header = True
            break
        elif response in ['n', 'no']:
            has_header = False
            break
        else:
            print("Please enter 'y' or 'n'")

    # Convert CSV to markdown
    try:
        markdown_content, num_columns, num_rows = convert_csv_to_markdown(csv_file, has_header)

        # Generate output filename
        base_name = os.path.splitext(csv_file)[0]
        output_file = f"{base_name}.md"

        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # Print summary
        print("\n" + "="*50)
        print("Conversion Complete!")
        print("="*50)
        print(f"Columns converted: {num_columns}")
        print(f"Rows converted: {num_rows}")
        print(f"Destination file: {output_file}")
        print("="*50)

    except Exception as e:
        print(f"Error converting file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
