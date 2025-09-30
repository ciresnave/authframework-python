"""Schema-based integration tests for API response validation.

Copyright (c) 2025 AuthFramework. All rights reserved.
"""

import os
import pytest
from datetime import datetime
from typing import Dict, Any

from pydantic_core import ValidationError

from authframework.models.api_responses import (
    ApiResponse,
    TokenValidationResponse,
    TokenValidationData,
    HealthCheckResponse,
    HealthCheckData,
    parse_api_response,
    ensure_success_response,
    extract_response_data,
)
from authframework.models import UserInfo, parse_datetime


class TestApiResponseSchemas:
    """Test API response schema validation."""

    def test_token_validation_response_valid_structure(self):
        """Test that valid token validation response passes schema validation."""
        valid_response = {
            "success": True,
            "data": {
                "id": "user123",
                "username": "testuser",
                "email": "test@example.com",
                "roles": ["user", "admin"],
                "mfa_enabled": True,
                "created_at": "2024-01-01T00:00:00Z",
                "last_login": "2024-01-01T12:00:00Z",
                "token_type": "bearer",
                "expires_at": "2024-01-02T00:00:00Z"
            },
            "message": "Token is valid"
        }
        
        # Should not raise any exceptions
        response = parse_api_response(valid_response, TokenValidationResponse)
        assert response.success is True
        assert response.data.id == "user123"
        assert response.data.username == "testuser"
        assert "user" in response.data.roles
        assert "admin" in response.data.roles

    def test_token_validation_response_rejects_old_format(self):
        """Test that old API format (with 'valid' instead of 'success') is rejected."""
        old_format_response = {
            "valid": True,  # Old field name - should be rejected
            "user_id": "user123",  # Old field name - should be rejected
            "username": "testuser",
            "scopes": ["user"]  # Old field name - should be rejected
        }
        
        with pytest.raises(ValidationError) as exc_info:
            parse_api_response(old_format_response, TokenValidationResponse)
        
        error_str = str(exc_info.value)
        # Should mention missing required fields
        assert "success" in error_str or "Field required" in error_str

    def test_token_validation_response_rejects_wrong_field_names(self):
        """Test that wrong field names in data section are rejected."""
        wrong_fields_response = {
            "success": True,
            "data": {
                "user_id": "user123",  # Should be 'id'
                "username": "testuser",
                "scopes": ["user"],  # Should be 'roles'
                "mfa_enabled": False
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            parse_api_response(wrong_fields_response, TokenValidationResponse)
        
        error_str = str(exc_info.value)
        # Should mention missing required 'id' field
        assert "id" in error_str and "Field required" in error_str

    def test_token_validation_response_missing_data_field(self):
        """Test that response without data field is rejected."""
        missing_data_response = {
            "success": True,
            "message": "Token is valid"
            # Missing 'data' field
        }
        
        with pytest.raises(ValidationError) as exc_info:
            parse_api_response(missing_data_response, TokenValidationResponse)
        
        # The data field is optional in our generic ApiResponse, but validation
        # will still fail when trying to access required fields in the data

    def test_token_validation_response_extra_fields_rejected(self):
        """Test that unexpected extra fields are rejected due to extra='forbid'."""
        extra_fields_response = {
            "success": True,
            "data": {
                "id": "user123",
                "username": "testuser",
                "roles": ["user"],
                "mfa_enabled": False,
                "unexpected_field": "should_be_rejected"  # Extra field
            },
            "unexpected_top_level": "also_rejected"  # Extra field
        }
        
        with pytest.raises(ValidationError) as exc_info:
            parse_api_response(extra_fields_response, TokenValidationResponse)
        
        error_str = str(exc_info.value)
        assert "unexpected" in error_str.lower() or "extra" in error_str.lower()

    def test_health_check_response_valid_structure(self):
        """Test that valid health check response passes schema validation."""
        valid_health_response = {
            "success": True,
            "data": {
                "status": "healthy",
                "version": "1.0.0",
                "uptime": 3600,
                "timestamp": "2024-01-01T00:00:00Z"
            }
        }
        
        response = parse_api_response(valid_health_response, HealthCheckResponse)
        assert response.success is True
        assert response.data.status == "healthy"
        assert response.data.version == "1.0.0"
        assert response.data.uptime == 3600

    def test_utility_functions_with_valid_response(self):
        """Test utility functions with valid API response."""
        valid_response = {
            "success": True,
            "data": {
                "id": "user123",
                "username": "testuser",
                "roles": ["user"],
                "mfa_enabled": False
            },
            "message": "Success"
        }
        
        # Should not raise exceptions
        ensure_success_response(valid_response)
        data = extract_response_data(valid_response)
        
        assert data["id"] == "user123"
        assert data["username"] == "testuser"

    def test_utility_functions_with_error_response(self):
        """Test utility functions properly handle error responses."""
        error_response = {
            "success": False,
            "message": "Authentication failed",
            "error_code": "INVALID_TOKEN"
        }
        
        with pytest.raises(ValueError) as exc_info:
            ensure_success_response(error_response)
        
        error_str = str(exc_info.value)
        assert "Authentication failed" in error_str
        assert "INVALID_TOKEN" in error_str

    def test_utility_functions_with_missing_data(self):
        """Test utility functions handle missing data field."""
        response_without_data = {
            "success": True,
            "message": "Success but no data"
        }
        
        with pytest.raises(ValueError) as exc_info:
            extract_response_data(response_without_data)
        
        assert "missing data field" in str(exc_info.value)


class TestUserInfoModelWithParsedData:
    """Test UserInfo model creation with parsed datetime data."""

    def test_userinfo_creation_with_parsed_api_data(self):
        """Test UserInfo creation using data from validated API response."""
        # Simulate validated API response data
        api_data = {
            "id": "user123",
            "username": "testuser",
            "email": "test@example.com",
            "roles": ["user", "admin"],
            "mfa_enabled": True,
            "created_at": "2024-01-01T00:00:00Z",
            "last_login": "2024-01-01T12:00:00Z"
        }
        
        # Create UserInfo using our datetime parsing utility
        user_info = UserInfo(
            id=api_data["id"],
            username=api_data["username"],
            email=api_data["email"],
            roles=api_data["roles"],
            mfa_enabled=api_data["mfa_enabled"],
            created_at=parse_datetime(api_data.get("created_at"), datetime.now()),
            last_login=parse_datetime(api_data.get("last_login"))
        )
        
        assert user_info.id == "user123"
        assert user_info.username == "testuser" 
        assert user_info.email == "test@example.com"
        assert "user" in user_info.roles
        assert "admin" in user_info.roles
        assert user_info.mfa_enabled is True
        assert isinstance(user_info.created_at, datetime)
        assert isinstance(user_info.last_login, datetime)

    def test_userinfo_creation_with_missing_optional_fields(self):
        """Test UserInfo creation with missing optional datetime fields."""
        api_data = {
            "id": "user123",
            "username": "testuser", 
            "email": "test@example.com",
            "roles": ["user"],
            "mfa_enabled": False
            # Missing created_at and last_login
        }
        
        user_info = UserInfo(
            id=api_data["id"],
            username=api_data["username"],
            email=api_data["email"],
            roles=api_data["roles"],
            mfa_enabled=api_data["mfa_enabled"],
            created_at=parse_datetime(api_data.get("created_at"), datetime.now()),
            last_login=parse_datetime(api_data.get("last_login"))  # Will be None
        )
        
        assert user_info.id == "user123"
        assert isinstance(user_info.created_at, datetime)  # Should have default
        assert user_info.last_login is None  # Should be None


@pytest.mark.integration
class TestSchemaValidationInIntegration:
    """Test schema validation in integration scenarios."""

    def test_runtime_validation_in_development_mode(self):
        """Test that runtime validation works in development mode."""
        # Set development environment
        original_env = os.environ.get("ENVIRONMENT")
        os.environ["ENVIRONMENT"] = "dev"
        
        try:
            from authframework.models.api_responses import validate_api_response_in_dev
            
            # Create a test function with validation
            @validate_api_response_in_dev(TokenValidationResponse)
            async def mock_token_validate(token: str) -> Dict[str, Any]:
                # Return valid response
                return {
                    "success": True,
                    "data": {
                        "id": "user123",
                        "username": "testuser",
                        "roles": ["user"],
                        "mfa_enabled": False
                    }
                }
            
            # Should not raise in development with valid response
            import asyncio
            result = asyncio.run(mock_token_validate("test-token"))
            assert result["success"] is True
            
        finally:
            # Restore original environment
            if original_env is not None:
                os.environ["ENVIRONMENT"] = original_env
            else:
                os.environ.pop("ENVIRONMENT", None)

    def test_runtime_validation_catches_invalid_response(self):
        """Test that runtime validation catches invalid responses in dev mode."""
        # Set development environment  
        original_env = os.environ.get("ENVIRONMENT")
        os.environ["ENVIRONMENT"] = "dev"
        
        try:
            from authframework.models.api_responses import validate_api_response_in_dev
            import io
            import sys
            from contextlib import redirect_stdout
            
            # Create a test function with validation
            @validate_api_response_in_dev(TokenValidationResponse)
            async def mock_invalid_token_validate(token: str) -> Dict[str, Any]:
                # Return invalid response (missing required fields)
                return {
                    "valid": True,  # Wrong field name!
                    "user_id": "user123"  # Wrong field name!
                }
            
            # Capture stdout to check warning output
            captured_output = io.StringIO()
            
            with redirect_stdout(captured_output):
                import asyncio
                result = asyncio.run(mock_invalid_token_validate("test-token"))
            
            # Should still return the result (doesn't fail in dev)
            assert result["valid"] is True
            
            # But should have printed a warning
            output = captured_output.getvalue()
            assert "API Response Validation Error" in output
            
        finally:
            # Restore original environment
            if original_env is not None:
                os.environ["ENVIRONMENT"] = original_env
            else:
                os.environ.pop("ENVIRONMENT", None)