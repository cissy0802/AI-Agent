# CVPR 2024 Conference Data Extractor

A Python script to extract and compile paper data from the CVPR 2024 conference website.

## Features

- Extracts paper metadata:
  - **Title** - Paper title
  - **Authors** - List of authors
  - **Abstract** - Paper abstract (optional, can be skipped for faster extraction)
  - **PDF URL** - Direct link to paper PDF
  - **Supplementary URL** - Link to supplementary materials (if available)
- Limits extraction to 100 papers by default (configurable)
- Saves data in CSV format and summary report
- Respectful web scraping with rate limiting
- Comprehensive error handling and logging

## Requirements

- Python 3.7+
- Internet connection

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with default settings (fetches abstracts, limits to 100 papers):

```bash
python cvpr2024_scraper.py
```

### Command-Line Options

**Skip abstract fetching (faster):**
```bash
python cvpr2024_scraper.py --no-abstracts
```

**Change the paper limit:**
```bash
python cvpr2024_scraper.py --max-papers 50
```

**Use a custom URL (e.g., different conference year):**
```bash
python cvpr2024_scraper.py --url "https://openaccess.thecvf.com/CVPR2023?day=all"
```

**Combine options:**
```bash
python cvpr2024_scraper.py --no-abstracts --max-papers 200
```

### What the script does:

1. Fetches the CVPR 2024 conference page
2. Extracts paper information (title, authors, PDF links, supplementary links)
3. Optionally visits individual paper pages to get abstracts
4. Stops after reaching the specified limit (default: 100 papers)
5. Saves the data to:
   - `cvpr2024_papers.csv` - Data in CSV format for Excel/Google Sheets
   - `cvpr2024_summary.txt` - Summary report with statistics

## Output Files

### CSV Format (`cvpr2024_papers.csv`)

Contains the following columns:
- `title` - Paper title
- `authors` - Semicolon-separated list of authors
- `abstract` - Paper abstract (if fetched)
- `pdf_url` - Direct link to PDF
- `supplementary_url` - Link to supplementary materials (if available)

### Summary Report (`cvpr2024_summary.txt`)

Contains:
- Total number of papers extracted
- Statistics (papers with abstracts, PDFs, etc.)
- Sample papers preview

## Additional Tools

### CSV Viewer

A simple Python script to view CSV files in a formatted table:

```bash
python view_csv.py
```

Options:
- `--max-rows N` - Show first N rows (default: 20)
- `--all` - Show all rows
- `--max-width N` - Set maximum column width (default: 50)

## Project Structure

```
scrape_cvpr/
├── cvpr2024_scraper.py    # Main scraper script
├── requirements.txt        # Python dependencies
├── view_csv.py            # CSV viewer utility
├── refresh_path.ps1       # PATH refresh script (Windows)
├── cvpr2024_papers.csv    # Output: extracted paper data
└── cvpr2024_summary.txt   # Output: summary report
```

## Notes

- The scraper includes rate limiting to be respectful to the server
- Processing time depends on the number of papers and whether abstracts are fetched
- Abstracts require visiting each paper page individually, which adds time
- Default limit is 100 papers to keep extraction time reasonable
- If the website structure changes, the scraper may need updates

## Troubleshooting

**No papers extracted:**
- Check your internet connection
- Verify the website URL is accessible
- The website structure may have changed - check the HTML structure

**Slow extraction:**
- This is normal - the script includes delays to be respectful
- Use `--no-abstracts` flag to skip abstract fetching for faster extraction
- Reduce `--max-papers` if you need results quickly

**Missing data:**
- Some papers may not have abstracts or supplementary materials
- PDF links should be available for most papers
- Author information is typically available for all papers

**Python not found:**
- On Windows, you may need to refresh PATH: `.\refresh_path.ps1`
- Or restart your terminal/PowerShell window

## License

This script is provided as-is for educational and research purposes. Please respect the website's terms of service and robots.txt when using this scraper.
