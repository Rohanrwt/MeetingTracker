"""Mock LLM integration for extracting action items - NO API KEY REQUIRED.

This uses pattern matching and NLP techniques to extract action items.
Perfect for demos, testing, and portfolio projects.
"""
import re
from typing import List, Dict, Any
from datetime import datetime, timedelta


def extract_action_items(transcript: str) -> List[Dict[str, Any]]:
    """
    Extract action items from meeting transcript using pattern matching.
    
    This is a mock implementation that doesn't require any API keys.
    It uses regex patterns to identify action items.
    
    Args:
        transcript: The meeting transcript text
        
    Returns:
        List of dictionaries with task, owner, and due_date fields
    """
    action_items = []
    
    # Split into sentences
    sentences = re.split(r'[.!?\n]+', transcript)
    
    # Action patterns to look for
    action_patterns = [
        # "John will prepare the report"
        r'(\w+)\s+will\s+(.+?)(?:\s+by\s+(.+?))?$',
        # "Sarah should review the document"
        r'(\w+)\s+should\s+(.+?)(?:\s+by\s+(.+?))?$',
        # "Mike needs to update the slides"
        r'(\w+)\s+needs?\s+to\s+(.+?)(?:\s+by\s+(.+?))?$',
        # "Jane agreed to finish the presentation"
        r'(\w+)\s+agreed\s+to\s+(.+?)(?:\s+by\s+(.+?))?$',
        # "Bob is going to prepare"
        r'(\w+)\s+is\s+going\s+to\s+(.+?)(?:\s+by\s+(.+?))?$',
        # "Alice mentioned she'll complete"
        r'(\w+)\s+mentioned\s+(?:she\'ll|he\'ll|they\'ll)\s+(.+?)(?:\s+by\s+(.+?))?$',
        # "We need to schedule/complete/finish"
        r'we\s+need\s+to\s+(.+?)(?:\s+by\s+(.+?))?$',
        # "Someone should/must/has to"
        r'someone\s+(?:should|must|has\s+to)\s+(.+?)(?:\s+by\s+(.+?))?$',
        # "Need to" at start
        r'^need\s+to\s+(.+?)(?:\s+by\s+(.+?))?$',
        # "Schedule/Complete/Finish" at start
        r'^(?:schedule|complete|finish|update|prepare|review|create|send)\s+(.+?)(?:\s+by\s+(.+?))?$',
    ]
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence or len(sentence) < 10:
            continue
            
        # Try each pattern
        for pattern in action_patterns:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                groups = match.groups()
                
                # Determine owner and task based on pattern
                if len(groups) == 3 and groups[0] and groups[0].lower() not in ['we', 'someone', 'need']:
                    # Pattern with named person
                    owner = groups[0].strip().capitalize()
                    task = groups[1].strip()
                    due_date_str = groups[2] if len(groups) > 2 and groups[2] else None
                elif len(groups) >= 2:
                    # Pattern without named person
                    owner = None
                    task = groups[0].strip()
                    due_date_str = groups[1] if len(groups) > 1 and groups[1] else None
                else:
                    continue
                
                # Clean up the task
                task = task.strip()
                if task.endswith(','):
                    task = task[:-1]
                
                # Parse due date
                due_date = parse_due_date(due_date_str) if due_date_str else None
                
                # Add action item
                action_items.append({
                    "task": task.capitalize(),
                    "owner": owner,
                    "due_date": due_date
                })
                break  # Found a match, move to next sentence
    
    return action_items


def parse_due_date(date_str: str) -> str:
    """
    Parse various date formats into YYYY-MM-DD.
    
    Handles:
    - "Friday", "Monday" -> next occurrence
    - "this week" -> end of week
    - "next week" -> end of next week
    - "tomorrow" -> tomorrow's date
    - "end of month" -> last day of month
    - Actual dates like "Dec 20", "2024-12-20"
    """
    if not date_str:
        return None
    
    date_str = date_str.strip().lower()
    today = datetime.now()
    
    # Handle relative dates
    if "tomorrow" in date_str:
        target_date = today + timedelta(days=1)
        return target_date.strftime("%Y-%m-%d")
    
    if "this week" in date_str or "week" in date_str:
        # End of week (Friday)
        days_until_friday = (4 - today.weekday()) % 7
        if days_until_friday == 0:
            days_until_friday = 7
        target_date = today + timedelta(days=days_until_friday)
        return target_date.strftime("%Y-%m-%d")
    
    if "next week" in date_str:
        days_until_friday = (4 - today.weekday()) % 7 + 7
        target_date = today + timedelta(days=days_until_friday)
        return target_date.strftime("%Y-%m-%d")
    
    if "end of month" in date_str or "month" in date_str:
        # Last day of current month
        if today.month == 12:
            target_date = datetime(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            target_date = datetime(today.year, today.month + 1, 1) - timedelta(days=1)
        return target_date.strftime("%Y-%m-%d")
    
    # Handle day names
    days_of_week = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }
    
    for day_name, day_num in days_of_week.items():
        if day_name in date_str:
            days_ahead = (day_num - today.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7  # Next occurrence
            target_date = today + timedelta(days=days_ahead)
            return target_date.strftime("%Y-%m-%d")
    
    # Try to match date patterns like "Dec 20", "December 20", "12/20"
    month_names = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'june': 6, 'july': 7, 'august': 8, 'september': 9,
        'october': 10, 'november': 11, 'december': 12
    }
    
    for month_name, month_num in month_names.items():
        if month_name in date_str:
            # Extract day number
            day_match = re.search(r'\d+', date_str)
            if day_match:
                day = int(day_match.group())
                # Use current year or next year if date has passed
                year = today.year
                try:
                    target_date = datetime(year, month_num, day)
                    if target_date < today:
                        target_date = datetime(year + 1, month_num, day)
                    return target_date.strftime("%Y-%m-%d")
                except ValueError:
                    pass
    
    # Check if already in YYYY-MM-DD format
    if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
        return date_str
    
    return None


def check_llm_health() -> bool:
    """
    Check if mock LLM service is operational.
    
    Returns:
        Always True since this is a mock implementation
    """
    return True