@echo off
title HL7 Generator 2000
echo.
echo   Starting HL7 Generator 2000...
echo   The web dashboard will open at http://localhost:8080
echo   Press Ctrl+C to stop.
echo.

:: Open browser after a short delay (in background)
start "" /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8080"

:: Launch the app with auto-start from the directory where this bat lives
cd /d "%~dp0"
hl7gen.exe --auto-start
