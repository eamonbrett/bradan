# Bradán

**AI-powered daily assistant**

Task management system using Claude in Cursor IDE. Automate daily planning, meeting notes, and weekly reviews.

> *Bradán* (Irish: "salmon") - Like the legendary Salmon of Knowledge, Bradán brings instant clarity to your workday.

## Quick Start

**Setup:** 30 minutes | **Daily use:** 5 minutes | **Time saved:** ~65 hours/year

### Prerequisites
- [Cursor IDE](https://cursor.com) - Required
- Python 3.8+
- Google Workspace account (Calendar, Gmail, Drive)

### Optional Enhancements
- **Gemini** (Google Workspace add-on) - Automated meeting transcription
- **Slack MCP** - For Slack message prioritization (requires custom setup)

### Install

```bash
pip install -r requirements.txt
```

See [SETUP.md](SETUP.md) for complete installation.

### Try It

After setup, ask Claude in Cursor:
```
"Good morning"
```

You'll get a daily file with your calendar, priorities, and meeting notes - automatically.

---

## What This Does

### Daily Automation
- **"Good morning"** → Generates daily file with calendar and priorities
- **Calendar integration** → Real Google Calendar events auto-populate
- **Gmail integration** → Email reading and prioritization included
- **Meeting stubs** → Pre-filled with attendees and links
- **Gemini meeting notes** → Optional: Auto-import transcriptions from Google Meet
- **Priority inbox** → Email aggregation (Slack requires additional setup)

### Weekly Planning
- **Monday:** Auto-generate weekly plan from last week
- **Friday:** Auto-extract accomplishments, archive old files
- **5 minutes** instead of 45 minutes per week

### Smart Features
- **Decision logging** → Never debate the same thing twice
- **Carry-forwards** → Incomplete tasks appear next day
- **Archive system** → Clean workspace, searchable history
- **Slack integration** → Optional mobile notifications

---

## Key Commands

| Say to Claude | What Happens |
|---------------|--------------|
| "Good morning" | Full morning setup |
| "Generate this week's file" | Weekly planning |
| "Archive this week" | Weekly review + archive |
| "Show me my priority inbox" | Email + Slack priorities |
| "Create decision log about X" | Document decision |

---

## Folder Structure

```
task-management/
├── work/              # Active work
│   ├── daily/         # Daily files
│   ├── weeks/         # Weekly plans
│   ├── meetings/      # Meeting notes
│   └── projects/      # Projects
├── reference/         # Reference materials
│   └── decisions/     # Decision logs
├── archive/           # Historical files
├── system/            # System files
│   ├── automation/    # Python scripts
│   ├── memory/        # AI context
│   └── templates/     # Templates
└── inbox/             # Temporary files
```

---

## Daily Workflow

### Morning (5 min)
```
"Good morning"
```
→ Calendar fetched, daily file created, meeting stubs generated

### During Day
- Work through Top 3 tasks
- Check off completed: `- [x]`
- Add notes as you go

### Evening (3 min)
- Quick review
- Incomplete items carry forward tomorrow

---

## Weekly Workflow

### Monday (2 min)
```
"Generate this week's file"
```

### Friday (3 min)
```
"Archive this week"
```

**Total:** 5 minutes of planning per week

---

## Customization

### Templates
Edit `system/templates/`:
- `daily.md` - Daily file format
- `meeting-v2.md` - Meeting notes
- `weekly.md` - Weekly planning
- `decision.md` - Decision logs

### Memory Bank
Customize `system/memory/` for your context:
- `activeContext.md` - Current focus
- `projectbrief.md` - Your goals
- `systemPatterns.md` - Your workflow

### Settings
Adjust `system/automation/config.py`:
- Timezone
- File paths
- Calendar preferences

---

## Why This Works

### vs Todo Apps
- No context switching (already in IDE)
- Files are portable and version-controlled
- AI understands context

### vs Notion/Obsidian
- No manual organizing (AI handles it)
- No plugins or sync issues
- Calendar integration automatic

### vs Paper
- Searchable history
- Automatic carry-forwards
- Multi-computer sync

---

## What You Get

**Time Savings:**
- 15 min/day on planning
- 30 min/week on reviews
- ~65 hours/year total

**Quality Improvements:**
- Better focus (Top 3 clarity)
- Complete context (searchable)
- Fewer missed tasks
- Better decisions (documented)

---

## Documentation

- **[SETUP.md](SETUP.md)** - Complete 30-minute setup guide
- **[QUICK_START.md](QUICK_START.md)** - One-page reference

---

## Tech Stack

- **Cursor IDE** - AI-powered development
- **Claude (Anthropic)** - AI assistant
- **Google Workspace MCP** - Calendar integration
- **Python 3.8+** - Automation scripts
- **Markdown** - File format

---

## License

Use freely for personal or team productivity.

---

**Ready to start?** → [SETUP.md](SETUP.md)
