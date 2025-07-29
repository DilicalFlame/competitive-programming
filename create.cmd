@echo off
REM Competitive Programming File Generator (CMD)
REM Creates boilerplate files for different platforms

setlocal enabledelayedexpansion

REM Get script directory
set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Check if Python script exists
set "PYTHON_SCRIPT=%SCRIPT_DIR%\scripts\file_generator.py"

if not exist "%PYTHON_SCRIPT%" (
    echo ❌ Error: Python script not found at %PYTHON_SCRIPT%
    exit /b 1
)

REM Run the Python script
uv run python "%PYTHON_SCRIPT%" %*

REM Check if the script ran successfully
if %errorlevel% equ 0 (
    echo.
    echo 🎉 Happy coding! Good luck with your competitive programming!
) else (
    echo.
    echo ❌ Something went wrong. Please check the error messages above.
    exit /b 1
)

goto :eof

:install_if_missing
set "package=%~1"
uv run python -c "import %package%" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing %package%...
    uv add %package% >nul 2>&1
    if !errorlevel! neq 0 (
        echo ⚠️  Could not install %package% automatically. Falling back to basic UI.
    )
)
goto :eof
