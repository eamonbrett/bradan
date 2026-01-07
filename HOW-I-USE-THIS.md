# How I Actually Use This System

**A Personal Walkthrough by Eamon**

This isn't documentation—it's how I actually work day-to-day. If you want to understand the system before adopting it, read this first.

---

## The Core Idea

I talk to Claude in Cursor, and it manages my files. That's it.

Instead of maintaining spreadsheets, todo apps, or complex systems, I have markdown files that Claude reads, writes, and organizes. Everything lives in one folder. Everything is searchable. Nothing syncs or breaks.

---

## My Actual Daily Workflow

### Morning (~5 min)

I open Cursor in my `task-management` folder and say:

```
"Good morning"
```

Claude then:
1. Checks my Google Calendar for today's meetings
2. Scans recent Slack/email for anything urgent
3. Generates my daily file with the schedule already filled in
4. Surfaces yesterday's incomplete tasks as carry-forwards
5. Creates stub files for today's meetings (with attendees, links, context)

I review my **Top 3 tasks** for the day and adjust if needed. Done.

### During the Day

I work through my Top 3. When I finish something, I check it off:

```markdown
- [x] Review Andre's proposal
- [ ] Send churn guidance update
```

When I have a meeting, I open the pre-created meeting file and add notes. The file already has:
- Date, time, attendees
- Google Meet link
- Any prep items from my calendar

When I make a decision worth remembering, I say:

```
"Create a decision log about the B2B case closure policy"
```

Claude generates a proper decision document with context, rationale, and action items.

### Evening (~3 min)

Before shutting down, I scan my daily file:
- Anything left undone becomes tomorrow's carry-forward
- I add any quick notes about what happened
- That's it—no elaborate review process

---

## My Weekly Rhythm

### Monday Morning

```
"Generate this week's file"
```

Claude creates `work/weeks/2025-12-08-week-50.md` with:
- Last week's carry-forwards (auto-extracted)
- A blank Top 3 priorities section for me to fill
- A Friday reflection section (empty until Friday)

I spend **2 minutes** picking my Top 3 priorities for the week.

### Friday Afternoon

```
"Update this week's file"
```

Claude:
- Auto-extracts what I completed from my daily files
- Prompts me with 3 reflection questions:
  - What went well?
  - What would I change?
  - Key learning?

I spend **3 minutes** answering. Then:

```
"Archive this week"
```

Daily files move to `archive/daily/2025-12-week-50/`. Workspace stays clean.

---

## Where Everything Lives

I have 5 folders. That's it.

```
task-management/
├── work/          # What I touch daily
│   ├── daily/     # This week's daily files (4-5 files)
│   ├── weeks/     # This week + last week (2 files)
│   ├── meetings/  # Recent meeting notes
│   └── projects/  # Active projects
│
├── reference/     # Stuff I look up occasionally
│   ├── decisions/ # Decision logs (never delete these)
│   ├── career/    # Career development docs
│   └── docs/      # Guides and documentation
│
├── archive/       # Old stuff (organized, searchable)
├── system/        # Automation scripts (don't touch)
└── inbox/         # Temporary files (auto-cleared)
```

**The rule:** If I touch it daily, it's in `work/`. If I look it up occasionally, it's in `reference/`. If it's old, it's in `archive/`.

---

## The Commands I Actually Use

| When | I say | What happens |
|------|-------|--------------|
| Every morning | "Good morning" | Full setup: calendar, inbox, daily file |
| Need a meeting file | "Create a meeting file for the Andre sync" | Pre-filled meeting template |
| Made a decision | "Create decision log about X" | Formatted decision document |
| Friday afternoon | "Update this week's file" | Auto-extracts accomplishments |
| Friday end of day | "Archive this week" | Moves files to archive |
| Feeling overwhelmed | "Show me my priority inbox" | Email + Slack prioritized |

---

## What Makes This Different

### vs. Todo Apps (Todoist, Things, etc.)
- No context switching—I'm already in my IDE
- Files are searchable, version-controllable, portable
- Claude understands context ("that meeting with Andre" works)

### vs. Notion/Obsidian
- No manual organizing—Claude handles structure
- No plugin management or sync issues
- Calendar integration is automatic, not manual entry

### vs. Paper/Notebooks
- Searchable
- Carry-forwards are automatic
- Can't lose it

---

## The Magic Moments

**1. "What did I decide about X?"**
I ask Claude. It searches my decision logs and tells me.

**2. Pre-filled meeting files**
When I open a meeting file, it already has attendees, links, and context from my calendar. I just add notes.

**3. Carry-forwards work**
Incomplete tasks from yesterday appear in today's file automatically. Nothing falls through cracks.

**4. Friday summaries**
Instead of trying to remember what I did, Claude extracts it from my daily files. Accurate, no effort.

**5. Priority inbox**
When I'm drowning in Slack and email, I ask for my priority inbox. Claude scores everything by urgency × impact and shows me what actually matters.

---

## How Long Before This Feels Natural

- **Day 1:** Follow the commands exactly. Feel clunky.
- **Week 1:** Start to trust the morning routine.
- **Week 2:** Notice you're not losing track of things.
- **Week 3:** Customize templates to your style.
- **Month 1:** Can't imagine going back.

---

## The Time Investment

**Setup:** 30 minutes (with my template)

**Daily:**
- Morning: 5 minutes
- During day: Just check off tasks
- Evening: 3 minutes

**Weekly:**
- Monday: 2 minutes
- Friday: 3 minutes

**Total planning overhead:** ~35 minutes/week

**Time saved:** 57 hours/year (according to my estimates—your mileage may vary)

---

## My Advice If You Try This

1. **Use "Good morning" every day for a week.** Don't customize yet. Just follow the system.

2. **Trust the carry-forwards.** Stop trying to remember things. If it matters, it'll show up tomorrow.

3. **Decision logs are underrated.** Every time you debate the same thing twice, you needed a decision log the first time.

4. **Keep Top 3 sacred.** Don't list 10 tasks. Pick 3. Finish them. Add more if you want.

5. **Friday archive is non-negotiable.** The weekly cleanup is what keeps this from becoming chaos.

---

## What You Need

- **Cursor IDE** (cursor.com) — This is non-negotiable. The AI integration is the whole point.
- **Google Workspace** — For calendar integration
- **30 minutes** — To set it up using my template

Optional:
- Slack integration (for priority inbox)
- Python (for some automation scripts)

---

## Questions People Ask

**"Isn't this just todo lists in markdown?"**

No. The AI integration is the difference. Claude doesn't just store my tasks—it creates files, extracts patterns, connects context, and does the tedious organizing I used to do manually.

**"What if Claude makes mistakes?"**

It does sometimes. But they're visible in markdown files I can edit. There's no black box.

**"Is this secure?"**

All files are local. Nothing syncs to a third-party service (except via MCP to Google/Slack, which I control). You can version control with a private GitHub repo.

**"Can I customize the templates?"**

Yes. Everything's in `system/templates/`. Edit to taste.

---

## Get Started

1. Get my template (see SETUP_GUIDE.md)
2. Spend 30 minutes setting up
3. Tomorrow morning, say "Good morning"
4. Report back in a week

---

*This is how I actually work. It's not perfect, but it's the best system I've found. Try it.*


