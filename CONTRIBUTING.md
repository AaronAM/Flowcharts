# Contributing to Flowchart Generator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Example input that causes the bug

### Suggesting Features

1. Check existing issues and roadmap
2. Create a new issue with:
   - Clear feature description
   - Use case and benefits
   - Proposed implementation (optional)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**:
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed
4. **Run tests**: `pytest tests/`
5. **Commit with clear messages**: `git commit -m "Add feature: description"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create Pull Request** with:
   - Clear description of changes
   - Reference to related issues
   - Test results

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Flowcharts.git
cd Flowcharts

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
pytest tests/
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and returns
- Write docstrings for classes and functions
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

## Testing Guidelines

- Write tests for all new features
- Ensure existing tests pass
- Aim for >80% code coverage
- Use descriptive test names
- Include edge cases and error conditions

## Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Keep docs clear and concise

## Commit Messages

Use clear, descriptive commit messages:

```
Add feature: workflow simplifier for narrative text

- Implement paragraph extraction with sequential indicators
- Add support for action verb detection
- Include tests for narrative formats
```

## Review Process

1. Maintainer reviews PR
2. Feedback provided if changes needed
3. Once approved, PR is merged
4. Your contribution is credited

## Questions?

Feel free to open an issue for questions or clarifications.

Thank you for contributing! 🚀
