# 🤝 Contributing to Video Automation

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## Ways to Contribute

- 🐛 **Report bugs** - Help us identify and fix issues
- 💡 **Suggest features** - Share ideas for improvements
- 📖 **Improve documentation** - Help make guides clearer
- 💻 **Submit code** - Fix bugs or add features
- 🎨 **Design improvements** - UI/UX enhancements
- 🧪 **Add tests** - Improve code reliability

---

## Getting Started

### 1. Fork the Repository

Click the "Fork" button on GitHub to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/video-automation.git
cd video-automation
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

---

## Development Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up Configuration

Follow [SETUP.md](SETUP.md) to configure your development environment.

### Run Tests

```bash
python -m pytest tests/
```

---

## Code Guidelines

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

### Example

```python
def process_video(file_path: str) -> dict:
    """
    Process a video file and return metadata.
    
    Args:
        file_path: Path to the video file
        
    Returns:
        dict: Video metadata including title, description
    """
    # Implementation here
    pass
```

### Code Organization

- Keep related code together
- Use modules for different services
- Avoid circular imports
- Follow existing project structure

---

## Making Changes

### 1. Write Code

Make your changes following the code guidelines above.

### 2. Test Your Changes

```bash
# Run all tests
python -m pytest

# Run specific test
python -m pytest tests/test_workflow.py

# Test manually
python main.py
```

### 3. Update Documentation

If your change affects:
- **Setup**: Update `SETUP.md`
- **Usage**: Update `README.md`
- **Configuration**: Update `config.example.py` comments
- **Troubleshooting**: Update `TROUBLESHOOTING.md`

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add support for .avi video format"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

---

## Submitting a Pull Request

### 1. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 2. Create Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill out the PR template

### PR Template

```markdown
## Description
Brief description of your changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
How did you test your changes?

## Checklist
- [ ] Code follows project style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No sensitive data in commits
```

### 3. Wait for Review

Maintainers will review your PR and may:
- Approve and merge
- Request changes
- Ask questions

---

## Reporting Bugs

### Before Reporting

1. Check [existing issues](https://github.com/YOUR_USERNAME/video-automation/issues)
2. Try the latest version
3. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Bug Report Template

```markdown
**Describe the bug**
Clear description of what happened

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen

**Environment**
- OS: [e.g., Windows 11]
- Python version: [e.g., 3.12.0]
- Error message: [full traceback]

**Additional context**
Any other relevant information
```

---

## Suggesting Features

### Feature Request Template

```markdown
**Is your feature related to a problem?**
Description of the problem

**Describe the solution**
How you'd like it to work

**Alternatives considered**
Other solutions you've thought about

**Additional context**
Mockups, examples, etc.
```

---

## Code Review Process

### What We Look For

- ✅ Code quality and readability
- ✅ Tests for new features
- ✅ Documentation updates
- ✅ No breaking changes (or clearly documented)
- ✅ Security considerations
- ✅ Performance impact

### Review Timeline

- Initial response: Within 48 hours
- Full review: Within 1 week
- Merge: After approval and CI passes

---

## Community Guidelines

### Be Respectful

- Use welcoming and inclusive language
- Respect differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Be Collaborative

- Help others learn and grow
- Share knowledge generously
- Give credit where due
- Assume good intentions

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

- 💬 Open a [Discussion](https://github.com/YOUR_USERNAME/video-automation/discussions)
- 📧 Email the maintainer
- 📖 Read the [FAQ](FAQ.md)

---

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
