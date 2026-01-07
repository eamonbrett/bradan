# Task Management Setup Guide

Get running in 30 minutes.

---

## Prerequisites

- Cursor IDE ([cursor.com](https://cursor.com))
- Python 3.8+
- Google Workspace account

---

## Setup (5 Steps)

### 1. Get the Files (2 min)

**GitHub Template:**
```bash
# Click "Use this template" on GitHub, then:
git clone YOUR-REPO-URL
cd your-task-management
```

**OR from ZIP:**
```bash
# Extract to:
cd ~/Documents/task-management
```

---

### 2. Install Dependencies (3 min)

```bash
pip install -r requirements.txt
```

---

### 3. Configure MCP (15 min)

Edit `~/.cursor/mcp.json`:

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

**Restart Cursor!**

Optional - Add Slack:
```json
"playground-slack-mcp": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "github:shopify-playground/slack-mcp"],
  "env": {
    "SLACK_BOT_TOKEN": "xoxb-your-token",
    "SLACK_USER_TOKEN": "xoxp-your-token"
  }
}
```

Get Slack tokens: [api.slack.com/apps](https://api.slack.com/apps)

---

### 4. Configure Settings (5 min)

Edit `automation/config.py`:

```python
USER_NAME = "Your Name"
USER_EMAIL = "you@example.com"
TIMEZONE = "America/New_York"  # Change to yours
```

---

### 5. Test It (5 min)

Open Cursor in the folder and ask:

```
"Generate today's daily file"
```

✅ **Success:** You see `daily/YYYY-MM-DD.md` with your calendar events!

---

## Daily Usage

### Morning (30 seconds)

Ask Cursor:
```
"Good morning"
```

Gets:
- Today's calendar
- Recent email/Slack
- Generated daily file
- Top 3 priorities

### Throughout Day

Work through your Top 3 in `daily/YYYY-MM-DD.md`

### Evening (5 min)

Check off completed tasks, add notes

---

## Weekly Workflow

### Monday (15 min)
```
"Generate weekly summary"
"Generate week plan"  
"Generate daily file"
```

### Friday (20 min)
```
"This week is over"  # Archives files, creates review
```

---

## Troubleshooting

### Calendar events not showing

1. Restart Cursor
2. Test: Ask "Can you check my calendar?"
3. If fails: Run `npx -y github:aaronsb/google-workspace-mcp` manually

### Files not generating

1. Check you're in right folder: `pwd`
2. Check templates exist: `ls daily/template-*.md`
3. Ask Cursor to check permissions

### MCP errors

Restart Cursor. MCP servers load on startup.

---

## Customization

**Templates:** Edit files in `daily/`, `meetings/`, `weekly-plans/`

**Strategic Focus:** Edit `memory-bank/activeContext.md`

**Your Workflow:** Update `memory-bank/systemPatterns.md`

---

## Key Commands

| Command | What It Does |
|---------|-------------|
| `"Good morning"` | Complete morning setup |
| `"Generate weekly summary"` | Extract meeting actions |
| `"Show me my priority inbox"` | Email + Slack prioritization |
| `"This week is over"` | Archive + weekly review |
| `"Create decision log about X"` | Document a decision |

---

## File Structure

```
task-management/
├── daily/           # Current week only
├── meetings/        # Meeting notes
├── decisions/       # Decision logs
├── reviews/         # Weekly/monthly
├── archive/         # Historical
├── automation/      # Scripts (don't edit)
└── memory-bank/     # AI context
```

---

## Tips

**Week 1:** Use "Good morning" every day  
**Week 2:** Try priority inbox and decision logs  
**Week 3:** Customize templates  

---

## Get Help

- Check logs: `automation/automation.log`
- Read memory-bank files
- Ask Cursor: "Help me troubleshoot [issue]"

---

**That's it. You're ready!**

Start tomorrow with: `"Good morning"`
