#!/usr/bin/env bash
set -euo pipefail

echo "Build script: desktop PyInstaller bundle"

# check python
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found. Install Python 3.8+ and re-run."
  exit 1
fi

# create venv
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# activate
# shellcheck disable=SC1091
. venv/bin/activate

# upgrade pip
python -m pip install --upgrade pip setuptools wheel

# install deps
echo "Installing from requirements.txt..."
pip install -r requirements.txt

# attempt to install system deps for webview on Debian/Ubuntu
if command -v apt-get >/dev/null 2>&1; then
  echo "Attempting to ensure libwebkit2gtk present (Debian/Ubuntu). Sudo may be required."
  sudo apt-get update -y || true
  sudo apt-get install -y libwebkit2gtk-4.0-dev gir1.2-webkit2-4.0 || true
fi

# clean previous builds
rm -rf build dist __pycache__ desktop_main.spec

# run pyinstaller
echo "Running PyInstaller..."
pyinstaller --onefile --noconsole desktop_main.py

echo "Build complete. Output: dist/desktop_main"