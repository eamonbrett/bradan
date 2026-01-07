#!/bin/bash
# Setup script for weekly meeting summary automation

echo "🚀 Setting up Weekly Meeting Summary Automation"
echo "================================================"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Make the Python script executable
chmod +x "$SCRIPT_DIR/weekly_meeting_summary.py"

# Create weekly-summaries directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/weekly-summaries"

# Get the current user
CURRENT_USER=$(whoami)

# Create a cron job that runs every Monday at 7:00 AM
CRON_COMMAND="0 7 * * 1 cd \"$PROJECT_ROOT\" && \"$SCRIPT_DIR/weekly_meeting_summary.py\" 1 >> \"$SCRIPT_DIR/automation.log\" 2>&1"

echo ""
echo "📅 Cron Job Configuration"
echo "========================="
echo "The following cron job will be added:"
echo ""
echo "$CRON_COMMAND"
echo ""
echo "This will run every Monday at 7:00 AM"
echo ""

# Ask user if they want to install the cron job
read -p "Do you want to install this cron job? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "weekly_meeting_summary.py"; then
        echo "⚠️  Cron job already exists. Skipping..."
    else
        # Add the cron job
        (crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -
        echo "✅ Cron job installed successfully!"
    fi
else
    echo "⏭️  Skipping cron job installation"
    echo ""
    echo "To manually run the weekly summary, use:"
    echo "  cd \"$PROJECT_ROOT\" && ./automation/weekly_meeting_summary.py"
fi

echo ""
echo "📝 Additional Setup Options"
echo "==========================="
echo ""
echo "Alternative scheduling options:"
echo ""
echo "1. Using launchd (macOS native, more reliable):"
echo "   ./automation/setup_launchd_weekly_summary.sh"
echo ""
echo "2. Manual execution:"
echo "   cd \"$PROJECT_ROOT\" && ./automation/weekly_meeting_summary.py"
echo ""
echo "3. For last 2 weeks:"
echo "   cd \"$PROJECT_ROOT\" && ./automation/weekly_meeting_summary.py 2"
echo ""
echo "✅ Setup complete!"
echo ""
echo "Weekly summaries will be saved to: $PROJECT_ROOT/weekly-summaries/"


