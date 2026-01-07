# Cursor Weekly Summary Workflow

## AI Agent Instructions

⚠️ **CRITICAL:** Follow FACTUAL_ACCURACY_GUIDELINES.md at all times. Never synthesize or hallucinate action items, meetings, or context.

When the user asks for a "weekly summary" or "generate weekly summary", follow this workflow:

### Step 1: Search for Gemini Meeting Notes

Use `mcp_gworkspace-mcp_search_drive` to find Gemini meeting notes from the past week (or specified timeframe):

```
Query: fullText contains "Gemini" and (name contains "Notes by Gemini" or name contains "Eamon") and modifiedTime > "[DATE]"
Order by: modifiedTime desc
```

**Date Calculation:**
- For "last week": Use the previous Monday through Sunday
- Current week: Use this Monday to today
- Can specify weeks back (e.g., "last 2 weeks")

### Step 2: Filter for User's Meetings

From the search results, filter for meetings where "Eamon" appears in the title (indicating he's an attendee).

Typical patterns:
- `Eamon / Olivia`
- `Taylor / Olivia / Eamon`
- `Eamon / Fabian`

### Step 3: Read Meeting Notes

For each filtered meeting, use `mcp_gworkspace-mcp_read_file` to get the full content.

Extract from each meeting:
- Meeting title
- Date (from title format: YYYY/MM/DD)
- Attendees (from title)
- "Suggested next steps" section

### Step 4: Parse Action Items

From the "Suggested next steps" section, extract action items in format:
```
[Name] will [action]
[Name] to [action]
```

Parse into:
- Owner (person name)
- Task (the action)
- Meeting context (which meeting it came from)

### Step 5: Organize and Generate Summary

Create a markdown file with:

1. **Header**: Week range and generation date
2. **Overview**: Stats (meetings, actions, people)
3. **Meetings List**: All meetings attended with dates
4. **Actions by Owner**: Grouped by person, then by meeting
5. **Actions by Meeting**: Context view of each meeting
6. **Key Themes**: High-level patterns (optional)

### Step 6: Save the File

Save to: `weekly-summaries/weekly-summary-YYYY-MM-DD.md`

Where YYYY-MM-DD is the Monday of the week being summarized.

### Output Format Template

```markdown
# Weekly Meeting Summary
**Week of [Start Date] - [End Date], [Year]**
*Generated: [Current Date and Time]*

---

## 📊 Overview
- **Total Meetings:** X
- **Action Items:** Y
- **People with Actions:** Z

---

## 🗓️ Meetings Attended

[List each meeting with date and title]

---

## ✅ Action Items by Owner

### [Person Name]

**From: [Meeting Name] ([Date])**
- [ ] [Action item]
- [ ] [Action item]

---

## 📋 Action Items by Meeting

### [Meeting Title]
*[Date]*

- **[Owner]**: [Action]

---

## 💡 Next Steps

1. Review and prioritize action items above
2. Add high-priority items to your task management system
3. Schedule time blocks for key deliverables
4. Follow up with stakeholders as needed

[Optional: Key Themes section]
```

## User Trigger Commands

The user can request summaries with:
- "Generate weekly summary"
- "Create weekly meeting summary"
- "Summarize last week's meetings"
- "Weekly summary"
- "Generate summary for the last 2 weeks" (for custom timeframes)

## Example Workflow Execution

```
User: "Generate weekly summary"

AI:
1. Searches Google Drive for Gemini notes from last week
2. Filters for meetings with "Eamon" in title
3. Reads 4 meeting notes
4. Extracts 16 action items
5. Organizes by owner and meeting
6. Generates weekly-summary-2025-10-14.md
7. Reports completion with summary stats
```

## Error Handling

- If no meetings found: Inform user, suggest checking date range
- If meeting notes can't be read: Log which meetings failed, continue with others
- If action items parsing fails: Note in summary, include meeting anyway

## Factual Accuracy Requirements

**MUST DO:**
- ✅ Only extract action items explicitly stated in "Suggested next steps"
- ✅ Quote meeting notes directly when uncertain
- ✅ State source file for every action item: "From meeting: [[file]]"
- ✅ If action item owner unclear, state "Owner unclear from notes"
- ✅ If no action items in meeting, state "No action items documented"
- ✅ Count actual meetings found, don't estimate

**NEVER DO:**
- ❌ Synthesize action items from discussion content
- ❌ Assume action item owners not explicitly named
- ❌ Infer themes or priorities not explicitly stated
- ❌ Create summary statistics not from actual data
- ❌ Fill gaps with "typical" action items

**If Gemini Notes Missing or Incomplete:**
```markdown
## Limitations
⚠️ Gemini notes found: X of Y expected meetings
❓ Missing notes for: [list meetings without documentation]
❓ No action items section in: [list meetings]
```

## Best Practices

1. Always confirm the time period being summarized
2. Mention how many meetings were found and processed
3. Highlight any meetings that couldn't be processed
4. Provide the file path of the generated summary
5. Offer to open the file or show a preview
6. **NEW:** Explicitly state confidence level in completeness

## Integration with Daily Files

The user may want to reference the weekly summary in their Monday daily file:

```markdown
## Week in Review
- [ ] Review weekly meeting summary: [[weekly-summaries/weekly-summary-YYYY-MM-DD]]
- [ ] Transfer priority actions to today's tasks
```

Suggest this integration when generating on Mondays.












