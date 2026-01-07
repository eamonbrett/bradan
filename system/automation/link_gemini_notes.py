"""
Link Gemini Meeting Notes to Meeting Stubs

This script searches Google Drive for Gemini meeting notes and automatically
links them to meeting stub files, extracting action items and summaries.

Usage (via Cursor):
    "Link Gemini notes for today's meetings"
    "Link Gemini notes for yesterday"
    "Link Gemini note for [meeting name]"
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Configuration
MEETINGS_DIR = Path(__file__).parent.parent / "meetings"


class GeminiNotesLinker:
    """Links Gemini meeting notes to meeting stub files."""
    
    # Common Gemini transcription errors (spelling corrections)
    NAME_CORRECTIONS = {
        "Burke": "Birk Angermann",
        "Deian": "Deann Evans",
        "Dian": "Deann Evans",
        "Dean": "Deann Evans",
    }
    
    def __init__(self):
        self.meetings_dir = MEETINGS_DIR
        
    def find_meeting_stubs(self, date: str) -> List[Path]:
        """
        Find all meeting stub files for a given date.
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            List of Path objects for meeting stubs
        """
        stubs = []
        
        # Check main meetings directory
        pattern = f"{date}-*.md"
        for stub in self.meetings_dir.glob(pattern):
            if stub.name != "template-meeting.md":
                stubs.append(stub)
        
        # Check subdirectories (1-on-1s, recurring, projects)
        for subdir in ["1-on-1s", "recurring", "projects"]:
            subdir_path = self.meetings_dir / subdir
            if subdir_path.exists():
                for stub in subdir_path.rglob(pattern):
                    stubs.append(stub)
        
        # Check archive directory
        archive_dir = self.meetings_dir / "archive"
        if archive_dir.exists():
            for stub in archive_dir.rglob(pattern):
                if "template" not in stub.name.lower():
                    stubs.append(stub)
        
        return stubs
    
    def extract_meeting_title(self, stub_path: Path) -> str:
        """
        Extract meeting title from stub file.
        
        Args:
            stub_path: Path to meeting stub file
            
        Returns:
            Meeting title
        """
        with open(stub_path, 'r') as f:
            content = f.read()
        
        # Look for title in first heading
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1)
        
        # Fallback to filename
        return stub_path.stem.replace(f"{stub_path.stem.split('-')[0]}-", "")
    
    def check_if_already_linked(self, stub_path: Path) -> bool:
        """
        Check if stub already has Gemini notes linked.
        
        Args:
            stub_path: Path to meeting stub
            
        Returns:
            True if already linked
        """
        with open(stub_path, 'r') as f:
            content = f.read()
        
        return "## Meeting Notes" in content or "Gemini Recording" in content
    
    def correct_names(self, text: str) -> str:
        """
        Correct common Gemini transcription errors in names.
        
        Args:
            text: Text to correct
            
        Returns:
            Corrected text
        """
        corrected = text
        for wrong, correct in self.NAME_CORRECTIONS.items():
            # Match whole words only to avoid partial replacements
            corrected = re.sub(r'\b' + re.escape(wrong) + r'\b', correct, corrected)
        return corrected
    
    def extract_gemini_summary(self, gemini_content: str) -> Dict[str, any]:
        """
        Extract key information from Gemini meeting notes.
        
        Args:
            gemini_content: Full Gemini notes content
            
        Returns:
            Dictionary with summary, action_items, decisions
        """
        # Correct common name misspellings first
        corrected_content = self.correct_names(gemini_content)
        
        # This will be filled in when we have actual Gemini note structure
        # For now, return placeholders
        return {
            "summary": "Meeting notes available - see Gemini doc for full details",
            "action_items": [],
            "decisions": []
        }
    
    def update_stub_with_notes(
        self, 
        stub_path: Path, 
        gemini_link: str,
        gemini_summary: Dict[str, any]
    ) -> bool:
        """
        Update meeting stub with Gemini notes link and extracted content.
        
        Args:
            stub_path: Path to meeting stub
            gemini_link: URL to Gemini notes
            gemini_summary: Extracted summary/actions/decisions
            
        Returns:
            True if updated successfully
        """
        with open(stub_path, 'r') as f:
            content = f.read()
        
        # Check if already has meeting notes section
        if "## Meeting Notes" in content:
            print(f"⚠️  {stub_path.name} already has meeting notes - skipping")
            return False
        
        # Build the meeting notes section
        notes_section = f"""

## Meeting Notes

📎 **[Gemini Recording & Notes]({gemini_link})**

**Summary:**
{gemini_summary.get('summary', 'See Gemini doc for full details')}
"""
        
        # Add action items if present
        if gemini_summary.get('action_items'):
            notes_section += "\n## Action Items\n"
            for item in gemini_summary['action_items']:
                notes_section += f"- [ ] {item}\n"
        
        # Add decisions if present
        if gemini_summary.get('decisions'):
            notes_section += "\n## Decisions\n"
            for decision in gemini_summary['decisions']:
                notes_section += f"- {decision}\n"
        
        # Insert before any existing action items or at the end
        if "## Action Items" in content and not gemini_summary.get('action_items'):
            # Insert before existing action items
            content = content.replace("## Action Items", notes_section + "\n## Action Items")
        else:
            # Append to end
            content += notes_section
        
        # Write back
        with open(stub_path, 'w') as f:
            f.write(content)
        
        return True
    
    def link_notes_for_date(
        self,
        date: str,
        gemini_docs: List[Dict[str, str]]
    ) -> Dict[str, int]:
        """
        Link Gemini notes to all meeting stubs for a given date.
        
        Args:
            date: Date in YYYY-MM-DD format
            gemini_docs: List of dicts with 'title', 'link', 'content' from Drive
            
        Returns:
            Dict with stats (linked, skipped, not_found)
        """
        stubs = self.find_meeting_stubs(date)
        
        stats = {
            "linked": 0,
            "skipped": 0,
            "not_found": 0
        }
        
        for stub in stubs:
            # Skip if already linked
            if self.check_if_already_linked(stub):
                print(f"⏭️  {stub.name} - Already linked")
                stats["skipped"] += 1
                continue
            
            # Extract meeting title from stub
            stub_title = self.extract_meeting_title(stub)
            
            # Try to find matching Gemini doc
            matched_doc = None
            for doc in gemini_docs:
                # Simple fuzzy matching on title
                if self._titles_match(stub_title, doc.get('title', '')):
                    matched_doc = doc
                    break
            
            if matched_doc:
                # Extract summary from Gemini content
                summary = self.extract_gemini_summary(matched_doc.get('content', ''))
                
                # Update stub
                if self.update_stub_with_notes(stub, matched_doc['link'], summary):
                    print(f"✅ {stub.name} - Linked to Gemini notes")
                    stats["linked"] += 1
                else:
                    stats["skipped"] += 1
            else:
                print(f"❌ {stub.name} - No matching Gemini doc found")
                stats["not_found"] += 1
        
        return stats
    
    def _titles_match(self, stub_title: str, gemini_title: str) -> bool:
        """
        Check if meeting titles match (fuzzy matching).
        
        Args:
            stub_title: Title from stub file
            gemini_title: Title from Gemini doc
            
        Returns:
            True if titles likely refer to same meeting
        """
        # Normalize titles
        stub_norm = stub_title.lower().strip()
        gemini_norm = gemini_title.lower().strip()
        
        # Remove common prefixes/dates
        stub_norm = re.sub(r'^\d{4}-\d{2}-\d{2}\s*-?\s*', '', stub_norm)
        
        # Exact match
        if stub_norm == gemini_norm:
            return True
        
        # Contains match (either direction)
        if stub_norm in gemini_norm or gemini_norm in stub_norm:
            return True
        
        # Key word overlap (for longer titles)
        stub_words = set(re.findall(r'\w+', stub_norm))
        gemini_words = set(re.findall(r'\w+', gemini_norm))
        
        # If 70%+ words overlap, consider it a match
        if len(stub_words) > 2 and len(gemini_words) > 2:
            overlap = len(stub_words & gemini_words)
            return overlap / len(stub_words) >= 0.7
        
        return False


def link_notes_command(date_str: str, gemini_docs: List[Dict]) -> Dict:
    """
    Command interface for linking Gemini notes.
    
    Args:
        date_str: Date string (YYYY-MM-DD, "today", "yesterday")
        gemini_docs: List of Gemini docs from Drive search
        
    Returns:
        Stats dictionary
    """
    # Parse date
    if date_str.lower() == "today":
        date = datetime.now().strftime("%Y-%m-%d")
    elif date_str.lower() == "yesterday":
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        date = date_str
    
    # Link notes
    linker = GeminiNotesLinker()
    stats = linker.link_notes_for_date(date, gemini_docs)
    
    # Print summary
    print(f"\n📊 Summary for {date}:")
    print(f"   ✅ Linked: {stats['linked']}")
    print(f"   ⏭️  Skipped (already linked): {stats['skipped']}")
    print(f"   ❌ Not found: {stats['not_found']}")
    
    return stats


if __name__ == "__main__":
    print("This script is meant to be called from Cursor/Claude")
    print('Usage: "Link Gemini notes for today\'s meetings"')

