"""Integration tests for resume deletion, user isolation, cache-control,
and AI Mock Interview personalization synchronization.
"""

import io
import os
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

VALID_PDF_BYTES = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"


async def register_and_get_client(async_client: AsyncClient, email: str, name: str) -> dict:
    reg_payload = {
        "email": email,
        "password": "Password123!",
        "full_name": name,
    }
    reg_res = await async_client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    return dict(reg_res.cookies)


async def test_delete_one_resume_when_multiple_exist(async_client: AsyncClient):
    cookies = await register_and_get_client(async_client, "multiresume@test.com", "Multi Student")

    # 1. Upload 3 resumes
    uploaded_ids = []
    for i in range(1, 4):
        files = {"file": (f"resume_{i}.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}
        res = await async_client.post("/api/v1/resume/upload", files=files, cookies=cookies)
        assert res.status_code == 201
        uploaded_ids.append(res.json()["id"])

    # 2. Verify all 3 appear in retrieval API
    list_res = await async_client.get("/api/v1/resume/my-resumes", cookies=cookies)
    assert list_res.status_code == 200
    assert list_res.json()["total_count"] == 3
    retrieved_ids = [r["id"] for r in list_res.json()["resumes"]]
    assert set(retrieved_ids) == set(uploaded_ids)

    # 3. Delete Resume 2
    del_id = uploaded_ids[1]
    del_res = await async_client.delete(f"/api/v1/resume/{del_id}", cookies=cookies)
    assert del_res.status_code == 200
    assert del_res.json()["message"] == "Resume deleted successfully."

    # 4. Verify Resume 2 is permanently absent from retrieval API
    after_res = await async_client.get("/api/v1/resume/my-resumes", cookies=cookies)
    assert after_res.status_code == 200
    assert after_res.json()["total_count"] == 2
    remaining_ids = [r["id"] for r in after_res.json()["resumes"]]
    assert del_id not in remaining_ids
    assert uploaded_ids[0] in remaining_ids
    assert uploaded_ids[2] in remaining_ids

    # 5. Attempting to start interview with deleted resume must fail (404)
    bad_sess_res = await async_client.post(
        "/api/v1/interviews/sessions",
        json={
            "interview_type": "technical",
            "target_role": "Python Developer",
            "experience_level": "Beginner",
            "duration_minutes": 10,
            "custom_skills": ["Python"],
            "resume_id": del_id,
        },
        cookies=cookies,
    )
    assert bad_sess_res.status_code == 404
    assert "Selected resume not found" in bad_sess_res.json()["detail"]

    # 6. Starting interview with remaining active resume succeeds
    good_sess_res = await async_client.post(
        "/api/v1/interviews/sessions",
        json={
            "interview_type": "technical",
            "target_role": "Python Developer",
            "experience_level": "Beginner",
            "duration_minutes": 10,
            "custom_skills": ["Python"],
            "resume_id": uploaded_ids[0],
        },
        cookies=cookies,
    )
    assert good_sess_res.status_code == 201
    assert good_sess_res.json()["resume_id"] == uploaded_ids[0]


async def test_delete_all_resumes_fallback_to_generic(async_client: AsyncClient):
    cookies = await register_and_get_client(async_client, "delall@test.com", "Delete All Student")

    # Upload 2 resumes
    files1 = {"file": ("resume_alpha.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}
    res1 = await async_client.post("/api/v1/resume/upload", files=files1, cookies=cookies)
    r1_id = res1.json()["id"]

    files2 = {"file": ("resume_beta.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}
    res2 = await async_client.post("/api/v1/resume/upload", files=files2, cookies=cookies)
    r2_id = res2.json()["id"]

    # Delete both resumes
    await async_client.delete(f"/api/v1/resume/{r1_id}", cookies=cookies)
    await async_client.delete(f"/api/v1/resume/{r2_id}", cookies=cookies)

    # Retrieval API returns 0 resumes
    list_res = await async_client.get("/api/v1/resume/my-resumes", cookies=cookies)
    assert list_res.status_code == 200
    assert list_res.json()["total_count"] == 0
    assert list_res.json()["resumes"] == []

    # Start generic interview session with resume_id = None
    generic_res = await async_client.post(
        "/api/v1/interviews/sessions",
        json={
            "interview_type": "mixed",
            "target_role": "Full Stack Developer",
            "experience_level": "Beginner",
            "duration_minutes": 15,
            "custom_skills": ["React"],
            "resume_id": None,
        },
        cookies=cookies,
    )
    assert generic_res.status_code == 201
    assert generic_res.json()["resume_id"] is None
    assert generic_res.json()["total_questions"] >= 3


async def test_upload_new_resume_after_deletion(async_client: AsyncClient):
    cookies = await register_and_get_client(async_client, "reupload@test.com", "Reupload Student")

    # Upload and delete initial resume
    files_old = {"file": ("initial.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}
    r_old = await async_client.post("/api/v1/resume/upload", files=files_old, cookies=cookies)
    old_id = r_old.json()["id"]
    await async_client.delete(f"/api/v1/resume/{old_id}", cookies=cookies)

    # Confirm 0 resumes
    empty_list = await async_client.get("/api/v1/resume/my-resumes", cookies=cookies)
    assert empty_list.json()["total_count"] == 0

    # Upload brand new resume
    files_new = {"file": ("brand_new_resume.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}
    r_new = await async_client.post("/api/v1/resume/upload", files=files_new, cookies=cookies)
    assert r_new.status_code == 201
    new_id = r_new.json()["id"]

    # Retrieval API immediately shows newly uploaded resume
    new_list = await async_client.get("/api/v1/resume/my-resumes", cookies=cookies)
    assert new_list.json()["total_count"] == 1
    assert new_list.json()["resumes"][0]["id"] == new_id
    assert new_list.json()["resumes"][0]["original_filename"] == "brand_new_resume.pdf"

    # Personalized interview works with the new resume
    new_sess = await async_client.post(
        "/api/v1/interviews/sessions",
        json={
            "interview_type": "behavioral",
            "target_role": "Software Developer",
            "experience_level": "Intermediate",
            "duration_minutes": 10,
            "custom_skills": ["Leadership"],
            "resume_id": new_id,
        },
        cookies=cookies,
    )
    assert new_sess.status_code == 201
    assert new_sess.json()["resume_id"] == new_id


async def test_user_isolation_on_resume_deletion(async_client: AsyncClient):
    cookies_a = await register_and_get_client(async_client, "isolated_a@test.com", "User A")
    cookies_b = await register_and_get_client(async_client, "isolated_b@test.com", "User B")

    # User A uploads resume A
    files_a = {"file": ("user_a.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}
    res_a = await async_client.post("/api/v1/resume/upload", files=files_a, cookies=cookies_a)
    id_a = res_a.json()["id"]

    # User B uploads resume B
    files_b = {"file": ("user_b.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}
    res_b = await async_client.post("/api/v1/resume/upload", files=files_b, cookies=cookies_b)
    id_b = res_b.json()["id"]

    # User A cannot delete User B's resume
    hack_del = await async_client.delete(f"/api/v1/resume/{id_b}", cookies=cookies_a)
    assert hack_del.status_code == 404

    # User B's resume is untouched
    list_b = await async_client.get("/api/v1/resume/my-resumes", cookies=cookies_b)
    assert list_b.json()["total_count"] == 1
    assert list_b.json()["resumes"][0]["id"] == id_b

    # User A deletes their own resume A
    own_del = await async_client.delete(f"/api/v1/resume/{id_a}", cookies=cookies_a)
    assert own_del.status_code == 200

    # User A now has 0 resumes
    list_a = await async_client.get("/api/v1/resume/my-resumes", cookies=cookies_a)
    assert list_a.json()["total_count"] == 0

    # User B's account is completely unaffected
    list_b_after = await async_client.get("/api/v1/resume/my-resumes", cookies=cookies_b)
    assert list_b_after.json()["total_count"] == 1
    assert list_b_after.json()["resumes"][0]["id"] == id_b

    # User B can personalize interview with resume B
    sess_b = await async_client.post(
        "/api/v1/interviews/sessions",
        json={
            "interview_type": "technical",
            "target_role": "Python Developer",
            "experience_level": "Beginner",
            "duration_minutes": 10,
            "custom_skills": ["Python"],
            "resume_id": id_b,
        },
        cookies=cookies_b,
    )
    assert sess_b.status_code == 201


async def test_logout_and_login_deleted_resumes_do_not_reappear(async_client: AsyncClient):
    cookies = await register_and_get_client(async_client, "logouttest@test.com", "Logout Student")

    # Upload resume
    files = {"file": ("temp_resume.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}
    res = await async_client.post("/api/v1/resume/upload", files=files, cookies=cookies)
    resume_id = res.json()["id"]

    # Delete resume
    del_res = await async_client.delete(f"/api/v1/resume/{resume_id}", cookies=cookies)
    assert del_res.status_code == 200

    # Logout
    logout_res = await async_client.post("/api/v1/auth/logout", cookies=cookies)
    assert logout_res.status_code == 200

    # Log back in
    login_res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "logouttest@test.com", "password": "Password123!"},
    )
    assert login_res.status_code == 200
    new_cookies = dict(login_res.cookies)

    # Fetch resumes after re-login
    my_resumes = await async_client.get("/api/v1/resume/my-resumes", cookies=new_cookies)
    assert my_resumes.status_code == 200
    assert my_resumes.json()["total_count"] == 0
    assert my_resumes.json()["resumes"] == []

    # Latest analysis returns null
    latest_analysis = await async_client.get("/api/v1/resume/latest/analysis", cookies=new_cookies)
    assert latest_analysis.status_code == 200
    assert latest_analysis.json() is None


async def test_cache_control_headers_prevent_stale_data(async_client: AsyncClient):
    cookies = await register_and_get_client(async_client, "cachecheck@test.com", "Cache Student")

    # 1. Check get_my_resumes Cache-Control header
    list_res = await async_client.get("/api/v1/resume/my-resumes", cookies=cookies)
    assert "no-store" in list_res.headers.get("Cache-Control", "")
    assert "no-cache" in list_res.headers.get("Cache-Control", "")

    # 2. Check upload Cache-Control header
    files = {"file": ("test_cache.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}
    up_res = await async_client.post("/api/v1/resume/upload", files=files, cookies=cookies)
    assert "no-store" in up_res.headers.get("Cache-Control", "")
    r_id = up_res.json()["id"]

    # 3. Check delete Cache-Control header
    del_res = await async_client.delete(f"/api/v1/resume/{r_id}", cookies=cookies)
    assert "no-store" in del_res.headers.get("Cache-Control", "")
