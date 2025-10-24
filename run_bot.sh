#!/bin/bash

# Telegram Bot Runner Script
# This script runs the bot in a screen session

BOT_DIR="/opt/telegram-bot"
SCREEN_NAME="telegram_bot"
LOG_FILE="$BOT_DIR/logs/bot.log"

# Create logs directory if it doesn't exist
mkdir -p "$BOT_DIR/logs"

# Function to check if screen session exists
check_screen() {
    screen -list | grep -q "$SCREEN_NAME"
}

# Function to start the bot
start_bot() {
    if check_screen; then
        echo "❌ Bot is already running in screen session '$SCREEN_NAME'"
        echo "   Use: screen -r $SCREEN_NAME to attach"
        exit 1
    fi
    
    echo "🚀 Starting Telegram Bot..."
    echo "📁 Bot directory: $BOT_DIR"
    echo "📺 Screen session: $SCREEN_NAME"
    echo "📝 Log file: $LOG_FILE"
    
    # Change to bot directory
    cd "$BOT_DIR"
    
    # Activate virtual environment and start bot
    screen -dmS "$SCREEN_NAME" bash -c "
        source venv/bin/activate && \
        cd bot && \
        python main.py 2>&1 | tee -a ../logs/bot.log
    "
    
    sleep 2
    
    if check_screen; then
        echo "✅ Bot started successfully!"
        echo "📺 Attach to session: screen -r $SCREEN_NAME"
        echo "📝 View logs: tail -f $LOG_FILE"
        echo "🛑 Stop bot: screen -S $SCREEN_NAME -X quit"
    else
        echo "❌ Failed to start bot. Check logs: $LOG_FILE"
        exit 1
    fi
}

# Function to stop the bot
stop_bot() {
    if ! check_screen; then
        echo "❌ Bot is not running"
        exit 1
    fi
    
    echo "🛑 Stopping Telegram Bot..."
    screen -S "$SCREEN_NAME" -X quit
    
    sleep 2
    
    if ! check_screen; then
        echo "✅ Bot stopped successfully!"
    else
        echo "❌ Failed to stop bot"
        exit 1
    fi
}

# Function to restart the bot
restart_bot() {
    echo "🔄 Restarting Telegram Bot..."
    stop_bot
    sleep 3
    start_bot
}

# Function to show bot status
status_bot() {
    if check_screen; then
        echo "✅ Bot is running in screen session '$SCREEN_NAME'"
        echo "📺 Attach: screen -r $SCREEN_NAME"
        echo "📝 Logs: tail -f $LOG_FILE"
    else
        echo "❌ Bot is not running"
    fi
}

# Function to show logs
logs_bot() {
    if [ -f "$LOG_FILE" ]; then
        echo "📝 Showing last 50 lines of bot logs:"
        echo "----------------------------------------"
        tail -n 50 "$LOG_FILE"
        echo "----------------------------------------"
        echo "📝 Follow logs: tail -f $LOG_FILE"
    else
        echo "❌ Log file not found: $LOG_FILE"
    fi
}

# Main script logic
case "$1" in
    start)
        start_bot
        ;;
    stop)
        stop_bot
        ;;
    restart)
        restart_bot
        ;;
    status)
        status_bot
        ;;
    logs)
        logs_bot
        ;;
    attach)
        if check_screen; then
            echo "📺 Attaching to bot session..."
            screen -r "$SCREEN_NAME"
        else
            echo "❌ Bot is not running"
            exit 1
        fi
        ;;
    *)
        echo "🤖 Telegram Bot Management Script"
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs|attach}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the bot in a screen session"
        echo "  stop    - Stop the bot"
        echo "  restart - Restart the bot"
        echo "  status  - Show bot status"
        echo "  logs    - Show recent logs"
        echo "  attach  - Attach to bot screen session"
        echo ""
        echo "Examples:"
        echo "  $0 start"
        echo "  $0 status"
        echo "  $0 logs"
        echo "  $0 attach"
        exit 1
        ;;
esac
