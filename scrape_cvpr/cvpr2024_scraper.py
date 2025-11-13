"""
CVPR 2024 Conference Data Extractor
Scrapes paper information from https://openaccess.thecvf.com/CVPR2024?day=all
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import re
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CVPR2024Scraper:
    """Scraper for CVPR 2024 conference papers"""
    
    def __init__(self, base_url: str = "https://openaccess.thecvf.com/CVPR2024?day=all", fetch_abstracts: bool = True, max_papers: int = 100):
        self.base_url = base_url
        self.fetch_abstracts = fetch_abstracts
        self.max_papers = max_papers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.papers = []
        
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage"""
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_paper_info(self, paper_element) -> Optional[Dict]:
        """Extract only: title, authors, pdf_url, supplementary_url"""
        try:
            paper_info = {}
            
            # Extract title from <dt> element
            title_elem = paper_element.find('dt')
            if title_elem:
                title_link = title_elem.find('a')
                if title_link:
                    paper_info['title'] = title_link.get_text(strip=True)
                    # Store paper URL temporarily for abstract fetching (not saved in final output)
                    href = title_link.get('href', '')
                    if href:
                        paper_info['_paper_url'] = urljoin("https://openaccess.thecvf.com/", href)
                else:
                    # Title might be direct text in dt
                    title_text = title_elem.get_text(strip=True)
                    if title_text:
                        paper_info['title'] = title_text
            
            # Extract authors from <dd> element
            authors_elem = paper_element.find('dd')
            if authors_elem:
                # CVF typically has author links
                author_links = authors_elem.find_all('a')
                if author_links:
                    paper_info['authors'] = [link.get_text(strip=True) for link in author_links]
                else:
                    # Fallback: extract from text
                    author_text = authors_elem.get_text(strip=True)
                    # Remove common prefixes
                    for prefix in ['Authors:', 'Author:', 'By:']:
                        if prefix in author_text:
                            author_text = author_text.split(prefix, 1)[-1].strip()
                            break
                    if author_text:
                        # Split by comma, but be careful with "Last, First" format
                        authors = [a.strip() for a in author_text.split(',')]
                        paper_info['authors'] = authors
            
            # Extract PDF link (usually in the same dd or dt)
            pdf_link = paper_element.find('a', href=re.compile(r'\.pdf$'))
            if pdf_link:
                href = pdf_link.get('href', '')
                if href:
                    paper_info['pdf_url'] = urljoin("https://openaccess.thecvf.com/", href)
            
            # Extract supplementary material link if available
            supp_link = paper_element.find('a', href=re.compile(r'supplemental|supplementary', re.I))
            if supp_link:
                href = supp_link.get('href', '')
                if href:
                    paper_info['supplementary_url'] = urljoin("https://openaccess.thecvf.com/", href)
            
            return paper_info if paper_info.get('title') else None
            
        except Exception as e:
            logger.error(f"Error extracting paper info: {e}")
            return None
    
    def scrape_papers(self) -> List[Dict]:
        """Scrape all papers from the CVPR 2024 website"""
        logger.info("Starting to scrape CVPR 2024 papers...")
        
        soup = self.fetch_page(self.base_url)
        if not soup:
            logger.error("Failed to fetch main page")
            return []
        
        papers = []
        
        # CVF website typically uses <dt> and <dd> pairs for papers
        # Find all <dt> elements which contain paper titles
        dt_elements = soup.find_all('dt')
        
        logger.info(f"Found {len(dt_elements)} potential paper entries (will stop at {self.max_papers} papers)")
        
        for idx, dt_elem in enumerate(dt_elements):
            # Stop if we've reached the limit
            if len(papers) >= self.max_papers:
                logger.info(f"Reached limit of {self.max_papers} papers. Stopping extraction.")
                break
            
            # Get the corresponding <dd> element (next sibling)
            dd_elem = dt_elem.find_next_sibling('dd')
            
            # Create a wrapper element for extraction
            wrapper = soup.new_tag('div')
            wrapper.append(dt_elem)
            if dd_elem:
                wrapper.append(dd_elem)
            
            paper_info = self.extract_paper_info(wrapper)
            if paper_info:
                papers.append(paper_info)
                logger.info(f"Extracted paper {len(papers)}/{self.max_papers}: {paper_info.get('title', 'Unknown')[:60]}...")
            
            # Be respectful with rate limiting
            if (idx + 1) % 20 == 0:
                time.sleep(0.3)
                logger.info(f"Progress: {idx + 1}/{len(dt_elements)} entries processed, {len(papers)} papers extracted")
        
        # If we found papers, try to get more details from individual paper pages
        if papers and self.fetch_abstracts:
            logger.info(f"Found {len(papers)} papers. Fetching abstracts...")
            papers = self.enrich_paper_details(papers)
        elif papers:
            logger.info(f"Found {len(papers)} papers. Skipping abstract fetching (use fetch_abstracts=True to enable).")
        
        self.papers = papers
        return papers
    
    def enrich_paper_details(self, papers: List[Dict]) -> List[Dict]:
        """Enrich paper information by visiting individual paper pages - only extract abstracts"""
        enriched_papers = []
        
        for idx, paper in enumerate(papers):
            # Try to find paper URL from title link (stored as _paper_url) or construct from PDF
            paper_url = paper.get('_paper_url')
            if not paper_url and 'pdf_url' in paper and paper['pdf_url']:
                # Convert PDF URL to paper page URL
                paper_url = paper['pdf_url'].replace('/papers/', '/').replace('.pdf', '.html')
            
            if paper_url:
                soup = self.fetch_page(paper_url)
                if soup:
                    # Try to extract abstract
                    abstract_elem = soup.find('div', id='abstract')
                    if not abstract_elem:
                        abstract_elem = soup.find('div', class_=re.compile(r'abstract', re.I))
                    if abstract_elem:
                        paper['abstract'] = abstract_elem.get_text(strip=True)
                    
                    # Extract PDF link if not already found
                    if 'pdf_url' not in paper or not paper['pdf_url']:
                        pdf_link = soup.find('a', href=re.compile(r'\.pdf$'))
                        if pdf_link:
                            href = pdf_link.get('href', '')
                            if href:
                                paper['pdf_url'] = urljoin("https://openaccess.thecvf.com/", href)
            
            # Remove temporary _paper_url field
            if '_paper_url' in paper:
                del paper['_paper_url']
            
            enriched_papers.append(paper)
            
            # Rate limiting
            if (idx + 1) % 5 == 0:
                time.sleep(1)
                logger.info(f"Enriched {idx + 1}/{len(papers)} papers...")
        
        return enriched_papers
    
    def save_to_csv(self, filename: str = 'cvpr2024_papers.csv'):
        """Save papers to CSV file - only required fields"""
        if not self.papers:
            logger.warning("No papers to save")
            return
        
        # Only include required fields
        fieldnames = ['title', 'authors', 'abstract', 'pdf_url', 'supplementary_url']
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for paper in self.papers:
                row = {
                    'title': paper.get('title', ''),
                    'authors': '; '.join(paper.get('authors', [])) if isinstance(paper.get('authors'), list) else paper.get('authors', ''),
                    'abstract': paper.get('abstract', ''),
                    'pdf_url': paper.get('pdf_url', ''),
                    'supplementary_url': paper.get('supplementary_url', '')
                }
                writer.writerow(row)
        
        logger.info(f"Saved {len(self.papers)} papers to {filename}")
    
    def save_summary(self, filename: str = 'cvpr2024_summary.txt'):
        """Save a summary report"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("CVPR 2024 Conference Papers Summary\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total Papers Extracted: {len(self.papers)}\n\n")
            
            # Count papers with abstracts
            papers_with_abstracts = sum(1 for p in self.papers if p.get('abstract'))
            f.write(f"Papers with Abstracts: {papers_with_abstracts}\n")
            
            # Count papers with PDFs
            papers_with_pdfs = sum(1 for p in self.papers if p.get('pdf_url'))
            f.write(f"Papers with PDF Links: {papers_with_pdfs}\n\n")
            
            f.write("Sample Papers:\n")
            f.write("-" * 50 + "\n")
            for i, paper in enumerate(self.papers[:10], 1):
                f.write(f"\n{i}. {paper.get('title', 'Unknown Title')}\n")
                if paper.get('authors'):
                    authors = paper['authors'] if isinstance(paper['authors'], list) else [paper['authors']]
                    f.write(f"   Authors: {', '.join(authors[:3])}")
                    if len(authors) > 3:
                        f.write(f" et al. ({len(authors)} total)")
                    f.write("\n")
                if paper.get('abstract'):
                    abstract = paper['abstract'][:200] + "..." if len(paper['abstract']) > 200 else paper['abstract']
                    f.write(f"   Abstract: {abstract}\n")
        
        logger.info(f"Saved summary to {filename}")


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract papers from CVPR 2024 conference website')
    parser.add_argument('--no-abstracts', action='store_true', 
                       help='Skip fetching abstracts (faster, but less complete data)')
    parser.add_argument('--url', type=str, default="https://openaccess.thecvf.com/CVPR2024?day=all",
                       help='URL to scrape (default: CVPR 2024)')
    parser.add_argument('--max-papers', type=int, default=100,
                       help='Maximum number of papers to extract (default: 100)')
    args = parser.parse_args()
    
    scraper = CVPR2024Scraper(base_url=args.url, fetch_abstracts=not args.no_abstracts, max_papers=args.max_papers)
    
    # Scrape papers
    papers = scraper.scrape_papers()
    
    if papers:
        # Save in CSV and summary formats
        scraper.save_to_csv()
        scraper.save_summary()
        
        print(f"\n✓ Successfully extracted {len(papers)} papers from CVPR 2024 (limited to {scraper.max_papers})")
        print("✓ Files created:")
        print("  - cvpr2024_papers.csv (CSV format)")
        print("  - cvpr2024_summary.txt (Summary report)")
    else:
        print("✗ No papers were extracted. The website structure may have changed.")
        print("  Please check the website manually or update the scraper.")


if __name__ == "__main__":
    main()

