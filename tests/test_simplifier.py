"""
Comprehensive tests for workflow simplifier.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessor import WorkflowSimplifier, StepExtractor, DecisionDetector

class TestStepExtractor:
    """Test step extraction from various formats."""
    
    def test_extract_numbered_list(self):
        """Test extraction from numbered list."""
        text = """
        1. First step
        2. Second step
        3. Third step
        """
        
        extractor = StepExtractor()
        steps = extractor.extract(text)
        
        assert len(steps) == 3
        assert steps[0]['text'] == 'First step'
        assert steps[1]['raw_number'] == 2
    
    def test_extract_step_prefix(self):
        """Test extraction from 'Step N:' format."""
        text = """
        Step 1: Connect USB drive
        Step 2: Boot from USB
        Step 3: Select option
        """
        
        extractor = StepExtractor()
        steps = extractor.extract(text)
        
        assert len(steps) == 3
        assert steps[0]['text'] == 'Connect USB drive'
        assert steps[2]['format'] == 'step_prefix'
    
    def test_extract_bullets(self):
        """Test extraction from bullet list."""
        text = """
        - First action
        - Second action
        - Third action
        """
        
        extractor = StepExtractor()
        steps = extractor.extract(text)
        
        assert len(steps) == 3
        assert steps[0]['format'] == 'bullet'
        assert steps[1]['text'] == 'Second action'
    
    def test_extract_table(self):
        """Test extraction from table format."""
        text = """
        | Step | Action |
        |------|--------|
        | 1 | Connect drive |
        | 2 | Boot system |
        | 3 | Install software |
        """
        
        extractor = StepExtractor()
        steps = extractor.extract(text)
        
        assert len(steps) == 3
        assert steps[0]['text'] == 'Connect drive'
        assert steps[2]['format'] == 'table'
    
    def test_extract_paragraphs(self):
        """Test extraction from narrative paragraphs."""
        text = """
        First, open the application. Then, load the configuration files.
        Next, verify the user is authenticated. Finally, display the dashboard.
        """
        
        extractor = StepExtractor()
        steps = extractor.extract(text)
        
        assert len(steps) >= 3
        assert any('open' in s['text'].lower() for s in steps)
        assert any('load' in s['text'].lower() for s in steps)

class TestDecisionDetector:
    """Test decision point detection."""
    
    def test_detect_if_statement(self):
        """Test detection of 'if' statements."""
        steps = [{
            'text': 'If user is authenticated, load dashboard',
            'raw_number': 1,
            'format': 'numbered'
        }]
        
        detector = DecisionDetector()
        result = detector.detect_decisions(steps)
        
        assert result[0]['type'] == 'decision'
        assert 'branches' in result[0]
    
    def test_detect_check_if(self):
        """Test detection of 'check if' patterns."""
        steps = [{
            'text': 'Check if data is valid',
            'raw_number': 1,
            'format': 'numbered'
        }]
        
        detector = DecisionDetector()
        result = detector.detect_decisions(steps)
        
        assert result[0]['type'] == 'decision'
        assert result[0]['text'].endswith('?')
    
    def test_extract_branches(self):
        """Test extraction of explicit branches."""
        steps = [{
            'text': 'If successful, continue; if not, show error',
            'raw_number': 1,
            'format': 'numbered'
        }]
        
        detector = DecisionDetector()
        result = detector.detect_decisions(steps)
        
        branches = result[0]['branches']
        assert len(branches) >= 2
        assert any('yes' in b.lower() for b in branches)

class TestWorkflowSimplifier:
    """Integration tests for complete simplification."""
    
    def test_simple_numbered_workflow(self):
        """Test simplification of simple numbered workflow."""
        messy = """
        1. Start the process
        2. Load data
        3. Process data
        4. Save results
        5. End
        """
        
        simplifier = WorkflowSimplifier()
        clean = simplifier.simplify(messy)
        
        assert '1. Start' in clean
        assert '2. Load data' in clean or '3. Load data' in clean
        assert 'End' in clean
    
    def test_paragraph_workflow(self):
        """Test simplification of paragraph format."""
        messy = """
        First, the user opens the application. Then the system loads 
        configuration files. Next, check if the user is authenticated.
        If authenticated, load the dashboard. Otherwise, redirect to login.
        """
        
        simplifier = WorkflowSimplifier()
        clean = simplifier.simplify(messy)
        
        lines = clean.split('\n')
        assert len(lines) >= 5
        assert any('Start' in line for line in lines)
        assert any('check if' in line.lower() for line in lines)
    
    def test_decision_with_branches(self):
        """Test that decisions create proper branch structure."""
        messy = """
        1. Get user input
        2. Validate data
        3. Check if data is valid
        4. If valid, save to database
        5. If invalid, show error
        6. End
        """
        
        simplifier = WorkflowSimplifier()
        clean = simplifier.simplify(messy)
        
        assert 'Check if' in clean or 'check if' in clean
        assert '- If yes:' in clean or '- If no:' in clean
    
    def test_auto_terminators(self):
        """Test that Start/End are added automatically."""
        messy = """
        1. Do task A
        2. Do task B
        3. Do task C
        """
        
        simplifier = WorkflowSimplifier()
        clean = simplifier.simplify(messy)
        
        lines = clean.split('\n')
        assert 'Start' in lines[0]
        assert 'End' in lines[-1]
    
    def test_simplify_to_dict(self):
        """Test structured data output."""
        messy = """
        1. First step
        2. Second step
        """
        
        simplifier = WorkflowSimplifier()
        result = simplifier.simplify_to_dict(messy)
        
        assert isinstance(result, list)
        assert all(isinstance(step, dict) for step in result)
        assert all('number' in step for step in result)
        assert all('text' in step for step in result)

class TestRealWorldExamples:
    """Test with real-world messy workflows."""
    
    def test_tech_setup_workflow(self):
        """Test typical tech setup procedure."""
        messy = """
        Connect the USB drive to the laptop. Press F12 to boot from USB.
        Select the USB option from the boot menu. The system will load
        the installation environment. Check if the drive is detected.
        If detected, proceed with installation. If not detected, restart
        and try again. Install the operating system. Configure network
        settings. Install required drivers.
        """
        
        simplifier = WorkflowSimplifier()
        clean = simplifier.simplify(messy)
        
        assert '1. Start' in clean
        assert 'Connect' in clean or 'connect' in clean
        assert 'Check if' in clean or 'check if' in clean
        assert 'End' in clean
    
    def test_business_process(self):
        """Test business process workflow."""
        messy = """
        Step 1: Receive customer inquiry
        Step 2: Review inquiry details
        Step 3: Determine if inquiry is valid
        Step 4a: If valid, assign to specialist
        Step 4b: If invalid, send rejection email
        Step 5: Specialist contacts customer
        Step 6: Close inquiry
        """
        
        simplifier = WorkflowSimplifier()
        clean = simplifier.simplify(messy)
        
        steps = clean.split('\n')
        assert len(steps) >= 6
        assert any('Determine if' in line or 'Check if' in line for line in steps)

# Pytest configuration
@pytest.fixture
def sample_messy_text():
    """Fixture providing sample messy text."""
    return """
    First, do step one. Then do step two.
    After that, check if condition is met.
    If yes, do step three. If no, do step four.
    Finally, complete the process.
    """

def test_with_fixture(sample_messy_text):
    """Test using fixture."""
    simplifier = WorkflowSimplifier()
    result = simplifier.simplify(sample_messy_text)
    assert 'Start' in result
    assert 'check if' in result.lower()

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
