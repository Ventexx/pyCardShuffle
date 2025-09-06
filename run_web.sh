#!/usr/bin/env bash
set -euo pipefail

# Usage:
# PORT=8992 ./run_web.sh
: "${PORT:=8992}"

# pick python
if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "python3 or python not found on PATH." >&2
  exit 1
fi

# project module: prefer app_web.py then app.py
if [ -f "app_web.py" ]; then
  MODULE_NAME="app_web"
elif [ -f "app.py" ]; then
  MODULE_NAME="app"
else
  echo "No app_web.py or app.py found in current directory." >&2
  exit 1
fi

# create venv if missing
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  "$PYTHON" -m venv venv
fi

# activate venv
# shellcheck disable=SC1091
. venv/bin/activate

# upgrade pip
python -m pip install --upgrade pip setuptools wheel

# install requirements
echo "Installing from requirements.txt..."
pip install -r requirements.txt

echo "Running $MODULE_NAME:app on 0.0.0.0:$PORT"

# prefer Waitress, then Gunicorn, then Flask dev server
if command -v waitress-serve >/dev/null 2>&1; then
  exec waitress-serve --host=0.0.0.0 --port="$PORT" "${MODULE_NAME}:app"
elif command -v gunicorn >/dev/null 2>&1; then
  exec gunicorn -w 4 -b "0.0.0.0:${PORT}" "${MODULE_NAME}:app"
else
  # fallback to Flask builtin dev server
  export FLASK_APP="$MODULE_NAME"
  exec flask run --host=0.0.0.0 --port="$PORT"
fi