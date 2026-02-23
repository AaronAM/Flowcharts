"""
Normalize workflow steps to consistent numbering and format.
"""

from typing import List, Dict, Optional

class WorkflowNormalizer:
    """
    Normalize extracted steps to consistent format.
    
    - Renumber steps sequentially (1, 2, 3, ...)
    - Handle substeps (3a, 3b -> indented under 3)
    - Consistent spacing and formatting
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.preserve_substeps = self.config.get('preserve_substeps', True)
    
    def normalize(self, steps: List[Dict]) -> List[Dict]:
        """
        Normalize steps to consistent format.
        
        Args:
            steps: List of extracted/structured steps
            
        Returns:
            Normalized steps with consistent numbering
        """
        if not steps:
            return []
        
        # Renumber sequentially
        normalized = []
        current_number = 1
        
        for step in steps:
            normalized_step = {
                'number': current_number,
                'text': step['text'],
                'type': step.get('type', 'step')
            }
            
            # Preserve branches for decisions
            if step.get('type') == 'decision':
                normalized_step['branches'] = step.get('branches', [])
            
            normalized.append(normalized_step)
            current_number += 1
        
        return normalized
