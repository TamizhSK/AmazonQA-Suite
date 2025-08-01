# Amazon India Test Suite

A comprehensive Selenium automation framework for testing Amazon India's e-commerce functionality with Python 3.8+ compatibility, single-window execution, and enhanced reporting capabilities.

## Test Categories Overview

### BASIC Tests
**Purpose**: Essential functionality validation  
**Scope**: Core features with enhanced reliability  
**Duration**: 3-5 minutes  

**Test Coverage**:
- Homepage load validation with single tab enforcement
- Search functionality with edge case handling
- Product page navigation with error handling
- India-specific search term validation
- Basic filter functionality
- Responsive design validation

### ADVANCED Tests
**Purpose**: Deep functional testing and comprehensive automation  
**Scope**: Complex workflows with enhanced capabilities  
**Duration**: 15-20 minutes  

**Test Coverage**:
- Multi-category search validation (electronics, fashion, books)
- Advanced price validation with accuracy reporting (40-50% realistic thresholds)
- Authentication flow simulation (email/mobile/OTP without actual login)
- Comprehensive redirection testing
- OTP and login flow simulation with Indian mobile numbers
- Advanced language support (Hindi/Tamil/Telugu/Kannada)
- Location changing with pincode validation
- Edge case search handling
- Comprehensive filter testing (price, brand, rating)
- Product interaction with mouse automation
- Performance monitoring with detailed metrics

### BOTH Tests
**Purpose**: Complete workflow integration  
**Scope**: Full comprehensive testing pipeline  
**Duration**: 15-20 minutes  

**Test Coverage**:
- Complete workflow from basic to advanced testing
- Enhanced reporting with screenshots and metrics
- Single window execution throughout

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Chrome browser (latest version)
- 8GB+ RAM (recommended for advanced tests)
- Stable internet connection

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd Amazon-Test_Suite

# Install dependencies
pip install -r requirements.txt
```

### Dependency Overview
```txt
# Core Selenium
selenium>=4.16.0,<5.0.0
webdriver-manager>=4.0.1,<5.0.0

# Testing Framework
pytest>=7.4.0,<8.0.0
pytest-html>=4.1.1,<5.0.0
pytest-xdist>=3.3.1,<4.0.0

# HTTP and Data Processing
requests>=2.31.0,<3.0.0
Pillow>=10.0.0,<11.0.0
beautifulsoup4>=4.12.0,<5.0.0

# Reporting and Utilities
colorlog>=6.7.0,<7.0.0
tabulate>=0.9.0,<1.0.0
faker>=20.0.0,<21.0.0
```

## Project Structure

```
Amazon-Test_Suite/
├── tests/
│   ├── conftest.py                # Pytest configuration with enhanced reporting
│   ├── test_amazon_complete.py    # Main comprehensive test suite
│   └── test_amazon_india.py       # Legacy reference implementation
├── utils/
│   ├── browser_config.py          # Single tab browser configuration
│   ├── test_helpers.py            # Enhanced utilities and helper functions
│   └── enhanced_reporting.py      # HTML and JSON reporting system
├── reports/                       # Generated HTML and JSON reports
├── screenshots/                   # Automatic failure screenshots
├── run_tests.py                   # Main test runner with category selection
├── requirements.txt               # Python dependencies
└── README.md                     # Project documentation
```

## Usage

### Interactive Mode (Recommended)
```bash
python run_tests.py
```

**Available Options**:
1. Run BASIC Tests (Essential functionality)
2. Run ADVANCED Tests (Comprehensive validation)
3. Run BOTH Tests (Complete suite)
4. Run Specific Test
5. Show Test Categories Info
6. Check Environment
7. Clean Artifacts

### Command Line Mode
```bash
# Execute specific test categories
python run_tests.py --basic      # Basic tests only
python run_tests.py --advanced   # Advanced tests only
python run_tests.py --both       # Complete test suite
```

## Key Features

### Single Window Execution
- All tests execute in a single browser instance
- Automatic prevention of new tabs/windows
- Intelligent tab management and cleanup
- Optimized memory usage and performance

### Enhanced Reporting
- Interactive HTML reports with progressive design
- Automatic screenshot capture on failures
- Performance metrics and timing analysis
- JSON reports for CI/CD integration
- Real-time report generation during execution

### Advanced Testing Capabilities
- Edge case handling for unusual inputs
- Authentication flow simulation without actual login
- Comprehensive localization testing
- Filter validation across multiple categories
- Specialized testing for Indian e-commerce scenarios

## Core Test Functions

### Data Extraction
```python
def extract_comprehensive_product_data(self, driver, max_products=10):
    """
    Extract detailed product information with fallback strategies
    Returns: title, price, rating, availability, image_present, has_prime
    """
```

### Popup Management
```python
def intelligent_popup_dismissal(self, driver):
    """
    Advanced popup dismissal using multiple strategies
    Handles: Continue shopping buttons, close buttons, modal overlays
    Uses: XPath, CSS selectors, JavaScript fallbacks
    """
```

### Mouse Automation
```python
def advanced_mouse_interactions(self, driver, product_elements):
    """
    Perform realistic mouse interactions with products
    Features: Hover effects, realistic movements, interaction validation
    """
```

### Price Validation
```python
def validate_price_accuracy(self, products_data, expected_max_price, tolerance_percent=25):
    """
    Validate price accuracy with detailed reporting
    Returns: accuracy percentage, valid/invalid counts, analysis
    """
```

### Performance Monitoring
```python
def measure_performance(self, driver, operation_name, operation_func):
    """
    Measure operation performance with comprehensive metrics
    Tracks: execution time, success rate, detailed error reporting
    """
```

## Test Validation Criteria

### BASIC Tests Thresholds
- Homepage must load with all essential elements
- Search functionality must return minimum 5 results
- Product pages must be accessible and navigable

### ADVANCED Tests Thresholds
- **Search Success Rate**: Minimum 75%
- **Price Accuracy**: Minimum 70% with 25% tolerance
- **Search Relevance**: Minimum 30% relevance score
- **Mouse Interactions**: Minimum 60% success rate
- **Performance Limits**: Homepage <12s, Search <8s

### Multi-Category Search Validation
**Electronics**: laptop dell, iphone 15, samsung galaxy, wireless headphones  
**Fashion**: men shirts formal, women dresses, sports shoes nike  
**Books**: python programming, fiction novels, cookbooks indian  
**Edge Cases**: empty strings, special characters, extended queries  

### Price Validation Scenarios
- "books under 500" - Budget category testing
- "mobile under 20000" - Mid-range electronics
- "laptop under 50000" - High-value electronics
- 25% price tolerance for validation
- 70% minimum accuracy threshold required

## Performance Benchmarks

### Load Time Thresholds
- **Homepage Load**: Maximum 12 seconds
- **Search Response**: Average 8 seconds
- **Data Extraction**: Tracked with performance monitoring
- **Memory Usage**: JavaScript heap usage monitoring

### Success Rate Requirements
- **Search Operations**: 75% minimum success rate
- **Product Interactions**: 60% minimum success rate
- **Price Validation**: 70% accuracy threshold
- **Relevance Scoring**: 30% minimum relevance

## Environment Validation

### System Requirements
- **Operating System**: Windows/Linux/Mac compatible
- **Python Version**: 3.8, 3.9, 3.10, 3.11, or 3.12
- **Memory**: 8GB+ RAM recommended for advanced tests
- **Browser**: Chrome (automatically managed via webdriver-manager)
- **Network**: Stable internet connection required

### Environment Check
```bash
python run_tests.py
# Select option 6: Check Environment
```

## Troubleshooting

### Common Issues

**Browser Not Displaying**:
- Run environment check to validate browser setup
- Ensure Chrome is installed and up-to-date
- Check firewall/antivirus blocking browser automation

**Test Failures**:
- Review screenshots in `screenshots/FAILED_*` directory
- Check HTML reports in `reports/` folder
- Examine console output for detailed error messages
- Verify network connectivity and Amazon accessibility

**Performance Issues**:
- Close other browser instances before testing
- Ensure minimum 8GB RAM for advanced tests
- Check system resource availability
- Verify stable internet connection

### Report Generation
- **HTML Reports**: Located in `reports/` directory with embedded screenshots
- **JSON Reports**: Machine-readable format for CI/CD integration
- **Screenshots**: Automatic capture on test failures
- **Performance Metrics**: Detailed timing and resource usage data

## Development Guidelines

### Code Organization
- All test logic consolidated in `test_amazon_complete.py`
- Helper functions separated in `utils/` directory
- Configuration management in `browser_config.py`
- Reporting system isolated in `enhanced_reporting.py`

### Best Practices
- Single window execution to prevent resource conflicts
- Comprehensive error handling with detailed logging
- Modular design with clear separation of concerns
- Performance monitoring integrated throughout test execution
- Automatic cleanup and resource management

### Extension Points
- Custom test categories can be added to the runner
- Additional validation criteria can be integrated
- Reporting formats can be extended
- Browser configurations can be customized

This framework provides a comprehensive testing solution for Amazon India's e-commerce functionality with clear categorization, professional reporting, and robust validation criteria suitable for both development and production environments.
