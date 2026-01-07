#!/usr/bin/env python3
"""
Weekly Archival Workflow
Consolidates daily files into weekly reviews and archives past week's dailies.

Usage:
    From Cursor, Claude calls this script with:
    - week_start_date: ISO format date (YYYY-MM-DD) for start of week to archive
    - daily_files: List of daily file paths from that week
    - weekly_summary_path: Path to weekly summary file (for action items)
    
Example:
    python automation/weekly_archival.py --week-start 2025-10-28
"""

import os
import shutil
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import json


class WeeklyArchival:
    """Manages weekly archival of daily files and context extraction"""
    
    def __init__(self, workspace_root: str = None):
        self.workspace_root = Path(workspace_root or os.getcwd())
        self.daily_dir = self.workspace_root / "work" / "daily"
        self.archive_dir = self.workspace_root / "archive" / "daily"
        self.reviews_dir = self.workspace_root / "work" / "weeks"  # Now uses consolidated weeks
        self.context_dir = self.workspace_root / "work"  # Active context in work folder
        self.meetings_dir = self.workspace_root / "work" / "meetings"
        self.meetings_archive_dir = self.workspace_root / "archive" / "meetings"
        
        # Ensure directories exist
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.reviews_dir.mkdir(parents=True, exist_ok=True)
        self.context_dir.mkdir(parents=True, exist_ok=True)
        self.meetings_archive_dir.mkdir(parents=True, exist_ok=True)
    
    def get_week_number(self, date: datetime) -> int:
        """Get ISO week number for a date"""
        return date.isocalendar()[1]
    
    def get_week_identifier(self, date: datetime) -> str:
        """Generate week identifier: YYYY-MM-week-WW"""
        year = date.year
        month = date.strftime("%m")
        week = self.get_week_number(date)
        return f"{year}-{month}-week-{week:02d}"
    
    def find_daily_files_for_week(self, week_start: datetime) -> List[Path]:
        """Find all daily files for a given week (Mon-Fri)"""
        daily_files = []
        
        for i in range(7):  # Check all 7 days
            day = week_start + timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d")
            
            # Check for both possible formats
            file_patterns = [
                self.daily_dir / f"{date_str}.md",
                self.daily_dir / f"{date_str}-*.md"  # Handle files like 2025-11-05-tuesday.md
            ]
            
            for pattern in file_patterns:
                if '*' in str(pattern):
                    # Use glob for wildcard patterns
                    for file in self.daily_dir.glob(pattern.name):
                        if file.is_file():
                            daily_files.append(file)
                elif pattern.exists():
                    daily_files.append(pattern)
        
        return sorted(set(daily_files))  # Remove duplicates and sort
    
    def extract_daily_highlights(self, daily_file: Path) -> Dict[str, any]:
        """Extract key information from a daily file"""
        if not daily_file.exists():
            return None
        
        content = daily_file.read_text()
        
        # Extract date from filename
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', daily_file.name)
        date_str = date_match.group(1) if date_match else "Unknown"
        date = datetime.strptime(date_str, "%Y-%m-%d")
        day_name = date.strftime("%A")
        
        highlights = {
            'date': date_str,
            'day_name': day_name,
            'file': daily_file.name,
            'top_3': [],
            'meetings': [],
            'key_updates': [],
            'follow_ups': []
        }
        
        # Extract Top 3 priorities
        top_3_section = re.search(r'## Top 3 Priorities\s+(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if top_3_section:
            priorities = re.findall(r'###\s+\d+\.\s+(.+?)(?=\n###|\n##|\Z)', top_3_section.group(1), re.DOTALL)
            for priority in priorities[:3]:
                # Get just the title (first line)
                title = priority.strip().split('\n')[0].strip()
                highlights['top_3'].append(title)
        
        # Extract meetings (from Calendar Overview)
        meeting_pattern = r'-\s+\*\*(\d{2}:\d{2}(?:-\d{2}:\d{2})?)\*\*\s+\|\s+([^\n]+)'
        meetings = re.findall(meeting_pattern, content)
        highlights['meetings'] = [{'time': time, 'title': title.strip()} for time, title in meetings]
        
        # Extract key updates section
        updates_section = re.search(r'## Key Updates.*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if updates_section:
            # Get first few bullet points
            bullets = re.findall(r'^-\s+(.+)$', updates_section.group(1), re.MULTILINE)
            highlights['key_updates'] = bullets[:5]  # Top 5 updates
        
        # Extract follow-up items
        followup_section = re.search(r'## Follow-Up Items.*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if followup_section:
            bullets = re.findall(r'^-\s+\[\s*\]\s+(.+)$', followup_section.group(1), re.MULTILINE)
            highlights['follow_ups'] = bullets[:5]  # Top 5 follow-ups
        
        return highlights
    
    def generate_daily_highlights_section(self, week_highlights: List[Dict]) -> str:
        """Generate markdown section with daily highlights"""
        if not week_highlights:
            return ""
        
        section = "## 📅 Daily Highlights This Week\n\n"
        
        for day in week_highlights:
            if not day:
                continue
                
            section += f"### {day['day_name']} ({day['date']})\n"
            
            # Top 3
            if day['top_3']:
                section += "**Priorities:**\n"
                for priority in day['top_3']:
                    section += f"- {priority}\n"
            
            # Meetings
            if day['meetings']:
                section += f"\n**Meetings:** {len(day['meetings'])} meetings\n"
                for meeting in day['meetings'][:3]:  # Show top 3 meetings
                    section += f"- {meeting['time']} - {meeting['title']}\n"
            
            # Key Updates
            if day['key_updates']:
                section += "\n**Key Updates:**\n"
                for update in day['key_updates'][:2]:  # Top 2 updates
                    section += f"- {update}\n"
            
            section += f"\n**Daily File:** [[archive/daily/{self.get_week_identifier(datetime.strptime(day['date'], '%Y-%m-%d'))}/{day['file']}]]\n"
            section += "\n---\n\n"
        
        return section
    
    def archive_week(self, week_start: datetime, dry_run: bool = False) -> Dict:
        """
        Archive a week's daily files and extract highlights
        
        Args:
            week_start: Start date of the week (Monday)
            dry_run: If True, don't actually move files, just report what would happen
        
        Returns:
            Dict with archive summary
        """
        week_id = self.get_week_identifier(week_start)
        week_archive_dir = self.archive_dir / week_id
        
        # Find all daily files for this week
        daily_files = self.find_daily_files_for_week(week_start)
        
        if not daily_files:
            return {
                'success': False,
                'message': f'No daily files found for week starting {week_start.strftime("%Y-%m-%d")}',
                'files_archived': 0
            }
        
        # Extract highlights from each daily file
        week_highlights = []
        for daily_file in daily_files:
            highlights = self.extract_daily_highlights(daily_file)
            if highlights:
                week_highlights.append(highlights)
        
        # Create archive directory
        if not dry_run:
            week_archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Move files to archive
        archived_files = []
        for daily_file in daily_files:
            dest = week_archive_dir / daily_file.name
            
            if dry_run:
                archived_files.append(str(daily_file.relative_to(self.workspace_root)))
            else:
                shutil.move(str(daily_file), str(dest))
                archived_files.append(str(dest.relative_to(self.workspace_root)))
        
        return {
            'success': True,
            'week_id': week_id,
            'week_start': week_start.strftime("%Y-%m-%d"),
            'week_end': (week_start + timedelta(days=6)).strftime("%Y-%m-%d"),
            'files_archived': len(archived_files),
            'archived_files': archived_files,
            'archive_location': str(week_archive_dir.relative_to(self.workspace_root)),
            'highlights': week_highlights,
            'dry_run': dry_run
        }
    
    def generate_enhanced_weekly_review(self, week_start: datetime, highlights: List[Dict], 
                                       weekly_summary_path: Optional[str] = None) -> str:
        """
        Generate enhanced weekly review content with daily highlights
        
        Args:
            week_start: Start date of week
            highlights: List of daily highlights dicts
            weekly_summary_path: Path to weekly summary file (for action items)
        
        Returns:
            Markdown content for enhanced weekly review
        """
        week_end = week_start + timedelta(days=6)
        friday = week_start + timedelta(days=4)
        next_week_start = week_start + timedelta(days=7)
        
        # Load template
        template_path = self.workspace_root / "system" / "templates" / "weekly.md"
        if template_path.exists():
            template = template_path.read_text()
        else:
            template = "# Weekly Review - Week of [START_DATE]\n\n"
        
        # Replace placeholders
        content = template.replace("[START_DATE]", week_start.strftime("%Y-%m-%d"))
        content = content.replace("[FRIDAY_DATE]", friday.strftime("%A, %B %d, %Y"))
        content = content.replace("[NEXT_START_DATE]", next_week_start.strftime("%Y-%m-%d"))
        content = content.replace("[NEXT_START]", next_week_start.strftime("%Y-%m-%d"))
        
        # Add daily highlights section after the header section
        daily_highlights = self.generate_daily_highlights_section(highlights)
        
        # Insert after the initial links section
        if "---" in content:
            parts = content.split("---", 1)
            content = parts[0] + "---\n\n" + daily_highlights + parts[1]
        
        return content
    
    def update_active_context(self, week_highlights: List[Dict], week_start: datetime):
        """Update the rolling 2-week active context window"""
        context_file = self.context_dir / "active-context.md"
        
        # Generate current week summary
        current_week_content = f"## Current Week ({week_start.strftime('%b %d-%d')})\n\n"
        
        # Extract top priorities from highlights
        all_priorities = []
        all_meetings = []
        
        for day in week_highlights:
            if day and day.get('top_3'):
                all_priorities.extend(day['top_3'])
            if day and day.get('meetings'):
                all_meetings.extend([m['title'] for m in day['meetings']])
        
        # Deduplicate priorities
        unique_priorities = list(dict.fromkeys(all_priorities))[:5]
        
        current_week_content += "**Top Priorities:**\n"
        for priority in unique_priorities:
            current_week_content += f"- {priority}\n"
        
        current_week_content += f"\n**Meeting Activity:** {len(all_meetings)} meetings this week\n"
        
        # Create or update context file
        if context_file.exists():
            # Read existing, shift current week to previous week
            existing = context_file.read_text()
            
            # Extract current week section and move to previous week
            # This is a simplified version - would need more sophisticated parsing
            content = f"# Active Context - Last Updated: {datetime.now().strftime('%Y-%m-%d')}\n\n"
            content += current_week_content
            content += "\n## Previous Week\n"
            content += "[See previous week's review for details]\n"
        else:
            content = f"# Active Context - Last Updated: {datetime.now().strftime('%Y-%m-%d')}\n\n"
            content += current_week_content
        
        context_file.write_text(content)
        
        return str(context_file.relative_to(self.workspace_root))
    
    def archive_old_meetings(self, days_old: int = 30) -> Dict[str, any]:
        """
        Archive meetings older than specified days.
        
        Args:
            days_old: Archive meetings older than this many days (default: 30)
            
        Returns:
            Dictionary with stats and archived file paths
        """
        cutoff_date = datetime.now() - timedelta(days=days_old)
        archived_files = []
        
        # Find all dated meeting files in main meetings dir
        for meeting_file in self.meetings_dir.glob("????-??-??-*.md"):
            # Skip templates
            if "template" in meeting_file.name.lower():
                continue
                
            # Extract date from filename
            date_match = re.match(r'(\d{4}-\d{2}-\d{2})', meeting_file.name)
            if not date_match:
                continue
                
            meeting_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
            
            if meeting_date < cutoff_date:
                # Archive by month
                archive_month_dir = self.meetings_archive_dir / meeting_date.strftime("%Y-%m")
                archive_month_dir.mkdir(parents=True, exist_ok=True)
                
                # Move file
                dest = archive_month_dir / meeting_file.name
                shutil.move(str(meeting_file), str(dest))
                archived_files.append(str(dest))
        
        return {
            "archived_count": len(archived_files),
            "archived_files": archived_files,
            "cutoff_date": cutoff_date.strftime("%Y-%m-%d")
        }


def archive_week_command(week_start_str: str, dry_run: bool = False, 
                        weekly_summary_path: Optional[str] = None) -> Dict:
    """
    Command-line interface for weekly archival
    
    Args:
        week_start_str: Date string in YYYY-MM-DD format (Monday of week to archive)
        dry_run: If True, show what would happen without actually moving files
        weekly_summary_path: Optional path to weekly summary file
    
    Returns:
        Dict with archival results
    """
    try:
        week_start = datetime.strptime(week_start_str, "%Y-%m-%d")
        
        # Verify it's a Monday
        if week_start.weekday() != 0:
            # Adjust to the Monday of that week
            week_start = week_start - timedelta(days=week_start.weekday())
        
        archival = WeeklyArchival()
        
        # Archive the week
        result = archival.archive_week(week_start, dry_run=dry_run)
        
        if result['success']:
            # Generate enhanced weekly review
            review_content = archival.generate_enhanced_weekly_review(
                week_start, 
                result['highlights'],
                weekly_summary_path
            )
            
            # Save enhanced review
            if not dry_run:
                review_file = archival.reviews_dir / f"{week_start.strftime('%Y-%m-%d')}-week-{archival.get_week_number(week_start):02d}.md"
                review_file.write_text(review_content)
                result['review_file'] = str(review_file.relative_to(archival.workspace_root))
                
                # Update active context
                context_file = archival.update_active_context(result['highlights'], week_start)
                result['context_updated'] = context_file
                
                # Archive old meetings (>30 days)
                meeting_stats = archival.archive_old_meetings(days_old=30)
                result['meetings_archived'] = meeting_stats
        
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Archive weekly daily files')
    parser.add_argument('--week-start', required=True, help='Week start date (YYYY-MM-DD, Monday)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would happen without moving files')
    parser.add_argument('--weekly-summary', help='Path to weekly summary file')
    
    args = parser.parse_args()
    
    result = archive_week_command(args.week_start, args.dry_run, args.weekly_summary)
    
    print(json.dumps(result, indent=2))

