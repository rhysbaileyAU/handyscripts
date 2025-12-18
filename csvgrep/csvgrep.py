#!/usr/bin/env python3
"""
CSV Grep - A grep-like tool for CSV files with column filtering support.

Usage:
    csvgrep.py [OPTIONS] PATTERN FILE

Options:
    -c, --columns COLS      Comma-separated column numbers to display (1-indexed)
                           Example: -c 1,3,5 or --columns 1-3,5
    -i, --ignore-case      Case-insensitive pattern matching
    -F, --fixed-strings    Interpret pattern as fixed string, not regex (like fgrep)
    -v, --invert-match     Invert match (show non-matching rows)
    -n, --line-number      Show line numbers
    -H, --with-header      Always show header row
    --no-header            Don't show header row even if it matches
    -d, --delimiter DELIM  CSV delimiter (default: auto-detect, fallback to comma)
    -h, --help             Show this help message

Examples:
    # Find rows containing "melbourne" and show columns 1, 2, and 5
    csvgrep.py -c 1,2,5 -i melbourne data.csv

    # Find rows containing "error" with line numbers
    csvgrep.py -n error logfile.csv

    # Find rows with exact string match (no regex interpretation)
    csvgrep.py -F "192.168.1.1" data.csv

    # Show only columns 1-3 and 6 from all rows (use empty pattern)
    csvgrep.py -c 1-3,6 "" data.csv

    # Invert match - show rows NOT containing "test"
    csvgrep.py -v test data.csv
"""

import csv
import re
import sys
import argparse
from typing import List, Set, TextIO


def parse_column_spec(spec: str, max_cols: int) -> Set[int]:
    """
    Parse column specification into a set of 0-indexed column numbers.

    Examples:
        "1,3,5" -> {0, 2, 4}
        "1-3,5" -> {0, 1, 2, 4}
        "1-3,5-7" -> {0, 1, 2, 4, 5, 6}
    """
    columns = set()

    for part in spec.split(','):
        part = part.strip()
        if '-' in part:
            # Range specification
            start, end = part.split('-', 1)
            start_idx = int(start) - 1
            end_idx = int(end) - 1

            if start_idx < 0 or end_idx >= max_cols:
                print(f"Warning: Column range {part} out of bounds (max: {max_cols})",
                      file=sys.stderr)

            for i in range(start_idx, end_idx + 1):
                if 0 <= i < max_cols:
                    columns.add(i)
        else:
            # Single column
            col_idx = int(part) - 1
            if col_idx < 0 or col_idx >= max_cols:
                print(f"Warning: Column {part} out of bounds (max: {max_cols})",
                      file=sys.stderr)
            else:
                columns.add(col_idx)

    return columns


def filter_columns(row: List[str], columns: Set[int]) -> List[str]:
    """Filter row to only include specified columns."""
    if not columns:
        return row

    return [row[i] for i in sorted(columns) if i < len(row)]


def detect_delimiter(file_path: str) -> str:
    """Detect the CSV delimiter by reading the first few lines."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sample = f.read(4096)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            return delimiter
    except:
        return ','


def csvgrep(
    file_path: str,
    pattern: str,
    columns: str = None,
    ignore_case: bool = False,
    fixed_strings: bool = False,
    invert_match: bool = False,
    show_line_numbers: bool = False,
    with_header: bool = False,
    no_header: bool = False,
    delimiter: str = None
):
    """
    Grep-like search through CSV file with column filtering.
    """
    # Detect delimiter if not specified
    if delimiter is None:
        delimiter = detect_delimiter(file_path)

    # Compile regex pattern or prepare fixed string search
    regex = None
    search_string = None

    if pattern:
        if fixed_strings:
            # Fixed string matching (like fgrep)
            search_string = pattern.lower() if ignore_case else pattern
        else:
            # Regex matching
            flags = re.IGNORECASE if ignore_case else 0
            try:
                regex = re.compile(pattern, flags)
            except re.error as e:
                print(f"Error: Invalid regex pattern: {e}", file=sys.stderr)
                sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=delimiter)

            # Read all rows first to determine column count
            rows = list(reader)
            if not rows:
                return

            # Determine max columns
            max_cols = max(len(row) for row in rows)

            # Parse column specification
            col_filter = None
            if columns:
                try:
                    col_filter = parse_column_spec(columns, max_cols)
                except ValueError as e:
                    print(f"Error: Invalid column specification: {e}", file=sys.stderr)
                    sys.exit(1)

            # Process rows
            for line_num, row in enumerate(rows, 1):
                is_header = (line_num == 1)

                # Handle header row
                if is_header:
                    if with_header or (not no_header and not pattern):
                        output_row = filter_columns(row, col_filter)
                        if show_line_numbers:
                            print(f"{line_num}:", end="")
                        print(delimiter.join(output_row))
                    elif no_header:
                        continue
                    else:
                        # Check if header matches pattern
                        row_text = delimiter.join(row)
                        if fixed_strings and search_string:
                            # Fixed string matching
                            row_to_search = row_text.lower() if ignore_case else row_text
                            matches = search_string in row_to_search
                        else:
                            # Regex matching
                            matches = regex.search(row_text) if regex else True

                        if (matches and not invert_match) or (not matches and invert_match):
                            output_row = filter_columns(row, col_filter)
                            if show_line_numbers:
                                print(f"{line_num}:", end="")
                            print(delimiter.join(output_row))
                    continue

                # Check if row matches pattern
                row_text = delimiter.join(row)
                if fixed_strings and search_string:
                    # Fixed string matching
                    row_to_search = row_text.lower() if ignore_case else row_text
                    matches = search_string in row_to_search
                else:
                    # Regex matching
                    matches = regex.search(row_text) if regex else True

                if (matches and not invert_match) or (not matches and invert_match):
                    output_row = filter_columns(row, col_filter)
                    if show_line_numbers:
                        print(f"{line_num}:", end="")
                    print(delimiter.join(output_row))

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='CSV Grep - A grep-like tool for CSV files with column filtering',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -c 1,2,5 -i melbourne data.csv
  %(prog)s -n error logfile.csv
  %(prog)s -F "192.168.1.1" data.csv
  %(prog)s -c 1-3,6 "" data.csv
  %(prog)s -v test data.csv
        """
    )

    parser.add_argument('pattern',
                       help='Regular expression pattern to search for (use "" to match all rows)')
    parser.add_argument('file',
                       help='CSV file to search')
    parser.add_argument('-c', '--columns',
                       help='Comma-separated column numbers to display (1-indexed, e.g., 1,3,5 or 1-3,5)')
    parser.add_argument('-i', '--ignore-case',
                       action='store_true',
                       help='Case-insensitive pattern matching')
    parser.add_argument('-F', '--fixed-strings',
                       action='store_true',
                       help='Interpret pattern as fixed string, not regex (like fgrep)')
    parser.add_argument('-v', '--invert-match',
                       action='store_true',
                       help='Invert match (show non-matching rows)')
    parser.add_argument('-n', '--line-number',
                       action='store_true',
                       help='Show line numbers')
    parser.add_argument('-H', '--with-header',
                       action='store_true',
                       help='Always show header row')
    parser.add_argument('--no-header',
                       action='store_true',
                       help="Don't show header row even if it matches")
    parser.add_argument('-d', '--delimiter',
                       help='CSV delimiter (default: auto-detect)')

    args = parser.parse_args()

    csvgrep(
        file_path=args.file,
        pattern=args.pattern,
        columns=args.columns,
        ignore_case=args.ignore_case,
        fixed_strings=args.fixed_strings,
        invert_match=args.invert_match,
        show_line_numbers=args.line_number,
        with_header=args.with_header,
        no_header=args.no_header,
        delimiter=args.delimiter
    )


if __name__ == '__main__':
    main()
