@echo off
CHCP 65001 > NUL
SETLOCAL

REM --- Configuration ---
SET SERVER_PORT=8000
SET DB_FILE=audioreflex.db
SET SERVER_DIR=server
SET CLIENT_MAIN=main.py

ECHO =======================================
ECHO Starting Audio Reflex Game Environment
ECHO =======================================

REM --- 1. Terminate existing processes on port %SERVER_PORT% ---
ECHO.
ECHO --- Checking for existing server process on port %SERVER_PORT% ---
FOR /F "tokens=5" %%a IN ('netstat -ano ^| findstr :%SERVER_PORT%') DO (
    SET PID=%%a
    GOTO :KILL_PROCESS
)
GOTO :NO_PROCESS

:KILL_PROCESS
ECHO Found process %PID% using port %SERVER_PORT%. Attempting to terminate...
TASKKILL /PID %PID% /F > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Failed to terminate process %PID%. It might be running as administrator or not exist.
) ELSE (
    ECHO Process %PID% terminated.
)
TIMEOUT /T 2 /NOBREAK > NUL
GOTO :CONTINUE

:NO_PROCESS
ECHO No process found on port %SERVER_PORT%.
GOTO :CONTINUE

:CONTINUE

REM --- 2. Delete existing database file ---
ECHO.
ECHO --- Deleting old database file (%DB_FILE%) ---
IF EXIST %DB_FILE% (
    DEL %DB_FILE%
    ECHO Deleted %DB_FILE%. New database will be created.
) ELSE (
    ECHO %DB_FILE% not found.
)
TIMEOUT /T 1 /NOBREAK > NUL

REM --- 3. Start the FastAPI server ---
ECHO.
ECHO --- Starting FastAPI server ---
START /B "" python -m uvicorn %SERVER_DIR%.main:app --host 127.0.0.1 --port %SERVER_PORT%
ECHO Server starting... Please wait a few seconds.
TIMEOUT /T 5 /NOBREAK > NUL

REM --- 4. Start the game client ---
ECHO.
ECHO --- Starting Audio Reflex Client ---
python %CLIENT_MAIN%

ECHO.
ECHO =======================================
ECHO Game client closed. Stopping server...
ECHO =======================================

REM --- Optional: Wait for user to terminate server if it's still running ---
REM This is tricky as the server is started in a new window.
REM The /B flag starts it in the same window, but without --reload it might not pick up changes.
REM For simplicity, we assume the user will manually close the server window if they want to.
REM Alternatively, we could kill the python processes.

ENDLOCAL