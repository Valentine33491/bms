@echo off
echo =============================================
echo Setting up JK BMS Controller Dev Environment
echo =============================================
echo.

REM Check if winget is available
where winget >nul 2>nul
if %errorlevel% neq 0 (
    echo winget not found. Please install App Installer from Microsoft Store.
    pause
    exit /b 1
)

REM Install Python (using winget)
echo Installing Python 3.12...
winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements

REM Install Git
echo Installing Git...
winget install Git.Git --accept-package-agreements --accept-source-agreements

REM Install Visual Studio Code (optional, but recommended for dev)
echo.
echo Installing VS Code (optional, you can skip this)...
winget install Microsoft.VisualStudioCode --accept-package-agreements --accept-source-agreements

REM Clone the repository (if not already in it)
echo.
set /p repo_url="Enter your GitHub repo URL (or press Enter to skip clone): "
if not "%repo_url%"=="" (
    git clone %repo_url%
    cd jk-bms-controller
)

REM Create virtual environment
echo.
echo Creating Python virtual environment...
python -m venv .venv

REM Activate and install requirements
echo Installing dependencies from requirements.txt...
call .venv\Scripts\activate.bat
pip install --upgrade pip
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found. Please create it.
)

echo.
echo =============================================
echo Setup complete!
echo To start developing, activate the environment with:
echo     .venv\Scripts\activate
echo Then run: python src/main.py
echo =============================================
pause