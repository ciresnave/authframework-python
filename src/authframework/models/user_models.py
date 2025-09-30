"""User management models for AuthFramework.

Copyright (c) 2025 AuthFramework. All rights reserved.
"""

from datetime import datetime
from typing import overload

from pydantic import BaseModel


@overload
def parse_datetime(value: str | datetime | None, default: datetime) -> datetime:
    ...


@overload
def parse_datetime(value: str | datetime | None, default: None = None) -> datetime | None:
    ...


def parse_datetime(
    value: str | datetime | None, default: datetime | None = None
) -> datetime | None:
    """Parse datetime from string, datetime object, or None.

    Args:
        value: The value to parse (string, datetime, or None)
        default: Default value to return if value is None

    Returns:
        Parsed datetime object or default value (timezone-naive)

    Raises:
        ValueError: If string value cannot be parsed
    """
    if value is None:
        return default
    if isinstance(value, datetime):
        # Return timezone-naive datetime
        return value.replace(tzinfo=None) if value.tzinfo else value
    if isinstance(value, str):
        try:
            # Handle ISO format with or without 'Z' suffix
            string_value = value  # Ensure type checker knows this is a string
            if string_value.endswith("Z"):
                string_value = string_value[:-1] + "+00:00"
            dt = datetime.fromisoformat(string_value)
            # Return timezone-naive datetime for consistency
            return dt.replace(tzinfo=None) if dt.tzinfo else dt
        except ValueError as e:
            raise ValueError(f"Cannot parse datetime from {type(value)}: {value}") from e
    raise ValueError(f"Cannot parse datetime from {type(value)}: {value}")


class UserInfo(BaseModel):
    """User information model."""

    id: str
    username: str
    email: str
    roles: list[str]
    mfa_enabled: bool
    created_at: datetime
    last_login: datetime | None = None


class UserProfile(BaseModel):
    """User profile model."""

    id: str
    user_id: str  # Alias for id for backwards compatibility
    username: str
    email: str
    display_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    timezone: str | None = None
    locale: str | None = None
    mfa_enabled: bool
    created_at: datetime
    updated_at: datetime


class UpdateProfileRequest(BaseModel):
    """Update profile request model."""

    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    timezone: str | None = None
    locale: str | None = None


class ChangePasswordRequest(BaseModel):
    """Change password request model."""

    current_password: str
    new_password: str


class CreateUserRequest(BaseModel):
    """Create user request model."""

    username: str
    email: str
    password: str
    roles: list[str] | None = None
    first_name: str | None = None
    last_name: str | None = None


class LoginResponse(BaseModel):
    """Login response model."""

    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user: UserInfo
