"""
Browser Configuration Utilities
Ensures all browser instances run with visible windows
"""

import os
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_visible_chrome_options():
    """Get Chrome options that ensure visible browser window"""
    chrome_options = webdriver.ChromeOptions()
    
    # Essential visibility options
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--disable-background-mode")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    
    # Performance optimizations (while keeping visible)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    
    # Keep GPU enabled for Windows compatibility
    # chrome_options.add_argument("--disable-gpu")  # Removed for Windows
    
    # Anti-detection measures
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-notifications")
    
    # Popup and tab management
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-default-apps")
    
    # Preferences for visible operation
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_settings.popups": 0,
        "profile.managed_default_content_settings.images": 1,
        "profile.default_content_settings.multiple-automatic-downloads": 1
    })
    
    # NEVER add headless arguments
    # chrome_options.add_argument("--headless")  # FORBIDDEN
    
    return chrome_options


def create_visible_chrome_driver():
    """Create a Chrome driver instance that is always visible"""
    chrome_options = get_visible_chrome_options()
    
    try:
        # Try to use system Chrome installation first
        print("[INFO] Attempting to create Chrome driver...")
        
        # Clear any existing webdriver cache first
        clear_webdriver_cache()
        
        # Force fresh ChromeDriver download to ensure compatibility
        print("[INFO] Downloading fresh ChromeDriver for compatibility...")
        chrome_driver_path = ChromeDriverManager().install()
        print(f"[INFO] ChromeDriver installed at: {chrome_driver_path}")
        
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Force window to be visible and on top
        driver.maximize_window()
        
        # Windows-specific visibility enforcement
        import time
        time.sleep(2)  # Allow window to stabilize
        
        # Force focus and bring to foreground
        driver.execute_script("window.focus();")
        
        # Additional Windows visibility tricks
        try:
            import ctypes
            from ctypes import wintypes
            # Get window handle and force it to foreground
            hwnd = driver.current_window_handle
            if hwnd:
                ctypes.windll.user32.SetForegroundWindow(int(hwnd, 16))
        except:
            pass
        
        # Verify window is actually visible
        window_size = driver.get_window_size()
        window_position = driver.get_window_position()
        print(f"[INFO] Window size: {window_size['width']}x{window_size['height']}")
        print(f"[INFO] Window position: {window_position['x']}, {window_position['y']}")
        
        # Force window to screen if it's hidden
        if window_position['x'] < -100 or window_position['y'] < -100:
            driver.set_window_position(100, 100)
            driver.maximize_window()
        
        # Test page load to ensure driver is working
        driver.get("data:text/html,<html><body><h1>Browser Test OK</h1></body></html>")
        time.sleep(1)
        
        # Anti-detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_script("window.chrome = {runtime: {}};")
        
        # Enhanced single window enforcement - redirect all new tabs/windows to current tab
        driver.execute_script("""
            // Override window.open to redirect to current tab
            window.originalOpen = window.open;
            window.open = function(url, name, features) {
                console.log('Redirecting new window/tab to current tab:', url);
                if (url && url !== 'about:blank' && url !== '') {
                    window.location.href = url;
                }
                return window;
            };
            
            // Override target="_blank" links
            document.addEventListener('DOMContentLoaded', function() {
                const observer = new MutationObserver(function(mutations) {
                    mutations.forEach(function(mutation) {
                        mutation.addedNodes.forEach(function(node) {
                            if (node.nodeType === 1) {
                                // Handle links with target="_blank"
                                const blankLinks = node.querySelectorAll ? node.querySelectorAll('a[target="_blank"]') : [];
                                blankLinks.forEach(function(link) {
                                    link.setAttribute('target', '_self');
                                    console.log('Changed target="_blank" to target="_self" for:', link.href);
                                });
                                
                                // Handle the node itself if it's a link
                                if (node.tagName === 'A' && node.getAttribute('target') === '_blank') {
                                    node.setAttribute('target', '_self');
                                    console.log('Changed target="_blank" to target="_self" for:', node.href);
                                }
                            }
                        });
                    });
                });
                observer.observe(document.body, { childList: true, subtree: true });
                
                // Handle existing links
                const existingBlankLinks = document.querySelectorAll('a[target="_blank"]');
                existingBlankLinks.forEach(function(link) {
                    link.setAttribute('target', '_self');
                    console.log('Changed existing target="_blank" to target="_self" for:', link.href);
                });
            });
            
            // Prevent form submissions from opening new windows
            document.addEventListener('submit', function(event) {
                const form = event.target;
                if (form.target === '_blank') {
                    form.target = '_self';
                    console.log('Changed form target="_blank" to target="_self"');
                }
            });
        """)
        
        print("[SUCCESS] Visible Chrome browser created successfully")
        return driver
        
    except Exception as e:
        print(f"Chrome driver creation failed: {e}")
        # Try with minimal options
        try:
            minimal_options = webdriver.ChromeOptions()
            minimal_options.add_argument("--start-maximized")
            minimal_options.add_argument("--disable-blink-features=AutomationControlled")
            minimal_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=minimal_options)
            driver.maximize_window()
            driver.execute_script("window.focus();")
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("Visible Chrome browser created with minimal options")
            return driver
            
        except Exception as e2:
            print(f"Minimal Chrome setup also failed: {e2}")
            
            # Try to clear webdriver cache and retry once more
            try:
                print("\n[INFO] Attempting to clear webdriver cache and retry...")
                clear_webdriver_cache()
                
                # Final attempt with cache cleared and version matching
                print("[INFO] Downloading latest ChromeDriver...")
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=minimal_options)
                driver.maximize_window()
                driver.execute_script("window.focus();")
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                print("[SUCCESS] Visible Chrome browser created after cache clear")
                return driver
                
            except Exception as e3:
                print(f"Final attempt failed: {e3}")
                print("\n[TROUBLESHOOTING] Required steps:")
                print("1. Update Chrome to latest version")
                print("2. Run: pip install --upgrade webdriver-manager")
                print("3. Manually clear webdriver cache folder")
                print("4. Restart your terminal/IDE")
                print("5. Check if Chrome is properly installed")
                print("6. Try: pip uninstall webdriver-manager && pip install webdriver-manager")
                raise Exception("VISIBLE browser window is required but could not be created")


def ensure_window_visibility(driver):
    """Ensure the browser window remains visible"""
    try:
        # Maximize and bring to front
        driver.maximize_window()
        driver.execute_script("window.focus();")
        
        # Check window state
        window_size = driver.get_window_size()
        if window_size['width'] < 100 or window_size['height'] < 100:
            driver.maximize_window()
            print("Window was minimized, restored to full size")
        
        # Verify window is actually visible
        window_position = driver.get_window_position()
        if window_position['x'] < -1000 or window_position['y'] < -1000:
            driver.set_window_position(0, 0)
            driver.maximize_window()
            print("Window was off-screen, moved to visible area")
            
        print("Browser window visibility confirmed")
        return True
        
    except Exception as e:
        print(f"Failed to ensure window visibility: {e}")
        return False


def clear_webdriver_cache():
    """Clear webdriver-manager cache to fix corrupted drivers"""
    try:
        # Common webdriver cache locations
        cache_paths = [
            Path.home() / ".wdm",  # Linux/Mac
            Path(os.environ.get("USERPROFILE", "")) / ".wdm",  # Windows
            Path(os.environ.get("LOCALAPPDATA", "")) / ".wdm",  # Windows LocalAppData
        ]
        
        cleared_paths = []
        for cache_path in cache_paths:
            if cache_path.exists():
                try:
                    shutil.rmtree(cache_path)
                    cleared_paths.append(str(cache_path))
                except:
                    continue
        
        if cleared_paths:
            print(f"[SUCCESS] Cleared webdriver cache: {', '.join(cleared_paths)}")
        else:
            print("[INFO] No webdriver cache found to clear")
            
    except Exception as e:
        print(f"[WARNING] Cache clear failed: {e}")


def enforce_single_tab_mode(driver):
    """Enforce single tab execution for all navigation"""
    try:
        # Inject single tab enforcement script into current page
        driver.execute_script("""
            // Enhanced single tab enforcement
            window.originalOpen = window.open;
            window.open = function(url, name, features) {
                console.log('Intercepted window.open:', url);
                if (url && url !== 'about:blank' && url !== '') {
                    window.location.href = url;
                }
                return window;
            };
            
            // Handle all links dynamically
            function enforceSingleTab() {
                const links = document.querySelectorAll('a[target="_blank"], a[target="blank"]');
                links.forEach(function(link) {
                    link.setAttribute('target', '_self');
                });
                
                const forms = document.querySelectorAll('form[target="_blank"], form[target="blank"]');
                forms.forEach(function(form) {
                    form.setAttribute('target', '_self');
                });
            }
            
            // Run enforcement immediately and on DOM changes
            enforceSingleTab();
            if (typeof MutationObserver !== 'undefined') {
                const observer = new MutationObserver(enforceSingleTab);
                observer.observe(document.body, { childList: true, subtree: true });
            }
        """)
        
        # Close any additional tabs that might have opened
        handles = driver.window_handles
        if len(handles) > 1:
            main_handle = handles[0]
            for handle in handles[1:]:
                driver.switch_to.window(handle)
                driver.close()
            driver.switch_to.window(main_handle)
            print(f"[INFO] Closed {len(handles)-1} additional tabs")
        
        return True
    except Exception as e:
        print(f"[WARNING] Single tab enforcement failed: {e}")
        return False


def validate_no_headless_mode(chrome_options):
    """Validate that no headless mode is configured"""
    args = chrome_options.arguments
    
    for arg in args:
        if '--headless' in arg.lower():
            raise ValueError("HEADLESS MODE DETECTED! All tests must run with visible browser window")
    
    print("No headless mode detected - browser will be visible")
    return True