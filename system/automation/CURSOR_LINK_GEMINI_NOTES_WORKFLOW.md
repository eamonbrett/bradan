# Cursor Workflow: Link Gemini Meeting Notes

## When User Says

- "Link Gemini notes for today's meetings"
- "Link Gemini notes for yesterday"
- "Connect Gemini notes to meeting stubs"
- "Update meetings with Gemini recordings"

## Workflow Steps

### Step 1: Search Google Drive for Gemini Notes

**Call MCP Tool:**
```
Tool: mcp_gworkspace-mcp_search_drive
Parameters:
  query: "name contains 'Gemini' and modifiedDate > 'YYYY-MM-DD'"
  orderBy: "modifiedDate desc"
```

**What to search for:**
- Gemini notes are typically named: "Gemini recording [Meeting Name]"
- Modified date should be the date we're looking for (or recent)
- Files are Google Docs in Drive

**Example:**
For today's meetings, search: `name contains 'Gemini' and modifiedDate > '{today}'`

---

### Step 2: Read Gemini Note Content

For each Gemini doc found:

**Call MCP Tool:**
```
Tool: mcp_gworkspace-mcp_read_file
Parameters:
  file_id: "{file_id from search results}"
  format: "markdown"
```

**Extract from content:**
- Full meeting transcript
- Action items (look for "Suggested next steps" or "Action items")
- Key decisions
- Summary

---

### Step 3: Prepare Data for Linking Script

Format the Gemini docs data:

```python
gemini_docs = [
    {
        "title": "Gemini recording Eamon & Deann Check-in",
        "link": "https://docs.google.com/document/d/FILE_ID",
        "content": "Full markdown content from MCP read"
    },
    # ... more docs
]
```

---

### Step 4: Run Link Script

**Call Python Script:**
```python
from automation.link_gemini_notes import link_notes_command

# For today's meetings
stats = link_notes_command("today", gemini_docs)

# For yesterday
stats = link_notes_command("yesterday", gemini_docs)

# For specific date
stats = link_notes_command("2025-11-06", gemini_docs)
```

---

### Step 5: Report Results

**Show user:**
```
✅ Linked Gemini notes for {date}:
   - {X} meetings updated
   - {Y} already had notes
   - {Z} meetings without Gemini notes

📝 Updated files:
   - meetings/2025-11-06-eamon-deann.md
   - meetings/1-on-1s/eamon-olivia/2025-11-06.md
```

---

## Complete Example Flow

**User:** "Link Gemini notes for today's meetings"

**Claude:**

1. Get today's date: `2025-11-06`

2. Search Drive:
```
mcp_gworkspace-mcp_search_drive(
  query="name contains 'Gemini' and modifiedDate > '2025-11-06'"
)
```

3. Results: 3 Gemini docs found

4. Read each doc:
```
For each file_id:
  mcp_gworkspace-mcp_read_file(file_id, format="markdown")
```

5. Build gemini_docs list:
```python
[
  {
    "title": "Gemini recording Eamon & Deann",
    "link": "https://docs.google.com/...",
    "content": "Full transcript..."
  },
  # ...
]
```

6. Run script:
```python
link_notes_command("2025-11-06", gemini_docs)
```

7. Report:
```
✅ Linked Gemini notes for 2025-11-06:
   - 3 meetings updated
   - 0 already had notes
   - 0 meetings without Gemini notes
```

---

## Name Corrections

**Gemini transcription errors are auto-corrected:**

| Wrong (Gemini) | Correct |
|----------------|---------|
| Deian, Dian, Dean | Deann Evans |
| Burke | Birk Angermann |

The script automatically fixes these in all extracted summaries and action items.

**To add more corrections:**
Edit `automation/link_gemini_notes.py` → `NAME_CORRECTIONS` dictionary

---

## Matching Logic

The script matches meeting stubs to Gemini docs by:

1. **Title similarity:** Fuzzy matching on meeting names
2. **Date:** Both from same day
3. **Word overlap:** 70%+ key words match

**Examples:**
- Stub: `2025-11-06-eamon-deann-check-in.md`
- Gemini: `Gemini recording Eamon & Deann Check-in`
- Match: ✅ Yes (key words: eamon, deann, check, in)

---

## Enhanced Extraction (Future)

Currently, the script adds a simple summary. In the future, enhance to extract:

### Action Items
Look for sections in Gemini notes:
- "Suggested next steps"
- "Action items"
- "Follow-up tasks"

Parse and format as:
```markdown
## Action Items
- [ ] Eamon - Follow up on GTM Craft (by Nov 10)
- [ ] Deann - Review priorities (by Nov 8)
```

### Decisions
Look for:
- "We decided to..."
- "Decision:"
- "Agreed to..."

Format as:
```markdown
## Decisions
- Prioritize GTM Craft over Q4
- Weekly check-ins on Tuesdays
```

### Key Discussion
First paragraph or summary section from Gemini

---

## Error Handling

**No Gemini docs found:**
```
❌ No Gemini notes found for {date}
   Make sure Gemini recorded the meetings.
```

**No matching stubs:**
```
ℹ️  Found {X} Gemini notes but no matching meeting stubs for {date}
   Gemini docs found:
   - Gemini recording Team Sync
   - Gemini recording Product Review
```

**Already linked:**
```
⏭️  All meetings already have Gemini notes linked
```

---

## Integration with Other Workflows

### Morning Workflow
```
"Good morning"
→ Generate daily file
→ (Later, after meetings) "Link Gemini notes"
```

### Evening Workflow
```
End of day:
"Link Gemini notes for today's meetings"
→ All meetings updated with recordings
```

### Weekly Workflow
```
"This week is over"
→ Archive old meetings
→ Generate weekly summary (includes Gemini action items)
```

---

## File Updates

The script updates meeting stubs by:

1. Reading existing stub content
2. Checking if already has "## Meeting Notes"
3. If not, appending new section with:
   - Link to Gemini doc
   - Summary
   - Action items (if extracted)
   - Decisions (if extracted)

**Before:**
```markdown
# 2025-11-06 - Eamon & Deann

## Agenda
- Q4 priorities
```

**After:**
```markdown
# 2025-11-06 - Eamon & Deann

## Agenda
- Q4 priorities

## Meeting Notes

📎 **[Gemini Recording & Notes](https://docs.google.com/...)**

**Summary:**
Discussed Q4 priorities and GTM Craft strategy.

## Action Items
- [ ] Eamon - Draft GTM proposal (by Nov 10)
- [ ] Deann - Review team allocation (by Nov 8)
```

---

## Tips

**Best Practice:**
- Link notes at end of each day (captures all meetings)
- Don't wait until weekly summary (harder to match)

**If match fails:**
- Check Gemini doc title matches meeting name
- Manually add link if needed
- Update script's matching logic for future

**Multiple meetings with same person:**
- Script uses full title match
- Ensure stub titles are unique per day

---

## Next Steps

After linking notes:
1. Review action items in daily file
2. Create decision logs for important outcomes
3. Update project files if needed
4. Let weekly summary aggregate everything

---

**Implementation Status:** ✅ Ready to use

Run: `"Link Gemini notes for today's meetings"`

