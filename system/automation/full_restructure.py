#!/usr/bin/env python3
"""
Full Task Management Restructure
Creates clean 5-folder structure: work/, reference/, archive/, system/, inbox/

Run with: python3 automation/full_restructure.py --dry-run
Then: python3 automation/full_restructure.py --execute
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class Restructure:
    def __init__(self, base_dir=None, dry_run=True):
        self.base = Path(base_dir) if base_dir else Path.cwd()
        self.dry_run = dry_run
        self.moves = []
        self.log = []
        
    def log_action(self, action):
        """Log an action."""
        self.log.append(action)
        print(f"  {action}")
    
    def mkdir(self, path):
        """Create directory."""
        full_path = self.base / path
        if self.dry_run:
            self.log_action(f"mkdir -p {path}")
        else:
            full_path.mkdir(parents=True, exist_ok=True)
            self.log_action(f"✅ Created {path}")
    
    def mv(self, src, dst):
        """Move file or directory."""
        src_path = self.base / src
        dst_path = self.base / dst
        
        if not src_path.exists():
            self.log_action(f"⚠️  Skip {src} (doesn't exist)")
            return
        
        if self.dry_run:
            self.log_action(f"mv {src} → {dst}")
        else:
            # Ensure destination parent exists
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dst_path))
            self.log_action(f"✅ Moved {src} → {dst}")
    
    def flatten_meetings(self):
        """Flatten meeting subdirectories to chronological structure."""
        meetings_dir = self.base / "work" / "meetings"
        
        if self.dry_run:
            self.log_action("Flatten meetings subdirectories:")
            subdirs = ["1-on-1s", "logistics", "projects", "recurring"]
            for subdir in subdirs:
                self.log_action(f"  mv work/meetings/{subdir}/*.md → work/meetings/")
            return
        
        # Move files from subdirectories to main meetings folder
        subdirs = ["1-on-1s", "logistics", "projects", "recurring"]
        for subdir in subdirs:
            subdir_path = meetings_dir / subdir
            if subdir_path.exists():
                for file in subdir_path.glob("*.md"):
                    dest = meetings_dir / file.name
                    if dest.exists():
                        # Add subdir prefix if name collision
                        dest = meetings_dir / f"{subdir}-{file.name}"
                    shutil.move(str(file), str(dest))
                    self.log_action(f"✅ Moved {file.name} to meetings/")
                
                # Remove empty subdirectory
                try:
                    subdir_path.rmdir()
                    self.log_action(f"✅ Removed empty {subdir}/")
                except:
                    self.log_action(f"⚠️  {subdir}/ not empty, keeping")
    
    def run(self):
        """Execute full restructure."""
        print("\n" + "="*60)
        if self.dry_run:
            print("DRY RUN - No changes will be made")
        else:
            print("EXECUTING RESTRUCTURE")
        print("="*60 + "\n")
        
        # Phase 1: Create new top-level structure
        print("Phase 1: Create new top-level folders\n")
        self.mkdir("work")
        self.mkdir("reference")
        self.mkdir("system")
        print()
        
        # Phase 2: Move to work/
        print("Phase 2: Move active work to work/\n")
        self.mv("daily", "work/daily")
        self.mv("weeks", "work/weeks")
        self.mv("meetings", "work/meetings")
        self.mv("projects", "work/projects")
        print()
        
        # Phase 3: Flatten meetings
        if not self.dry_run:
            print("Phase 3: Flatten meeting subdirectories\n")
            self.flatten_meetings()
            print()
        else:
            print("Phase 3: Flatten meeting subdirectories\n")
            self.flatten_meetings()
            print()
        
        # Phase 4: Move to reference/
        print("Phase 4: Move reference materials to reference/\n")
        self.mv("decisions", "reference/decisions")
        self.mv("career-development", "reference/career")
        self.mv("analysis", "reference/analysis")
        self.mv("docs", "reference/docs")
        self.mv("actions", "reference/actions")
        print()
        
        # Phase 5: Move to system/
        print("Phase 5: Move system files to system/\n")
        self.mv("automation", "system/automation")
        self.mv("memory-bank", "system/memory")
        self.mkdir("system/templates")
        
        # Move templates to system/templates
        if (self.base / "work" / "daily" / "template-daily-v2.md").exists():
            self.mv("work/daily/template-daily-v2.md", "system/templates/daily.md")
        if (self.base / "reviews" / "template-weekly-review-enhanced.md").exists():
            self.mv("reviews/template-weekly-review-enhanced.md", "system/templates/weekly.md")
        print()
        
        # Phase 6: Organize remaining folders
        print("Phase 6: Organize remaining folders\n")
        # Keep inbox at root (temporary by nature)
        # Keep archive at root (historical by nature)
        
        # Move weekly-summaries to archive (historical Gemini notes)
        self.mv("weekly-summaries", "archive/weekly-summaries")
        
        # Clean up empty reviews folder
        if (self.base / "reviews").exists():
            self.mv("reviews/template-monthly-review.md", "system/templates/monthly.md")
            self.mv("reviews", "archive/reviews-old")
        print()
        
        # Phase 7: Update README
        print("Phase 7: Update documentation\n")
        if not self.dry_run:
            self.update_readme()
        else:
            self.log_action("Update README.md with new structure")
        print()
        
        # Summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60 + "\n")
        
        if self.dry_run:
            print("This was a DRY RUN - no changes were made.")
            print("\nTo execute: python3 automation/full_restructure.py --execute")
        else:
            print("✅ Restructure complete!")
            print("\nNew structure:")
            print("  work/          - Active work (daily, weeks, meetings, projects)")
            print("  reference/     - Reference materials (decisions, career, analysis)")
            print("  archive/       - Historical files")
            print("  system/        - Automation & configuration")
            print("  inbox/         - Temporary (Slack summaries)")
            
            # Save log
            log_file = self.base / "docs" / "system-updates" / f"restructure-log-{datetime.now().strftime('%Y-%m-%d-%H%M')}.txt"
            log_file.parent.mkdir(parents=True, exist_ok=True)
            log_file.write_text("\n".join(self.log))
            print(f"\n📝 Log saved: {log_file}")
        
        print()
    
    def update_readme(self):
        """Update README with new structure."""
        readme_path = self.base / "README.md"
        
        new_readme = """# Task Management System

**5-Folder Structure** - Clear, simple, effective

---

## 📂 Structure

```
task-management/
├── 📅 work/              # Active work (what you touch daily)
│   ├── daily/           # Daily files
│   ├── weeks/           # Weekly files (consolidated)
│   ├── meetings/        # Meeting notes (chronological)
│   └── projects/        # Active projects
│
├── 📚 reference/         # Reference materials (look up as needed)
│   ├── decisions/       # Decision logs (never archived)
│   ├── career/          # Career development
│   ├── analysis/        # Data analysis
│   ├── docs/            # Documentation
│   └── actions/         # Action items
│
├── 📦 archive/           # Historical files (searchable)
│   ├── daily/           # Old daily files (by week)
│   ├── deprecated/      # Old systems
│   └── ...
│
├── 🔧 system/            # System files (automation & config)
│   ├── automation/      # Python scripts
│   ├── memory/          # AI memory bank
│   └── templates/       # File templates
│
└── 📥 inbox/             # Temporary (auto-generated, auto-cleared)
    └── slack-priority-summary-*.md
```

---

## 🚀 Quick Start

### Daily Workflow
**Morning:** "Generate today's daily file"  
**Evening:** Check off completed tasks

### Weekly Workflow
**Monday (2 min):** "Generate this week's file" - Review carry-forwards  
**Friday (3 min):** "Update this week's file" - Answer 3 reflection questions

### Finding Things
- **Active work:** Check `work/`
- **Reference:** Check `reference/decisions/` or `reference/career/`
- **History:** Check `archive/daily/YYYY-MM-week-N/`
- **Automation:** Check `system/automation/`

---

## 📝 Key Commands

| Task | Command |
|------|---------|
| Daily file | "Generate today's daily file" |
| Weekly setup | "Generate this week's file" |
| Weekly reflection | "Update this week's file" |
| Archive week | "Archive week of [date]" |

---

## 📊 System Overview

**Time Investment:**
- Monday: 2 minutes (week setup)
- Daily: 10 minutes (planning & review)
- Friday: 3 minutes (reflection)
- **Total:** 5 minutes/week for planning

**Auto-Extraction:**
- Completed tasks from daily files
- Meeting outcomes and decisions
- Carry-forward items
- Priority patterns

**Documentation:**
- System guides: `reference/docs/`
- Implementation: `reference/docs/implementation/`
- System updates: `reference/docs/system-updates/`

---

## 🔄 Recent Updates

**November 10, 2025:**
- ✅ Consolidated weekly files (plan + summary + review → one file)
- ✅ Auto-extraction from daily work (90% automated)
- ✅ Simplified weekly review (3 questions, 10 minutes)
- ✅ Restructured folders (5 clear top-level folders)
- ✅ Flattened meetings (chronological, not categorized)

**Result:** 40 min/week saved, clearer structure, less toil

---

**Last Updated:** November 10, 2025
"""
        
        if readme_path.exists():
            # Backup old README
            backup = self.base / "archive" / "README-old.md"
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(str(readme_path), str(backup))
            self.log_action(f"✅ Backed up old README to archive/")
        
        readme_path.write_text(new_readme)
        self.log_action(f"✅ Updated README.md")


def main():
    import sys
    
    dry_run = "--execute" not in sys.argv
    
    restructure = Restructure(dry_run=dry_run)
    restructure.run()


if __name__ == "__main__":
    main()

