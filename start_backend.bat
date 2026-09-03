@echo off
echo Starting SHILP AI Backend Server...
cd backend
python -m uvicorn app.main:app --reload --port 8000
