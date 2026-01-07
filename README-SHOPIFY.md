# Bradán - Shopify Internal Version

**AI-powered daily assistant** - Enhanced for Shopifolk

Task management system using Claude in Cursor IDE. Automate daily planning, meeting notes, and weekly reviews **with full Shopify integration**.

> *Bradán* (Irish: "salmon") - Like the legendary Salmon of Knowledge, Bradán brings instant clarity to your workday.

---

## 🎯 Shopify-Specific Features

This internal version includes:

### Full Shopify MCP Integration
- ✅ **Vault** - Search projects, people, products, missions
- ✅ **Slack** - Full message reading & prioritization  
- ✅ **Data Portal** - Query Shopify DW from Cursor
- ✅ **Revenue MCP** - Salesforce, Salesloft, account enrichment
- ✅ **Support Core** - Merchant data & ticket search
- ✅ **Dev MCP** - Shopify dev environment tools
- ✅ **Vault Set Search** - Internal documentation search

### vs. Public Version
The [public version](https://github.com/eamonbrett/bradan) works great but requires manual Slack MCP setup and doesn't include Vault, data access, or CRM integration.

**This version is optimized for Shopifolk** with access to internal tools.

---

## Quick Start

**Setup:** 15 minutes | **Daily use:** 5 minutes | **Time saved:** ~65 hours/year

### Prerequisites
- [Cursor IDE](https://cursor.com) - Required
- Python 3.8+
- Google Workspace (Shopify account)
- Access to Shopify MCP servers

### Install

```bash
git clone https://github.com/eamonbrett/bradan.git
cd bradan
git checkout shopify-internal
pip install -r requirements.txt
```

See [SETUP-SHOPIFY.md](SETUP-SHOPIFY.md) for complete installation.

### Try It

After setup, ask Claude in Cursor:
```
"Good morning"
```

You'll get a daily file with:
- Your Google Calendar
- Slack messages (last 24h, prioritized)
- Gmail priority inbox
- Meeting notes (with Gemini transcriptions)
- Top 3 tasks for the day

---

## Shopify Workflows

### Daily Morning (5 min)
```
"Good morning"
```

**What you get:**
- Calendar with Gemini meeting notes auto-linked
- Slack messages from last 24h (P1-P4 prioritized)
- Gmail priority inbox
- Top 3 tasks
- Meeting stubs pre-filled

### Search Vault
```
"Search Vault for projects about Plus"
"Who owns the Checkout product?"
"Find latest posts from Tobi"
```

### Query Data
```
"Query Shopify data: top 10 Plus merchants by GMV"
"Show me POS adoption in retail vertical"
```

### CRM Lookup
```
"Find Salesforce account for Allbirds"
"Show me my book of business"
"Search Salesloft for calls with [merchant]"
```

### Support Context
```
"Search tickets for shop domain example.myshopify.com"
"Find merchant by email merchant@example.com"
```

### Weekly Review (Friday, 3 min)
```
"Archive this week"
```

**Auto-extracts:**
- Weekly accomplishments
- Action items
- Decision logs
- Sends Slack summary (optional)

---

## Key Commands

| Say to Claude | What Happens |
|---------------|--------------|
| "Good morning" | Full morning setup with Shopify integrations |
| "Show me my priority inbox" | Email + Slack prioritized together |
| "Search Vault for X" | Find Vault projects, people, docs |
| "Query Shopify data: X" | Run BigQuery via Data Portal |
| "Find Salesforce account for X" | Search CRM with context |
| "Generate this week's file" | Weekly planning |
| "Archive this week" | Weekly review + archive |
| "Create decision log about X" | Document decision |

---

## Folder Structure

```
task-management/
├── work/              # Active work
│   ├── daily/         # Daily files (auto-generated)
│   ├── weeks/         # Weekly plans
│   ├── meetings/      # Meeting notes (Gemini auto-populated)
│   └── projects/      # Project tracking
├── reference/         # Reference materials
│   └── decisions/     # Decision logs
├── archive/           # Historical files (auto-archived)
├── system/            # System files
│   ├── automation/    # Python scripts + Shopify workflows
│   ├── memory/        # AI context (customize for your role)
│   └── templates/     # Templates (customize as needed)
└── inbox/             # Temporary staging
```

---

## Daily Workflow

### Morning (5 min)
1. Open Cursor in this folder
2. Say: `"Good morning"`
3. Review your generated daily file:
   - Calendar events with meeting notes
   - Slack priority inbox
   - Gmail priority inbox
   - Top 3 tasks

### During Day
- Work through Top 3 tasks
- Check off completed: `- [x]`
- Add notes as you go
- Meeting notes auto-populate from Gemini

### Evening (3 min)
- Quick review
- Incomplete items carry forward tomorrow

---

## Weekly Workflow

### Monday (2 min)
```
"Generate this week's file"
```

### Friday (3 min)
```
"Archive this week"
```

Optionally sends Slack summary to your team!

---

## MCP Servers Included

| MCP | What It Does | Documentation |
|-----|--------------|---------------|
| **vault-mcp** | Search Vault (projects, people, products, posts) | vault.shopify.io/mcp |
| **playground-slack-mcp** | Read & send Slack messages | @shopify-internal/slack-mcp |
| **gworkspace-mcp** | Calendar, Gmail, Drive | Public MCP |
| **data-portal-mcp** | Query Shopify DW (BigQuery) | data.shopify.io |
| **revenue-mcp** | Salesforce, Salesloft, enrichment | revenue-funnel.shopify.io |
| **support-core** | Ticket search, merchant data | support.shopify.io/internal |
| **dev-mcp** | Shopify dev environment tools | /opt/dev/bin/devx |
| **vault-set-search** | Search internal documentation | vault.shopify.io |

See [SETUP-SHOPIFY.md](SETUP-SHOPIFY.md) for configuration details.

---

## Customization

### Templates
Edit `system/templates/`:
- `daily.md` - Daily file format
- `meeting-v2.md` - Meeting notes (Gemini notes auto-populate)
- `weekly.md` - Weekly planning
- `decision.md` - Decision logs

### Memory Bank
Customize `system/memory/` for your context:
- `activeContext.md` - Your current priorities, team, projects
- `projectbrief.md` - Your mandate and goals
- `systemPatterns.md` - Your workflow preferences

**Tip:** Add your:
- Direct reports
- Key stakeholders  
- Active projects
- Reporting structure

This gives Claude full context when generating your daily files!

### Settings
Adjust `system/automation/config.py`:
- Timezone
- File paths
- Calendar preferences

---

## Why This Works at Shopify

### vs Todo Apps
- No context switching (already in IDE/Cursor)
- AI has Shopify context (Vault, data, CRM)
- Files are portable and version-controlled

### vs Notion/Jira
- No manual organizing (AI handles it)
- Shopify data integrated (query DW directly)
- Calendar + Slack + Email in one place

### vs Paper
- Searchable history
- Automatic Shopify context
- Multi-computer sync
- AI understands your work

---

## What You Get

**Time Savings:**
- 15 min/day on planning
- 30 min/week on reviews
- ~65 hours/year total

**Shopify Integration:**
- Vault search in your daily context
- Slack + Email prioritized together
- Data queries from daily file
- CRM context when needed
- Support lookups instant

**Quality Improvements:**
- Better focus (Top 3 clarity)
- Complete context (Shopify data integrated)
- Fewer missed tasks
- Better decisions (documented with Vault context)

---

## Documentation

- **[SETUP-SHOPIFY.md](SETUP-SHOPIFY.md)** - Complete 15-minute setup guide
- **[QUICK_START.md](QUICK_START.md)** - One-page reference
- **[COMPATIBILITY.md](COMPATIBILITY.md)** - Public vs Shopify version comparison

---

## Tech Stack

- **Cursor IDE** - AI-powered development
- **Claude (Anthropic)** - AI assistant
- **Shopify MCP Servers** - Vault, Slack, Data, Revenue, Support
- **Google Workspace MCP** - Calendar, Gmail, Drive
- **Python 3.8+** - Automation scripts
- **Markdown** - File format

---

## Share with Teammates

Your colleagues with Shopify MCP access can use this:

```bash
git clone https://github.com/eamonbrett/bradan.git
cd bradan
git checkout shopify-internal
pip install -r requirements.txt
```

Then follow [SETUP-SHOPIFY.md](SETUP-SHOPIFY.md)!

---

## Privacy & Security

**This branch:**
- Contains Shopify-internal MCP configurations
- Should remain in **private** repository
- Includes sample MCP tokens (update with your own)

**No sensitive data in git:**
- Daily files are `.gitignore`d by default
- Meeting notes excluded
- Personal context excluded

See `.gitignore` for full exclusions.

---

## License

Use freely for personal or team productivity within Shopify.

---

**Ready to start?** → [SETUP-SHOPIFY.md](SETUP-SHOPIFY.md)

**Questions?** Ask in #team-productivity or DM @eamonbrett

