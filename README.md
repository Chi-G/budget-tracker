# Budget Tracker API - Complete Documentation

## Project Overview

The Budget Tracker API is a RESTful backend application built with Django and Django REST Framework. It allows users to manage their personal finances by tracking income and expenses with categorization and comprehensive reporting features.

## 🏗️ Project Structure

```
Simple-Budget-Tracker-API/
├── budget_tracker/           # Main Django project
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── users/                    # User management app
│   ├── models.py            # User model
│   ├── views.py             # Authentication views
│   ├── serializers.py       # User serializers
│   ├── urls.py              # User URL patterns
│   └── admin.py             # Admin configuration
├── categories/               # Category management app
│   ├── models.py            # Category model
│   ├── views.py             # Category CRUD views
│   ├── serializers.py       # Category serializers
│   ├── urls.py              # Category URL patterns
│   ├── admin.py             # Admin configuration
│   └── management/          # Custom management commands
│       └── commands/
│           └── create_default_categories.py
├── transactions/             # Transaction management app
│   ├── models.py            # Transaction model
│   ├── views.py             # Transaction CRUD and filtering views
│   ├── serializers.py       # Transaction serializers
│   ├── urls.py              # Transaction URL patterns
│   └── admin.py             # Admin configuration
├── summary/                  # Financial summary app
│   ├── views.py             # Summary and reporting views
│   ├── serializers.py       # Summary serializers
│   └── urls.py              # Summary URL patterns
├── requirements.txt          # Python dependencies
├── manage.py                # Django management script
├── test_api.py              # Comprehensive API testing script
└── db.sqlite3               # SQLite database (generated)
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Simple-Budget-Tracker-API
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment
```bash
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Apply Database Migrations
```bash
python manage.py migrate
```

### Step 6: Create Default Categories (Optional)
```bash
python manage.py create_default_categories
```

### Step 7: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

## 🗄️ Database Schema

### User Model
- **Fields**: id, username, email, first_name, last_name, password, date_joined, created_at, updated_at
- **Features**: Extends Django's AbstractUser with additional timestamps

### Category Model
- **Fields**: id, name, description, created_at, updated_at
- **Constraints**: name must be unique
- **Relationships**: One-to-many with Transaction

### Transaction Model
- **Fields**: id, user, amount, type, category, date, description, created_at, updated_at
- **Types**: 'income' or 'expense'
- **Constraints**: amount must be positive
- **Relationships**: 
  - Many-to-one with User
  - Many-to-one with Category

## 🔐 Authentication

The API uses Token-based authentication:

1. **Register**: Create an account and receive a token
2. **Login**: Authenticate with username/password to get a token
3. **Authorization**: Include token in headers: `Authorization: Token <your-token>`
4. **Logout**: Delete the token

## 📚 API Endpoints

### Base URL: `http://127.0.0.1:8000/api/`

### Authentication Endpoints

#### 1. User Registration
- **POST** `/users/register/`
- **Body**:
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```
- **Response**: User data + authentication token

#### 2. User Login
- **POST** `/auth/login/`
- **Body**:
  ```json
  {
    "username": "john_doe",
    "password": "securepass123"
  }
  ```
- **Response**: User data + authentication token

#### 3. User Profile
- **GET** `/users/me/` (requires authentication)
- **PUT/PATCH** `/users/me/` (update profile)

#### 4. User Logout
- **POST** `/auth/logout/` (requires authentication)

### Category Endpoints

#### 1. List/Create Categories
- **GET** `/categories/` - List all categories
- **POST** `/categories/` - Create new category
  ```json
  {
    "name": "Food & Dining",
    "description": "Groceries, restaurants, etc."
  }
  ```

#### 2. Category Details
- **GET** `/categories/{id}/` - Get category details
- **PUT/PATCH** `/categories/{id}/` - Update category
- **DELETE** `/categories/{id}/` - Delete category

### Transaction Endpoints

#### 1. List/Create Transactions
- **GET** `/transactions/` - List user's transactions
- **POST** `/transactions/` - Create new transaction
  ```json
  {
    "amount": "150.00",
    "type": "expense",
    "category": 1,
    "date": "2025-08-01T10:00:00Z",
    "description": "Grocery shopping"
  }
  ```

#### 2. Transaction Details
- **GET** `/transactions/{id}/` - Get transaction details
- **PUT/PATCH** `/transactions/{id}/` - Update transaction
- **DELETE** `/transactions/{id}/` - Delete transaction

#### 3. Advanced Filtering
- **GET** `/transactions/filter/` - Advanced filtering with parameters:
  - `type`: income/expense
  - `category`: category ID
  - `start_date`: YYYY-MM-DD
  - `end_date`: YYYY-MM-DD
  - `search`: search in description/category name

### Summary Endpoints

#### 1. Financial Summary
- **GET** `/summary/` - Complete financial overview
- **Optional Parameters**:
  - `start_date`: Filter by date range
  - `end_date`: Filter by date range

#### 2. Category Summary
- **GET** `/summary/categories/` - Category-wise breakdown
- **Optional Parameters**:
  - `type`: income/expense
  - `start_date`: Filter by date range
  - `end_date`: Filter by date range

## 📊 Example API Responses

### Financial Summary Response
```json
{
  "total_income": "5500.00",
  "total_expenses": "1310.50",
  "net_balance": "4189.50",
  "transaction_count": 5,
  "income_count": 2,
  "expense_count": 3,
  "category_breakdown": {
    "income": [
      {
        "category__name": "Salary",
        "total_amount": 5000.0,
        "transaction_count": 1
      }
    ],
    "expenses": [
      {
        "category__name": "Rent",
        "total_amount": 1200.0,
        "transaction_count": 1
      }
    ]
  }
}
```

### Transaction List Response
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "amount": "5000.00",
      "type": "income",
      "category": 9,
      "category_detail": {
        "id": 9,
        "name": "Salary",
        "description": "Primary income from employment",
        "transaction_count": 1
      },
      "date": "2025-08-01T07:15:14.688160+01:00",
      "description": "Monthly salary",
      "user_username": "testuser",
      "created_at": "2025-08-01T07:15:14.700928+01:00",
      "updated_at": "2025-08-01T07:15:14.700928+01:00"
    }
  ]
}
```

## 🧪 Testing

### Run the Comprehensive Test Suite
```bash
python test_api.py
```

This script tests all API endpoints and functionality including:
- User registration and authentication
- Category management
- Transaction CRUD operations
- Filtering and search
- Financial summaries
- Error handling

### Run Django Unit Tests
```bash
python manage.py test
```

## 🔧 Configuration

### Key Settings (settings.py)

- **Database**: SQLite (development) - easily changeable to PostgreSQL for production
- **Authentication**: Token-based authentication
- **Pagination**: 20 items per page
- **Time Zone**: UTC
- **Debug Mode**: True (development)

### Environment Variables (Optional)
Create a `.env` file for sensitive settings:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

## 📋 Default Categories

The system comes with 15 pre-configured categories:

**Income Categories:**
- Salary
- Freelance
- Investment
- Gift

**Expense Categories:**
- Food & Dining
- Transportation
- Utilities
- Entertainment
- Healthcare
- Shopping
- Education
- Rent
- Insurance
- Savings
- Other

## 🛡️ Security Features

1. **Token Authentication**: Secure API access
2. **User Isolation**: Users can only access their own data
3. **Input Validation**: Comprehensive data validation
4. **SQL Injection Protection**: Django ORM provides protection
5. **CSRF Protection**: Built-in Django protection
6. **Password Validation**: Django's built-in password validators

## 🚀 Deployment Considerations

### For Production:
1. Set `DEBUG = False`
2. Configure proper database (PostgreSQL recommended)
3. Set up environment variables for sensitive settings
4. Configure static file serving
5. Set up proper domain and HTTPS
6. Consider using Redis for caching
7. Set up logging and monitoring

### Dependencies for Production:
```txt
django==4.2.7
djangorestframework==3.14.0
python-decouple==3.8
psycopg2-binary==2.9.6  # For PostgreSQL
gunicorn==20.1.0        # For production server
django-filter==23.3
```

## 🎯 Future Enhancements

1. **Recurring Transactions**: Support for recurring income/expenses
2. **Budget Planning**: Set budget limits per category
3. **Data Export**: Export data to CSV/PDF
4. **Mobile App**: React Native or Flutter app
5. **Multi-currency Support**: Handle different currencies
6. **Data Visualization**: Charts and graphs
7. **Expense Receipt Upload**: Image upload for receipts
8. **Notifications**: Email/SMS notifications for budget limits

## 🐛 Troubleshooting

### Common Issues:

1. **Django-admin not found**: Use `python -m django` instead
2. **Package installation errors**: Ensure virtual environment is activated
3. **Migration errors**: Delete migrations and recreate if needed
4. **Permission errors**: Ensure proper authentication headers
5. **Date format errors**: Use ISO format (YYYY-MM-DDTHH:MM:SSZ)

### Getting Help:

1. Check Django documentation: https://docs.djangoproject.com/
2. Django REST Framework docs: https://www.django-rest-framework.org/
3. Check the test script for usage examples
4. Review error messages in the terminal

## 📄 API Documentation Tools

For interactive API documentation, you can add:

1. **Django REST Framework Browsable API**: Built-in (available at each endpoint)
2. **Swagger/OpenAPI**: Add `drf-spectacular` for automatic API documentation
3. **Postman Collection**: Import endpoints for easy testing

## 🎉 Conclusion

Your Budget Tracker API is now fully functional with:

✅ Complete CRUD operations for transactions and categories  
✅ User authentication and authorization  
✅ Advanced filtering and search capabilities  
✅ Comprehensive financial summaries  
✅ Well-structured codebase following Django best practices  
✅ Comprehensive test suite  
✅ Admin interface for easy data management  
✅ Production-ready architecture  

The API successfully demonstrates your Django and Python skills and provides a solid foundation for a personal finance management system!
