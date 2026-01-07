# Cursor Workflow: Weekly Archival System

**Purpose:** Complete end-of-week workflow to archive daily files, generate enhanced weekly reviews, and maintain active context window.

**When to Use:** Every Friday afternoon as part of weekly review process

**User Commands:**
- `"This week is over"` (simplest)
- `"Generate end-of-week archival"` (formal)
- `"Archive week of [date]"` (for specific weeks)

---

## Complete Friday Workflow

This workflow combines archival with weekly review to maintain a clean, organized workspace.

### Step-by-Step Process

#### 1. Identify Week to Archive

**Determine week start date (Monday):**
```python
from datetime import datetime, timedelta

# If today is Friday, archive this week
today = datetime.now()
# Find the Monday of this week
week_start = today - timedelta(days=today.weekday())
week_start_str = week_start.strftime("%Y-%m-%d")
```

**Or use user-provided date:**
- User says: "Archive week of October 28"
- Parse date and find Monday of that week

#### 2. Call Weekly Archival Script

**Using Python execution from Cursor:**

```python
import sys
sys.path.append('/Users/eamonbrett/Documents/task-management/automation')
from weekly_archival import archive_week_command

# Archive the week
result = archive_week_command(
    week_start_str="2025-10-28",  # Monday of week to archive
    dry_run=False,  # Set to True for preview
    weekly_summary_path="weekly-summaries/weekly-summary-2025-10-28.md"  # Optional
)

print(result)
```

**Expected Output:**
```json
{
  "success": true,
  "week_id": "2025-10-week-44",
  "week_start": "2025-10-28",
  "week_end": "2025-11-03",
  "files_archived": 5,
  "archived_files": [
    "archive/daily/2025-10-week-44/2025-10-28.md",
    "archive/daily/2025-10-week-44/2025-10-29.md",
    "archive/daily/2025-10-week-44/2025-10-30.md",
    "archive/daily/2025-10-week-44/2025-11-03.md"
  ],
  "archive_location": "archive/daily/2025-10-week-44",
  "review_file": "reviews/weekly/2025-10-28-week-44.md",
  "context_updated": "context/active-context.md",
  "highlights": [
    {
      "date": "2025-10-28",
      "day_name": "Monday",
      "top_3": ["Andre Prep", "Launch Cases", "GTM Craft"],
      "meetings": [...],
      "key_updates": [...]
    },
    ...
  ]
}
```

#### 3. Review Generated Files

**Show user what was created:**

1. **Enhanced Weekly Review** - `reviews/weekly/[DATE]-week-[WW].md`
   - Contains daily highlights from archived files
   - Auto-populated with meetings, priorities, key updates
   - Ready for user to complete reflection sections

2. **Archived Dailies** - `archive/daily/[WEEK_ID]/`
   - All daily files moved to organized week folder
   - Still accessible via links in weekly review
   - Clean daily/ folder with only current week

3. **Updated Active Context** - `context/active-context.md`
   - Current week section updated with this week's priorities
   - Previous week section moved to archive reference
   - Strategic threads maintained across weeks

#### 4. Complete Weekly Review

**Guide user through review completion:**

```
✅ Archival complete! Your weekly review is ready at:
reviews/weekly/[DATE]-week-[WW].md

The daily highlights section has been auto-populated from your daily files.

Please complete the following sections:
- [ ] Week Completion Check (mark priority status)
- [ ] Strategic Alignment Check (how did this advance your mandate?)
- [ ] Wins & Achievements (what went well?)
- [ ] Challenges & Learnings (what was difficult?)
- [ ] Key Insights (what did you learn?)
- [ ] Decisions Made This Week (link to decision logs)
- [ ] Metrics & Data (time allocation, energy levels)
- [ ] Next Week Preview (priorities and prep needed)

Estimated time: 15-20 minutes
```

#### 5. Optional: Send Weekly Summary to Slack

**If user wants Slack notification:**

```python
# After review is complete, send summary to Slack
from automation.slack_notifier import SlackNotifier

notifier = SlackNotifier()
message = notifier.friday_review_reminder()

# Or send custom weekly summary
message = f"""
📊 Week of {week_start_str} - Complete!

**Archived:** {result['files_archived']} daily files
**Review:** reviews/weekly/{week_start_str}-week-{week_number:02d}.md

Take 20 minutes to complete your weekly review and reflect on the week.
"""

# Send to Slack (using MCP)
# Claude calls: mcp_playground-slack-mcp_slack_send_message
```

---

## Detailed Implementation Guide

### Data Flow

```
1. User triggers workflow
   ↓
2. Claude identifies week to archive (Monday-Friday)
   ↓
3. Python script executes:
   a. Find all daily files for that week
   b. Extract highlights from each daily
   c. Move daily files to archive/daily/[WEEK_ID]/
   d. Generate enhanced weekly review with daily highlights
   e. Update active context window
   ↓
4. Claude presents results to user
   ↓
5. User completes weekly review reflection sections
   ↓
6. Optional: Send summary to Slack
```

### Key Functions in weekly_archival.py

#### `archive_week_command(week_start_str, dry_run, weekly_summary_path)`

Main entry point for archival workflow.

**Parameters:**
- `week_start_str`: Monday date in "YYYY-MM-DD" format
- `dry_run`: Boolean - if True, preview without moving files
- `weekly_summary_path`: Optional path to weekly summary for action items

**Returns:**
- Dict with archival results and file paths

#### `WeeklyArchival.extract_daily_highlights(daily_file)`

Extracts key information from a daily file.

**Extracts:**
- Top 3 priorities (from ## Top 3 Priorities section)
- Meetings (from Calendar Overview section)
- Key updates (from ## Key Updates section)
- Follow-up items (from ## Follow-Up Items section)

**Returns:**
- Dict with structured highlights

#### `WeeklyArchival.generate_daily_highlights_section(week_highlights)`

Generates markdown for daily highlights section in weekly review.

**Creates:**
- One section per day of the week
- Priorities, meetings, updates for each day
- Links to archived daily files

#### `WeeklyArchival.update_active_context(week_highlights, week_start)`

Updates the rolling 2-week active context window.

**Updates:**
- Current week → Previous week
- New highlights → Current week
- Maintains strategic threads

---

## Error Handling

### No Daily Files Found

```python
if result['success'] == False and 'No daily files found' in result['message']:
    # Week has no daily files - nothing to archive
    print(f"No daily files found for week starting {week_start_str}")
    print("This is normal if you didn't work that week or files are already archived.")
```

### Files Already Archived

```python
# Check if archive directory already exists
archive_dir = f"archive/daily/{week_id}"
if os.path.exists(archive_dir):
    print(f"⚠️ Week {week_id} appears to already be archived at {archive_dir}")
    print("Do you want to re-archive? (This will overwrite)")
    # Wait for user confirmation
```

### Partial Week

```python
# If archiving current week mid-week
if week_start <= datetime.now() < week_end:
    print(f"⚠️ This week is not complete yet (today is {datetime.now().strftime('%A')})")
    print(f"Found {len(daily_files)} daily files to archive.")
    print("Proceed with partial week archive? Usually done on Fridays.")
    # Wait for user confirmation
```

---

## Best Practices

### Timing

**Recommended: Friday afternoon (3-5 PM)**
- Week is complete (Monday-Friday)
- Fresh context for weekly review
- Mental closure on the week
- Preview next week before weekend

**Alternative: Monday morning**
- Review last week before planning this week
- Use insights to inform this week's priorities
- Requires discipline to complete review from previous week

### Dry Run First

**For new users or important weeks:**
```python
# Preview what will happen
result = archive_week_command(week_start_str, dry_run=True)

# Show user the preview
print(f"Would archive {result['files_archived']} files:")
for file in result['archived_files']:
    print(f"  - {file}")

# Then execute if confirmed
result = archive_week_command(week_start_str, dry_run=False)
```

### Weekly Review Quality

**Auto-populated sections:**
- ✅ Daily highlights (from daily files)
- ✅ Archive references (links to daily files)
- ✅ Template structure

**User completes:**
- Priority completion status
- Strategic alignment check
- Wins and achievements
- Challenges and learnings
- Key insights about effectiveness
- Metrics and data (time allocation, energy)
- Next week preview and intentions

**Time investment:** 15-20 minutes of focused reflection

### Active Context Maintenance

**The active context file should always show:**
- Current week (in progress)
- Previous week (just archived)
- Strategic threads (last 4 weeks)

**Updates automatically:**
- Every Friday during archival
- Current week → Previous week
- New week starts fresh Monday

**Manual updates:**
- Mid-week priority changes
- Important insights or patterns
- Stakeholder dynamic shifts

---

## Integration with Other Workflows

### Monday Morning Workflow

```
1. "Generate weekly summary" (from Gemini meeting notes)
2. "Show me active context" (review last 2 weeks)
3. "Generate week plan" (with context from weekly summary + active context)
4. "Generate daily file"
```

**Active context provides:**
- Carry-forward items from last week
- Strategic threads to maintain
- Stakeholder dynamics to monitor

### Monthly Review Workflow

```
1. Archive all weeks of the month (4 weeks)
2. Read all 4 weekly reviews
3. Generate monthly review (synthesize insights)
4. Update strategic alignment docs
```

**Monthly review uses:**
- All 4 weekly reviews for the month
- Decision logs from the month
- Active context for current state

### Quarterly Review Workflow

```
1. Complete all monthly reviews for quarter (3 months)
2. Read all 3 monthly reviews
3. Generate quarterly review (strategic reflection)
4. Update memory bank with major patterns
5. Plan next quarter priorities
```

---

## Troubleshooting

### Issue: Daily files not found

**Check:**
- Are daily files in `daily/` directory?
- Is the date format correct? (YYYY-MM-DD.md)
- Have files already been archived?

**Solution:**
```bash
ls -la daily/2025-10-*.md
# Check what files exist

ls -la archive/daily/
# Check if already archived
```

### Issue: Archive directory already exists

**Check:**
```bash
ls -la archive/daily/2025-10-week-44/
# See what's already there
```

**Solution:**
- If re-archiving, manually delete old archive first
- Or modify script to append/merge instead of replace

### Issue: Weekly review not generated

**Check:**
- Does `reviews/template-weekly-review.md` exist?
- Is `reviews/weekly/` directory created?
- Check script output for errors

**Solution:**
```python
# Check if template exists
template_path = "reviews/template-weekly-review-enhanced.md"
if not os.path.exists(template_path):
    print(f"Template not found at {template_path}")
    print("Using simplified template")
```

### Issue: Active context not updating

**Check:**
- Does `context/active-context.md` exist?
- Is file writable?

**Solution:**
```bash
# Check file permissions
ls -la context/active-context.md

# If doesn't exist, create it
mkdir -p context
touch context/active-context.md
```

---

## Command Reference

### Archive Current Week

```
User: "This week is over"
or
User: "Archive this week"

Claude:
1. Figure out this week's Monday
2. Call archive_week_command(week_start_str, dry_run=False)
3. Show results
4. User fills in the review
```

### Archive Specific Week

```
User: "Archive week of October 28"

Claude:
1. Parse "October 28" → "2025-10-28"
2. Find Monday of that week
3. Call archive_week_command(week_start_str, dry_run=False)
4. Present results
```

### Preview Archive (Dry Run)

```
User: "Show me what would be archived this week"

Claude:
1. Call archive_week_command(week_start_str, dry_run=True)
2. Show list of files that would be moved
3. Show where they would go
4. Ask if user wants to proceed
```

### Complete End-of-Week Workflow

```
User: "Generate end-of-week archival"

Claude:
1. Archive this week's dailies
2. Generate enhanced weekly review
3. Update active context
4. Open weekly review
5. Optional: Send Slack summary
```

---

## File Organization After Archival

### Before

```
daily/
├── 2025-10-14.md
├── 2025-10-15.md
├── 2025-10-16.md
├── ... (20+ files)
├── 2025-11-03.md
├── 2025-11-04.md
└── 2025-11-05.md
```

### After

```
daily/
├── 2025-11-04.md       # Current week only
├── 2025-11-05.md
└── template-daily-v2.md

archive/
└── daily/
    ├── 2025-10-week-42/
    │   ├── 2025-10-14.md
    │   ├── 2025-10-15.md
    │   └── 2025-10-16.md
    └── 2025-10-week-44/
        ├── 2025-10-28.md
        ├── 2025-10-29.md
        └── 2025-10-30.md

reviews/
└── weekly/
    ├── 2025-10-14-week-42.md
    ├── 2025-10-21-week-43.md
    └── 2025-10-28-week-44.md

context/
└── active-context.md  # Updated with current + previous week
```

**Result:** Clean workspace with only current week visible, all historical context preserved and organized.

---

## Success Criteria

After running weekly archival workflow:

- ✅ Daily folder contains only current week (7 days or less)
- ✅ Previous week's dailies in `archive/daily/[WEEK_ID]/`
- ✅ Enhanced weekly review created in `reviews/weekly/`
- ✅ Daily highlights section auto-populated in review
- ✅ Active context updated with current + previous week
- ✅ All file links work (daily files, meetings, decisions)
- ✅ User has clear 15-20 min task to complete review
- ✅ Next week prep section ready to inform Monday planning

**Weekly review completion checklist:**
- [ ] Priority completion status marked
- [ ] Strategic alignment check completed
- [ ] Wins and achievements captured
- [ ] Challenges and learnings documented
- [ ] Key insights about effectiveness noted
- [ ] Decisions made this week summarized
- [ ] Time allocation and energy levels assessed
- [ ] Next week priorities drafted
- [ ] Intentions for next week set

---

## Next Steps

After implementing this workflow for 4 weeks:

1. **Generate first monthly review** (synthesize 4 weekly reviews)
2. **Evaluate archival pattern** (is weekly the right cadence?)
3. **Add search functionality** ("Find when we decided about X")
4. **Implement quarterly reviews** (strategic reflection)
5. **Consider automation** (trigger archival automatically on Fridays)

**Long-term vision:**
- Searchable knowledge base of all work
- Strategic patterns visible across months/quarters
- Easy reference to past decisions and context
- Clean workspace that doesn't overwhelm
- Continuous improvement through regular reflection

---

*This workflow maintains a professional, scalable task management system. Weekly archival prevents clutter while ensuring important context is never lost. The enhanced weekly review with daily highlights provides both detailed and summary views of each week's work.*

