#!/bin/bash

echo "========================================"
echo "AUTOMATED ETL PIPELINE"
echo "Autism Screening Data"
echo "========================================"
echo ""

# Activate virtual environment if exists
if [ -d "../venv" ]; then
    echo "Activating virtual environment..."
    source ../venv/bin/activate
fi

echo ""
echo "========================================"
echo "STEP 1: EXTRACT"
echo "========================================"
python Code/Extract.py
if [ $? -ne 0 ]; then
    echo ""
    echo "X Extract failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "STEP 2: TRANSFORM"
echo "========================================"
python Code/Transform.py
if [ $? -ne 0 ]; then
    echo ""
    echo "X Transform failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "STEP 3: LOAD"
echo "========================================"
python Code/Load.py
if [ $? -ne 0 ]; then
    echo ""
    echo "X Load failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "ETL PIPELINE COMPLETED SUCCESSFULLY"
echo "========================================"
echo ""
echo "All steps executed:"
echo "  - Extract: Data downloaded"
echo "  - Transform: Data cleaned and merged"
echo "  - Load: Data loaded into Oracle"
echo ""