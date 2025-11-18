---
description: Repository Information Overview
alwaysApply: true
---

# Repository Information Overview

## Repository Summary

PayOrbit (PayLoop) is a web-based vendor collection system for managing daily, weekly, and monthly payment collections with role-based access control. The application features customer management, shop management, payment tracking, and JWT-based authentication with a responsive mobile-first interface.

## Repository Structure

This is a multi-project monorepo containing a Python FastAPI backend and static HTML/CSS/JavaScript frontend:

### Main Repository Components

- **Backend**: FastAPI-based REST API with SQLAlchemy ORM, Alembic migrations, and PostgreSQL database
- **Frontend**: Static HTML5 web interface with Tailwind CSS and vanilla JavaScript for customer, shop, payment, and user management
- **Database Migrations**: Alembic-managed PostgreSQL schema versioning

---

## Projects

### Backend (FastAPI REST API)

**Configuration File**: `backend/requirements.txt`, `backend/.env.example`, `backend/alembic.ini`

#### Language & Runtime

**Language**: Python  
**Version**: 3.8+ (tested with Python 3.11.9)  
**Build System**: None (Python application)  
**Package Manager**: pip

#### Dependencies

**Main Dependencies**:
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- sqlalchemy==2.0.23
- alembic==1.12.1
- psycopg2-binary==2.9.9
- pydantic==2.5.0
- pydantic-settings==2.1.0
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- python-multipart==0.0.6
- python-dotenv==1.0.0

#### Build & Installation

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run database migrations
alembic upgrade head

# Create admin user (optional)
python create_admin.py

# Start development server
python run.py
```

Server runs on `http://0.0.0.0:8000` with hot reload enabled.

#### Main Files & Resources

- **Entry Points**: `backend/run.py` (main server), `backend/create_admin.py` (admin setup)
- **Application Core**: `backend/app/main.py` - FastAPI app with routers for auth, users, customers, shops, payments
- **API Routes**: 
  - `backend/app/api/auth.py` - JWT authentication
  - `backend/app/api/users.py` - User management
  - `backend/app/api/customers.py` - Customer operations
  - `backend/app/api/shops.py` - Shop management
  - `backend/app/api/payments.py` - Payment recording
- **Database Configuration**: `backend/app/db/database.py` - SQLAlchemy session management
- **Database Models**: `backend/app/models/` - User, Customer, Shop, Payment ORM models
- **Request/Response Schemas**: `backend/app/schemas/` - Pydantic validation schemas
- **Security**: `backend/app/core/security.py` - Password hashing, JWT operations
- **Database Migrations**: `backend/alembic/versions/` - Versioned schema changes

#### Configuration

**Environment Variables** (`.env`):
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing secret
- `ALGORITHM`: JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration (30 minutes)

---

### Frontend (Static Web Application)

**Type**: HTML5, CSS, Vanilla JavaScript

#### Specification & Tools

**Type**: Static web application  
**Technologies**: HTML5, Tailwind CSS, Vanilla JavaScript  
**Required Tools**: Web server (optional), modern web browser  

#### Key Resources

**Main Files**:
- `frontend/index.html` - Login/authentication page
- `frontend/dashboard.html` - Admin dashboard
- `frontend/customers.html` - Customer management interface
- `frontend/shops.html` - Shop management interface
- `frontend/payments.html` - Payment recording interface
- `frontend/users.html` - User management interface

**Static Assets**:
- `frontend/static/js/config.js` - API configuration and endpoint management
- `frontend/static/js/auth.js` - Authentication and token management
- `frontend/static/js/dashboard.js` - Dashboard logic
- `frontend/static/js/customers.js` - Customer CRUD operations
- `frontend/static/js/shops.js` - Shop operations
- `frontend/static/js/payments.js` - Payment recording
- `frontend/static/js/users.js` - User management
- `frontend/static/css/` - Tailwind CSS styling

#### Usage & Operations

**Serving the Frontend**:
```bash
# Option 1: Using Python HTTP server
cd frontend
python -m http.server 8080

# Option 2: Using Node.js http-server
http-server frontend -p 8080

# Option 3: Using any static web server (nginx, Apache, etc.)
```

**API Integration**: Frontend connects to backend API at configured endpoint (typically `http://localhost:8000` via `config.js`)

**Authentication Flow**: 
1. User logs in via `index.html` (calls `/api/auth` endpoint)
2. JWT token stored in localStorage
3. Subsequent requests include Authorization header
4. Role-based access control enforced client-side and server-side

---

## Development Setup Summary

**Prerequisites**:
- Python 3.8+
- PostgreSQL database
- Web browser for frontend

**Quick Start**:
```bash
# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python run.py

# Frontend setup (in another terminal)
cd frontend
python -m http.server 8080
```

Access frontend at `http://localhost:8080` and backend API at `http://localhost:8000`

## Database

- **System**: PostgreSQL
- **Migrations**: Alembic-managed with version control
- **ORM**: SQLAlchemy 2.0
- **Initial Setup**: Create database `payloop` before running migrations
