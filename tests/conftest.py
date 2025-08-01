"""
Pytest configuration - Enhanced setup with reporting
"""

import pytest
import time
from datetime import datetime
from utils.browser_config import create_visible_chrome_driver
from utils.test_helpers import ensure_directories, take_screenshot
from utils.enhanced_reporting import enhanced_reporter


@pytest.fixture(scope="session")
def browser_setup():
    """Single browser session for all tests with enhanced reporting"""
    print("[SETUP] Setting up browser and enhanced reporting...")
    
    ensure_directories()
    enhanced_reporter.start_session()
    
    driver = create_visible_chrome_driver()
    
    yield driver
    
    print("[CLEANUP] Closing browser and generating reports...")
    enhanced_reporter.end_session()
    
    # Generate enhanced reports
    html_report = enhanced_reporter.generate_enhanced_html_report()
    json_report = enhanced_reporter.generate_json_report()
    
    print(f"[REPORTS] Enhanced HTML report: {html_report}")
    print(f"[REPORTS] JSON report: {json_report}")
    
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Enhanced test reporting with screenshots and metrics"""
    start_time = time.time()
    outcome = yield
    end_time = time.time()
    rep = outcome.get_result()
    
    if rep.when == "call":
        duration = end_time - start_time
        
        # Determine test status
        if rep.passed:
            status = "passed"
            error_message = None
        elif rep.failed:
            status = "failed"
            error_message = str(rep.longrepr) if rep.longrepr else "Test failed"
        else:
            status = "skipped"
            error_message = str(rep.longrepr) if rep.longrepr else None
        
        # Take screenshot on failure
        screenshot_path = None
        if rep.failed and hasattr(item, "funcargs") and "browser_setup" in item.funcargs:
            driver = item.funcargs["browser_setup"]
            screenshot_path = take_screenshot(driver, f"FAILED_{item.name}")
            enhanced_reporter.add_screenshot(screenshot_path, f"Failure screenshot for {item.name}")
        
        # Add test result to enhanced reporter
        enhanced_reporter.add_test_result(
            test_name=item.name,
            status=status,
            duration=duration,
            error_message=error_message,
            screenshot_path=screenshot_path
        )
        
        # Add performance metric
        if duration > 0:
            enhanced_reporter.add_performance_metric(f"test_{item.name}_duration", duration)


def pytest_configure(config):
    """Configure pytest markers and enhanced reporting"""
    config.addinivalue_line("markers", "basic: Basic functionality tests")
    config.addinivalue_line("markers", "advanced: Advanced test scenarios with comprehensive validation")
    config.addinivalue_line("markers", "both: Combined basic and advanced test workflows")
    
    # Configure enhanced HTML reports
    config.option.htmlpath = f"reports/pytest_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"


def pytest_sessionstart(session):
    """Session start hook"""
    print(f"[SESSION] Starting Amazon India test session at {datetime.now()}")


def pytest_sessionfinish(session, exitstatus):
    """Session finish hook"""
    print(f"[SESSION] Test session completed with exit status: {exitstatus}")
    
    # Add session-level performance metrics
    if hasattr(session, 'testscollected'):
        enhanced_reporter.add_performance_metric("total_tests_collected", session.testscollected, "tests")