import os
import pytest
import io
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

# Valid PDF header: %PDF-1.4
VALID_PDF_BYTES = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
# Valid DOCX header: PK\x03\x04
VALID_DOCX_BYTES = b"PK\x03\x04\x14\x00\x06\x00\x08\x00\x00\x00\x00\x00"


async def get_auth_cookies(async_client: AsyncClient, email: str = "resumestudent@example.com"):
    reg_payload = {
        "email": email,
        "password": "password123",
        "full_name": "Resume Student"
    }
    reg_res = await async_client.post("/api/v1/auth/register", json=reg_payload)
    return reg_res.cookies


async def test_upload_valid_pdf(async_client: AsyncClient):
    cookies = await get_auth_cookies(async_client, "pdf_user@example.com")
    files = {"file": ("my_resume.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}

    response = await async_client.post("/api/v1/resume/upload", files=files, cookies=cookies)
    assert response.status_code == 201
    data = response.json()
    assert data["original_filename"] == "my_resume.pdf"
    assert data["mime_type"] == "application/pdf"
    assert data["file_size"] == len(VALID_PDF_BYTES)


async def test_upload_valid_docx(async_client: AsyncClient):
    cookies = await get_auth_cookies(async_client, "docx_user@example.com")
    files = {"file": ("my_resume.docx", io.BytesIO(VALID_DOCX_BYTES), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}

    response = await async_client.post("/api/v1/resume/upload", files=files, cookies=cookies)
    assert response.status_code == 201
    data = response.json()
    assert data["original_filename"] == "my_resume.docx"
    assert "wordprocessingml" in data["mime_type"]


async def test_upload_unauthenticated(async_client: AsyncClient):
    files = {"file": ("resume.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}
    response = await async_client.post("/api/v1/resume/upload", files=files)
    assert response.status_code == 401


async def test_upload_file_exceeds_5mb(async_client: AsyncClient):
    cookies = await get_auth_cookies(async_client, "large_user@example.com")
    # Generate 5.1 MB fake PDF stream starting with %PDF
    large_bytes = VALID_PDF_BYTES + (b"A" * (5 * 1024 * 1024 + 100))
    files = {"file": ("large_resume.pdf", io.BytesIO(large_bytes), "application/pdf")}

    response = await async_client.post("/api/v1/resume/upload", files=files, cookies=cookies)
    assert response.status_code == 400
    assert "exceeds maximum allowed limit" in response.json()["detail"]


async def test_upload_invalid_extension(async_client: AsyncClient):
    cookies = await get_auth_cookies(async_client, "bad_ext@example.com")
    files = {"file": ("script.py", io.BytesIO(b"print('hello')"), "text/x-python")}

    response = await async_client.post("/api/v1/resume/upload", files=files, cookies=cookies)
    assert response.status_code == 400
    assert "Only PDF" in response.json()["detail"]


async def test_upload_invalid_magic_bytes(async_client: AsyncClient):
    cookies = await get_auth_cookies(async_client, "bad_magic@example.com")
    # File named .pdf but containing plain text
    files = {"file": ("fake_resume.pdf", io.BytesIO(b"This is not a real PDF file header"), "application/pdf")}

    response = await async_client.post("/api/v1/resume/upload", files=files, cookies=cookies)
    assert response.status_code == 400
    assert "signature mismatch" in response.json()["detail"]


async def test_max_resumes_limit(async_client: AsyncClient):
    cookies = await get_auth_cookies(async_client, "limit_user@example.com")

    # Upload 5 valid resumes
    for i in range(5):
        files = {"file": (f"resume_{i}.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}
        res = await async_client.post("/api/v1/resume/upload", files=files, cookies=cookies)
        assert res.status_code == 201

    # 6th upload attempt must fail
    files_extra = {"file": ("resume_6.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}
    res_extra = await async_client.post("/api/v1/resume/upload", files=files_extra, cookies=cookies)
    assert res_extra.status_code == 400
    assert "Maximum limit" in res_extra.json()["detail"]


async def test_get_and_delete_resume(async_client: AsyncClient):
    cookies = await get_auth_cookies(async_client, "owner_user@example.com")
    files = {"file": ("to_delete.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}

    upload_res = await async_client.post("/api/v1/resume/upload", files=files, cookies=cookies)
    assert upload_res.status_code == 201
    resume_id = upload_res.json()["id"]

    # Verify resume exists in list
    list_res = await async_client.get("/api/v1/resume/my-resumes", cookies=cookies)
    assert list_res.status_code == 200
    assert list_res.json()["total_count"] == 1

    # Delete resume
    del_res = await async_client.delete(f"/api/v1/resume/{resume_id}", cookies=cookies)
    assert del_res.status_code == 200
    assert del_res.json()["message"] == "Resume deleted successfully."

    # Verify list is empty
    list_after = await async_client.get("/api/v1/resume/my-resumes", cookies=cookies)
    assert list_after.json()["total_count"] == 0


async def test_user_isolation(async_client: AsyncClient):
    cookies_a = await get_auth_cookies(async_client, "user_a@example.com")
    cookies_b = await get_auth_cookies(async_client, "user_b@example.com")

    # User A uploads resume
    files = {"file": ("user_a_resume.pdf", io.BytesIO(VALID_PDF_BYTES), "application/pdf")}
    upload_res = await async_client.post("/api/v1/resume/upload", files=files, cookies=cookies_a)
    resume_id = upload_res.json()["id"]

    # User B attempts to delete User A's resume
    del_res = await async_client.delete(f"/api/v1/resume/{resume_id}", cookies=cookies_b)
    assert del_res.status_code == 404
