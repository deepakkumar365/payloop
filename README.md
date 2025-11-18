# PayLoop - Vendor Collection System

A web-based vendor collection system for managing daily/weekly/monthly payment collections with role-based access control.

## Features

- **Role-Based Access**: Admin and Agent roles with different permissions
- **Customer Management**: Track customers with different collection cycles (daily/weekly/monthly)
- **Shop Management**: Manage shops linked to customers or as direct payers
- **Payment Collection**: Record and track payment history
- **JWT Authentication**: Secure token-based authentication
- **Mobile Responsive**: Works seamlessly on mobile devices

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy + Alembic
- PostgreSQL
- JWT Authentication
- Python 3.8+

### Frontend
- HTML5
- Tailwind CSS
- Vanilla JavaScript
- Mobile-first responsive design

## Project Structure

```
PayOrbit/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── customers.py
│   │   │   ├── shops.py
│   │   │   └── payments.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── deps.py
│   │   ├── db/
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── customer.py
│   │   │   ├── shop.py
│   │   │   └── payment.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── customer.py
│   │   │   ├── shop.py
│   │   │   └── payment.py
│   │   └── main.py
│   ├── alembic/
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py
└── frontend/
    ├── static/
    │   └── js/
    │       ├── config.js
    │       ├── auth.js
    │       ├── dashboard.js
    │       ├── customers.js
    │       ├── shops.js
    │       ├── payments.js
    │       └── users.js
    ├── index.html
    ├── dashboard.html
    ├── customers.html
    ├── shops.html
    ├── payments.html
    └── users.html
```

## Setup Instructions

### 1. Database Setup

Install PostgreSQL and create a database:

```bash
createdb payloop
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env file with your settings:
# DATABASE_URL=postgresql://username:password@localhost:5432/payloop
# SECRET_KEY=your-secret-key-here
# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30

# Run migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Create initial admin user (Python shell)
python
```

In Python shell:
```python
from app.db.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

db = SessionLocal()
admin = User(
    email="admin@payloop.com",
    username="admin",
    hashed_password=get_password_hash("admin123"),
    full_name="System Admin",
    role=UserRole.ADMIN,
    is_active=True
)
db.add(admin)
db.commit()
exit()
```

### 3. Run Backend

```bash
python run.py
```

Backend will run on: http://localhost:8000

API Documentation: http://localhost:8000/docs

### 4. Frontend Setup

Open `frontend/index.html` in a web browser or serve it using a simple HTTP server:

```bash
cd frontend

# Python 3
python -m http.server 8080

# Or use any other static file server
```

Frontend will be available at: http://localhost:8080

### 5. Login

Default credentials:
- **Username**: admin
- **Password**: admin123

## Usage

### Admin Features
- Create and manage agents
- View all customers, shops, and payments
- Full system access

### Agent Features
- Manage their own customers
- Add shops for customers
- Collect payments
- View payment history

### Collection Cycles
- **Daily**: Collect payments every day
- **Weekly**: Collect payments every week
- **Monthly**: Collect payments every month

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login and get JWT token

### Users
- `GET /api/users` - List users
- `POST /api/users` - Create user (Admin only)
- `GET /api/users/me` - Get current user
- `GET /api/users/{id}` - Get user by ID
- `PUT /api/users/{id}` - Update user (Admin only)
- `DELETE /api/users/{id}` - Delete user (Admin only)

### Customers
- `GET /api/customers` - List customers
- `POST /api/customers` - Create customer
- `GET /api/customers/{id}` - Get customer
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer

### Shops
- `GET /api/shops` - List shops
- `POST /api/shops` - Create shop
- `GET /api/shops/{id}` - Get shop
- `PUT /api/shops/{id}` - Update shop
- `DELETE /api/shops/{id}` - Delete shop

### Payments
- `GET /api/payments` - List payments
- `POST /api/payments` - Create payment
- `GET /api/payments/{id}` - Get payment
- `DELETE /api/payments/{id}` - Delete payment (Admin only)

## Security

- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control
- CORS enabled for frontend integration

## Mobile Responsive

All pages are fully responsive and work on:
- Desktop browsers
- Tablets
- Mobile phones

## License

MIT License
