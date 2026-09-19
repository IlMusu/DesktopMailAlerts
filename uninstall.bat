@echo off
setlocal

set "APP_NAME=Desktop Mail Notifier"

echo Uninstalling %APP_NAME%

:: ################### KILLING CURRENT TASK
echo.
echo Destroying scheduled task...

taskkill /F /IM "%APP_NAME%.exe" >nul 2>&1
schtasks /Delete /TN "%APP_NAME%" /F >nul 2>&1

echo [92mDone![0m

:: ################### CLEARING PREVIOUS BUILD

echo.
echo Clearing previous build...

if exist "dist" rmdir /S /Q "dist"
if exist "build" rmdir /S /Q "build"
if exist "%APP_NAME%.spec" del /Q "%APP_NAME%.spec"

echo [92mDone![0m

:: ################### UNINSTALLATION DONE

echo.
echo [92mUninstallation complete![0m

if /I not "%~1"=="silent" pause