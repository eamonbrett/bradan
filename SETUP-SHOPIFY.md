# Bradán Setup Guide - Shopify Internal

**AI-powered daily assistant** | Get running in 15 minutes with Shopify MCPs.

**For Shopifolk:** This version includes all Shopify-internal MCP servers for maximum productivity.

---

## 1. Install Dependencies (3 min)

```bash
pip install -r requirements.txt
```

---

## 2. Configure MCP (10 min)

### Shopify MCP Configuration

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "vault-mcp": {
      "type": "streamable-http",
      "url": "https://vault.shopify.io/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
      }
    },
    "gworkspace-mcp": {
      "type": "stdio",
      "command": "/opt/homebrew/bin/uvx",
      "args": ["gworkspace-mcp"]
    },
    "dev-mcp": {
      "type": "stdio",
      "command": "/opt/dev/bin/devx",
      "args": ["mcp"],
      "env": {}
    },
    "playground-slack-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@shopify-internal/slack-mcp@latest"],
      "env": {}
    },
    "data-portal-mcp": {
      "type": "stdio",
      "command": "/opt/homebrew/bin/uvx",
      "args": ["data-portal-mcp"],
      "env": {}
    },
    "vault-set-search": {
      "type": "stdio",
      "command": "/opt/homebrew/bin/npx",
      "args": [
        "--registry=https://npm.shopify.io/node/",
        "-y",
        "vault-set-mcp-ts"
      ],
      "env": {}
    },
    "support-core": {
      "type": "stdio",
      "command": "uvx",
      "args": ["shopify-mcp-bridge"],
      "env": {
        "MCP_TARGET_URL": "https://support.shopify.io/internal/mcp",
        "MCP_MINERVA_CLIENT_ID": "0oa1bpdvm5ia0Zzhs0x8"
      }
    },
    "revenue-mcp": {
      "type": "stdio",
      "command": "/opt/homebrew/bin/uvx",
      "args": ["shopify-mcp-bridge"],
      "env": {
        "MCP_TARGET_URL": "https://revenue-funnel.shopify.io/mcp",
        "MCP_MINERVA_CLIENT_ID": "0oa1ao6npm85AT2Hr0x8"
      }
    }
  }
}
```

### What Each MCP Does

| MCP | Purpose |
|-----|---------|
| **vault-mcp** | Search Vault for projects, people, docs |
| **gworkspace-mcp** | Calendar, Gmail, Drive access |
| **dev-mcp** | Shopify dev tooling |
| **playground-slack-mcp** | Slack message reading & prioritization |
| **data-portal-mcp** | Query Shopify data warehouse |
| **vault-set-search** | Search Shopify internal docs |
| **support-core** | Support ticket search & merchant data |
| **revenue-mcp** | Salesforce, Salesloft, account enrichment |

### Restart Cursor

**Important:** Quit and restart Cursor for MCP to load.

---

## 3. Configure Settings (2 min)

Edit `system/automation/config.py`:

```python
# Calendar settings
DEFAULT_TIMEZONE = "America/New_York"  # Or your timezone
CALENDAR_NAME = "primary"
```

---

## 4. Test It

Ask Claude in Cursor:

```
"Good morning"
```

**Success:** Daily file created with:
- ✅ Google Calendar events
- ✅ Slack messages (last 24h)
- ✅ Gmail prioritization
- ✅ Meeting stubs with Gemini notes

---

## Shopify-Specific Features

### Vault Integration
```
"Search Vault for projects related to checkout"
"Who owns the payments product?"
"Find the latest post from [person]"
```

### Slack Prioritization
The "Good morning" command automatically:
- Reads last 24h of Slack messages
- Prioritizes by P1-P4
- Includes in your daily Priority Inbox

### Data Portal
```
"Query Shopify data: top 10 merchants by GMV"
"Show me Plus adoption metrics"
```

### Revenue Tools
```
"Find Salesforce account for [company]"
"Show me my book of business"
"Search Salesloft for recent calls"
```

### Support Tools
```
"Search tickets for merchant email [email]"
"Find support history for shop [shop_id]"
```

---

## Key Commands (Shopify Version)

| Command | What It Does |
|---------|--------------|
| `"Good morning"` | Full setup: Calendar + Gmail + Slack + priorities |
| `"Show me my priority inbox"` | Email + Slack aggregated & prioritized |
| `"Search Vault for X"` | Find Vault resources |
| `"Query Shopify data: X"` | Run BigQuery via Data Portal |
| `"Find Salesforce account for X"` | Search CRM |
| `"Archive this week"` | Weekly review + archive |

---

## Advantages Over Public Version

**You get:**
- ✅ **Slack integration** - Full message reading & prioritization
- ✅ **Vault search** - Projects, people, docs in your daily context
- ✅ **Data access** - Query DW directly from Cursor
- ✅ **CRM integration** - Salesforce & Salesloft data
- ✅ **Support tools** - Merchant & ticket lookup
- ✅ **Dev tooling** - Shopify dev environment integration

**vs. Public version:**
- Public version works great but requires manual Slack MCP setup
- No Vault, data portal, or CRM integration in public version

---

## Gemini Meeting Notes

**Highly recommended** for Shopify meetings:

1. **Enable Google Meet recording** in your settings
2. **Gemini is already enabled** for Shopify Google Workspace
3. **Bradán automatically reads** meeting notes from Drive

After meetings, your meeting stub will auto-populate with Gemini's transcription summary!

---

## Backup (Recommended)

Push to private GitHub repo:

```bash
git remote add origin YOUR-PRIVATE-REPO
git push -u origin shopify-internal
```

**Note:** Keep this repo private - contains Shopify MCP configurations.

---

## Troubleshooting

### Slack not working
1. Check `playground-slack-mcp` is in `~/.cursor/mcp.json`
2. Restart Cursor
3. Test: `"Can you read my recent Slack messages?"`

### Vault not working
1. Check your Vault token in mcp.json
2. Visit vault.shopify.io to refresh token
3. Update Authorization header

### Data Portal errors
1. Ensure `data-portal-mcp` is installed
2. Check you're on Shopify network/VPN
3. Test: `"List available datasets"`

### Revenue MCP issues
1. Check Minerva auth
2. Ensure shopify-mcp-bridge is installed: `uvx shopify-mcp-bridge`
3. Test: `"Get my Salesforce identity"`

---

## Next Steps

1. **Use "Good morning" daily** - See the Shopify integrations in action
2. **Explore Vault search** - Ask about projects, people, products
3. **Try data queries** - Query the DW directly from your daily file
4. **Priority inbox** - See Slack + email together
5. **Share with teammates** - This setup works for any Shopifolk!

---

## Share with Colleagues

Send them:
```
git clone https://github.com/eamonbrett/bradan.git
cd bradan
git checkout shopify-internal
```

Then follow this setup guide!

---

**You're ready!** Start tomorrow with: `"Good morning"`

For Shopify-specific questions, ask Claude about Vault, data portal, or revenue tools!

