@echo off
setlocal

:: Check if Python is installed
where python >nul 2>nul || (
    echo Python could not be found. Please install Python and run this script again.
    exit /b 1
)

:: Check if pip is installed
where pip >nul 2>nul || (
    echo pip could not be found. Please install pip and run this script again.
    exit /b 1
)

:: Install the required Python packages
echo Installing Python packages...
pip install spotipy pytube pydub google-api-python-client mutagen

echo Installation completed successfully.
