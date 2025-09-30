# Contributing to AuthFramework Python SDK

We love your input! We want to make contributing to the AuthFramework Python SDK as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Setup

### Prerequisites

- Python 3.9+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Git

### Setup Development Environment

```bash
# Clone your fork
git clone https://github.com/yourusername/authframework-python.git
cd authframework-python

# Install dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=authframework --cov-report=html

# Run specific test file
uv run pytest tests/test_client.py -v

# Run tests matching a pattern
uv run pytest -k "test_auth"
```

### Code Quality

```bash
# Format code with Black
uv run black src tests

# Sort imports with isort
uv run isort src tests

# Lint with flake8
uv run flake8 src tests

# Type check with mypy
uv run mypy src

# Run all quality checks
uv run pre-commit run --all-files
```

## Code Style

- We use [Black](https://black.readthedocs.io/) for code formatting
- We use [isort](https://pycqa.github.io/isort/) for import sorting
- We use [flake8](https://flake8.pycqa.org/) for linting
- We use [mypy](http://mypy-lang.org/) for type checking
- Line length is 100 characters
- We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide

## Documentation

- All public APIs must have docstrings
- Use Google-style docstrings
- Update README.md if you change functionality
- Add examples for new features

## Testing

- Write tests for all new functionality
- Maintain or improve test coverage
- Use pytest fixtures for common test setup
- Mock external dependencies
- Test both success and error cases

## Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test changes
- `refactor:` for code refactoring
- `style:` for formatting changes
- `chore:` for maintenance tasks

Examples:
```
feat: add support for custom token validation
fix: handle network timeouts in auth requests
docs: update FastAPI integration examples
test: add tests for password reset flow
```

## Issue Reporting

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/ciresnave/authframework-python/issues/new).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists or is planned
2. Open an issue describing the feature
3. Explain the use case and benefit
4. Be open to discussion and feedback

## Security Issues

Please do not report security vulnerabilities through public GitHub issues. Instead, send an email to ciresnave@gmail.com.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open a [discussion](https://github.com/ciresnave/authframework-python/discussions) if you have questions about contributing!