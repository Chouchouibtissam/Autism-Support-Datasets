#!/usr/bin/env bash
set -e

# Name of the virtual environment
VENV_NAME="my_venv"

# -------------------------------
# Check if virtual environment exists
# -------------------------------
if [ ! -f "$VENV_NAME/bin/activate" ]; then
    echo "Virtual environment not found. Creating $VENV_NAME..."
    python3 -m venv "$VENV_NAME"
else
    echo "Virtual environment $VENV_NAME already exists."
fi

# -------------------------------
# Activate virtual environment
# -------------------------------
source "$VENV_NAME/bin/activate"

# -------------------------------
# Upgrade pip
# -------------------------------
echo "Upgrading pip..."
python -m pip install --upgrade pip

# -------------------------------
# Install required packages
# -------------------------------
echo "Installing Python packages..."
python -m pip install -r requirements.txt

# -------------------------------
# Run pipeline
# -------------------------------
echo "Running crawling step..."
cd aquisition/crawler
scrapy crawl childmind_guide
scrapy crawl autismhub
scrapy crawl medscape
cd ../..

echo "Running extraction step..."
python extract/ask_autism.py
python extract/childmind.py
python extract/medscape.py
python extract/parents_guide_to_autism.py

echo "Running transform step..."
python transform/transform.py

echo "Pipeline finished successfully."
