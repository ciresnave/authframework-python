# AuthFramework Python SDK

This is the Python SDK workspace for AuthFramework. This workspace is configured to work independently of the main AuthFramework repository.

## Quick Start

### Open the Python SDK Workspace

1. **Option 1: Use the workspace file**
   - Open VS Code
   - Go to `File > Open Workspace from File...`
   - Select `authframework-python-sdk.code-workspace`

2. **Option 2: Open the folder directly**
   - Open VS Code
   - Go to `File > Open Folder...`
   - Select the `sdks/python` directory

### Setup Environment

The workspace is configured to use `uv` for Python environment management:

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest tests -v

# Run tests with coverage
uv run pytest tests --cov=authframework --cov-report=html

# Format code
uv run black src tests

# Lint code
uv run flake8 src tests

# Type check
uv run mypy src
```

### VS Code Tasks

The workspace includes several pre-configured tasks accessible via `Ctrl+Shift+P > Tasks: Run Task`:

- **Install Dependencies**: Runs `uv sync`
- **Run Tests**: Runs pytest with verbose output
- **Run Tests with Coverage**: Runs pytest with coverage reporting
- **Format Code**: Formats code with Black
- **Lint Code**: Lints code with Flake8
- **Type Check**: Type checks with MyPy
- **Build Package**: Builds the distribution package

### Debugging

The workspace includes launch configurations for:

- **Python: Current File**: Debug the currently open Python file
- **Python: Run Tests**: Debug pytest test execution

## Import Resolution

When working in this workspace, Pylance will correctly resolve all relative imports within the `authframework` package since the workspace root is at the Python SDK level, not the repository root.

## Integration with Main Repository

This workspace can be used independently for Python SDK development while still being part of the larger AuthFramework repository. Changes made here will be reflected in the main repository's `sdks/python/` directory.
