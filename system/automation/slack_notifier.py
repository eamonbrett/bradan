#!/usr/bin/env python3
"""
Slack Notification Module for Task Management System

This module provides Slack notification functionality via the playground-slack-mcp server.
All notifications are sent as personal DMs to the user.

Designed to be called from Cursor/Claude environment where MCP functions are available.
"""

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import re


class SlackNotifier:
    """Handle all Slack notifications for the task management system."""
    
    def __init__(self, user_id: str = None):
        """Initialize the Slack notifier.
        
        Args:
            user_id: Slack user ID (e.g., 'U12345ABC'). If None, sends to 'me'.
        """
        self.user_id = user_id or "me"
    
    def format_monday_morning_summary(self, 
                                     weekly_summary_path: Path,
                                     week_plan_path: Path,
                                     daily_file_path: Path) -> str:
        """Format the Monday morning summary notification.
        
        Args:
            weekly_summary_path: Path to generated weekly summary
            week_plan_path: Path to generated week plan
            daily_file_path: Path to generated daily file
            
        Returns:
            Formatted Slack message
        """
        today = date.today()
        
        # Read the files to extract key information
        top_3 = self._extract_top_3_from_week_plan(week_plan_path)
        action_count = self._count_action_items(weekly_summary_path)
        meeting_count = self._count_meetings(weekly_summary_path)
        
        message = f"""🌅 *Good morning! Your week is planned and ready.*

📅 *Week of {today.strftime('%B %d, %Y')}*

---

📊 *Weekly Summary Generated*
• {meeting_count} meetings from last week processed
• {action_count} action items extracted and organized
• All commitments captured

📋 *Week Plan Created*
Your Top 3 priorities this week:

{self._format_top_3_for_slack(top_3)}

📝 *Today's File Ready*
Your daily file is ready with calendar events and tasks.

---

*Files created:*
• Weekly Summary: `{weekly_summary_path.name}`
• Week Plan: `{week_plan_path.name}`
• Daily File: `{daily_file_path.name}`

💪 *Ready to make this week count!*
"""
        return message
    
    def format_daily_file_notification(self,
                                       target_date: date,
                                       top_3_tasks: List[str],
                                       meeting_count: int,
                                       daily_file_path: Path) -> str:
        """Format the daily file generation notification.
        
        Args:
            target_date: The date for the daily file
            top_3_tasks: List of top 3 tasks for the day
            meeting_count: Number of meetings scheduled
            daily_file_path: Path to generated daily file
            
        Returns:
            Formatted Slack message
        """
        day_name = target_date.strftime('%A')
        date_str = target_date.strftime('%B %d, %Y')
        
        message = f"""☀️ *{day_name} Ready!*

📅 *{date_str}*

---

🎯 *Your Top 3 Tasks Today:*

{self._format_tasks_for_slack(top_3_tasks)}

📆 *Meetings:* {meeting_count} scheduled

---

✅ *Daily file created:* `{daily_file_path.name}`

*Let's make today count!*
"""
        return message
    
    def format_action_item_reminder(self,
                                    actions: List[Dict[str, str]],
                                    reminder_type: str = "weekly") -> str:
        """Format action item reminder.
        
        Args:
            actions: List of action items with 'task', 'meeting', 'date' keys
            reminder_type: 'weekly' or 'daily' reminder
            
        Returns:
            Formatted Slack message
        """
        if reminder_type == "weekly":
            header = "📌 *Your Action Items for This Week*"
        else:
            header = "📌 *Action Item Reminder*"
        
        message = f"""{header}

You have {len(actions)} action item(s) to complete:

"""
        
        # Group by meeting if available
        by_meeting = {}
        for action in actions:
            meeting = action.get('meeting', 'Other')
            if meeting not in by_meeting:
                by_meeting[meeting] = []
            by_meeting[meeting].append(action)
        
        for meeting, items in by_meeting.items():
            if meeting != 'Other':
                message += f"*From: {meeting}*\n"
            for item in items:
                task = item.get('task', 'Unknown task')
                message += f"• {task}\n"
            message += "\n"
        
        message += "💡 *Tip:* Add these to your daily file if they're priority today!"
        
        return message
    
    def format_friday_review_reminder(self) -> str:
        """Format Friday afternoon weekly review reminder.
        
        Returns:
            Formatted Slack message
        """
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        
        message = f"""🎯 *Time for Your Weekly Review!*

📅 *Week of {week_start.strftime('%B %d, %Y')}*

---

It's Friday afternoon - time to reflect on the week and prep for next week.

*Your 20-minute reflection ritual:*

1️⃣ *Generate Review* (10 min)
   Ask Claude: "Generate weekly review"

2️⃣ *Complete Sections* (5 min)
   • What worked well this week?
   • What was challenging?
   • Key learnings

3️⃣ *Update Projects* (5 min)
   • Mark completed milestones
   • Update project statuses
   • Note any blockers

---

💭 *Remember:* Reviews create learning. Don't skip this!

*Ready to reflect?*
"""
        return message
    
    def format_daily_plan_notification(self,
                                        target_date: date,
                                        top_3_tasks: List[str],
                                        schedule: List[Dict[str, str]],
                                        meeting_count: int,
                                        strategic_focus: str = None,
                                        daily_file_path: Path = None) -> str:
        """Format comprehensive daily plan notification.
        
        Args:
            target_date: The date for the daily plan
            top_3_tasks: List of top 3 tasks for the day
            schedule: List of schedule items with 'time', 'title', 'type' keys
            meeting_count: Number of meetings scheduled
            strategic_focus: Optional strategic focus for the day
            daily_file_path: Path to daily file
            
        Returns:
            Formatted Slack message
        """
        day_name = target_date.strftime('%A')
        date_str = target_date.strftime('%B %d, %Y')
        
        message = f"""📅 *Your Daily Plan - {day_name}*

*{date_str}*

---

"""
        
        # Strategic focus if provided
        if strategic_focus:
            message += f"🎯 *Today's Strategic Focus*\n{strategic_focus}\n\n---\n\n"
        
        # Top 3 Tasks
        message += "🔥 *Top 3 Tasks Today:*\n\n"
        message += self._format_tasks_for_slack(top_3_tasks)
        message += "\n\n---\n\n"
        
        # Schedule
        if schedule:
            message += "📆 *Today's Schedule:*\n\n"
            
            # Group by time of day
            morning = [s for s in schedule if self._is_morning(s.get('time', ''))]
            afternoon = [s for s in schedule if self._is_afternoon(s.get('time', ''))]
            evening = [s for s in schedule if self._is_evening(s.get('time', ''))]
            
            if morning:
                message += "*Morning*\n"
                for item in morning:
                    icon = '📞' if item.get('type') == 'meeting' else '⏰'
                    message += f"{icon} {item.get('time', '')}: {item.get('title', 'Event')}\n"
                message += "\n"
            
            if afternoon:
                message += "*Afternoon*\n"
                for item in afternoon:
                    icon = '📞' if item.get('type') == 'meeting' else '⏰'
                    message += f"{icon} {item.get('time', '')}: {item.get('title', 'Event')}\n"
                message += "\n"
            
            if evening:
                message += "*Evening*\n"
                for item in evening:
                    icon = '📞' if item.get('type') == 'meeting' else '⏰'
                    message += f"{icon} {item.get('time', '')}: {item.get('title', 'Event')}\n"
                message += "\n"
            
            message += f"_Total: {meeting_count} meetings_\n\n"
            message += "---\n\n"
        
        # Footer
        if daily_file_path:
            message += f"📝 *Daily file:* `{daily_file_path.name}`\n\n"
        
        message += "💪 *Let's make today count!*"
        
        return message
    
    def format_meeting_reminder(self,
                               meeting_title: str,
                               meeting_time: str,
                               meeting_duration: str,
                               attendees: List[str],
                               agenda_items: List[str],
                               prep_items: List[str],
                               meeting_link: str = None,
                               location: str = None) -> str:
        """Format pre-meeting reminder with agenda and prep.
        
        Args:
            meeting_title: Title of the meeting
            meeting_time: Start time (formatted string)
            meeting_duration: Duration (e.g., "30 min", "1 hour")
            attendees: List of attendee names
            agenda_items: List of agenda topics
            prep_items: List of prep tasks
            meeting_link: Optional Google Meet or Zoom link
            location: Optional location string
            
        Returns:
            Formatted Slack message
        """
        message = f"""⏰ *Upcoming Meeting Reminder*

📅 *{meeting_title}*
🕐 *Starting:* {meeting_time} ({meeting_duration})
"""
        
        if meeting_link:
            message += f"🔗 *Join:* {meeting_link}\n"
        elif location:
            message += f"📍 *Location:* {location}\n"
        
        if attendees:
            attendee_str = ', '.join(attendees[:3])
            if len(attendees) > 3:
                attendee_str += f" +{len(attendees) - 3} others"
            message += f"👥 *Attendees:* {attendee_str}\n"
        
        message += "\n---\n\n"
        
        if agenda_items:
            message += "📋 *Agenda:*\n"
            for i, item in enumerate(agenda_items, 1):
                message += f"{i}. {item}\n"
            message += "\n"
        
        if prep_items:
            message += "✅ *Your Prep:*\n"
            for item in prep_items:
                message += f"• {item}\n"
            message += "\n"
        
        message += "---\n\n💡 *Ready to contribute!*"
        
        return message
    
    def _extract_top_3_from_week_plan(self, week_plan_path: Path) -> List[Dict[str, str]]:
        """Extract Top 3 priorities from week plan file.
        
        Args:
            week_plan_path: Path to week plan file
            
        Returns:
            List of dicts with 'type' and 'task' keys
        """
        if not week_plan_path.exists():
            return []
        
        try:
            with open(week_plan_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for Top 3 Priorities section
            top_3_section = re.search(
                r'## Top 3 Priorities.*?\n(.*?)(?=\n##|\Z)',
                content,
                re.DOTALL
            )
            
            if not top_3_section:
                return []
            
            section_text = top_3_section.group(1)
            
            # Extract the three priorities
            priorities = []
            
            # Strategic Priority
            strategic = re.search(r'### 🎯 Strategic Priority.*?\n\*\*Task:\*\* (.*?)(?=\n\*\*|\n###|\Z)', section_text, re.DOTALL)
            if strategic:
                priorities.append({'type': 'Strategic', 'task': strategic.group(1).strip()})
            
            # Stakeholder Priority
            stakeholder = re.search(r'### 🤝 Stakeholder Priority.*?\n\*\*Task:\*\* (.*?)(?=\n\*\*|\n###|\Z)', section_text, re.DOTALL)
            if stakeholder:
                priorities.append({'type': 'Stakeholder', 'task': stakeholder.group(1).strip()})
            
            # Operational Priority
            operational = re.search(r'### 🔧 Operational Priority.*?\n\*\*Task:\*\* (.*?)(?=\n\*\*|\n###|\Z)', section_text, re.DOTALL)
            if operational:
                priorities.append({'type': 'Operational', 'task': operational.group(1).strip()})
            
            return priorities
            
        except Exception as e:
            print(f"Error extracting Top 3: {e}")
            return []
    
    def _count_action_items(self, weekly_summary_path: Path) -> int:
        """Count action items in weekly summary.
        
        Args:
            weekly_summary_path: Path to weekly summary file
            
        Returns:
            Number of action items
        """
        if not weekly_summary_path.exists():
            return 0
        
        try:
            with open(weekly_summary_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count checkbox items
            checkboxes = re.findall(r'- \[ \]', content)
            return len(checkboxes)
            
        except Exception:
            return 0
    
    def _count_meetings(self, weekly_summary_path: Path) -> int:
        """Count meetings in weekly summary.
        
        Args:
            weekly_summary_path: Path to weekly summary file
            
        Returns:
            Number of meetings
        """
        if not weekly_summary_path.exists():
            return 0
        
        try:
            with open(weekly_summary_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for the overview section
            overview = re.search(r'\*\*Total Meetings:\*\* (\d+)', content)
            if overview:
                return int(overview.group(1))
            
            return 0
            
        except Exception:
            return 0
    
    def _format_top_3_for_slack(self, top_3: List[Dict[str, str]]) -> str:
        """Format Top 3 priorities for Slack message.
        
        Args:
            top_3: List of priority dicts
            
        Returns:
            Formatted string
        """
        if not top_3:
            return "_(Top 3 priorities to be defined)_"
        
        icons = {
            'Strategic': '🎯',
            'Stakeholder': '🤝',
            'Operational': '🔧'
        }
        
        formatted = []
        for i, priority in enumerate(top_3, 1):
            icon = icons.get(priority['type'], '•')
            task = priority['task']
            # Truncate if too long
            if len(task) > 100:
                task = task[:97] + "..."
            formatted.append(f"{i}. {icon} *{priority['type']}:* {task}")
        
        return '\n'.join(formatted)
    
    def _format_tasks_for_slack(self, tasks: List[str]) -> str:
        """Format task list for Slack message.
        
        Args:
            tasks: List of task strings
            
        Returns:
            Formatted string
        """
        if not tasks:
            return "_(No tasks defined yet)_"
        
        formatted = []
        for i, task in enumerate(tasks[:3], 1):  # Limit to 3
            # Truncate if too long
            if len(task) > 150:
                task = task[:147] + "..."
            formatted.append(f"{i}. {task}")
        
        return '\n'.join(formatted)
    
    def _is_morning(self, time_str: str) -> bool:
        """Check if time is morning (before noon).
        
        Args:
            time_str: Time string (e.g., '9:00 AM', '11:30 AM')
            
        Returns:
            True if morning time
        """
        import re
        match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM)?', time_str, re.IGNORECASE)
        if match:
            hour = int(match.group(1))
            am_pm = match.group(3)
            
            if am_pm:
                # 12-hour format
                if am_pm.upper() == 'AM' and hour != 12:
                    return True
                elif am_pm.upper() == 'AM' and hour == 12:
                    return False  # Midnight
            else:
                # 24-hour format
                return 0 <= hour < 12
        
        return False
    
    def _is_afternoon(self, time_str: str) -> bool:
        """Check if time is afternoon (noon to 5pm).
        
        Args:
            time_str: Time string
            
        Returns:
            True if afternoon time
        """
        import re
        match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM)?', time_str, re.IGNORECASE)
        if match:
            hour = int(match.group(1))
            am_pm = match.group(3)
            
            if am_pm:
                # 12-hour format
                if am_pm.upper() == 'PM' and hour != 12:
                    return hour < 5
                elif am_pm.upper() == 'PM' and hour == 12:
                    return True  # Noon
            else:
                # 24-hour format
                return 12 <= hour < 17
        
        return False
    
    def _is_evening(self, time_str: str) -> bool:
        """Check if time is evening (after 5pm).
        
        Args:
            time_str: Time string
            
        Returns:
            True if evening time
        """
        import re
        match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM)?', time_str, re.IGNORECASE)
        if match:
            hour = int(match.group(1))
            am_pm = match.group(3)
            
            if am_pm:
                # 12-hour format
                if am_pm.upper() == 'PM' and hour >= 5 and hour != 12:
                    return True
            else:
                # 24-hour format
                return hour >= 17
        
        return False
    
    def send_message(self, message: str) -> Dict[str, any]:
        """Prepare message to be sent via Slack MCP.
        
        This returns the data structure that Claude should use to call
        the playground-slack-mcp send message function.
        
        Args:
            message: Formatted message to send
            
        Returns:
            Dict with message details for MCP call
        """
        return {
            'recipient': self.user_id,
            'message': message,
            'mcp_function': 'mcp_playground-slack-mcp_slack_send_message',
            'note': 'Claude should call the Slack MCP function with this message'
        }


def create_monday_morning_notification(weekly_summary_path: str,
                                       week_plan_path: str,
                                       daily_file_path: str) -> Dict[str, any]:
    """Create Monday morning summary notification.
    
    Args:
        weekly_summary_path: Path to weekly summary file
        week_plan_path: Path to week plan file
        daily_file_path: Path to daily file
        
    Returns:
        Message data for Slack MCP call
    """
    notifier = SlackNotifier()
    message = notifier.format_monday_morning_summary(
        Path(weekly_summary_path),
        Path(week_plan_path),
        Path(daily_file_path)
    )
    return notifier.send_message(message)


def create_daily_notification(target_date: date,
                              top_3_tasks: List[str],
                              meeting_count: int,
                              daily_file_path: str) -> Dict[str, any]:
    """Create daily file notification.
    
    Args:
        target_date: Date for the daily file
        top_3_tasks: List of top 3 tasks
        meeting_count: Number of meetings
        daily_file_path: Path to daily file
        
    Returns:
        Message data for Slack MCP call
    """
    notifier = SlackNotifier()
    message = notifier.format_daily_file_notification(
        target_date,
        top_3_tasks,
        meeting_count,
        Path(daily_file_path)
    )
    return notifier.send_message(message)


def create_action_reminder(actions: List[Dict[str, str]],
                          reminder_type: str = "weekly") -> Dict[str, any]:
    """Create action item reminder notification.
    
    Args:
        actions: List of action items
        reminder_type: 'weekly' or 'daily'
        
    Returns:
        Message data for Slack MCP call
    """
    notifier = SlackNotifier()
    message = notifier.format_action_item_reminder(actions, reminder_type)
    return notifier.send_message(message)


def create_friday_review_reminder() -> Dict[str, any]:
    """Create Friday review reminder notification.
    
    Returns:
        Message data for Slack MCP call
    """
    notifier = SlackNotifier()
    message = notifier.format_friday_review_reminder()
    return notifier.send_message(message)


def create_meeting_reminder(meeting_title: str,
                           meeting_time: str,
                           meeting_duration: str,
                           attendees: List[str],
                           agenda_items: List[str],
                           prep_items: List[str],
                           meeting_link: str = None,
                           location: str = None) -> Dict[str, any]:
    """Create pre-meeting reminder notification.
    
    Args:
        meeting_title: Title of meeting
        meeting_time: Start time string
        meeting_duration: Duration string
        attendees: List of attendee names
        agenda_items: List of agenda topics
        prep_items: List of prep tasks
        meeting_link: Optional meeting link
        location: Optional location
        
    Returns:
        Message data for Slack MCP call
    """
    notifier = SlackNotifier()
    message = notifier.format_meeting_reminder(
        meeting_title,
        meeting_time,
        meeting_duration,
        attendees,
        agenda_items,
        prep_items,
        meeting_link,
        location
    )
    return notifier.send_message(message)


def create_daily_plan_notification(target_date: date,
                                   top_3_tasks: List[str],
                                   schedule: List[Dict[str, str]],
                                   meeting_count: int,
                                   strategic_focus: str = None,
                                   daily_file_path: str = None) -> Dict[str, any]:
    """Create comprehensive daily plan notification.
    
    Args:
        target_date: Date for the daily plan
        top_3_tasks: List of top 3 tasks
        schedule: List of schedule items with 'time', 'title', 'type' keys
        meeting_count: Number of meetings
        strategic_focus: Optional strategic focus
        daily_file_path: Path to daily file
        
    Returns:
        Message data for Slack MCP call
    """
    notifier = SlackNotifier()
    message = notifier.format_daily_plan_notification(
        target_date,
        top_3_tasks,
        schedule,
        meeting_count,
        strategic_focus,
        Path(daily_file_path) if daily_file_path else None
    )
    return notifier.send_message(message)


if __name__ == "__main__":
    print("❌ This module is designed to be imported and used from Cursor/Claude environment.")
    print("📌 It provides Slack notification formatting and MCP integration helpers.")

