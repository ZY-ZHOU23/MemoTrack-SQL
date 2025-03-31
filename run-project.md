
# Starting and Stopping the Personal Memo System

## Starting the Project

1. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
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
