## CSV Grep - A grep-like tool for CSV files with column filtering support. ##

```
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
```
