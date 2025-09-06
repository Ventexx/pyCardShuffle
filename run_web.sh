#!/usr/bin/env bash
set -euo pipefail

# pick python
if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "python3 or python not found on PATH." >&2
  exit 1
fi

# upgrade pip
python -m pip install --upgrade pip setuptools wheel

# create venv if missing
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  "$PYTHON" -m venv venv
fi

# activate venv
. venv/bin/activate

# install requirements
echo "Installing from requirements.txt..."
pip install -r requirements.txt

# Start app
python app.py