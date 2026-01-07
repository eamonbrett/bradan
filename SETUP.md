# Setup Guide

Get running in 30 minutes.

---

## 1. Install Dependencies (3 min)

```bash
pip install -r requirements.txt
```

---

## 2. Configure MCP (15 min)

MCP (Model Context Protocol) connects Cursor to Google Calendar.

### Edit `~/.cursor/mcp.json`

Create or edit this file:

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

### Restart Cursor

**Important:** Quit and restart Cursor for MCP to load.

### Optional: Slack Integration

Add to the same `mcp.json`:

```json
{
  "mcpServers": {
    "gworkspace-mcp": { ... },
    "playground-slack-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "github:shopify-playground/slack-mcp"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-token",
        "SLACK_USER_TOKEN": "xoxp-your-token"
      }
    }
  }
}
```

Get tokens: [api.slack.com/apps](https://api.slack.com/apps)

---

## 3. Configure Settings (5 min)

Edit `system/automation/config.py`:

```python
# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DAILY_DIR = PROJECT_ROOT / "work" / "daily"
MEETINGS_DIR = PROJECT_ROOT / "work" / "meetings"

# Calendar settings
DEFAULT_TIMEZONE = "America/New_York"  # Change to yours
CALENDAR_NAME = "primary"

# Automation settings
DEFAULT_RUN_TIME = "07:00"  # 7 AM
```

---

## 4. Customize Memory Bank (5 min)

Edit `system/memory/activeContext.md` to add your:
- Current priorities
- Active projects
- Key stakeholders

This gives Claude context about your work.

---

## 5. Test It (2 min)

Open Cursor in this folder and ask Claude:

```
"Generate today's daily file"
```

**Success:** You see `work/daily/YYYY-MM-DD.md` with your calendar events!

---

## Troubleshooting

### Calendar events not showing

1. **Restart Cursor** (MCP loads on startup)
2. Test: Ask "Can you check my calendar?"
3. If fails: Check `~/.cursor/mcp.json` syntax
4. Try manual: `npx -y github:aaronsb/google-workspace-mcp`

### Files not generating

1. Check folder: `pwd` (should be in task-management)
2. Check templates: `ls system/templates/`
3. Check Python: `python --version` (need 3.8+)
4. Check permissions: `ls -la work/`

### MCP errors

- Restart Cursor
- Check JSON syntax in `~/.cursor/mcp.json`
- Ensure npx is installed: `npx --version`
- Check logs: `system/automation/automation.log`

### Authentication issues

Google Calendar authentication happens via MCP server:
1. First run will prompt for Google login
2. Grant calendar read permissions
3. Token saved automatically

---

## Daily Usage

### Morning
```
"Good morning"
```
→ Daily file created with calendar and priorities

### Throughout Day
Work through your Top 3 tasks in the daily file

### Weekly
- **Monday:** `"Generate this week's file"`
- **Friday:** `"Archive this week"`

---

## Key Commands

| Command | What It Does |
|---------|--------------|
| `"Good morning"` | Complete morning setup |
| `"Generate weekly summary"` | Extract meeting actions |
| `"Show me my priority inbox"` | Email + Slack prioritization |
| `"Archive this week"` | Archive + weekly review |
| `"Create decision log about X"` | Document decision |

---

## Customization

### Change Timezone

Edit `system/automation/config.py`:
```python
DEFAULT_TIMEZONE = "Europe/Dublin"  # Your timezone
```

### Adjust Templates

Edit files in `system/templates/`:
- `daily.md` - Daily file structure
- `meeting-v2.md` - Meeting note format
- `weekly.md` - Weekly planning format

### Modify Workflow

Edit `system/memory/systemPatterns.md` to document your workflow preferences.

---

## Backup Your Work

### Option 1: GitHub (Recommended)

```bash
git init
git remote add origin YOUR-GITHUB-REPO
git add .
git commit -m "Initial backup"
git push -u origin main
```

**Benefits:** Version control, multi-computer sync, disaster recovery

### Option 2: Google Drive

Move to Google Drive and create symlink:

```bash
mv ~/Documents/task-management ~/Google\ Drive/My\ Drive/
ln -s ~/Google\ Drive/My\ Drive/task-management ~/Documents/
```

**Benefits:** Automatic sync, zero maintenance

---

## Next Steps

1. **Use "Good morning" daily** for a week
2. **Trust the carry-forwards** - stop trying to remember things
3. **Create decision logs** - every time you debate something
4. **Keep Top 3 sacred** - don't list 10 tasks, pick 3
5. **Friday archive is key** - keeps system clean

---

## Get Help

- Check logs: `system/automation/automation.log`
- Review memory bank files: `system/memory/`
- Ask Claude: "Help me troubleshoot [issue]"

---

**You're ready!** Start tomorrow with: `"Good morning"`

