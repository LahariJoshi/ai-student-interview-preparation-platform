import os
import uuid
import re
from pathlib import Path
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.db.models.user import User
from app.db.models.resume import Resume
from app.modules.resume.schemas import (
    ResumeOut,
    ResumeListOut,
    ResumeTextOut,
    MessageResponse,
)

from app.modules.resume.services.pdf_extractor import extract_text_from_pdf
from app.modules.resume.services.docx_extractor import extract_text_from_docx

router = APIRouter(prefix="/resume", tags=["Resume"])

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_RESUMES_PER_USER = 5

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/octet-stream",  # Browser fallback check validated by magic bytes
}

PDF_MAGIC_BYTES = b"%PDF"
DOCX_MAGIC_BYTES = b"PK\x03\x04"


def sanitize_filename(filename: str) -> str:
    # Extract only the base name (prevents path traversal)
    clean_name = Path(filename).name
    # Remove any non-printable or null characters
    clean_name = re.sub(r'[\x00-\x1f\x7f]', '', clean_name)
    # Replace whitespace and unsafe characters with underscores
    clean_name = re.sub(r'[^\w\.-]', '_', clean_name)
    return clean_name or "uploaded_resume.pdf"


@router.post("/upload", response_model=ResumeOut, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 1. Enforce max 5 resumes per student limit
    count_query = select(func.count(Resume.id)).where(Resume.user_id == current_user.id)
    count_result = await db.execute(count_query)
    user_resume_count = count_result.scalar_one()

    if user_resume_count >= MAX_RESUMES_PER_USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum limit of {MAX_RESUMES_PER_USER} uploaded resumes reached. Delete an existing resume to upload a new one."
        )

    # 2. Path Traversal & Filename check
    if not file.filename or ".." in file.filename or "/" in file.filename or "\\" in file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or malicious filename provided."
        )

    sanitized_original = sanitize_filename(file.filename)
    file_ext = Path(sanitized_original).suffix.lower()

    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF (.pdf) and DOCX (.docx) files are supported."
        )

    # 3. Read header bytes for magic byte validation & size check
    header_bytes = await file.read(1024)
    if not header_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty."
        )

    # Validate Magic Bytes
    is_pdf = header_bytes.startswith(PDF_MAGIC_BYTES)
    is_docx = header_bytes.startswith(DOCX_MAGIC_BYTES)

    if file_ext == ".pdf" and not is_pdf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File content signature mismatch. Expected valid PDF document."
        )
    elif file_ext == ".docx" and not is_docx:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File content signature mismatch. Expected valid DOCX document."
        )

    # Reset stream position & compute total file size safely
    await file.seek(0)

    # Read in chunks to enforce 5 MB limit without consuming unlimited RAM
    chunk_size = 1024 * 1024  # 1 MB chunk
    total_size = 0
    file_content = bytearray()

    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        total_size += len(chunk)
        if total_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds maximum allowed limit of 5 MB."
            )
        file_content.extend(chunk)

    # Determine stored MIME type
    determined_mime = "application/pdf" if file_ext == ".pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    # 4. Generate unique stored filename & ensure user directory exists
    resume_uuid = uuid.uuid4()
    stored_filename = f"{resume_uuid.hex[:8]}_{sanitized_original}"
    user_upload_dir = os.path.join(settings.UPLOADS_DIR, str(current_user.id))
    os.makedirs(user_upload_dir, exist_ok=True)

    full_file_path = os.path.join(user_upload_dir, stored_filename)

    # 5. Write to physical disk
    with open(full_file_path, "wb") as f:
        f.write(file_content)

    # 6. Save Resume ORM record in Database
    new_resume = Resume(
        id=resume_uuid,
        user_id=current_user.id,
        original_filename=sanitized_original,
        stored_filename=stored_filename,
        file_path=full_file_path,
        file_size=total_size,
        mime_type=determined_mime,
    )
    db.add(new_resume)
    await db.commit()
    await db.refresh(new_resume)

    return new_resume


@router.get("/my-resumes", response_model=ResumeListOut)
async def get_my_resumes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Resume)
        .where(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
    )
    resumes = result.scalars().all()
    return {
        "resumes": resumes,
        "total_count": len(resumes)
    }


@router.delete("/{resume_id}", response_model=MessageResponse)
async def delete_resume(
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id)
    )
    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found or access unauthorized."
        )

    # Remove physical file from disk if present
    if os.path.exists(resume.file_path):
        try:
            os.remove(resume.file_path)
        except OSError:
            pass  # File system removal warning logged gracefully

    # Delete database record
    await db.delete(resume)
    await db.commit()

    return {"message": "Resume deleted successfully."}

@router.post("/{resume_id}/extract-text", response_model=ResumeTextOut)
async def extract_resume_text(
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # 1. Find the resume and verify ownership
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == current_user.id,
        )
    )
    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found or access unauthorized.",
        )

    # 2. Check that the physical file still exists
    if not os.path.exists(resume.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume file not found on the server.",
        )

    try:
        # 3. Select the correct extractor
        if resume.mime_type == "application/pdf":
            extracted_text = extract_text_from_pdf(resume.file_path)

        elif resume.mime_type == (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            extracted_text = extract_text_from_docx(resume.file_path)

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported resume file type.",
            )

        # 4. Check whether any meaningful text was extracted
        if not extracted_text.strip():
            resume.extraction_status = "failed_empty"
            resume.raw_text = None
            resume.character_count = 0
            resume.word_count = 0
            await db.commit()

            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "No readable text could be extracted from this resume. "
                    "The file may be empty or image-based."
                ),
            )

        # 5. Save extracted text and statistics
        resume.raw_text = extracted_text
        resume.character_count = len(extracted_text)
        resume.word_count = len(extracted_text.split())
        resume.extraction_status = "completed"
        resume.extracted_at = datetime.now(timezone.utc)

        await db.commit()
        await db.refresh(resume)

        return resume

    except HTTPException:
        raise

    except Exception:
        resume.extraction_status = "failed"
        await db.commit()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to extract text from the resume.",
        )
    
@router.get("/{resume_id}/text", response_model=ResumeTextOut)
async def get_resume_text(
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Find resume and verify ownership
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == current_user.id,
        )
    )

    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found or access unauthorized.",
        )

    # Return extraction information
    return resume