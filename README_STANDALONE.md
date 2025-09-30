# AuthFramework Python SDK

The official Python SDK for AuthFramework authentication and authorization service.

[![PyPI version](https://badge.fury.io/py/authframework.svg)](https://badge.fury.io/py/authframework)
[![Python Support](https://img.shields.io/pypi/pyversions/authframework.svg)](https://pypi.org/project/authframework/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/ciresnave/authframework-python/workflows/Tests/badge.svg)](https://github.com/ciresnave/authframework-python/actions)
[![Coverage](https://codecov.io/gh/authframework/authframework-python/branch/main/graph/badge.svg)](https://codecov.io/gh/authframework/authframework-python)

## Features

- 🔐 **Complete Authentication**: Login, logout, registration, password reset
- 🛡️ **Authorization**: Role-based access control (RBAC) and permissions
- 🔑 **Token Management**: JWT token validation and refresh
- 👤 **User Management**: Profile management and user operations
- 🔧 **Admin Operations**: User administration and system management
- 🚀 **Framework Integrations**: FastAPI and Flask middleware
- ⚡ **Async Support**: Full async/await support with httpx
- 🧪 **Type Safety**: Full type hints and Pydantic validation
- 📊 **Comprehensive Testing**: High test coverage with pytest

## Installation

```bash
pip install authframework
```

### With Framework Integrations

```bash
# For FastAPI integration
pip install "authframework[fastapi]"

# For Flask integration  
pip install "authframework[flask]"

# For development
pip install "authframework[dev]"
```

## Quick Start

### Basic Usage

```python
import asyncio
from authframework import AuthFrameworkClient

async def main():
    # Initialize the client
    client = AuthFrameworkClient(
        base_url="https://your-auth-server.com",
        api_key="your-api-key"  # Optional
    )
    
    # Login
    response = await client.auth.login("username", "password")
    print(f"Access token: {response['access_token']}")
    
    # Get user profile
    profile = await client.auth.get_profile()
    print(f"User: {profile['username']}")
    
    # Validate token
    validation = await client.tokens.validate()
    print(f"Token valid: {validation['valid']}")

asyncio.run(main())
```

### FastAPI Integration

```python
from fastapi import FastAPI, Depends
from authframework import AuthFrameworkClient
from authframework.integrations.fastapi import AuthFrameworkFastAPI, AuthUser

app = FastAPI()
client = AuthFrameworkClient("https://your-auth-server.com")
auth = AuthFrameworkFastAPI(client)

@app.get("/protected")
async def protected_route(user: AuthUser = Depends(auth.require_auth())):
    return {"message": f"Hello {user.username}!", "roles": user.roles}

@app.get("/admin-only")
async def admin_route(user: AuthUser = Depends(auth.require_role("admin"))):
    return {"message": "Admin access granted"}
```

### Flask Integration

```python
from flask import Flask
from authframework import AuthFrameworkClient
from authframework.integrations.flask import AuthFrameworkFlask

app = Flask(__name__)
client = AuthFrameworkClient("https://your-auth-server.com")
auth = AuthFrameworkFlask(client)

@app.route("/protected")
@auth.require_auth()
def protected_route():
    user = auth.get_current_user()
    return {"message": f"Hello {user.username}!", "roles": user.roles}

@app.route("/admin-only")  
@auth.require_role("admin")
def admin_route():
    return {"message": "Admin access granted"}
```

## Documentation

- **[API Reference](https://authframework-python.readthedocs.io/)**: Complete API documentation
- **[Examples](./examples/)**: Code examples and use cases
- **[Integration Guides](./docs/integrations/)**: Framework-specific guides
- **[Migration Guide](./docs/migration.md)**: Upgrading from previous versions

## Development

### Prerequisites

- Python 3.9+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Setup

```bash
# Clone the repository
git clone https://github.com/ciresnave/authframework-python.git
cd authframework-python

# Install dependencies with uv (recommended)
uv sync

# Or with pip
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run tests with uv
uv run pytest

# Run tests with coverage
uv run pytest --cov=authframework --cov-report=html

# Run specific test file
uv run pytest tests/test_client.py -v
```

### Code Quality

```bash
# Format code
uv run black src tests

# Sort imports
uv run isort src tests

# Lint code
uv run flake8 src tests

# Type check
uv run mypy src
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass (`uv run pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Support

- **Documentation**: [https://authframework-python.readthedocs.io/](https://authframework-python.readthedocs.io/)
- **Issues**: [GitHub Issues](https://github.com/ciresnave/authframework-python/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ciresnave/authframework-python/discussions)
- **Security**: Report security issues to security@authframework.dev

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.