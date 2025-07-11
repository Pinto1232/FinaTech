@echo off
echo Starting FinaTech Development Environment...
echo.

echo [1/3] Starting Backend Server...
start "FinaTech Backend" cmd /k "cd backend && python app.py"

echo [2/3] Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo [3/3] Starting Frontend Server...
start "FinaTech Frontend" cmd /k "cd frontend && npm start"

echo.
echo Development servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause > nul