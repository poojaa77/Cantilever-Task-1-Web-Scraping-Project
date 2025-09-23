#!/usr/bin/env python3
"""
Basic test for Flipkart Scraper setup
Run this to test if your scraper is working correctly
"""

from scraper import FlipkartScraper
import time

def test_driver_setup():
    """Test if Chrome driver can be initialized"""
    print("🔍 Testing Chrome driver setup...")
    
    try:
        scraper = FlipkartScraper(headless=True)
        success = scraper.setup_driver()
        
        if success:
            print("✅ Chrome driver setup successful")
            
            # Test basic navigation
            scraper.driver.get("https://www.google.com")
            title = scraper.driver.title
            print(f"✅ Navigation test passed. Page title: {title}")
            
            scraper.driver.quit()
            return True
        else:
            print("❌ Chrome driver setup failed")
            return False
            
    except Exception as e:
        print(f"❌ Driver test error: {e}")
        return False

def test_flipkart_access():
    """Test if we can access Flipkart"""
    print("\n🔍 Testing Flipkart access...")
    
    try:
        scraper = FlipkartScraper(headless=True)
        scraper.setup_driver()
        
        scraper.driver.get("https://www.flipkart.com")
        time.sleep(3)
        
        # Check if we can find the search box
        search_box = scraper.driver.find_element_by_name("q")
        if search_box:
            print("✅ Flipkart access successful - search box found")
            scraper.driver.quit()
            return True
        
    except Exception as e:
        print(f"❌ Flipkart access error: {e}")
        if 'scraper' in locals() and scraper.driver:
            scraper.driver.quit()
        return False

def test_mini_scrape():
    """Test a mini scrape with just 1 page"""
    print("\n🔍 Testing mini scrape (1 page, 'mobile')...")
    
    try:
        scraper = FlipkartScraper(headless=True)
        products = scraper.scrape_products("mobile", max_pages=1)
        
        if products and len(products) > 0:
            print(f"✅ Mini scrape successful - found {len(products)} products")
            
            # Show first product
            first_product = products[0]
            print(f"\nSample product:")
            print(f"Title: {first_product['title']}")
            print(f"Price: {first_product['price']}")
            print(f"Rating: {first_product['rating']}")
            
            return True
        else:
            print("❌ Mini scrape failed - no products found")
            return False
            
    except Exception as e:
        print(f"❌ Mini scrape error: {e}")
        return False

def main():
    """Run all basic tests"""
    print("🚀 Flipkart Scraper Basic Tests")
    print("=" * 50)
    
    tests = [
        ("Driver Setup", test_driver_setup),
        ("Flipkart Access", test_flipkart_access),
        ("Mini Scrape", test_mini_scrape)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except KeyboardInterrupt:
            print("\n❌ Test interrupted by user")
            break
        except Exception as e:
            print(f"❌ {test_name} failed with unexpected error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your scraper is ready to use.")
        print("\nTry running: python scraper.py")
    else:
        print("⚠  Some tests failed. Check the errors above.")

if _name_ == "_main_":
    main()
    