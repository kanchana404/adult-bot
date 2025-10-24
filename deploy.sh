#!/bin/bash

# Telegram Bot Deployment Script for VPS
# This script sets up the bot environment and dependencies

set -e

echo "🚀 Starting Telegram Bot Deployment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3.11+ and pip
echo "🐍 Installing Python 3.11+ and pip..."

# Check if Python 3.11 is available, otherwise use available version
if apt list python3.11 2>/dev/null | grep -q python3.11; then
    echo "Installing Python 3.11..."
    sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
else
    echo "Python 3.11 not available, installing latest Python 3.x..."
    sudo apt install -y python3 python3-venv python3-dev python3-pip
    
    # Check Python version
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo "Installed Python version: $PYTHON_VERSION"
    
    # Create symlink for python3.11 if needed
    if [ ! -f /usr/bin/python3.11 ]; then
        echo "Creating python3.11 symlink..."
        sudo ln -sf /usr/bin/python3 /usr/bin/python3.11
    fi
fi

# Install MongoDB (if not using cloud MongoDB)
echo "🍃 Installing MongoDB..."

# Get Ubuntu codename
UBUNTU_CODENAME=$(lsb_release -cs)

# Add MongoDB GPG key using new method
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu $UBUNTU_CODENAME/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update package list and install MongoDB
sudo apt update
sudo apt install -y mongodb-org

# Start and enable MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

echo "✅ MongoDB installed and started"

# Install screen for session management
echo "📺 Installing screen..."
sudo apt install -y screen

# Create bot directory
echo "📁 Setting up bot directory..."
BOT_DIR="/opt/telegram-bot"
sudo mkdir -p $BOT_DIR
sudo chown $USER:$USER $BOT_DIR

# Copy bot files (assuming you're in the bot directory)
echo "📋 Copying bot files..."
cp -r . $BOT_DIR/

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
cd $BOT_DIR
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r bot/requirements.txt

# Create .env file from template
echo "⚙️ Setting up environment file..."
if [ ! -f bot/.env ]; then
    cp bot/env.example bot/.env
    echo "📝 Created bot/.env file. Please edit it with your configuration!"
fi

# Create logs directory
echo "📝 Creating logs directory..."
mkdir -p logs

# Set proper permissions
echo "🔐 Setting permissions..."
chmod +x run_bot.sh
chmod +x manage_bot.sh

echo "✅ Deployment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit bot/.env with your configuration"
echo "2. Run: ./manage_bot.sh start"
echo "3. Check logs: tail -f logs/bot.log"
echo ""
echo "🔧 Configuration file: bot/.env"
echo "📊 Logs: logs/bot.log"
echo "🎮 Management: ./manage_bot.sh"
