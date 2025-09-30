"""AuthFramework models package.

Copyright (c) 2025 AuthFramework. All rights reserved.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from .admin_models import CreatePermissionRequest, CreateRoleRequest, Permission, Role, SystemStats
from .api_responses import (
    ApiResponse,
    HealthCheckData,
    HealthCheckResponse,
    LoginData,
    TokenValidationData,
    TokenValidationResponse,
    ensure_success_response,
    extract_response_data,
    parse_api_response,
    validate_api_response_in_dev,
)

# Import from domain-specific model files
from .health_models import (
    DetailedHealthStatus,
    HealthMetrics,
    HealthStatus,
    LivenessCheck,
    ReadinessCheck,
    ServiceHealth,
)
from .mfa_models import DisableMFARequest, MFASetupResponse, MFAVerifyRequest, MFAVerifyResponse
from .oauth_models import (
    IntrospectTokenRequest,
    OAuthAuthorizeParams,
    OAuthTokenRequest,
    OAuthTokenResponse,
    RevokeTokenRequest,
    TokenIntrospectionResponse,
)
from .rate_limit_models import RateLimitConfig, RateLimitStats
from .token_models import (
    CreateTokenRequest,
    CreateTokenResponse,
    RefreshTokenRequest,
    TokenInfo,
    TokenResponse,
    TokenValidationResponse,
)
from .user_models import (
    ChangePasswordRequest,
    CreateUserRequest,
    LoginResponse,
    UpdateProfileRequest,
    UserInfo,
    UserProfile,
    parse_datetime,
)


# Base models that don't fit into domain-specific categories
class RequestOptions(BaseModel):
    """Request options model."""

    timeout: float | None = None
    retries: int | None = None
    headers: dict[str, str] | None = None

    class Config:
        """Pydantic configuration."""

        extra = "allow"


class ListOptions(BaseModel):
    """List options model."""

    page: int | None = 1
    limit: int | None = 20
    search: str | None = None
    sort: str | None = None
    order: str | None = None


class UserListOptions(ListOptions):
    """User list options model."""

    role: str | None = None


# Re-export all models for backward compatibility
__all__ = [
    # Health models
    "HealthStatus",
    "ServiceHealth",
    "DetailedHealthStatus",
    "HealthMetrics",
    "ReadinessCheck",
    "LivenessCheck",
    # Token models
    "TokenValidationResponse",
    "CreateTokenRequest",
    "CreateTokenResponse",
    "TokenInfo",
    "RefreshTokenRequest",
    "TokenResponse",
    # Rate limit models
    "RateLimitConfig",
    "RateLimitStats",
    # Admin models
    "Permission",
    "Role",
    "CreatePermissionRequest",
    "CreateRoleRequest",
    "SystemStats",
    # User models
    "UserInfo",
    "UserProfile",
    "UpdateProfileRequest",
    "ChangePasswordRequest",
    "CreateUserRequest",
    "LoginResponse",
    "parse_datetime",
    # API Response models
    "ApiResponse",
    "TokenValidationData",
    "TokenValidationResponse",
    "HealthCheckData",
    "HealthCheckResponse",
    "LoginData",
    "validate_api_response_in_dev",
    "parse_api_response",
    "ensure_success_response",
    "extract_response_data",
    # OAuth models
    "OAuthTokenRequest",
    "OAuthTokenResponse",
    "RevokeTokenRequest",
    "IntrospectTokenRequest",
    "TokenIntrospectionResponse",
    "OAuthAuthorizeParams",
    # MFA models
    "MFASetupResponse",
    "MFAVerifyRequest",
    "MFAVerifyResponse",
    "DisableMFARequest",
    # Base models
    "RequestOptions",
    "ListOptions",
    "UserListOptions",
]
