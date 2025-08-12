"""
Budget Tracker API - Testing Script
This script demonstrates all the API endpoints and functionality.
Run this script to test the complete API workflow.
"""

import requests
import json
from datetime import datetime, timedelta
from decimal import Decimal

# Base URL for the API
BASE_URL = 'http://127.0.0.1:8000/api'

class BudgetTrackerAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.user_id = None
        self.categories = {}
        
    def print_response(self, title, response):
        """Helper method to print API responses nicely."""
        print(f"\n{'='*60}")
        print(f"🔍 {title}")
        print(f"{'='*60}")
        print(f"Status Code: {response.status_code}")
        
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2, default=str)}")
        except:
            print(f"Response: {response.text}")
        
        print(f"{'='*60}\n")
    
    def test_api_root(self):
        """Test the API root endpoint."""
        response = self.session.get(f"{BASE_URL}/")
        self.print_response("API Root", response)
        return response.status_code == 200
    
    def test_user_registration(self):
        """Test user registration."""
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = self.session.post(f"{BASE_URL}/users/register/", json=user_data)
        self.print_response("User Registration", response)
        
        if response.status_code == 201:
            data = response.json()
            self.auth_token = data.get('token')
            self.user_id = data.get('user', {}).get('id')
            # Set authorization header for future requests
            self.session.headers.update({'Authorization': f'Token {self.auth_token}'})
            return True
        return False
    
    def test_user_login(self):
        """Test user login (alternative to registration)."""
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        response = self.session.post(f"{BASE_URL}/auth/login/", json=login_data)
        self.print_response("User Login", response)
        
        if response.status_code == 200:
            data = response.json()
            self.auth_token = data.get('token')
            self.session.headers.update({'Authorization': f'Token {self.auth_token}'})
            return True
        return False
    
    def test_user_profile(self):
        """Test getting user profile."""
        response = self.session.get(f"{BASE_URL}/users/me/")
        self.print_response("User Profile", response)
        return response.status_code == 200
    
    def test_categories_list(self):
        """Test listing all categories."""
        response = self.session.get(f"{BASE_URL}/categories/")
        self.print_response("Categories List", response)
        
        if response.status_code == 200:
            categories = response.json()
            # Store categories for later use
            for category in categories:
                self.categories[category['name']] = category['id']
            return True
        return False
    
    def test_create_category(self):
        """Test creating a new category."""
        category_data = {
            "name": "Test Category",
            "description": "A category created for testing purposes"
        }
        
        response = self.session.post(f"{BASE_URL}/categories/", json=category_data)
        self.print_response("Create Category", response)
        
        if response.status_code == 201:
            data = response.json()
            self.categories['Test Category'] = data['id']
            return True
        return False
    
    def test_create_transactions(self):
        """Test creating various transactions."""
        # Get some category IDs
        salary_cat = self.categories.get('Salary', 1)
        food_cat = self.categories.get('Food & Dining', 2)
        rent_cat = self.categories.get('Rent', 3)
        
        transactions = [
            {
                "amount": "5000.00",
                "type": "income",
                "category": salary_cat,
                "date": datetime.now().isoformat(),
                "description": "Monthly salary"
            },
            {
                "amount": "1200.00",
                "type": "expense",
                "category": rent_cat,
                "date": datetime.now().isoformat(),
                "description": "Monthly rent payment"
            },
            {
                "amount": "85.50",
                "type": "expense",
                "category": food_cat,
                "date": (datetime.now() - timedelta(days=1)).isoformat(),
                "description": "Grocery shopping"
            },
            {
                "amount": "25.00",
                "type": "expense",
                "category": food_cat,
                "date": (datetime.now() - timedelta(days=2)).isoformat(),
                "description": "Lunch at restaurant"
            },
            {
                "amount": "500.00",
                "type": "income",
                "category": self.categories.get('Freelance', 1),
                "date": (datetime.now() - timedelta(days=3)).isoformat(),
                "description": "Freelance project payment"
            }
        ]
        
        created_transactions = []
        for i, transaction_data in enumerate(transactions):
            response = self.session.post(f"{BASE_URL}/transactions/", json=transaction_data)
            self.print_response(f"Create Transaction {i+1}", response)
            if response.status_code == 201:
                created_transactions.append(response.json())
        
        return len(created_transactions) == len(transactions)
    
    def test_list_transactions(self):
        """Test listing user's transactions."""
        response = self.session.get(f"{BASE_URL}/transactions/")
        self.print_response("List Transactions", response)
        return response.status_code == 200
    
    def test_filter_transactions(self):
        """Test filtering transactions."""
        # Test filtering by type
        response = self.session.get(f"{BASE_URL}/transactions/?type=income")
        self.print_response("Filter Transactions - Income Only", response)
        
        # Test filtering by category
        food_cat_id = self.categories.get('Food & Dining')
        if food_cat_id:
            response = self.session.get(f"{BASE_URL}/transactions/?category={food_cat_id}")
            self.print_response("Filter Transactions - Food Category", response)
        
        # Test date range filtering
        start_date = (datetime.now() - timedelta(days=7)).date().isoformat()
        end_date = datetime.now().date().isoformat()
        response = self.session.get(f"{BASE_URL}/transactions/?start_date={start_date}&end_date={end_date}")
        self.print_response("Filter Transactions - Last 7 Days", response)
        
        return True
    
    def test_advanced_filtering(self):
        """Test advanced filtering endpoint."""
        # Test search functionality
        response = self.session.get(f"{BASE_URL}/transactions/filter/?search=salary")
        self.print_response("Advanced Filter - Search 'salary'", response)
        
        # Test multiple filters
        response = self.session.get(f"{BASE_URL}/transactions/filter/?type=expense&search=food")
        self.print_response("Advanced Filter - Expense + Food Search", response)
        
        return True
    
    def test_financial_summary(self):
        """Test financial summary endpoint."""
        response = self.session.get(f"{BASE_URL}/summary/")
        self.print_response("Financial Summary", response)
        return response.status_code == 200
    
    def test_category_summary(self):
        """Test category-wise summary."""
        response = self.session.get(f"{BASE_URL}/summary/categories/")
        self.print_response("Category Summary", response)
        
        # Test filtering by transaction type
        response = self.session.get(f"{BASE_URL}/summary/categories/?type=expense")
        self.print_response("Category Summary - Expenses Only", response)
        
        return True
    
    def test_transaction_crud(self):
        """Test full CRUD operations on transactions."""
        # Create a transaction
        transaction_data = {
            "amount": "50.00",
            "type": "expense",
            "category": self.categories.get('Entertainment', 1),
            "date": datetime.now().isoformat(),
            "description": "Movie tickets"
        }
        
        # CREATE
        response = self.session.post(f"{BASE_URL}/transactions/", json=transaction_data)
        self.print_response("CRUD - Create Transaction", response)
        
        if response.status_code != 201:
            return False
        
        transaction_id = response.json()['id']
        
        # READ
        response = self.session.get(f"{BASE_URL}/transactions/{transaction_id}/")
        self.print_response("CRUD - Read Transaction", response)
        
        # UPDATE
        update_data = {
            "amount": "55.00",
            "type": "expense",
            "category": self.categories.get('Entertainment', 1),
            "date": datetime.now().isoformat(),
            "description": "Movie tickets + popcorn"
        }
        
        response = self.session.put(f"{BASE_URL}/transactions/{transaction_id}/", json=update_data)
        self.print_response("CRUD - Update Transaction", response)
        
        # DELETE
        response = self.session.delete(f"{BASE_URL}/transactions/{transaction_id}/")
        self.print_response("CRUD - Delete Transaction", response)
        
        return True
    
    def test_logout(self):
        """Test user logout."""
        response = self.session.post(f"{BASE_URL}/auth/logout/")
        self.print_response("User Logout", response)
        return response.status_code == 200
    
    def run_all_tests(self):
        """Run all tests in sequence."""
        print("🚀 Starting Budget Tracker API Testing...")
        print("=" * 80)
        
        tests = [
            ("API Root", self.test_api_root),
            ("User Registration", self.test_user_registration),
            ("User Profile", self.test_user_profile),
            ("List Categories", self.test_categories_list),
            ("Create Category", self.test_create_category),
            ("Create Transactions", self.test_create_transactions),
            ("List Transactions", self.test_list_transactions),
            ("Filter Transactions", self.test_filter_transactions),
            ("Advanced Filtering", self.test_advanced_filtering),
            ("Financial Summary", self.test_financial_summary),
            ("Category Summary", self.test_category_summary),
            ("Transaction CRUD", self.test_transaction_crud),
            ("User Logout", self.test_logout),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🧪 Running: {test_name}")
            try:
                result = test_func()
                if result:
                    print(f"✅ {test_name} - PASSED")
                    passed += 1
                else:
                    print(f"❌ {test_name} - FAILED")
            except Exception as e:
                print(f"💥 {test_name} - ERROR: {str(e)}")
        
        print(f"\n\n📊 TEST RESULTS")
        print("=" * 50)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All tests passed! Your API is working perfectly!")
        else:
            print(f"\n⚠️  Some tests failed. Please check the output above.")


def main():
    """Main function to run the API tests."""
    print("Budget Tracker API - Testing Suite")
    print("Make sure the Django development server is running on http://127.0.0.1:8000")
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("❌ API server is not responding correctly. Please start the Django server.")
            return
    except requests.ConnectionError:
        print("❌ Cannot connect to API server. Please start the Django server with: python manage.py runserver")
        return
    
    tester = BudgetTrackerAPITester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
