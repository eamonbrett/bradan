# Task Management - Quick Start

## Setup (30 min)

**1. Install**
```bash
pip install -r requirements.txt
```

**2. Configure MCP**
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
Restart Cursor!

**3. Edit Config**
Edit `automation/config.py` with your name, email, timezone.

**4. Test**
Ask Cursor: `"Generate today's daily file"`

---

## Daily Workflow

**Morning:** `"Good morning"` → Get daily file + priorities  
**During Day:** Work through Top 3 tasks  
**Evening:** Check off completed, add notes

---

## Weekly Workflow

**Monday:** `"Generate weekly summary"` + `"Generate week plan"`  
**Friday:** `"This week is over"` → Archive + review

---

## Key Commands

- `"Good morning"` - Morning setup
- `"Generate weekly summary"` - Extract meeting actions
- `"Show me my priority inbox"` - Email + Slack prioritization
- `"This week is over"` - Archive week
- `"Create decision log about X"` - Document decision

---

## Folder Structure

```
daily/       → Current week only
meetings/    → Meeting notes
decisions/   → Decision logs
archive/     → Historical files
reviews/     → Weekly/monthly reviews
automation/  → Scripts (don't touch)
memory-bank/ → AI context (customize this!)
```

---

## Customization

**Templates:** `daily/template-*.md`, `meetings/template-*.md`  
**Your Context:** `memory-bank/activeContext.md`  
**Your Workflow:** `memory-bank/systemPatterns.md`

---

## Troubleshooting

**No calendar?** Restart Cursor, check MCP config  
**No files?** Check you're in right folder (`pwd`)  
**Errors?** Check `automation/automation.log`

---

## Time Saved

**Before:** 15-20 min manual setup each morning  
**After:** 30 seconds with "Good morning"

**Savings:** ~15 min/day = 65 hours/year

---

**Print this card and keep it handy!**

