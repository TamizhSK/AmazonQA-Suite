

import pytest
import time
import random
import re
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException


@pytest.mark.basic
class TestAmazonBasic:
    """Basic Amazon India functionality tests - Essential features only"""
    
    def test_homepage_load(self, browser_setup):
        """Test Amazon India homepage loads correctly"""
        driver = browser_setup
        
        driver.get("https://www.amazon.in")
        time.sleep(3)  # Allow page to fully load
        
        # Basic element verification
        assert "Amazon" in driver.title
        
        # Wait for search box to be visible (it's the most reliable element)
        wait = WebDriverWait(driver, 15)
        search_box = wait.until(EC.element_to_be_clickable((By.NAME, "field-keywords")))
        assert search_box.is_displayed()
        
        print(" Homepage loaded successfully")
    
    def test_basic_search(self, browser_setup):
        """Test basic search functionality"""
        driver = browser_setup
        wait = WebDriverWait(driver, 15)
        
        driver.get("https://www.amazon.in")
        time.sleep(3)  # Allow page to fully load
        
        search_box = wait.until(EC.element_to_be_clickable((By.NAME, "field-keywords")))
        search_box.clear()
        search_box.send_keys("laptop")
        search_box.send_keys(Keys.RETURN)
        
        # Wait for results
        results = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "[data-component-type='s-search-result']")
        ))
        
        assert len(results) >= 5, f"Expected at least 5 results, got {len(results)}"
        print(f" Found {len(results)} search results")
    
    def test_product_page_navigation(self, browser_setup):
        """Test navigation to product page"""
        driver = browser_setup
        wait = WebDriverWait(driver, 15)
        
        driver.get("https://www.amazon.in")
        time.sleep(3)  # Allow page to fully load
        
        # Search and click first product
        search_box = wait.until(EC.element_to_be_clickable((By.NAME, "field-keywords")))
        search_box.clear()
        search_box.send_keys("books")
        search_box.send_keys(Keys.RETURN)
        
        # Wait for search results with multiple selector strategies
        first_product = None
        selectors_to_try = [
            (By.CSS_SELECTOR, "[data-component-type='s-search-result'] h2 a"),
            (By.CSS_SELECTOR, ".s-result-item .a-link-normal"),
            (By.CSS_SELECTOR, "[data-cy='title-recipe-fixer']"),
        ]
        
        for selector_type, selector in selectors_to_try:
            try:
                first_product = wait.until(EC.element_to_be_clickable((selector_type, selector)))
                break
            except:
                continue
        
        assert first_product is not None, "Could not find any clickable product"
        first_product.click()
        
        # Verify product page with multiple selectors
        product_page_found = False
        product_selectors = [
            (By.ID, "productTitle"),
            (By.CSS_SELECTOR, "h1"),
            (By.CSS_SELECTOR, ".a-page-title"),
        ]
        
        for selector_type, selector in product_selectors:
            try:
                product_element = wait.until(EC.presence_of_element_located((selector_type, selector)))
                if product_element.is_displayed():
                    product_page_found = True
                    break
            except:
                continue
        
        assert product_page_found, "Product page elements not found"
        print(" Product page navigation successful")




@pytest.mark.advanced
class TestAmazonAdvanced:
    """Advanced Amazon India testing with comprehensive validation and automation"""
    
    @classmethod 
    def setup_class(cls):
        """Setup advanced test data and configuration"""
        cls.test_data = {
            "search_terms": {
                "electronics": ["laptop dell", "iphone 15", "samsung galaxy", "wireless headphones"],
                "fashion": ["men shirts formal", "women dresses", "sports shoes nike"],
                "books": ["python programming", "fiction novels", "cookbooks indian"],
                "edge_cases": ["", "   ", "!@#$%^&*()", "verylongquerywithoutanyspaces123456789"],
                "price_based": ["laptop under 50000", "mobile under 20000", "books under 500"]
            },
            "categories": ["Electronics", "Books", "Fashion", "Home & Kitchen"],
            "price_limits": {
                "books under 500": 500,
                "mobile under 20000": 20000,
                "laptop under 50000": 50000
            }
        }
    
    def advanced_wait_for_element(self, driver, locator, timeout=15, condition="presence"):
        """Advanced element waiting with multiple strategies"""
        wait = WebDriverWait(driver, timeout)
        
        conditions = {
            "presence": EC.presence_of_element_located,
            "visible": EC.visibility_of_element_located,
            "clickable": EC.element_to_be_clickable,
        }
        
        try:
            return wait.until(conditions.get(condition, EC.presence_of_element_located)(locator))
        except TimeoutException:
            self.capture_screenshot(driver, f"element_wait_failed_{condition}")
            return None
    
    def intelligent_popup_dismissal(self, driver):
        """Advanced popup dismissal with multiple strategies"""
        popup_selectors = [
            # Continue shopping (highest priority)
            "//button[contains(text(), 'Continue shopping')]",
            "//span[contains(text(), 'Continue shopping')]/parent::button",
            "//a[contains(text(), 'Continue shopping')]",
            
            # General close buttons
            "//button[contains(text(), 'Close')]",
            "//button[contains(text(), 'No thanks')]",
            "//button[contains(text(), 'Not now')]",
            "//button[contains(text(), 'Skip')]",
            "//button[contains(text(), 'Maybe later')]",
            
            # CSS selectors
            ".a-modal-close",
            ".a-button-close",
            "[data-action='close']",
            "[aria-label*='Close']"
        ]
        
        dismissed_count = 0
        for attempt in range(3):
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
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                                time.sleep(0.3)
                                element.click()
                                dismissed_count += 1
                                found_popup = True
                                print(f"✓ Dismissed popup using: {selector}")
                                time.sleep(1)
                                break
                            except:
                                # Try JavaScript click
                                try:
                                    driver.execute_script("arguments[0].click();", element)
                                    dismissed_count += 1
                                    found_popup = True
                                    time.sleep(1)
                                    break
                                except:
                                    continue
                    if found_popup:
                        break
                except:
                    continue
            
            if not found_popup:
                break
            time.sleep(0.5)
        
        return dismissed_count
    
    def extract_comprehensive_product_data(self, driver, max_products=10):
        """Extract detailed product information with multiple fallback strategies"""
        products_data = []
        
        try:
            # Multiple selectors for product containers
            product_selectors = [
                "[data-component-type='s-search-result']",
                ".s-result-item",
                ".sg-row .sg-col-inner"
            ]
            
            products = []
            for selector in product_selectors:
                products = driver.find_elements(By.CSS_SELECTOR, selector)
                if products and len(products) >= 3:
                    break
            
            if not products:
                return products_data
            
            for i, product in enumerate(products[:max_products]):
                try:
                    product_info = {
                        "index": i + 1,
                        "title": self.extract_product_title(product),
                        "price": self.extract_product_price(product),
                        "rating": self.extract_product_rating(product),
                        "availability": self.extract_availability(product),
                        "image_present": self.check_image_presence(product),
                        "has_prime": self.check_prime_badge(product)
                    }
                    
                    if product_info["title"]:  # Only add if we found a title
                        products_data.append(product_info)
                        
                except Exception as e:
                    print(f"Error extracting product {i}: {e}")
                    continue
            
            return products_data
            
        except Exception as e:
            print(f"Product data extraction failed: {e}")
            return products_data
    
    def extract_product_title(self, product_element):
        """Extract product title with multiple strategies"""
        title_selectors = [
            "h2 a span",
            ".a-link-normal .a-text-normal",
            "[data-cy='title-recipe-fixer']",
            ".s-size-mini .a-color-base",
            "h2 .a-link-normal"
        ]
        
        for selector in title_selectors:
            try:
                element = product_element.find_element(By.CSS_SELECTOR, selector)
                title = element.text.strip()
                if title and len(title) > 10:
                    return title
            except (NoSuchElementException, AttributeError):
                continue
        return None
    
    def extract_product_price(self, product_element):
        """Extract product price with currency validation"""
        price_selectors = [
            ".a-price-whole",
            ".a-price .a-offscreen",
            ".a-price-range .a-offscreen",
            ".a-price-symbol + .a-price-whole"
        ]
        
        for selector in price_selectors:
            try:
                element = product_element.find_element(By.CSS_SELECTOR, selector)
                price_text = element.text.strip() or element.get_attribute("textContent").strip()
                
                # Extract numeric price
                price_match = re.search(r'[\d,]+', price_text.replace(',', ''))
                if price_match:
                    price = int(price_match.group().replace(',', ''))
                    if 50 <= price <= 1000000:  # Reasonable price range
                        return price
            except (NoSuchElementException, ValueError, AttributeError):
                continue
        return None
    
    def extract_product_rating(self, product_element):
        """Extract product rating"""
        rating_selectors = [
            ".a-icon-alt",
            "[aria-label*='out of 5 stars']",
            ".a-icon-star .a-icon-alt"
        ]
        
        for selector in rating_selectors:
            try:
                element = product_element.find_element(By.CSS_SELECTOR, selector)
                rating_text = element.get_attribute("textContent") or element.text
                rating_match = re.search(r'(\d+\.?\d*)\s*out of', rating_text)
                if rating_match:
                    return float(rating_match.group(1))
            except (NoSuchElementException, ValueError, AttributeError):
                continue
        return None
    
    def extract_availability(self, product_element):
        """Check product availability"""
        try:
            availability_indicators = product_element.find_elements(By.CSS_SELECTOR, 
                ".a-color-success, .a-color-price, [aria-label*='In stock']")
            for indicator in availability_indicators:
                text = indicator.text.lower()
                if "in stock" in text or "available" in text:
                    return "Available"
        except:
            pass
        return "Unknown"
    
    def check_image_presence(self, product_element):
        """Check if product has image"""
        try:
            image = product_element.find_element(By.CSS_SELECTOR, ".s-image, img[data-image-latency]")
            return image.get_attribute("src") is not None
        except:
            return False
    
    def check_prime_badge(self, product_element):
        """Check if product has Prime badge"""
        try:
            prime_elements = product_element.find_elements(By.CSS_SELECTOR, 
                "[aria-label*='Prime'], .a-icon-prime, [alt*='Prime']")
            return len(prime_elements) > 0
        except:
            return False
    
    def perform_advanced_search_with_validation(self, driver, search_term):
        """Perform search with comprehensive validation"""
        try:
            # Navigate if needed
            if "amazon.in" not in driver.current_url:
                driver.get("https://www.amazon.in")
            
            # Dismiss any popups
            self.intelligent_popup_dismissal(driver)
            
            # Find search box with advanced waiting
            search_box = self.advanced_wait_for_element(driver, (By.CSS_SELECTOR, "input[name='field-keywords']"), condition="clickable")
            if not search_box:
                return False, "Search box not found"
            
            # Clear and perform human-like typing
            search_box.clear()
            time.sleep(0.5)
            
            for char in search_term:
                search_box.send_keys(char)
                time.sleep(random.uniform(0.03, 0.12))  # Human-like typing
            
            # Submit search
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results with multiple strategies
            result_indicators = [
                (By.CSS_SELECTOR, "[data-component-type='s-search-result']"),
                (By.CSS_SELECTOR, ".s-result-item"),
                (By.CSS_SELECTOR, ".sg-row")
            ]
            
            for locator in result_indicators:
                if self.advanced_wait_for_element(driver, locator, timeout=10):
                    return True, "Search successful"
            
            return False, "No results found"
            
        except Exception as e:
            return False, f"Search failed: {e}"
    
    def validate_price_accuracy(self, products_data, expected_max_price, tolerance_percent=25):
        """Validate price accuracy with detailed reporting"""
        if not products_data:
            return {"accuracy": 0, "details": "No products to validate"}
        
        valid_prices = []
        invalid_prices = []
        tolerance_amount = expected_max_price * (tolerance_percent / 100)
        max_allowed = expected_max_price + tolerance_amount
        
        for product in products_data:
            if product.get("price"):
                if product["price"] <= max_allowed:
                    valid_prices.append(product["price"])
                else:
                    invalid_prices.append({
                        "title": product.get("title", "Unknown")[:50],
                        "price": product["price"],
                        "expected_max": expected_max_price
                    })
        
        total_with_prices = len(valid_prices) + len(invalid_prices)
        accuracy = (len(valid_prices) / total_with_prices * 100) if total_with_prices > 0 else 0
        
        return {
            "accuracy": accuracy,
            "valid_count": len(valid_prices),
            "invalid_count": len(invalid_prices),
            "total_products": len(products_data),
            "products_with_prices": total_with_prices,
            "invalid_products": invalid_prices[:3],  # Show first 3 invalid products
            "passed": accuracy >= 70  # 70% accuracy threshold
        }
    
    def advanced_mouse_interactions(self, driver, product_elements):
        """Perform advanced mouse interactions with products"""
        interactions_successful = 0
        
        for i, product in enumerate(product_elements[:3]):  # Test first 3 products
            try:
                # Scroll to product
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product)
                time.sleep(0.5)
                
                # Hover over product
                actions = ActionChains(driver)
                actions.move_to_element(product).perform()
                time.sleep(random.uniform(0.8, 1.5))
                
                # Try to find and hover over image
                try:
                    image = product.find_element(By.CSS_SELECTOR, ".s-image, img")
                    actions.move_to_element(image).perform()
                    time.sleep(0.5)
                    interactions_successful += 1
                except:
                    pass
                
                # Move mouse in realistic pattern
                actions.move_by_offset(random.randint(-20, 20), random.randint(-10, 10)).perform()
                time.sleep(0.3)
                
            except Exception as e:
                print(f"Mouse interaction {i} failed: {e}")
                continue
        
        return interactions_successful
    
    def capture_screenshot(self, driver, name):
        """Capture screenshot for debugging"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshots/{name}_{timestamp}.png"
            os.makedirs("screenshots", exist_ok=True)
            driver.save_screenshot(filename)
            return filename
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return None
    
    def measure_performance(self, driver, operation_name, operation_func):
        """Measure operation performance"""
        start_time = time.time()
        try:
            result = operation_func()
            execution_time = time.time() - start_time
            return {"success": True, "time": execution_time, "result": result}
        except Exception as e:
            execution_time = time.time() - start_time
            return {"success": False, "time": execution_time, "error": str(e)}
    

    
    def test_comprehensive_search_with_categories(self, browser_setup):
        """Test comprehensive search across multiple categories with validation"""
        driver = browser_setup
        search_results = {}
        
        for category, terms in self.test_data["search_terms"].items():
            if category == "edge_cases":
                continue  # Skip edge cases for main test
                
            category_results = []
            
            for term in terms[:2]:  # Test first 2 terms from each category
                success, message = self.perform_advanced_search_with_validation(driver, term)
                
                if success:
                    products_data = self.extract_comprehensive_product_data(driver, max_products=8)
                    
                    # Calculate search relevance
                    relevance_score = self.calculate_search_relevance(term, products_data)
                    
                    result_info = {
                        "term": term,
                        "success": True,
                        "products_found": len(products_data),
                        "products_with_prices": sum(1 for p in products_data if p.get("price")),
                        "products_with_ratings": sum(1 for p in products_data if p.get("rating")),
                        "relevance_score": relevance_score,
                        "products": products_data[:3]  # Store first 3 products
                    }
                else:
                    result_info = {
                        "term": term,
                        "success": False,
                        "error": message,
                        "products_found": 0
                    }
                
                category_results.append(result_info)
                time.sleep(2)  # Rate limiting
            
            search_results[category] = category_results
        
        # Validate overall results
        total_searches = sum(len(results) for results in search_results.values())
        successful_searches = sum(1 for results in search_results.values() 
                                for result in results if result.get("success", False))
        
        success_rate = successful_searches / total_searches if total_searches > 0 else 0
        
        assert success_rate >= 0.75, f"Search success rate too low: {success_rate:.2f}"
        
        print(f" Comprehensive search test passed - Success rate: {success_rate:.2f}")
        print(f"   Categories tested: {len(search_results)}")
        print(f"   Total searches: {total_searches}")
        print(f"   Successful searches: {successful_searches}")
    
    def test_advanced_price_validation_with_accuracy(self, browser_setup):
        """Test price validation with comprehensive accuracy reporting"""
        driver = browser_setup
        price_validation_results = []
        
        for search_term, price_limit in self.test_data["price_limits"].items():
            success, message = self.perform_advanced_search_with_validation(driver, search_term)
            
            if success:
                products_data = self.extract_comprehensive_product_data(driver, max_products=10)
                
                if len(products_data) >= 3:  # Minimum products required
                    validation_result = self.validate_price_accuracy(products_data, price_limit)
                    
                    test_result = {
                        "search_term": search_term,
                        "price_limit": price_limit,
                        "products_found": len(products_data),
                        "validation": validation_result,
                        "passed": validation_result["passed"]
                    }
                    
                    price_validation_results.append(test_result)
                    
                    print(f"   {search_term}: {validation_result['accuracy']:.1f}% accurate "
                          f"({validation_result['valid_count']}/{validation_result['products_with_prices']} valid prices)")
                    
                    assert validation_result["passed"], \
                        f"Price validation failed for '{search_term}': {validation_result['accuracy']:.1f}% accuracy"
                
                time.sleep(2)  # Rate limiting
        
        # Overall validation
        if price_validation_results:
            overall_accuracy = sum(r["validation"]["accuracy"] for r in price_validation_results) / len(price_validation_results)
            passed_tests = sum(1 for r in price_validation_results if r["passed"])
            
            assert overall_accuracy >= 70, f"Overall price accuracy too low: {overall_accuracy:.1f}%"
            
            print(f" Advanced price validation passed")
            print(f"   Overall accuracy: {overall_accuracy:.1f}%")
            print(f"   Tests passed: {passed_tests}/{len(price_validation_results)}")
    
    def test_advanced_product_interaction_with_mouse_automation(self, browser_setup):
        """Test advanced product interactions with mouse automation"""
        driver = browser_setup
        
        # Search for products
        success, message = self.perform_advanced_search_with_validation(driver, "wireless headphones")
        assert success, f"Search failed: {message}"
        
        # Get product elements
        products = driver.find_elements(By.CSS_SELECTOR, "[data-component-type='s-search-result']")
        assert len(products) >= 3, f"Insufficient products found: {len(products)}"
        
        # Perform advanced mouse interactions
        interaction_score = self.advanced_mouse_interactions(driver, products)
        
        # Test product page navigation
        navigation_successful = 0
        for i, product in enumerate(products[:2]):  # Test first 2 products
            try:
                # Get product link
                title_link = product.find_element(By.CSS_SELECTOR, "h2 a")
                original_url = driver.current_url
                
                # Advanced click with JavaScript fallback
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_link)
                    time.sleep(0.5)
                    title_link.click()
                except:
                    driver.execute_script("arguments[0].click();", title_link)
                
                # Validate product page
                try:
                    WebDriverWait(driver, 8).until(
                        EC.any_of(
                            EC.presence_of_element_located((By.ID, "productTitle")),
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".a-price")),
                            EC.presence_of_element_located((By.ID, "add-to-cart-button"))
                        )
                    )
                    navigation_successful += 1
                    print(f"   Product {i+1}: Navigation successful")
                except TimeoutException:
                    print(f"   Product {i+1}: Navigation failed - page elements not found")
                
                # Return to search results
                driver.back()
                time.sleep(2)
                
            except Exception as e:
                print(f"   Product {i+1}: Interaction failed - {e}")
                continue
        
        # Calculate success rates
        interaction_success_rate = interaction_score / len(products[:3]) if products[:3] else 0
        navigation_success_rate = navigation_successful / 2 if 2 > 0 else 0
        
        # Assertions
        assert interaction_success_rate >= 0.6, f"Mouse interaction success rate too low: {interaction_success_rate:.2f}"
        assert navigation_success_rate >= 0.5, f"Product navigation success rate too low: {navigation_success_rate:.2f}"
        
        print(f" Advanced product interaction test passed")
        print(f"   Mouse interactions: {interaction_score}/{len(products[:3])} successful")
        print(f"   Product navigation: {navigation_successful}/2 successful")
    
    def test_performance_and_comprehensive_validation(self, browser_setup):
        """Test performance with comprehensive validation"""
        driver = browser_setup
        performance_metrics = {}
        
        # Homepage load performance
        homepage_perf = self.measure_performance(driver, "homepage_load", 
            lambda: driver.get("https://www.amazon.in"))
        
        performance_metrics["homepage_load"] = homepage_perf
        assert homepage_perf["success"], "Homepage load failed"
        assert homepage_perf["time"] < 12, f"Homepage load too slow: {homepage_perf['time']:.2f}s"
        
        # Search performance
        search_terms = ["laptop", "mobile", "books"]
        search_times = []
        
        for term in search_terms:
            search_perf = self.measure_performance(driver, f"search_{term}",
                lambda: self.perform_advanced_search_with_validation(driver, term))
            
            if search_perf["success"] and search_perf["result"][0]:  # If search was successful
                search_times.append(search_perf["time"])
            
            time.sleep(1)
        
        if search_times:
            avg_search_time = sum(search_times) / len(search_times)
            performance_metrics["average_search_time"] = avg_search_time
            assert avg_search_time < 8, f"Average search time too slow: {avg_search_time:.2f}s"
        
        # Data extraction performance
        if search_times:  # If we have successful searches
            extraction_perf = self.measure_performance(driver, "data_extraction",
                lambda: self.extract_comprehensive_product_data(driver, max_products=15))
            
            performance_metrics["data_extraction"] = extraction_perf
            assert extraction_perf["success"], "Data extraction failed"
            
            if extraction_perf["result"]:
                extracted_count = len(extraction_perf["result"])
                assert extracted_count >= 5, f"Insufficient data extracted: {extracted_count}"
        
        # Memory and page metrics
        try:
            page_metrics = driver.execute_script("""
                return {
                    memory_used: window.performance.memory ? window.performance.memory.usedJSHeapSize : null,
                    navigation_timing: window.performance.timing ? {
                        load_time: window.performance.timing.loadEventEnd - window.performance.timing.navigationStart,
                        dom_ready: window.performance.timing.domContentLoadedEventEnd - window.performance.timing.navigationStart
                    } : null,
                    page_size: document.documentElement.innerHTML.length
                };
            """)
            performance_metrics["page_metrics"] = page_metrics
        except:
            print("   Browser performance metrics not available")
        
        print(f" Performance and validation test passed")
        print(f"   Homepage load: {homepage_perf['time']:.2f}s")
        if search_times:
            print(f"   Average search: {avg_search_time:.2f}s")
        print(f"   All performance thresholds met")
    
    def calculate_search_relevance(self, search_term, products_data):
        """Calculate search relevance score"""
        if not products_data or not search_term.strip():
            return 0
        
        relevant_count = 0
        search_words = [word.lower() for word in search_term.split() if len(word) > 2]
        
        for product in products_data:
            if product.get("title"):
                title_lower = product["title"].lower()
                if any(word in title_lower for word in search_words):
                    relevant_count += 1
        
        return (relevant_count / len(products_data)) * 100 if products_data else 0




@pytest.mark.both
class TestAmazonBoth:
    """Combined basic and advanced testing - Full comprehensive suite"""
    
    def test_complete_workflow_basic_to_advanced(self, browser_setup):
        """Complete workflow from basic to advanced testing"""
        driver = browser_setup
        
        # Phase 1: Basic validation
        print("🔷 Phase 1: Basic Validation")
        driver.get("https://www.amazon.in")
        assert "Amazon" in driver.title
        
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='field-keywords']"))
        )
        search_box.clear()
        search_box.send_keys("smartphone")
        search_box.send_keys(Keys.RETURN)
        
        # Wait for basic results
        basic_results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-component-type='s-search-result']"))
        )
        assert len(basic_results) >= 5, "Basic search failed"
        print(f"    Basic search: {len(basic_results)} results found")
        
        # Phase 2: Advanced validation
        print("🔷 Phase 2: Advanced Validation")
        advanced_tester = TestAmazonAdvanced()
        
        # Extract comprehensive data
        products_data = advanced_tester.extract_comprehensive_product_data(driver, max_products=10)
        assert len(products_data) >= 5, "Advanced data extraction failed"
        
        # Validate data quality
        products_with_prices = sum(1 for p in products_data if p.get("price"))
        products_with_ratings = sum(1 for p in products_data if p.get("rating"))
        
        assert products_with_prices >= 3, f"Insufficient price data: {products_with_prices}"
        print(f"    Advanced extraction: {len(products_data)} products, {products_with_prices} with prices")
        
        # Phase 3: Interactive validation
        print("🔷 Phase 3: Interactive Validation")
        interaction_score = advanced_tester.advanced_mouse_interactions(driver, basic_results[:3])
        assert interaction_score >= 1, "Mouse interactions failed"
        print(f"    Mouse interactions: {interaction_score}/3 successful")
        
        print(" Complete workflow test passed - Basic to Advanced integration successful")