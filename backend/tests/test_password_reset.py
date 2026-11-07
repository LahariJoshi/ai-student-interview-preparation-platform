import hashlib
import secrets
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock
import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.core.config import settings
from app.db.models.user import User
from app.db.models.password_reset import PasswordResetToken

pytestmark = pytest.mark.asyncio


async def test_recovery_status_endpoint(async_client: AsyncClient):
    response = await async_client.get("/api/v1/auth/recovery-status")
    assert response.status_code == 200
    data = response.json()
    assert "smtp_configured" in data
    assert "environment" in data
    assert "dev_recovery_available" in data
    assert data["dev_recovery_available"] is True


async def test_forgot_password_unconfigured_smtp(async_client: AsyncClient):
    with patch("app.modules.auth.router.is_email_configured", return_value=False):
        response = await async_client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "student@college.edu"},
        )
        assert response.status_code == 503
        assert "Email delivery" in response.json()["detail"]


async def test_forgot_password_success_and_reset_flow(async_client: AsyncClient, db_session):
    # 1. Register a student user
    email = f"reset_test_{secrets.token_hex(4)}@college.edu"
    initial_password = "originalPassword123"
    reg_response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": initial_password,
            "full_name": "Reset Test Student",
        },
    )
    assert reg_response.status_code == 201

    # 2. Mock SMTP and request password reset
    with patch("app.modules.auth.router.is_email_configured", return_value=True), \
         patch("app.modules.auth.router.send_password_reset_email") as mock_send_email:
        mock_send_email.return_value = None

        reset_req = await async_client.post(
            "/api/v1/auth/forgot-password",
            json={"email": email},
        )
        assert reset_req.status_code == 200
        assert "password reset link has been sent" in reset_req.json()["message"]
        assert mock_send_email.called
        call_args = mock_send_email.call_args[1]
        assert call_args["to_email"] == email
        reset_link = call_args["reset_link"]
        assert "/reset-password?token=" in reset_link
        raw_token = reset_link.split("token=")[1]

    # 3. Verify token endpoint
    verify_res = await async_client.get(f"/api/v1/auth/verify-reset-token?token={raw_token}")
    assert verify_res.status_code == 200
    assert verify_res.json()["valid"] is True

    # 4. Verify invalid token returns 400
    invalid_verify = await async_client.get("/api/v1/auth/verify-reset-token?token=invalid_random_token_12345")
    assert invalid_verify.status_code == 400

    # 5. Complete password reset with new password
    new_password = "brandNewSecurePassword456"
    complete_res = await async_client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": raw_token,
            "new_password": new_password,
        },
    )
    assert complete_res.status_code == 200
    assert "Password successfully reset" in complete_res.json()["message"]

    # 6. Verify old password no longer works
    old_login = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": initial_password},
    )
    assert old_login.status_code == 401

    # 7. Verify new password successfully logs in
    new_login = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": new_password},
    )
    assert new_login.status_code == 200
    assert new_login.json()["email"] == email

    # 8. Verify the used token cannot be reused
    reused_res = await async_client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": raw_token,
            "new_password": "anotherPassword789",
        },
    )
    assert reused_res.status_code == 400
    assert "already been used" in reused_res.json()["detail"]


async def test_reset_expired_token(async_client: AsyncClient, db_session):
    email = f"expired_test_{secrets.token_hex(4)}@college.edu"
    reg_response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "somePassword123",
            "full_name": "Expired Test User",
        },
    )
    assert reg_response.status_code == 201

    # Insert an already-expired token directly
    user_res = await db_session.execute(select(User).where(User.email == email))
    user = user_res.scalar_one()

    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    expired_token = PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=10),
        used=False,
    )
    db_session.add(expired_token)
    await db_session.commit()

    # Try verifying expired token
    verify_res = await async_client.get(f"/api/v1/auth/verify-reset-token?token={raw_token}")
    assert verify_res.status_code == 400
    assert "expired" in verify_res.json()["detail"]

    # Try resetting with expired token
    reset_res = await async_client.post(
        "/api/v1/auth/reset-password",
        json={"token": raw_token, "new_password": "newPassword123"},
    )
    assert reset_res.status_code == 400
    assert "expired" in reset_res.json()["detail"]


async def test_dev_reset_password_success(async_client: AsyncClient):
    # Register student
    email = f"dev_success_{secrets.token_hex(4)}@college.edu"
    full_name = "Alice Student"
    initial_password = "initialPassword123"

    reg_res = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": initial_password,
            "full_name": full_name,
        },
    )
    assert reg_res.status_code == 201

    # Execute Dev Reset with correct full name and dev recovery key
    new_password = "updatedDevPassword456"
    dev_res = await async_client.post(
        "/api/v1/auth/dev-reset-password",
        json={
            "email": email,
            "full_name": "alice student",  # case-insensitive check
            "dev_recovery_key": settings.DEV_RECOVERY_KEY,
            "new_password": new_password,
        },
    )
    assert dev_res.status_code == 200
    assert "Password successfully updated" in dev_res.json()["message"]

    # Verify old password is now invalid
    old_login = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": initial_password},
    )
    assert old_login.status_code == 401

    # Verify new password successfully logs in
    new_login = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": new_password},
    )
    assert new_login.status_code == 200
    assert new_login.json()["email"] == email


async def test_dev_reset_identity_verification_failure(async_client: AsyncClient):
    # Register student
    email = f"dev_identity_{secrets.token_hex(4)}@college.edu"
    full_name = "Real Account Holder"
    initial_password = "originalPassword123"

    reg_res = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": initial_password,
            "full_name": full_name,
        },
    )
    assert reg_res.status_code == 201

    # Attempt reset with WRONG name (attacker does not know registered name)
    wrong_name_res = await async_client.post(
        "/api/v1/auth/dev-reset-password",
        json={
            "email": email,
            "full_name": "Attacker Unknown",
            "dev_recovery_key": settings.DEV_RECOVERY_KEY,
            "new_password": "attackerPassword456",
        },
    )
    assert wrong_name_res.status_code == 401
    assert "Identity verification failed" in wrong_name_res.json()["detail"]

    # Verify the real account holder's password remains unchanged
    still_valid_login = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": initial_password},
    )
    assert still_valid_login.status_code == 200


async def test_dev_reset_invalid_key(async_client: AsyncClient):
    res = await async_client.post(
        "/api/v1/auth/dev-reset-password",
        json={
            "email": "test@college.edu",
            "full_name": "Test Student",
            "dev_recovery_key": "wrong_key_12345",
            "new_password": "someNewPassword123",
        },
    )
    assert res.status_code == 401
    assert "Invalid development recovery authorization key" in res.json()["detail"]


async def test_dev_reset_forbidden_in_production(async_client: AsyncClient):
    original_env = settings.ENVIRONMENT
    try:
        settings.ENVIRONMENT = "production"
        res = await async_client.post(
            "/api/v1/auth/dev-reset-password",
            json={
                "email": "test@college.edu",
                "full_name": "Test Student",
                "dev_recovery_key": settings.DEV_RECOVERY_KEY,
                "new_password": "someNewPassword123",
            },
        )
        assert res.status_code == 403
        assert "strictly forbidden" in res.json()["detail"]
    finally:
        settings.ENVIRONMENT = original_env


async def test_authenticated_change_password(async_client: AsyncClient):
    email = f"change_pwd_{secrets.token_hex(4)}@college.edu"
    initial_password = "myOldPassword123"

    reg_res = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": initial_password,
            "full_name": "Change Password Student",
        },
    )
    assert reg_res.status_code == 201

    # 1. Change password with incorrect current password -> 400
    fail_res = await async_client.post(
        "/api/v1/auth/change-password",
        json={
            "current_password": "incorrectOldPassword",
            "new_password": "brandNewPassword456",
        },
        cookies=reg_res.cookies,
    )
    assert fail_res.status_code == 400
    assert "Incorrect current password" in fail_res.json()["detail"]

    # 2. Change password with correct current password -> 200
    new_password = "brandNewPassword456"
    success_res = await async_client.post(
        "/api/v1/auth/change-password",
        json={
            "current_password": initial_password,
            "new_password": new_password,
        },
        cookies=reg_res.cookies,
    )
    assert success_res.status_code == 200
    assert "changed successfully" in success_res.json()["message"]

    # 3. Verify old password no longer logs in
    old_login = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": initial_password},
    )
    assert old_login.status_code == 401

    # 4. Verify new password successfully logs in
    new_login = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": new_password},
    )
    assert new_login.status_code == 200
    assert new_login.json()["email"] == email
