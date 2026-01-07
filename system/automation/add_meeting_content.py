#!/usr/bin/env python3
"""
Helper script to add meeting recordings, transcripts, and artifacts to meeting files.

This script helps you quickly add meeting content after meetings are completed.
"""

import os
import sys
from datetime import date, datetime
from pathlib import Path
import re

def find_meeting_file(meeting_title: str, target_date: date = None) -> Path:
    """Find the meeting file for a given title and date."""
    if target_date is None:
        target_date = date.today()
    
    meetings_dir = Path("meetings")
    if not meetings_dir.exists():
        print(f"Meetings directory not found: {meetings_dir}")
        return None
    
    # Create slug from meeting title
    slug = re.sub(r'[^\w\s-]', '', meeting_title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip('-')[:50] if slug else 'meeting'
    
    # Look for matching file
    pattern = f"{target_date.strftime('%Y-%m-%d')}-{slug}.md"
    meeting_file = meetings_dir / pattern
    
    if meeting_file.exists():
        return meeting_file
    
    # If not found, list available files for the date
    print(f"Meeting file not found: {meeting_file}")
    print(f"Available meeting files for {target_date}:")
    for file in meetings_dir.glob(f"{target_date.strftime('%Y-%m-%d')}-*.md"):
        print(f"  - {file.name}")
    
    return None

def add_recording_link(meeting_file: Path, recording_url: str, duration: str = None, quality: str = None):
    """Add recording information to meeting file."""
    if not meeting_file.exists():
        print(f"Meeting file not found: {meeting_file}")
        return False
    
    try:
        with open(meeting_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace recording placeholders
        content = re.sub(
            r'\[Add Google Meet recording or other recording URL\]',
            recording_url,
            content
        )
        
        if duration:
            content = re.sub(
                r'\[Actual meeting duration\]',
                duration,
                content
            )
        
        if quality:
            content = re.sub(
                r'\[Good/Fair/Poor - any issues\?\]',
                quality,
                content
            )
        
        with open(meeting_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Added recording information to {meeting_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating meeting file: {e}")
        return False

def add_transcript_link(meeting_file: Path, transcript_url: str, auto_transcript: bool = None):
    """Add transcript information to meeting file."""
    if not meeting_file.exists():
        print(f"Meeting file not found: {meeting_file}")
        return False
    
    try:
        with open(meeting_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace transcript placeholders
        content = re.sub(
            r'\[Link to full transcript if available\]',
            transcript_url,
            content
        )
        
        if auto_transcript is not None:
            auto_text = "Yes" if auto_transcript else "No"
            content = re.sub(
                r'\[Yes/No - from Google Meet, Otter\.ai, etc\.\]',
                auto_text,
                content
            )
        
        with open(meeting_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Added transcript information to {meeting_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating meeting file: {e}")
        return False

def add_meeting_artifacts(meeting_file: Path, shared_content: str = None, whiteboard_notes: str = None, chat_log: str = None):
    """Add meeting artifacts to meeting file."""
    if not meeting_file.exists():
        print(f"Meeting file not found: {meeting_file}")
        return False
    
    try:
        with open(meeting_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace artifact placeholders
        if shared_content:
            content = re.sub(
                r'\[Links to shared documents, presentations\]',
                shared_content,
                content
            )
        
        if whiteboard_notes:
            content = re.sub(
                r'\[Links to collaborative notes, Miro boards, etc\.\]',
                whiteboard_notes,
                content
            )
        
        if chat_log:
            content = re.sub(
                r'\[Any important chat messages or links shared\]',
                chat_log,
                content
            )
        
        with open(meeting_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Added meeting artifacts to {meeting_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating meeting file: {e}")
        return False

def interactive_add_content():
    """Interactive mode to add meeting content."""
    print("=== Meeting Content Adder ===\n")
    
    # Get meeting title
    meeting_title = input("Enter meeting title: ").strip()
    if not meeting_title:
        print("❌ Meeting title is required")
        return
    
    # Get date
    date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if date_input:
        try:
            target_date = datetime.strptime(date_input, '%Y-%m-%d').date()
        except ValueError:
            print("❌ Invalid date format. Using today's date.")
            target_date = date.today()
    else:
        target_date = date.today()
    
    # Find meeting file
    meeting_file = find_meeting_file(meeting_title, target_date)
    if not meeting_file:
        return
    
    print(f"\nFound meeting file: {meeting_file}")
    
    # Add recording
    print("\n--- Recording Information ---")
    recording_url = input("Recording URL (or press Enter to skip): ").strip()
    if recording_url:
        duration = input("Meeting duration (e.g., '45 minutes'): ").strip()
        quality = input("Recording quality (Good/Fair/Poor): ").strip()
        add_recording_link(meeting_file, recording_url, duration, quality)
    
    # Add transcript
    print("\n--- Transcript Information ---")
    transcript_url = input("Transcript URL (or press Enter to skip): ").strip()
    if transcript_url:
        auto_transcript = input("Auto-transcript available? (y/n): ").strip().lower() == 'y'
        add_transcript_link(meeting_file, transcript_url, auto_transcript)
    
    # Add artifacts
    print("\n--- Meeting Artifacts ---")
    shared_content = input("Shared screen content/links (or press Enter to skip): ").strip()
    whiteboard_notes = input("Whiteboard/collaborative notes (or press Enter to skip): ").strip()
    chat_log = input("Important chat messages (or press Enter to skip): ").strip()
    
    if shared_content or whiteboard_notes or chat_log:
        add_meeting_artifacts(meeting_file, shared_content, whiteboard_notes, chat_log)
    
    print(f"\n✅ Meeting content added to {meeting_file}")

def main():
    """Main function."""
    if len(sys.argv) > 1:
        # Command line mode
        meeting_title = sys.argv[1]
        meeting_file = find_meeting_file(meeting_title)
        
        if meeting_file and len(sys.argv) > 2:
            recording_url = sys.argv[2]
            add_recording_link(meeting_file, recording_url)
        elif meeting_file:
            print(f"Found meeting file: {meeting_file}")
            print("Use interactive mode to add content, or provide recording URL as second argument")
        else:
            print("Meeting file not found")
    else:
        # Interactive mode
        interactive_add_content()

if __name__ == "__main__":
    main()




