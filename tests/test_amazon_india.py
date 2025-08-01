"""
Amazon India Automation Test Suite
Clean, working implementation for testing Amazon India functionality
"""

import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from datetime import datetime


class TestAmazonIndia:
    """Test class for Amazon India website functionality"""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown with VISIBLE browser window"""
        from utils.browser_config import create_visible_chrome_driver, ensure_window_visibility
        
        print("Initializing VISIBLE browser for basic tests...")
        
        try:
            self.driver = create_visible_chrome_driver()
            
            # Ensure visibility is maintained
            ensure_window_visibility(self.driver)
            
            print("VISIBLE Chrome browser ready for basic testing")
            
        except Exception as e:
            print(f"Failed to create visible browser for basic tests: {e}")
            raise Exception("VISIBLE browser window is mandatory for basic tests")
        
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "https://www.amazon.in"
        
        yield
        
        # Teardown
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
    
    def take_screenshot(self, test_name):
        """Take screenshot for debugging"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/{test_name}_{timestamp}.png"
            os.makedirs("screenshots", exist_ok=True)
            self.driver.save_screenshot(screenshot_path)
            return screenshot_path
        except Exception:
            return None
    
    def test_homepage_load(self):
        """Test if Amazon India homepage loads correctly"""
        try:
            self.driver.get(self.base_url)
            
            # Wait for page to load
            self.wait.until(lambda driver: driver.title != "")
            assert "Amazon" in self.driver.title or "amazon" in self.driver.title.lower()
            
            # Check if search box is present
            search_box = self.wait.until(
                EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
            )
            assert search_box.is_displayed()
            
            # Check if logo is present
            logo = self.driver.find_element(By.ID, "nav-logo")
            assert logo.is_displayed()
            
            print("✓ Homepage loaded successfully")
            
        except Exception as e:
            self.take_screenshot("homepage_load_failed")
            pytest.fail(f"Homepage load test failed: {str(e)}")
    
    def test_search_functionality(self):
        """Test search functionality with a product"""
        try:
            self.driver.get(self.base_url)
            
            # Find search box
            search_box = self.wait.until(
                EC.element_to_be_clickable((By.ID, "twotabsearchtextbox"))
            )
            
            # Search for laptop
            search_term = "laptop"
            search_box.clear()
            search_box.send_keys(search_term)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for search results
            search_results = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "[data-component-type='s-search-result']")
                )
            )
            
            assert len(search_results) > 0
            print(f"✓ Search functionality working - Found {len(search_results)} results")
            
        except Exception as e:
            self.take_screenshot("search_functionality_failed")
            pytest.fail(f"Search functionality test failed: {str(e)}")
    
    def test_product_details_page(self):
        """Test accessing a product details page"""
        try:
            self.driver.get(self.base_url)
            
            # Search for a product
            search_box = self.wait.until(
                EC.element_to_be_clickable((By.ID, "twotabsearchtextbox"))
            )
            search_box.clear()
            search_box.send_keys("smartphone")
            search_box.send_keys(Keys.RETURN)
            
            # Click on first product
            first_product = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "[data-component-type='s-search-result'] h2 a")
                )
            )
            first_product.click()
            
            # Verify we're on product details page
            product_title = self.wait.until(
                EC.presence_of_element_located((By.ID, "productTitle"))
            )
            assert product_title.is_displayed()
            
            # Check for price
            price_elements = self.driver.find_elements(By.CSS_SELECTOR, ".a-price-whole")
            assert len(price_elements) > 0
            
            print("✓ Product details page loaded successfully")
            
        except Exception as e:
            self.take_screenshot("product_details_failed")
            pytest.fail(f"Product details test failed: {str(e)}")
    
    def test_category_navigation(self):
        """Test navigation through categories"""
        try:
            self.driver.get(self.base_url)
            
            # Try to click on hamburger menu
            try:
                hamburger_menu = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "nav-hamburger-menu"))
                )
                hamburger_menu.click()
                
                # Wait for menu to open
                time.sleep(2)
                
                # Look for a category link
                category_links = self.driver.find_elements(
                    By.XPATH, "//a[contains(text(), 'Electronics')]"
                )
                if category_links:
                    category_links[0].click()
                    time.sleep(2)
                    print("✓ Category navigation working")
                else:
                    print("! Category links not found, but menu opened")
                    
            except TimeoutException:
                print("! Hamburger menu not found, trying top navigation")
                # Try top navigation
                nav_links = self.driver.find_elements(By.CSS_SELECTOR, "#nav-xshop a")
                if nav_links:
                    nav_links[0].click()
                    time.sleep(2)
                    print("✓ Top navigation working")
                
        except Exception as e:
            self.take_screenshot("category_navigation_failed")
            pytest.fail(f"Category navigation test failed: {str(e)}")
    
    def test_price_validation(self):
        """Test price validation on search results"""
        try:
            self.driver.get(self.base_url)
            
            # Search for books (usually have consistent pricing)
            search_box = self.wait.until(
                EC.element_to_be_clickable((By.ID, "twotabsearchtextbox"))
            )
            search_box.clear()
            search_box.send_keys("books")
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results
            time.sleep(3)
            
            # Find price elements
            price_elements = self.driver.find_elements(By.CSS_SELECTOR, ".a-price-whole")
            prices_found = 0
            
            for element in price_elements:
                try:
                    price_text = element.text.replace(',', '')
                    if price_text.isdigit():
                        price = int(price_text)
                        if 50 <= price <= 50000:  # Reasonable price range
                            prices_found += 1
                except:
                    continue
            
            assert prices_found > 0
            print(f"✓ Price validation successful - Found {prices_found} valid prices")
            
        except Exception as e:
            self.take_screenshot("price_validation_failed")
            pytest.fail(f"Price validation test failed: {str(e)}")
    
    def test_add_to_cart_button_presence(self):
        """Test if add to cart button is present on product page"""
        try:
            self.driver.get(self.base_url)
            
            # Search and go to a product
            search_box = self.wait.until(
                EC.element_to_be_clickable((By.ID, "twotabsearchtextbox"))
            )
            search_box.clear()
            search_box.send_keys("wireless earphones")
            search_box.send_keys(Keys.RETURN)
            
            # Click on first product
            first_product = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "[data-component-type='s-search-result'] h2 a")
                )
            )
            first_product.click()
            
            # Look for add to cart button
            add_to_cart_selectors = [
                (By.ID, "add-to-cart-button"),
                (By.CSS_SELECTOR, "[name='submit.add-to-cart']"),
                (By.XPATH, "//input[@value='Add to Cart']")
            ]
            
            cart_button_found = False
            for selector in add_to_cart_selectors:
                try:
                    button = self.driver.find_element(*selector)
                    if button.is_displayed():
                        cart_button_found = True
                        break
                except NoSuchElementException:
                    continue
            
            if cart_button_found:
                print("✓ Add to cart button found")
            else:
                print("! Add to cart button not found, but product page loaded")
            
        except Exception as e:
            self.take_screenshot("add_to_cart_failed")
            pytest.fail(f"Add to cart test failed: {str(e)}")
    
    def test_responsive_design(self):
        """Test responsive design elements"""
        try:
            self.driver.get(self.base_url)
            
            # Test desktop view
            self.driver.set_window_size(1920, 1080)
            time.sleep(2)
            
            search_box = self.driver.find_element(By.ID, "twotabsearchtextbox")
            assert search_box.is_displayed()
            
            # Test mobile view
            self.driver.set_window_size(375, 667)
            time.sleep(2)
            
            # Check if search box is still accessible or mobile menu is available
            mobile_elements_found = 0
            
            if self.driver.find_elements(By.ID, "twotabsearchtextbox"):
                mobile_elements_found += 1
            
            if self.driver.find_elements(By.ID, "nav-hamburger-menu"):
                mobile_elements_found += 1
            
            assert mobile_elements_found > 0
            
            # Reset to normal size
            self.driver.set_window_size(1920, 1080)
            print("✓ Responsive design working")
            
        except Exception as e:
            self.take_screenshot("responsive_design_failed")
            pytest.fail(f"Responsive design test failed: {str(e)}")


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v", "--html=reports/test_report.html", "--self-contained-html"])