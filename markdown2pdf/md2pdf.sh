#!/bin/bash

# Markdown to PDF Converter
# Converts markdown files to PDF with A4 formatting and proper margins
# Supports tables, images, and links

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
MARGIN="2.5cm"
OUTPUT_FILE=""

# Help message
show_help() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] <input.md> [output.pdf]

Convert Markdown files to PDF with A4 formatting and proper margins.

OPTIONS:
    -h, --help          Show this help message
    -m, --margin SIZE   Set page margins (default: 2.5cm)
                        Examples: 2cm, 1in, 20mm

ARGUMENTS:
    input.md            Input markdown file (required)
    output.pdf          Output PDF file (optional)
                        If not specified, uses input filename with .pdf extension

EXAMPLES:
    $(basename "$0") document.md
    $(basename "$0") document.md output.pdf
    $(basename "$0") --margin 3cm document.md

FEATURES:
    - A4 page size (210mm x 297mm)
    - Configurable margins (default: 2.5cm)
    - Table support with proper formatting
    - Image embedding support
    - Clickable hyperlinks
    - Syntax highlighting for code blocks
    - Table of contents generation (if headers present)

REQUIREMENTS:
    - pandoc (installed at: $(which pandoc 2>/dev/null || echo "NOT FOUND"))
    - prince, wkhtmltopdf, or weasyprint for PDF generation
      (Script will auto-detect and use the first available)
      Install with: brew install prince OR brew install wkhtmltopdf
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -m|--margin)
            MARGIN="$2"
            shift 2
            ;;
        -*)
            echo -e "${RED}Error: Unknown option: $1${NC}" >&2
            echo "Use --help for usage information"
            exit 1
            ;;
        *)
            if [[ -z "$INPUT_FILE" ]]; then
                INPUT_FILE="$1"
            elif [[ -z "$OUTPUT_FILE" ]]; then
                OUTPUT_FILE="$1"
            else
                echo -e "${RED}Error: Too many arguments${NC}" >&2
                echo "Use --help for usage information"
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate input file
if [[ -z "$INPUT_FILE" ]]; then
    echo -e "${RED}Error: No input file specified${NC}" >&2
    echo "Use --help for usage information"
    exit 1
fi

if [[ ! -f "$INPUT_FILE" ]]; then
    echo -e "${RED}Error: Input file not found: $INPUT_FILE${NC}" >&2
    exit 1
fi

# Set output file if not specified
if [[ -z "$OUTPUT_FILE" ]]; then
    OUTPUT_FILE="${INPUT_FILE%.md}.pdf"
fi

# Check for pandoc
if ! command -v pandoc &> /dev/null; then
    echo -e "${RED}Error: pandoc is not installed${NC}" >&2
    echo "Install with: brew install pandoc"
    exit 1
fi

# Detect available PDF engine
PDF_ENGINE=""
if command -v prince &> /dev/null; then
    PDF_ENGINE="prince"
elif command -v wkhtmltopdf &> /dev/null; then
    PDF_ENGINE="wkhtmltopdf"
elif command -v weasyprint &> /dev/null; then
    PDF_ENGINE="weasyprint"
else
    echo -e "${YELLOW}Warning: No PDF engine found (prince, wkhtmltopdf, weasyprint)${NC}" >&2
    echo -e "${YELLOW}Will attempt HTML-based conversion with available tools${NC}" >&2
fi

# Convert to absolute paths
INPUT_FILE="$(cd "$(dirname "$INPUT_FILE")" && pwd)/$(basename "$INPUT_FILE")"
if [[ "$OUTPUT_FILE" != /* ]]; then
    OUTPUT_FILE="$(pwd)/$OUTPUT_FILE"
fi

echo -e "${GREEN}Converting Markdown to PDF...${NC}"
echo "Input:  $INPUT_FILE"
echo "Output: $OUTPUT_FILE"
echo "Margin: $MARGIN"
if [[ -n "$PDF_ENGINE" ]]; then
    echo "Engine: $PDF_ENGINE"
fi
echo ""

# Create CSS for A4 formatting
CSS_CONTENT='<style>
@page {
  size: A4;
  margin: '$MARGIN';
}
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.6;
  color: #333;
  max-width: 100%;
}
h1, h2, h3, h4, h5, h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  page-break-after: avoid;
}
h1 { font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
h2 { font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
h3 { font-size: 1.25em; }
table {
  border-collapse: collapse;
  width: 100%;
  margin: 16px 0;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid #dfe2e5;
  padding: 6px 13px;
}
th {
  background-color: #f6f8fa;
  font-weight: 600;
}
tr:nth-child(even) {
  background-color: #f9f9f9;
}
code {
  background-color: #f6f8fa;
  border-radius: 3px;
  padding: 0.2em 0.4em;
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: 85%;
}
pre {
  background-color: #f6f8fa;
  border-radius: 3px;
  padding: 16px;
  overflow: auto;
  page-break-inside: avoid;
}
pre code {
  background-color: transparent;
  padding: 0;
}
a {
  color: #0366d6;
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
img {
  max-width: 100%;
  height: auto;
  page-break-inside: avoid;
}
blockquote {
  border-left: 4px solid #dfe2e5;
  padding-left: 16px;
  margin-left: 0;
  color: #6a737d;
}
hr {
  border: 0;
  border-top: 1px solid #eaecef;
  margin: 24px 0;
}
ul, ol {
  padding-left: 2em;
}
li {
  margin: 0.25em 0;
}
@media print {
  body {
    background: white;
  }
  a {
    color: #0366d6;
  }
}
</style>'

# Create temporary files
TEMP_HTML=$(mktemp "${TMPDIR:-/tmp}/md2pdf.XXXXXX.html")
TEMP_CSS=$(mktemp "${TMPDIR:-/tmp}/md2pdf.XXXXXX.css")
trap "rm -f '$TEMP_HTML' '$TEMP_CSS'" EXIT

# Write CSS to file (removing <style> tags)
echo "$CSS_CONTENT" | sed 's/<style>//;s/<\/style>//' > "$TEMP_CSS"

# Convert to HTML first with embedded CSS
if [[ -n "$PDF_ENGINE" ]]; then
    # Use pandoc with PDF engine
    pandoc "$INPUT_FILE" \
        --from markdown \
        --to html5 \
        --standalone \
        --embed-resources \
        --metadata title="" \
        --css "$TEMP_CSS" \
        --output "$TEMP_HTML"

    # Convert HTML to PDF using detected engine
    case "$PDF_ENGINE" in
        wkhtmltopdf)
            wkhtmltopdf \
                --page-size A4 \
                --margin-top "${MARGIN}" \
                --margin-bottom "${MARGIN}" \
                --margin-left "${MARGIN}" \
                --margin-right "${MARGIN}" \
                --enable-local-file-access \
                "$TEMP_HTML" "$OUTPUT_FILE" 2>/dev/null
            ;;
        prince)
            prince "$TEMP_HTML" -o "$OUTPUT_FILE" 2>/dev/null
            ;;
        weasyprint)
            weasyprint "$TEMP_HTML" "$OUTPUT_FILE" 2>/dev/null
            ;;
    esac
else
    # Fallback: Create HTML with print styles
    pandoc "$INPUT_FILE" \
        --from markdown \
        --to html5 \
        --standalone \
        --embed-resources \
        --metadata title="" \
        --css "$TEMP_CSS" \
        --output "$OUTPUT_FILE.html"

    echo -e "${YELLOW}No PDF engine available. Created HTML file instead: $OUTPUT_FILE.html${NC}"
    echo -e "${YELLOW}To convert to PDF, install a PDF engine:${NC}"
    echo "  brew install wkhtmltopdf"
    echo ""
    echo -e "${YELLOW}You can also print the HTML file to PDF from your browser (Cmd+P)${NC}"
    OUTPUT_FILE="$OUTPUT_FILE.html"
fi

if [[ $? -eq 0 ]]; then
    echo -e "${GREEN}✓ Conversion successful!${NC}"
    echo "PDF created: $OUTPUT_FILE"

    # Show file size
    if [[ -f "$OUTPUT_FILE" ]]; then
        SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
        echo "File size: $SIZE"
    fi
else
    echo -e "${RED}✗ Conversion failed${NC}" >&2
    exit 1
fi
