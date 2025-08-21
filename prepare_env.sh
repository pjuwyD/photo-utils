#!/bin/bash

set -e

echo "Creating Python virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
# shellcheck disable=SC1091
source venv/bin/activate

echo "Checking for required system dependencies..."

SYSTEM_DEPS=(exiftool)
MISSING_DEPS=()

for dep in "${SYSTEM_DEPS[@]}"; do
    if ! command -v "$dep" >/dev/null 2>&1; then
        MISSING_DEPS+=("$dep")
    fi
done

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo "The following system packages are required but not installed: ${MISSING_DEPS[*]}"
    read -p "Do you want to install them now? [y/N] " yn
    case $yn in
        [Yy]* )
            if ! command -v brew >/dev/null 2>&1; then
                echo "Homebrew not found. Please install Homebrew first: https://brew.sh/"
                exit 1
            fi
            for dep in "${MISSING_DEPS[@]}"; do
                brew install "$dep"
            done
            ;;
        * ) echo "Skipping system package installation. You may need to install them manually."; ;;
    esac
else
    echo "All required system dependencies are installed."
fi

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Environment setup complete. You can now use the virtual environment."