#!/bin/bash

echo "Updating package lists..."
pkg update -y

echo "Installing dependencies..."
pkg install -y python git youtube-dl mpv

echo "Installing Python packages..."
pip install requests beautifulsoup4 termcolor tqdm

echo "Running the main script..."
python karaoke_search.py
