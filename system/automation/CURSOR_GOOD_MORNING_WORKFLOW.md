# Cursor Workflow: "Good morning" Complete Morning Setup

## When User Says

- "Good morning"

## What This Triggers

Complete morning preparation workflow that gets everything ready before 9:00 AM work start time.

---

## Workflow Steps (Execute in Order)

### Step 1: Fetch Today's Calendar Events

**Call MCP Tool:**
```
Tool: mcp_gworkspace-mcp_calendar_events
Parameters:
  calendar_id: "primary"
  time_min: "{today} 00:00:00"
  time_max: "{today} 23:59:59"
  include_attendees: true
```

**Extract:**
- Meeting times
- Attendees
- Google Meet links
- Locations

---

### Step 2: Check Recent Emails (Last 24 Hours)

**Call MCP Tool:**
```
Tool: mcp_gworkspace-mcp_read_mail
Parameters:
  query: "after:{yesterday}"
  max_results: 50
  include_body: true
```

**Look for:**
- Urgent messages (urgent keywords, from leadership)
- Action items directed at you
- Decisions needing input
- Time-sensitive requests

---

### Step 3: Analyze Recent Slack Messages (Last 24 Hours)

**Call MCP Tool:**
```
Tool: mcp_playground-slack-mcp_slack_my_messages
Parameters:
  after: "{yesterday's date in YYYY-MM-DD}"
  count: 100
```

**Look for:**
- Direct mentions (@eamon)
- Commitments you made
- Requests from others
- Active threads needing follow-up
- Important channel discussions

---

### Step 4: Check for Gemini Meeting Notes from Previous Day

**Call MCP Tool:**
```
Tool: mcp_gworkspace-mcp_search_drive
Parameters:
  query: "name contains 'Gemini' and modifiedTime > '{yesterday}'"
  orderBy: "modifiedTime desc"
```

**For each Gemini note found:**
- Extract action items from "Suggested next steps"
- Identify your action items
- Note any decisions made

---

### Step 5: Generate Daily File with All Context

**Call Python Script:**
```python
from system.automation.cursor_generate_daily import CursorDailyGenerator

generator = CursorDailyGenerator()
generator.generate_daily_file(
    target_date="{today}",
    calendar_events=calendar_data,
    enable_slack=True
)
```

**File generated:** `work/daily/YYYY-MM-DD.md` with:
- Today's schedule (from calendar)
- Meeting stubs created
- Template structure ready

---

### Step 6: Create Top 3 Prioritized Tasks

**Analyze and combine:**
- P1 items from priority inbox
- Action items from yesterday's Gemini notes (your items only)
- Carry-forward from yesterday's daily file
- This week's priorities from week file

**Generate Top 3:**
1. 🔴 **HIGH** - Most urgent/important (P1 item or critical action)
2. 🟡 **MEDIUM** - Important but not blocking (strategic work)
3. 🟢 **LOW** - Lower priority but should complete (operational)

**Add to daily file** in "Top 3 Tasks Today" section

---

### Step 7: Create Calendar Time Blocks

**Add to daily file under "Calendar Blocks to Add" section:**

**Protected blocks:**
- [ ] **10:00-11:00 AM** - "🐕 Dog Walking (Do Not Schedule)" ⚠️ ALWAYS PROTECTED

**Focus blocks (based on meeting gaps):**
- [ ] Morning focus block - Between meetings and before dog walk
- [ ] Afternoon focus block 1 - Between meetings  
- [ ] Afternoon focus block 2 - End of day wrap up

**User must manually add these to Google Calendar to prevent overbooking.**

**Example blocks for today:**
```
- [ ] 9:30-10:00 AM - "Focus: Priority Inbox"
- [ ] 10:00-11:00 AM - "🐕 Dog Walking (Protected)" ⚠️
- [ ] 11:00-12:00 PM - "Focus: Meeting Prep"
- [ ] 2:00-3:00 PM - "Focus: Leadership Day"
- [ ] 3:30-5:00 PM - "Focus: Documentation"
```

---

### Step 8: Generate Slack Priority Summary

**Call Python Script:**
```python
from system.automation.priority_inbox import PriorityInbox

inbox = PriorityInbox()
summary = inbox.generate_summary(
    emails=email_data,
    slack_messages=slack_data,
    format="slack"
)
```

**Save to:** `inbox/slack-priority-summary-{today}.md`

**Include:**
- P1/P2 urgent items
- Stats (total items, decisions needed)
- Recommended actions

---

### Step 9: Update Daily File with Latest Context

**Add to daily file:**

1. **Strategic Focus** section:
   - Pull from this week's file
   - Connection to mandate

2. **Top 3 Tasks** (from Step 6)

3. **Schedule** (from Step 1):
   - Morning block
   - Afternoon block
   - Protected dog walking time

4. **Meetings Today** (from Step 1):
   - Count
   - List with times and links

5. **Priority Inbox Summary** (from Step 8):
   - Brief mention of P1/P2 count
   - Link to full summary in inbox/

---

### Step 10: Report to User

**Show summary:**
```
☀️ Good morning! Your day is ready:

📅 Calendar: {X} meetings scheduled
📧 Priority Inbox: {Y} items ({Z} urgent)
🎯 Top 3 Tasks: [List them]
⏰ Protected Time: 10:00-11:00 AM (dog walking)

✅ Generated:
   - work/daily/2025-11-20.md
   - inbox/slack-priority-summary-2025-11-20.md
   - {X} meeting stubs

📍 Your day starts at 9:00 AM
🐕 Dog walk: 10:00 AM
```

---

## Output Files Created

1. **`work/daily/YYYY-MM-DD.md`** - Today's daily file with:
   - Strategic focus
   - Top 3 tasks (prioritized from all sources)
   - Full schedule with time blocks
   - Meeting list with stubs
   - Priority inbox summary reference

2. **`inbox/slack-priority-summary-YYYY-MM-DD.md`** - Priority inbox with:
   - All emails + Slack (last 24h)
   - Sorted by urgency × impact
   - P1/P2/P3/P4 categories
   - Recommended actions

3. **`work/meetings/YYYY-MM-DD-[meeting-name].md`** - Meeting stubs with:
   - Attendees
   - Time
   - Google Meet link
   - Agenda template

---

## Time Saved

**Without automation:** 15-20 minutes
- Check calendar (2 min)
- Check email (5 min)
- Check Slack (5 min)
- Create daily file (3 min)
- Set up meeting stubs (2 min)
- Prioritize tasks (3 min)

**With "Good morning":** 30 seconds
- Say command
- Review output
- Start working

**Daily savings:** ~15 minutes = 65 hours/year

---

## Best Practices

### Timing
- Run between 7:00-9:00 AM (before work starts at 9:00 AM)
- Gives you time to review before first meeting (9:30 AM)
- Dog walking at 10:00 AM is automatically protected

### What to Review (5 min)
1. **Priority inbox summary** - Any P1 items?
2. **Top 3 tasks** - Do these make sense?
3. **Schedule** - Any conflicts or prep needed?
4. **Meeting stubs** - Add agenda items if needed

### Integration with Weekly
- Monday: Also run "Generate this week's file" first
- Friday: Run "This week is over" instead
- Other days: Just "Good morning"

---

## Error Handling

**No calendar events:**
- Still generates daily file
- Shows "No meetings scheduled"

**No urgent emails/Slack:**
- Priority summary shows "No urgent items"
- File still generated

**Gemini notes not found:**
- Continues workflow
- Note in summary: "No Gemini notes from yesterday"

---

## Implementation Status

✅ Calendar integration (gworkspace-mcp)  
✅ Gmail integration (gworkspace-mcp)  
✅ Slack integration (playground-slack-mcp)  
✅ Daily file generation (cursor_generate_daily.py)  
✅ Priority inbox (priority_inbox.py)  
✅ Gemini note search (Drive MCP)  
✅ Meeting stubs creation  
✅ Top 3 prioritization  
✅ Time block protection (10:00 AM dog walking)  

**Status:** ✅ Fully operational

---

**Usage:** Simply say `"Good morning"` and everything is ready!

