# Task Management System

**AI-Powered Task Management with Cursor IDE**

A comprehensive task management system that uses Claude in Cursor to automate daily planning, meeting notes, weekly reviews, and more. Say goodbye to manual todo lists and hello to AI-assisted productivity.

---

## 🚀 Quick Start

**Setup Time:** 30 minutes  
**Daily Time Investment:** 5 minutes  
**Time Saved:** ~65 hours/year

### Prerequisites
- **Cursor IDE** (cursor.com) - Required for AI integration
- **Python 3.8+** - For automation scripts
- **Google Workspace** - For calendar integration
- **30 minutes** - For initial setup

### Installation

1. **Use this template** (if on GitHub) or clone this repo
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure MCP** - Follow `SETUP_GUIDE.md` (15 min)
4. **Test it:**
   ```bash
   # In Cursor, ask Claude:
   "Generate today's daily file"
   ```

**Success!** You should see a daily file with your calendar events.

---

## 📖 Documentation

**Start Here:**
1. **`HOW-I-USE-THIS.md`** - Read this first! Real-world walkthrough
2. **`SETUP_GUIDE.md`** - Complete 30-minute setup
3. **`sharing-template-quickstart.md`** - One-page reference card

**Additional Guides:**
- **`BACKUP_STRATEGY.md`** - Don't lose your work
- **`EXPORT-CHECKLIST.md`** - How to share this system
- **`README-EXPORT-SUMMARY.md`** - Complete export guide

---

## ✨ What This System Does

### Daily Automation
- **"Good morning"** → Generates daily file with calendar, priorities, meeting stubs
- **Calendar integration** → Real Google Calendar events auto-populate
- **Meeting notes** → Pre-filled templates with attendees and links
- **Priority inbox** → Email + Slack aggregated and prioritized

### Weekly Planning
- **Monday:** Generate weekly plan from last week's work
- **Friday:** Auto-extract accomplishments, archive files
- **Weekly reviews** → Takes 5 minutes instead of 45

### Smart Features
- **Decision logging** → Never debate the same thing twice
- **Carry-forwards** → Incomplete tasks auto-appear next day
- **Archive system** → Clean workspace, searchable history
- **Slack integration** → Optional notifications (mobile-friendly)

---

## 📂 Folder Structure

```
task-management/
├── work/              # Active work (what you touch daily)
│   ├── daily/         # Daily files (current week only)
│   ├── weeks/         # Weekly files
│   ├── meetings/      # Meeting notes
│   └── projects/      # Active projects
├── reference/         # Reference materials (look up as needed)
│   ├── decisions/     # Decision logs (never archived)
│   ├── career/        # Career development
│   └── docs/          # Documentation
├── archive/           # Historical files (searchable)
├── system/            # System files (automation & config)
│   ├── automation/    # Python scripts
│   ├── memory/        # AI memory bank
│   └── templates/     # File templates
└── inbox/             # Temporary (auto-generated, auto-cleared)
```

---

## 🎯 Daily Workflow

### Morning (5 minutes)
```
Say to Claude in Cursor: "Good morning"
```

This automatically:
1. Fetches your calendar
2. Checks recent email/Slack
3. Generates daily file with Top 3 tasks
4. Creates meeting stubs
5. Shows priority inbox

### During Day
- Work through your Top 3 tasks
- Check off completed items: `- [x]`
- Add notes as you go

### Evening (3 minutes)
- Quick review of what got done
- Incomplete items carry forward tomorrow

---

## 📅 Weekly Workflow

### Monday (2 minutes)
```
"Generate this week's file"
```
- Review carry-forwards from last week
- Set Top 3 priorities for the week

### Friday (3 minutes)
```
"Archive this week"
```
- Auto-extracts accomplishments
- Answer 3 reflection questions
- Archives daily files

**Total weekly planning time: 5 minutes**

---

## 💡 Key Commands

| When | Say | What Happens |
|------|-----|--------------|
| **Every morning** | "Good morning" | Full morning setup |
| **Monday** | "Generate this week's file" | Weekly planning |
| **Friday** | "Archive this week" | Weekly review + archive |
| **Any time** | "Show me my priority inbox" | Email + Slack priorities |
| **After decision** | "Create decision log about X" | Document decision |

---

## 🎁 What You Get

### Immediate Benefits
- ✅ **15 min/day saved** on manual planning
- ✅ **Automated carry-forwards** - Nothing falls through cracks
- ✅ **Pre-filled meeting notes** - Attendees, links, context ready
- ✅ **Priority inbox** - See what matters, ignore noise
- ✅ **Decision history** - Stop debating settled issues

### Time Savings
- **Daily:** 15 minutes saved
- **Weekly:** 30 minutes saved
- **Yearly:** ~65 hours back

### Quality Improvements
- Better focus (Top 3 clarity)
- Complete context (searchable history)
- Fewer missed tasks (auto carry-forward)
- Better decisions (documented rationale)

---

## 🔧 Customization

### Templates
Edit files in `system/templates/`:
- `daily.md` - Daily file format
- `meeting-v2.md` - Meeting notes format
- `weekly.md` - Weekly planning format
- `decision.md` - Decision log format

### Memory Bank
Customize `system/memory/` for your context:
- `activeContext.md` - Current focus areas
- `projectbrief.md` - Your project goals
- `systemPatterns.md` - Your workflow patterns

### Automation
Adjust `system/automation/config.py`:
- Timezone settings
- File paths
- Calendar preferences

---

## 🤝 Contributing & Sharing

### Personal Use
- Set up on multiple computers
- Customize templates freely
- Adjust workflows to your style

### Sharing with Others
- Use "Template repository" feature on GitHub
- Recipients get clean copy
- See `EXPORT-CHECKLIST.md` for details

### Backup
- Use private GitHub repo (recommended)
- Or Google Drive Desktop
- See `BACKUP_STRATEGY.md`

---

## 🆘 Troubleshooting

### Calendar not showing
1. Restart Cursor
2. Check `~/.cursor/mcp.json` configuration
3. Test: Ask "Can you check my calendar?"

### Files not generating
1. Verify you're in correct folder: `pwd`
2. Check templates exist: `ls system/templates/`
3. Check Python: `python --version` (needs 3.8+)

### MCP errors
- Restart Cursor (MCP servers load on startup)
- Verify `~/.cursor/mcp.json` syntax
- See `SETUP_GUIDE.md` for configuration

---

## 📊 System Requirements

**Minimum:**
- Cursor IDE (free trial available)
- Python 3.8+
- Google Workspace account
- 30 minutes setup time

**Recommended:**
- macOS, Linux, or Windows
- Slack workspace (optional)
- GitHub account (for backup)

---

## 🎓 Learning Curve

**Day 1:** Follow commands exactly (feels clunky)  
**Week 1:** Start to trust the morning routine  
**Week 2:** Notice you're not losing track of things  
**Week 3:** Customize templates to your style  
**Month 1:** Can't imagine going back

---

## 📝 What Makes This Different

### vs. Todo Apps (Todoist, Things)
- No context switching (already in your IDE)
- Files are searchable, portable, version-controlled
- AI understands context ("that meeting with Sarah")

### vs. Notion/Obsidian
- No manual organizing (AI handles structure)
- No plugin management or sync issues
- Calendar integration is automatic

### vs. Paper/Notebooks
- Searchable across all history
- Automatic carry-forwards
- Can't lose it
- Works across computers

---

## 🔐 Privacy & Security

- **All files local** - Nothing syncs to third-party (except via MCP to Google/Slack you control)
- **No cloud storage** - Unless you choose GitHub/Drive backup
- **Your data** - You own everything, no vendor lock-in
- **Open source** - Inspect and modify all code

---

## 🚀 Get Started

1. **Clone or use this template**
2. **Read `HOW-I-USE-THIS.md`** (10 min) - See how it actually works
3. **Follow `SETUP_GUIDE.md`** (30 min) - Complete setup
4. **Tomorrow morning:** Say "Good morning" to Claude
5. **Report back in a week!**

---

## 📬 Questions?

- **Setup issues?** See `SETUP_GUIDE.md` troubleshooting section
- **Customization?** Check `system/templates/` and `system/memory/`
- **Export/sharing?** See `EXPORT-CHECKLIST.md`

---

## 🙏 Acknowledgments

Built with:
- **Cursor IDE** - AI-powered development
- **Claude (Anthropic)** - AI assistant
- **Google Workspace MCP** - Calendar integration
- **Model Context Protocol** - AI tool integration

---

**Ready to transform your productivity?**

**Start here:** `HOW-I-USE-THIS.md`

---

*Last Updated: January 2026*  
*Version: 1.0 (Export Package)*
