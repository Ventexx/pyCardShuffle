@echo off
setlocal

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

:: pick module (app_web.py preferred)
if exist app_web.py (
  set "MODULE_NAME=app_web"
) else (
  set "MODULE_NAME=app"
)
set "APP_MODULE=%MODULE_NAME%:app"

:: try to run with Waitress (production). fallback to builtin server.
where.exe waitress-serve >nul 2>&1
if %errorlevel%==0 (
  echo Starting production server with Waitress on http://0.0.0.0:8992
  waitress-serve --port=8992 %APP_MODULE%
) else (
  echo Waitress not found. Starting Flask builtin server on http://0.0.0.0:8992
  python -u -c "import %MODULE_NAME% as m; m.app.run(host='0.0.0.0', port=8992)"
)

endlocal