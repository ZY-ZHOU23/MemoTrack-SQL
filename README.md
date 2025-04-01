# Personal Memo System

A full-stack application for managing personal memos, tracking metrics, and organizing information with categories and tags.

## Table of Contents
- [Project Structure](#project-structure)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Key Dependencies](#key-dependencies)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

```
personal-memo-system/
├── backend/                    # Main FastAPI application
│   ├── api/                   # API endpoints
│   │   └── api_v1/           # API version 1
│   │       ├── api.py        # Main API router
│   │       └── endpoints/    # Individual endpoint modules
│   ├── core/                 # Core configurations
│   ├── db/                   # Database configurations
│   ├── models/               # Database models
│   │   ├── base.py          # Base model class
│   │   ├── user.py          # User model
│   │   ├── category.py      # Category model
│   │   ├── entry.py         # Entry model
│   │   ├── metric.py        # Metric model
│   │   ├── tag.py           # Tag model
│   │   └── audit.py         # Audit logging model
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── utils/               # Utility functions
│   └── main.py              # Application entry point
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

## Features

- User authentication and authorization
- CRUD operations for entries, categories, and tags
- Metric tracking and goal setting
- Analytics and statistics
- Tag-based organization
- Category-based organization
- Activity timeline
- Progress tracking
- Customizable dashboard with recent entries at the top
- Advanced metrics visualization:
  - Summary statistics (average, min, max)
  - Raw metric values visualization with scatter plots and trend lines
  - Metrics organized by category and metric name
  - Time-based analysis of metric values

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
4. Configure environment variables:
   - Create a `.env` file in the project root with the following variables:
     ```
     DATABASE_URL=mysql://user:password@localhost:3306/personal_memo
     REDIS_URL=redis://localhost:6379
     SECRET_KEY=your_secret_key
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     ```
5. Apply database migrations:
   ```bash
   cd backend
   alembic upgrade head
   cd ..
   ```
6. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
7. Start the backend server:
   ```bash
   uvicorn backend.main:app --reload
   ```
8. Start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```

## Usage

- Access the application at `http://localhost:3000` after starting both the backend and frontend servers.
- Use the dashboard to manage memos, track metrics, and organize information.
- Explore the analytics section for insights and visualizations.

## API Documentation

Once the backend server is running, visit `http://localhost:8000/docs` to access the Swagger UI documentation for all API endpoints.

## Key Dependencies

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **Pydantic**: Data validation and settings management
- **MySQL**: Database storage
- **Redis**: Caching and performance optimization
- **JWT**: Authentication mechanism

### Frontend
- **React**: UI framework
- **Material-UI**: Component library
- **Chart.js**: Data visualization
- **Axios**: HTTP client
- **React Router**: Navigation
- **TypeScript**: Static typing

## License

This project is licensed under the MIT License - see the LICENSE file for details. 