"""
Essential Test Utilities
Core utilities for Amazon India testing - no bloat, just essentials
"""

import os
import time
import re
from datetime import datetime
from utils.browser_config import enforce_single_tab_mode
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import requests
from bs4 import BeautifulSoup


def take_screenshot(driver, name):
    """Take screenshot with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{name}_{timestamp}.png"
    
    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot(filename)
    return filename


def ensure_directories():
    """Ensure required directories exist"""
    for directory in ["screenshots", "reports", "logs"]:
        os.makedirs(directory, exist_ok=True)


def navigate_single_tab(driver, url, wait_time=3):
    """Navigate to URL ensuring single tab execution"""
    try:
        # Enforce single tab mode before navigation
        enforce_single_tab_mode(driver)
        
        # Navigate to URL
        driver.get(url)
        time.sleep(wait_time)
        
        # Re-enforce after page load
        enforce_single_tab_mode(driver)
        
        print(f"[INFO] Navigated to {url} in single tab mode")
        return True
    except Exception as e:
        print(f"[ERROR] Navigation failed: {e}")
        return False


def click_element_single_tab(driver, element):
    """Click element ensuring it stays in single tab"""
    try:
        # Enforce single tab mode before clicking
        enforce_single_tab_mode(driver)
        
        # Use JavaScript click to avoid new tab issues
        driver.execute_script("arguments[0].click();", element)
        time.sleep(2)  # Allow navigation to complete
        
        # Re-enforce after click
        enforce_single_tab_mode(driver)
        
        return True
    except Exception as e:
        print(f"[ERROR] Click failed: {e}")
        return False


def advanced_element_finder(driver, selectors_list, timeout=10, condition="presence"):
    """Advanced element finder with multiple selector strategies and fallbacks"""
    wait = WebDriverWait(driver, timeout)
    
    # Define condition mappings
    conditions = {
        "presence": EC.presence_of_element_located,
        "visible": EC.visibility_of_element_located,
        "clickable": EC.element_to_be_clickable
    }
    
    condition_func = conditions.get(condition, EC.presence_of_element_located)
    
    for selector_info in selectors_list:
        try:
            if isinstance(selector_info, tuple):
                by_type, selector = selector_info
            else:
                # Auto-detect selector type
                by_type, selector = auto_detect_selector_type(selector_info)
            
            element = wait.until(condition_func((by_type, selector)))
            if element and element.is_displayed():
                return element
                
        except (TimeoutException, NoSuchElementException):
            continue
            
    return None


def auto_detect_selector_type(selector_string):
    """Auto-detect selector type based on string pattern"""
    if selector_string.startswith('#'):
        return By.ID, selector_string[1:]
    elif selector_string.startswith('.'):
        return By.CLASS_NAME, selector_string[1:]
    elif selector_string.startswith('//'):
        return By.XPATH, selector_string
    elif '[' in selector_string and ']' in selector_string:
        return By.CSS_SELECTOR, selector_string
    elif selector_string.startswith('name='):
        return By.NAME, selector_string[5:]
    else:
        return By.CSS_SELECTOR, selector_string


def robust_element_click(driver, element, max_attempts=3):
    """Robust element click with multiple strategies"""
    for attempt in range(max_attempts):
        try:
            # Scroll element into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            
            # Try regular click first
            element.click()
            return True
            
        except ElementClickInterceptedException:
            # Try JavaScript click
            try:
                driver.execute_script("arguments[0].click();", element)
                return True
            except Exception as e:
                print(f"   JavaScript click attempt {attempt + 1} failed: {e}")
                
        except Exception as e:
            print(f"   Click attempt {attempt + 1} failed: {e}")
            
        time.sleep(1)
    
    return False


def smart_price_extractor(driver, product_elements):
    """Advanced price extraction with multiple strategies"""
    prices_found = []
    
    for product in product_elements:
        price_data = extract_price_from_element(product)
        if price_data:
            prices_found.append(price_data)
    
    return prices_found


def extract_price_from_element(product_element):
    """Extract price from product element using multiple strategies"""
    # Multiple price selector strategies
    price_selectors = [
        # Standard Amazon price selectors
        ".a-price-whole",
        ".a-price .a-offscreen",
        ".a-price-range .a-offscreen",
        ".a-price-symbol + .a-price-whole",
        
        # Alternative selectors
        "[data-a-price] .a-offscreen",
        ".a-price-display .a-offscreen",
        ".a-price .a-price-whole",
        ".a-price-range .a-price-whole",
        
        # Backup selectors
        "*[class*='price'] *[class*='whole']",
        "*[class*='price'] *[class*='amount']",
        "*[data-testid*='price']",
        "*[aria-label*='price']"
    ]
    
    for selector in price_selectors:
        try:
            price_elements = product_element.find_elements(By.CSS_SELECTOR, selector)
            
            for price_element in price_elements:
                # Try different methods to get price text
                price_text = None
                
                # Method 1: element.text
                if price_element.text.strip():
                    price_text = price_element.text.strip()
                
                # Method 2: textContent attribute
                elif price_element.get_attribute("textContent"):
                    price_text = price_element.get_attribute("textContent").strip()
                
                # Method 3: innerHTML parsing
                elif price_element.get_attribute("innerHTML"):
                    html_content = price_element.get_attribute("innerHTML")
                    # Remove HTML tags and get text
                    price_text = re.sub(r'<[^>]+>', '', html_content).strip()
                
                if price_text:
                    # Extract numeric price using regex
                    price_match = re.search(r'[\d,]+', price_text.replace(',', ''))
                    if price_match:
                        try:
                            price_value = int(price_match.group().replace(',', ''))
                            # Validate price range (reasonable for e-commerce)
                            if 50 <= price_value <= 10000000:  # ₹50 to ₹1 crore
                                return {
                                    "price": price_value,
                                    "original_text": price_text,
                                    "selector_used": selector
                                }
                        except ValueError:
                            continue
                            
        except (NoSuchElementException, Exception):
            continue
    
    return None


def smart_product_finder(driver, max_products=10, timeout=15):
    """Smart product finder with multiple strategies and web scraping fallback"""
    wait = WebDriverWait(driver, timeout)
    
    # Multiple product container selectors
    product_selectors = [
        # Primary selectors
        "[data-component-type='s-search-result']",
        ".s-result-item",
        ".sg-row .sg-col-inner",
        
        # Alternative selectors
        "*[data-cy='title-recipe-fixer']",
        ".s-card-container",
        "*[data-testid='product-card']",
        
        # Backup selectors
        "*[class*='result-item']",
        "*[class*='product-item']",
        "*[data-asin]",
        ".widgetContainer .s-card-border"
    ]
    
    products = []
    
    for selector in product_selectors:
        try:
            found_products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
            if found_products and len(found_products) >= 3:
                products = found_products[:max_products]
                print(f"   ✅ Found {len(products)} products using selector: {selector}")
                break
        except TimeoutException:
            continue
    
    # Fallback: Use BeautifulSoup for web scraping
    if not products:
        try:
            print("   🔍 Attempting web scraping fallback...")
            products = web_scraping_product_fallback(driver)
        except Exception as e:
            print(f"   ⚠️ Web scraping fallback failed: {e}")
    
    return products


def web_scraping_product_fallback(driver):
    """Web scraping fallback using BeautifulSoup"""
    try:
        # Get page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find product containers using BeautifulSoup
        product_containers = []
        
        # Try multiple approaches
        selectors_to_try = [
            {'attrs': {'data-component-type': 's-search-result'}},
            {'class_': lambda x: x and 's-result-item' in x},
            {'attrs': {'data-asin': True}},
            {'class_': lambda x: x and 'product' in str(x).lower()}
        ]
        
        for selector in selectors_to_try:
            found = soup.find_all('div', **selector)
            if found and len(found) >= 3:
                product_containers = found[:10]
                break
        
        # Convert BeautifulSoup elements back to Selenium elements
        if product_containers:
            selenium_products = []
            for i, container in enumerate(product_containers):
                # Find corresponding Selenium element
                try:
                    # Use data-asin or unique attributes to locate
                    asin = container.get('data-asin')
                    if asin:
                        selenium_element = driver.find_element(By.CSS_SELECTOR, f"[data-asin='{asin}']")
                        selenium_products.append(selenium_element)
                    elif i < 10:  # Fallback: use nth-child
                        xpath = f"(//div[contains(@class, 'result') or contains(@class, 'product')])[{i+1}]"
                        selenium_element = driver.find_element(By.XPATH, xpath)
                        selenium_products.append(selenium_element)
                except NoSuchElementException:
                    continue
            
            print(f"   ✅ Web scraping found {len(selenium_products)} products")
            return selenium_products
            
    except Exception as e:
        print(f"   ❌ Web scraping fallback error: {e}")
    
    return []


def intelligent_popup_dismissal(driver, max_attempts=5):
    """Intelligent popup dismissal with comprehensive strategies"""
    dismissed_count = 0
    
    # Comprehensive popup selectors
    popup_selectors = [
        # Continue shopping (highest priority)
        "//button[contains(text(), 'Continue shopping')]",
        "//span[contains(text(), 'Continue shopping')]/parent::button",
        "//a[contains(text(), 'Continue shopping')]",
        
        # Close buttons
        "//button[contains(text(), 'Close')]",
        "//button[contains(text(), 'No thanks')]",
        "//button[contains(text(), 'Not now')]",
        "//button[contains(text(), 'Skip')]",
        "//button[contains(text(), 'Maybe later')]",
        "//button[contains(text(), 'Dismiss')]",
        "//button[contains(text(), 'Cancel')]",
        
        # CSS selectors
        ".a-modal-close",
        ".a-button-close",
        "[data-action='close']",
        "[aria-label*='Close']",
        "[aria-label*='close']",
        ".close-button",
        ".modal-close",
        ".popup-close",
        
        # Generic close patterns
        "button[class*='close']",
        "*[role='button'][aria-label*='close']",
        ".a-button-text:contains('Close')",
        
        # Cookie/GDPR popups
        "//button[contains(text(), 'Accept')]",
        "//button[contains(text(), 'OK')]",
        "[data-testid='accept-button']",
        ".cookie-accept"
    ]
    
    for attempt in range(max_attempts):
        found_popup = False
        
        for selector in popup_selectors:
            try:
                if selector.startswith('//'):
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        try:
                            # Scroll into view and click
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                            time.sleep(0.3)
                            
                            if robust_element_click(driver, element):
                                dismissed_count += 1
                                found_popup = True
                                print(f"   ✅ Dismissed popup using: {selector}")
                                time.sleep(1)
                                break
                                
                        except Exception as e:
                            print(f"   ⚠️ Popup dismissal failed: {e}")
                            continue
                            
                if found_popup:
                    break
                    
            except Exception:
                continue
        
        if not found_popup:
            break
        
        time.sleep(0.5)
    
    return dismissed_count