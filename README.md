# Personal Memo System

A full-stack application for managing personal memos, tracking metrics, and organizing information with categories and tags.

## Project Structure

```
personal-memo-system/
├── backend/                    # Backend API server
│   ├── __init__.py
│   ├── main.py                # Main FastAPI application entry point
│   ├── database.py            # Database configuration and connection setup
│   ├── auth.py                # Authentication and authorization logic
│   ├── models.py              # SQLAlchemy database models
│   ├── schemas.py             # Pydantic data validation schemas
│   └── routers/               # API route handlers
│       ├── __init__.py
│       ├── categories.py      # Category management endpoints
│       ├── entries.py         # Entry management endpoints
│       ├── metrics.py         # Metric tracking endpoints
│       ├── tags.py            # Tag management endpoints
│       └── analytics.py       # Analytics and statistics endpoints
│
├── frontend/                  # Frontend React application
│   ├── public/               # Static files
│   ├── src/                  # Source code
│   │   ├── components/       # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service functions
│   │   ├── utils/           # Utility functions
│   │   ├── App.tsx          # Main application component
│   │   └── index.tsx        # Application entry point
│   ├── package.json         # Node.js dependencies
│   └── tsconfig.json        # TypeScript configuration
│
├── venv/                     # Python virtual environment
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## Backend Structure

### Core Components

1. **main.py**
   - FastAPI application initialization
   - CORS configuration
   - Router registration
   - Health check endpoint

2. **database.py**
   - SQLAlchemy database configuration
   - Database session management
   - Connection setup

3. **auth.py**
   - JWT token management
   - User authentication
   - Password hashing
   - User registration and login

4. **models.py**
   - SQLAlchemy ORM models
   - Database table definitions
   - Relationships between models
   - Includes User, Category, Entry, Metric, and Tag models

5. **schemas.py**
   - Pydantic data validation schemas
   - Request/response models
   - Data serialization/deserialization

### Routers

1. **categories.py**
   - CRUD operations for categories
   - Category listing and filtering
   - Category ownership management

2. **entries.py**
   - CRUD operations for entries
   - Entry categorization
   - Tag management for entries
   - Entry ownership management

3. **metrics.py**
   - CRUD operations for metrics
   - Progress tracking
   - Goal management
   - Metric value updates

4. **tags.py**
   - CRUD operations for tags
   - Tag usage statistics
   - Entry-tag relationships
   - Tag-based entry filtering

5. **analytics.py**
   - Entry statistics
   - Metric progress tracking
   - Tag usage analysis
   - Activity timeline

## Frontend Structure

### Core Components

1. **components/**
   - Reusable UI components
   - Form components
   - Layout components
   - Navigation components

2. **pages/**
   - Page-level components
   - Route-specific views
   - Page layouts

3. **services/**
   - API integration
   - Data fetching
   - State management
   - Authentication services

4. **utils/**
   - Helper functions
   - Constants
   - Type definitions
   - Utility hooks

## Features

- User authentication and authorization
- CRUD operations for entries, categories, and tags
- Metric tracking and goal setting
- Analytics and statistics
- Tag-based organization
- Category-based organization
- Activity timeline
- Progress tracking

## Setup Instructions

1. Clone the repository
2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
5. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
6. Start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```

## API Documentation

Once the backend server is running, visit `http://localhost:8000/docs` to access the Swagger UI documentation for all API endpoints.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 