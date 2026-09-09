# Contributing to LitEngram

Thank you for your interest in contributing! This guide will help you get started.

---

## Code of Conduct

- Be respectful and inclusive
- Focus on the code, not the person
- Help others learn and grow

---

## How to Contribute

### 1. Report Bugs

Found a bug? Create a GitHub issue:

1. Go to: https://github.com/cyracaid/litengram/issues
2. Click "New issue"
3. Title: `[BUG] Short description`
4. Description:
   - What happened (symptoms)
   - Steps to reproduce
   - Expected vs actual
   - Environment (OS, Python, Zotero version)

### 2. Suggest Features

Have an idea? Create a discussion:

1. Go to: https://github.com/cyracaid/litengram/discussions
2. Create "New discussion"
3. Category: "Ideas"
4. Describe what you want and why

### 3. Improve Documentation

Found a typo or unclear section?

1. Fork the repo
2. Edit .md files
3. Submit a pull request

### 4. Write Code

Want to add a feature?

1. Create an issue first (discuss approach)
2. Get approval from maintainers
3. Fork the repo
4. Create a branch: `feature/your-feature-name`
5. Write code + tests
6. Submit a pull request

---

## Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/litengram.git
cd litengram

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dev dependencies
pip install -r requirements.txt
pip install pytest black mypy  # Dev tools

# 4. Set up git hooks (optional)
# (future: pre-commit hooks)

# 5. Create a branch
git checkout -b feature/your-feature-name
```

---

## Code Style

- **Format**: Black (`black scripts/`)
- **Type hints**: Use for public APIs
- **Tests**: Write for new features
- **Docstrings**: Include for all functions

```python
# Example
def process_annotation(text: str, highlight_text: str) -> Dict[str, str]:
    """
    Extract 4-layer structure from annotation text.
    
    Args:
        text: Full annotation text
        highlight_text: The highlighted portion
    
    Returns:
        Dict with keys: layer_1_definition, layer_2_role, etc
    """
    ...
```

---

## Testing

```bash
# Run existing tests
pytest tests/

# Run specific test
pytest tests/test_parser.py::test_extract_definition

# With coverage
pytest --cov=scripts tests/
```

---

## Git Workflow

1. **Create branch** from `main`
2. **Make changes** with clear commit messages
3. **Push** to your fork
4. **Create PR** with:
   - Title: Clear description
   - Body: Why this change, what it fixes
   - Linked issue: "Fixes #123"
5. **Respond to review** comments
6. **Merge** when approved

Example PR:
```
Title: Add batch annotation verification

Body:
Adds db.verify_annotations() method to check for missing
authorName or comment fields.

Fixes #42
```

---

## Commit Messages

Use conventional commits:

```
feat: add batch verification method
fix: handle database lock timeout
docs: clarify 4-layer structure
test: add unit tests for parser
refactor: extract markdown parsing logic
chore: update dependencies
```

---

## Review Process

1. **Automated checks**: Tests pass, code style OK
2. **Code review**: Maintainer reviews for quality
3. **Approval**: 2 maintainers approve
4. **Merge**: Squash commits if needed

---

## Areas for Contribution

### High Priority
- [ ] Expand API_REFERENCE.md with more examples
- [ ] Add tests for annotation parser
- [ ] Create CI/CD workflows (.github/workflows/)
- [ ] Support additional languages (Spanish, French, etc)

### Medium Priority
- [ ] Improve error messages
- [ ] Add logging framework
- [ ] Create web UI prototype
- [ ] Obsidian/Logseq/Roam integration examples

### Low Priority
- [ ] Performance optimizations
- [ ] Additional LLM models
- [ ] Custom domain templates

---

## Questions?

- GitHub Discussions: https://github.com/cyracaid/litengram/discussions
- Issues: https://github.com/cyracaid/litengram/issues
- Email: [contact info if available]

---

Thank you for contributing! 🎉
