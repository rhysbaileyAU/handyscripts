# Markdown to PDF Converter

A shell script to convert Markdown files to PDF with proper A4 formatting, margins, and table support.

## Installation

The script requires:
- **pandoc** - For markdown parsing (already installed)
- **weasyprint** - For PDF generation (already installed)

If you need to install on another system:
```bash
brew install pandoc weasyprint
```

## Usage

Basic usage:
```bash
./md2pdf.sh document.md
```

This creates `document.pdf` in the same directory as the input file.

### Options

```bash
# Custom output path
./md2pdf.sh input.md output.pdf

# Custom margins (default: 2.5cm)
./md2pdf.sh --margin 2cm document.md

# Show help
./md2pdf.sh --help
```

### Examples

```bash
# Convert with default settings
./md2pdf.sh workshops/workshop4-discussionpoints.md

# Convert with 3cm margins
./md2pdf.sh --margin 3cm workshops/workshop4-discussionpoints.md

# Specify custom output location
./md2pdf.sh workshops/workshop4-discussionpoints.md ~/Desktop/output.pdf
```

## Features

- **A4 page size** (210mm x 297mm)
- **Configurable margins** (default: 2.5cm)
- **Table support** with proper formatting and borders
- **Image embedding** from local files or URLs
- **Clickable hyperlinks** in the PDF
- **Syntax highlighting** for code blocks
- **Clean formatting** with GitHub-style CSS

## Output Quality

The script generates professional-looking PDFs with:
- Readable 11pt font
- Proper heading hierarchy
- Well-formatted tables with alternating row colors
- Clean code block styling
- Page breaks that avoid splitting tables
- Proper link colors and styling

## Troubleshooting

If you see "No PDF engine available":
```bash
brew install weasyprint
```

The script will auto-detect and use the first available PDF engine from:
- weasyprint (recommended)
- prince
- wkhtmltopdf (discontinued)
