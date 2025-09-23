#!/usr/bin/env python3
"""
Flipkart Web Scraper - Working Version
"""

import os
import logging
import time
import json
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Create directories first
if os.path.exists('data') and os.path.isfile('data'):
    os.remove('data')  # Remove if it's a file
os.makedirs('data', exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/scraper.log"),
        logging.StreamHandler()
    ]
)

class FlipkartScraper:
    """
    Main class for scraping Flipkart product data
    """
    
    def __init__(self, headless=True, storage_type="csv"):
        """
        Initialize the scraper
        
        Args:
            headless (bool): Run browser in headless mode
            storage_type (str): How to store data - 'csv', 'json'
        """
        self.headless = headless
        self.storage_type = storage_type
        self.driver = None
        self.wait = None
        
        logging.info("FlipkartScraper initialized")
    
    def setup_driver(self):
        """
        Set up Chrome driver with appropriate options
        """
        try:
            chrome_options = Options()
            
            # Basic options for stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            
            # User agent to look more like a real browser
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            # Headless mode
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Auto-install ChromeDriver
            service = Service(ChromeDriverManager().install())
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
            logging.info("Chrome driver setup successful")
            return True
            
        except Exception as e:
            logging.error(f"Failed to setup Chrome driver: {e}")
            return False
    
    def close_login_popup(self):
        """
        Handle Flipkart's login popup that appears on first visit
        """
        try:
            close_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='_2KpZ6l _2doB4z']"))
            )
            close_button.click()
            logging.info("Login popup closed")
            time.sleep(1)
            return True
        except TimeoutException:
            logging.info("No login popup detected")
            return True
        except Exception as e:
            logging.warning(f"Could not close login popup: {e}")
            return False
    
    def search_products(self, search_term):
        """
        Search for products on Flipkart
        """
        try:
            search_box = self.wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys(search_term)
            
            search_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            search_button.click()
            
            # Wait for results to load
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-id]"))
            )
            
            logging.info(f"Search completed for: {search_term}")
            time.sleep(2)
            return True
            
        except Exception as e:
            logging.error(f"Search failed for {search_term}: {e}")
            return False
    
    
    def extract_product_info(self, product_element):
        """
        Extract information from a single product element
        Updated with current Flipkart selectors
        """
        product_data = {}
        
        try:
            # Product title - try multiple selectors
            try:
                # Try common title selectors for Flipkart 2024
                title_selectors = [
                    "._4rR01T",           # Old selector
                    ".s1Q9rs",            # Alternative selector
                    "._2WkVRV",           # Another alternative
                    ".IRpwTa",            # New selector
                    "._1fQZEK",           # Another new selector
                    "a[title]",           # Generic title attribute
                    ".KzDlHZ",            # Mobile page specific
                    "div[title]",         # Div with title
                    "span[title]"         # Span with title
                ]
                
                title = None
                for selector in title_selectors:
                    try:
                        element = product_element.find_element(By.CSS_SELECTOR, selector)
                        title = element.get_attribute('title') or element.text
                        if title and title.strip():
                            break
                    except:
                        continue
                
                product_data['title'] = title.strip() if title else "Title not found"
                
            except Exception as e:
                product_data['title'] = "Title extraction failed"
                logging.debug(f"Title extraction error: {e}")
            
            # Price - try multiple selectors
            try:
                price_selectors = [
                    "._30jeq3",           # Old price selector
                    "._1_TUDb",           # Alternative price
                    ".ZY8OJN",            # Another alternative
                    "._3tbKJL",           # New price selector
                    "._25b18c",           # Another new selector
                    "._1vC4OE",           # Mobile specific
                    ".Nx9bqj",            # Current price
                    "._2rQ-NK"            # Price container
                ]
                
                price = None
                for selector in price_selectors:
                    try:
                        element = product_element.find_element(By.CSS_SELECTOR, selector)
                        price = element.text
                        if price and price.strip() and '₹' in price:
                            break
                    except:
                        continue
                
                product_data['price'] = price.strip() if price else "Price not available"
                
            except Exception as e:
                product_data['price'] = "Price extraction failed"
                logging.debug(f"Price extraction error: {e}")
            
            # Rating - try multiple selectors
            try:
                rating_selectors = [
                    "._3LWZlK",           # Old rating selector
                    "._2_R_DZ",           # Alternative rating
                    "._3Ay6Sb",           # New rating selector
                    ".XQDdHH",            # Another new selector
                    "._2d4LTz",           # Rating container
                    "._1BLPMq"            # Mobile specific rating
                ]
                
                rating = None
                for selector in rating_selectors:
                    try:
                        element = product_element.find_element(By.CSS_SELECTOR, selector)
                        rating = element.text
                        if rating and rating.strip():
                            break
                    except:
                        continue
                
                product_data['rating'] = rating.strip() if rating else "No rating"
                
            except Exception as e:
                product_data['rating'] = "Rating extraction failed"
                logging.debug(f"Rating extraction error: {e}")
            
            # Additional data extraction
            try:
                # Product image
                img_element = product_element.find_element(By.CSS_SELECTOR, "img")
                product_data['image_url'] = img_element.get_attribute("src") or "No image"
            except:
                product_data['image_url'] = "No image"
            
            # Add timestamp
            product_data['scraped_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Debug logging
            if product_data['title'] != "Title not found" and product_data['title'] != "Title extraction failed":
                logging.info(f"✅ Successfully extracted: {product_data['title'][:50]}...")
            else:
                logging.warning(f"❌ Failed to extract valid title from product element")
                # Log the first 200 characters of the element's HTML for debugging
                try:
                    element_html = product_element.get_attribute('outerHTML')[:200]
                    logging.debug(f"Element HTML sample: {element_html}")
                except:
                    pass
            
            return product_data
            
        except Exception as e:
            logging.warning(f"Error extracting product info: {e}")
            return None
    
    def scrape_page(self):
        """
        Scrape all products from current page
        """
        products = []
        
        try:
            # Try different product container selectors
            product_selectors = ["[data-id]", "._1AtVbE", "._13oc-S", "._2kHMtA", "._1fQZEK"]
            product_elements = []

            for selector in product_selectors:
                product_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if product_elements:
                    logging.info(f"Found {len(product_elements)} products using selector: {selector}")
                    break

            if not product_elements:
                logging.error("No product elements found with any selector")
                return []

            # Add a longer wait for dynamic content 
            time.sleep(3)

            for i, element in enumerate(product_elements):
                try:
                    product_data = self.extract_product_info(element)
                    if product_data and product_data.get('title') not in ["Title not found", "Title extraction failed"]:
                        products.append(product_data)
                        logging.info(f"Product {i+1}: ✅ {product_data['title'][:50]}")
                    else:
                        logging.warning(f"Product {i+1}: ❌ Could not extract valid data")
                    
                except Exception as e:
                    logging.warning(f"Failed to extract product {i+1}: {e}")
                    continue

            logging.info(f"Successfully extracted {len(products)} out of {len(product_elements)} products")
            return products
            
        except Exception as e:
            logging.error(f"Failed to scrape page: {e}")
            return []
    
    def scrape_products(self, search_term, max_pages=1):
        """
        Main method to scrape products from Flipkart
        """
        all_products = []
        
        try:
            # Setup driver
            if not self.setup_driver():
                logging.error("Failed to setup driver")
                return []
            
            # Navigate to Flipkart
            logging.info("Navigating to Flipkart...")
            self.driver.get("https://www.flipkart.com")
            
            # Handle login popup
            self.close_login_popup()
            
            # Search for products
            if not self.search_products(search_term):
                logging.error("Search failed")
                return []
            
            # Scrape page
            logging.info(f"Scraping page 1/{max_pages}")
            page_products = self.scrape_page()
            all_products.extend(page_products)
            
            logging.info(f"Page 1: Found {len(page_products)} products")
            logging.info(f"Scraping completed. Total products: {len(all_products)}")
            return all_products
            
        except Exception as e:
            logging.error(f"Scraping failed: {e}")
            return []
        
        finally:
            # Clean up
            # if self.driver:
            #    self.driver.quit()
            #     logging.info("Browser closed")
            pass
   
    def save_to_csv(self, products, filename):
        """
        Save products to CSV file
        """
        if not products:
            logging.warning("No products to save")
            return None
        
        try:
            df = pd.DataFrame(products)
            
            # Save to CSV
            csv_file = f"data/{filename}.csv"
            df.to_csv(csv_file, index=False)
            
            logging.info(f"Data saved to {csv_file}")
            print(f"✅ Saved {len(products)} products to {csv_file}")
            
            return df
            
        except Exception as e:
            logging.error(f"Failed to save CSV: {e}")
            return None

# Example usage and testing
if __name__ == "__main__":
    # Create scraper instance
    scraper = FlipkartScraper(headless=False)  # Set to False to see browser
    
    # Test with a simple search
    search_term = "smartphone"
    max_pages = 5
    
    print(f"🔍 Starting test scrape for '{search_term}' (max {max_pages} page)")
    print("This may take a minute...")
    
    # Scrape products
    products = scraper.scrape_products(search_term, max_pages)
    
    if products:
        print(f"\n📊 Successfully scraped {len(products)} products!")
        
        # Save data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"flipkart_{search_term}_{timestamp}"
        
        # Save as CSV
        df = scraper.save_to_csv(products, filename)
        
        # Display sample data
        print("\n📋 Sample products:")
        for i, product in enumerate(products[:3]):
            print(f"\n{i+1}. {product['title']}")
            print(f"   Price: {product['price']}")
            print(f"   Rating: {product['rating']}")
    
    else:
        print("❌ No products were scraped. Check logs for errors.")