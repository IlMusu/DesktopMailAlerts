@echo off
setlocal

set "APP_NAME=Desktop Mail Notifier"
set "CHECK_INTERVAL_MINUTES=30"

echo Installing %APP_NAME%

set "PROJECT_DIR=%~dp0"
set "PROJECT_DIR=%PROJECT_DIR:~0,-1%"

cd /d "%PROJECT_DIR%"

:: ################### CLEARING PREVIOUS BUILD

call uninstall.bat silent

:: ################### CHECKING PYTHON

where python >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not available in PATH.
    pause
    exit /b 1
)

:: ################### CREATING PYTHON VIRTUAL ENVIRONMENT

echo.
echo Creating virtual environment...
if not exist ".venv" (
    python -m venv ".venv"
)

set "PYTHON=%PROJECT_DIR%\.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

echo [92mDone![0m

:: ################### INSTALLING PYTHON DEPENDENCIES

echo.
echo Installing dependencies...
"%PYTHON%" -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip.
    pause
    exit /b 1
)

"%PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)
echo [92mDone![0m

:: ################### BUILDING EXECUTABLE APPLICATION

echo.
echo Building Desktop Mail Notifier...

"%PYTHON%" -m PyInstaller --noconfirm --clean --noconsole --name "%APP_NAME%" main.py

if errorlevel 1 (
    echo.
    echo Failed to build Desktop Mail Notifier.
    pause
    exit /b 1
)

set "APP_EXE=%PROJECT_DIR%\dist\%APP_NAME%\%APP_NAME%.exe"

if not exist "%APP_EXE%" (
    echo.
    echo Application executable was not created.
    pause
    exit /b 1
)
echo [92mDone![0m

:: ################### CREATING WINDOWS SCHEDULED TASK

echo.
echo Creating scheduled task...

schtasks /Create /TN "Desktop Mail Notifier" /TR "\"%APP_EXE%\"" /SC MINUTE /MO %CHECK_INTERVAL_MINUTES% /F

if errorlevel 1 (
    echo.
    echo Failed to create scheduled task.
    pause
    exit /b 1
)

echo [92mDone![0m

:: ################### INSTALLATION DONE

echo.
echo [92mInstallation complete![0m

:: ################### STARTING APPLICATION

echo.
echo Starting Desktop Mail Notifier...
start "" "%APP_EXE%"
echo [92mDone![0m

echo.
pause