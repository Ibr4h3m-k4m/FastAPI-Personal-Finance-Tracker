# Personal Finance Tracker API - V1 (MVP)

A RESTful API built with FastAPI for managing personal finances. This is the MVP (Minimum Viable Product) version featuring user authentication and profile management.

## 🚀 Features

### V1 - Authentication & User Management
- ✅ User registration with email and username
- ✅ JWT-based authentication
- ✅ Secure password hashing (Argon2)
- ✅ User profile management (view, update, delete)
- ✅ Protected endpoints with token-based authorization

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (python-jose)
- **Password Hashing:** Passlib with Argon2
- **Validation:** Pydantic
- **Server:** Uvicorn

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip (Python package manager)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ibr4h3m-k4m/FastAPI-Personal-Finance-Tracker.git
cd FastAPI-Personal-Finance-Tracker
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE finance_tracker;
CREATE USER finance_app_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE finance_tracker TO finance_app_user;
\q
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Application Settings
APP_NAME=Personal-Finance-Tracker-API
DEBUG=True
API_V1_STR=/api/v1

# Security
SECRET_KEY=your-super-secret-key-here-generate-with-openssl
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql://finance_app_user:your_password@localhost:5432/finance_tracker
DB_ECHO=False
```

**Generate a secure SECRET_KEY:**
```bash
openssl rand -hex 32
```

### 6. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### API Endpoints

#### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login and get JWT token | No |

#### User Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/users/me` | Get current user profile | Yes |
| PUT | `/api/v1/users/me` | Update user profile | Yes |
| DELETE | `/api/v1/users/me` | Delete user account | Yes |

### Example Usage

#### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

#### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword123"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 3. Get User Profile (Protected)

```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 4. Update User Profile

```bash
curl -X PUT "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com",
    "username": "newusername"
  }'
```

#### 5. Delete Account

```bash
curl -X DELETE "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🗂️ Project Structure

```
FastAPI-Personal-Finance-Tracker/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration and settings
│   ├── database.py                # Database connection setup
│   │
│   ├── models/                    # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── schemas/                   # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── token.py
│   │
│   ├── routers/                   # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── users.py
│   │
│   ├── core/                      # Core functionality
│   │   ├── __init__.py
│   │   └── security.py            # Password hashing, JWT tokens
│   │
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       └── dependencies.py        # FastAPI dependencies
│
├── .env                           # Environment variables (not in git)
├── .env.example                   # Environment variables template
├── .gitignore
├── requirements.txt               # Python dependencies
└── README.md
```

## 🔐 Security Features

- **Password Hashing:** Argon2 algorithm (industry standard)
- **JWT Tokens:** Secure token-based authentication with expiration
- **Protected Routes:** All user management endpoints require authentication
- **Input Validation:** Pydantic schemas validate all input data
- **SQL Injection Protection:** SQLAlchemy ORM prevents SQL injection
- **CORS:** Configurable Cross-Origin Resource Sharing

## 🧪 Testing

### Using Swagger UI (Recommended for Beginners)

1. Navigate to http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. For protected endpoints:
   - First, use `/auth/login` to get a token
   - Click the "Authorize" button (top right, green lock icon)
   - Enter your credentials or paste your token
   - Click "Authorize"
   - Now you can test protected endpoints

### Using curl (Command Line)

See the [Example Usage](#example-usage) section above.

### Using Postman/Thunder Client

1. Create a POST request to `/api/v1/auth/login`
2. Set body type to `x-www-form-urlencoded`
3. Add `username` and `password` fields
4. Send request and copy the `access_token`
5. For protected endpoints, add header:
   - Key: `Authorization`
   - Value: `Bearer YOUR_TOKEN`

## 🐛 Common Issues & Troubleshooting

### Database Connection Error

**Error:** `connection to server failed: FATAL: password authentication failed`

**Solution:** 
- Check your DATABASE_URL in `.env`
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Ensure database and user exist

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:** Run uvicorn from the project root directory:
```bash
uvicorn app.main:app --reload
```

### Token Expired

**Error:** `401 Unauthorized - Could not validate credentials`

**Solution:** Your JWT token has expired (default: 30 minutes). Login again to get a new token.

### Peer Authentication Failed (PostgreSQL)

**Error:** `FATAL: Peer authentication failed`

**Solution:** Add `-h localhost` to force password authentication:
```bash
psql -U finance_app_user -d finance_tracker -h localhost
```

## 🗺️ Roadmap

### V2 - Categories & Budgets (Coming Soon)
- Transaction categories
- Budget management
- Spending analytics by category
- Budget vs actual spending comparison

### V3 - Advanced Features (Planned)
- Recurring transactions
- Financial goals tracking
- Income vs expense reports

### V4 - Premium Features (Future)
- Multi-currency support
- Data export (CSV, PDF)
- Email notifications
- Advanced analytics and charts

## 📖 Additional Documentation

For detailed development guide and architecture:
- [Project Development Guide](./finance_tracker_guide.md)

## 🤝 Contributing

This is a learning project, but suggestions and feedback are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📝 License

This project is for educational purposes.

## 👤 Author

**Ibrahim Kamra**
- GitHub: [@Ibr4h3m-k4m](https://github.com/Ibr4h3m-k4m)

## 🙏 Acknowledgments

- Built as a portfolio project to demonstrate backend development skills
- Following industry best practices and modern Python web development standards
- Inspired by real-world financial tracking applications

---

**Current Version:** V1 (MVP) - Authentication & User Management  
**Status:** ✅ Complete  
**Last Updated:** December 2024
