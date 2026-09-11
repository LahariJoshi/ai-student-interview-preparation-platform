import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_register_student(async_client: AsyncClient):
    payload = {
        "email": "student@example.com",
        "password": "securepassword123",
        "full_name": "Test Student"
    }
    response = await async_client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "student@example.com"
    assert data["full_name"] == "Test Student"
    assert data["role"] == "student"
    assert "access_token" in response.cookies


async def test_login_student(async_client: AsyncClient):
    # Register user first
    reg_payload = {
        "email": "student2@example.com",
        "password": "password123",
        "full_name": "Second Student"
    }
    await async_client.post("/api/v1/auth/register", json=reg_payload)

    # Login
    login_payload = {
        "email": "student2@example.com",
        "password": "password123"
    }
    response = await async_client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    assert "access_token" in response.cookies


async def test_get_current_user_me(async_client: AsyncClient):
    reg_payload = {
        "email": "me@example.com",
        "password": "password123",
        "full_name": "Me Student"
    }
    # Registration automatically logs in and sets cookie
    reg_res = await async_client.post("/api/v1/auth/register", json=reg_payload)

    # Fetch me endpoint using the set cookie
    me_res = await async_client.get("/api/v1/auth/me", cookies=reg_res.cookies)
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["email"] == "me@example.com"


async def test_get_and_update_profile(async_client: AsyncClient):
    reg_payload = {
        "email": "profile@example.com",
        "password": "password123",
        "full_name": "Profile Student"
    }
    reg_res = await async_client.post("/api/v1/auth/register", json=reg_payload)
    cookies = reg_res.cookies

    # GET Profile
    prof_res = await async_client.get("/api/v1/profile", cookies=cookies)
    assert prof_res.status_code == 200
    prof_data = prof_res.json()
    assert prof_data["target_role"] is None

    # UPDATE Profile
    update_payload = {
        "target_role": "Full Stack Software Engineer",
        "experience_level": "Entry Level",
        "tech_skills": ["Python", "TypeScript", "React", "FastAPI", "PostgreSQL"],
        "github_url": "https://github.com/student",
        "linkedin_url": "https://linkedin.com/in/student"
    }
    put_res = await async_client.put("/api/v1/profile", json=update_payload, cookies=cookies)
    assert put_res.status_code == 200
    updated_data = put_res.json()
    assert updated_data["target_role"] == "Full Stack Software Engineer"
    assert "Python" in updated_data["tech_skills"]


async def test_logout_student(async_client: AsyncClient):
    reg_payload = {
        "email": "logout@example.com",
        "password": "password123",
        "full_name": "Logout Student"
    }
    reg_res = await async_client.post("/api/v1/auth/register", json=reg_payload)
    
    logout_res = await async_client.post("/api/v1/auth/logout")
    assert logout_res.status_code == 200
    assert logout_res.json()["message"] == "Logged out successfully"
