#!/usr/bin/env python3
"""
Weekly Meeting Summary Generator
Automatically generates a summary of Gemini meeting notes with action items.
Designed to run every Monday morning to summarize the previous week.
"""

import logging
import sys
import json
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
import re

# Add the automation directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from config import PROJECT_ROOT, LOG_FILE, LOG_LEVEL

# Set up logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class WeeklyMeetingSummaryGenerator:
    """Generate weekly summaries of Gemini meeting notes with action items."""
    
    def __init__(self, output_dir: Path = None):
        """Initialize the generator.
        
        Args:
            output_dir: Directory to save weekly summaries (defaults to PROJECT_ROOT/weekly-summaries)
        """
        self.output_dir = output_dir or PROJECT_ROOT / "weekly-summaries"
        self.output_dir.mkdir(exist_ok=True)
        
    def get_date_range(self, weeks_back: int = 1) -> tuple[str, str]:
        """Get the date range for the previous week(s).
        
        Args:
            weeks_back: Number of weeks to go back (1 = last week, 2 = last 2 weeks)
            
        Returns:
            Tuple of (start_date, end_date) in ISO format
        """
        today = date.today()
        # Get the previous Monday
        days_since_monday = (today.weekday() + 7) % 7
        if days_since_monday == 0:  # If today is Monday
            last_monday = today - timedelta(days=7)
        else:
            last_monday = today - timedelta(days=days_since_monday)
        
        # Calculate start date based on weeks_back
        start_date = last_monday - timedelta(weeks=weeks_back-1)
        end_date = last_monday + timedelta(days=6)  # Sunday
        
        return start_date.isoformat(), end_date.isoformat()
    
    def search_gemini_notes(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Search for Gemini meeting notes in Google Drive.
        
        Args:
            start_date: Start date in ISO format (YYYY-MM-DD)
            end_date: End date in ISO format (YYYY-MM-DD)
            
        Returns:
            List of meeting note file information
        """
        logger.info(f"Searching for Gemini notes between {start_date} and {end_date}")
        
        # Convert dates to RFC3339 format for Google Drive API
        start_datetime = f"{start_date}T00:00:00Z"
        
        # Build the search query
        query = f'fullText contains "Gemini" and (name contains "Notes by Gemini" or name contains "Eamon") and modifiedTime > "{start_datetime}"'
        
        try:
            # Use MCP to search Google Drive
            result = subprocess.run(
                ['npx', '-y', '@modelcontextprotocol/inspector', 'call-tool', 
                 'gworkspace-mcp', 'search_drive', 
                 json.dumps({'query': query, 'orderBy': 'modifiedTime desc'})],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                logger.error(f"Error searching Drive: {result.stderr}")
                return []
            
            # Parse the response
            response = json.loads(result.stdout)
            files = response.get('files', [])
            
            logger.info(f"Found {len(files)} Gemini meeting notes")
            return files
            
        except Exception as e:
            logger.error(f"Error searching Gemini notes: {e}")
            return []
    
    def read_meeting_note(self, file_id: str) -> Dict[str, Any]:
        """Read a Gemini meeting note file.
        
        Args:
            file_id: Google Drive file ID
            
        Returns:
            Dictionary with meeting note content
        """
        try:
            result = subprocess.run(
                ['npx', '-y', '@modelcontextprotocol/inspector', 'call-tool',
                 'gworkspace-mcp', 'read_file',
                 json.dumps({'file_id': file_id, 'format': 'markdown'})],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                logger.error(f"Error reading file {file_id}: {result.stderr}")
                return {}
            
            return json.loads(result.stdout)
            
        except Exception as e:
            logger.error(f"Error reading meeting note {file_id}: {e}")
            return {}
    
    def extract_action_items(self, content: str) -> List[Dict[str, str]]:
        """Extract action items from meeting note content.
        
        Args:
            content: The meeting note content
            
        Returns:
            List of action items with owner and task
        """
        actions = []
        
        # Look for "Suggested next steps" section
        next_steps_match = re.search(r'Suggested next steps(.*?)(?=\n##|\n\*\*|$)', content, re.DOTALL | re.IGNORECASE)
        
        if next_steps_match:
            next_steps_section = next_steps_match.group(1)
            
            # Extract individual action items
            # Pattern: Name will verb... or Name to verb...
            action_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:will|to)\s+(.+?)(?=\n[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:will|to)|\n\n|$)'
            
            matches = re.finditer(action_pattern, next_steps_section, re.MULTILINE)
            for match in matches:
                owner = match.group(1).strip()
                task = match.group(2).strip()
                # Clean up task text
                task = re.sub(r'\.$', '', task)  # Remove trailing period
                actions.append({
                    'owner': owner,
                    'task': task
                })
        
        return actions
    
    def extract_meeting_metadata(self, content: str, title: str) -> Dict[str, Any]:
        """Extract meeting metadata from content.
        
        Args:
            content: The meeting note content
            title: The document title
            
        Returns:
            Dictionary with meeting metadata
        """
        metadata = {
            'title': title,
            'date': '',
            'attendees': []
        }
        
        # Extract date from title (format: YYYY/MM/DD HH:MM TZ)
        date_match = re.search(r'(\d{4}/\d{2}/\d{2})', title)
        if date_match:
            date_str = date_match.group(1)
            metadata['date'] = datetime.strptime(date_str, '%Y/%m/%d').strftime('%B %d, %Y')
        
        # Extract attendees from title (names before the date)
        title_parts = title.split(' - ')
        if len(title_parts) > 0:
            attendees_str = title_parts[0]
            # Split by common separators
            attendees = re.split(r'[/,&]|\band\b', attendees_str)
            metadata['attendees'] = [a.strip() for a in attendees if a.strip()]
        
        return metadata
    
    def group_actions_by_owner(self, all_actions: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, str]]]:
        """Group all action items by owner.
        
        Args:
            all_actions: List of all action items with meeting context
            
        Returns:
            Dictionary mapping owner names to their action items
        """
        grouped = {}
        
        for action_item in all_actions:
            owner = action_item['owner']
            if owner not in grouped:
                grouped[owner] = []
            grouped[owner].append(action_item)
        
        return grouped
    
    def generate_summary_markdown(self, meetings: List[Dict[str, Any]], 
                                  actions_by_owner: Dict[str, List[Dict[str, str]]],
                                  start_date: str, end_date: str) -> str:
        """Generate markdown summary of meetings and actions.
        
        Args:
            meetings: List of meeting metadata
            actions_by_owner: Action items grouped by owner
            start_date: Week start date
            end_date: Week end date
            
        Returns:
            Markdown-formatted summary
        """
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        
        md = f"""# Weekly Meeting Summary
**Week of {start_dt.strftime('%B %d')} - {end_dt.strftime('%B %d, %Y')}**
*Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*

---

## 📊 Overview
- **Total Meetings:** {len(meetings)}
- **Action Items:** {sum(len(items) for items in actions_by_owner.values())}
- **People with Actions:** {len(actions_by_owner)}

---

## 🗓️ Meetings Attended

"""
        # List all meetings
        for meeting in meetings:
            attendees_str = ' / '.join(meeting['attendees'][:3])
            if len(meeting['attendees']) > 3:
                attendees_str += f" + {len(meeting['attendees']) - 3} others"
            
            md += f"### {attendees_str}\n"
            if meeting['date']:
                md += f"**Date:** {meeting['date']}  \n"
            md += f"**Full Title:** {meeting['title']}\n\n"
        
        md += "\n---\n\n## ✅ Action Items by Owner\n\n"
        
        # Sort owners alphabetically
        for owner in sorted(actions_by_owner.keys()):
            items = actions_by_owner[owner]
            md += f"### {owner}\n\n"
            
            # Group by meeting
            meeting_groups = {}
            for item in items:
                meeting_key = item['meeting_title'].split(' - ')[0]  # Get just the names
                if meeting_key not in meeting_groups:
                    meeting_groups[meeting_key] = []
                meeting_groups[meeting_key].append(item)
            
            for meeting_key, meeting_items in meeting_groups.items():
                md += f"**From: {meeting_key}**\n"
                for item in meeting_items:
                    md += f"- [ ] {item['task']}\n"
                md += "\n"
        
        md += "\n---\n\n## 📋 Action Items by Meeting\n\n"
        
        # List actions by meeting
        for meeting in meetings:
            meeting_title = meeting['title']
            meeting_actions = [a for actions in actions_by_owner.values() 
                             for a in actions 
                             if a['meeting_title'] == meeting_title]
            
            if meeting_actions:
                attendees_str = ' / '.join(meeting['attendees'][:3])
                md += f"### {attendees_str}\n"
                if meeting['date']:
                    md += f"*{meeting['date']}*\n\n"
                
                for action in meeting_actions:
                    md += f"- **{action['owner']}**: {action['task']}\n"
                md += "\n"
        
        md += "\n---\n\n## 💡 Next Steps\n\n"
        md += "1. Review and prioritize action items above\n"
        md += "2. Add high-priority items to your task management system\n"
        md += "3. Schedule time blocks for key deliverables\n"
        md += "4. Follow up with stakeholders as needed\n\n"
        
        return md
    
    def generate_summary(self, weeks_back: int = 1, output_filename: str = None) -> str:
        """Generate the weekly meeting summary.
        
        Args:
            weeks_back: Number of weeks to include (default: 1 = last week only)
            output_filename: Custom output filename (optional)
            
        Returns:
            Path to the generated summary file
        """
        logger.info(f"Generating weekly meeting summary for the last {weeks_back} week(s)")
        
        # Get date range
        start_date, end_date = self.get_date_range(weeks_back)
        logger.info(f"Date range: {start_date} to {end_date}")
        
        # Search for Gemini notes
        files = self.search_gemini_notes(start_date, end_date)
        
        if not files:
            logger.warning("No Gemini meeting notes found for the specified period")
            return None
        
        # Process each meeting note
        meetings = []
        all_actions = []
        
        for file_info in files:
            file_id = file_info.get('id')
            file_title = file_info.get('name', 'Unknown Meeting')
            
            # Only process files where Eamon is likely an attendee
            if 'Eamon' not in file_title:
                continue
            
            logger.info(f"Processing: {file_title}")
            
            # Read the meeting note
            note_data = self.read_meeting_note(file_id)
            if not note_data:
                continue
            
            # Get content (handle both structured and simple formats)
            content = ''
            if 'content' in note_data:
                content = note_data['content']
            elif 'tabs' in note_data:
                # Concatenate all tab content
                content = '\n\n'.join(tab.get('content', '') for tab in note_data['tabs'])
            
            # Extract metadata
            metadata = self.extract_meeting_metadata(content, file_title)
            meetings.append(metadata)
            
            # Extract action items
            actions = self.extract_action_items(content)
            for action in actions:
                action['meeting_title'] = file_title
                action['meeting_date'] = metadata['date']
                all_actions.append(action)
            
            logger.info(f"Found {len(actions)} action items")
        
        # Group actions by owner
        actions_by_owner = self.group_actions_by_owner(all_actions)
        
        # Generate markdown summary
        summary_content = self.generate_summary_markdown(meetings, actions_by_owner, start_date, end_date)
        
        # Determine output filename
        if not output_filename:
            week_start = datetime.fromisoformat(start_date)
            output_filename = f"weekly-summary-{week_start.strftime('%Y-%m-%d')}.md"
        
        # Write to file
        output_path = self.output_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        logger.info(f"Weekly summary generated: {output_path}")
        return str(output_path)


def main():
    """Main entry point."""
    logger.info("Starting weekly meeting summary generation")
    
    # Parse command line arguments
    weeks_back = 1
    if len(sys.argv) > 1:
        try:
            weeks_back = int(sys.argv[1])
            logger.info(f"Generating summary for the last {weeks_back} week(s)")
        except ValueError:
            logger.error(f"Invalid weeks_back value: {sys.argv[1]}. Must be an integer.")
            sys.exit(1)
    
    # Generate the summary
    generator = WeeklyMeetingSummaryGenerator()
    summary_path = generator.generate_summary(weeks_back)
    
    if summary_path:
        logger.info(f"✅ Weekly summary successfully generated: {summary_path}")
        print(f"\n✅ Weekly summary saved to: {summary_path}\n")
        sys.exit(0)
    else:
        logger.error("❌ Failed to generate weekly summary")
        sys.exit(1)


if __name__ == "__main__":
    main()


