"""Template processing utilities for daily file generation."""

import re
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class TemplateProcessor:
    """Handles template loading and processing for daily files."""
    
    def __init__(self, template_path: Path):
        self.template_path = template_path
        self.template_content = self._load_template()
    
    def _load_template(self) -> str:
        """Load template content from file."""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"Template file not found: {self.template_path}")
            return self._get_fallback_template()
        except Exception as e:
            logger.error(f"Error loading template: {e}")
            return self._get_fallback_template()
    
    def _get_fallback_template(self) -> str:
        """Provide a fallback template if main template fails to load."""
        return """# Daily Note - {date}

## Today's Focus
- [ ] 🔴 High priority task ~2h #project
- [ ] 🟡 Medium priority task ~45min #admin
- [ ] 🟢 Low priority task ~15min #quick

## Schedule
{schedule_section}

## Meetings Today
{meetings_section}

## Inbox Processing
- [ ] Check and respond to emails
- [ ] Review Slack notifications
- [ ] Process yesterday's notes

## Notes & Ideas
[Capture random thoughts, decisions, insights]

## Tomorrow's Prep
- [ ] Review calendar for tomorrow
- [ ] Identify top 3 priorities
- [ ] Prep any meeting materials

---
**Energy Level:** [High/Medium/Low]
**Mood:** [How you're feeling]
**Weather:** [If it affects your work]"""

    def process_template(self, context: Dict[str, Any]) -> str:
        """Process template with provided context data."""
        content = self.template_content
        
        # Replace basic placeholders
        content = content.replace('[DATE]', context.get('date', ''))
        content = content.replace('{date}', context.get('date', ''))
        
        # Process schedule section - replace the existing schedule section
        schedule_section = self._format_schedule_section(context.get('calendar_events', []))
        content = self._replace_schedule_section(content, schedule_section)
        
        # Process meetings section - replace the existing meetings section
        meetings_section = self._format_meetings_section(context.get('calendar_events', []))
        content = self._replace_meetings_section(content, meetings_section)
        
        return content
    
    def _format_schedule_section(self, events: List[Dict]) -> str:
        """Format calendar events into schedule section."""
        if not events:
            return """### Morning
- 9:00 AM - [Meeting/Block]
- 10:30 AM - [Meeting/Block]

### Afternoon
- 1:00 PM - [Meeting/Block]
- 3:00 PM - [Meeting/Block]"""
        
        morning_events = []
        afternoon_events = []
        
        for event in events:
            event_time = event.get('start_time', '')
            event_title = event.get('title', 'Event')
            
            # Parse time to determine morning/afternoon
            try:
                time_obj = datetime.strptime(event_time, '%H:%M').time()
                formatted_time = time_obj.strftime('%I:%M %p').lstrip('0')
                event_line = f"- {formatted_time} - {event_title}"
                
                if time_obj.hour < 12:
                    morning_events.append(event_line)
                else:
                    afternoon_events.append(event_line)
            except ValueError:
                # If time parsing fails, add to morning by default
                morning_events.append(f"- {event_time} - {event_title}")
        
        # Build schedule section
        schedule_parts = []
        
        if morning_events:
            schedule_parts.append("### Morning")
            schedule_parts.extend(morning_events)
        else:
            schedule_parts.extend(["### Morning", "- [No morning meetings]"])
        
        schedule_parts.append("")  # Empty line between sections
        
        if afternoon_events:
            schedule_parts.append("### Afternoon")
            schedule_parts.extend(afternoon_events)
        else:
            schedule_parts.extend(["### Afternoon", "- [No afternoon meetings]"])
        
        return "\n".join(schedule_parts)
    
    def _format_meetings_section(self, events: List[Dict]) -> str:
        """Format calendar events into meetings section with file references."""
        if not events:
            return "- [No meetings scheduled]"
        
        meeting_lines = []
        for event in events:
            event_time = event.get('start_time', '')
            event_title = event.get('title', 'Event')
            event_date = event.get('date', datetime.now().strftime('%Y-%m-%d'))
            
            # Create meeting file slug (simplified title)
            meeting_slug = self._create_meeting_slug(event_title)
            meeting_file = f"@meetings/{event_date}-{meeting_slug}.md"
            
            # Format time for display
            try:
                time_obj = datetime.strptime(event_time, '%H:%M').time()
                display_time = time_obj.strftime('%I:%M %p').lstrip('0')
            except ValueError:
                display_time = event_time
            
            meeting_line = f"- {display_time} - {event_title} ({meeting_file})"
            meeting_lines.append(meeting_line)
        
        return "\n".join(meeting_lines)
    
    def _replace_schedule_section(self, content: str, new_schedule: str) -> str:
        """Replace the schedule section in the template with new content."""
        import re
        
        # Pattern to match the schedule section
        pattern = r'(## Schedule\n)(.*?)(\n## Meetings Today|\n## Inbox Processing|\Z)'
        
        def replace_func(match):
            return match.group(1) + new_schedule + '\n' + match.group(3)
        
        # Use re.DOTALL to match newlines with .*
        result = re.sub(pattern, replace_func, content, flags=re.DOTALL)
        return result
    
    def _replace_meetings_section(self, content: str, new_meetings: str) -> str:
        """Replace the meetings section in the template with new content."""
        import re
        
        # Pattern to match the meetings section
        pattern = r'(## Meetings Today\n)(.*?)(\n## Inbox Processing|\n## Notes & Ideas|\Z)'
        
        def replace_func(match):
            return match.group(1) + new_meetings + '\n' + match.group(3)
        
        # Use re.DOTALL to match newlines with .*
        result = re.sub(pattern, replace_func, content, flags=re.DOTALL)
        return result
    
    def _create_meeting_slug(self, title: str) -> str:
        """Create a URL-friendly slug from meeting title."""
        # Remove special characters and convert to lowercase
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        # Replace spaces and multiple hyphens with single hyphen
        slug = re.sub(r'[-\s]+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        # Limit length
        return slug[:50] if slug else 'meeting'

def create_daily_context(target_date: date, calendar_events: List[Dict] = None) -> Dict[str, Any]:
    """Create context dictionary for daily file generation."""
    return {
        'date': target_date.strftime('%Y-%m-%d'),
        'calendar_events': calendar_events or [],
        'day_of_week': target_date.strftime('%A'),
        'month_name': target_date.strftime('%B'),
    }
