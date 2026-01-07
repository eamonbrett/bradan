# Active Context: Current Work Focus

## Current Status
**Date:** [Current Date]  
**Status:** System ready for use

---

## 🎯 This Week's Focus

### Current Priorities
[User customizes this section with their weekly priorities]

1. **Priority 1** - [Description]
2. **Priority 2** - [Description]
3. **Priority 3** - [Description]

### Key Milestones
[User tracks important dates and milestones]

---

## 📊 Active Projects

[User maintains list of active projects here]

### Project 1: [Name]
- **Status:** [In Progress / Blocked / Complete]
- **Next Actions:** [List key next steps]
- **Key Stakeholders:** [Names]

### Project 2: [Name]
- **Status:** [In Progress / Blocked / Complete]
- **Next Actions:** [List key next steps]
- **Key Stakeholders:** [Names]

---

## ☀️ "Good Morning" Automation (KEY COMMAND)

### IMPORTANT: "Good morning" is an AUTOMATION COMMAND, not a greeting

When you say "Good morning", the system executes immediately:

**What It Does:**
1. Fetch today's calendar events
2. Check email for last 24h
3. Check Slack messages for last 24h
4. Generate priority inbox file
5. Update/create daily file with all context
6. Create meeting stubs for each meeting
7. Generate Top 3 prioritized tasks
8. Report summary

**Output Files:**
- `work/daily/YYYY-MM-DD.md` - Daily file
- `inbox/priority-inbox-YYYY-MM-DD.md` - Priority inbox
- `work/meetings/YYYY-MM-DD-[meeting-name].md` - Meeting stubs

**Time Saved:** ~15 minutes daily (65 hours/year)

**Reference:** `system/automation/CURSOR_GOOD_MORNING_WORKFLOW.md`

---

## 🎯 Priority Inbox Workflow

### One-Screen Prioritized Communication Summary

**Command:** `"Show me my priority inbox"` or `"What's on deck for me?"`

**Priority Levels:**
- 🔴 **P1**: Urgent & High Impact - Do immediately
- 🟠 **P2**: High Priority - Schedule for today
- 🟡 **P3**: Medium Priority - Plan for this week
- 🟢 **P4**: Low Priority - Review later

**Integration with Daily Files:**
- View priority inbox
- Add P1 items to daily Top 3 tasks
- Schedule P2/P3 items appropriately

---

## 📝 Decision Log System

### Automated Decision Documentation

**Commands:**
- `"Create decision log"` - General decision documentation
- `"Document decision about [topic]"` - Specific topic
- `"Create decision log from yesterday's meeting"` - From meeting

**Template Sections:**
- Context: Problem, background, stakeholders
- The Decision: What was decided
- Rationale: Why this vs alternatives
- Implementation: Action items, timeline
- Success Criteria: How we'll know it worked

**File Location:** `reference/decisions/`

---

## 📦 Weekly Archival System

### Automated File Organization

**Purpose:** Keep workspace clean by archiving old daily files

**Commands:**
- `"Generate end-of-week archival"` - Friday workflow
- `"Archive this week and create weekly review"` - Full process
- `"Archive week of [date]"` - Specific week

**What It Does:**
1. Extract highlights from daily files
2. Generate enhanced weekly review
3. Move daily files to archive
4. Update active context
5. Clean daily/ folder

**File Structure:**
```
work/daily/           # Current week only
archive/daily/        # Organized by week
  └── YYYY-MM-week-WW/
reviews/weekly/       # Weekly reviews
```

---

## 🆕 Integrated System Workflows

### Weekly Rhythm

**Monday Morning (15 min):**
1. "Generate weekly summary"
2. "Generate week plan"
3. "Generate daily file"

**Daily (10 min):**
- Morning: "Good morning"
- Review Top 3 tasks
- Evening: Check off completed, note insights

**Friday (20 min):**
1. "Generate end-of-week archival"
2. Complete reflection sections
3. Update active projects

---

## 📚 MCP Integration

### Real MCP Integration

**Configured MCP Servers:**
- **gworkspace-mcp**: Google Calendar, Gmail, Drive
- **slack-mcp**: Slack (optional - requires custom setup)

**What This Enables:**
- ✅ Actual meetings from Google Calendar
- ✅ Attendee lists with emails
- ✅ Google Meet links
- ✅ Event descriptions and locations
- ✅ Timezone aware
- ✅ Optional Slack notifications

---

## 📁 Key Documentation

### Automation Workflow Files
Location: `system/automation/`

| File | Purpose | Command |
|------|---------|---------|
| `CURSOR_GOOD_MORNING_WORKFLOW.md` | Morning setup | "Good morning" |
| `CURSOR_WEEKLY_ARCHIVAL_WORKFLOW.md` | Friday archival | "This week is over" |
| `CURSOR_PRIORITY_INBOX_WORKFLOW.md` | Priority inbox | "Show me my priority inbox" |
| `CURSOR_DECISION_LOG_WORKFLOW.md` | Decision docs | "Create decision log" |

### User-Facing Guides
| File | Purpose |
|------|---------|
| `README.md` | System overview |
| `QUICK_START.md` | Quick reference |

---

## 🔗 Quick Links

- **This Week:** [[work/weeks/YYYY-MM-DD-week-WW.md]]
- **Today:** [[work/daily/YYYY-MM-DD.md]]
- **Active Projects:** [[work/projects/ACTIVE_PROJECTS.md]]
- **Priority Inbox:** [[inbox/priority-inbox-YYYY-MM-DD.md]]

---

## 📝 Recent Changes

[User tracks recent system changes or customizations]

---

**Last Updated:** [Date]  
**Status:** [Current status]  
**Current Week:** [Week number]
