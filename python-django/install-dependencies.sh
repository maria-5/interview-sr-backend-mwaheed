#!/usr/bin/bash

# Codespace run this script to install dependencies

# Install dependencies for the backend
echo "Installing Python dependencies..."
pip install --user -r python-django/requirements.txt

# Install dependencies for the frontend
echo "Installing Node.js dependencies..."
cd python-django/interview-calendar-frontend && npm ci

echo "Installation complete!"
