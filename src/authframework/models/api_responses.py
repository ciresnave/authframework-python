"""Strongly-typed API response models for runtime validation.

Copyright (c) 2025 AuthFramework. All rights reserved.
"""

import os
from datetime import datetime
from functools import wraps
from typing import Any, Dict, Generic, Optional, TypeVar, Union, Callable, Type

from pydantic import BaseModel, Field, ValidationError, ConfigDict


T = TypeVar("T")
ResponseModelType = TypeVar("ResponseModelType", bound=BaseModel)


class ApiResponse(BaseModel, Generic[T]):
    """Base API response wrapper that enforces correct field structure."""

    success: bool = Field(..., description="Whether the request was successful")
    data: Optional[T] = None
    message: Optional[str] = None
    error_code: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class TokenValidationData(BaseModel):
    """Token validation response data structure - matches exact API format."""

    id: str = Field(..., description="User ID (not user_id!)")
    username: str
    email: Optional[str] = None
    roles: list[str] = Field(default_factory=list, description="User roles (not scopes!)")
    mfa_enabled: bool = False
    created_at: Optional[str] = None  # ISO string from API
    last_login: Optional[str] = None  # ISO string from API
    token_type: Optional[str] = "bearer"
    expires_at: Optional[str] = None

    class Config:
        """Pydantic configuration."""

        extra = "forbid"  # Catch unexpected fields


class HealthCheckData(BaseModel):
    """Health check response data structure."""

    status: str
    version: Optional[str] = None
    uptime: Optional[int] = None
    timestamp: Optional[str] = None

    class Config:
        """Pydantic configuration."""

        extra = "allow"  # Health checks may have additional fields


class LoginData(BaseModel):
    """Login response data structure."""

    token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[str] = None
    user: Optional[Dict[str, Any]] = None

    class Config:
        """Pydantic configuration."""

        extra = "forbid"


# Specific response types with required data fields
class TokenValidationResponse(BaseModel):
    """Token validation API response with required data field."""

    success: bool = Field(..., description="Whether the request was successful")
    data: TokenValidationData = Field(..., description="Required user token data")
    message: Optional[str] = None
    error_code: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


# Specific response types
class HealthCheckResponse(BaseModel):
    """Health check API response with required data field."""

    success: bool = Field(..., description="Whether the request was successful")
    data: HealthCheckData = Field(..., description="Required health check data")
    message: Optional[str] = None
    error_code: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


# Type aliases for other responses
LoginResponse = ApiResponse[LoginData]


def validate_api_response_in_dev(response_model: type[BaseModel]) -> Callable:
    """Decorator to validate API responses in development/test environments.

    Args:
        response_model: The Pydantic model to validate against

    Returns:
        Decorator function that validates responses in dev/test mode
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            result = await func(*args, **kwargs)

            # Only validate in development/test environments
            if os.getenv("ENVIRONMENT", "").lower() in ("dev", "development", "test"):
                try:
                    response_model.model_validate(result)
                except ValidationError as e:
                    print(f"⚠️  API Response Validation Error in {func.__name__}:")
                    print(f"   Expected: {response_model.__name__}")
                    print(f"   Errors: {e}")
                    print(f"   Response: {result}")
                    # Don't fail in dev, just warn loudly

            return result

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            # Only validate in development/test environments
            if os.getenv("ENVIRONMENT", "").lower() in ("dev", "development", "test"):
                try:
                    response_model.model_validate(result)
                except ValidationError as e:
                    print(f"⚠️  API Response Validation Error in {func.__name__}:")
                    print(f"   Expected: {response_model.__name__}")
                    print(f"   Errors: {e}")
                    print(f"   Response: {result}")
                    # Don't fail in dev, just warn loudly

            return result

        # Return the appropriate wrapper based on whether the function is async
        import inspect

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def parse_api_response(response_data: Dict[str, Any], response_model: Type[ResponseModelType]) -> ResponseModelType:
    """Parse and validate API response data.

    Args:
        response_data: Raw response data from API
        response_model: Pydantic model to parse into

    Returns:
        Validated response model instance

    Raises:
        ValidationError: If response doesn't match expected schema
    """
    # Let Pydantic validation errors bubble up directly
    # This preserves all the detailed error information
    return response_model.model_validate(response_data)


# Validation utilities for common patterns
def ensure_success_response(response: Dict[str, Any]) -> None:
    """Ensure response has success=True, raise descriptive error if not."""
    if not response.get("success", False):
        error_msg = response.get("message", "Unknown error")
        error_code = response.get("error_code", "UNKNOWN")
        raise ValueError(f"API request failed: {error_msg} (code: {error_code})")


def extract_response_data(response: Dict[str, Any]) -> Dict[str, Any]:
    """Safely extract data field from API response."""
    ensure_success_response(response)
    data = response.get("data")
    if data is None:
        raise ValueError("API response missing data field")
    return data
