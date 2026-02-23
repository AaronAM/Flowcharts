# Workflow Simplifier Documentation

Convert messy, unstructured workflow text into clean, numbered format ready for flowchart generation.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Supported Input Formats](#supported-input-formats)
5. [Decision Detection](#decision-detection)
6. [Configuration](#configuration)
7. [API Reference](#api-reference)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)

## Features

- **Multiple input formats**: Paragraphs, numbered lists, bullets, tables, mixed formats
- **Decision detection**: Automatic detection of if/then/else logic
- **Branch structuring**: Converts decisions to clear branch format
- **Smart extraction**: Handles narrative text, sequential indicators, action verbs
- **Automatic terminators**: Adds Start/End steps if missing
- **Configurable**: Customize behavior with configuration options

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Command Line

```bash
# Basic simplification
py -m cli.main simplify messy_workflow.txt -o clean_workflow.txt

# Analyze workflow structure
py -m cli.main analyze messy.txt

# Verbose output
py -m cli.main simplify messy.txt -o clean.txt -v
```

### Python API

```python
from src.preprocessor import WorkflowSimplifier

# Basic usage
simplifier = WorkflowSimplifier()
clean_text = simplifier.simplify(messy_text)

# With configuration
config = {
    'preserve_substeps': True,
    'auto_terminators': True,
    'merge_multiline': True
}
simplifier = WorkflowSimplifier(config)
clean_text = simplifier.simplify(messy_text)

# Get structured data
steps = simplifier.simplify_to_dict(messy_text)
for step in steps:
    print(f"{step['number']}. {step['text']}")
    if step['type'] == 'decision':
        for branch in step['branches']:
            print(f"   - {branch}")
```

## Supported Input Formats

### 1. Numbered Lists
```
1. First step
2. Second step
3. Third step
```

### 2. Step Prefix Format
```
Step 1: Do this
Step 2: Do that
Step 3: Do something else
```

### 3. Bullet Lists
```
- First action
- Second action
- Third action
```

### 4. Tables
```
| Step | Action |
|------|--------|
| 1 | Connect USB |
| 2 | Boot system |
```

### 5. Narrative Paragraphs
```
First, open the application. Then, load configuration.
Next, verify authentication. Finally, display dashboard.
```

### 6. Mixed Formats
The simplifier can handle documents with mixed formatting styles.

## Decision Detection

The simplifier automatically detects decision points:

**Input:**
```
Check if user is authenticated. If authenticated, load dashboard.
Otherwise, redirect to login page.
```

**Output:**
```
3. Check if user is authenticated?
   - If yes: Load dashboard
   - If no: Redirect to login page
```

### Detected Patterns

- `if` statements
- `Check if` / `check whether`
- `Verify if` / `verify whether`
- Questions ending with `?`
- `Determine if` / `determine whether`

## Configuration

```python
config = {
    # Keep sub-steps (3a, 3b) indented under main step
    'preserve_substeps': True,  # default: True
    
    # Automatically add Start/End steps if missing
    'auto_terminators': True,  # default: True
    
    # Merge steps split across multiple lines
    'merge_multiline': True,  # default: True
}
```

## API Reference

### WorkflowSimplifier

#### `__init__(config: Optional[Dict] = None)`

Initialize simplifier with optional configuration.

#### `simplify(messy_text: str) -> str`

Convert messy workflow text to clean, numbered format.

**Parameters:**
- `messy_text`: Raw, unstructured workflow text

**Returns:**
- Clean, numbered workflow text

#### `simplify_to_dict(messy_text: str) -> List[Dict]`

Simplify and return structured data.

**Returns:**
- List of step dictionaries with keys:
  - `number`: int
  - `text`: str
  - `type`: 'step' | 'decision' | 'start' | 'end'
  - `branches`: Optional[List[str]]

## Examples

### Example 1: Tech Setup

**Input:**
```
Connect USB drive. Press F12 to boot. Select USB option.
Check if drive is detected. If detected, proceed with install.
If not detected, restart and try again.
```

**Output:**
```
1. Start
2. Connect USB drive
3. Press F12 to boot
4. Select USB option
5. Check if drive is detected?
   - If yes: Proceed with install
   - If no: Restart and try again
6. End
```

### Example 2: Business Process

**Input:**
```
Step 1: Receive inquiry
Step 2: Review details
Step 3: Determine validity
Step 4a: If valid, assign specialist
Step 4b: If invalid, send rejection
```

**Output:**
```
1. Start
2. Receive inquiry
3. Review details
4. Determine validity?
   - If yes: Assign specialist
   - If no: Send rejection
5. End
```

## Troubleshooting

### Steps Not Detected

If steps aren't being extracted:
- Ensure steps have sequential indicators (First, Then, Next)
- Use action verbs (Open, Click, Select, Press)
- Add numbering (1., 2., 3.)

### Decisions Not Detected

If decision points aren't recognized:
- Use clear decision language: "If X, then Y"
- Use "Check if" or "Verify whether"
- End questions with `?`

### Wrong Format Detected

If the wrong extraction method is used:
- Make input format more consistent
- Use explicit numbering
- Separate steps with blank lines

## Architecture

```
src/preprocessor/
├── text_cleaner.py       # Main orchestrator
├── step_extractor.py     # Extract steps from formats
├── decision_detector.py  # Detect decision logic
└── normalizer.py         # Normalize to consistent format
```

## Testing

```bash
# Run all tests
pytest tests/test_simplifier.py

# Run specific test class
pytest tests/test_simplifier.py::TestStepExtractor

# Run with coverage
pytest tests/test_simplifier.py --cov=src/preprocessor
```
