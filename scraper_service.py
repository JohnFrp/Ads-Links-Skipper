"""
scraper_service.py

Contains all business logic for scraping.
This class is fully self-contained and has no dependency on Flask.
It can be imported and used in any other Python script (e.g., a CLI).

This adheres to:
- Single Responsibility Principle (SRP): Its only job is to scrape.
- Dependency Inversion Principle (DIP): It depends on abstractions
  (like a list of domains) passed to it, not on concrete global variables.
"""
import re
from urllib.parse import urljoin
import cloudscraper
from bs4 import BeautifulSoup

class ScraperService:
    """
    A reusable service to perform the two-step link extraction.
    """
    def __init__(self, allowed_domains, headers):
        """
        Initializes the service with its dependencies.
        """
        self.allowed_domains = allowed_domains
        self.scraper = cloudscraper.create_scraper()
        self.scraper.headers.update(headers)

    def _get_base_url(self, url):
        """Extracts the base URL (e.g., https://example.com)"""
        parts = url.split('/')
        if len(parts) >= 3:
            return f"{parts[0]}//{parts[2]}"
        return None
    
    def _create_regex_pattern(self, url):
        """Dynamically creates the regex pattern for intermediate links."""
        base_url = self._get_base_url(url)
        if not base_url:
            raise ValueError("Could not determine base URL.")
        # Creates a pattern like: ^https://rmcmm\.org/links/.+?/$
        return rf"^{re.escape(base_url)}/links/.+?/$"

    def _find_intermediate_links(self, url, pattern):
        """
        Step 1: Scrapes the initial URL to find links matching the regex pattern.
        """
        intermediate_links = set()
        print(f"[Step 1] Fetching initial URL: {url}")
        
        response = self.scraper.get(url)
        response.raise_for_status()  # Will raise an error if status code is not 200
        
        soup = BeautifulSoup(response.text, 'html.parser')
        base_url = self._get_base_url(url)
        
        for a in soup.find_all('a', href=True):
            full_url = urljoin(base_url, a['href'])
            if re.match(pattern, full_url):
                intermediate_links.add(full_url)
        
        print(f"[Step 1] Found {len(intermediate_links)} intermediate links.")
        return intermediate_links

    def _find_final_download_links(self, intermediate_links):
        """
        Step 2: Scrapes each intermediate link to find the final download links.
        """
        final_links = set()
        errors = []
        
        for link in intermediate_links:
            try:
                print(f"[Step 2] Fetching intermediate link: {link}")
                response = self.scraper.get(link)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                base_url = self._get_base_url(link)
                
                found_on_page = False
                for a in soup.find_all('a', href=True):
                    full_url = urljoin(base_url, a['href'])
                    
                    if any(domain in full_url.lower() for domain in self.allowed_domains):
                        final_links.add(full_url)
                        found_on_page = True
                
                if not found_on_page:
                    print(f"[Step 2] No final links found on: {link}")
                    
            except Exception as e:
                error_msg = f"Step 2 Error (Scraping {link}): {str(e)}"
                print(error_msg)
                errors.append(error_msg)
                
        return sorted(list(final_links)), errors

    def extract_links(self, url):
        """
        Public method to orchestrate the full scraping process.
        This is the main interface for this service.
        """
        try:
            # --- Step 1 ---
            link_pattern_regex = self._create_regex_pattern(url)
            intermediate_links = self._find_intermediate_links(url, link_pattern_regex)
            
            if not intermediate_links:
                return None, "Step 1: No intermediate links found matching the pattern (e.g., .../links/...).".strip()
            
            # --- Step 2 ---
            final_links, step2_errors = self._find_final_download_links(intermediate_links)
            
            error_message = None
            if step2_errors:
                error_message = " | ".join(step2_errors)
            
            if not final_links and not error_message:
                error_message = "Step 2: Found intermediate links, but no final download links (usersdrive, etc.) were found on those pages."
            
            return final_links, error_message

        except Exception as e:
            print(f"Error in extract_links: {e}")
            return None, f"An unexpected error occurred: {str(e)}"
