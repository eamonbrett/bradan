# Bradán - Compatibility Guide

**For users outside of Shopify:** This system is fully compatible with standard tools!

---

## ✅ Works Out-of-the-Box

The core system requires only **publicly available tools**:

### Required
- **Cursor IDE** - [cursor.com](https://cursor.com) (Free or Pro)
- **Python 3.8+** - Standard Python installation
- **Google Workspace** - Personal or business Gmail account

### MCP Server (Public)
- **gworkspace-mcp** - `github:aaronsb/google-workspace-mcp`
  - Provides: Calendar, Gmail, Drive access
  - Fully open source and free
  - No Shopify dependencies

---

## ⚙️ Optional Enhancements

### Gemini (Google Workspace Add-on)
- **What it does:** Automated meeting transcription
- **Cost:** Google Workspace add-on ($30/user/month)
- **Status:** Standard Google product, works for anyone
- **Bradán support:** Built-in Drive integration reads Gemini notes

### Slack Integration
- **What it does:** Slack message prioritization
- **Status:** Requires custom MCP setup
- **Options:**
  1. Build your own Slack MCP server (Slack API is public)
  2. Wait for community MCP servers
  3. Use without Slack (system works great with just email)

---

## 🚫 Not Included (Shopify-Internal Only)

The following were removed from the public release:

- **Vault MCP** - Internal Shopify tool
- **Revenue MCP** - Internal Shopify tool
- **Support Core MCP** - Internal Shopify tool
- **Data Portal MCP** - Internal Shopify tool
- **Playground Slack MCP** - Internal Shopify Slack server

**Impact:** None. These were optional features used by the original author at Shopify. The core system works perfectly without them.

---

## 📊 Feature Compatibility

| Feature | Public Version | Notes |
|---------|----------------|-------|
| Daily file generation | ✅ Full | Works with Google Calendar |
| Meeting stubs | ✅ Full | Google Calendar integration |
| Gmail prioritization | ✅ Full | Via gworkspace-mcp |
| Gemini meeting notes | ✅ Full | Standard Google Workspace |
| Weekly archival | ✅ Full | Pure Python automation |
| Decision logging | ✅ Full | Markdown files |
| Slack integration | ⚠️ Partial | Requires custom MCP setup |
| Mobile notifications | ⚠️ Optional | Via Slack (if configured) |

---

## 🎯 What You Get

**With just Cursor + Google Workspace:**
- ✅ "Good morning" command
- ✅ Calendar integration
- ✅ Gmail reading & prioritization
- ✅ Meeting note automation
- ✅ Daily/weekly planning
- ✅ Archive system
- ✅ Decision logs
- ✅ All Python automation

**Optional additions:**
- Gemini for meeting transcription
- Slack integration (DIY or wait for community MCPs)

---

## 🚀 Getting Started

1. Install Cursor IDE
2. Clone this repo
3. Run `pip install -r requirements.txt`
4. Configure `~/.cursor/mcp.json` with gworkspace-mcp
5. Say "Good morning" to Claude

See [SETUP.md](SETUP.md) for detailed instructions.

---

**Bottom line:** This system is 100% compatible with public tools. No Shopify access required!

