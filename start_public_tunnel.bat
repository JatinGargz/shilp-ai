@echo off
title SHILP AI - Public Cloudflare Tunnel
echo ============================================================
echo   SHILP AI - Starting Live Public HTTPS Tunnel
echo ============================================================
echo.
"C:\Users\Jatin\.gemini\antigravity\scratch\cloudflared.exe" tunnel --url http://127.0.0.1:8000
pause
