@echo off

:: check python
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

:: upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: install requirements
echo Installing from requirements.txt...
pip install -r requirements.txt

:: start app
python app.py