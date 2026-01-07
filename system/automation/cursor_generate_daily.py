#!/usr/bin/env python3
"""
Cursor-Native Daily File Generator with Real MCP Integration

This script is designed to be executed from within the Cursor/Claude environment
where Google Workspace MCP and Slack MCP functions are directly available.

DO NOT run this as a standalone Python script - it won't work.
Instead, ask Claude in Cursor: "Generate today's daily file"
"""

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import re
import sys

# Add automation directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "automation"))

class CursorDailyGenerator:
    """Generate daily files using real MCP data from Cursor environment."""
    
    def __init__(self, project_root: Path = None, enable_slack: bool = True):
        if project_root is None:
            # Script is in system/automation/, go up 2 levels to project root
            project_root = Path(__file__).parent.parent.parent
        
        self.project_root = project_root
        self.daily_dir = project_root / "work" / "daily"
        self.meetings_dir = project_root / "work" / "meetings"
        # Use template from system/templates
        template_dir = Path(__file__).parent.parent / "templates"
        self.template_path = template_dir / "daily.md"
        self.enable_slack = enable_slack
        
        # Ensure directories exist
        self.daily_dir.mkdir(exist_ok=True)
        self.meetings_dir.mkdir(exist_ok=True)
    
    def parse_mcp_event(self, event: Dict) -> Optional[Dict]:
        """Parse MCP calendar event into standardized format."""
        try:
            # Extract start time
            start_info = event.get('start', {})
            end_info = event.get('end', {})
            
            # Handle both dict format and string format
            if isinstance(start_info, dict):
                start_str = start_info.get('dateTime', start_info.get('date', ''))
            else:
                start_str = str(start_info)
            
            if isinstance(end_info, dict):
                end_str = end_info.get('dateTime', end_info.get('date', ''))
            else:
                end_str = str(end_info)
            
            # Parse timed vs all-day events
            if 'T' in start_str:  # Timed event
                # Handle timezone offsets
                if start_str.endswith('Z'):
                    start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                else:
                    start_dt = datetime.fromisoformat(start_str)
                
                formatted_start = start_dt.strftime('%H:%M')
                event_date = start_dt.strftime('%Y-%m-%d')
                
                # Parse end time
                if end_str and 'T' in end_str:
                    if end_str.endswith('Z'):
                        end_dt = datetime.fromisoformat(end_str.replace('Z', '+00:00'))
                    else:
                        end_dt = datetime.fromisoformat(end_str)
                    formatted_end = end_dt.strftime('%H:%M')
                else:
                    formatted_end = formatted_start
            else:  # All-day event
                formatted_start = 'All day'
                formatted_end = 'All day'
                try:
                    event_date = datetime.strptime(start_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                except (ValueError, TypeError):
                    event_date = date.today().strftime('%Y-%m-%d')
            
            # Extract attendees
            attendees = []
            for attendee in event.get('attendees', []):
                if isinstance(attendee, dict) and 'email' in attendee:
                    attendees.append(attendee['email'])
                elif isinstance(attendee, str):
                    attendees.append(attendee)
            
            # Get conference/meeting link
            conference_info = event.get('conferenceData', {})
            meet_link = ''
            if conference_info:
                entry_points = conference_info.get('entryPoints', [])
                for entry in entry_points:
                    if entry.get('entryPointType') == 'video':
                        meet_link = entry.get('uri', '')
                        break
            
            # Also check hangoutLink field
            if not meet_link:
                meet_link = event.get('hangoutLink', '')
            
            return {
                'title': event.get('summary', 'Untitled Event'),
                'start_time': formatted_start,
                'end_time': formatted_end,
                'date': event_date,
                'attendees': attendees,
                'location': event.get('location', ''),
                'description': event.get('description', ''),
                'status': event.get('status', 'confirmed'),
                'meet_link': meet_link
            }
            
        except Exception as e:
            print(f"Error parsing event {event.get('summary', 'Unknown')}: {e}")
            return None
    
    def format_schedule_section(self, events: List[Dict]) -> str:
        """Format events into schedule section with morning/afternoon split."""
        if not events:
            return """### Morning
- [No morning meetings]

### Afternoon
- [No afternoon meetings]"""
        
        morning_events = []
        afternoon_events = []
        all_day_events = []
        
        for event in events:
            if event.get('start_time') == 'All day':
                all_day_events.append(f"- {event.get('title', 'Event')}")
                continue
            
            event_time = event.get('start_time', '')
            event_title = event.get('title', 'Event')
            
            try:
                time_obj = datetime.strptime(event_time, '%H:%M').time()
                formatted_time = time_obj.strftime('%I:%M %p').lstrip('0')
                event_line = f"- {formatted_time} - {event_title}"
                
                if time_obj.hour < 12:
                    morning_events.append(event_line)
                else:
                    afternoon_events.append(event_line)
            except ValueError:
                afternoon_events.append(f"- {event_time} - {event_title}")
        
        # Build schedule
        parts = []
        
        # All-day events first if any
        if all_day_events:
            parts.append("### All Day")
            parts.extend(all_day_events)
            parts.append("")
        
        # Morning
        parts.append("### Morning")
        if morning_events:
            parts.extend(morning_events)
        else:
            parts.append("- [No morning meetings]")
        parts.append("")
        
        # Afternoon
        parts.append("### Afternoon")
        if afternoon_events:
            parts.extend(afternoon_events)
        else:
            parts.append("- [No afternoon meetings]")
        
        return "\n".join(parts)
    
    def format_meetings_section(self, events: List[Dict], target_date: date) -> str:
        """Format events into meetings section with file cross-references."""
        if not events:
            return "- [No meetings scheduled]"
        
        meeting_lines = []
        for event in events:
            # Skip all-day events
            if event.get('start_time') == 'All day':
                continue
            
            event_time = event.get('start_time', '')
            event_title = event.get('title', 'Event')
            event_date = target_date.strftime('%Y-%m-%d')
            
            meeting_slug = self._create_meeting_slug(event_title)
            meeting_file = f"@meetings/{event_date}-{meeting_slug}.md"
            
            try:
                time_obj = datetime.strptime(event_time, '%H:%M').time()
                display_time = time_obj.strftime('%I:%M %p').lstrip('0')
            except ValueError:
                display_time = event_time
            
            meeting_line = f"- {display_time} - {event_title} ({meeting_file})"
            meeting_lines.append(meeting_line)
        
        return "\n".join(meeting_lines) if meeting_lines else "- [No meetings scheduled]"
    
    def _create_meeting_slug(self, title: str) -> str:
        """Create URL-friendly slug from meeting title."""
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')[:50] if slug else 'meeting'
    
    def create_meeting_content(self, event: Dict, target_date: date) -> str:
        """Generate meeting file content."""
        title = event.get('title', 'Meeting')
        start_time = event.get('start_time', '')
        end_time = event.get('end_time', '')
        attendees = ', '.join(event.get('attendees', []))
        location = event.get('location', '')
        meet_link = event.get('meet_link', '')
        description = event.get('description', '')
        
        # Format time range
        time_range = start_time
        if end_time and end_time != start_time:
            try:
                start_12h = datetime.strptime(start_time, '%H:%M').strftime('%I:%M %p').lstrip('0')
                end_12h = datetime.strptime(end_time, '%H:%M').strftime('%I:%M %p').lstrip('0')
                time_range = f"{start_12h} - {end_12h}"
            except ValueError:
                time_range = f"{start_time} - {end_time}"
        
        # Handle location and meet link
        if meet_link and not location:
            location = f"Google Meet: {meet_link}"
        elif meet_link and location:
            location += f"\nGoogle Meet: {meet_link}"
        
        return f"""# Meeting: {title}
**Date:** {target_date.strftime('%Y-%m-%d')}
**Time:** {time_range}
**Attendees:** {attendees}
**Location:** {location}

## Pre-Meeting
**Objective:** [What we want to achieve]
**My prep:**
- [ ] Review agenda
- [ ] Prepare questions
- [ ] Gather relevant documents

## Agenda
1. [Agenda item 1] - [Time allocation]
2. [Agenda item 2] - [Time allocation]
3. [Agenda item 3] - [Time allocation]

## Notes
### [Agenda Item 1]
- Key points discussed
- Decisions made
- Questions raised

### [Agenda Item 2]
- Key points discussed
- Decisions made
- Questions raised

## Key Decisions
- ✅ Decision 1: [What was decided and why]
- ✅ Decision 2: [What was decided and why]

## Action Items
- [ ] [Task] - [Owner] - Due: YYYY-MM-DD
- [ ] [Task] - [Owner] - Due: YYYY-MM-DD

## Follow-up
- **Next meeting:** [Date/Time if scheduled]
- **Documents to share:** [List any docs to send]
- **People to update:** [Who needs to know outcomes]

## Meeting Content
### Recording
- [ ] **Recording Link:** [Add Google Meet recording or other recording URL]
- [ ] **Recording Duration:** [Actual meeting duration]
- [ ] **Recording Quality:** [Good/Fair/Poor - any issues?]

### Transcript
- [ ] **Auto-transcript Available:** [Yes/No - from Google Meet, Otter.ai, etc.]
- [ ] **Transcript Link:** [Link to full transcript if available]
- [ ] **Key Quotes:** [Important quotes or statements from the meeting]

### Meeting Artifacts
- [ ] **Shared Screen Content:** [Links to shared documents, presentations]
- [ ] **Whiteboard/Notes:** [Links to collaborative notes, Miro boards, etc.]
- [ ] **Chat Log:** [Any important chat messages or links shared]

## Personal Notes
[Your private thoughts, concerns, ideas]

---
**Meeting Rating:** [1-5 stars]
**Was this meeting necessary?** [Yes/No and why]

{description if description else ''}
"""
    
    def generate_daily_file(self, target_date: date, calendar_events: List[Dict]) -> bool:
        """Generate daily file with real MCP calendar data."""
        try:
            # Parse all events
            parsed_events = []
            for event in calendar_events:
                parsed = self.parse_mcp_event(event)
                if parsed:
                    parsed_events.append(parsed)
            
            # Load template
            if not self.template_path.exists():
                print(f"Error: Template not found at {self.template_path}")
                return False
            
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Process template
            content = template_content
            content = content.replace('[DATE]', target_date.strftime('%Y-%m-%d'))
            content = content.replace('{date}', target_date.strftime('%Y-%m-%d'))
            
            # Replace schedule section
            schedule_section = self.format_schedule_section(parsed_events)
            content = re.sub(
                r'(## Schedule\n)(.*?)(\n## )',
                lambda m: m.group(1) + schedule_section + '\n\n' + m.group(3),
                content,
                flags=re.DOTALL
            )
            
            # Replace meetings section
            meetings_section = self.format_meetings_section(parsed_events, target_date)
            content = re.sub(
                r'(## Meetings Today\n)(.*?)(\n## )',
                lambda m: m.group(1) + meetings_section + '\n\n' + m.group(3),
                content,
                flags=re.DOTALL
            )
            
            # Write daily file
            daily_file_path = self.daily_dir / f"{target_date.strftime('%Y-%m-%d')}.md"
            
            # Check if file exists
            if daily_file_path.exists():
                print(f"⚠️  Daily file already exists: {daily_file_path}")
                return True
            
            with open(daily_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Created daily file: {daily_file_path}")
            
            # Create meeting stubs
            self._create_meeting_stubs(target_date, parsed_events)
            
            # Prepare Slack notification data if enabled
            if self.enable_slack:
                slack_data = self._prepare_slack_notification(
                    target_date, 
                    daily_file_path,
                    parsed_events
                )
                return {'success': True, 'slack_data': slack_data, 'file_path': str(daily_file_path)}
            
            return {'success': True, 'file_path': str(daily_file_path)}
            
        except Exception as e:
            print(f"❌ Error generating daily file: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _create_meeting_stubs(self, target_date: date, events: List[Dict]):
        """Create meeting file stubs for calendar events."""
        for event in events:
            try:
                # Skip all-day events
                if event.get('start_time') == 'All day':
                    continue
                
                title = event.get('title', 'meeting')
                meeting_slug = self._create_meeting_slug(title)
                meeting_file_path = self.meetings_dir / f"{target_date.strftime('%Y-%m-%d')}-{meeting_slug}.md"
                
                if meeting_file_path.exists():
                    continue
                
                meeting_content = self.create_meeting_content(event, target_date)
                
                with open(meeting_file_path, 'w', encoding='utf-8') as f:
                    f.write(meeting_content)
                
                print(f"✅ Created meeting stub: {meeting_file_path}")
                
            except Exception as e:
                print(f"⚠️  Error creating meeting stub for {event.get('title', 'unknown')}: {e}")
    
    def format_slack_summary(self, target_date: date, events: List[Dict]) -> str:
        """Format a Slack-friendly summary of the day."""
        date_str = target_date.strftime('%A, %B %d, %Y')
        
        if not events:
            return f"📅 Daily file generated for *{date_str}*\nNo meetings scheduled for today! 🎉"
        
        # Count meetings (exclude all-day events)
        meetings = [e for e in events if e.get('start_time') != 'All day']
        all_day = [e for e in events if e.get('start_time') == 'All day']
        
        message_parts = [f"📅 Daily file generated for *{date_str}*\n"]
        
        if all_day:
            message_parts.append(f"🗓️ *All-day events:* {len(all_day)}")
            for event in all_day[:3]:  # Show first 3
                message_parts.append(f"  • {event.get('title')}")
            if len(all_day) > 3:
                message_parts.append(f"  • ...and {len(all_day) - 3} more")
            message_parts.append("")
        
        if meetings:
            message_parts.append(f"🎯 *Meetings today:* {len(meetings)}")
            for event in meetings[:5]:  # Show first 5
                time = event.get('start_time', '')
                title = event.get('title', '')
                try:
                    time_obj = datetime.strptime(time, '%H:%M').time()
                    display_time = time_obj.strftime('%I:%M %p').lstrip('0')
                except ValueError:
                    display_time = time
                message_parts.append(f"  • {display_time} - {title}")
            if len(meetings) > 5:
                message_parts.append(f"  • ...and {len(meetings) - 5} more")
        
        return "\n".join(message_parts)
    
    def _prepare_slack_notification(self, 
                                    target_date: date,
                                    daily_file_path: Path,
                                    events: List[Dict]) -> Dict:
        """Prepare Slack notification data for daily file.
        
        Args:
            target_date: The date for the daily file
            daily_file_path: Path to the generated file
            events: List of parsed calendar events
            
        Returns:
            Dict with Slack notification data
        """
        try:
            # Extract Top 3 tasks from the generated file
            top_3_tasks = self._extract_top_3_from_daily_file(daily_file_path)
            
            # Count meetings (exclude all-day events)
            meeting_count = len([e for e in events if e.get('start_time') != 'All day'])
            
            # Import slack_notifier
            from slack_notifier import create_daily_notification
            
            # Create notification
            return create_daily_notification(
                target_date,
                top_3_tasks,
                meeting_count,
                str(daily_file_path)
            )
            
        except Exception as e:
            print(f"⚠️ Error preparing Slack notification: {e}")
            return None
    
    def _extract_top_3_from_daily_file(self, daily_file_path: Path) -> List[str]:
        """Extract Top 3 tasks from generated daily file.
        
        Args:
            daily_file_path: Path to daily file
            
        Returns:
            List of top 3 task strings
        """
        if not daily_file_path.exists():
            return []
        
        try:
            with open(daily_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for "Top 3 Tasks Today" or "Today's Top 3" section
            top_3_section = re.search(
                r'## (?:Top 3 Tasks Today|Today\'s Top 3).*?\n(.*?)(?=\n##|\Z)',
                content,
                re.DOTALL
            )
            
            if not top_3_section:
                return []
            
            section_text = top_3_section.group(1)
            
            # Extract task lines (looking for numbered or bulleted lists)
            tasks = []
            # Match lines starting with 1., 2., 3. or - or *
            task_lines = re.findall(r'^(?:\d+\.|[-*])\s+(.+)$', section_text, re.MULTILINE)
            
            # Take first 3
            tasks = task_lines[:3] if task_lines else []
            
            # Clean up task text (remove checkbox markers, extra whitespace)
            cleaned_tasks = []
            for task in tasks:
                # Remove checkbox markers
                task = re.sub(r'\[[ x]\]', '', task).strip()
                # Remove priority markers
                task = re.sub(r'^[🔴🟡🟢]\s*', '', task).strip()
                if task:
                    cleaned_tasks.append(task)
            
            return cleaned_tasks
            
        except Exception as e:
            print(f"Error extracting Top 3: {e}")
            return []


def generate_daily_for_date(target_date: date = None) -> Dict:
    """
    This function is meant to be called by Claude from within Cursor.
    It will return the necessary data structure that Claude can use
    to generate the files.
    
    Returns a dict with status and details for Claude to process.
    """
    if target_date is None:
        target_date = date.today()
    
    return {
        'target_date': target_date.strftime('%Y-%m-%d'),
        'instructions': 'Claude should call MCP functions and pass results to generator.generate_daily_file()',
        'mcp_call_needed': 'mcp_gworkspace_mcp_calendar_events',
        'parameters': {
            'calendar_id': 'primary',
            'time_min': target_date.strftime('%Y-%m-%dT00:00:00Z'),
            'time_max': target_date.strftime('%Y-%m-%dT23:59:59Z'),
            'max_results': 25,
            'include_attendees': True,
            'attendee_detail_level': 'basic'
        }
    }


if __name__ == "__main__":
    print("❌ This script is designed to run from within Cursor, not as a standalone script.")
    print("📌 Instead, ask Claude in Cursor: 'Generate today's daily file'")
    print("🔧 Claude will call the necessary MCP functions and use this code to generate your files.")

