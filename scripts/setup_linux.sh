#!/bin/bash
set -e  # Exit on error

echo "============================================="
echo "Setting up JK BMS Controller Dev Environment"
echo "============================================="

# Update package list and install Python3, venv, pip, git
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git

# Install VS Code (optional)
read -p "Install VS Code? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
    sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
    sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
    sudo apt update
    sudo apt install -y code
fi

# Clone repo (if not already in one)
read -p "Enter your GitHub repo URL (or press Enter to skip clone): " repo_url
if [ ! -z "$repo_url" ]; then
    git clone $repo_url
    cd jk-bms-controller
fi

# Create virtual environment
python3 -m venv .venv

# Activate and install deps
source .venv/bin/activate
pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Please create it."
fi

echo "============================================="
echo "Setup complete!"
echo "To start developing, activate the environment with:"
echo "    source .venv/bin/activate"
echo "Then run: python src/main.py"
echo "============================================="