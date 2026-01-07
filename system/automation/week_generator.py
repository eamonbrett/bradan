"""
Week Generator - Create consolidated weekly files with auto-populated data

Combines weekly plan + weekly summary + weekly review into ONE file
that's 90% auto-populated from your actual work.
"""

from datetime import datetime, timedelta
from pathlib import Path
from week_extractor import extract_week_data
from priority_recommender import PriorityRecommender


def generate_week_file(week_start_str: str, base_dir: str = None) -> dict:
    """
    Generate a consolidated week file.
    
    Args:
        week_start_str: Monday date in YYYY-MM-DD format
        base_dir: Base directory (optional)
    
    Returns:
        dict with file_path and data
    """
    week_start = datetime.strptime(week_start_str, '%Y-%m-%d')
    week_end = week_start + timedelta(days=4)
    week_num = week_start.isocalendar()[1]
    
    # Set up paths
    if base_dir:
        base_path = Path(base_dir)
    else:
        # Default to project root (three levels up from system/automation/)
        base_path = Path(__file__).parent.parent.parent
    
    weeks_dir = base_path / "work" / "weeks"
    weeks_dir.mkdir(exist_ok=True)
    
    filename = f"{week_start_str}-week-{week_num}.md"
    filepath = weeks_dir / filename
    
    # Check if this is a new week (Monday setup) or end-of-week (Friday reflection)
    today = datetime.now()
    is_setup = today.weekday() == 0  # Monday
    is_reflection = today.weekday() == 4  # Friday
    
    # Extract data from last week if this is Monday setup
    if is_setup:
        last_week_start = week_start - timedelta(days=7)
        last_week_data = extract_week_data(last_week_start.strftime('%Y-%m-%d'))
    else:
        last_week_data = None
    
    # Extract data from this week if this is Friday or later
    if is_reflection or today >= week_end:
        this_week_data = extract_week_data(week_start_str)
    else:
        this_week_data = None
    
    # Generate the content
    content = generate_week_content(
        week_start=week_start,
        week_end=week_end,
        week_num=week_num,
        last_week_data=last_week_data,
        this_week_data=this_week_data,
        is_setup=is_setup,
        is_reflection=is_reflection
    )
    
    # Write file
    filepath.write_text(content)
    
    return {
        'file_path': str(filepath),
        'week_start': week_start_str,
        'week_end': week_end.strftime('%Y-%m-%d'),
        'last_week_data': last_week_data,
        'this_week_data': this_week_data
    }


def generate_week_content(week_start, week_end, week_num, last_week_data, this_week_data, is_setup, is_reflection):
    """Generate the consolidated week file content."""
    
    week_start_str = week_start.strftime('%Y-%m-%d')
    week_end_str = week_end.strftime('%Y-%m-%d')
    week_display = week_start.strftime('%b %d') + " - " + week_end.strftime('%b %d, %Y')
    
    content = f"""# Week of {week_display}

**Week Number:** {week_num}  
**Dates:** {week_start_str} to {week_end_str}  
**Archive:** [[archive/daily/{week_start.year}-{week_start.month:02d}-week-{week_num}/]]

---

"""
    
    # MONDAY SETUP SECTION (if generating on Monday)
    if is_setup and last_week_data:
        content += generate_monday_setup(last_week_data)
    
    # WHAT ACTUALLY HAPPENED (if generating on Friday or later)
    if this_week_data:
        content += generate_what_happened(this_week_data)
    
    # FRIDAY REFLECTION SECTION (always included, filled on Friday)
    content += generate_reflection_section(is_reflection)
    
    return content


def generate_monday_setup(last_week_data):
    """Generate the Monday morning setup section."""
    
    section = """## 📋 Monday Setup (2 Minutes)

*Auto-generated from last week's reality*

### What Carried Forward from Last Week

"""
    
    # Collect all carry-forwards
    all_carry_forwards = []
    
    # Incomplete tasks from last week
    if last_week_data['incomplete_tasks']:
        section += "**Unfinished Work:**\n"
        for task in last_week_data['incomplete_tasks'][:10]:  # Top 10
            section += f"- [ ] {task}\n"
            all_carry_forwards.append(task)
        section += "\n"
    
    # Meeting actions that didn't get done
    incomplete_actions = []
    for meeting in last_week_data['meeting_outcomes']:
        for action in meeting['actions']:
            action_text = f"{action} (from {meeting['meeting']})"
            incomplete_actions.append(action_text)
            all_carry_forwards.append(action_text)
    
    if incomplete_actions:
        section += "**Meeting Action Items:**\n"
        for action in incomplete_actions[:5]:  # Top 5
            section += f"- [ ] {action}\n"
        section += "\n"
    
    # Generate smart recommendations
    if all_carry_forwards:
        try:
            recommender = PriorityRecommender()
            recommendations = recommender.recommend_top3(all_carry_forwards)
            
            section += """### Your Top 3 Priorities This Week

*Recommended based on carry-forwards, urgency, and impact. Adjust as needed:*

"""
            
            for rec in recommendations:
                section += f"{rec['priority']}. **{rec['title']}** - {rec['category']}\n"
                section += f"   - Why: {rec['why']}\n"
                
                if rec.get('actions'):
                    section += f"   - Actions:\n"
                    for action in rec['actions'][:3]:
                        section += f"     - [ ] {action}\n"
                
                section += "\n"
            
        except Exception as e:
            # Fallback to template if recommendation fails
            section += """### Your Top 3 Priorities This Week

*Adjust based on carry-forwards above:*

1. **[Priority 1]** - 🎯 Strategic / 🤝 Stakeholder / 🔧 Operational
   - Why: [From carry-forwards]
   - Actions: [Key actions]
   
2. **[Priority 2]** - 🎯 Strategic / 🤝 Stakeholder / 🔧 Operational
   - Why: [From carry-forwards]
   - Actions: [Key actions]
   
3. **[Priority 3]** - 🎯 Strategic / 🤝 Stakeholder / 🔧 Operational
   - Why: [From carry-forwards]
   - Actions: [Key actions]

"""
    else:
        # No carry-forwards - fresh week
        section += """### Your Top 3 Priorities This Week

*Set your priorities for a fresh week:*

1. **[Priority 1]** - 🎯 Strategic / 🤝 Stakeholder / 🔧 Operational
   - Why: [Strategic focus]
   - Actions: [Key actions]
   
2. **[Priority 2]** - 🎯 Strategic / 🤝 Stakeholder / 🔧 Operational
   - Why: [Stakeholder alignment]
   - Actions: [Key actions]
   
3. **[Priority 3]** - 🎯 Strategic / 🤝 Stakeholder / 🔧 Operational
   - Why: [Operational needs]
   - Actions: [Key actions]

"""
    
    section += "---\n\n"
    
    return section


def generate_what_happened(week_data):
    """Generate the 'what actually happened' section."""
    
    section = f"""## ✅ What Actually Happened

*Auto-extracted from this week's daily files and meetings*

### Deliverables Completed ({len(week_data['completed_tasks'])} total)

"""
    
    # Completed tasks
    if week_data['completed_tasks']:
        for task in week_data['completed_tasks'][:15]:  # Top 15
            section += f"- ✅ {task}\n"
        
        if len(week_data['completed_tasks']) > 15:
            section += f"\n*...and {len(week_data['completed_tasks']) - 15} more completed tasks*\n"
    else:
        section += "*No completed tasks found in daily files*\n"
    
    section += "\n"
    
    # Decision logs created
    if week_data['decision_logs']:
        section += f"### Decisions Documented ({len(week_data['decision_logs'])} logs)\n\n"
        for decision in week_data['decision_logs']:
            section += f"- **{decision['title']}** - {decision['status']}\n"
            section += f"  - File: [[{decision['file']}]]\n"
        section += "\n"
    
    # Meetings that mattered
    if week_data['meeting_outcomes']:
        section += f"### Meetings That Mattered ({len(week_data['meeting_outcomes'])} with outcomes)\n\n"
        for meeting in week_data['meeting_outcomes']:
            section += f"**{meeting['meeting']}**\n"
            if meeting['decisions']:
                section += "- Decisions:\n"
                for decision in meeting['decisions'][:2]:  # Top 2
                    section += f"  - {decision}\n"
            if meeting['actions']:
                section += "- Actions:\n"
                for action in meeting['actions'][:3]:  # Top 3
                    section += f"  - {action}\n"
            section += "\n"
    
    # Time reality check
    section += f"""### Time Reality Check

- **Meetings:** {week_data['meeting_count']} meetings
- **Priorities worked:** {len(set(week_data['priorities_worked']))} different priorities across the week

"""
    
    # Patterns in priorities
    if week_data['priorities_worked']:
        priority_counts = {}
        for priority in week_data['priorities_worked']:
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        top_priorities = sorted(priority_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        section += "**Most worked priorities:**\n"
        for priority, count in top_priorities:
            section += f"- {priority} ({count} days)\n"
    
    section += "\n---\n\n"
    
    return section


def generate_reflection_section(is_filled):
    """Generate the Friday reflection section."""
    
    section = """## 💭 3-Minute Reflection (Friday)

"""
    
    if is_filled:
        section += "*Complete these 3 questions on Friday afternoon:*\n\n"
    else:
        section += "*Fill this out on Friday - auto-generated data above*\n\n"
    
    section += """### 1. What went really well?
**The biggest win or progress you're proud of:**

[Your answer - 1-2 sentences]

---

### 2. What would you do differently?
**One thing you'd change if you could do the week over:**

[Your answer - 1-2 sentences]

---

### 3. What's the key learning?
**One insight or pattern worth remembering:**

[Your answer - 1-2 sentences]

---

## ✅ Week Complete

**Reviewed:** [Date]  
**Next week:** [Next Monday date]  
**Next week's file:** [[weeks/[next-week-date]-week-[N].md]]

---

*5 minutes total: 2 min Monday setup + 3 min Friday reflection. That's it.*
"""
    
    return section


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        week_start = sys.argv[1]
    else:
        # Default to current Monday
        today = datetime.now()
        days_since_monday = today.weekday()
        monday = today - timedelta(days=days_since_monday)
        week_start = monday.strftime('%Y-%m-%d')
    
    result = generate_week_file(week_start)
    
    print(f"\n✅ Generated: {result['file_path']}")
    print(f"📅 Week: {result['week_start']} to {result['week_end']}")
    
    if result['last_week_data']:
        print(f"\n📊 Extracted from last week:")
        print(f"  - {len(result['last_week_data']['completed_tasks'])} completed tasks")
        print(f"  - {len(result['last_week_data']['incomplete_tasks'])} carry-forwards")
    
    if result['this_week_data']:
        print(f"\n📊 Extracted from this week:")
        print(f"  - {len(result['this_week_data']['completed_tasks'])} completed tasks")
        print(f"  - {result['this_week_data']['meeting_count']} meetings")

