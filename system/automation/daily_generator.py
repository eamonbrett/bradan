#!/usr/bin/env python3
"""Main script for generating daily task management files."""

import logging
import sys
from datetime import date, datetime
from pathlib import Path

# Add the automation directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    PROJECT_ROOT, DAILY_DIR, DAILY_TEMPLATE, DAILY_FILE_PATTERN,
    CHECK_EXISTING_FILES, LOG_FILE, LOG_LEVEL, ensure_directories
)
from template_processor import TemplateProcessor, create_daily_context
from calendar_sync import CalendarSync

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

class DailyFileGenerator:
    """Main class for generating daily task management files."""
    
    def __init__(self):
        self.template_processor = TemplateProcessor(DAILY_TEMPLATE)
        self.calendar_sync = CalendarSync()
        ensure_directories()
    
    def generate_daily_file(self, target_date: date = None) -> bool:
        """Generate a daily file for the specified date.
        
        Args:
            target_date: Date to generate file for (defaults to today)
            
        Returns:
            bool: True if file was generated successfully, False otherwise
        """
        if target_date is None:
            target_date = date.today()
        
        logger.info(f"Generating daily file for {target_date}")
        
        # Check if file already exists
        daily_file_path = self._get_daily_file_path(target_date)
        if CHECK_EXISTING_FILES and daily_file_path.exists():
            logger.info(f"Daily file already exists: {daily_file_path}")
            return True
        
        try:
            # Get calendar events
            logger.info("Fetching calendar events...")
            calendar_events = self.calendar_sync.get_formatted_events(target_date)
            logger.info(f"Found {len(calendar_events)} calendar events")
            
            # Create template context
            context = create_daily_context(target_date, calendar_events)
            
            # Process template
            logger.info("Processing template...")
            daily_content = self.template_processor.process_template(context)
            
            # Write daily file
            logger.info(f"Writing daily file: {daily_file_path}")
            self._write_daily_file(daily_file_path, daily_content)
            
            # Create meeting file stubs if needed
            self._create_meeting_stubs(target_date, calendar_events)
            
            logger.info(f"Successfully generated daily file: {daily_file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating daily file: {e}")
            return False
    
    def _get_daily_file_path(self, target_date: date) -> Path:
        """Get the file path for a daily file."""
        filename = DAILY_FILE_PATTERN.format(date=target_date.strftime('%Y-%m-%d'))
        return DAILY_DIR / filename
    
    def _write_daily_file(self, file_path: Path, content: str):
        """Write content to daily file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Error writing daily file {file_path}: {e}")
            raise
    
    def _create_meeting_stubs(self, target_date: date, events: list):
        """Create meeting file stubs for calendar events."""
        from config import MEETINGS_DIR, MEETING_FILE_PATTERN
        
        for event in events:
            try:
                # Create meeting slug
                title = event.get('title', 'meeting')
                meeting_slug = self._create_meeting_slug(title)
                
                # Create meeting file path
                filename = MEETING_FILE_PATTERN.format(
                    date=target_date.strftime('%Y-%m-%d'),
                    meeting_slug=meeting_slug
                )
                meeting_path = MEETINGS_DIR / filename
                
                # Skip if file already exists
                if meeting_path.exists():
                    continue
                
                # Create basic meeting file content
                meeting_content = self._create_meeting_content(event, target_date)
                
                # Write meeting file
                with open(meeting_path, 'w', encoding='utf-8') as f:
                    f.write(meeting_content)
                
                logger.info(f"Created meeting stub: {meeting_path}")
                
            except Exception as e:
                logger.warning(f"Error creating meeting stub for {event.get('title', 'unknown')}: {e}")
    
    def _create_meeting_slug(self, title: str) -> str:
        """Create a URL-friendly slug from meeting title."""
        import re
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')[:50] if slug else 'meeting'
    
    def _create_meeting_content(self, event: dict, target_date: date) -> str:
        """Create enhanced meeting file content with recording/transcript sections."""
        title = event.get('title', 'Meeting')
        start_time = event.get('start_time', '')
        end_time = event.get('end_time', '')
        attendees = ', '.join(event.get('attendees', []))
        location = event.get('location', '')
        meet_link = event.get('meet_link', '')
        description = event.get('description', '')
        
        # Format time range
        time_range = f"{start_time}"
        if end_time and end_time != start_time:
            time_range += f" - {end_time}"
        
        # Add meet link to location if available
        if meet_link and not location:
            location = f"Google Meet: {meet_link}"
        elif meet_link and location:
            location += f" (Google Meet: {meet_link})"
        
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

{description}
"""

def main():
    """Main entry point."""
    logger.info("Starting daily file generation")
    
    generator = DailyFileGenerator()
    
    # Generate file for today by default
    target_date = date.today()
    
    # Check command line arguments for custom date
    if len(sys.argv) > 1:
        try:
            target_date = datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
            logger.info(f"Using custom date: {target_date}")
        except ValueError:
            logger.error(f"Invalid date format: {sys.argv[1]}. Use YYYY-MM-DD format.")
            sys.exit(1)
    
    # Generate the daily file
    success = generator.generate_daily_file(target_date)
    
    if success:
        logger.info("Daily file generation completed successfully")
        sys.exit(0)
    else:
        logger.error("Daily file generation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
