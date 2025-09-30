"""Integration test configuration with mock server."""

from typing import AsyncGenerator

import httpx
import pytest
import respx

from authframework import AuthFrameworkClient


@pytest.fixture
async def mock_server():
    """Set up a mock AuthFramework server for integration tests."""
    with respx.mock(base_url="http://localhost:8088") as mock:
        # Health endpoints
        mock.get("/health").mock(
            return_value=httpx.Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "status": "healthy",
                        "timestamp": "2025-09-29T10:00:00Z",
                        "version": "1.0.0",
                    },
                },
            )
        )

        mock.get("/health/detailed").mock(
            return_value=httpx.Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "status": "healthy",
                        "timestamp": "2025-09-29T10:00:00Z",
                        "version": "1.0.0",
                        "services": {
                            "database": {"status": "healthy"},
                            "cache": {"status": "healthy"},
                        },
                    },
                },
            )
        )

        mock.get("/health/ready").mock(
            return_value=httpx.Response(200, json={"success": True, "data": {"status": "ready"}})
        )

        mock.get("/health/live").mock(
            return_value=httpx.Response(200, json={"success": True, "data": {"status": "alive"}})
        )

        # Auth endpoints (require authentication)
        mock.get("/auth/profile").mock(
            return_value=httpx.Response(
                401,
                json={
                    "success": False,
                    "error": {"code": "UNAUTHORIZED", "message": "Authentication required"},
                },
            )
        )

        mock.post("/auth/login").mock(
            return_value=httpx.Response(
                401,
                json={
                    "success": False,
                    "error": {
                        "code": "INVALID_CREDENTIALS",
                        "message": "Invalid username or password",
                    },
                },
            )
        )

        # Token endpoints
        mock.post("/tokens/validate").mock(
            return_value=httpx.Response(
                401,
                json={
                    "success": False,
                    "error": {"code": "INVALID_TOKEN", "message": "Token is invalid or expired"},
                },
            )
        )

        mock.post("/tokens/refresh").mock(
            return_value=httpx.Response(
                401,
                json={
                    "success": False,
                    "error": {
                        "code": "INVALID_REFRESH_TOKEN",
                        "message": "Refresh token is invalid or expired",
                    },
                },
            )
        )

        # Admin endpoints (require authentication)
        mock.get("/admin/users").mock(
            return_value=httpx.Response(
                401,
                json={
                    "success": False,
                    "error": {"code": "UNAUTHORIZED", "message": "Authentication required"},
                },
            )
        )

        yield mock


@pytest.fixture
async def integration_client(mock_server) -> AsyncGenerator[AuthFrameworkClient, None]:
    """Create a client for integration tests with mock server."""
    async with AuthFrameworkClient(
        base_url="http://localhost:8088",
        timeout=10.0,
        retries=2,
    ) as client:
        yield client
