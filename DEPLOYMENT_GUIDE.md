# Telegram Bot VPS Deployment Guide

This guide will help you deploy your Telegram bot to a VPS using screen sessions and systemd services.

## 🚀 Quick Start (Screen Method)

### 1. Upload Your Bot to VPS

```bash
# On your local machine, upload the bot files
scp -r . user@your-vps-ip:/opt/telegram-bot/
```

### 2. Run the Deployment Script

```bash
# SSH into your VPS
ssh user@your-vps-ip

# Navigate to bot directory
cd /opt/telegram-bot

# Make scripts executable
chmod +x deploy.sh run_bot.sh manage_bot.sh

# Run deployment (optional - installs dependencies)
./deploy.sh
```

### 3. Configure Environment

```bash
# Edit the environment file
nano bot/.env
```

Fill in your configuration:
```env
BOT_TOKEN=your_bot_token_here
MONGODB_URI=mongodb+srv://user:pass@cluster/db?retryWrites=true&w=majority
MONGODB_DB=onii_bot
ADMIN_IDS=123456789,987654321
BOT_PUBLIC_USERNAME=YourBotUsername
```

### 4. Start the Bot

```bash
# Start the bot in a screen session
./manage_bot.sh start

# Check status
./manage_bot.sh status

# View logs
./manage_bot.sh logs

# Attach to session (to see real-time output)
./manage_bot.sh attach
```

## 🎮 Bot Management Commands

```bash
# Start bot
./manage_bot.sh start

# Stop bot
./manage_bot.sh stop

# Restart bot
./manage_bot.sh restart

# Check status
./manage_bot.sh status

# View logs
./manage_bot.sh logs

# Attach to screen session
./manage_bot.sh attach
```

## 🔧 Screen Session Management

### Manual Screen Commands

```bash
# List all screen sessions
screen -list

# Attach to bot session
screen -r telegram_bot

# Detach from session (while inside)
Ctrl+A, then D

# Kill a screen session
screen -S telegram_bot -X quit
```

## 🛠️ Alternative: Systemd Service (Auto-restart)

If you prefer systemd over screen for auto-restart:

### 1. Install the Service

```bash
# Copy service file
sudo cp telegram-bot.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service (auto-start on boot)
sudo systemctl enable telegram-bot

# Start service
sudo systemctl start telegram-bot
```

### 2. Manage Systemd Service

```bash
# Check status
sudo systemctl status telegram-bot

# View logs
sudo journalctl -u telegram-bot -f

# Restart service
sudo systemctl restart telegram-bot

# Stop service
sudo systemctl stop telegram-bot
```

## 📊 Monitoring & Logs

### Log Files
- **Screen method**: `/opt/telegram-bot/logs/bot.log`
- **Systemd method**: `sudo journalctl -u telegram-bot -f`

### Check Bot Health
```bash
# Check if bot is responding
curl -s "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe"

# Check screen session
screen -list

# Check systemd service
sudo systemctl status telegram-bot
```

## 🔒 Security Best Practices

### 1. Firewall Setup
```bash
# Allow SSH and block everything else
sudo ufw allow ssh
sudo ufw enable
```

### 2. Bot User (Recommended)
```bash
# Create dedicated user for bot
sudo useradd -m -s /bin/bash telegram-bot
sudo usermod -aG sudo telegram-bot

# Change ownership
sudo chown -R telegram-bot:telegram-bot /opt/telegram-bot

# Switch to bot user
sudo su - telegram-bot
```

### 3. Environment Security
```bash
# Secure .env file
chmod 600 bot/.env

# Don't commit .env to git
echo "bot/.env" >> .gitignore
```

## 🚨 Troubleshooting

### Bot Won't Start
```bash
# Check logs
./manage_bot.sh logs

# Check environment variables
cat bot/.env

# Test Python environment
cd /opt/telegram-bot
source venv/bin/activate
python bot/main.py
```

### Database Connection Issues
```bash
# Test MongoDB connection
python -c "
import motor.motor_asyncio
import asyncio
async def test():
    client = motor.motor_asyncio.AsyncIOMotorClient('your_mongodb_uri')
    await client.admin.command('ping')
    print('MongoDB connection successful!')
asyncio.run(test())
"
```

### Screen Session Issues
```bash
# Kill all screen sessions
screen -wipe

# Start fresh
./manage_bot.sh start
```

## 📈 Performance Optimization

### 1. Resource Monitoring
```bash
# Check system resources
htop
df -h
free -h
```

### 2. Log Rotation
```bash
# Create logrotate config
sudo nano /etc/logrotate.d/telegram-bot
```

Add:
```
/opt/telegram-bot/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    notifempty
    create 644 telegram-bot telegram-bot
}
```

### 3. Auto-restart on Crash
The systemd service automatically restarts on failure. For screen method, you can use a wrapper script:

```bash
# Create auto-restart wrapper
cat > /opt/telegram-bot/auto_restart.sh << 'EOF'
#!/bin/bash
while true; do
    ./manage_bot.sh start
    sleep 10
    if ! screen -list | grep -q telegram_bot; then
        echo "Bot crashed, restarting in 10 seconds..."
        sleep 10
    else
        sleep 60
    fi
done
EOF

chmod +x /opt/telegram-bot/auto_restart.sh
```

## 🎯 Production Checklist

- [ ] Bot token configured
- [ ] MongoDB connection working
- [ ] Environment variables set
- [ ] Logs directory created
- [ ] Firewall configured
- [ ] Bot responding to /start
- [ ] Auto-restart enabled
- [ ] Log rotation configured
- [ ] Monitoring set up
- [ ] Backup strategy in place

## 📞 Support

If you encounter issues:

1. Check logs: `./manage_bot.sh logs`
2. Verify configuration: `cat bot/.env`
3. Test manually: `python bot/main.py`
4. Check system resources: `htop`
5. Verify network connectivity

Your bot should now be running successfully on your VPS! 🎉
