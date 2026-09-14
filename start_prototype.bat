@echo off
echo =========================================================================
echo    KALAKART (kala-kart) - SIH 2026 PROTOTYPE LAUNCHER (PS 26090)
echo    Ministry of Social Justice and Empowerment (MoSJE)
echo =========================================================================
echo.
echo [1/3] Launching Master 11-Panel Frontend Prototype in Browser...
start "" "%~dp0index.html"

echo [2/3] Checking Backend Python Environment...
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [3/3] Starting FastAPI Backend on http://localhost:8000 ...
    cd /d "%~dp0backend"
    python -m uvicorn app.main:app --reload --port 8000
) else (
    echo [!] Python not found in PATH. Static frontend is live in browser!
    pause
)
