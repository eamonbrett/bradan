# Cursor Priority Inbox Workflow

## AI Agent Instructions

⚠️ **CRITICAL:** Follow FACTUAL_ACCURACY_GUIDELINES.md at all times. Only use actual MCP data - never synthesize messages, senders, or urgency scores.

When the user asks for their "priority inbox" or "what's on deck", follow this workflow:

---

## Step 1: Fetch Emails

Use `mcp_gworkspace-mcp_read_mail` to get recent emails:

```python
# Default parameters:
{
    "query": "is:unread OR newer_than:1d",  # Unread or from last day
    "max_results": 50,  # Reasonable limit
    "include_body": False  # Just need snippets for prioritization
}
```

**Custom timeframes:**
- "last 4 hours": `newer_than:4h`
- "today": `newer_than:1d`
- "this week": `newer_than:7d`

**Extract from each email:**
- From (sender name and email)
- Subject
- Snippet (preview text)
- Date
- Has attachment (boolean)

---

## Step 2: Fetch Slack Messages

Use your Slack MCP's message retrieval function (if configured) to get recent Slack activity:

```python
# Default parameters:
{
    "after": "[DATE]",  # Start date (e.g., yesterday)
    "before": "[DATE]",  # End date (e.g., now)
    "count": 100  # Reasonable limit
}
```

**For date calculations:**
- "last 24 hours": after = yesterday, before = now
- "last 4 hours": after = 4 hours ago, before = now
- "today": after = start of today, before = now

**Extract from each message:**
- User (sender)
- Channel name
- Text (message content)
- Timestamp
- Thread status (is it in a thread?)
- Is it a DM?
- Were you @mentioned?

---

## Step 3: Process with Priority Inbox Module

Import and use the `priority_inbox.py` module:

```python
from automation.priority_inbox import PriorityInbox, format_one_screen_output

# Create inbox
inbox = PriorityInbox()

# Add emails
emails = [
    {
        'id': email_id,
        'from': sender,
        'subject': subject,
        'snippet': preview_text,
        'date': date_string,
        'has_attachment': True/False
    }
    # ... more emails
]
inbox.add_emails(emails)

# Add Slack messages
messages = [
    {
        'user': user_name,
        'user_name': display_name,
        'channel_name': channel,
        'text': message_text,
        'ts': timestamp,
        'thread_ts': thread_timestamp,
        'channel_type': 'im' or 'channel',
        'is_mention': True/False
    }
    # ... more messages
]
inbox.add_slack_messages(messages)

# Get prioritized summary
summary = inbox.get_prioritized_summary(max_items=25)

# Format for display
output = format_one_screen_output(summary)
```

---

## Step 4: Display the Output

Present the formatted one-screen output to the user.

The output includes:
- Header with generation time
- Stats overview (total items, high priority count, etc.)
- P1 items (🔴 Urgent & High Impact)
- P2 items (🟠 High Priority)
- P3 items (🟡 Medium Priority)
- P4 items (🟢 Low Priority)
- Recommended actions

---

## Step 5: Optional - Send to Slack

If user requests "send to Slack", use the notification formatter:

```python
from automation.priority_inbox import create_priority_inbox_notification

notification_text = create_priority_inbox_notification(summary)

# Then use MCP to send
[your-slack-mcp]_send_message(
    recipient="me",
    message=notification_text
)
```

---

## User Trigger Commands

The user can request priority inbox with:
- "Show me my priority inbox"
- "What's on deck for me?"
- "Check my emails and Slack"
- "Priority inbox for today"
- "What needs my attention?"
- "Show me urgent items"

**With Slack notification:**
- "Show priority inbox and send to Slack"
- "Send me priority inbox notification"

**Filtered requests:**
- "Show me only P1 items"
- "What decisions do I need to make?"
- "Show emails only" (skip Slack)
- "Check Slack only" (skip emails)

---

## Example Workflow Execution

```
User: "Show me my priority inbox"

AI:
1. Calls mcp_gworkspace-mcp_read_mail (last 24h, max 50)
   → Gets 23 emails

2. Calls Slack MCP message function (if configured - last 24h, max 100)
   → Gets 34 Slack messages

3. Processes with priority_inbox.py:
   - Calculates urgency scores
   - Calculates impact scores
   - Assigns priority levels (P1-P4)
   - Categorizes by type

4. Generates one-screen summary:
   - 6 P1 items (urgent & high impact)
   - 8 P2 items (high priority)
   - 12 P3 items (medium priority)
   - 31 P4 items (low priority)

5. Displays formatted output with recommendations

6. Reports: "Your priority inbox shows 6 urgent items that need immediate attention"
```

---

## Prioritization Logic

### Urgency Calculation

**High Urgency (score >= 5):**
- Contains urgent keywords: "urgent", "asap", "critical", "approval needed"
- Direct message (Slack DM)
- Direct @mention
- From executive (CTO, VP, Director)
- Decision/approval required

**Medium Urgency (score 2-4):**
- Has attachment
- From important stakeholder
- Meeting-related
- Mentioned but not directly

**Low Urgency (score < 2):**
- General announcements
- FYI messages
- No special indicators

### Impact Calculation

**High Impact (score >= 4):**
- Business-critical keywords: "revenue", "customer escalation", "strategy", "quarterly"
- Executive topics
- Production/system issues
- Budget/resource decisions

**Medium Impact (score 2-3):**
- Strategic topics
- Team/people matters
- Project decisions

**Low Impact (score < 2):**
- Informational
- General updates
- Optional participation

### Priority Matrix

```
Priority = Urgency × Impact

P1 (9): High Urgency × High Impact
P2 (6-8): High Urgency × Medium Impact, or Medium Urgency × High Impact
P3 (4-5): Mixed levels
P4 (1-3): Low on both dimensions
```

---

## Error Handling

**If Gmail access fails:**
- Inform user
- Continue with Slack only
- Note in output that emails were skipped

**If Slack access fails:**
- Inform user
- Continue with emails only
- Note in output that Slack was skipped

**If both fail:**
- Report error
- Suggest checking MCP configuration
- Offer to help with troubleshooting

**If no items found:**
- Celebrate: "You're all caught up! 🎉"
- Suggest checking again later
- Offer to adjust timeframe

---

## Best Practices

### 1. Always Confirm Timeframe

Tell the user what period you're checking:
- "Checking emails and Slack from the last 24 hours..."
- "Scanning your inbox from the past 4 hours..."

### 2. Highlight Key Numbers

After generating, summarize:
- "Found 47 items total"
- "6 urgent items need immediate attention"
- "4 decisions are waiting on you"

### 3. Provide Context

Explain priority levels:
- "P1 items are urgent AND high-impact - handle these first"
- "P2 items should be scheduled for today"

### 4. Offer Actions

After displaying, suggest:
- "Would you like me to add P1 items to your daily file?"
- "Should I send this summary to Slack for mobile access?"
- "Want to filter for decision-required items only?"

### 5. Respect Privacy

- Never show full email/message content without permission
- Keep previews to 80 characters max
- Remind user this is private data

---

## Factual Accuracy Requirements

**MUST DO:**
- ✅ Only show messages actually retrieved from MCP tools
- ✅ Use exact urgency/impact scores from priority_inbox.py algorithm
- ✅ State actual message count: "Found X emails, Y Slack messages"
- ✅ Use real timestamps from MCP data
- ✅ Show actual senders (don't anonymize unless requested)
- ✅ Quote message subject/preview exactly as received

**NEVER DO:**
- ❌ Synthesize example messages not in actual inbox
- ❌ Inflate urgency scores for emphasis
- ❌ Estimate message counts ("about 50 items")
- ❌ Assume sender importance not in scoring algorithm
- ❌ Create categories not in documented categorization rules
- ❌ Add context not in message preview

**When MCP Data Unavailable:**
```markdown
## Priority Inbox Status
⚠️ Unable to fetch [email/Slack] data
Error: [specific MCP error message]
Showing partial inbox with available data only
```

**Always Include Data Summary:**
```markdown
## Data Summary
- Emails scanned: X (from last Yh)
- Slack messages scanned: Z (from last Yh)
- Urgency scoring: Applied algorithm from priority_inbox.py
- Impact scoring: Applied algorithm from priority_inbox.py
- Manual review recommended for: [sensitive items]
```

---

## Integration with Daily Files

### Suggest Adding to Daily Top 3

After showing priority inbox, offer:

```
"I see 6 P1 items. Would you like me to add the top 3 to your daily file?"
```

Then update the daily file's Top 3 section with highest priority items.

### Morning Workflow Integration

When generating daily files in the morning:

```
User: "Generate daily file"

AI: 
1. Generates daily file
2. Offers: "Would you like me to check your priority inbox to populate Top 3 tasks?"
3. If yes, runs priority inbox
4. Adds P1 items to daily file
```

---

## Sample Output Format

```markdown
# 🎯 Priority Inbox
*Generated: 2025-10-16 08:30*

## 📊 Overview
**47 items** | ✉️ 23 emails | 💬 24 Slack | 🔴 6 urgent | 🎯 4 need decision

## 🔴 URGENT & HIGH IMPACT - Do First
*6 item(s)*

- ✉️ **ryan.thompson**: Approve: Q4 SE Compensation Framework [📎]
  _🎯 Decision Required_ | Urgency: HIGH | Impact: HIGH
  `Please review attached framework. Need approval by 10am to share with team...`

- 💬 **sarah.jones**: Budget approval needed [@you, 📎]
  _🎯 Decision Required_ | Urgency: HIGH | Impact: HIGH
  `Can you approve the Q4 SE budget changes? Attached spreadsheet...`

[... more items ...]

---

## ✅ Recommended Actions

1. **🔴 Handle 6 P1 item(s) immediately** - These are blocking others or time-sensitive
2. **🟠 Schedule 8 P2 item(s) for today** - Add to your daily Top 3 if needed
3. **🎯 Make 4 decision(s)** - Others are waiting on you

💡 *Tip: Use `Mark as complete` or `Snooze` in your inbox to clear items*
```

---

## Advanced Features

### Filter by Category

User can ask:
```
"Show me only decision-required items"
"Filter priority inbox for meeting-related"
"Show active Slack threads only"
```

Process normally, then filter results before displaying.

### Save to File

User can ask:
```
"Save priority inbox to file"
"Create priority-inbox-2025-10-16.md"
```

Write the formatted output to a new markdown file in the root directory or `daily/` folder.

### Compare Time Periods

User can ask:
```
"Show priority inbox for today vs yesterday"
"How many urgent items compared to last week?"
```

Run priority inbox for two timeframes and present comparison stats.

---

## Performance Considerations

**API Limits:**
- Gmail: Limit to 50 emails max
- Slack: Limit to 100 messages max

**Processing Time:**
- Should complete in < 10 seconds for typical volumes
- Notify user if processing is taking longer

**Context Size:**
- One-screen output typically 25-30 items
- Full summary limited to 25 items by default
- Remaining items summarized as counts

---

## Testing Checklist

Before presenting to user, verify:
- [ ] All P1 items have clear urgency/impact justification
- [ ] No duplicate items
- [ ] Dates/times are accurate
- [ ] Previews are sanitized (no sensitive data leaking)
- [ ] Stats are accurate (counts match items)
- [ ] Output fits on one screen (not too long)
- [ ] Action recommendations make sense

---

## Future Enhancements

Potential additions (not yet implemented):

- **Learn from user feedback**: "This wasn't urgent" → adjust scoring
- **Track completion**: Mark items as done in the system
- **Scheduled delivery**: Auto-generate at 8am daily
- **Smart filtering**: "Hide newsletters", "Only from team"
- **Trend analysis**: "Am I getting more urgent items than last week?"
- **Integration with calendar**: "Is this meeting prep urgent because meeting is today?"

---

**Last Updated:** October 16, 2025

