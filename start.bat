@echo off
title MediAI - Starting Servers

echo Starting MediAI Backend on port 3000...
start "MediAI Backend" cmd /k "cd /d "%~dp0backend" && "C:\Users\Yashwant\AppData\Local\Programs\Python\Python313\python.exe" -m uvicorn main:app --reload --port 3000"

timeout /t 2 /nobreak >nul

echo Starting MediAI Frontend on port 8080...
start "MediAI Frontend" cmd /k "cd /d "%~dp0frontend" && "C:\Users\Yashwant\AppData\Local\Programs\Python\Python313\python.exe" -m http.server 8080"

timeout /t 3 /nobreak >nul

echo.
echo Both servers are running!
echo Frontend: http://localhost:8080
echo Backend:  http://localhost:3000/api/health
echo.
start "" "http://localhost:8080"
