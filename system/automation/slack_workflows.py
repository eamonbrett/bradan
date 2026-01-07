#!/usr/bin/env python3
"""
Slack Workflow Integrations

This module provides high-level workflow functions that combine
task management operations with Slack notifications.

To be called from Cursor/Claude environment where MCP is available.
"""

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import sys

sys.path.insert(0, str(Path(__file__).parent))

from slack_notifier import (
    create_monday_morning_notification,
    create_action_reminder,
    create_friday_review_reminder,
    create_meeting_reminder
)


class SlackWorkflowIntegration:
    """High-level workflow integration with Slack notifications."""
    
    def __init__(self, project_root: Path = None):
        """Initialize workflow integration.
        
        Args:
            project_root: Root directory of the project
        """
        if project_root is None:
            project_root = Path(__file__).parent.parent
        
        self.project_root = project_root
        self.weekly_summaries_dir = project_root / "weekly-summaries"
        self.weekly_plans_dir = project_root / "weekly-plans"
        self.daily_dir = project_root / "daily"
    
    def monday_morning_workflow(self,
                                weekly_summary_file: str,
                                week_plan_file: str,
                                daily_file: str) -> Dict:
        """Generate Monday morning summary notification.
        
        This combines:
        - Full weekly summary overview
        - Top 3 priorities for the week
        - Action items extracted from meetings
        
        Args:
            weekly_summary_file: Filename of weekly summary (e.g., 'weekly-summary-2025-10-14.md')
            week_plan_file: Filename of week plan (e.g., 'week-2025-10-14.md')
            daily_file: Filename of daily file (e.g., '2025-10-14.md')
            
        Returns:
            Slack notification data dict
        """
        weekly_summary_path = str(self.weekly_summaries_dir / weekly_summary_file)
        week_plan_path = str(self.weekly_plans_dir / week_plan_file)
        daily_file_path = str(self.daily_dir / daily_file)
        
        return create_monday_morning_notification(
            weekly_summary_path,
            week_plan_path,
            daily_file_path
        )
    
    def extract_my_action_items(self, weekly_summary_path: Path, my_name: str = "Eamon") -> List[Dict[str, str]]:
        """Extract action items assigned to me from weekly summary.
        
        Args:
            weekly_summary_path: Path to weekly summary file
            my_name: My name to filter action items
            
        Returns:
            List of my action items with meeting context
        """
        if not weekly_summary_path.exists():
            return []
        
        try:
            with open(weekly_summary_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            actions = []
            
            # Look for action items by owner section
            import re
            
            # Find my section
            my_section = re.search(
                rf'### {my_name}\s*\n\n(.*?)(?=\n###|\n---|\Z)',
                content,
                re.DOTALL
            )
            
            if not my_section:
                return []
            
            section_text = my_section.group(1)
            
            # Extract meeting contexts and tasks
            current_meeting = None
            for line in section_text.split('\n'):
                line = line.strip()
                
                # Meeting header
                if line.startswith('**From:'):
                    current_meeting = line.replace('**From:', '').replace('**', '').strip()
                
                # Task item
                elif line.startswith('- [ ]'):
                    task = line.replace('- [ ]', '').strip()
                    actions.append({
                        'task': task,
                        'meeting': current_meeting or 'General',
                        'owner': my_name
                    })
            
            return actions
            
        except Exception as e:
            print(f"Error extracting action items: {e}")
            return []
    
    def send_action_reminders(self, weekly_summary_file: str, my_name: str = "Eamon") -> Dict:
        """Send DM reminder of my action items.
        
        Args:
            weekly_summary_file: Filename of weekly summary
            my_name: My name to filter actions
            
        Returns:
            Slack notification data dict
        """
        weekly_summary_path = self.weekly_summaries_dir / weekly_summary_file
        actions = self.extract_my_action_items(weekly_summary_path, my_name)
        
        if not actions:
            return None
        
        return create_action_reminder(actions, reminder_type="weekly")
    
    def send_friday_reminder(self) -> Dict:
        """Send Friday afternoon weekly review reminder.
        
        Returns:
            Slack notification data dict
        """
        return create_friday_review_reminder()
    
    def prepare_meeting_reminder(self,
                                 meeting_file_path: Path,
                                 minutes_before: int = 15) -> Optional[Dict]:
        """Prepare meeting reminder from meeting file.
        
        Args:
            meeting_file_path: Path to meeting note file
            minutes_before: Minutes before meeting to send reminder
            
        Returns:
            Slack notification data dict or None if can't prepare
        """
        if not meeting_file_path.exists():
            return None
        
        try:
            with open(meeting_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract meeting details
            import re
            
            # Title
            title_match = re.search(r'# Meeting: (.+)', content)
            title = title_match.group(1) if title_match else "Meeting"
            
            # Time
            time_match = re.search(r'\*\*Time:\*\* (.+)', content)
            time_str = time_match.group(1) if time_match else "Time TBD"
            
            # Attendees
            attendees_match = re.search(r'\*\*Attendees:\*\* (.+)', content)
            attendees_str = attendees_match.group(1) if attendees_match else ""
            attendees = [a.strip() for a in attendees_str.split(',') if a.strip()]
            
            # Location/Link
            location_match = re.search(r'\*\*Location:\*\* (.+)', content)
            location = location_match.group(1) if location_match else ""
            
            # Extract Google Meet link if in location
            meet_link = None
            if 'meet.google.com' in location:
                meet_match = re.search(r'(https://meet\.google\.com/[^\s\)]+)', location)
                if meet_match:
                    meet_link = meet_match.group(1)
            
            # Extract agenda items
            agenda_section = re.search(r'## Agenda\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
            agenda_items = []
            if agenda_section:
                for line in agenda_section.group(1).split('\n'):
                    line = line.strip()
                    if line and (line.startswith('-') or re.match(r'^\d+\.', line)):
                        # Clean up the line
                        item = re.sub(r'^[-\d.)\s]+', '', line).strip()
                        # Remove time allocation if present
                        item = re.sub(r'\s*-\s*\[.*?\]$', '', item)
                        if item:
                            agenda_items.append(item)
            
            # Extract prep items
            prep_section = re.search(r'\*\*My prep:\*\*\s*\n(.*?)(?=\n##|\n\*\*|\Z)', content, re.DOTALL)
            prep_items = []
            if prep_section:
                for line in prep_section.group(1).split('\n'):
                    line = line.strip()
                    if line.startswith('- [ ]') or line.startswith('-'):
                        item = re.sub(r'^-\s*\[[ x]\]\s*', '', line).strip()
                        if item:
                            prep_items.append(item)
            
            # Estimate duration from time string
            duration = "Duration TBD"
            if '-' in time_str:
                duration = "Meeting scheduled"
            
            return create_meeting_reminder(
                title,
                time_str,
                duration,
                attendees,
                agenda_items,
                prep_items,
                meet_link,
                location if not meet_link else None
            )
            
        except Exception as e:
            print(f"Error preparing meeting reminder: {e}")
            return None
    
    def should_send_meeting_reminder(self, meeting_file_path: Path, minutes_before: int = 15) -> bool:
        """Check if it's time to send meeting reminder.
        
        Args:
            meeting_file_path: Path to meeting note file
            minutes_before: Minutes before meeting to send
            
        Returns:
            True if reminder should be sent now
        """
        if not meeting_file_path.exists():
            return False
        
        try:
            with open(meeting_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            import re
            
            # Extract date and time
            date_match = re.search(r'\*\*Date:\*\* (\d{4}-\d{2}-\d{2})', content)
            time_match = re.search(r'\*\*Time:\*\* (\d{1,2}:\d{2}\s*(?:AM|PM))', content)
            
            if not date_match or not time_match:
                return False
            
            date_str = date_match.group(1)
            time_str = time_match.group(1)
            
            # Parse meeting datetime
            meeting_datetime = datetime.strptime(
                f"{date_str} {time_str}",
                "%Y-%m-%d %I:%M %p"
            )
            
            # Calculate reminder time
            reminder_time = meeting_datetime - timedelta(minutes=minutes_before)
            now = datetime.now()
            
            # Check if we're within 5 minutes of reminder time
            time_diff = abs((now - reminder_time).total_seconds())
            return time_diff < 300  # Within 5 minutes
            
        except Exception as e:
            print(f"Error checking reminder time: {e}")
            return False


def get_todays_meetings(daily_file_path: Path) -> List[Path]:
    """Get list of meeting file paths from today's daily file.
    
    Args:
        daily_file_path: Path to daily file
        
    Returns:
        List of meeting file paths
    """
    if not daily_file_path.exists():
        return []
    
    try:
        with open(daily_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        import re
        
        # Find meeting references
        meeting_refs = re.findall(r'@meetings/([\w-]+\.md)', content)
        
        meetings_dir = daily_file_path.parent.parent / "meetings"
        meeting_paths = []
        
        for ref in meeting_refs:
            meeting_path = meetings_dir / ref
            if meeting_path.exists():
                meeting_paths.append(meeting_path)
        
        return meeting_paths
        
    except Exception as e:
        print(f"Error getting today's meetings: {e}")
        return []


# Convenience functions for Claude to call

def monday_morning_slack_notification(weekly_summary_file: str,
                                      week_plan_file: str,
                                      daily_file: str) -> Dict:
    """Generate Monday morning Slack notification.
    
    Usage from Claude:
        slack_data = monday_morning_slack_notification(
            'weekly-summary-2025-10-14.md',
            'week-2025-10-14.md',
            '2025-10-14.md'
        )
        # Then call Slack MCP with slack_data
    """
    workflow = SlackWorkflowIntegration()
    return workflow.monday_morning_workflow(
        weekly_summary_file,
        week_plan_file,
        daily_file
    )


def action_item_reminder(weekly_summary_file: str, my_name: str = "Eamon") -> Dict:
    """Generate action item reminder notification.
    
    Usage from Claude:
        slack_data = action_item_reminder('weekly-summary-2025-10-14.md')
        # Then call Slack MCP with slack_data
    """
    workflow = SlackWorkflowIntegration()
    return workflow.send_action_reminders(weekly_summary_file, my_name)


def friday_review_reminder() -> Dict:
    """Generate Friday review reminder notification.
    
    Usage from Claude:
        slack_data = friday_review_reminder()
        # Then call Slack MCP with slack_data
    """
    workflow = SlackWorkflowIntegration()
    return workflow.send_friday_reminder()


def meeting_reminder(meeting_file: str) -> Optional[Dict]:
    """Generate meeting reminder notification.
    
    Usage from Claude:
        slack_data = meeting_reminder('2025-10-14-team-sync.md')
        # Then call Slack MCP with slack_data
    """
    workflow = SlackWorkflowIntegration()
    project_root = Path(__file__).parent.parent
    meeting_path = project_root / "meetings" / meeting_file
    return workflow.prepare_meeting_reminder(meeting_path)


if __name__ == "__main__":
    print("❌ This module is designed to be imported and used from Cursor/Claude environment.")
    print("📌 It provides high-level workflow functions that integrate Slack notifications.")





