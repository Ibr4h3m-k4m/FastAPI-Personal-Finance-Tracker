# Personal Finance Tracker API - Development Guide

## Project Overview
A RESTful API for managing personal finances, tracking expenses, setting budgets, and analyzing spending patterns.

---

## Technology Stack

### Core
- **FastAPI**: Main framework
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migrations
- **Pydantic**: Data validation and settings management
- **PostgreSQL**: Database

### Security & Auth
- **python-jose**: JWT token handling
- **passlib**: Password hashing
- **python-multipart**: Form data handling

### Additional
- **uvicorn**: ASGI server
- **pytest**: Testing framework

---

## Project Structure

```
finance_tracker/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app instance
│   ├── config.py               # Settings and environment variables
│   ├── database.py             # Database connection setup
│   │
│   ├── models/                 # SQLAlchemy models (database tables)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── transaction.py
│   │   ├── category.py
│   │   └── budget.py
│   │
│   ├── schemas/                # Pydantic schemas (request/response models)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── transaction.py
│   │   ├── category.py
│   │   └── budget.py
│   │
│   ├── routers/                # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── transactions.py
│   │   ├── categories.py
│   │   └── budgets.py
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── transaction_service.py
│   │
│   └── utils/                  # Helper functions
│       ├── __init__.py
│       ├── security.py         # Password hashing, token generation
│       └── dependencies.py     # Dependency injection (get_db, get_current_user)
│
├── alembic/                    # Database migrations
├── tests/                      # Test files
├── .env                        # Environment variables
├── requirements.txt
└── README.md
```

---

## Version 1: MVP (Authentication & Basic Transactions)

### Learning Goals
- FastAPI basics (routes, request/response) [X]
- Database integration with SQLAlchemy [X]
- JWT authentication [X]
- CRUD operations (Create Read Update Delete) [X]
- Data validation with Pydantic [X]

### Database Models

**User Model:** [X]
- id (primary key)
- email (unique)
- username (unique)
- hashed_password
- created_at
- is_active

**Transaction Model:** [X]
- id (primary key)
- user_id (foreign key)
- amount (decimal)
- description
- transaction_type (enum: income/expense)
- date
- created_at
- Relationship back to User

### API Endpoints

**Authentication:** [X]
- `POST /auth/register` - Create new user account [X]
- `POST /auth/login` - Login and receive JWT token [X]
- `POST /auth/refresh` - Refresh access token [X]

**Users:** [X]
- `GET /users/me` - Get current user profile [X]
- `PUT /users/me` - Update user profile [X]
- `DELETE /users/me` - Delete user account [X]

**Transactions:**
- `POST /transactions` - Create new transaction
- `GET /transactions` - List all user transactions (with pagination)
- `GET /transactions/{id}` - Get specific transaction
- `PUT /transactions/{id}` - Update transaction
- `DELETE /transactions/{id}` - Delete transaction

### Implementation Steps

1. **Setup & Configuration** [X]
   - Install FastAPI and dependencies [X]
   - Create project structure [X]
   - Setup database connection in `database.py` [X]
   - Configure environment variables in `config.py` [X]

2. **User Model & Authentication** [X]
   - Create User SQLAlchemy model [X]
   - Create User Pydantic schemas (UserCreate, UserResponse, UserLogin) [X]
   - Implement password hashing utilities [X]
   - Implement JWT token generation and validation [X]
   - Create auth router with register/login endpoints [X]

3. **Database Dependency & Security** [X]
   - Create `get_db()` dependency for database sessions [X]
   - Create `get_current_user()` dependency for protected routes [X]
   - Test authentication flow [X]

4. **Transaction CRUD**
   - Create Transaction model and schemas
   - Implement transaction router with all CRUD endpoints
   - Add user_id filtering (users can only see their own transactions)
   - Implement pagination for listing transactions

5. **Testing & Documentation**
   - Write basic tests for auth [X]
   - Write basic tests for transactions
   - Check automatic API docs at `/docs` [X]

### Key Concepts to Learn
- Dependency injection in FastAPI [X]
- JWT authentication flow [X]
- SQLAlchemy relationships and queries
- Pydantic validators and serialization
- HTTP status codes and error handling [X]
- Database sessions and transactions

---

## Version 2: Categories & Budgets

### Learning Goals
- Complex database relationships (one-to-many)
- Query filtering and aggregation
- Date range queries
- Business logic in services layer

### New Database Models

**Category Model:**
- id (primary key)
- user_id (foreign key)
- name
- color (hex code)
- icon (optional)
- created_at

**Budget Model:**
- id (primary key)
- user_id (foreign key)
- category_id (foreign key, nullable)
- amount (decimal)
- period (enum: daily/weekly/monthly/yearly)
- start_date
- end_date (optional)
- created_at

### Updates to Existing Models
- Add `category_id` (foreign key, nullable) to Transaction model

### New API Endpoints

**Categories:**
- `POST /categories` - Create category
- `GET /categories` - List all user categories
- `PUT /categories/{id}` - Update category
- `DELETE /categories/{id}` - Delete category (what happens to associated transactions?)

**Budgets:**
- `POST /budgets` - Create budget
- `GET /budgets` - List all budgets
- `GET /budgets/{id}` - Get specific budget with spending analysis
- `PUT /budgets/{id}` - Update budget
- `DELETE /budgets/{id}` - Delete budget

**Analytics:**
- `GET /analytics/spending` - Spending by category (date range filter)
- `GET /analytics/income-vs-expense` - Compare income and expenses over time
- `GET /analytics/budget-status` - Check all budgets status (over/under budget)

### Implementation Steps

1. **Create Category System**
   - Create Category model and schemas
   - Create category router with CRUD endpoints
   - Update Transaction model to include category_id
   - Modify transaction endpoints to accept/return category info

2. **Implement Budgets**
   - Create Budget model and schemas
   - Create budget router
   - Implement budget calculation logic in services layer
   - Create endpoint that calculates if user is over/under budget

3. **Add Analytics Endpoints**
   - Create analytics router
   - Implement spending aggregation by category
   - Implement income vs expense comparison
   - Use SQLAlchemy's aggregation functions (func.sum, group_by)

4. **Database Migration**
   - Learn Alembic basics
   - Create migration for new tables
   - Create migration for adding category_id to transactions

### Key Concepts to Learn
- Database migrations with Alembic
- Complex SQLAlchemy queries (joins, aggregations)
- Service layer pattern for business logic
- Handling nullable foreign keys
- Date/time handling in Python and SQL
- Enum types in databases

---

## Version 3: Recurring Transactions & Goals

### Learning Goals
- Background tasks and scheduling
- More complex business logic
- State management

### New Database Models

**RecurringTransaction Model:**
- id (primary key)
- user_id (foreign key)
- amount (decimal)
- description
- category_id (foreign key, nullable)
- transaction_type (enum: income/expense)
- frequency (enum: daily/weekly/monthly/yearly)
- start_date
- end_date (optional)
- next_occurrence_date
- is_active
- created_at

**Goal Model:**
- id (primary key)
- user_id (foreign key)
- name
- target_amount (decimal)
- current_amount (decimal)
- deadline (date, optional)
- status (enum: active/completed/cancelled)
- created_at

**GoalContribution Model:**
- id (primary key)
- goal_id (foreign key)
- transaction_id (foreign key)
- amount (decimal)
- created_at

### New API Endpoints

**Recurring Transactions:**
- `POST /recurring` - Create recurring transaction template
- `GET /recurring` - List all recurring transactions
- `PUT /recurring/{id}` - Update recurring transaction
- `DELETE /recurring/{id}` - Deactivate recurring transaction
- `POST /recurring/{id}/process` - Manually trigger creation of transaction

**Goals:**
- `POST /goals` - Create financial goal
- `GET /goals` - List all goals
- `GET /goals/{id}` - Get goal details with progress
- `PUT /goals/{id}` - Update goal
- `POST /goals/{id}/contribute` - Link a transaction as contribution to goal
- `DELETE /goals/{id}` - Delete goal

### Implementation Steps

1. **Recurring Transactions**
   - Create RecurringTransaction model and schemas
   - Create recurring transactions router
   - Implement logic to calculate next occurrence date
   - Create background task to check and create due recurring transactions
   - Consider: Do you want to auto-create transactions or require manual approval?

2. **Financial Goals**
   - Create Goal and GoalContribution models
   - Create goals router
   - Implement progress calculation logic
   - Allow linking existing transactions to goals
   - Create endpoint to show goal progress over time

3. **Background Processing**
   - Learn about FastAPI BackgroundTasks
   - Or explore APScheduler for cron-like scheduling
   - Create a task that runs daily to process recurring transactions

### Key Concepts to Learn
- Background tasks in FastAPI
- Scheduling and cron jobs
- Complex state management
- Cascade deletes and orphaned records
- Transaction atomicity (ensuring data consistency)

---

## Version 4: Advanced Features

### Learning Goals
- File handling and generation
- External API integration (currency conversion)
- Notifications/webhooks
- Performance optimization

### New Features

**Data Export/Import:**
- `GET /export/csv` - Export transactions as CSV
- `GET /export/pdf` - Export monthly report as PDF
- `POST /import/csv` - Import transactions from CSV

**Multi-Currency Support:**
- Add `currency` field to User and Transaction models
- Integrate with exchange rate API (e.g., exchangerate-api.io)
- `GET /currencies` - List supported currencies
- `POST /transactions/convert` - Convert transaction to user's base currency

**Notifications:**
- Add notification preferences to User model
- Budget overspending alerts
- Upcoming recurring transaction reminders
- Goal milestone achievements

**Performance:**
- Add database indexes for frequently queried fields
- Implement caching with Redis (optional)
- Add query result pagination to all list endpoints

### Implementation Steps

1. **Export/Import System**
   - Learn CSV handling with Python's csv module
   - Learn PDF generation with ReportLab or WeasyPrint
   - Create export endpoints that generate files
   - Create import endpoint with validation

2. **Multi-Currency**
   - Integrate with exchange rate API
   - Add currency conversion logic
   - Update all financial calculations to handle different currencies
   - Store historical exchange rates

3. **Notifications**
   - Design notification system (email? in-app? webhooks?)
   - Create notification preferences in user settings
   - Implement notification triggers based on budget/goal events
   - Consider using Celery for async email sending

### Key Concepts to Learn
- File generation and streaming in FastAPI
- External API integration and error handling
- Async/await for concurrent operations
- Caching strategies
- Email sending with SMTP
- Database indexing and query optimization

---

## Testing Strategy

### What to Test

**Unit Tests:**
- Utility functions (password hashing, token generation)
- Service layer business logic
- Pydantic model validation

**Integration Tests:**
- API endpoints (status codes, response formats)
- Database operations (CRUD)
- Authentication flow

**Tools:**
- pytest for test framework
- TestClient from FastAPI for endpoint testing
- Factory Boy or pytest fixtures for test data


## Deployment Considerations (For Learning)

1. **Environment Variables**
   - Database URL [X]
   - Secret key for JWT [X]
   - API keys for external services

2. **Docker** 
   - Create Dockerfile for the app
   - Docker Compose for app + database

3. **Simple Deployment Options**
   - Railway.app (free tier)
   - Render.com (free tier)