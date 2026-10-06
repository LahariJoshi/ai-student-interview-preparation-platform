import hashlib
import threading
from collections import OrderedDict
from typing import Dict, Any, Optional


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model: Optional[Any] = None
_model_lock = threading.Lock()

# Thread-safe LRU cache for computed text embeddings to avoid re-encoding
_embedding_cache: Dict[str, Any] = OrderedDict()
_cache_lock = threading.Lock()
MAX_CACHE_SIZE = 512


def get_model() -> Any:
    """
    Load the Sentence Transformer model once and reuse it across requests.
    Thread-safe and prefers local cached files to prevent blocking network requests.
    """
    global _model

    if _model is None:
        with _model_lock:
            if _model is None:
                try:
                    from sentence_transformers import SentenceTransformer
                except ImportError as e:
                    raise RuntimeError(
                        "The 'sentence-transformers' package is required for ATS semantic analysis. "
                        "Please install it via requirements.txt."
                    ) from e

                # Attempt fast load from local cached weights first to bypass network overhead
                try:
                    _model = SentenceTransformer(MODEL_NAME, local_files_only=True)
                except Exception:
                    # Fallback to standard download if local cache is not available
                    _model = SentenceTransformer(MODEL_NAME)

    return _model


def _get_embedding(text: str, model: Any) -> Any:
    """
    Compute or retrieve cached tensor embedding for the given text.
    """
    text_key = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

    with _cache_lock:
        if text_key in _embedding_cache:
            _embedding_cache.move_to_end(text_key)
            return _embedding_cache[text_key]

    embedding = model.encode(text, convert_to_tensor=True)

    with _cache_lock:
        _embedding_cache[text_key] = embedding
        if len(_embedding_cache) > MAX_CACHE_SIZE:
            _embedding_cache.popitem(last=False)

    return embedding


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

    resume_embedding = _get_embedding(resume_text, model)
    jd_embedding = _get_embedding(job_description, model)

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
