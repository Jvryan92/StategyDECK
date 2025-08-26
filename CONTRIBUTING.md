# Contributing to StrategyDECK

Thank you for your interest in contributing to the StrategyDECK project! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic familiarity with SVG and icon design principles

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/StategyDECK.git
   cd StategyDECK
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Pre-commit Hooks** (Optional but recommended)
   ```bash
   pip install pre-commit
   pre-commit install
   ```

4. **Test the Setup**
   ```bash
   # Generate icons
   python scripts/generate_icons.py
   
   # Run tests
   pytest tests/ -v
   
   # Check code quality
   flake8 scripts/
   black --check scripts/ tests/
   ```

## 📋 Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Follow the existing code style and conventions
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes
```bash
# Run the full test suite
pytest tests/ -v

# Check code formatting
black scripts/ tests/
flake8 scripts/

# Test icon generation
python scripts/generate_icons.py
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add your feature description"
```

Use conventional commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for adding tests
- `refactor:` for code refactoring

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## 🎯 Types of Contributions

### Icon Improvements
- New icon variants or finishes
- Updates to color schemes or design tokens
- Master SVG file enhancements

### Code Contributions
- Bug fixes in icon generation script
- Performance optimizations
- New utility functions

### Documentation
- README improvements
- Code comments and docstrings
- Usage examples and guides

### Workflow & Infrastructure
- GitHub Actions workflow improvements
- Testing enhancements
- Development tooling

## 📏 Code Style Guidelines

### Python
- Follow PEP 8 style guidelines
- Use Black for code formatting (line length: 127 characters)
- Add type hints where appropriate
- Include docstrings for functions and classes

### Documentation
- Use clear, concise language
- Include code examples where helpful
- Update relevant documentation when making changes

### Git Commits
- Use descriptive commit messages
- Keep commits focused and atomic
- Reference issues when applicable

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_generate_icons.py -v

# Run with coverage
pytest tests/ --cov=scripts
```

### Writing Tests
- Add tests for new functions or features
- Use descriptive test names
- Include edge cases and error conditions
- Follow existing test patterns in `tests/test_generate_icons.py`

## 📚 Project Structure

```
StrategyDECK/
├── .github/
│   ├── workflows/          # GitHub Actions
│   └── dependabot.yml      # Dependency updates
├── assets/
│   ├── masters/            # Source SVG files
│   └── icons/              # Generated variants
├── scripts/
│   └── generate_icons.py   # Main generation script
├── tests/
│   └── test_*.py           # Test files
├── docs/
│   └── *.md                # Documentation
└── requirements.txt        # Python dependencies
```

## 🔄 Automated Processes

The repository uses GitHub Actions for:

- **Continuous Integration**: Runs tests and linting on PRs
- **Continuous Deployment**: Generates and deploys assets
- **Issue Management**: Auto-labels and assigns issues
- **PR Management**: Auto-assigns reviewers and labels PRs
- **Documentation**: Updates docs and examples

When you submit a PR, these workflows will automatically:
- Run tests across multiple Python versions
- Check code formatting and style
- Generate icon assets
- Assign appropriate reviewers
- Apply size labels (XS, S, M, L, XL)

## 🐛 Reporting Issues

When reporting bugs or requesting features:

1. **Search existing issues** first
2. **Use the issue templates** when available
3. **Provide clear reproduction steps** for bugs
4. **Include system information** (Python version, OS)
5. **Add relevant labels** or let the auto-labeler handle it

## 💬 Getting Help

- **GitHub Issues**: For bugs, features, and questions
- **Discussions**: For general questions and community chat
- **Pull Request Reviews**: For code-specific feedback

## 📄 License

By contributing to StrategyDECK, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to StrategyDECK! 🎉