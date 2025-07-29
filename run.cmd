@echo off
REM Competitive Programming Test Runner (CMD)
REM Compiles and tests C++ solutions against test cases

setlocal enabledelayedexpansion

REM Get script directory
set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Show help if no arguments
if "%1"=="" (
    echo 🏃 Competitive Programming Test Runner
    echo ======================================
    echo.
    echo Usage:
    echo   run.cmd ^<filename^>                    # Run tests for filename.cpp
    echo   run.cmd ^<filename^> -g -DDEBUG        # Run with additional compile flags
    echo.
    echo Examples:
    echo   run.cmd 4A                          # Test 4A.cpp
    echo   run.cmd two_sum -O0 -g              # Test two_sum.cpp with debug flags
    echo.
    echo Note: The script automatically finds .cpp files in any subfolder
    exit /b 1
)

set "filename=%1"
shift /1

REM Collect remaining arguments as compile flags
set "compile_flags="
:collect_args
if "%1"=="" goto :done_collecting
set "compile_flags=%compile_flags% %1"
shift /1
goto :collect_args
:done_collecting

REM Check if Python script exists
set "PYTHON_SCRIPT=%SCRIPT_DIR%\scripts\test_runner.py"

echo.

REM Create necessary directories
set "IO_DIR=%SCRIPT_DIR%\io"
if not exist "%IO_DIR%" mkdir "%IO_DIR%"

REM Run the Python test runner
if "%compile_flags%"=="" (
    uv run python "%PYTHON_SCRIPT%" "%filename%"
) else (
    uv run python "%PYTHON_SCRIPT%" "%filename%" %compile_flags%
)

set "exit_code=%errorlevel%"
exit /b %exit_code%
