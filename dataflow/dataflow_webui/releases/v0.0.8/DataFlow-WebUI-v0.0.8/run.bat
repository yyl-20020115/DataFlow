@echo off
setlocal
cd /d "%~dp0"

cd backend

uvicorn app.main:app --reload --port 8000  --reload-dir app --host=0.0.0.0
