"""
Priority Inbox Module
Aggregates emails, Slack messages, and notifications into a prioritized one-screen summary.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
import re


class PriorityInbox:
    """Aggregate and prioritize communications from multiple sources."""
    
    # Urgency keywords
    URGENT_KEYWORDS = [
        'urgent', 'asap', 'emergency', 'critical', 'immediate',
        'escalation', 'blocked', 'blocker', 'deadline today',
        'needs approval', 'approval needed', 'action required'
    ]
    
    # Impact indicators
    HIGH_IMPACT_KEYWORDS = [
        'executive', 'cto', 'vp', 'director', 'revenue',
        'customer escalation', 'production', 'outage',
        'board', 'strategy', 'quarterly', 'okr', 'budget'
    ]
    
    # Meeting-related keywords
    MEETING_KEYWORDS = [
        'meeting', 'sync', 'call', 'calendar', 'invite',
        'reschedule', 'cancel', 'confirm attendance'
    ]
    
    # Decision/approval keywords
    DECISION_KEYWORDS = [
        'approve', 'decision', 'review needed', 'feedback needed',
        'sign off', 'needs your input', 'waiting on you'
    ]
    
    def __init__(self):
        """Initialize the priority inbox."""
        self.items = []
    
    def add_emails(self, emails: List[Dict[str, Any]]) -> None:
        """
        Add emails to the priority inbox.
        
        Args:
            emails: List of email dicts with keys: id, from, subject, snippet, date, has_attachment
        """
        for email in emails:
            item = {
                'source': 'email',
                'from': email.get('from', 'Unknown'),
                'subject': email.get('subject', 'No Subject'),
                'preview': email.get('snippet', '')[:100],
                'timestamp': email.get('date', ''),
                'has_attachment': email.get('has_attachment', False),
                'raw_data': email
            }
            
            # Calculate priority
            item['urgency'] = self._calculate_urgency(item)
            item['impact'] = self._calculate_impact(item)
            item['priority'] = self._calculate_priority(item['urgency'], item['impact'])
            item['category'] = self._categorize_item(item)
            
            self.items.append(item)
    
    def add_slack_messages(self, messages: List[Dict[str, Any]]) -> None:
        """
        Add Slack messages to the priority inbox.
        
        Args:
            messages: List of Slack message dicts with keys: channel, user, text, timestamp, thread_ts
        """
        for msg in messages:
            # Skip bot messages
            if msg.get('bot_id'):
                continue
            
            item = {
                'source': 'slack',
                'from': msg.get('user_name', msg.get('user', 'Unknown')),
                'subject': f"#{msg.get('channel_name', 'direct-message')}",
                'preview': msg.get('text', '')[:100],
                'timestamp': msg.get('ts', ''),
                'is_dm': msg.get('channel_type') == 'im',
                'is_mention': '@' in msg.get('text', '') or msg.get('is_mention', False),
                'has_thread': bool(msg.get('thread_ts')) and msg.get('thread_ts') != msg.get('ts'),
                'reactions': msg.get('reactions', []),
                'raw_data': msg
            }
            
            # Calculate priority
            item['urgency'] = self._calculate_urgency(item)
            item['impact'] = self._calculate_impact(item)
            item['priority'] = self._calculate_priority(item['urgency'], item['impact'])
            item['category'] = self._categorize_item(item)
            
            self.items.append(item)
    
    def _calculate_urgency(self, item: Dict[str, Any]) -> str:
        """
        Calculate urgency level: HIGH, MEDIUM, LOW.
        
        Based on:
        - Keywords in subject/text
        - Source type (DM vs channel)
        - Recency
        - Direct mentions
        """
        score = 0
        text = f"{item.get('subject', '')} {item.get('preview', '')}".lower()
        
        # Check urgent keywords
        for keyword in self.URGENT_KEYWORDS:
            if keyword in text:
                score += 3
                break
        
        # Direct messages are more urgent
        if item.get('source') == 'slack' and item.get('is_dm'):
            score += 2
        
        # Direct mentions are urgent
        if item.get('is_mention'):
            score += 2
        
        # Email from VIP (could be enhanced with actual VIP list)
        if item.get('source') == 'email':
            from_field = item.get('from', '').lower()
            if any(title in from_field for title in ['cto', 'vp', 'director', 'ceo']):
                score += 2
        
        # Has attachment that might need review
        if item.get('has_attachment'):
            score += 1
        
        # Decision/approval needed
        for keyword in self.DECISION_KEYWORDS:
            if keyword in text:
                score += 2
                break
        
        # Map score to urgency level
        if score >= 5:
            return 'HIGH'
        elif score >= 2:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _calculate_impact(self, item: Dict[str, Any]) -> str:
        """
        Calculate impact level: HIGH, MEDIUM, LOW.
        
        Based on:
        - Business-critical keywords
        - Sender importance
        - Topic significance
        """
        score = 0
        text = f"{item.get('subject', '')} {item.get('preview', '')}".lower()
        
        # Check high-impact keywords
        for keyword in self.HIGH_IMPACT_KEYWORDS:
            if keyword in text:
                score += 3
                break
        
        # Strategic topics
        if any(word in text for word in ['strategy', 'vision', 'roadmap', 'okr', 'quarterly']):
            score += 2
        
        # Revenue/customer impact
        if any(word in text for word in ['revenue', 'customer', 'escalation', 'churn']):
            score += 2
        
        # Team/people topics
        if any(word in text for word in ['hiring', 'performance', 'team', 'org', 'compensation']):
            score += 1
        
        # Map score to impact level
        if score >= 4:
            return 'HIGH'
        elif score >= 2:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _calculate_priority(self, urgency: str, impact: str) -> int:
        """
        Calculate overall priority score (1-9).
        
        Priority Matrix:
        - P1 (9): High Urgency + High Impact
        - P2 (7-8): High Urgency + Med Impact, or Med Urgency + High Impact
        - P3 (4-6): High Urgency + Low Impact, Med + Med, Low + High
        - P4 (1-3): Everything else
        """
        urgency_score = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}[urgency]
        impact_score = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}[impact]
        
        return urgency_score * impact_score
    
    def _categorize_item(self, item: Dict[str, Any]) -> str:
        """Categorize the item by type."""
        text = f"{item.get('subject', '')} {item.get('preview', '')}".lower()
        
        if any(keyword in text for keyword in self.DECISION_KEYWORDS):
            return '🎯 Decision Required'
        elif any(keyword in text for keyword in self.MEETING_KEYWORDS):
            return '📅 Meeting-Related'
        elif item.get('source') == 'slack' and item.get('has_thread'):
            return '💬 Active Thread'
        elif item.get('has_attachment'):
            return '📎 Review Required'
        elif item.get('is_mention'):
            return '👤 Direct Mention'
        else:
            return '📬 Info/FYI'
    
    def get_prioritized_summary(self, max_items: int = 25) -> Dict[str, Any]:
        """
        Get prioritized summary of all items.
        
        Args:
            max_items: Maximum number of items to include
            
        Returns:
            Dict with categorized and prioritized items
        """
        # Sort by priority (highest first)
        sorted_items = sorted(self.items, key=lambda x: x['priority'], reverse=True)
        
        # Take top items
        top_items = sorted_items[:max_items]
        
        # Group by priority tier
        p1_items = [item for item in top_items if item['priority'] == 9]
        p2_items = [item for item in top_items if item['priority'] in [6, 8]]
        p3_items = [item for item in top_items if item['priority'] in [4, 5]]
        p4_items = [item for item in top_items if item['priority'] <= 3]
        
        # Stats
        stats = {
            'total_items': len(self.items),
            'emails': len([i for i in self.items if i['source'] == 'email']),
            'slack_messages': len([i for i in self.items if i['source'] == 'slack']),
            'high_priority': len([i for i in self.items if i['priority'] >= 7]),
            'needs_decision': len([i for i in self.items if 'Decision' in i['category']]),
            'has_mentions': len([i for i in self.items if i.get('is_mention')]),
        }
        
        return {
            'generated_at': datetime.now().isoformat(),
            'stats': stats,
            'p1': p1_items,
            'p2': p2_items,
            'p3': p3_items,
            'p4': p4_items
        }


def format_one_screen_output(summary: Dict[str, Any]) -> str:
    """
    Format the priority summary for one-screen display.
    
    Args:
        summary: Output from get_prioritized_summary()
        
    Returns:
        Formatted markdown string
    """
    lines = []
    
    # Header
    lines.append("# 🎯 Priority Inbox")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    
    # Stats bar
    stats = summary['stats']
    lines.append("## 📊 Overview")
    lines.append(f"**{stats['total_items']} items** | "
                f"✉️ {stats['emails']} emails | "
                f"💬 {stats['slack_messages']} Slack | "
                f"🔴 {stats['high_priority']} urgent | "
                f"🎯 {stats['needs_decision']} need decision\n")
    
    # Priority sections
    sections = [
        ('P1', '🔴 URGENT & HIGH IMPACT - Do First', summary['p1']),
        ('P2', '🟠 HIGH PRIORITY - Do Today', summary['p2']),
        ('P3', '🟡 MEDIUM PRIORITY - Plan For', summary['p3']),
        ('P4', '🟢 LOW PRIORITY - Review Later', summary['p4'])
    ]
    
    for priority, title, items in sections:
        if not items:
            continue
        
        lines.append(f"## {title}")
        lines.append(f"*{len(items)} item(s)*\n")
        
        for item in items[:10]:  # Limit to 10 per section for one-screen fit
            source_icon = '✉️' if item['source'] == 'email' else '💬'
            
            # Build one-line summary
            from_name = item['from'].split('@')[0] if '@' in item['from'] else item['from']
            subject = item['subject'][:40] + '...' if len(item['subject']) > 40 else item['subject']
            
            # Add context badges
            badges = []
            if item.get('is_dm'):
                badges.append('DM')
            if item.get('is_mention'):
                badges.append('@you')
            if item.get('has_attachment'):
                badges.append('📎')
            if item.get('has_thread'):
                badges.append('💬thread')
            
            badge_str = f" [{', '.join(badges)}]" if badges else ""
            
            lines.append(f"- {source_icon} **{from_name}**: {subject}{badge_str}")
            lines.append(f"  _{item['category']}_ | Urgency: {item['urgency']} | Impact: {item['impact']}")
            
            # Show brief preview if space allows
            if item['preview']:
                preview = item['preview'][:80].replace('\n', ' ')
                lines.append(f"  `{preview}...`")
            
            lines.append("")
    
    # Action summary
    lines.append("---")
    lines.append("## ✅ Recommended Actions")
    
    p1_count = len(summary['p1'])
    p2_count = len(summary['p2'])
    
    if p1_count > 0:
        lines.append(f"1. **🔴 Handle {p1_count} P1 item(s) immediately** - These are blocking others or time-sensitive")
    
    if p2_count > 0:
        lines.append(f"2. **🟠 Schedule {p2_count} P2 item(s) for today** - Add to your daily Top 3 if needed")
    
    if summary['stats']['needs_decision'] > 0:
        lines.append(f"3. **🎯 Make {summary['stats']['needs_decision']} decision(s)** - Others are waiting on you")
    
    lines.append("\n💡 *Tip: Use `Mark as complete` or `Snooze` in your inbox to clear items*")
    
    return '\n'.join(lines)


def create_priority_inbox_notification(summary: Dict[str, Any]) -> str:
    """
    Create a Slack-friendly notification of priority inbox.
    
    Args:
        summary: Output from get_prioritized_summary()
        
    Returns:
        Formatted string for Slack message
    """
    lines = []
    
    stats = summary['stats']
    
    lines.append("🎯 *Priority Inbox Summary*")
    lines.append(f"_{datetime.now().strftime('%A, %B %d at %I:%M %p')}_")
    lines.append("")
    lines.append("📊 *What's On Deck:*")
    lines.append(f"• {stats['total_items']} total items")
    lines.append(f"• {stats['high_priority']} high priority")
    lines.append(f"• {stats['needs_decision']} need your decision")
    lines.append(f"• {stats['has_mentions']} direct mentions")
    lines.append("")
    
    # Top priorities
    if summary['p1']:
        lines.append("🔴 *URGENT (P1):*")
        for item in summary['p1'][:3]:
            source_icon = '✉️' if item['source'] == 'email' else '💬'
            from_name = item['from'].split('@')[0] if '@' in item['from'] else item['from']
            lines.append(f"{source_icon} {from_name}: {item['subject'][:50]}")
        if len(summary['p1']) > 3:
            lines.append(f"... and {len(summary['p1']) - 3} more")
        lines.append("")
    
    if summary['p2']:
        lines.append("🟠 *HIGH PRIORITY (P2):*")
        for item in summary['p2'][:3]:
            source_icon = '✉️' if item['source'] == 'email' else '💬'
            from_name = item['from'].split('@')[0] if '@' in item['from'] else item['from']
            lines.append(f"{source_icon} {from_name}: {item['subject'][:50]}")
        if len(summary['p2']) > 3:
            lines.append(f"... and {len(summary['p2']) - 3} more")
        lines.append("")
    
    lines.append("---")
    lines.append("💡 Ask me for the full priority inbox to see all details")
    
    return '\n'.join(lines)

