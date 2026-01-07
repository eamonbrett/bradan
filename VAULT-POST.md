# How I Use AI to Save 65 Hours/Year at Shopify

**TL;DR:** Built an AI daily assistant that integrates with Vault, Slack, Calendar, Gmail, Salesforce, and our data warehouse. One command every morning = instant clarity on what matters. Open sourced it for Shopifolk.

---

## The Problem

Working at Shopify means:
- 6-12 meetings per day across multiple projects
- Hundreds of Slack messages across 20+ channels
- 50-100 emails daily
- Multiple workstreams at different stages
- Context switching every 30 minutes
- Fast-moving priorities

Every morning, I was spending 15-20 minutes just **rebuilding my mental model**:
- What meetings do I have today?
- What's actually urgent in Slack?
- What emails need responses?
- What did I commit to yesterday?
- What are my Top 3 priorities?

By 9:15 AM, I'd finally know what my day looked like. **That's 65 hours per year just on morning planning.**

---

## The Solution: Bradán

I built an AI-powered daily assistant that runs in Cursor IDE using Claude. It's called **Bradán** (Irish for "salmon" - Salmon of Knowledge reference).

Every morning, I open Cursor and say:

```
"Good morning"
```

**30 seconds later**, I have a fully-generated daily file with:

✅ **My Google Calendar** - all events for today  
✅ **Gemini meeting notes** - auto-linked from yesterday's meetings  
✅ **Slack priority inbox** - last 24h of messages, P1-P4 scored  
✅ **Gmail priority inbox** - categorized by urgency  
✅ **Top 3 tasks** - carried forward from yesterday + new priorities  
✅ **Meeting stubs** - pre-filled with attendees, links, and prep notes  

**Planning time: 15 minutes → 30 seconds**

---

## How It Works

### The Stack
- **Cursor IDE** - Claude integration via Composer
- **Python automation** - File generation, archival, templating
- **Shopify MCP servers** - Deep integration with our tools
- **Markdown files** - Portable, version-controlled, searchable

### The MCPs (This is the Magic)
Bradán connects to **7 Shopify MCP servers**:

| MCP | What I Use It For |
|-----|-------------------|
| **playground-slack-mcp** | Read all Slack messages, prioritize them automatically |
| **vault-mcp** | Search for projects, find project owners, link to missions |
| **gworkspace-mcp** | Pull calendar events, read Gmail, access Gemini notes |
| **data-portal-mcp** | Query DW directly from my daily file |
| **revenue-mcp** | Look up Salesforce accounts, search Salesloft calls |
| **support-core** | Find merchant tickets, check shop status |
| **dev-mcp** | Dev environment context |

All of this happens **automatically** when I run "Good morning."

---

## Real Workflow Examples

### Monday Morning (5 min)
```
Me: "Good morning"
```

**Claude generates:**
```markdown
# Daily Note - Monday, January 6, 2025

## 🎯 Top 3 Tasks Today

### 1. Product Review - POS Pro Expansion 🎯 Strategic
Why: Q1 priority for Retail team
Time: 10:00-11:30 AM | Energy: High
Status: Gemini notes from last week's prep meeting linked

Meeting Link: [Join](https://meet.google.com/...)
Attendees: @sarah, @james, @priya

Prep:
- [x] Review GMV data (see below)
- [ ] Check Vault for latest POS strategy
- [ ] Review Salesforce pipeline

---

## 📬 Priority Inbox (24 hours)

### P1 - Immediate Action Required (2)
1. **Slack - @sarah in #retail-strategy**
   "Can you review the Q1 deck before 2pm today?"
   → Draft response: [Link to comment]

2. **Email - james@shopify.com**
   "Need your input on the merchant escalation"
   → Ticket context: [support ticket link]

### P2 - Important, Not Urgent (5)
...

### P3 - FYI, Context (12)
...

### P4 - Low Priority (23)
...

---

## 📊 Quick Data Query

> Query: "Show me POS Pro adoption in retail vertical, last 30 days"

[Claude automatically queries data-portal-mcp]

Results: 
- 234 new POS Pro merchants
- 45% growth MoM
- Top vertical: Apparel (67 merchants)

---

## 📅 Calendar (5 events today)

10:00 - POS Pro Product Review
       📄 Gemini notes: [Link to yesterday's prep meeting]
       
14:00 - 1:1 with Sarah
       📝 Last time: Discussed Q1 roadmap priorities
       
...
```

**Total time to generate this: 30 seconds**  
**Time saved: 14.5 minutes**

---

### During the Day

As I work, I just check things off:

```markdown
- [x] Review Q1 deck for Sarah
- [x] Respond to merchant escalation
- [ ] Follow up on POS Pro feedback (moved to tomorrow)
```

**Incomplete tasks automatically carry forward to tomorrow's file.**

---

### Friday Afternoon (3 min)

```
Me: "Archive this week"
```

**Claude:**
1. Reads all 5 daily files from this week
2. Extracts every completed task
3. Finds all decision logs I created
4. Generates a weekly summary
5. Archives old files to `archive/2025/week-01/`
6. Prompts me with 3 reflection questions

**Output:**
```markdown
# Week 01 - January 1-5, 2025

## ✅ Accomplishments (23 completed tasks)

### Strategic Work
- Completed Q1 POS Pro planning review
- Finalized retail merchant segmentation strategy
- Shipped updated reporting dashboard

### Operational
- Resolved 3 merchant escalations
- Completed 8 1:1s with team
- Reviewed 12 project proposals in Vault

## 🎯 Key Decisions
- [[decisions/2025-01-03-pos-pricing-strategy.md]]
- [[decisions/2025-01-04-retail-pilot-scope.md]]

## 📊 Metrics
- Meetings: 18 (6h 30m)
- Top 3 completion: 89% (24/27)
- Response time: P1 items <2h average

## 🤔 Reflection
1. What worked well? [I fill this in]
2. What would I change? [I fill this in]
3. What's my #1 priority next week? [I fill this in]
```

**Time to generate: 5 minutes (including my reflection answers)**  
**Manual weekly review used to take: 45 minutes**

---

## Shopify-Specific Features I Love

### 1. Vault Integration
```
Me: "Search Vault for projects related to checkout optimization"
```

Claude searches Vault and links relevant projects directly in my daily file. I can see:
- Who owns it
- What stage it's in
- Recent updates
- How it connects to my work

### 2. Slack Prioritization
Instead of manually scanning 20 channels, Claude:
- Reads all messages from last 24h
- Scores them P1-P4 based on:
  - Mentions of me
  - Questions asked
  - Urgency signals
  - Context from my active projects
- Groups by priority

**I only read the P1s and P2s.** P3/P4 are collapsed for reference.

### 3. Data Queries
```
Me: "Add a data query: top 10 Plus merchants by GMV in Canada"
```

Claude queries data-portal-mcp and embeds the results right in my daily file. No switching to data.shopify.io.

### 4. Salesforce Context
```
Me: "Find Salesforce account for Allbirds"
```

Claude pulls the account details, recent opportunities, and key contacts. I have CRM context without leaving Cursor.

### 5. Gemini Meeting Notes
After every meeting with Gemini enabled:
- Gemini creates transcript + summary in Drive
- Claude automatically finds it
- Links it in my daily file
- Extracts action items

**I never manually create meeting notes anymore.**

---

## What This Looks Like in Practice

### Before Bradán
**Morning routine (15-20 min):**
1. Open Google Calendar → note meetings
2. Scan Slack (20 channels) → mentally prioritize
3. Check Gmail → flag important ones
4. Open Notion → write today's plan
5. Check Vault → any updates on my projects?
6. Open yesterday's notes → what's incomplete?
7. Create meeting note files manually

**Weekly review (45 min):**
1. Open each daily note
2. Copy/paste accomplishments
3. Find decision logs
4. Write summary
5. Archive files manually

**Total: 2h 15m per week**

### After Bradán
**Morning routine (30 sec):**
```
"Good morning"
```

**Weekly review (5 min):**
```
"Archive this week"
[Answer 3 reflection questions]
```

**Total: 22 minutes per week**

**Time saved: 1h 53m per week = 99 hours per year**

_(I conservatively report 65 hours because not every week is the same)_

---

## The Files

Everything lives in **markdown files** in one folder:

```
task-management/
├── work/daily/          # One file per day
├── work/weeks/          # Weekly plans
├── work/meetings/       # Meeting notes
├── work/projects/       # Project tracking
├── reference/decisions/ # Decision logs
└── archive/             # Historical files
```

**Benefits:**
- ✅ Version controlled (git)
- ✅ Searchable (grep/Spotlight)
- ✅ Portable (just markdown)
- ✅ No vendor lock-in
- ✅ Works offline
- ✅ AI-readable context

---

## Decision Logging

One underrated feature: **Decision logs**

Anytime I make a decision, I ask:
```
"Create a decision log about why we're focusing on retail vertical first"
```

Claude creates:
```markdown
# Decision: Focus Retail Vertical First

Date: 2025-01-06
Status: Decided
Owner: @eamonbrett

## Context
We need to prioritize one vertical for POS Pro expansion in Q1.

## Decision
Focus on Retail (apparel, home goods) instead of F&B.

## Rationale
- Higher GMV potential: $2.3M vs $800K
- Better product-market fit: 67% adoption vs 23%
- Fewer integration complexities

## Alternatives Considered
1. Food & Beverage - rejected due to lower GMV
2. Multi-vertical approach - rejected due to resource constraints

## Impact
- Marketing team focuses retail messaging
- Sales team prioritizes retail prospects
- Product roadmap deprioritizes F&B features for Q1

## Next Review
End of Q1 (March 31, 2025)
```

**Why this matters:**
- I never re-debate the same decision
- New team members understand context
- I can link to decisions in project docs
- Creates institutional knowledge

---

## How to Get It

I've open sourced this as **Bradán** for Shopifolk.

### Setup (15 minutes)

```bash
git clone https://github.com/eamonbrett/bradan.git
cd bradan
git checkout shopify-internal
pip install -r requirements.txt
```

Then follow [SETUP-SHOPIFY.md](https://github.com/eamonbrett/bradan/blob/shopify-internal/SETUP-SHOPIFY.md)

**You'll need:**
- Cursor IDE (free or pro)
- Python 3.8+
- Access to Shopify MCP servers (you already have this)

**Setup includes:**
- Configuring 7 MCP servers in `~/.cursor/mcp.json`
- Setting your timezone
- Customizing templates
- Testing with "Good morning"

---

## FAQ

**Q: Does this work if I don't use Cursor?**  
A: No - it's built specifically for Cursor + Claude integration.

**Q: What if I don't want Slack integration?**  
A: You can skip playground-slack-mcp and it still works great with just Calendar + Gmail.

**Q: Is my data private?**  
A: Yes - everything is local markdown files. Claude only sees what you share via Cursor. No data leaves your machine except MCP API calls (which you control).

**Q: Can I customize it?**  
A: Absolutely! Edit templates in `system/templates/` and customize the "memory bank" in `system/memory/` to match your role.

**Q: Do I need Cursor Pro?**  
A: Recommended. Free tier works but you'll hit limits quickly (50 requests/month). Pro gives you 500 requests/month which is plenty.

**Q: What about mobile?**  
A: It's desktop-focused (needs Cursor). But you can set up Slack notifications to ping you about P1 items.

---

## Results After 3 Months

**Time saved:**
- ✅ 15 min/day on morning planning = **5 hours/month**
- ✅ 40 min/week on weekly reviews = **2.5 hours/month**
- ✅ **Total: ~23 hours saved in 3 months**

**Quality improvements:**
- ✅ Never miss a Slack mention
- ✅ Calendar is always in context
- ✅ Decisions are documented
- ✅ Projects stay organized
- ✅ Weekly reviews actually happen

**Unexpected benefits:**
- ✅ Better 1:1s (I have context on what I committed to)
- ✅ Faster onboarding (teammates read my decision logs)
- ✅ Less context switching (everything in one place)
- ✅ Better work-life boundary (clear end-of-day review)

---

## Who This Is For

**Great fit:**
- Working across multiple projects
- 5+ meetings per day
- Active in 10+ Slack channels
- Need to track commitments
- Want better weekly reviews
- Like markdown/git workflows

**Maybe not for you:**
- Prefer visual tools (Notion, Jira)
- Don't use Cursor
- Mostly synchronous work (not many meetings)
- Already have a system that works

---

## Try It

**Repo:** https://github.com/eamonbrett/bradan/tree/shopify-internal  
**Setup guide:** [SETUP-SHOPIFY.md](https://github.com/eamonbrett/bradan/blob/shopify-internal/SETUP-SHOPIFY.md)  
**Questions?** DM me @eamonbrett or comment below

---

## One More Thing

There's also a **public version** (main branch) that works without Shopify MCP servers. I'm sharing it publicly on LinkedIn this week. If you know someone drowning in context switches, send them: https://github.com/eamonbrett/bradan

---

**Tags:** #productivity #ai #cursor #automation #workflow

**Built with:** Cursor, Claude, Python, Shopify MCPs, Google Workspace

**License:** Use freely for personal or team productivity

---

_Like the Salmon of Knowledge, instant clarity for your workday_ 🍀

