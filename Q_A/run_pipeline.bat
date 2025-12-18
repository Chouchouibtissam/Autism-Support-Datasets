@echo off
setlocal

REM Name of the virtual environment
set VENV_NAME=my_venv

REM -------------------------------
REM Check if virtual environment exists
REM -------------------------------
if not exist "%VENV_NAME%\Scripts\activate.bat" (
    echo Virtual environment not found. Creating %VENV_NAME%...
    python -m venv %VENV_NAME%
    if errorlevel 1 (
        echo Failed to create virtual environment
        exit /b 1
    )
) else (
    echo Virtual environment %VENV_NAME% already exists.
)

REM -------------------------------
REM Activate virtual environment
REM -------------------------------
call "%VENV_NAME%\Scripts\activate.bat"

REM -------------------------------
REM Upgrade pip
REM -------------------------------
echo Upgrading pip...
python -m pip install --upgrade pip

REM -------------------------------
REM Install required packages
REM -------------------------------
echo Installing Python packages...
python -m pip install -r requirements.txt

REM -------------------------------
REM Run pipeline
REM -------------------------------
echo Running crawling step...
cd aquisition/crawler
scrapy crawl childmind_guide
scrapy crawl autismhub
scrapy crawl medscape
cd ../..

echo Running extraction step...
python extract\ask_autism.py
python extract\childmind.py
python extract\medscape.py
python extract\parents_guide_to_autism.py

echo Running transform step...
python transform\transform.py

echo Pipeline finished successfully.
endlocal