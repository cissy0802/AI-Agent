# CVPR 2024 Conference Data Extractor

A Python script to extract and compile paper data from the CVPR 2024 conference website.

## Features

- Extracts paper metadata including:
  - Title
  - Authors
  - Abstract (when available)
  - PDF download links
  - Supplementary material links
  - Paper IDs
- Saves data in multiple formats:
  - JSON (structured data)
  - CSV (spreadsheet-compatible)
  - Summary report (text file)
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

Run the scraper with default settings (fetches abstracts):

```bash
python cvpr2024_scraper.py
```

### Command-Line Options

**Skip abstract fetching (faster):**
```bash
python cvpr2024_scraper.py --no-abstracts
```

**Use a custom URL:**
```bash
python cvpr2024_scraper.py --url "https://openaccess.thecvf.com/CVPR2023?day=all"
```

**Combine options:**
```bash
python cvpr2024_scraper.py --no-abstracts --url "https://openaccess.thecvf.com/CVPR2023?day=all"
```

### What the script does:
1. Fetch the CVPR 2024 conference page
2. Extract all paper information
3. Visit individual paper pages to get abstracts and additional details
4. Save the data to three files:
   - `cvpr2024_papers.json` - Complete data in JSON format
   - `cvpr2024_papers.csv` - Data in CSV format for Excel/Google Sheets
   - `cvpr2024_summary.txt` - Summary report with statistics

## Output Files

### JSON Format (`cvpr2024_papers.json`)
Contains complete paper data with nested structures:
```json
{
  "index": 1,
  "paper_id": "123",
  "title": "Paper Title",
  "authors": ["Author 1", "Author 2"],
  "abstract": "Paper abstract...",
  "paper_url": "https://...",
  "pdf_url": "https://...",
  "supplementary_url": "https://...",
  "keywords": ["keyword1", "keyword2"]
}
```

### CSV Format (`cvpr2024_papers.csv`)
Flat structure suitable for spreadsheet applications:
- Authors are semicolon-separated
- Keywords are semicolon-separated
- All fields are in a single row per paper

### Summary Report (`cvpr2024_summary.txt`)
Contains:
- Total number of papers extracted
- Statistics (papers with abstracts, PDFs, etc.)
- Sample papers preview

## Customization

You can modify the scraper by editing `cvpr2024_scraper.py`:

- Change the base URL to scrape different conferences
- Adjust rate limiting delays
- Add additional fields to extract
- Modify output formats

## Notes

- The scraper includes rate limiting to be respectful to the server
- Processing time depends on the number of papers (typically 2000+ for CVPR)
- Abstracts are fetched from individual paper pages, which may take additional time
- If the website structure changes, the scraper may need updates

## Troubleshooting

**No papers extracted:**
- Check your internet connection
- Verify the website URL is accessible
- The website structure may have changed - check the HTML structure

**Slow extraction:**
- This is normal - the script includes delays to be respectful
- Abstracts require visiting each paper page individually
- Consider disabling abstract fetching if speed is critical

**Missing data:**
- Some papers may not have abstracts or supplementary materials
- PDF links should be available for most papers
- Author information is typically available for all papers

## License

This script is provided as-is for educational and research purposes. Please respect the website's terms of service and robots.txt when using this scraper.

