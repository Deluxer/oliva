# Welcome to Oliva Contributing Guide! 👋

We're thrilled that you're interested in contributing to Oliva! As an open-source multi-agent assistant, every contribution helps make AI more accessible to everyone 🚀

## Ways to Contribute

Every contribution matters, no matter how small! Here are some ways you can help:

- 📝 Fixing typos or improving documentation
- 🐛 Reporting and fixing bugs
- ✨ Adding new features or enhancements
- 🔧 Improving existing code
- 🎨 Enhancing the user interface
- 🌍 Adding support for different languages or platforms
- 🧪 Writing tests
- 📚 Improving examples and tutorials

## Quick Start Guide

1. **Fork & Clone**
   ```bash
   git clone https://github.com/Deluxer/oliva.git
   cd oliva
   git remote add upstream https://github.com/Deluxer/oliva.git
   ```

2. **Set Up Environment**
   ```bash
   # Create virtual environment with uv
   uv sync

   # Configure your environment
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

3. **Start Coding**
   ```bash
   # Create a new branch
   git checkout -b feature/amazing-feature
   # or
   git checkout -b fix/bug-description
   ```

## Development Guidelines

### 🔧 Technical Requirements

- Python 3.12+
- Docker (for Qdrant)
- Livekit account
- Deepgram account
- OpenAI API key

### 📝 Code Style

- Follow PEP 8
- Use type hints
- Write descriptive docstrings
- Keep functions focused and modular
- Add comments for complex logic

### ✅ Before Submitting

1. **Test Your Changes**
   ```bash
   # Run all tests
   make test

   # Check code style
   make lint
   ```

2. **Update Documentation**
   - Add docstrings for new functions
   - Update README if needed
   - Add examples for new features

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```
   Use conventional commits:
   - `feat:` new features
   - `fix:` bug fixes
   - `docs:` documentation
   - `test:` adding tests
   - `refactor:` code improvements

## 🐛 Reporting Issues

Found a bug? Have a suggestion? We'd love to hear from you! When creating an issue:

1. Check if the issue already exists
2. Include:
   - Your Python and dependency versions
   - Clear steps to reproduce
   - Expected vs actual behavior
   - Relevant logs or screenshots
   - Operating system details

## 🚀 Pull Request Process

1. Update your fork
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Push your changes
   ```bash
   git push origin your-branch-name
   ```

3. Open a PR with:
   - Clear description of changes
   - Screenshots for UI changes
   - Reference to related issues
   - List of breaking changes (if any)

4. Respond to review comments

## 📞 Questions

Please send your questions to gerardoangeln@gmail.com or creating a public issue.

## ✨ Recognition

Contributors are listed in our [CONTRIBUTORS.md](./CONTRIBUTORS.md) file. Thank you for making Oliva better! 🙏

Let's build the future of AI assistants together! 🤖✨