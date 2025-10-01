"""Comprehensive test runner for JLOH package."""
import pytest
import sys
import os
import argparse
from pathlib import Path


def run_basic_tests():
    """Run basic import and package tests."""
    print("🧪 Running basic tests (imports, package metadata)...")
    result = pytest.main([
        "-v", 
        "--tb=short",
        str(Path(__file__).parent / "tests" / "test_basic.py")
    ])
    return result == 0


def run_smoke_tests():
    """Run smoke tests (help functionality)."""
    print("💨 Running smoke tests (help functionality)...")
    result = pytest.main([
        "-v", 
        "--tb=short",
        str(Path(__file__).parent / "tests" / "test_smoke.py")
    ])
    return result == 0


def run_integration_tests():
    """Run integration tests with real data."""
    print("🔗 Running integration tests (real data processing)...")
    result = pytest.main([
        "-v", 
        "--tb=short", 
        "-x",  # Stop on first failure for integration tests
        str(Path(__file__).parent / "tests" / "test_modules.py")
    ])
    return result == 0


def run_all_tests():
    """Run all available tests."""
    print("🚀 Running all tests...")
    
    all_passed = True
    
    # Run each test suite
    print("\n" + "="*60)
    if not run_basic_tests():
        all_passed = False
        print("❌ Basic tests failed!")
    else:
        print("✅ Basic tests passed!")
    
    print("\n" + "="*60)
    if not run_smoke_tests():
        all_passed = False
        print("❌ Smoke tests failed!")
    else:
        print("✅ Smoke tests passed!")
    
    print("\n" + "="*60)
    if not run_integration_tests():
        all_passed = False
        print("❌ Integration tests failed!")
    else:
        print("✅ Integration tests passed!")
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 All tests passed successfully!")
    else:
        print("💥 Some tests failed. See output above.")
    
    return all_passed


def run_quick_tests():
    """Run quick tests (basic + smoke, skip integration)."""
    print("⚡ Running quick tests (basic + smoke)...")
    
    basic_passed = run_basic_tests()
    print()
    smoke_passed = run_smoke_tests()
    
    if basic_passed and smoke_passed:
        print("\n✅ Quick tests passed!")
        return True
    else:
        print("\n❌ Quick tests failed!")
        return False


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description='JLOH Test Runner')
    parser.add_argument(
        'test_type', 
        nargs='?', 
        default='quick',
        choices=['basic', 'smoke', 'integration', 'all', 'quick'],
        help='Type of tests to run (default: quick)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    print(f"JLOH Test Runner")
    print(f"Test directory: {Path(__file__).parent / 'tests'}")
    print(f"Running: {args.test_type} tests")
    print("="*60)
    
    # Run the specified test type
    if args.test_type == 'basic':
        success = run_basic_tests()
    elif args.test_type == 'smoke':
        success = run_smoke_tests()
    elif args.test_type == 'integration':
        success = run_integration_tests()
    elif args.test_type == 'all':
        success = run_all_tests()
    elif args.test_type == 'quick':
        success = run_quick_tests()
    else:
        print(f"Unknown test type: {args.test_type}")
        return 1
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())