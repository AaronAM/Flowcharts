# 🔹 Flowchart Generator with Workflow Simplifier

Automated flowchart generator that converts messy workflow text into clean, numbered formats and generates flowchart visualizations.

## ✨ Features

### Workflow Simplifier
- **Multiple input formats**: Paragraphs, numbered lists, bullets, tables, mixed formats
- **Decision detection**: Automatic detection of if/then/else logic
- **Branch structuring**: Converts decisions to clear branch format
- **Smart extraction**: Handles narrative text, sequential indicators, action verbs
- **Automatic terminators**: Adds Start/End steps if missing
- **Configurable**: Customize behavior with configuration options

### Coming Soon
- Flowchart image generation
- Multiple output formats (PNG, SVG, PDF)
- Custom styling and themes
- Web interface

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/AaronAM/Flowcharts.git
cd Flowcharts

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Basic Usage

```bash
# Simplify a messy workflow
py -m cli.main simplify messy_workflow.txt -o clean_workflow.txt

# Analyze workflow structure
py -m cli.main analyze messy_workflow.txt

# Verbose output
py -m cli.main simplify messy.txt -o clean.txt -v
```

### Python API

```python
from src.preprocessor import WorkflowSimplifier

# Basic usage
simplifier = WorkflowSimplifier()
clean_text = simplifier.simplify(messy_text)
print(clean_text)

# Get structured data
steps = simplifier.simplify_to_dict(messy_text)
for step in steps:
    print(f"{step['number']}. {step['text']}")
    if step['type'] == 'decision':
        for branch in step['branches']:
            print(f"   - {branch}")
```

## 📋 Examples

### Example 1: From Paragraphs

**Input:**
```
First, open the application. Then, load configuration.
Next, verify authentication. Finally, display dashboard.
```

**Output:**
```
1. Start
2. Open the application
3. Load configuration
4. Verify authentication
5. Display dashboard
6. End
```

### Example 2: With Decisions

**Input:**
```
Check if user is authenticated. If authenticated, load dashboard.
Otherwise, redirect to login page.
```

**Output:**
```
1. Start
2. Check if user is authenticated?
   - If yes: Load dashboard
   - If no: Redirect to login page
3. End
```

### Example 3: Tech Setup Workflow

**Input:**
```
Step 1: Connect USB drive
Step 2: Press F12 to boot
Step 3: Check if drive detected
Step 4: If detected, install OS
Step 5: If not, restart and retry
```

**Output:**
```
1. Start
2. Connect USB drive
3. Press F12 to boot
4. Check if drive detected?
   - If yes: Install OS
   - If no: Restart and retry
5. End
```

## 🛠️ Supported Input Formats

1. **Numbered lists**: `1. 2. 3.`
2. **Step prefix**: `Step 1: Step 2:`
3. **Bullets**: `- * •`
4. **Tables**: Markdown and text tables
5. **Paragraphs**: Narrative with sequential indicators
6. **Mixed formats**: Combination of above

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_simplifier.py

# Run with coverage
pytest tests/ --cov=src/preprocessor

# Verbose output
pytest tests/ -v
```

## 📁 Project Structure

```
Flowcharts/
├── src/
│   ├── preprocessor/          # Workflow simplifier
│   │   ├── text_cleaner.py     # Main orchestrator
│   │   ├── step_extractor.py   # Extract steps
│   │   ├── decision_detector.py # Detect decisions
│   │   └── normalizer.py       # Normalize format
│   ├── parser/                # (Coming soon)
│   ├── builder/               # (Coming soon)
│   └── renderer/              # (Coming soon)
├── cli/
│   └── main.py                # CLI commands
├── tests/
│   └── test_simplifier.py     # Comprehensive tests
├── docs/
│   └── SIMPLIFIER.md          # Simplifier docs
├── requirements.txt
└── README.md
```

## 📚 Documentation

- [Workflow Simplifier Documentation](docs/SIMPLIFIER.md)
- [API Reference](docs/API.md) (Coming soon)
- [Examples](examples/) (Coming soon)

## 🛣️ Roadmap

### Phase 1: Workflow Simplifier ✅
- [x] Core simplification engine
- [x] Multiple format support
- [x] Decision detection
- [x] CLI commands
- [x] Comprehensive tests
- [x] Documentation

### Phase 2: Flowchart Generator (In Progress)
- [ ] Text-to-flowchart parser
- [ ] Flowchart builder
- [ ] Image renderer (PNG, SVG)
- [ ] Layout optimization
- [ ] Custom styling

### Phase 3: Advanced Features
- [ ] Web interface
- [ ] API server
- [ ] Real-time preview
- [ ] Export to Mermaid/PlantUML
- [ ] Collaboration features

### Phase 4: Integrations
- [ ] GitHub Actions integration
- [ ] VS Code extension
- [ ] Confluence/Jira plugins
- [ ] CI/CD pipeline visualization

## 🤝 Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 👤 Author

**Aren Garro**
- GitHub: [@AaronAM](https://github.com/AaronAM)
- Company: Aren Garro LLC

## 🚀 Use Cases

- **Documentation**: Convert process docs to visual flowcharts
- **Onboarding**: Create training materials from SOPs
- **Process Improvement**: Visualize and optimize workflows
- **Technical Writing**: Auto-generate diagrams from text
- **Compliance**: Document procedures visually
- **Software Development**: Visualize algorithms and logic

## ⭐ Star History

If you find this useful, please star the repository!

---

**Built with ❤️ by Aren Garro | Simplifying workflows, one flowchart at a time**
