# System Patterns: Task Management Architecture

## Core Architecture
```
task-management/
├── automation/          # Automation scripts & workflows
│   ├── daily_generator.py
│   ├── weekly_archival.py          # NEW: Weekly archival system
│   ├── priority_inbox.py
│   ├── slack_notifier.py
│   └── config.py
├── daily/              # Current week only (rolling 7 days)
├── archive/            # NEW: Organized historical files
│   ├── daily/          # Archived dailies by week
│   │   ├── 2025-10-week-42/
│   │   └── 2025-11-week-44/
│   ├── projects/       # Completed projects by quarter
│   └── weekly-plans/   # Old week plans by quarter
├── context/            # NEW: Active context management
│   └── active-context.md  # Rolling 2-week window
├── reviews/            # NEW: Organized review structure
│   ├── weekly/         # All weekly reviews
│   ├── monthly/        # Monthly reviews
│   └── quarterly/      # Quarterly reviews
├── meetings/           # Meeting notes (existing)
├── projects/           # Active projects only
└── templates/          # Template system
```

## Key Design Patterns

### Template System
- **Base Template**: `daily/template-daily.md` as source of truth
- **Dynamic Substitution**: Replace placeholders with actual data
- **Date Formatting**: Consistent YYYY-MM-DD format throughout
- **Cross-reference Generation**: Auto-create meeting file references

### Calendar Integration Pattern
```python
# Calendar → Daily File Flow
Calendar Events → Filter & Format → Template Merge → File Generation
```

### File Naming Convention
- Daily files: `YYYY-MM-DD.md`
- Meeting files: `YYYY-MM-DD-meeting-name.md`
- Consistent date format across all files

### Data Flow
1. **Calendar Fetch**: Retrieve today's events via Google Workspace MCP
2. **Template Processing**: Load template and prepare substitutions
3. **Event Formatting**: Convert calendar events to markdown format
4. **File Generation**: Create daily file with populated data
5. **Cross-reference Creation**: Generate meeting file placeholders

## Integration Points

### Google Calendar API
- Use Google Workspace MCP for authentication and data access
- Filter events by time range (today's events)
- Extract: title, time, attendees, location
- Handle recurring events and exceptions

### Slack API
- Use Playground Slack MCP for Slack integration
- Send personal DM notifications to user
- Format messages with Markdown
- Triggered at key workflow points:
  - Monday morning: comprehensive weekly summary
  - Daily files: Top 3 tasks notification
  - Action reminders: personal action items
  - Friday: review reminder
  - Pre-meeting: agenda and prep items

### File System
- Check for existing daily files (avoid overwriting)
- Create meeting file stubs when needed
- Maintain consistent directory structure
- Handle file permissions and access

### Template Engine
- Simple string replacement for basic fields
- Smart formatting for calendar events
- Preserve existing task structure
- Maintain priority and tagging systems

## Error Handling Patterns
- **Calendar Access**: Graceful degradation if API unavailable
- **Slack Access**: Continue workflow if Slack MCP unavailable
- **File Conflicts**: Skip if daily file already exists
- **Template Errors**: Use fallback template if main template corrupted
- **Permission Issues**: Clear error messages for file access problems
- **Notification Failures**: Log but don't block main workflow

## Slack Notification Architecture

### Notification Flow
```
Workflow Trigger → Generate Files → Extract Data → Format Message → MCP Call → Slack DM
```

### Key Modules
- `automation/slack_notifier.py` - Core notification formatting
- `automation/slack_workflows.py` - High-level workflow integration
- `cursor_generate_daily.py` - Daily file with Slack support

### Notification Types
1. **Monday Morning Summary**
   - Weekly summary overview
   - Top 3 priorities
   - File confirmations
   - Function: `monday_morning_slack_notification()`

2. **Daily File Notification**
   - Top 3 tasks for today
   - Meeting count
   - File created confirmation
   - Function: `create_daily_notification()`

3. **Action Item Reminders**
   - Personal action items only
   - Grouped by meeting
   - Checkbox format
   - Function: `action_item_reminder()`

4. **Friday Review Reminder**
   - Time to reflect prompt
   - 3-step process
   - Motivation message
   - Function: `friday_review_reminder()`

5. **Pre-Meeting Reminders**
   - Agenda items
   - Prep checklist
   - Meeting details
   - Function: `meeting_reminder()`

### Design Principles
- All notifications are personal DMs (to "me")
- Non-blocking (failures don't stop workflow)
- Opt-in per workflow (user controls when to send)
- Rich formatting with Markdown
- Mobile-friendly (concise, scannable)

---

## Consolidated Week System (Added Nov 10, 2025) 🆕

### Purpose
Eliminate duplication between weekly plans, summaries, and reviews. Reduce weekly planning from 45 minutes to 5 minutes through smart auto-extraction.

### One File Instead of Three
**Old system (eliminated):**
- `weekly-plans/` - Manual planning (15 min)
- `weekly-summaries/` - Gemini notes (auto but duplicative)
- `reviews/weekly/` - Manual review (15 min)
- **Total:** 3 files, 90% duplication, 45+ min/week

**New system:**
- `weeks/YYYY-MM-DD-week-N.md` - One consolidated file
- 90% auto-populated from actual Cursor work
- **Total:** 1 file, 5 min/week (2 min Monday + 3 min Friday)

### Auto-Extraction Sources
**System automatically extracts from:**
1. Daily files (`daily/` and `archive/daily/`)
   - ✅ Completed tasks (checked checkboxes)
   - 🔲 Incomplete tasks (carry-forwards)
   - 🎯 Top 3 priorities worked
   - 📊 Patterns across week

2. Meeting notes (`meetings/`)
   - 💭 Decisions made
   - 📋 Action items
   - 🔗 Outcomes that matter

3. Decision logs (`decisions/`)
   - 📄 New decisions this week
   - ⚖️ Status of each

4. Calendar events
   - 📅 Meeting count
   - ⏰ Time allocation

### Monday Workflow (2 Minutes)
**Command:** "Generate this week's file"

**What happens:**
1. System extracts from last week:
   - Unfinished tasks from dailies
   - Incomplete meeting actions
   - Priority patterns
2. Generates `weeks/2025-11-10-week-46.md`
3. Pre-populates carry-forwards and priorities

**You do:**
- Scan carry-forwards (1 min)
- Adjust Top 3 priorities (1 min)
- Done!

### Friday Workflow (3 Minutes)
**Command:** "Update this week's file"

**What happens:**
1. System extracts from this week:
   - All completed tasks
   - Meeting decisions/actions
   - Decision logs created
   - Time reality check
2. Updates `weeks/2025-11-10-week-46.md`

**You do:**
- Answer 3 reflection questions (3 min):
  1. What went well?
  2. What to change?
  3. Key learning?
- Done!

### Key Files
1. **`automation/week_extractor.py`** - Extract data from daily work
2. **`automation/week_generator.py`** - Generate consolidated files
3. **`automation/CURSOR_CONSOLIDATED_WEEK_WORKFLOW.md`** - Complete guide
4. **`weeks/YYYY-MM-DD-week-N.md`** - Consolidated weekly files

### Time Savings
- **Before:** 45 min/week (plan + summary + review)
- **After:** 5 min/week (2 min Monday + 3 min Friday)
- **Savings:** 40 min/week = 35 hours/year

### What Was Deleted
- ❌ `reviews/template-weekly-review.md` (old bureaucratic 303-line template)
- ❌ `daily/template-daily.md` (old v1 template)
- ❌ Old weekly review standalone files

### What's Deprecated
- `weekly-plans/` - Keep for reference, don't create new
- `reviews/weekly/` - Keep for reference, use `weeks/` going forward
- `weekly-summaries/` - Gemini notes still generated, data auto-extracted

### Integration
- Daily files unchanged - continue checking off tasks
- Meeting notes unchanged - continue documenting
- Decision logs unchanged - continue creating
- System extracts automatically

---

## Weekly Archival System (Added Nov 5, 2025)

### Purpose
Maintain clean workspace by archiving old daily files while preserving context in organized structure.

### Archival Pattern
```
Friday Workflow:
1. Extract highlights from week's daily files
2. Generate enhanced weekly review with daily highlights
3. Move daily files to archive/daily/YYYY-MM-week-WW/
4. Update active context window (rolling 2 weeks)
5. Clean daily/ folder (keep only current week)
```

### Three-Tier Context System

**Tier 1: Active (Always Visible)**
- Current week daily files (7 days max in `daily/`)
- Active context window (`context/active-context.md`)
- In-progress projects
- Current week plan

**Tier 2: Recent (Quick Access)**
- Last 4 weekly reviews (`reviews/weekly/`)
- Last month's review (`reviews/monthly/`)
- Recent decision logs (last 30 days)

**Tier 3: Archive (Searchable)**
- Historical dailies organized by week (`archive/daily/YYYY-MM-week-WW/`)
- All weekly reviews chronologically
- Completed projects by quarter
- Monthly/quarterly reviews

### Active Context Window Pattern

**Purpose:** Rolling 2-week visibility without clutter

**Structure:**
```markdown
## Current Week (Nov 4-8)
- Top 3 priorities in flight
- Active meetings and decisions
- Key stakeholder conversations

## Previous Week (Oct 28-Nov 1)
- Completed priorities
- Decisions made
- Carry-forward items

## Strategic Thread (Last 4 weeks)
- Major initiatives and their evolution
- Patterns across weeks
```

**Update Frequency:**
- Automatic: Every Friday during archival
- Manual: Mid-week for important context

### Enhanced Weekly Review Pattern

**Auto-Populated Sections:**
- Daily highlights from each day's file
- Top 3 priorities per day
- Meeting summaries
- Key updates
- Links to archived daily files

**User Completes:**
- Priority completion status
- Strategic alignment check
- Wins and challenges
- Key insights
- Metrics and next week preview

**Time Investment:** 15-20 minutes focused reflection

### File Organization Best Practices

**Keep Visible (Root Level):**
- Current week dailies only (≤7 files)
- Active projects (in-progress only)
- Current week plan
- Last 2 weekly reviews
- Active context window

**Archive Immediately:**
- Daily files older than 7 days → `archive/daily/[WEEK_ID]/`
- Weekly reviews older than 2 weeks → `reviews/weekly/`
- Completed projects → `archive/projects/[QUARTER]/`
- Old weekly plans → `archive/weekly-plans/[QUARTER]/`

**Never Archive:**
- Decision logs (permanent, always searchable)
- Memory bank files
- Strategic alignment docs
- Templates

### Weekly Archival Workflow Script

**File:** `automation/weekly_archival.py`

**Core Functions:**
1. `find_daily_files_for_week()` - Locate week's dailies
2. `extract_daily_highlights()` - Pull key info from each daily
3. `archive_week()` - Move files to organized archive
4. `generate_enhanced_weekly_review()` - Create review with highlights
5. `update_active_context()` - Refresh 2-week window

**Command Interface:**
```python
archive_week_command(
    week_start_str="2025-10-28",  # Monday
    dry_run=False,
    weekly_summary_path="..."
)
```

**Returns:**
- Archive location
- Files archived count
- Review file path
- Extracted highlights
- Updated context path

### Integration with Existing Workflows

**Monday Morning Enhanced:**
```
1. "Show me active context"          # Quick catch-up
2. "Generate weekly summary"         # From meetings
3. "Generate week plan"              # With context
4. "Generate daily file"             # Start week
```

**Friday Afternoon Complete:**
```
1. "Generate end-of-week archival"   # Archive + review
2. Complete weekly review sections   # Reflection
3. "Send Friday summary to Slack"    # Optional
```

**Monthly/Quarterly:**
- Monthly: Synthesize 4 weekly reviews
- Quarterly: Synthesize 3 monthly reviews
- Update memory bank with major patterns

### Search & Discovery Pattern

**Find Past Work:**
- `"What did I work on in October?"` → Search monthly review + weeklies
- `"When did we decide about X?"` → Search decision logs + reviews
- `"Show me week of Oct 28"` → Navigate to archive

**Navigation:**
- All archived dailies linked from weekly reviews
- Weekly reviews organized chronologically
- Decision logs never move (permanent reference)

### Scalability Pattern

**After 1 Month:**
- ~4-5 archived weeks
- 1 monthly review
- Clean daily/ folder

**After 1 Quarter:**
- ~13 archived weeks
- 3 monthly reviews
- 1 quarterly review
- Archive old projects to `archive/projects/YYYY-QX/`

**After 1 Year:**
- ~52 archived weeks (organized by week number)
- 12 monthly reviews
- 4 quarterly reviews
- Complete searchable history

### Error Handling Patterns

**No Daily Files:**
- Normal if week off or already archived
- Check archive directory first

**Partial Week:**
- Confirm before archiving incomplete week
- Usually run on Fridays only

**Already Archived:**
- Check for existing archive directory
- Confirm before re-archiving

### Success Criteria

Post-archival state:
- ✅ Daily folder has ≤7 files
- ✅ Week's dailies in `archive/daily/[WEEK_ID]/`
- ✅ Enhanced review in `reviews/weekly/`
- ✅ Daily highlights auto-populated
- ✅ Active context shows current + previous week
- ✅ All links functional
- ✅ User has clear review completion task

**Maintenance:**
- Weekly archival prevents accumulation
- Monthly reviews synthesize insights
- Quarterly reviews inform strategic planning
- Memory bank captures major patterns

