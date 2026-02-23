"""
Detect and structure decision points (if/then/else logic) in workflows.
"""

import re
from typing import List, Dict, Optional

class DecisionDetector:
    """
    Detect decision points and convert to structured format.
    
    Detects patterns like:
    - "If X, then Y"
    - "Check if X"
    - "Verify whether X"
    - "Is X valid?"
    - Conditional branches
    """
    
    # Decision patterns
    DECISION_PATTERNS = [
        r'\b[Ii]f\b',
        r'\b[Cc]heck\s+if\b',
        r'\b[Cc]heck\s+whether\b',
        r'\b[Vv]erify\s+if\b',
        r'\b[Vv]erify\s+whether\b',
        r'\b[Dd]etermine\s+if\b',
        r'\b[Dd]etermine\s+whether\b',
        r'\?$',  # Questions
    ]
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
    
    def detect_decisions(self, steps: List[Dict]) -> List[Dict]:
        """
        Identify decision points and add branch structure.
        
        Args:
            steps: List of extracted steps
            
        Returns:
            Steps with 'type' and 'branches' added to decision points
        """
        structured_steps = []
        
        for step in steps:
            text = step['text']
            
            # Check if this is a decision point
            is_decision = self._is_decision(text)
            
            if is_decision:
                # Structure the decision
                decision_step = self._structure_decision(step)
                structured_steps.append(decision_step)
            else:
                # Regular step
                step['type'] = 'step'
                structured_steps.append(step)
        
        return structured_steps
    
    def _is_decision(self, text: str) -> bool:
        """Check if text represents a decision point."""
        return any(re.search(pattern, text) for pattern in self.DECISION_PATTERNS)
    
    def _structure_decision(self, step: Dict) -> Dict:
        """
        Structure a decision step with branches.
        
        Returns:
            Step dict with:
                - type: 'decision'
                - branches: List of branch options
        """
        text = step['text']
        
        # Try to extract branches from text
        branches = self._extract_branches(text)
        
        # Clean up the decision text
        decision_text = self._clean_decision_text(text)
        
        return {
            'raw_number': step.get('raw_number'),
            'text': decision_text,
            'type': 'decision',
            'branches': branches,
            'format': step.get('format')
        }
    
    def _extract_branches(self, text: str) -> List[str]:
        """
        Extract explicit branch options from decision text.
        
        Looks for patterns like:
        - "if yes, do X; if no, do Y"
        - "then X, otherwise Y"
        - "continue if valid, stop if invalid"
        """
        branches = []
        
        # Pattern: "if yes... if no..."
        yes_match = re.search(r'[Ii]f\s+yes[,:]?\s+([^;.]+)', text)
        no_match = re.search(r'[Ii]f\s+no[,:]?\s+([^;.]+)', text)
        
        if yes_match:
            branches.append(f"If yes: {yes_match.group(1).strip()}")
        if no_match:
            branches.append(f"If no: {no_match.group(1).strip()}")
        
        # Pattern: "then X, otherwise Y"
        then_match = re.search(r'[Tt]hen\s+([^,]+)[,.]?\s+[Oo]therwise\s+([^.]+)', text)
        if then_match:
            branches.append(f"If yes: {then_match.group(1).strip()}")
            branches.append(f"If no: {then_match.group(2).strip()}")
        
        # If no explicit branches found, add generic ones
        if not branches:
            branches = [
                "If yes: Continue",
                "If no: [Specify action]"
            ]
        
        return branches
    
    def _clean_decision_text(self, text: str) -> str:
        """
        Clean decision text to make it a clear question.
        
        Converts:
        - "Check if data is valid" -> "Check if data is valid?"
        - "Verify whether user is authenticated" -> "Check if user is authenticated?"
        """
        # Remove branch clauses
        text = re.sub(r',?\s+[Tt]hen\s+.+', '', text)
        text = re.sub(r',?\s+[Oo]therwise\s+.+', '', text)
        text = re.sub(r',?\s+[Ii]f\s+yes.+', '', text)
        text = re.sub(r',?\s+[Ii]f\s+no.+', '', text)
        
        # Normalize to "Check if" format
        text = re.sub(r'^[Vv]erify\s+(whether|if)\s+', 'Check if ', text)
        text = re.sub(r'^[Dd]etermine\s+(whether|if)\s+', 'Check if ', text)
        
        # Ensure it ends with question mark if it looks like a question
        if 'Check if' in text or 'check if' in text:
            if not text.endswith('?'):
                text += '?'
        
        return text.strip()
