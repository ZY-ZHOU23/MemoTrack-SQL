# Starting and Stopping the Personal Memo System

## Prerequisites

1. **MySQL database** must be running
2. **Redis server** must be running
3. **Environment variables** must be configured in a `.env` file:
   ```
   DATABASE_URL=mysql://user:password@localhost:3306/personal_memo
   REDIS_URL=redis://localhost:6379
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
4. **Python virtual environment** must be created and dependencies installed
5. **Node.js and npm** must be installed

## Starting the Project

1. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Apply database migrations** (if there are new migrations):
   ```bash
   cd backend
   alembic upgrade head
   cd ..
   ```

3. **Start the backend server**:
   ```bash
   # Run from the project root directory
   uvicorn backend.main:app --reload
   ```
   The backend will be available at: http://localhost:8000
   API documentation: http://localhost:8000/docs

4. **Start the frontend** (in a new terminal window):
   ```bash
   cd frontend
   npm start
   ```
   The frontend will be available at: http://localhost:3000

## Stopping the Project

1. **Stop the backend server**:
   Press `Ctrl+C` in the terminal where the backend is running.

2. **Stop the frontend server**:
   Press `Ctrl+C` in the terminal where the frontend is running.

3. **If processes are still running** (for example, if the backend crashed):
   ```bash
   # Find the process ID
   ps aux | grep uvicorn

   # Kill the process (replace PID with the actual process ID)
   kill -9 PID
   ```

4. **Deactivate the virtual environment**:
   ```bash
   deactivate
   ```

## Key Features

1. **User Authentication**: Register, login, and manage user sessions
2. **Memo Management**: Create, update, and delete personal memos
3. **Categorization**: Organize memos in categories
4. **Tagging**: Add tags to memos for easier searching and filtering
5. **Metrics Tracking**: Add metrics to entries to track progress
6. **Dashboard**: View statistics and recent memos at a glance
7. **Metrics Visualization**:
   - Summary charts showing average, minimum, and maximum values for metrics
   - Raw metric values visualization with scatter plots and trend lines
   - Time-based analysis of metric progress

## Troubleshooting

1. **Database Connection Issues**:
   - Verify MySQL is running: `sudo systemctl status mysql`
   - Check database credentials in `.env` file
   - Ensure the database exists: `mysql -u root -p -e "SHOW DATABASES;"`

2. **Backend Startup Issues**:
   - Check for missing dependencies: `pip install -r requirements.txt`
   - Verify Python version (3.9+ recommended)
   - Check error logs for specific issues

3. **Frontend Startup Issues**:
   - Verify npm dependencies: `npm install`
   - Check for Node.js compatibility (v14+ recommended)
   - Clear npm cache if needed: `npm cache clean --force`
