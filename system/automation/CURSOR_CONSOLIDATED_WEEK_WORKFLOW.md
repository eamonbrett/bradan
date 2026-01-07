# Consolidated Week Workflow - Cursor Instructions

## Overview

**OLD SYSTEM (Eliminated):**
- 3 separate files: Weekly Plan + Weekly Summary + Weekly Review
- 90% manual work, tons of duplication
- 45+ minutes of manual data entry per week

**NEW SYSTEM:**
- 1 consolidated file: `weeks/YYYY-MM-DD-week-N.md`
- 90% auto-populated from your actual work in Cursor
- 5 minutes total: 2 min Monday setup + 3 min Friday reflection

---

## File Locations

### New (Active)
- **Weeks:** `weeks/2025-11-10-week-46.md` (consolidated)
- **Templates:** `reviews/template-weekly-review-enhanced.md` (simplified)
- **Daily:** `daily/template-daily-v2.md` (current)

### Deleted (Old/Duplicate)
- ❌ `reviews/template-weekly-review.md` (old bureaucratic template)
- ❌ `daily/template-daily.md` (old v1 template)
- ❌ `reviews/weekly-review-2025-10-14.md` (standalone file)

---

## How It Works

### Auto-Extraction Sources

The system automatically extracts from:

1. **Daily Files** (`daily/` and `archive/daily/`)
   - ✅ Completed tasks (checked checkboxes)
   - 🔲 Incomplete tasks (unchecked checkboxes)
   - 🎯 Top 3 priorities worked each day
   - 📊 Patterns across the week

2. **Meeting Notes** (`meetings/`)
   - 💭 Decisions made
   - 📋 Action items (incomplete)
   - 🔗 Meeting outcomes that matter

3. **Decision Logs** (`decisions/`)
   - 📄 New decisions documented this week
   - ⚖️ Status of each decision

4. **Calendar Events**
   - 📅 Meeting count for the week
   - ⏰ Time allocation

---

## Monday Morning Workflow (2 Minutes)

**User says:** `"Generate this week's file"` or `"Set up week of Nov 10"`

**What happens:**

1. **Claude runs:** `python3 automation/week_generator.py 2025-11-10`

2. **System extracts from last week:**
   - Unfinished tasks from daily files
   - Incomplete meeting action items
   - Patterns in priorities worked

3. **File generated:** `weeks/2025-11-10-week-46.md` with:
   - ✅ Carry-forwards automatically listed
   - 📋 Top 3 priorities pre-populated (user adjusts)
   - 📊 Section ready for Friday reflection

4. **User reviews (2 min):**
   - Scan carry-forwards
   - Adjust Top 3 priorities
   - Done!

---

## Friday Afternoon Workflow (3 Minutes)

**User says:** `"Update this week's file"` or `"Complete week of Nov 10"`

**What happens:**

1. **Claude runs:** `python3 automation/week_generator.py 2025-11-10`

2. **System extracts from this week:**
   - All completed tasks (✅)
   - Decision logs created
   - Meetings that had outcomes
   - Time reality check (meeting count, priorities)

3. **File updated with auto-generated section:**
   - ✅ What Actually Happened (all extracted)
   - 📊 Deliverables completed
   - 💭 Meetings that mattered
   - ⏰ Time reality check

4. **User completes reflection (3 min):**
   - Answer 3 simple questions:
     1. What went really well?
     2. What would you do differently?
     3. What's the key learning?
   - Done!

---

## Commands

### Generate New Week File (Monday)
```python
python3 automation/week_generator.py 2025-11-10
```

**Cursor command:** "Generate this week's file" or "Set up week of Nov 10"

### Update Week File (Friday)
```python
python3 automation/week_generator.py 2025-11-10
```

**Cursor command:** "Update this week's file" or "Complete week of Nov 10"

*Same command - system automatically detects whether to generate Monday setup or Friday reflection based on day of week*

### Extract Data Only (Debug)
```python
python3 automation/week_extractor.py 2025-11-10
```

---

## What Gets Auto-Populated

### Monday (from last week's data):
- ✅ Unfinished work (from unchecked tasks)
- 📋 Meeting action items (from incomplete actions)
- 🎯 Suggested priorities (from patterns)

### Friday (from this week's data):
- ✅ All completed tasks (up to top 15)
- 📄 Decision logs created
- 💭 Meetings with decisions/actions
- ⏰ Meeting count and time allocation
- 📊 Priority patterns (what you actually worked on)

---

## What You Fill In

### Monday (2 minutes):
- Review carry-forwards (pre-populated)
- Adjust Top 3 priorities (pre-populated template)
- That's it!

### Friday (3 minutes):
- Answer 3 reflection questions (1-2 sentences each)
- That's it!

---

## Integration with Other Workflows

### Daily Files
- Continue using `daily/YYYY-MM-DD.md` as normal
- Check off tasks as you complete them
- System extracts automatically on Friday

### Meeting Notes
- Continue documenting in `meetings/` as normal
- Add decisions and action items as you do now
- System extracts automatically

### Decision Logs
- Continue creating in `decisions/` as normal
- System detects new ones this week

### Weekly Archival
- Friday archival workflow unchanged
- Daily files move to `archive/daily/YYYY-MM-week-N/`
- Week file stays in `weeks/` (not archived)

---

## File Structure

```
task-management/
├── weeks/                          # NEW - Consolidated weekly files
│   ├── 2025-11-10-week-46.md
│   └── 2025-11-17-week-47.md
│
├── daily/                          # Unchanged
│   ├── 2025-11-10.md
│   └── template-daily-v2.md       # KEPT - current template
│
├── weekly-plans/                   # DEPRECATED - will phase out
├── weekly-summaries/               # DEPRECATED - Gemini summaries still generated here
│
├── reviews/                        # SIMPLIFIED
│   ├── template-weekly-review-enhanced.md  # KEPT - simplified template
│   └── weekly/
│       └── 2025-11-03-week-45.md  # OLD FORMAT - being phased out
│
├── automation/
│   ├── week_extractor.py          # NEW - Extract data from daily work
│   ├── week_generator.py          # NEW - Generate consolidated files
│   └── CURSOR_CONSOLIDATED_WEEK_WORKFLOW.md  # This file
│
└── archive/daily/                  # Unchanged
    └── 2025-11-week-45/
```

---

## Benefits

### Time Savings
- **Before:** 45 min/week (15 min plan + 15 min summary + 15 min review)
- **After:** 5 min/week (2 min Monday + 3 min Friday)
- **Savings:** 40 minutes per week = 35 hours per year

### No Duplication
- **Before:** Same data copied 3 times manually
- **After:** Extracted once automatically

### Always Current
- **Before:** Manual entries lag reality
- **After:** Reflects actual work done in Cursor

### Reduced Cognitive Load
- **Before:** "What did I do this week? Let me remember..."
- **After:** "Here's what you actually did. Any thoughts?"

---

## Troubleshooting

### File not generating
**Check:** Is `weeks/` directory created?
```bash
mkdir -p weeks
```

### No data extracted
**Check:** Are daily files using checkboxes?
- Use: `- [ ]` and `- [x]`
- Not: `* [ ]` or other formats

### Extraction errors
**Run debug command:**
```bash
python3 automation/week_extractor.py 2025-11-10
```

### Wrong week
**Specify date explicitly:**
```bash
python3 automation/week_generator.py 2025-11-10
```

---

## Future Enhancements

### Potential Additions (not yet built):
- Auto-suggest Top 3 priorities using AI pattern matching
- Auto-categorize completed tasks (strategic vs operational)
- Meeting time vs deep work analysis
- Trend analysis across multiple weeks
- Integration with Google Calendar for time tracking

### Not Planned:
- Complex metrics and dashboards (keep it simple)
- Detailed time tracking (not helpful)
- Bureaucratic sections (eliminated intentionally)

---

## Migration from Old System

### What to do with existing files:

**Weekly Plans (`weekly-plans/`):**
- Keep for reference
- Don't create new ones
- Use `weeks/` going forward

**Weekly Summaries (`weekly-summaries/`):**
- Keep for meeting notes reference
- Gemini summaries still valuable
- Data auto-extracted to `weeks/`

**Weekly Reviews (`reviews/weekly/`):**
- Keep old ones for reference
- Don't create new ones
- Use `weeks/` going forward

### Cleanup (optional):
```bash
# Move old plans to archive
mkdir -p archive/old-weekly-plans
mv weekly-plans/*.md archive/old-weekly-plans/

# Move old reviews to archive (keep summaries)
mkdir -p archive/old-weekly-reviews
mv reviews/weekly/*.md archive/old-weekly-reviews/
```

---

## Quick Reference

| Task | Command | Time |
|------|---------|------|
| Monday setup | "Generate this week's file" | 2 min |
| Friday reflection | "Update this week's file" | 3 min |
| View last week | Open `weeks/2025-11-03-week-45.md` | 0 min |
| Debug extraction | `python3 automation/week_extractor.py [date]` | - |

---

**Last Updated:** November 10, 2025  
**Status:** ✅ Active - Ready to use  
**Next Review:** After 4 weeks of usage (Dec 8, 2025)

