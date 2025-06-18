# Contributing to Dify Knowledge Client

Thank you for your interest in contributing to the Dify Knowledge Client! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/DifyKnowledgeClient.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests (when available)
6. Commit your changes: `git commit -am 'Add new feature'`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your Dify API credentials

4. Run the CLI:
   ```bash
   python cli.py
   ```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Add type hints where appropriate

## Adding New Features

When adding new features:

1. **API Methods**: Add them to the appropriate manager class in `dify_client/`
2. **CLI Commands**: Update the relevant menu in `cli.py`
3. **Documentation**: Update the README and add examples if needed
4. **Error Handling**: Ensure proper error handling with meaningful messages

## Testing

Currently, the project doesn't have automated tests. When adding tests:

- Use pytest for testing
- Place tests in a `tests/` directory
- Mock API calls to avoid requiring actual API credentials
- Test both success and error cases

## Documentation

- Update the README for any new features
- Add docstrings to new functions and classes
- Include usage examples for complex features
- Update the API documentation if endpoints change

## Pull Request Guidelines

1. **Title**: Use a clear, descriptive title
2. **Description**: Explain what changes you made and why
3. **Small PRs**: Keep pull requests focused on a single feature or fix
4. **Documentation**: Update relevant documentation
5. **Examples**: Add examples for new features

## Reporting Issues

When reporting issues:

1. Check if the issue already exists
2. Use a clear, descriptive title
3. Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Error messages (if any)
   - Environment details (OS, Python version)

## Feature Requests

Feature requests are welcome! Please:

1. Check if the feature has already been requested
2. Provide a clear use case
3. Explain why this feature would be valuable
4. If possible, suggest an implementation approach

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect different viewpoints and experiences

## Questions?

If you have questions about contributing, feel free to:

- Open an issue with the "question" label
- Start a discussion in the GitHub Discussions tab

Thank you for contributing to make Dify Knowledge Client better!