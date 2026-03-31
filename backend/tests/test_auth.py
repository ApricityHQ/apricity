"""
Unit tests for auth.py.

No real Clerk credentials required. Tests verify that verify_clerk_token
raises the correct HTTPException when JWKS is not configured.
"""
import os
import sys

import pytest
from fastapi import HTTPException

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_verify_clerk_token_raises_500_when_jwks_not_configured(monkeypatch):
    """
    verify_clerk_token raises HTTPException 500 when jwk_client is None.

    This covers the case where CLERK_JWKS_URL is missing from the environment,
    which leaves jwk_client uninitialized. Callers should receive a clear 500
    rather than an unhandled AttributeError.

    Args:
        monkeypatch: pytest fixture to patch module-level state.
    """
    import auth
    monkeypatch.setattr(auth, "jwk_client", None)

    with pytest.raises(HTTPException) as exc_info:
        auth.verify_clerk_token("any.token.here")

    assert exc_info.value.status_code == 500
    assert "CLERK_JWKS_URL" in exc_info.value.detail
