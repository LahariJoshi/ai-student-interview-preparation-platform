import os
import uuid
import re
from pathlib import Path
from datetime import datetime, timezone

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
    UploadFile,
    File,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, update

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user

from app.db.models.user import User
from app.db.models.resume import Resume
from app.db.models.resume_analysis import ResumeAnalysis
from app.db.models.ats_analysis import ATSAnalysis
from app.db.models.interview import InterviewSession

from app.modules.resume.schemas import (
    ResumeOut,
    ResumeListOut,
    ResumeTextOut,
    ResumeAnalysisOut,
    AnalysisTriggerResponse,
    MessageResponse,
)

from app.modules.resume.services.pdf_extractor import extract_text_from_pdf
from app.modules.resume.services.docx_extractor import extract_text_from_docx
from app.modules.resume.services.resume_analyzer import analyze_resume


router = APIRouter(prefix="/resume", tags=["Resume"])


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_RESUMES_PER_USER = 5

ALLOWED_EXTENSIONS = {".pdf", ".docx"}

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/octet-stream",
}

PDF_MAGIC_BYTES = b"%PDF"
DOCX_MAGIC_BYTES = b"PK\x03\x04"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize the uploaded filename to prevent path traversal
    and unsafe characters.
    """

    clean_name = Path(filename).name

    clean_name = re.sub(
        r"[\x00-\x1f\x7f]",
        "",
        clean_name,
    )

    clean_name = re.sub(
        r"[^\w\.-]",
        "_",
        clean_name,
    )

    return clean_name or "uploaded_resume.pdf"


def set_no_cache_headers(response: Response) -> None:
    """Ensure client and intermediate proxies do not cache dynamic resume state."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"


# ============================================================================
# UPLOAD RESUME
# ============================================================================

@router.post(
    "/upload",
    response_model=ResumeOut,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    response: Response,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    set_no_cache_headers(response)
    # 1. Enforce maximum resume count
    count_query = select(func.count(Resume.id)).where(
        Resume.user_id == current_user.id
    )

    count_result = await db.execute(count_query)

    user_resume_count = count_result.scalar_one()

    if user_resume_count >= MAX_RESUMES_PER_USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Maximum limit of {MAX_RESUMES_PER_USER} uploaded resumes "
                "reached. Delete an existing resume to upload a new one."
            ),
        )

    # 2. Filename validation
    if (
        not file.filename
        or ".." in file.filename
        or "/" in file.filename
        or "\\" in file.filename
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or malicious filename provided.",
        )

    sanitized_original = sanitize_filename(file.filename)

    file_ext = Path(sanitized_original).suffix.lower()

    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid file type. Only PDF (.pdf) and DOCX (.docx) "
                "files are supported."
            ),
        )

    # 3. Magic byte validation
    header_bytes = await file.read(1024)

    if not header_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    is_pdf = header_bytes.startswith(PDF_MAGIC_BYTES)
    is_docx = header_bytes.startswith(DOCX_MAGIC_BYTES)

    if file_ext == ".pdf" and not is_pdf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "File content signature mismatch. "
                "Expected valid PDF document."
            ),
        )

    if file_ext == ".docx" and not is_docx:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "File content signature mismatch. "
                "Expected valid DOCX document."
            ),
        )

    # Reset stream
    await file.seek(0)

    # 4. Read file in chunks
    chunk_size = 1024 * 1024
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
                detail=(
                    "File size exceeds maximum allowed limit of 5 MB."
                ),
            )

        file_content.extend(chunk)

    # 5. Determine MIME type
    determined_mime = (
        "application/pdf"
        if file_ext == ".pdf"
        else (
            "application/"
            "vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    )

    # 6. Generate unique filename
    resume_uuid = uuid.uuid4()

    stored_filename = (
        f"{resume_uuid.hex[:8]}_{sanitized_original}"
    )

    user_upload_dir = os.path.join(
        settings.UPLOADS_DIR,
        str(current_user.id),
    )

    os.makedirs(
        user_upload_dir,
        exist_ok=True,
    )

    full_file_path = os.path.join(
        user_upload_dir,
        stored_filename,
    )

    # 7. Write file to disk
    with open(full_file_path, "wb") as f:
        f.write(file_content)

    # 8. Create database record
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


# ============================================================================
# GET USER RESUMES
# ============================================================================

@router.get(
    "/my-resumes",
    response_model=ResumeListOut,
)
async def get_my_resumes(
    response: Response,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    set_no_cache_headers(response)

    result = await db.execute(
        select(Resume)
        .where(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
    )

    resumes = result.scalars().all()

    return {
        "resumes": resumes,
        "total_count": len(resumes),
    }


# ============================================================================
# DELETE RESUME
# ============================================================================

@router.delete(
    "/{resume_id}",
    response_model=MessageResponse,
)
async def delete_resume(
    resume_id: uuid.UUID,
    response: Response,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    set_no_cache_headers(response)

    # 1. Fetch resume and verify strict ownership
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

    # 2. Clean up referencing records across all application modules
    # Detach linked interview sessions by setting resume_id to NULL
    await db.execute(
        update(InterviewSession)
        .where(InterviewSession.resume_id == resume_id)
        .values(resume_id=None)
    )

    # Delete ATS analysis records tied to this resume
    await db.execute(
        delete(ATSAnalysis).where(ATSAnalysis.resume_id == resume_id)
    )

    # Delete ResumeAnalysis records tied to this resume
    await db.execute(
        delete(ResumeAnalysis).where(ResumeAnalysis.resume_id == resume_id)
    )

    # 3. Permanently remove physical file from server storage
    candidate_file_paths = {
        resume.file_path,
        os.path.abspath(resume.file_path),
        os.path.join(settings.UPLOADS_DIR, str(current_user.id), resume.stored_filename),
        os.path.abspath(os.path.join(settings.UPLOADS_DIR, str(current_user.id), resume.stored_filename)),
        os.path.join("backend", settings.UPLOADS_DIR, str(current_user.id), resume.stored_filename),
        os.path.abspath(os.path.join("backend", settings.UPLOADS_DIR, str(current_user.id), resume.stored_filename)),
    }
    for file_p in candidate_file_paths:
        if file_p and os.path.isfile(file_p):
            try:
                os.remove(file_p)
            except OSError:
                pass

    # Clean up empty user upload directory if no files remain
    user_upload_dirs = {
        os.path.dirname(resume.file_path),
        os.path.join(settings.UPLOADS_DIR, str(current_user.id)),
        os.path.join("backend", settings.UPLOADS_DIR, str(current_user.id)),
    }
    for udir in user_upload_dirs:
        if udir and os.path.isdir(udir):
            try:
                if not os.listdir(udir):
                    os.rmdir(udir)
            except OSError:
                pass

    # 4. Permanently delete database record
    await db.delete(resume)
    await db.commit()

    return {
        "message": "Resume deleted successfully."
    }


# ============================================================================
# EXTRACT RESUME TEXT
# ============================================================================

@router.post(
    "/{resume_id}/extract-text",
    response_model=ResumeTextOut,
)
async def extract_resume_text(
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
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

    file_path_to_use = resume.file_path
    if not os.path.exists(file_path_to_use):
        candidate_paths = [
            os.path.abspath(resume.file_path),
            os.path.join(settings.UPLOADS_DIR, str(current_user.id), resume.stored_filename),
            os.path.abspath(os.path.join(settings.UPLOADS_DIR, str(current_user.id), resume.stored_filename)),
            os.path.join("backend", settings.UPLOADS_DIR, str(current_user.id), resume.stored_filename),
            os.path.abspath(os.path.join("backend", settings.UPLOADS_DIR, str(current_user.id), resume.stored_filename)),
        ]
        found = False
        for alt_path in candidate_paths:
            if alt_path and os.path.isfile(alt_path):
                file_path_to_use = alt_path
                resume.file_path = alt_path
                found = True
                break

        if not found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume file not found on the server.",
            )

    try:

        if resume.mime_type == "application/pdf":

            extracted_text = extract_text_from_pdf(
                resume.file_path
            )

        elif resume.mime_type == (
            "application/"
            "vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):

            extracted_text = extract_text_from_docx(
                resume.file_path
            )

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported resume file type.",
            )

        # Check extracted text
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

        # Save extraction results
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


# ============================================================================
# GET RESUME TEXT
# ============================================================================

@router.get(
    "/{resume_id}/text",
    response_model=ResumeTextOut,
)
async def get_resume_text(
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
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

    return resume


# ============================================================================
# M3 + M4 — ANALYZE RESUME
# ============================================================================

@router.post(
    "/{resume_id}/analyze",
    response_model=ResumeAnalysisOut,
)
async def analyze_resume_endpoint(
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Run deterministic M3 + M4 resume analysis.

    Requires text extraction to be completed.

    The analysis record is upserted:
        - create if no analysis exists
        - update if analysis already exists
    """

    # 1. Find resume and verify ownership
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

    # 2. Require extraction
    if (
        resume.extraction_status != "completed"
        or not resume.raw_text
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Resume text has not been extracted yet. "
                "Call POST /resume/{resume_id}/extract-text first."
            ),
        )

    # 3. Run M3 + M4 analysis
    try:

        analysis_result = analyze_resume(
            raw_text=resume.raw_text,
            word_count=resume.word_count or 0,
            character_count=resume.character_count or 0,
        )

    except Exception as exc:

        # Keep the original exception internally available during
        # development while returning a safe API message.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Resume analysis failed due to an internal error.",
        ) from exc

    # 4. Check whether an analysis already exists
    existing_result = await db.execute(
        select(ResumeAnalysis).where(
            ResumeAnalysis.resume_id == resume_id
        )
    )

    analysis = existing_result.scalar_one_or_none()

    # ========================================================================
    # UPDATE EXISTING ANALYSIS
    # ========================================================================

    if analysis:

        analysis.analysis_status = "completed"

        # Final score = M4 advanced score
        analysis.quality_score = analysis_result[
            "quality_score"
        ]

        analysis.sections_json = analysis_result[
            "sections"
        ]

        analysis.skills_json = analysis_result[
            "skills"
        ]

        analysis.gaps_json = analysis_result[
            "gaps"
        ]

        # Store both M3 and M4 breakdowns
        analysis.quality_details_json = {
            "m3_structural": analysis_result[
                "quality_details"
            ],
            "m4_advanced": analysis_result[
                "advanced_quality_details"
            ],
        }

        analysis.analyzed_at = analysis_result[
            "analyzed_at"
        ]

    # ========================================================================
    # CREATE NEW ANALYSIS
    # ========================================================================

    else:

        analysis = ResumeAnalysis(
            resume_id=resume_id,
            user_id=current_user.id,
            analysis_status="completed",

            # Final score = M4 score
            quality_score=analysis_result[
                "quality_score"
            ],

            sections_json=analysis_result[
                "sections"
            ],

            skills_json=analysis_result[
                "skills"
            ],

            gaps_json=analysis_result[
                "gaps"
            ],

            # Store both M3 and M4 breakdowns
            quality_details_json={
                "m3_structural": analysis_result[
                    "quality_details"
                ],
                "m4_advanced": analysis_result[
                    "advanced_quality_details"
                ],
            },

            analyzed_at=analysis_result[
                "analyzed_at"
            ],
        )

        db.add(analysis)

    # 5. Persist
    await db.commit()

    await db.refresh(analysis)

    return analysis


# ============================================================================
# GET STORED ANALYSIS
# ============================================================================

@router.get("/latest/analysis")
async def get_latest_resume_analysis(
    response: Response,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    set_no_cache_headers(response)

    result = await db.execute(
        select(ResumeAnalysis)
        .join(Resume, ResumeAnalysis.resume_id == Resume.id)
        .where(
            ResumeAnalysis.user_id == current_user.id,
            Resume.user_id == current_user.id,
        )
        .order_by(ResumeAnalysis.created_at.desc())
        .limit(1)
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        return None
    return analysis


@router.get(
    "/{resume_id}/analysis",
    response_model=ResumeAnalysisOut,
)
async def get_resume_analysis(
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve the stored M3 + M4 analysis for a resume.
    """

    # 1. Verify resume ownership
    resume_result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == current_user.id,
        )
    )

    resume = resume_result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found or access unauthorized.",
        )

    # 2. Fetch analysis
    analysis_result = await db.execute(
        select(ResumeAnalysis).where(
            ResumeAnalysis.resume_id == resume_id
        )
    )

    analysis = analysis_result.scalar_one_or_none()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "No analysis found for this resume. "
                "Run POST /resume/{resume_id}/analyze first."
            ),
        )

    return analysis
