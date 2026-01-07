# Technical Context: Implementation Details

## Technology Stack

### Core Technologies
- **Python 3.8+**: Main automation language
- **Cursor IDE**: AI-powered development environment with MCP support
- **Google Workspace MCP**: Calendar integration via Model Context Protocol
- **Markdown**: File format (maintaining existing structure)
- **macOS/Linux/Windows**: Cross-platform compatible
- **Zsh/Bash**: Shell environment

### Dependencies
```python
# requirements.txt
requests>=2.28.0
python-dateutil>=2.8.0
pyyaml>=6.0
pytz>=2023.3
```

### Development Setup
```bash
# Project structure
cd ~/Documents/task-management
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Google Workspace MCP Integration
- **Authentication**: OAuth2 flow via MCP server
- **Scope**: Calendar read access (`https://www.googleapis.com/auth/calendar.readonly`)
- **API Endpoints**: 
  - List calendars
  - Get calendar events
  - Query availability

### Configuration Management
```yaml
# config.yaml
calendar:
  primary_calendar: "primary"
  time_zone: "America/New_York"  # Adjust to your timezone
  
templates:
  daily_template: "system/templates/daily.md"
  meeting_template: "system/templates/meeting-v2.md"

paths:
  daily_dir: "work/daily"
  meetings_dir: "work/meetings"
  
automation:
  run_time: "07:00"  # 7 AM daily
  check_existing: true
```

## Technical Constraints

### File System
- **Cross-Platform Paths**: Use Path library for reliability
- **Permissions**: Ensure read/write access to project directory
- **Concurrent Access**: Handle potential file locking issues

### Calendar API
- **Rate Limits**: Google Calendar API quotas
- **Authentication**: Handle token refresh automatically
- **Timezone Handling**: Convert all times to local timezone

### Error Recovery
- **Network Issues**: Retry logic with exponential backoff
- **API Failures**: Fallback to manual template without calendar data
- **File Conflicts**: Skip existing files, log warnings

## Deployment Strategy

### Local Development
- Manual execution during development
- Configuration via environment variables
- Logging to console for debugging

### Production Automation
- **Cursor-triggered**: Say "Good morning" to Claude in Cursor
- **Logging**: File-based logging for monitoring
- **Configuration**: YAML config file
- **Error Notifications**: Optional email/slack alerts

## Security Considerations
- **API Keys**: Store in environment variables or secure config
- **File Permissions**: Restrict access to task management directory
- **Calendar Access**: Minimal scope (read-only calendar access)
- **Logging**: Avoid logging sensitive calendar information

## MCP Architecture

### How MCP Works in This System
```
User: "Generate today's daily file"
    ↓
Claude (in Cursor) ← Has access to MCP servers
    ↓
MCP Server Call: gworkspace-mcp calendar_events
    ↓
Python Processing: cursor_generate_daily.py
    ↓
Output: Daily file with real calendar data
```

### MCP Server Configuration
Located in `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "gworkspace-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "github:aaronsb/google-workspace-mcp"]
    }
  }
}
```

## Platform Compatibility

### macOS
- Full support
- Native path handling
- cron for scheduling (optional)

### Linux
- Full support
- Use appropriate paths
- cron for scheduling (optional)

### Windows
- Compatible with WSL or native Python
- Adjust paths for Windows filesystem
- Task Scheduler for automation (optional)
