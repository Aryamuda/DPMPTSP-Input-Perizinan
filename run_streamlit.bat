@echo off

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python to continue.
    exit /b
)

:: Check if pip is installed
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo pip is not installed. Please install pip to continue.
    exit /b
)

:: Install dependencies
pip install -r requirements.txt

:: Run the Streamlit app
streamlit run app.py