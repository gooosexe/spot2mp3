#!/bin/bash

# Check if Python is installed
if! command -v python &> /dev/null; then
    echo "Python could not be found"
    exit 1
fi

# Check if pip is installed
if! command -v pip &> /dev/null; then
    echo "pip could not be found"
    exit 1
fi

# Install the required Python packages
echo "Installing Python packages..."
pip install spotipy pytube pydub google-api-python-client mutagen

echo "Installation completed successfully."