#!/usr/bin/env python3
"""
Business Search App - Automated Test Runner
This script runs automated tests against the backend API
"""

import requests
import json
import time
import sys
from typing import Dict, Any, List

# Configuration
BASE_URL = "http://localhost:5000"
TIMEOUT = 10

class TestRunner:
    def __init__(self):
        self.base_url = BASE_URL
        self.results = []
        self.start_time = time.time()
    
    def log(self, message: str):
        """Print formatted log message"""
        print(f"[{time.strftime('%H:%M:%S')}] {message}")
    
    def test_endpoint(self, method: str, endpoint: str, expected_status: int = 200, 
                     data: Dict = None, name: str = None) -> bool:
        """Test a single API endpoint"""
        if name is None:
            name = f"{method} {endpoint}"
        
        self.log(f"Testing: {name}")
        
        try:
            if method.upper() == "GET":
                response = requests.get(f"{self.base_url}{endpoint}", timeout=TIMEOUT)
            elif method.upper() == "POST":
                response = requests.post(f"{self.base_url}{endpoint}", 
                                       json=data, timeout=TIMEOUT)
            else:
                self.log(f"❌ Unsupported method: {method}")
                return False
            
            if response.status_code == expected_status:
                self.log(f"✅ PASS: {name}")
                return True
            else:
                self.log(f"❌ FAIL: {name} - Expected {expected_status}, got {response.status_code}")
                if response.text:
                    self.log(f"   Response: {response.text[:200]}...")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log(f"❌ ERROR: {name} - {str(e)}")
            return False
    
    def test_search_functionality(self) -> List[bool]:
        """Test search functionality"""
        results = []
        
        # Test 1: Basic search
        results.append(self.test_endpoint(
            "POST", "/api/search",
            data={"query": "housing", "limit": 5},
            name="Basic search for 'housing'"
        ))
        
        # Test 2: Natural language search
        results.append(self.test_endpoint(
            "POST", "/api/search",
            data={"query": "affordable housing near 94103 for families", "limit": 5},
            name="Natural language search"
        ))
        
        # Test 3: Location-based search
        results.append(self.test_endpoint(
            "POST", "/api/search",
            data={"query": "veterans", "location": {"zip": "85004", "radius_miles": 10}, "limit": 5},
            name="Location-based search"
        ))
        
        # Test 4: Cause filtering
        results.append(self.test_endpoint(
            "POST", "/api/search",
            data={"query": "education", "filters": {"cause": ["education", "youth"]}, "limit": 5},
            name="Cause-based filtering"
        ))
        
        # Test 5: Rating filter
        results.append(self.test_endpoint(
            "POST", "/api/search",
            data={"query": "housing", "filters": {"min_rating": 4.5}, "limit": 5},
            name="Rating filter"
        ))
        
        return results
    
    def test_sorting(self) -> List[bool]:
        """Test different sorting options"""
        results = []
        
        sort_options = ["relevance", "distance", "rating", "popularity", "impact", "newest"]
        
        for sort_option in sort_options:
            results.append(self.test_endpoint(
                "POST", "/api/search",
                data={"query": "housing", "sort": sort_option, "limit": 3},
                name=f"Sort by {sort_option}"
            ))
        
        return results
    
    def test_edge_cases(self) -> List[bool]:
        """Test edge cases and error handling"""
        results = []
        
        # Test 1: Empty query
        results.append(self.test_endpoint(
            "POST", "/api/search",
            data={"query": "", "limit": 5},
            name="Empty query"
        ))
        
        # Test 2: Invalid ZIP code
        results.append(self.test_endpoint(
            "POST", "/api/search",
            data={"query": "housing", "location": {"zip": "99999", "radius_miles": 10}, "limit": 5},
            name="Invalid ZIP code"
        ))
        
        # Test 3: Large radius
        results.append(self.test_endpoint(
            "POST", "/api/search",
            data={"query": "housing", "location": {"zip": "94103", "radius_miles": 1000}, "limit": 5},
            name="Large radius search"
        ))
        
        # Test 4: Multiple cause filters
        results.append(self.test_endpoint(
            "POST", "/api/search",
            data={"query": "support", "filters": {"cause": ["housing", "families", "education", "veterans"]}, "limit": 5},
            name="Multiple cause filters"
        ))
        
        return results
    
    def run_all_tests(self):
        """Run all test suites"""
        self.log("🚀 Starting Business Search App Test Suite")
        self.log("=" * 50)
        
        # Test basic endpoints
        self.log("\n📋 Testing Basic Endpoints")
        self.log("-" * 30)
        basic_tests = [
            self.test_endpoint("GET", "/health", name="Health check"),
            self.test_endpoint("GET", "/api/businesses", name="Get all organizations"),
            self.test_endpoint("GET", "/api/businesses/org_001", name="Get specific organization"),
            self.test_endpoint("GET", "/api/businesses/invalid_id", expected_status=404, name="Organization not found")
        ]
        
        # Test search functionality
        self.log("\n🔍 Testing Search Functionality")
        self.log("-" * 30)
        search_tests = self.test_search_functionality()
        
        # Test sorting
        self.log("\n📊 Testing Sorting Options")
        self.log("-" * 30)
        sorting_tests = self.test_sorting()
        
        # Test edge cases
        self.log("\n⚠️ Testing Edge Cases")
        self.log("-" * 30)
        edge_tests = self.test_edge_cases()
        
        # Summary
        self.log("\n📈 Test Summary")
        self.log("=" * 50)
        
        all_tests = basic_tests + search_tests + sorting_tests + edge_tests
        passed = sum(all_tests)
        total = len(all_tests)
        
        self.log(f"Total Tests: {total}")
        self.log(f"Passed: {passed}")
        self.log(f"Failed: {total - passed}")
        self.log(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            self.log("🎉 All tests passed!")
            return True
        else:
            self.log("❌ Some tests failed. Check the logs above.")
            return False

def main():
    """Main function"""
    print("Business Search App - Automated Test Runner")
    print("Make sure the backend is running on http://localhost:5000")
    print()
    
    # Check if backend is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend is not responding correctly")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("❌ Backend is not running. Please start the backend first:")
        print("   cd backend && python server.py")
        sys.exit(1)
    
    # Run tests
    runner = TestRunner()
    success = runner.run_all_tests()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
