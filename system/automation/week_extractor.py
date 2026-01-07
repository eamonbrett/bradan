"""
Week Extractor - Auto-populate weekly files from daily work

Extracts from:
- Daily files (completed tasks, incomplete items, patterns)
- Meeting notes (decisions, action items)
- Decision logs (new this week)
- Project updates (changes this week)
- Calendar events (meeting count, time allocation)
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

class WeekExtractor:
    def __init__(self, base_dir: str = None):
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            # Default to project root (two levels up from system/automation/)
            self.base_dir = Path(__file__).parent.parent.parent
        
        # Use work/ directory structure
        self.daily_dir = self.base_dir / "work" / "daily"
        self.meetings_dir = self.base_dir / "work" / "meetings"
        self.decisions_dir = self.base_dir / "reference" / "decisions"
        self.archive_dir = self.base_dir / "archive" / "daily"
    
    def find_week_files(self, week_start: datetime) -> Dict[str, List[Path]]:
        """Find all files for a given week."""
        week_dates = [week_start + timedelta(days=i) for i in range(7)]
        
        files = {
            'dailies': [],
            'meetings': [],
            'decisions': []
        }
        
        # Find daily files (check both daily/ and archive/)
        for date in week_dates:
            date_str = date.strftime('%Y-%m-%d')
            
            # Check daily folder first
            daily_file = self.daily_dir / f"{date_str}.md"
            if daily_file.exists():
                files['dailies'].append(daily_file)
            else:
                # Check archive
                week_num = date.isocalendar()[1]
                archive_week = self.archive_dir / f"{date.year}-{date.month:02d}-week-{week_num}"
                archived_file = archive_week / f"{date_str}.md"
                if archived_file.exists():
                    files['dailies'].append(archived_file)
        
        # Find meeting files for this week
        for date in week_dates:
            date_str = date.strftime('%Y-%m-%d')
            for meeting_file in self.meetings_dir.glob(f"{date_str}-*.md"):
                files['meetings'].append(meeting_file)
        
        # Find decision logs for this week
        for date in week_dates:
            date_str = date.strftime('%Y-%m')
            for decision_file in self.decisions_dir.glob(f"{date_str}-*.md"):
                files['decisions'].append(decision_file)
        
        return files
    
    def extract_completed_tasks(self, daily_files: List[Path]) -> List[str]:
        """Extract completed tasks (checked checkboxes) from daily files."""
        completed = []
        
        for daily_file in daily_files:
            try:
                content = daily_file.read_text()
                
                # Find all completed tasks: - [x] or - [X]
                pattern = r'^- \[x\] (.+)$'
                matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
                
                for task in matches:
                    # Clean up the task text
                    task = task.strip()
                    if task and not task.startswith('['):
                        completed.append(task)
                        
            except Exception as e:
                print(f"Error reading {daily_file}: {e}")
        
        # Deduplicate while preserving order
        seen = set()
        unique_completed = []
        for task in completed:
            task_lower = task.lower()
            if task_lower not in seen:
                seen.add(task_lower)
                unique_completed.append(task)
        
        return unique_completed
    
    def extract_incomplete_tasks(self, daily_files: List[Path]) -> List[str]:
        """Extract incomplete tasks (unchecked checkboxes) from daily files."""
        incomplete = []
        
        for daily_file in daily_files:
            try:
                content = daily_file.read_text()
                
                # Find all incomplete tasks: - [ ]
                pattern = r'^- \[ \] (.+)$'
                matches = re.findall(pattern, content, re.MULTILINE)
                
                for task in matches:
                    task = task.strip()
                    if task and not task.startswith('['):
                        incomplete.append(task)
                        
            except Exception as e:
                print(f"Error reading {daily_file}: {e}")
        
        # Deduplicate
        seen = set()
        unique_incomplete = []
        for task in incomplete:
            task_lower = task.lower()
            if task_lower not in seen:
                seen.add(task_lower)
                unique_incomplete.append(task)
        
        return unique_incomplete
    
    def extract_meeting_outcomes(self, meeting_files: List[Path]) -> List[Dict]:
        """Extract key decisions and action items from meeting files."""
        outcomes = []
        
        for meeting_file in meeting_files:
            try:
                content = meeting_file.read_text()
                
                # Extract meeting title
                title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else meeting_file.stem
                
                outcome = {
                    'meeting': title,
                    'file': str(meeting_file.relative_to(self.base_dir)),
                    'decisions': [],
                    'actions': []
                }
                
                # Extract decisions
                decisions_section = re.search(r'## Decisions Made(.+?)(?=##|\Z)', content, re.DOTALL)
                if decisions_section:
                    decisions_text = decisions_section.group(1)
                    # Find decision patterns
                    decision_patterns = [
                        r'\*\*Decision:\*\* (.+?)(?=\n|$)',
                        r'- \*\*Decision:\*\* (.+?)(?=\n|$)'
                    ]
                    for pattern in decision_patterns:
                        matches = re.findall(pattern, decisions_text, re.MULTILINE)
                        outcome['decisions'].extend(matches)
                
                # Extract action items
                actions_section = re.search(r'## Action Items(.+?)(?=##|\Z)', content, re.DOTALL)
                if actions_section:
                    actions_text = actions_section.group(1)
                    # Find unchecked action items
                    action_pattern = r'^- \[ \] (.+)$'
                    matches = re.findall(action_pattern, actions_text, re.MULTILINE)
                    outcome['actions'].extend(matches)
                
                # Only add if there are decisions or actions
                if outcome['decisions'] or outcome['actions']:
                    outcomes.append(outcome)
                    
            except Exception as e:
                print(f"Error reading {meeting_file}: {e}")
        
        return outcomes
    
    def extract_decision_logs(self, decision_files: List[Path]) -> List[Dict]:
        """Extract decision logs created this week."""
        decisions = []
        
        for decision_file in decision_files:
            try:
                content = decision_file.read_text()
                
                # Extract title
                title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else decision_file.stem
                
                # Extract status
                status_match = re.search(r'\*\*Status:\*\* (.+)', content)
                status = status_match.group(1) if status_match else "Unknown"
                
                decisions.append({
                    'title': title,
                    'file': str(decision_file.relative_to(self.base_dir)),
                    'status': status
                })
                
            except Exception as e:
                print(f"Error reading {decision_file}: {e}")
        
        return decisions
    
    def extract_top3_priorities(self, daily_files: List[Path]) -> List[str]:
        """Extract Top 3 priorities from daily files to see patterns."""
        all_priorities = []
        
        for daily_file in daily_files:
            try:
                content = daily_file.read_text()
                
                # Find Top 3 section
                top3_section = re.search(r'## 🔥 Top 3 Tasks Today(.+?)(?=##|\Z)', content, re.DOTALL)
                if top3_section:
                    section_text = top3_section.group(1)
                    
                    # Extract priority titles (### lines)
                    priority_pattern = r'^### \d\.\s+\*\*(.+?)\*\*'
                    matches = re.findall(priority_pattern, section_text, re.MULTILINE)
                    all_priorities.extend(matches)
                    
            except Exception as e:
                print(f"Error reading {daily_file}: {e}")
        
        return all_priorities
    
    def count_meetings(self, meeting_files: List[Path]) -> int:
        """Count meetings for the week."""
        return len(meeting_files)
    
    def generate_week_data(self, week_start: datetime) -> Dict:
        """Generate all extracted data for a week."""
        print(f"Extracting data for week of {week_start.strftime('%Y-%m-%d')}...")
        
        files = self.find_week_files(week_start)
        
        print(f"Found {len(files['dailies'])} daily files, {len(files['meetings'])} meetings, {len(files['decisions'])} decisions")
        
        data = {
            'week_start': week_start,
            'week_end': week_start + timedelta(days=4),  # Friday
            'completed_tasks': self.extract_completed_tasks(files['dailies']),
            'incomplete_tasks': self.extract_incomplete_tasks(files['dailies']),
            'meeting_outcomes': self.extract_meeting_outcomes(files['meetings']),
            'decision_logs': self.extract_decision_logs(files['decisions']),
            'priorities_worked': self.extract_top3_priorities(files['dailies']),
            'meeting_count': self.count_meetings(files['meetings']),
            'files': files
        }
        
        return data


def extract_week_data(week_start_str: str) -> Dict:
    """
    Extract data for a week.
    
    Args:
        week_start_str: Date string in YYYY-MM-DD format (Monday)
    
    Returns:
        Dictionary with all extracted data
    """
    week_start = datetime.strptime(week_start_str, '%Y-%m-%d')
    
    extractor = WeekExtractor()
    return extractor.generate_week_data(week_start)


if __name__ == "__main__":
    # Test with current week
    import sys
    
    if len(sys.argv) > 1:
        week_start = sys.argv[1]
    else:
        # Default to current Monday
        today = datetime.now()
        days_since_monday = today.weekday()
        monday = today - timedelta(days=days_since_monday)
        week_start = monday.strftime('%Y-%m-%d')
    
    data = extract_week_data(week_start)
    
    print(f"\n=== Week of {week_start} ===")
    print(f"\nCompleted: {len(data['completed_tasks'])} tasks")
    print(f"Incomplete: {len(data['incomplete_tasks'])} tasks")
    print(f"Meetings: {data['meeting_count']}")
    print(f"Decisions logged: {len(data['decision_logs'])}")

