"""
Priority Recommender - Suggest Top 3 priorities for the week

Analyzes:
- Carry-forward tasks (what's incomplete)
- Meeting schedule (what's coming up)
- Decision logs (what needs closure)
- Priority patterns (what you typically work on)
- Action items (what's assigned to you)
"""

import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple
from collections import Counter


class PriorityRecommender:
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent.parent.parent
        
        # Strategic keywords for categorization
        self.strategic_keywords = [
            '2026 planning', 'strategy', 'vision', 'transformation', 
            'craft', 'improvement', 'initiative', 'roadmap'
        ]
        self.stakeholder_keywords = [
            'andre', 'olivia', 'riley', 'deann', 'meeting', 'sync',
            'alignment', 'communication', 'stakeholder'
        ]
        self.operational_keywords = [
            'spif', 'compensation', 'review', 'approve', 'sign off',
            'validation', 'technical', 'analysis', 'investigation'
        ]
    
    def categorize_task(self, task: str) -> Tuple[str, int]:
        """
        Categorize a task and assign priority score.
        
        Returns:
            (category, priority_score)
            category: 'Strategic', 'Stakeholder', 'Operational'
            priority_score: 1-10 (higher = more important)
        """
        task_lower = task.lower()
        
        # Check for urgency indicators
        urgency_boost = 0
        if any(word in task_lower for word in ['urgent', 'asap', 'critical', 'blocked', 'waiting']):
            urgency_boost = 3
        if any(word in task_lower for word in ['this week', 'monday', 'today']):
            urgency_boost = 2
        
        # Check for impact indicators
        impact_boost = 0
        if any(word in task_lower for word in ['decision', 'approval', 'sign off', 'review']):
            impact_boost = 2
        if any(word in task_lower for word in ['team', 'se', 'leadership', 'regional']):
            impact_boost = 1
        
        # Categorize
        strategic_score = sum(1 for kw in self.strategic_keywords if kw in task_lower)
        stakeholder_score = sum(1 for kw in self.stakeholder_keywords if kw in task_lower)
        operational_score = sum(1 for kw in self.operational_keywords if kw in task_lower)
        
        if strategic_score >= stakeholder_score and strategic_score >= operational_score:
            category = 'Strategic'
            base_score = 8  # Strategic is typically highest priority
        elif stakeholder_score >= operational_score:
            category = 'Stakeholder'
            base_score = 7
        else:
            category = 'Operational'
            base_score = 6
        
        total_score = base_score + urgency_boost + impact_boost
        
        return category, min(total_score, 10)  # Cap at 10
    
    def extract_upcoming_meetings(self, week_start: datetime) -> List[Dict]:
        """Extract meetings scheduled for this week (requires calendar data passed in)."""
        # This would need calendar data passed from Cursor
        # For now, return empty list - Claude will pass calendar data
        return []
    
    def analyze_carry_forwards(self, carry_forwards: List[str]) -> List[Dict]:
        """Analyze and prioritize carry-forward tasks."""
        analyzed = []
        
        for task in carry_forwards:
            category, score = self.categorize_task(task)
            
            analyzed.append({
                'task': task,
                'category': category,
                'score': score,
                'reasons': self._explain_priority(task, category, score)
            })
        
        # Sort by score (highest first)
        analyzed.sort(key=lambda x: x['score'], reverse=True)
        
        return analyzed
    
    def _explain_priority(self, task: str, category: str, score: int) -> List[str]:
        """Explain why this task has this priority."""
        reasons = []
        task_lower = task.lower()
        
        # Urgency reasons
        if 'urgent' in task_lower or 'asap' in task_lower:
            reasons.append("Marked as urgent")
        if 'blocked' in task_lower or 'waiting' in task_lower:
            reasons.append("Blocking others")
        if 'approval' in task_lower or 'decision' in task_lower:
            reasons.append("Decision required")
        
        # Impact reasons
        if 'team' in task_lower or 'leadership' in task_lower:
            reasons.append("Team impact")
        if any(name in task_lower for name in ['andre', 'riley', 'olivia', 'deann']):
            reasons.append("Key stakeholder")
        
        # Strategic reasons
        if '2026' in task_lower or 'planning' in task_lower:
            reasons.append("Strategic planning")
        if 'craft' in task_lower or 'improvement' in task_lower:
            reasons.append("SE Craft advancement")
        
        return reasons if reasons else ["Carry-forward from last week"]
    
    def group_by_category(self, analyzed_tasks: List[Dict]) -> Dict[str, List[Dict]]:
        """Group analyzed tasks by category."""
        groups = {
            'Strategic': [],
            'Stakeholder': [],
            'Operational': []
        }
        
        for task in analyzed_tasks:
            groups[task['category']].append(task)
        
        return groups
    
    def recommend_top3(
        self, 
        carry_forwards: List[str],
        calendar_events: List[Dict] = None,
        pending_decisions: List[str] = None
    ) -> List[Dict]:
        """
        Recommend Top 3 priorities for the week.
        
        Args:
            carry_forwards: Incomplete tasks from last week
            calendar_events: (Optional) Meetings scheduled this week
            pending_decisions: (Optional) Decisions that need closure
        
        Returns:
            List of 3 recommended priorities with reasoning
        """
        # Analyze carry-forwards
        analyzed = self.analyze_carry_forwards(carry_forwards)
        
        # Group by category
        grouped = self.group_by_category(analyzed)
        
        # Build recommendations (aim for 1 of each category)
        recommendations = []
        
        # 1. Top Strategic (if any)
        if grouped['Strategic']:
            top_strategic = grouped['Strategic'][0]
            recommendations.append({
                'priority': 1,
                'title': self._extract_clean_title(top_strategic['task']),
                'category': '🎯 Strategic',
                'why': self._build_why_statement(top_strategic),
                'actions': self._extract_actions(top_strategic['task'], carry_forwards),
                'source': 'Carry-forward + strategic alignment'
            })
        
        # 2. Top Stakeholder (if any)
        if grouped['Stakeholder']:
            top_stakeholder = grouped['Stakeholder'][0]
            recommendations.append({
                'priority': len(recommendations) + 1,
                'title': self._extract_clean_title(top_stakeholder['task']),
                'category': '🤝 Stakeholder',
                'why': self._build_why_statement(top_stakeholder),
                'actions': self._extract_actions(top_stakeholder['task'], carry_forwards),
                'source': 'Carry-forward + stakeholder alignment'
            })
        
        # 3. Top Operational (if any)
        if grouped['Operational']:
            top_operational = grouped['Operational'][0]
            recommendations.append({
                'priority': len(recommendations) + 1,
                'title': self._extract_clean_title(top_operational['task']),
                'category': '🔧 Operational',
                'why': self._build_why_statement(top_operational),
                'actions': self._extract_actions(top_operational['task'], carry_forwards),
                'source': 'Carry-forward + operational needs'
            })
        
        # Fill remaining slots if needed
        all_remaining = [t for t in analyzed if not any(
            t['task'] == r.get('task', '') for r in recommendations
        )]
        
        while len(recommendations) < 3 and all_remaining:
            next_task = all_remaining[0]
            recommendations.append({
                'priority': len(recommendations) + 1,
                'title': self._extract_clean_title(next_task['task']),
                'category': f"{'🎯' if next_task['category'] == 'Strategic' else '🤝' if next_task['category'] == 'Stakeholder' else '🔧'} {next_task['category']}",
                'why': self._build_why_statement(next_task),
                'actions': self._extract_actions(next_task['task'], carry_forwards),
                'source': 'Carry-forward'
            })
            all_remaining.pop(0)
        
        return recommendations[:3]
    
    def _extract_clean_title(self, task: str) -> str:
        """Extract a clean title from task text."""
        # Remove checkbox markup
        task = re.sub(r'^\s*-\s*\[[ x]\]\s*', '', task)
        
        # Try to extract the main action
        # Look for patterns like "Review X", "Complete Y", "Check Z"
        action_pattern = r'^(Review|Complete|Check|Update|Create|Generate|Prepare|Address|Follow up on|Document)\s+(.+?)(?:\s*-|$)'
        match = re.match(action_pattern, task, re.IGNORECASE)
        
        if match:
            action = match.group(1).title()
            subject = match.group(2).strip()
            # Limit length
            if len(subject) > 40:
                subject = subject[:40] + '...'
            return f"{action} {subject}"
        
        # Otherwise, use first 50 chars
        return task[:50] + ('...' if len(task) > 50 else '')
    
    def _build_why_statement(self, task_data: Dict) -> str:
        """Build a 'why' statement for a priority."""
        reasons = task_data.get('reasons', [])
        
        if not reasons:
            return "Carry-forward from last week"
        
        # Combine reasons into a statement
        if len(reasons) == 1:
            return reasons[0]
        elif len(reasons) == 2:
            return f"{reasons[0]} and {reasons[1].lower()}"
        else:
            return f"{reasons[0]}, {reasons[1].lower()}, and {reasons[2].lower()}"
    
    def _extract_actions(self, main_task: str, all_tasks: List[str]) -> List[str]:
        """Extract related action items for a priority."""
        actions = []
        
        # Try to find related tasks
        main_keywords = set(re.findall(r'\b\w{4,}\b', main_task.lower()))
        
        for task in all_tasks[:10]:  # Check first 10 tasks
            task_keywords = set(re.findall(r'\b\w{4,}\b', task.lower()))
            
            # If shares 2+ keywords, likely related
            if len(main_keywords & task_keywords) >= 2:
                clean_task = re.sub(r'^\s*-\s*\[[ x]\]\s*', '', task).strip()
                if clean_task and clean_task != main_task:
                    actions.append(clean_task)
        
        return actions[:5]  # Max 5 actions
    
    def format_recommendations(self, recommendations: List[Dict]) -> str:
        """Format recommendations as markdown."""
        output = "### Your Top 3 Priorities This Week\n\n"
        output += "*Recommended based on carry-forwards, patterns, and urgency:*\n\n"
        
        for rec in recommendations:
            output += f"{rec['priority']}. **{rec['title']}** - {rec['category']}\n"
            output += f"   - Why: {rec['why']}\n"
            
            if rec.get('actions'):
                output += f"   - Actions:\n"
                for action in rec['actions'][:3]:
                    output += f"     - [ ] {action}\n"
            
            output += "\n"
        
        return output


def recommend_priorities(
    carry_forwards: List[str],
    calendar_events: List[Dict] = None,
    pending_decisions: List[str] = None
) -> List[Dict]:
    """
    Main function to get priority recommendations.
    
    Usage from Cursor:
        from system.automation.priority_recommender import recommend_priorities
        
        carry_forwards = [list of incomplete tasks from last week]
        recommendations = recommend_priorities(carry_forwards)
    """
    recommender = PriorityRecommender()
    return recommender.recommend_top3(
        carry_forwards=carry_forwards,
        calendar_events=calendar_events,
        pending_decisions=pending_decisions
    )


if __name__ == "__main__":
    # Test with sample data
    sample_carry_forwards = [
        "Review and sign off on Q3 SPIF communication draft",
        "Complete launch detection validation for Sascha (multi-store logic)",
        "Check if AMER Regional RevOps made decision",
        "Continue SE craft improvement work documentation",
        "Follow up with Mary on APAC tooling compilation",
        "Prepare for andre meeting on 2026 planning",
        "Update stakeholders on merchant experience transformation"
    ]
    
    recommender = PriorityRecommender()
    recommendations = recommender.recommend_top3(sample_carry_forwards)
    
    print("\n=== RECOMMENDED TOP 3 PRIORITIES ===\n")
    print(recommender.format_recommendations(recommendations))
    
    print("\n=== ANALYSIS BREAKDOWN ===")
    analyzed = recommender.analyze_carry_forwards(sample_carry_forwards)
    for task in analyzed[:5]:
        print(f"\n{task['category']} (Score: {task['score']}): {task['task'][:60]}")
        print(f"  Reasons: {', '.join(task['reasons'])}")

