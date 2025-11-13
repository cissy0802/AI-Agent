"""
Simple CSV Viewer
Displays CSV files in a formatted table in the terminal
"""

import csv
import sys
from typing import List

def print_table(data: List[List[str]], headers: List[str], max_width: int = 80):
    """Print data in a formatted table"""
    if not data:
        print("No data to display")
        return
    
    # Calculate column widths
    num_cols = len(headers)
    col_widths = [len(str(header)) for header in headers]
    
    for row in data:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Limit column width to max_width
    for i in range(len(col_widths)):
        col_widths[i] = min(col_widths[i], max_width)
    
    # Print header
    header_row = " | ".join(str(headers[i])[:col_widths[i]].ljust(col_widths[i]) 
                           for i in range(num_cols))
    print("=" * len(header_row))
    print(header_row)
    print("=" * len(header_row))
    
    # Print rows
    for row in data:
        display_row = []
        for i, cell in enumerate(row):
            if i < num_cols:
                cell_str = str(cell)
                if len(cell_str) > col_widths[i]:
                    cell_str = cell_str[:col_widths[i]-3] + "..."
                display_row.append(cell_str.ljust(col_widths[i]))
        print(" | ".join(display_row))
    
    print("=" * len(header_row))
    print(f"\nTotal rows: {len(data)}")

def view_csv(filename: str, max_rows: int = None, max_col_width: int = 50):
    """View CSV file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)  # Read header row
            
            data = []
            for i, row in enumerate(reader):
                if max_rows and i >= max_rows:
                    break
                # Pad row if needed
                while len(row) < len(headers):
                    row.append('')
                data.append(row[:len(headers)])
        
        print(f"\n📄 Viewing: {filename}")
        print(f"Columns: {', '.join(headers)}\n")
        
        if max_rows and len(data) > max_rows:
            print(f"Showing first {max_rows} rows (use --max-rows to change):\n")
        
        print_table(data, headers, max_col_width)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error reading CSV: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='View CSV files in formatted table')
    parser.add_argument('filename', nargs='?', default='cvpr2024_papers.csv',
                       help='CSV file to view (default: cvpr2024_papers.csv)')
    parser.add_argument('--max-rows', type=int, default=20,
                       help='Maximum number of rows to display (default: 20)')
    parser.add_argument('--max-width', type=int, default=50,
                       help='Maximum column width (default: 50)')
    parser.add_argument('--all', action='store_true',
                       help='Display all rows (ignores --max-rows)')
    
    args = parser.parse_args()
    
    max_rows = None if args.all else args.max_rows
    view_csv(args.filename, max_rows, args.max_width)

if __name__ == "__main__":
    main()

