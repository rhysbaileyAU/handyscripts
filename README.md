# handyscripts
Collection of handy scripts - mostly for data processing and conversion between data structures.

## CSV-to-JSON ##
Pretty self explanatory.  Converts a CSV file to single depth JSON - prompts for which column to use as index.

## CSV-to-MD ##
Converts Data in CSV file to a Markdown Table.

## CSVgrep ##
grep/fgrep functionality when reading CSV files at the CLI.  Allows String/regex matching on rows, while also allowing filtering column view based on column number.

## markdown2pdf ##
Wrapper for converting markdown file to PDF using pandoc.  Not perfect, but OK for exporting MD content for sharing with others.

## trim-csv ##
Removes empty columns from a CSV file and saves output as <csvfilename>-trimmed.csv.  Handy when paired with CSV-to-MD.
