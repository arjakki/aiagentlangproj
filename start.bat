@echo off
if not exist .env (
    echo ERROR: .env file not found. Copy .env.example and fill in your credentials.
    exit /b 1
)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
