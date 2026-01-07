# Backup Strategy - Don't Lose Your Context

**Goal:** Switch laptops without losing any work or context.

---

## Option 1: Private GitHub Repo (Recommended) ⭐

**Best for:** Version control + cloud backup + easy sync

### Setup (10 min)

**1. Create Private Repo**
```bash
cd ~/Documents/task-management
git init
```

Go to GitHub → New Repository → **Make it PRIVATE** → Create

```bash
git remote add origin git@github.com:YOUR-USERNAME/my-task-management.git
```

**2. Create .gitignore**
```bash
cat > .gitignore << 'EOF'
# Logs and temp files
*.log
__pycache__/
.DS_Store

# Optional: Exclude very personal files
# daily/2025-*.md  # Uncomment if you want to keep dailies local only
# meetings/2025-*.md
EOF
```

**3. Backup Everything**
```bash
git add .
git commit -m "Initial backup"
git push -u origin main
```

### Daily Backup (Automatic with Cursor)

Cursor can auto-commit for you, or just run occasionally:

```bash
git add .
git commit -m "Backup $(date +%Y-%m-%d)"
git push
```

### New Laptop Setup (5 min)

```bash
git clone git@github.com:YOUR-USERNAME/my-task-management.git
cd my-task-management
pip install -r requirements.txt
# Configure MCP in Cursor (copy from old laptop's ~/.cursor/mcp.json)
```

**Done! All your context restored.**

---

## Option 2: Google Drive Sync (Simplest)

**Best for:** Non-technical, automatic sync, no git knowledge needed

### Setup (5 min)

**1. Move to Google Drive**
```bash
mv ~/Documents/task-management ~/Google\ Drive/My\ Drive/task-management
```

**2. Create Symlink (so Cursor still finds it)**
```bash
ln -s ~/Google\ Drive/My\ Drive/task-management ~/Documents/task-management
```

**3. Enable Google Drive Desktop**

Download from: [google.com/drive/download](https://google.com/drive/download)

### New Laptop Setup (2 min)

1. Install Google Drive Desktop
2. Let it sync
3. Files appear automatically in `~/Google Drive/My Drive/task-management`
4. Create symlink: `ln -s ~/Google\ Drive/My\ Drive/task-management ~/Documents/task-management`

**Done! Automatic backup forever.**

---

## Option 3: Both (Maximum Protection)

**Best for:** Paranoid (in a good way!)

**Use GitHub for:** Code, templates, automation scripts  
**Use Google Drive for:** Daily files, meetings, personal context

### Setup

1. Follow Option 1 (GitHub) with this `.gitignore`:
```
# Only backup structure, not personal files
daily/*.md
!daily/template-*.md
meetings/*.md
!meetings/template-*.md
decisions/*.md
!decisions/template-*.md
reviews/*.md
!reviews/template-*.md
inbox/*.md
archive/
*.log
```

2. Separately backup personal files to Drive:
```bash
# Create backup folder in Drive
mkdir -p ~/Google\ Drive/My\ Drive/task-mgmt-personal

# Copy personal files
cp -r daily/*.md ~/Google\ Drive/My\ Drive/task-mgmt-personal/daily/
cp -r meetings/*.md ~/Google\ Drive/My\ Drive/task-mgmt-personal/meetings/
cp -r decisions/*.md ~/Google\ Drive/My\ Drive/task-mgmt-personal/decisions/
```

**Result:**
- GitHub has system (templates, automation, memory-bank)
- Google Drive has your daily work
- Can restore everything on new laptop

---

## What to Backup

### ✅ Always Backup
- `daily/` - All your daily files
- `meetings/` - All meeting notes
- `decisions/` - Decision logs
- `reviews/` - Weekly/monthly reviews
- `memory-bank/` - Your context (important!)
- `automation/` - Your scripts
- `weekly-plans/`, `weekly-summaries/`
- All template files

### ⚠️ Optional (Can Recreate)
- `inbox/` - Priority inbox summaries (ephemeral)
- `archive/` - Already archived, low priority

### ❌ Don't Need to Backup
- `__pycache__/`, `*.log` - Generated files
- `.DS_Store` - System files

---

## Quick Comparison

| Method | Setup Time | Auto-Sync | Version Control | Privacy |
|--------|------------|-----------|-----------------|---------|
| **Private GitHub** | 10 min | Manual/Automated | ✅ Yes | ✅ Private |
| **Google Drive** | 5 min | ✅ Automatic | ❌ No | ✅ Private |
| **Both** | 15 min | Partial | ✅ Yes | ✅ Private |

---

## Recommended: Private GitHub

**Why:**
- Version control (see what changed when)
- Works from any laptop
- Can roll back mistakes
- Easy to share with new laptop

**Setup:**
```bash
# One time (10 min)
git init
# Create private repo on GitHub
git remote add origin YOUR-PRIVATE-REPO
git add .
git commit -m "Initial backup"
git push -u origin main

# Ongoing (30 sec, whenever you want)
git add .
git commit -m "Backup"
git push
```

**Recovery on new laptop:**
```bash
git clone YOUR-PRIVATE-REPO
# Done! Everything restored.
```

---

## Emergency Recovery

### Lost your laptop?

**If using GitHub:**
1. Clone repo on new laptop
2. Reconfigure MCP in Cursor
3. All context intact ✅

**If using Google Drive:**
1. Install Drive Desktop
2. Let it sync
3. All context intact ✅

**If using neither:**
- Everything is gone 😢
- Set up backup NOW

---

## Automation (Optional)

### Auto-commit every day

Add to `automation/backup.sh`:
```bash
#!/bin/bash
cd ~/Documents/task-management
git add .
git commit -m "Auto backup $(date +%Y-%m-%d)" || true
git push || true
```

Run daily:
```bash
chmod +x automation/backup.sh
# Add to crontab: 0 18 * * * ~/Documents/task-management/automation/backup.sh
```

Or just use Google Drive Desktop (automatic!).

---

## Test Your Backup

**Do this now (5 min):**

1. Create backup (GitHub or Drive)
2. Create test file: `echo "test" > test-backup.txt`
3. Push/sync it
4. Delete local file: `rm test-backup.txt`
5. Pull/sync from backup
6. Verify file returns ✅

**If test works, your real backup will work!**

---

## My Recommendation

**For you:** Private GitHub repo

**Steps:**
1. Create private GitHub repo (2 min)
2. Add `.gitignore` (1 min)
3. Initial commit + push (2 min)
4. Push updates weekly (or when switching laptops)

**Result:** Never lose your context again. Switch laptops in 5 minutes.

---

**Pick one method and set it up today. Future you will thank you!** 🙏

