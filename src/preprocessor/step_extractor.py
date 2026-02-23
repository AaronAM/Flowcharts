"""
Extract workflow steps from various input formats.
"""

import re
from typing import List, Dict, Optional

class StepExtractor:
    """
    Extract steps from messy text in various formats.
    
    Supported formats:
    - Numbered lists (1., 2., 3. or 1), 2), 3))
    - Lettered lists (a., b., c. or a), b), c))
    - Roman numerals (i., ii., iii.)
    - Bullet points (-, *, •)
    - Paragraphs with sequential actions
    - Tables (Markdown, simple text tables)
    - Mixed formats
    """
    
    # Regex patterns for different step formats
    PATTERNS = {
        'numbered': r'^\s*(\d+)[.):]\s+(.+)$',
        'lettered': r'^\s*([a-z])[.):]\s+(.+)$',
        'roman': r'^\s*(i{1,3}|iv|v|vi{0,3}|ix|x)[.):]\s+(.+)$',
        'bullet': r'^\s*[-*•]\s+(.+)$',
        'step_prefix': r'^\s*[Ss]tep\s+(\d+)[:]?\s+(.+)$',
        'table_row': r'^\s*\|\s*(\d+)\s*\|\s*(.+?)\s*\|',
    }
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.merge_multiline = self.config.get('merge_multiline', True)
    
    def extract(self, text: str) -> List[Dict]:
        """
        Extract steps from text.
        
        Returns:
            List of step dictionaries with keys:
                - 'raw_number': original numbering (if any)
                - 'text': step text
                - 'format': detected format type
        """
        # Try different extraction methods
        steps = []
        
        # 1. Try numbered list extraction
        numbered_steps = self._extract_numbered(text)
        if numbered_steps:
            return numbered_steps
        
        # 2. Try table extraction
        table_steps = self._extract_from_table(text)
        if table_steps:
            return table_steps
        
        # 3. Try bullet list extraction
        bullet_steps = self._extract_bullets(text)
        if bullet_steps:
            return bullet_steps
        
        # 4. Fall back to paragraph extraction
        paragraph_steps = self._extract_from_paragraphs(text)
        return paragraph_steps
    
    def _extract_numbered(self, text: str) -> List[Dict]:
        """Extract from numbered lists (1. 2. 3. format)."""
        steps = []
        lines = text.split('\n')
        
        for line in lines:
            # Try numbered pattern
            match = re.match(self.PATTERNS['numbered'], line)
            if match:
                number, step_text = match.groups()
                steps.append({
                    'raw_number': int(number),
                    'text': step_text.strip(),
                    'format': 'numbered'
                })
                continue
            
            # Try "Step N:" pattern
            match = re.match(self.PATTERNS['step_prefix'], line)
            if match:
                number, step_text = match.groups()
                steps.append({
                    'raw_number': int(number),
                    'text': step_text.strip(),
                    'format': 'step_prefix'
                })
        
        return steps if steps else []
    
    def _extract_from_table(self, text: str) -> List[Dict]:
        """Extract steps from table format."""
        steps = []
        lines = text.split('\n')
        
        for line in lines:
            match = re.match(self.PATTERNS['table_row'], line)
            if match:
                number, step_text = match.groups()
                steps.append({
                    'raw_number': int(number),
                    'text': step_text.strip(),
                    'format': 'table'
                })
        
        return steps
    
    def _extract_bullets(self, text: str) -> List[Dict]:
        """Extract from bullet point lists."""
        steps = []
        lines = text.split('\n')
        
        for line in lines:
            match = re.match(self.PATTERNS['bullet'], line)
            if match:
                step_text = match.group(1)
                steps.append({
                    'raw_number': None,
                    'text': step_text.strip(),
                    'format': 'bullet'
                })
        
        return steps
    
    def _extract_from_paragraphs(self, text: str) -> List[Dict]:
        """
        Extract steps from narrative paragraphs.
        Looks for sequential indicators: First, Then, Next, After, Finally, etc.
        """
        steps = []
        
        # Sequential indicators
        indicators = [
            r'\b[Ff]irst\b',
            r'\b[Tt]hen\b',
            r'\b[Nn]ext\b',
            r'\b[Aa]fter\s+that\b',
            r'\b[Ff]inally\b',
            r'\b[Ll]astly\b',
            r'\b[Ss]ubsequently\b',
        ]
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Check if sentence contains sequential indicator
            has_indicator = any(re.search(pattern, sentence) for pattern in indicators)
            
            # Check if sentence looks like an action (imperative verb)
            is_action = self._is_action_sentence(sentence)
            
            if has_indicator or is_action:
                # Clean up the indicator
                for pattern in indicators:
                    sentence = re.sub(pattern + r',?\s*', '', sentence)
                
                steps.append({
                    'raw_number': None,
                    'text': sentence.strip(),
                    'format': 'paragraph'
                })
        
        return steps
    
    def _is_action_sentence(self, sentence: str) -> bool:
        """
        Heuristic to detect if sentence is an action/imperative.
        Looks for action verbs at the start.
        """
        action_verbs = [
            r'^\s*[Oo]pen\b',
            r'^\s*[Cc]lose\b',
            r'^\s*[Cc]lick\b',
            r'^\s*[Ss]elect\b',
            r'^\s*[Cc]hoose\b',
            r'^\s*[Ee]nter\b',
            r'^\s*[Tt]ype\b',
            r'^\s*[Pp]ress\b',
            r'^\s*[Ll]oad\b',
            r'^\s*[Ss]ave\b',
            r'^\s*[Dd]elete\b',
            r'^\s*[Cc]reate\b',
            r'^\s*[Ii]nstall\b',
            r'^\s*[Cc]onfigure\b',
            r'^\s*[Vv]erify\b',
            r'^\s*[Cc]heck\b',
            r'^\s*[Cc]onnect\b',
            r'^\s*[Dd]isconnect\b',
            r'^\s*[Rr]un\b',
            r'^\s*[Ee]xecute\b',
            r'^\s*[Ss]tart\b',
            r'^\s*[Ss]top\b',
        ]
        
        return any(re.search(pattern, sentence) for pattern in action_verbs)
