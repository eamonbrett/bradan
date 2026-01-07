#!/bin/bash
# Setup launchd (macOS native scheduler) for weekly meeting summary

echo "🚀 Setting up Weekly Summary with launchd (macOS)"
echo "================================================="

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Get the current user
CURRENT_USER=$(whoami)

# Create the plist file
PLIST_FILE="$HOME/Library/LaunchAgents/com.eamon.weekly-meeting-summary.plist"

cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.eamon.weekly-meeting-summary</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>$SCRIPT_DIR/weekly_meeting_summary.py</string>
        <string>1</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>$PROJECT_ROOT</string>
    
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    
    <key>StandardOutPath</key>
    <string>$SCRIPT_DIR/automation.log</string>
    
    <key>StandardErrorPath</key>
    <string>$SCRIPT_DIR/automation.log</string>
    
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

echo "✅ Created launchd plist file at:"
echo "   $PLIST_FILE"
echo ""

# Load the plist
launchctl unload "$PLIST_FILE" 2>/dev/null
launchctl load "$PLIST_FILE"

echo "✅ launchd job loaded successfully!"
echo ""
echo "The weekly summary will run every Monday at 7:00 AM"
echo ""
echo "🔧 Management Commands:"
echo "======================="
echo ""
echo "Check status:"
echo "  launchctl list | grep weekly-meeting-summary"
echo ""
echo "Run immediately (test):"
echo "  launchctl start com.eamon.weekly-meeting-summary"
echo ""
echo "Disable:"
echo "  launchctl unload $PLIST_FILE"
echo ""
echo "Re-enable:"
echo "  launchctl load $PLIST_FILE"
echo ""
echo "View logs:"
echo "  tail -f $SCRIPT_DIR/automation.log"
echo ""
echo "✅ Setup complete!"


