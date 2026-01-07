# Quick Start

**One-page reference** - print this!

---

## Setup (30 min)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure MCP (~/.cursor/mcp.json)
{
  "mcpServers": {
    "gworkspace-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "github:aaronsb/google-workspace-mcp"]
    }
  }
}

# 3. Restart Cursor

# 4. Edit system/automation/config.py (set timezone)

# 5. Test
# Ask Claude: "Generate today's daily file"
```

---

## Daily Commands

| Say | Result |
|-----|--------|
| `"Good morning"` | Daily file + calendar + priorities |
| `"Show me my priority inbox"` | Email + Slack prioritized |
| `"Create decision log about X"` | Document decision |

---

## Weekly Commands

| Day | Say | Result |
|-----|-----|--------|
| **Monday** | `"Generate this week's file"` | Weekly plan |
| **Friday** | `"Archive this week"` | Review + archive |

---

## Workflow

### Morning (5 min)
1. `"Good morning"`
2. Review Top 3 tasks
3. Check calendar

### During Day
- Work through Top 3
- Check off: `- [x]`
- Add notes

### Evening (3 min)
- Review completed
- Incomplete → tomorrow

---

## Folder Structure

```
work/
  daily/      ← Today's file
  weeks/      ← This week's plan
  meetings/   ← Meeting notes
  projects/   ← Active projects
reference/
  decisions/  ← Decision logs
archive/      ← Old files
system/       ← Don't touch
  automation/ ← Scripts
  templates/  ← Customize these
  memory/     ← AI context
```

---

## Customization

**Templates:** `system/templates/*.md`  
**AI Context:** `system/memory/activeContext.md`  
**Settings:** `system/automation/config.py`

---

## Troubleshooting

**No calendar?**  
→ Restart Cursor, check `~/.cursor/mcp.json`

**No files?**  
→ Check you're in right folder (`pwd`)

**Errors?**  
→ Check `system/automation/automation.log`

---

## Time Saved

**Before:** 15-20 min/day manual setup  
**After:** 30 seconds with "Good morning"

**Savings:** 65 hours/year

---

**Print this. Keep handy. You're set!**
