# AuthFramework Python SDK - Integration Testing Roadmap

## Current State

The AuthFramework Python SDK has been successfully separated into its own workspace and is functioning well:

- **37/39 meaningful tests passing** ✅
- **Core SDK functionality working** ✅
- **Mock server infrastructure partially implemented** ✅
- **2 integration tests failing** due to missing real server

### Test Results Summary
```
37 passed, 2 failed, 4 skipped, 4 warnings
Coverage: 44%
```

### Failing Tests
Both failures are integration tests expecting authentication errors (401) but receiving 404 Not Found:
- `test_health_endpoint_accessible` 
- `test_auth_endpoints_require_authentication`

## Problem Statement

The current integration tests attempt to connect to `http://localhost:8088` expecting a real AuthFramework server, but:
1. No server is running in the standalone Python SDK workspace
2. The existing test server management (`integration_conftest.py`) expects the full Rust project structure
3. Mock-only testing doesn't validate real server compatibility

## Solution: Hybrid Testing Approach

Implement both mock and real server testing to ensure:
- **Fast feedback** with mock servers
- **Real integration validation** with actual AuthFramework server
- **CI/CD compatibility** without requiring Rust toolchain

## Implementation Plan

### Phase 1: Pre-built Server Infrastructure

#### 1.1 Server Binary Management
Create test server infrastructure:

```
tests/
├── test-servers/                   # Pre-built server binaries
│   ├── windows/
│   │   └── auth-framework.exe
│   ├── linux/
│   │   └── auth-framework
│   ├── macos/
│   │   └── auth-framework
│   ├── download_servers.py         # Script to fetch/update binaries
│   └── versions.json               # Track server versions
```

#### 1.2 Server Manager Implementation
Create `tests/server_manager.py`:

```python
class AuthFrameworkTestServer:
    """Manages pre-built AuthFramework server binaries for testing."""
    
    def __init__(self, port: int = None):
        self.port = port or self._find_free_port()
        self.binary_path = self._get_platform_binary()
        self.process = None
    
    async def start(self) -> None:
        """Start server with test configuration."""
        
    async def stop(self) -> None:
        """Clean shutdown of test server."""
        
    def _get_platform_binary(self) -> Path:
        """Get the appropriate binary for current platform."""
        
    def _find_free_port(self) -> int:
        """Find an available port for testing."""
```

### Phase 2: Test Structure Reorganization

#### 2.1 Separate Mock and Real Tests
```
tests/
├── integration/
│   ├── conftest.py                 # Both mock and real server fixtures
│   ├── test_mock_integration.py    # Fast mock-based tests
│   └── test_real_integration.py    # Real server integration tests
└── unit/                          # Existing unit tests
```

#### 2.2 Pytest Markers
```python
# Markers for different test types
@pytest.mark.mock          # Fast mock server tests
@pytest.mark.integration   # Real server tests  
@pytest.mark.slow          # Mark real server tests as slow
@pytest.mark.requires_auth # Tests needing authentication
```

#### 2.3 Fixture Strategy
```python
@pytest.fixture(params=["mock", "real"])
async def integration_client(request):
    """Parameterized fixture for both mock and real testing."""
    if request.param == "mock":
        return await create_mock_client()
    else:
        return await create_real_server_client()

@pytest.fixture(scope="session")
async def real_server():
    """Session-scoped real server for integration tests."""
    server = AuthFrameworkTestServer()
    await server.start()
    yield server
    await server.stop()
```

### Phase 3: CI/CD Integration

#### 3.1 Test Execution Strategy
```bash
# Development - fast feedback
pytest -m mock

# Pre-commit - comprehensive validation
pytest -m "mock or integration"

# CI/CD - full test suite
pytest --cov=authframework --cov-report=html
```

#### 3.2 GitHub Actions Integration
```yaml
- name: Run Mock Tests
  run: uv run pytest -m mock -v

- name: Download Test Servers
  run: python tests/test-servers/download_servers.py

- name: Run Integration Tests
  run: uv run pytest -m integration -v
```

## Current Files That Need Updates

### 1. `tests/integration/conftest.py`
- Currently has basic mock server setup
- Needs real server fixture integration
- Requires parameterized client fixture

### 2. `tests/integration_conftest.py`
- Contains sophisticated server management for full project
- Needs adaptation for pre-built binaries
- Should be merged/replaced with new approach

### 3. Test Files
- `tests/integration/test_server_integration.py` - Update assertions for proper error handling
- `tests/integration/test_simple_integration.py` - Fix authentication error expectations

## Dependencies and Requirements

### Python Dependencies (Already Available)
- `pytest` - Test framework
- `pytest-asyncio` - Async test support
- `respx` - HTTP mocking
- `httpx` - HTTP client

### External Requirements
- **Pre-built AuthFramework server binaries** for Windows, Linux, macOS
- Server binaries should be built from the same codebase version as SDK targets
- Binaries need to support test configuration (in-memory database, test secrets, etc.)

## Expected Benefits

1. **Developer Experience**
   - Fast mock tests for immediate feedback
   - Comprehensive real server validation
   - No Rust toolchain requirement

2. **CI/CD Reliability**
   - Consistent test environment
   - Platform-specific testing
   - Reduced external dependencies

3. **Quality Assurance**
   - Real API compatibility validation
   - Error handling verification
   - Performance characteristics testing

## Next Steps

1. **Generate pre-built server binaries** from Rust AuthFramework project
2. **Implement server manager** and download infrastructure
3. **Update test fixtures** to support both mock and real testing
4. **Reorganize test files** according to new structure
5. **Update CI/CD pipelines** to use new testing approach
6. **Document testing procedures** for contributors

## Notes

- Current SDK test coverage is 44% - focus on increasing this with both mock and real tests
- Integration tests should validate not just success cases but proper error handling
- Consider adding performance/load testing with real server infrastructure
- Server binary versioning should align with SDK release versions

## Files Modified in This Session

- `pyrightconfig.json` - Fixed malformed JSON configuration
- `tests/integration/conftest.py` - Added basic mock server setup (needs expansion)

## Command References

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest tests -v

# Run with coverage
uv run pytest tests --cov=authframework --cov-report=html

# Run specific test types (when implemented)
uv run pytest -m mock -v
uv run pytest -m integration -v
```