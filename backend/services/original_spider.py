import requests
import time
import re
from typing import List, Optional
from bs4 import BeautifulSoup
from datetime import datetime

from core.config import settings
from models.article import ArticleSchema

# Selenium imports (optional)
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class OriginalScholarSpider:
    """Based on the original working google_scholar_spider.py"""
    
    def __init__(self):
        self.base_url = 'https://scholar.google.com/scholar?start={}&q={}&hl=en&as_sdt=0,5'
        self.startyear_url = '&as_ylo={}'
        self.endyear_url = '&as_yhi={}'
        self.robot_keywords = ['unusual traffic from your computer network', 'not a robot']
        self.session = None
        self.driver = None
        
    async def __aenter__(self):
        # Create a requests session
        self.session = requests.Session()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()
        if self.driver:
            self.driver.quit()
    
    def _create_main_url(self, start_year: Optional[int] = None, end_year: Optional[int] = None) -> str:
        """Create main URL based on year filters"""
        gscholar_main_url = self.base_url
        
        if start_year:
            gscholar_main_url = gscholar_main_url + self.startyear_url.format(start_year)
            
        if end_year and end_year != datetime.now().year:
            gscholar_main_url = gscholar_main_url + self.endyear_url.format(end_year)
            
        return gscholar_main_url
    
    def _get_citations(self, content: str) -> int:
        """Extract citation count from content"""
        citation_start = content.find('Cited by ')
        if citation_start == -1:
            return 0
        citation_end = content.find('<', citation_start)
        try:
            return int(content[citation_start + 9:citation_end])
        except:
            return 0
    
    def _get_year(self, content: str) -> int:
        """Extract year from content"""
        try:
            for char in range(len(content)):
                if content[char] == '-':
                    out = content[char - 5:char - 1]
                    if out.isdigit():
                        return int(out)
        except:
            pass
        return 0
    
    def _get_author(self, content: str) -> str:
        """Extract author from content"""
        try:
            author_end = content.find('-')
            return content[2:author_end - 1] if author_end > 2 else content
        except:
            return "Author not found"
    
    def _setup_driver(self):
        """Setup Chrome driver like the original code"""
        if not SELENIUM_AVAILABLE:
            print("❌ Selenium not available")
            return None
            
        try:
            chrome_options = Options()
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            # Don't use headless mode for CAPTCHA solving
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            print(f"❌ Failed to setup Chrome driver: {e}")
            return None
    
    def _get_element(self, driver, xpath, attempts=5, count=0):
        """Safe get_element method with multiple attempts (from original code)"""
        try:
            element = driver.find_element(By.XPATH, xpath)
            return element
        except Exception as e:
            if count < attempts:
                time.sleep(1)
                return self._get_element(driver, xpath, attempts=attempts, count=count + 1)
            else:
                print("Element not found")
                return None
    
    def _get_content_with_selenium(self, url):
        """Get content with Selenium (adapted from original code)"""
        if not SELENIUM_AVAILABLE:
            return None
            
        try:
            if not self.driver:
                self.driver = self._setup_driver()
                
            if not self.driver:
                return None
            
            print(f"🌐 Opening URL with Selenium: {url}")
            self.driver.get(url)
            
            el = self._get_element(self.driver, "/html/body")
            if not el:
                return None
                
            content = el.get_attribute('innerHTML')
            
            if any(kw in content for kw in self.robot_keywords):
                print("🚨 CAPTCHA detected! Please solve manually...")
                print("The browser window should be open. Solve the CAPTCHA and the search will continue automatically.")
                
                # Wait for user to solve CAPTCHA
                # In a production environment, you might implement a more sophisticated solution
                time.sleep(30)  # Give user time to solve CAPTCHA
                
                # Get content again after CAPTCHA solving
                self.driver.get(url)
                el = self._get_element(self.driver, "/html/body")
                if el:
                    content = el.get_attribute('innerHTML')
            
            return content.encode('utf-8')
            
        except Exception as e:
            print(f"❌ Selenium error: {e}")
            return None
    
    def _parse_gs_or_div(self, div) -> Optional[ArticleSchema]:
        """Parse a single gs_or div element to extract article data"""
        try:
            # Title and link
            title_elem = div.find('h3')
            if not title_elem:
                return None
                
            title_link = title_elem.find('a')
            if title_link:
                title = title_link.text.strip()
                url = title_link.get('href', '')
            else:
                title = title_elem.text.strip()
                url = None
            
            # Citations
            citations = self._get_citations(str(div))
            
            # Author info from gs_a div
            gs_a_div = div.find('div', {'class': 'gs_a'})
            if gs_a_div:
                gs_a_text = gs_a_div.text
                
                # Year
                year = self._get_year(gs_a_text)
                
                # Author
                author = self._get_author(gs_a_text)
                
                # Publisher and venue
                try:
                    parts = gs_a_text.split("-")
                    publisher = parts[-1].strip() if len(parts) > 1 else "Publisher not found"
                    
                    if len(parts) > 2:
                        venue_part = parts[-2]
                        venue = " ".join(venue_part.split(",")[:-1]).strip()
                    else:
                        venue = "Venue not found"
                except:
                    publisher = "Publisher not found"
                    venue = "Venue not found"
            else:
                year = 0
                author = "Author not found"
                publisher = "Publisher not found"
                venue = "Venue not found"
            
            # Description from gs_rs div
            description = None
            gs_rs_div = div.find('div', {'class': 'gs_rs'})
            if gs_rs_div:
                description = gs_rs_div.text.strip()
            
            # Calculate citations per year
            citations_per_year = 0.0
            if year > 0 and citations > 0:
                years_passed = max(1, datetime.now().year - year)
                citations_per_year = round(citations / years_passed, 2)
            
            return ArticleSchema(
                title=title,
                authors=author,
                venue=venue,
                publisher=publisher,
                year=year if year > 0 else None,
                citations=citations,
                citations_per_year=citations_per_year,
                description=description,
                url=url
            )
            
        except Exception as e:
            print(f"Error parsing article: {e}")
            return None
    
    async def search(self, keyword: str, num_results: int = 50, 
                    start_year: Optional[int] = None, 
                    end_year: Optional[int] = None) -> List[ArticleSchema]:
        """Search Google Scholar using the original working method"""
        
        articles = []
        gscholar_main_url = self._create_main_url(start_year, end_year)
        
        print(f"🔍 Searching Google Scholar for '{keyword}' (target: {num_results} results)")
        print(f"🌐 Using URL pattern: {gscholar_main_url}")
        
        # Get content from URLs in batches of 10
        for n in range(0, num_results, 10):
            url = gscholar_main_url.format(str(n), keyword.replace(' ', '+'))
            print(f"📖 Fetching page {n//10 + 1}, URL: {url}")
            
            try:
                # Make request
                page = self.session.get(url)
                content = page.content
                
                # Check for robot detection
                content_str = content.decode('ISO-8859-1', errors='ignore')
                if any(kw in content_str for kw in self.robot_keywords):
                    print("🤖 Robot checking detected, trying Selenium...")
                    # Use Selenium fallback like the original code
                    try:
                        content = self._get_content_with_selenium(url)
                        if not content:
                            print("❌ Selenium fallback failed")
                            continue
                    except Exception as e:
                        print(f"❌ Selenium error: {e}")
                        continue
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
                
                # Find articles using the original selector
                mydivs = soup.findAll("div", {"class": "gs_or"})
                print(f"📄 Found {len(mydivs)} article divs on this page")
                
                if not mydivs:
                    print("⚠️  No articles found, might be blocked or end of results")
                    break
                
                # Parse each article
                page_articles = 0
                for div in mydivs:
                    if len(articles) >= num_results:
                        break
                        
                    article = self._parse_gs_or_div(div)
                    if article and article.title and article.title != 'Could not catch title':
                        articles.append(article)
                        page_articles += 1
                        print(f"✅ Parsed: {article.title[:60]}... ({article.citations} citations)")
                
                print(f"📊 Successfully parsed {page_articles} articles from this page")
                
                if len(articles) >= num_results:
                    break
                
                # Original delay
                print("⏳ Waiting 0.5s before next request...")
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Error fetching page {n//10 + 1}: {e}")
                continue
        
        print(f"🎉 Search completed: {len(articles)} articles found")
        return articles