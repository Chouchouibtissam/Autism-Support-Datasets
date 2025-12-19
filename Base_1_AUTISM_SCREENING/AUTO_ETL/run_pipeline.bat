@echo off
echo ========================================
echo AUTOMATED ETL PIPELINE
echo Autism Screening Data
echo ========================================
echo.

REM Activate virtual environment if exists
if exist ..\venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call ..\venv\Scripts\activate.bat
)

echo.
echo ========================================
echo STEP 1: EXTRACT
echo ========================================
python Code\Extract.py
if errorlevel 1 (
    echo.
    echo X Extract failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo STEP 2: TRANSFORM
echo ========================================
python Code\Transform.py
if errorlevel 1 (
    echo.
    echo X Transform failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo STEP 3: LOAD
echo ========================================
python Code\Load.py
if errorlevel 1 (
    echo.
    echo X Load failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo ETL PIPELINE COMPLETED SUCCESSFULLY
echo ========================================
echo.
pause