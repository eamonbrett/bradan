#!/usr/bin/env python3
"""
Slack Context Extraction Module

Extracts commitments, action items, and key discussions from Slack
to enhance weekly summaries and daily planning.

Designed to be called from Cursor/Claude environment where MCP is available.
"""

from datetime import date, datetime, timedelta
from typing import List, Dict, Optional
import re


class SlackContextExtractor:
    """Extract action items and context from Slack messages."""
    
    def __init__(self):
        """Initialize the Slack context extractor."""
        pass
    
    def extract_commitments_from_messages(self, 
                                          messages: List[Dict],
                                          user_name: str = "Eamon") -> List[Dict[str, str]]:
        """Extract commitments from Slack messages.
        
        Looks for patterns like:
        - "I'll..."
        - "I will..."
        - "I can..."
        - "I'll do..."
        - "Let me..."
        - "I'm going to..."
        
        Args:
            messages: List of Slack message dicts from MCP
            user_name: User's name for context
            
        Returns:
            List of commitment dicts with 'text', 'channel', 'timestamp', 'link'
        """
        commitments = []
        
        # Commitment patterns
        patterns = [
            r"I'?ll\s+(.+?)(?:\.|$|\n)",
            r"I will\s+(.+?)(?:\.|$|\n)",
            r"I can\s+(.+?)(?:\.|$|\n)",
            r"Let me\s+(.+?)(?:\.|$|\n)",
            r"I'm going to\s+(.+?)(?:\.|$|\n)",
            r"I'?m planning to\s+(.+?)(?:\.|$|\n)",
        ]
        
        for message in messages:
            text = message.get('text', '')
            if not text:
                continue
            
            # Check each pattern
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    commitment_text = match.group(1).strip()
                    
                    # Clean up the commitment text
                    commitment_text = self._clean_commitment_text(commitment_text)
                    
                    # Skip if it's too short or looks like a question
                    if len(commitment_text) < 10 or commitment_text.endswith('?'):
                        continue
                    
                    commitments.append({
                        'text': commitment_text,
                        'channel': message.get('channel', 'Unknown'),
                        'timestamp': message.get('ts', ''),
                        'permalink': message.get('permalink', ''),
                        'date': self._format_timestamp(message.get('ts', ''))
                    })
        
        return commitments
    
    def extract_mentions_and_requests(self, 
                                      messages: List[Dict],
                                      user_id: str = None) -> List[Dict[str, str]]:
        """Extract messages where user was mentioned or asked to do something.
        
        Args:
            messages: List of Slack message dicts from MCP
            user_id: User's Slack ID (e.g., 'U12345')
            
        Returns:
            List of mention/request dicts
        """
        mentions = []
        
        for message in messages:
            text = message.get('text', '')
            
            # Check for user mention
            if user_id and f"<@{user_id}>" in text:
                mentions.append({
                    'text': text,
                    'type': 'mention',
                    'from': message.get('user', 'Unknown'),
                    'channel': message.get('channel', 'Unknown'),
                    'timestamp': message.get('ts', ''),
                    'permalink': message.get('permalink', ''),
                    'date': self._format_timestamp(message.get('ts', ''))
                })
            
            # Check for request patterns (Could you..., Can you..., Please...)
            request_patterns = [
                r"(?:could|can)\s+you\s+(.+?)(?:\?|$|\n)",
                r"(?:would|will)\s+you\s+(.+?)(?:\?|$|\n)",
                r"please\s+(.+?)(?:\.|$|\n)",
            ]
            
            for pattern in request_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    request_text = match.group(1).strip()
                    if len(request_text) > 10:
                        mentions.append({
                            'text': request_text,
                            'type': 'request',
                            'from': message.get('user', 'Unknown'),
                            'channel': message.get('channel', 'Unknown'),
                            'timestamp': message.get('ts', ''),
                            'permalink': message.get('permalink', ''),
                            'date': self._format_timestamp(message.get('ts', ''))
                        })
                    break
        
        return mentions
    
    def extract_decisions(self, messages: List[Dict]) -> List[Dict[str, str]]:
        """Extract decisions from Slack messages.
        
        Looks for patterns like:
        - "We decided..."
        - "Decision: ..."
        - "We'll go with..."
        - "The plan is..."
        
        Args:
            messages: List of Slack message dicts from MCP
            
        Returns:
            List of decision dicts
        """
        decisions = []
        
        decision_patterns = [
            r"(?:we'?ve|we have)?\s*decided\s+(?:to\s+)?(.+?)(?:\.|$|\n)",
            r"decision:\s*(.+?)(?:\.|$|\n)",
            r"we'?ll go with\s+(.+?)(?:\.|$|\n)",
            r"the plan is\s+(?:to\s+)?(.+?)(?:\.|$|\n)",
            r"we agreed\s+(?:to\s+)?(.+?)(?:\.|$|\n)",
        ]
        
        for message in messages:
            text = message.get('text', '')
            
            for pattern in decision_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    decision_text = match.group(1).strip()
                    
                    # Clean up
                    decision_text = self._clean_commitment_text(decision_text)
                    
                    if len(decision_text) > 10:
                        decisions.append({
                            'text': decision_text,
                            'channel': message.get('channel', 'Unknown'),
                            'timestamp': message.get('ts', ''),
                            'permalink': message.get('permalink', ''),
                            'date': self._format_timestamp(message.get('ts', ''))
                        })
        
        return decisions
    
    def group_by_channel(self, items: List[Dict]) -> Dict[str, List[Dict]]:
        """Group items by Slack channel.
        
        Args:
            items: List of items with 'channel' key
            
        Returns:
            Dictionary mapping channel names to items
        """
        grouped = {}
        
        for item in items:
            channel = item.get('channel', 'Unknown')
            if channel not in grouped:
                grouped[channel] = []
            grouped[channel].append(item)
        
        return grouped
    
    def get_active_threads(self, messages: List[Dict]) -> List[Dict[str, str]]:
        """Identify active threads from messages.
        
        Args:
            messages: List of Slack message dicts
            
        Returns:
            List of active thread summaries
        """
        threads = {}
        
        for message in messages:
            thread_ts = message.get('thread_ts')
            if thread_ts:
                if thread_ts not in threads:
                    threads[thread_ts] = {
                        'count': 0,
                        'channel': message.get('channel', 'Unknown'),
                        'first_message': message.get('text', '')[:100],
                        'timestamp': thread_ts,
                        'permalink': message.get('permalink', '')
                    }
                threads[thread_ts]['count'] += 1
        
        # Return threads with multiple messages
        active_threads = [
            thread for thread in threads.values() 
            if thread['count'] > 1
        ]
        
        return active_threads
    
    def _clean_commitment_text(self, text: str) -> str:
        """Clean up commitment text.
        
        Args:
            text: Raw commitment text
            
        Returns:
            Cleaned text
        """
        # Remove Slack formatting
        text = re.sub(r'<[^>]+>', '', text)  # Remove <@mentions> and <links>
        text = re.sub(r'[*_~`]', '', text)   # Remove markdown
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Capitalize first letter
        if text:
            text = text[0].upper() + text[1:]
        
        return text
    
    def _format_timestamp(self, ts: str) -> str:
        """Format Slack timestamp to readable date.
        
        Args:
            ts: Slack timestamp (e.g., '1634567890.123456')
            
        Returns:
            Formatted date string
        """
        try:
            timestamp = float(ts.split('.')[0])
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime('%B %d, %Y')
        except:
            return 'Unknown date'
    
    def format_slack_context_for_summary(self,
                                         commitments: List[Dict],
                                         mentions: List[Dict],
                                         decisions: List[Dict],
                                         threads: List[Dict]) -> str:
        """Format Slack context as markdown for weekly summary.
        
        Args:
            commitments: List of commitment dicts
            mentions: List of mention dicts
            decisions: List of decision dicts
            threads: List of active thread dicts
            
        Returns:
            Markdown-formatted Slack context section
        """
        md = """
## 💬 Slack Activity & Commitments

"""
        
        if commitments:
            md += f"### Your Commitments from Slack\n\n"
            # Group by channel
            by_channel = self.group_by_channel(commitments)
            for channel, items in sorted(by_channel.items()):
                if items:
                    md += f"**{channel}**\n"
                    for item in items:
                        md += f"- [ ] {item['text']}\n"
                        if item.get('permalink'):
                            md += f"  _Source: [Slack message]({item['permalink']})_\n"
                    md += "\n"
        
        if mentions:
            md += f"### Requests & Mentions\n\n"
            for mention in mentions[:5]:  # Limit to top 5
                md += f"- **{mention.get('from', 'Someone')}** in {mention.get('channel', 'Unknown')}: "
                md += f"{mention['text'][:100]}\n"
        
        if decisions:
            md += f"\n### Key Decisions from Slack\n\n"
            for decision in decisions[:5]:  # Limit to top 5
                md += f"- {decision['text']}\n"
                md += f"  _{decision.get('channel', 'Unknown')} • {decision.get('date', 'Unknown date')}_\n\n"
        
        if threads:
            md += f"\n### Active Threads ({len(threads)})\n\n"
            for thread in threads[:3]:  # Limit to top 3
                md += f"- **{thread.get('channel', 'Unknown')}**: {thread['first_message']}\n"
                md += f"  _{thread['count']} replies_\n\n"
        
        return md


def extract_slack_context(messages: List[Dict],
                          user_name: str = "Eamon",
                          user_id: str = None) -> Dict[str, any]:
    """Extract all Slack context from messages.
    
    Convenience function for Claude to call.
    
    Args:
        messages: List of Slack message dicts from MCP
        user_name: User's name for context
        user_id: User's Slack ID
        
    Returns:
        Dictionary with all extracted context
    """
    extractor = SlackContextExtractor()
    
    commitments = extractor.extract_commitments_from_messages(messages, user_name)
    mentions = extractor.extract_mentions_and_requests(messages, user_id)
    decisions = extractor.extract_decisions(messages)
    threads = extractor.get_active_threads(messages)
    
    return {
        'commitments': commitments,
        'mentions': mentions,
        'decisions': decisions,
        'active_threads': threads,
        'summary_markdown': extractor.format_slack_context_for_summary(
            commitments, mentions, decisions, threads
        )
    }


def format_slack_section_for_summary(slack_context: Dict) -> str:
    """Format Slack context as markdown section for weekly summary.
    
    Args:
        slack_context: Dictionary from extract_slack_context()
        
    Returns:
        Markdown-formatted section
    """
    return slack_context.get('summary_markdown', '')


if __name__ == "__main__":
    print("❌ This module is designed to be imported and used from Cursor/Claude environment.")
    print("📌 It extracts commitments and context from Slack messages for weekly summaries.")

