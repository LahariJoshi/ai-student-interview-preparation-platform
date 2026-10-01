from typing import Dict, Any, Optional


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model: Optional[Any] = None


def get_model() -> Any:
    """
    Load the Sentence Transformer model once and reuse it.
    """
    global _model

    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            raise RuntimeError(
                "The 'sentence-transformers' package is required for ATS semantic analysis. "
                "Please install it via requirements.txt."
            ) from e
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def calculate_semantic_similarity(
    resume_text: str,
    job_description: str,
) -> Dict[str, float]:
    """
    Calculate semantic similarity between resume text
    and job description using Sentence Transformers.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    try:
        from sentence_transformers import util
    except ImportError as e:
        raise RuntimeError(
            "The 'sentence-transformers' package is required for ATS semantic analysis. "
            "Please install it via requirements.txt."
        ) from e

    model = get_model()

    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=True,
    )

    jd_embedding = model.encode(
        job_description,
        convert_to_tensor=True,
    )

    similarity = util.cos_sim(
        resume_embedding,
        jd_embedding,
    ).item()

    similarity = max(0.0, min(1.0, similarity))

    semantic_score = similarity * 100

    return {
        "cosine_similarity": round(similarity, 4),
        "semantic_score": round(semantic_score, 2),
    }