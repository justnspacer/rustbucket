#!/bin/bash
# Quick start script for Nothing App

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/Scripts/activate
fi

# Run the application
python main.py
