@echo off
setlocal enabledelayedexpansion

:: check for python
python --version >nul 2>&1
if errorlevel 1 (
  echo Python not found on PATH. Install Python 3.8+ and re-run.
  pause
  exit /b 1
)

:: create venv if missing
if not exist "venv\Scripts\activate" (
  echo Creating virtual environment...
  python -m venv venv
)

:: activate venv
call venv\Scripts\activate

:: upgrade pip & build tools
python -m pip install --upgrade pip setuptools wheel

:: install dependencies
echo Installing from requirements.txt...
pip install -r requirements.txt
pip install pyinstaller

:: clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
if exist desktop_main.spec del /q desktop_main.spec

:: build single-file exe
echo Running PyInstaller...
pyinstaller --onefile --noconsole desktop_main.py

if errorlevel 1 (
  echo PyInstaller failed.
  pause
  exit /b 1
)

:: done
echo Build complete.
echo Output: dist\desktop_main.exe
pause
endlocal
