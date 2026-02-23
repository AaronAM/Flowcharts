"""
Main entry point for workflow simplification.
Orchestrates extraction, detection, and normalization.
"""

from typing import List, Dict, Optional
from .step_extractor import StepExtractor
from .decision_detector import DecisionDetector
from .normalizer import WorkflowNormalizer

class WorkflowSimplifier:
    """
    Main class for converting messy workflow text into clean format.
    
    Handles:
    - Multiple input formats (paragraphs, tables, lists, mixed)
    - Decision point detection (if/then/else)
    - Step extraction and merging
    - Consistent numbering
    - Automatic Start/End insertion
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize simplifier with optional configuration.
        
        Args:
            config: Optional configuration dict with keys:
                - 'preserve_substeps': bool (default True)
                - 'auto_terminators': bool (default True)
                - 'merge_multiline': bool (default True)
        """
        self.config = config or {}
        self.extractor = StepExtractor(self.config)
        self.detector = DecisionDetector(self.config)
        self.normalizer = WorkflowNormalizer(self.config)
        
    def simplify(self, messy_text: str) -> str:
        """
        Convert messy workflow text to clean, numbered format.
        
        Args:
            messy_text: Raw, unstructured workflow text
            
        Returns:
            Clean, numbered workflow text ready for flowchart generation
            
        Example:
            >>> simplifier = WorkflowSimplifier()
            >>> messy = "First do this. Then do that. If successful, continue."
            >>> clean = simplifier.simplify(messy)
            >>> print(clean)
            1. Start
            2. Do this
            3. Do that
            4. Check if successful
               - If yes: Continue
               - If no: [specify action]
            5. End
        """
        # Step 1: Extract raw steps from various formats
        raw_steps = self.extractor.extract(messy_text)
        
        # Step 2: Detect and structure decision points
        structured_steps = self.detector.detect_decisions(raw_steps)
        
        # Step 3: Normalize numbering and format
        normalized_steps = self.normalizer.normalize(structured_steps)
        
        # Step 4: Ensure Start/End terminators
        if self.config.get('auto_terminators', True):
            normalized_steps = self._ensure_terminators(normalized_steps)
        
        # Step 5: Format final output
        return self._format_output(normalized_steps)
    
    def simplify_to_dict(self, messy_text: str) -> List[Dict]:
        """
        Simplify and return structured data instead of text.
        Useful for programmatic access to workflow structure.
        
        Returns:
            List of step dictionaries with keys:
                - 'number': int
                - 'text': str
                - 'type': 'step' | 'decision' | 'start' | 'end'
                - 'branches': Optional[List[str]]
        """
        raw_steps = self.extractor.extract(messy_text)
        structured_steps = self.detector.detect_decisions(raw_steps)
        normalized_steps = self.normalizer.normalize(structured_steps)
        
        if self.config.get('auto_terminators', True):
            normalized_steps = self._ensure_terminators(normalized_steps)
            
        return normalized_steps
    
    def _ensure_terminators(self, steps: List[Dict]) -> List[Dict]:
        """Add Start/End steps if not present."""
        # Check for Start
        if not steps or steps[0].get('type') != 'start':
            steps.insert(0, {
                'number': 1,
                'text': 'Start',
                'type': 'start'
            })
        
        # Check for End
        if not steps or steps[-1].get('type') != 'end':
            steps.append({
                'number': len(steps) + 1,
                'text': 'End',
                'type': 'end'
            })
        
        # Renumber after insertion
        for idx, step in enumerate(steps, start=1):
            step['number'] = idx
            
        return steps
    
    def _format_output(self, steps: List[Dict]) -> str:
        """Convert structured steps to formatted text."""
        lines = []
        
        for step in steps:
            number = step['number']
            text = step['text']
            step_type = step.get('type', 'step')
            
            if step_type == 'decision':
                lines.append(f"{number}. {text}")
                branches = step.get('branches', [])
                for branch in branches:
                    lines.append(f"   - {branch}")
            else:
                lines.append(f"{number}. {text}")
        
        return '\n'.join(lines)
