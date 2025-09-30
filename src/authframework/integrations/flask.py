"""Flask integration for AuthFramework."""

from __future__ import annotations

import functools
from datetime import datetime
from typing import Any, Callable, Optional

try:
    from flask import current_app, g, jsonify, request

    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

from ..client import AuthFrameworkClient
from ..exceptions import AuthFrameworkError
from ..models import UserInfo
from ..models.api_responses import (
    TokenValidationResponse,
    ensure_success_response,
    extract_response_data,
    parse_api_response,
)
from ..models.user_models import parse_datetime


class FlaskAuthUser:
    """Authenticated user information for Flask."""

    def __init__(self, user_info: UserInfo, token: str):
        self.user_info = user_info
        self.token = token
        self.id = user_info.id
        self.username = user_info.username
        self.email = user_info.email
        self.roles = user_info.roles
        self.mfa_enabled = user_info.mfa_enabled

    def has_role(self, role: str) -> bool:
        """Check if user has a specific role."""
        return role in self.roles

    def has_any_role(self, roles: list[str]) -> bool:
        """Check if user has any of the specified roles."""
        return any(role in self.roles for role in roles)


class AuthFrameworkFlask:
    """Flask integration for AuthFramework authentication."""

    def __init__(self, client: AuthFrameworkClient):
        if not FLASK_AVAILABLE:
            raise ImportError("Flask is not installed. Install it with: pip install flask")

        self.client = client

    def _get_token_from_request(self) -> Optional[str]:
        """Extract token from request headers."""
        if not FLASK_AVAILABLE:
            raise RuntimeError("Flask is not installed")
        
        # Import here to avoid issues when Flask is not available
        from flask import request as flask_request
        
        auth_header = flask_request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header[7:]  # Remove 'Bearer ' prefix
        return None

    async def _validate_token(self, token: str) -> FlaskAuthUser:
        """Validate token and return user information."""
        try:
            # Validate token using the tokens service
            validation_result = await self.client.tokens.validate(token)

            # Parse and validate the API response structure
            try:
                response = parse_api_response(validation_result, TokenValidationResponse)
                ensure_success_response(validation_result)
                user_data = extract_response_data(validation_result)
            except (ValueError, KeyError) as e:
                raise AuthFrameworkError(f"Invalid token validation response: {e}") from e

            # Get user information from the validated data
            user_id = user_data.get("id")
            if not user_id:
                raise AuthFrameworkError("Token does not contain user information")

            # Create user info object from the API response data
            user_info = UserInfo(
                id=user_id,
                username=user_data.get("username", ""),
                email=user_data.get("email", ""),  # May not be present in auth response
                roles=user_data.get("roles", []),
                mfa_enabled=user_data.get("mfa_enabled", False),  # May not be present
                created_at=parse_datetime(user_data.get("created_at"), datetime.now()),
                last_login=parse_datetime(user_data.get("last_login")),
            )

            return FlaskAuthUser(user_info, token)

        except AuthFrameworkError:
            raise

    def _handle_auth_error(self, message: str, status_code: int = 401):
        """Handle authentication errors."""
        if not FLASK_AVAILABLE:
            raise RuntimeError("Flask is not installed")
        
        # Import here to avoid issues when Flask is not available
        from flask import jsonify as flask_jsonify
        
        return flask_jsonify({"error": message}), status_code


def get_current_user() -> Optional[FlaskAuthUser]:
    """Get the current authenticated user from Flask's g object."""
    if not FLASK_AVAILABLE:
        raise RuntimeError("Flask is not installed")
    
    # Import here to avoid issues when Flask is not available
    from flask import g as flask_g
    
    return getattr(flask_g, "current_user", None)


# Add a single decorator‐factory to capture all common logic:
def _make_auth_decorator(
    auth_framework: AuthFrameworkFlask,
    *,
    post_check: Callable[[FlaskAuthUser], bool] | None = None,
    error_builder: Callable[[FlaskAuthUser | None], str] | None = None,
    error_status: int = 403,
) -> Callable[[Callable], Callable]:
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            token = auth_framework._get_token_from_request()
            if not token:
                return auth_framework._handle_auth_error("Authorization header missing")

            try:
                user = await auth_framework._validate_token(token)
                # Import here to avoid issues when Flask is not available
                from flask import g as flask_g
                flask_g.current_user = user
            except AuthFrameworkError as e:
                return auth_framework._handle_auth_error(f"Authentication failed: {e}")

            if post_check and not post_check(user):
                msg = error_builder(user) if error_builder else "Forbidden"
                return auth_framework._handle_auth_error(msg, error_status)

            return await f(*args, **kwargs)

        return wrapper

    return decorator


# Then simplify the four public decorators:


def auth_required(auth_framework: AuthFrameworkFlask):
    """Decorator to require authentication."""
    return _make_auth_decorator(auth_framework)


def role_required(auth_framework: AuthFrameworkFlask, role: str):
    """Decorator to require a specific role."""
    return _make_auth_decorator(
        auth_framework,
        post_check=lambda u: u.has_role(role),
        error_builder=lambda u: f"Role '{role}' required",
    )


def any_role_required(auth_framework: AuthFrameworkFlask, roles: list[str]):
    """Decorator to require any of the specified roles."""
    return _make_auth_decorator(
        auth_framework,
        post_check=lambda u: u.has_any_role(roles),
        error_builder=lambda u: "One of the following roles required: "
        + ", ".join(f"'{r}'" for r in roles),
    )


def permission_required(auth_framework: AuthFrameworkFlask, resource: str, action: str):
    """Decorator to require a specific permission."""

    # Placeholder: granular permission checks are not yet supported
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Permission checks for '{action}' on '{resource}' are not yet implemented."
            )

        return wrapper

    return decorator
