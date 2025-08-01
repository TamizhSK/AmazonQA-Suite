
import subprocess
import sys
import os
from datetime import datetime


def show_banner():
    """Display test runner banner"""
    print("=" * 70)
    print("Amazon India Test Suite - Basic | Advanced | Both")
    print("=" * 70)
    print("[BASIC] Essential functionality testing")
    print("[ADVANCED] Comprehensive validation with automation")
    print("[BOTH] Complete workflow from basic to advanced")
    print("[INFO] All tests run with visible browser windows")
    print(f"[TIME] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)


def check_environment():
    """Check if environment is ready"""
    print("[CHECK] Checking environment...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("[ERROR] Python 3.8+ required")
        return False
    print(f"[SUCCESS] Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Check required packages
    required = ['pytest', 'selenium', 'webdriver_manager']
    for package in required:
        try:
            __import__(package)
            print(f"[SUCCESS] {package}")
        except ImportError:
            print(f"[ERROR] {package} - Run: pip install {package}")
            return False
    
    # Check test files
    test_files = [
        "tests/test_amazon_complete.py",
        "utils/browser_config.py"
    ]
    
    for file_path in test_files:
        if not os.path.exists(file_path):
            print(f"[ERROR] {file_path} not found")
            return False
    print("[SUCCESS] All test files ready")
    
    # Ensure directories
    for directory in ["screenshots", "reports", "logs"]:
        os.makedirs(directory, exist_ok=True)
    print("[SUCCESS] Directories ready")
    
    return True


def run_basic_tests():
    """Run basic functionality tests"""
    print("\n[BASIC] Running BASIC tests...")
    print("   Essential functionality testing")
    
    cmd = [
        "pytest",
        "tests/test_amazon_complete.py::TestAmazonBasic",
        "-m", "basic",
        "-v",
        "--tb=short",
        f"--html=reports/basic_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
        "--self-contained-html"
    ]
    
    return subprocess.run(cmd)


def run_advanced_tests():
    """Run advanced comprehensive tests"""
    print("\n[ADVANCED] Running ADVANCED tests...")
    print("   Comprehensive validation with automation")
    print("   [WARNING] Advanced tests take 10-15 minutes to complete")
    
    cmd = [
        "pytest",
        "tests/test_amazon_complete.py::TestAmazonAdvanced",
        "-m", "advanced",
        "-v",
        "--tb=short",
        f"--html=reports/advanced_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
        "--self-contained-html"
    ]
    
    return subprocess.run(cmd)


def run_both_tests():
    """Run combined basic and advanced tests"""
    print("\n[BOTH] Running BOTH tests...")
    print("   Complete workflow from basic to advanced")
    print("   [WARNING] This includes all test capabilities and takes 15-20 minutes")
    
    cmd = [
        "pytest",
        "tests/test_amazon_complete.py",
        "-v",
        "--tb=short",
        f"--html=reports/complete_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
        "--self-contained-html"
    ]
    
    return subprocess.run(cmd)


def run_specific_test_category(category, test_name):
    """Run specific test from a category"""
    print(f"\n[TARGET] Running specific {category.upper()} test: {test_name}")
    
    class_map = {
        "basic": "TestAmazonBasic",
        "advanced": "TestAmazonAdvanced", 
        "both": "TestAmazonBoth"
    }
    
    test_class = class_map.get(category.lower())
    if not test_class:
        print(f"[ERROR] Invalid category: {category}")
        return None
    
    cmd = [
        "pytest",
        f"tests/test_amazon_complete.py::{test_class}::{test_name}",
        "-v",
        "--tb=short",
        "-s"
    ]
    
    return subprocess.run(cmd)


def clean_artifacts():
    """Clean old reports and screenshots"""
    print("[CLEAN] Cleaning old artifacts...")
    
    cleaned = 0
    for directory in ["reports", "screenshots"]:
        if os.path.exists(directory):
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    cleaned += 1
    
    print(f"[SUCCESS] Cleaned {cleaned} files")


def show_test_categories():
    """Show available test categories and their descriptions"""
    print("\n[INFO] Test Categories:")
    print("-" * 60)
    
    print("[BASIC] BASIC Tests:")
    print("   • Homepage load and validation")
    print("   • Basic search functionality")
    print("   • Product page navigation")
    print("   Duration: ~3-5 minutes")
    print()
    
    print("[ADVANCED] ADVANCED Tests:")
    print("   • Comprehensive search with multi-category validation")
    print("   • Advanced price validation with accuracy reporting")
    print("   • Product interaction with mouse automation")
    print("   • Performance monitoring and metrics collection")
    print("   • Deep data extraction with fallback strategies")
    print("   • Intelligent popup dismissal")
    print("   Duration: ~10-15 minutes")
    print()
    
    print("[BOTH] BOTH Tests:")
    print("   • Complete workflow integration")
    print("   • Basic to advanced progression testing")
    print("   • Full comprehensive validation")
    print("   Duration: ~15-20 minutes")
    print("-" * 60)


def show_menu():
    """Display interactive menu"""
    print("\n[TARGET] Test Execution Options:")
    print("-" * 50)
    print("1. [BASIC] Run BASIC Tests (Essential functionality)")
    print("2. [ADVANCED] Run ADVANCED Tests (Comprehensive validation)")
    print("3. [BOTH] Run BOTH Tests (Complete suite)")
    print("4. [TARGET] Run Specific Test")
    print("5. [INFO] Show Test Categories Info")
    print("6. [CONFIG] Check Environment")
    print("7. [CLEAN] Clean Artifacts")
    print("0. [EXIT] Exit")
    print("-" * 50)


def show_specific_test_menu():
    """Show specific test selection menu"""
    print("\n[TARGET] Select Test Category:")
    print("-" * 40)
    print("1. [BASIC] BASIC Test")
    print("2. [ADVANCED] ADVANCED Test")
    print("3. [BOTH] BOTH Test")
    print("0. ← Back to main menu")
    print("-" * 40)


def show_basic_tests():
    """Show available basic tests"""
    print("\n[BASIC] Available BASIC Tests:")
    print("-" * 40)
    print("1. test_homepage_load")
    print("2. test_basic_search")
    print("3. test_product_page_navigation")
    print("-" * 40)


def show_advanced_tests():
    """Show available advanced tests"""
    print("\n[ADVANCED] Available ADVANCED Tests:")
    print("-" * 50)
    print("1. test_comprehensive_search_with_categories")
    print("2. test_advanced_price_validation_with_accuracy")
    print("3. test_advanced_product_interaction_with_mouse_automation")
    print("4. test_performance_and_comprehensive_validation")
    print("5. test_location_and_language_testing")
    print("6. test_authentication_flow_simulation")
    print("7. test_comprehensive_filter_testing")
    print("8. test_edge_case_search_handling")
    print("9. test_advanced_redirection_testing")
    print("10. test_comprehensive_otp_login_simulation")
    print("11. test_advanced_language_changing")
    print("12. test_comprehensive_location_changing")
    print("-" * 50)


def show_both_tests():
    """Show available combined tests"""
    print("\n[BOTH] Available BOTH Tests:")
    print("-" * 40)
    print("1. test_complete_workflow_basic_to_advanced")
    print("-" * 40)


def handle_specific_test_selection():
    """Handle specific test selection workflow"""
    while True:
        show_specific_test_menu()
        category_choice = input("\n[TARGET] Enter category choice (0-3): ").strip()
        
        if category_choice == "0":
            return  # Back to main menu
        elif category_choice == "1":
            show_basic_tests()
            test_choice = input("\nEnter test number (1-3): ").strip()
            basic_tests = [
                "test_homepage_load",
                "test_basic_search", 
                "test_product_page_navigation"
            ]
            if test_choice in ["1", "2", "3"]:
                test_name = basic_tests[int(test_choice) - 1]
                run_specific_test_category("basic", test_name)
                break
        elif category_choice == "2":
            show_advanced_tests()
            test_choice = input("\nEnter test number (1-12): ").strip()
            advanced_tests = [
                "test_comprehensive_search_with_categories",
                "test_advanced_price_validation_with_accuracy",
                "test_advanced_product_interaction_with_mouse_automation", 
                "test_performance_and_comprehensive_validation",
                "test_location_and_language_testing",
                "test_authentication_flow_simulation",
                "test_comprehensive_filter_testing",
                "test_edge_case_search_handling",
                "test_advanced_redirection_testing",
                "test_comprehensive_otp_login_simulation",
                "test_advanced_language_changing",
                "test_comprehensive_location_changing"
            ]
            if test_choice in [str(i) for i in range(1, 13)]:
                test_name = advanced_tests[int(test_choice) - 1]
                run_specific_test_category("advanced", test_name)
                break
        elif category_choice == "3":
            show_both_tests()
            test_choice = input("\nEnter test number (1): ").strip()
            if test_choice == "1":
                run_specific_test_category("both", "test_complete_workflow_basic_to_advanced")
                break
        else:
            print("[ERROR] Invalid choice. Please select 0-3.")


def main():
    """Main execution function"""
    show_banner()
    
    if not check_environment():
        print("\n[ERROR] Environment check failed. Please install requirements:")
        print("   pip install -r requirements.txt")
        return 1
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "--basic":
            return run_basic_tests().returncode
        elif arg == "--advanced":
            return run_advanced_tests().returncode
        elif arg == "--both" or arg == "--all":
            return run_both_tests().returncode
        else:
            print(f"[ERROR] Unknown argument: {sys.argv[1]}")
            print("   Valid options: --basic, --advanced, --both")
            return 1
    
    # Interactive mode
    while True:
        show_menu()
        choice = input("\n[TARGET] Enter your choice (0-7): ").strip()
        
        try:
            if choice == "1":
                run_basic_tests()
            elif choice == "2":
                run_advanced_tests()
            elif choice == "3":
                run_both_tests()
            elif choice == "4":
                handle_specific_test_selection()
            elif choice == "5":
                show_test_categories()
            elif choice == "6":
                check_environment()
            elif choice == "7":
                clean_artifacts()
            elif choice == "0":
                print("[EXIT] Goodbye!")
                break
            else:
                print("[ERROR] Invalid choice. Please select 0-7.")
            
            if choice in ["1", "2", "3", "4"] and choice != "4":
                input("\n[PAUSE]  Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n[EXIT] Goodbye!")
            break
        except Exception as e:
            print(f"[ERROR] Error: {e}")
            input("\n[PAUSE]  Press Enter to continue...")

    return 0


if __name__ == "__main__":
    sys.exit(main())