# Export Checklist - Preparing Your System for Sharing

**Use this checklist before creating a GitHub template or ZIP file.**

---

## Pre-Export Steps (15 minutes)

### 1. Privacy Audit (5 min)

**Search for personal information:**
```bash
cd ~/Documents/task-management

# Find your email
grep -r "eamonbrett" . --exclude-dir=.git --exclude-dir=archive

# Find Shopify references
grep -r "shopify.com" . --exclude-dir=.git --exclude-dir=archive

# Find personal names
grep -r "Eamon" . --exclude-dir=.git --exclude-dir=archive
```

**Clean these files:**
- [ ] `system/automation/config.py` - Remove personal timezone, names
- [ ] `system/memory/*` - Genericize context files
- [ ] `README.md` - Remove company-specific references
- [ ] Any automation scripts with hardcoded paths/emails

---

### 2. File Structure Verification (3 min)

**Ensure these exist:**
- [ ] `system/templates/` - All 6 templates (daily, meeting-v2, decision, monthly, project, weekly)
- [ ] `system/automation/` - All Python scripts
- [ ] `system/memory/` - Generic memory bank files
- [ ] `requirements.txt` - Python dependencies
- [ ] `README.md` - System overview
- [ ] `.gitignore-TEMPLATE` - Ready to rename
- [ ] `SETUP_GUIDE.md` - From Sharing Template Package
- [ ] `HOW-I-USE-THIS.md` - From Sharing Template Package

---

### 3. Create Sample Files (5 min)

**Create these examples:**
```bash
# Sample daily file
cp work/daily/2026-01-07.md work/daily/2025-01-01-SAMPLE.md
# Edit to remove personal content, keep structure

# Sample meeting file
cp work/meetings/2026-01-07-emea-2026-kick-off.md work/meetings/2025-01-01-team-sync-SAMPLE.md
# Edit to remove personal content, keep structure

# Sample weekly file
cp work/weeks/2026-01-06-week-02.md work/weeks/2025-01-01-week-01-SAMPLE.md
# Edit to remove personal content, keep structure
```

---

### 4. Genericize Memory Bank (2 min)

**Edit these files to remove personal context:**

`system/memory/projectbrief.md`:
```markdown
# Task Management System

A Cursor-powered task management system using AI-assisted markdown files.

## Purpose
- Automate daily planning and weekly reviews
- Integrate calendar and communication tools
- Maintain searchable decision logs
```

`system/memory/activeContext.md`:
```markdown
# Active Context

## Current Focus
[User will customize this]

## Recent Changes
[User will customize this]

## Next Steps
[User will customize this]
```

`system/memory/productContext.md`:
```markdown
# Product Context

## What This System Does
- AI-assisted task management via Cursor IDE
- Automated daily file generation from calendar
- Weekly planning and review workflows
- Decision logging and meeting notes

## Core Workflows
1. Morning: "Good morning" command
2. Weekly: Generate and archive
3. Ad-hoc: Decision logs, meeting notes
```

---

## Export Methods

### Method 1: GitHub Template (Recommended) ⭐

**Steps:**
1. **Copy `.gitignore-TEMPLATE` to root:**
```bash
cp .gitignore-TEMPLATE .gitignore
```

2. **Initialize Git (if not already done):**
```bash
git init
```

3. **Stage files:**
```bash
git add .
git status  # Review what will be committed
```

4. **Create GitHub repository:**
   - Go to github.com → New Repository
   - Name: `cursor-task-management-template`
   - Make it **PUBLIC** (for template sharing) or **PRIVATE** (share link directly)
   - Enable "Template repository" in Settings → General

5. **Push files:**
```bash
git remote add origin git@github.com:YOUR-USERNAME/cursor-task-management-template.git
git commit -m "Initial template setup"
git push -u origin main
```

6. **Share link:**
   - Recipients click "Use this template" button
   - GitHub creates copy in their account
   - They follow `SETUP_GUIDE.md`

---

### Method 2: ZIP File

**Steps:**
1. **Create clean export directory:**
```bash
mkdir -p ~/Desktop/task-management-export
```

2. **Copy essential files:**
```bash
# Copy core structure
cp -r system/ ~/Desktop/task-management-export/
cp -r work/daily/2025-01-01-SAMPLE.md ~/Desktop/task-management-export/work/daily/
cp -r work/meetings/2025-01-01-team-sync-SAMPLE.md ~/Desktop/task-management-export/work/meetings/
cp -r work/weeks/2025-01-01-week-01-SAMPLE.md ~/Desktop/task-management-export/work/weeks/

# Copy docs
cp README.md ~/Desktop/task-management-export/
cp requirements.txt ~/Desktop/task-management-export/
cp .gitignore-TEMPLATE ~/Desktop/task-management-export/
cp work/projects/Sharing\ Template\ Package/SETUP_GUIDE.md ~/Desktop/task-management-export/
cp work/projects/Sharing\ Template\ Package/HOW-I-USE-THIS.md ~/Desktop/task-management-export/
cp work/projects/Sharing\ Template\ Package/sharing-template-quickstart.md ~/Desktop/task-management-export/
```

3. **Create ZIP:**
```bash
cd ~/Desktop
zip -r task-management-template.zip task-management-export/
```

4. **Share:**
   - Upload to Google Drive / Dropbox
   - Share link with `SETUP_GUIDE.md` instructions

---

## Post-Export Verification

**Test the export yourself:**

1. **Create test environment:**
```bash
# Simulate fresh install
mkdir ~/test-task-management
cd ~/test-task-management

# If GitHub: git clone YOUR-TEMPLATE-REPO
# If ZIP: unzip task-management-template.zip
```

2. **Follow SETUP_GUIDE.md exactly:**
   - Install requirements
   - Configure MCP
   - Edit config.py
   - Test with "Generate today's daily file"

3. **Verify:**
   - [ ] Daily file generates with calendar events
   - [ ] Templates are accessible
   - [ ] No personal data appears
   - [ ] All automation scripts work

---

## Distribution Options

### For Personal Use (e.g., home computer):
- **Use GitHub private repo** - Keep your work history
- Clone to home computer
- Customize `system/memory/` for personal projects

### For Sharing with Others:
- **Use GitHub public template** - Enable "Use this template" button
- Or provide ZIP file with `SETUP_GUIDE.md`
- Direct them to read `HOW-I-USE-THIS.md` first for inspiration

### For Teams:
- **GitHub organization template** - Centralized, version controlled
- Team members clone and customize
- Shared templates, individual daily work

---

## Quick Commands Summary

```bash
# Privacy audit
grep -r "YOUR-EMAIL" . --exclude-dir=.git
grep -r "YOUR-NAME" . --exclude-dir=.git

# Create samples
cp work/daily/YYYY-MM-DD.md work/daily/2025-01-01-SAMPLE.md

# Export via GitHub
cp .gitignore-TEMPLATE .gitignore
git init
git add .
git commit -m "Initial template"
git push origin main

# Export via ZIP
mkdir ~/Desktop/task-management-export
# ... copy files ...
zip -r task-management-template.zip task-management-export/
```

---

## What Recipients Need

**Minimum requirements:**
- Cursor IDE (free trial available)
- Python 3.8+
- Google Workspace account
- 30 minutes setup time

**What they get:**
- ✅ Automated daily planning
- ✅ Calendar integration
- ✅ Meeting note generation
- ✅ Decision logging system
- ✅ Weekly review workflows
- ✅ AI-assisted task management

---

**Estimated Time:**
- Privacy audit: 5 min
- File prep: 5 min
- Samples: 5 min
- Export: 5-10 min
- **Total: 20-25 minutes**

---

*Last Updated: January 7, 2026*

