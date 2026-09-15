"""
Contact Detector — detects presence of contact fields in raw resume text.
Stores booleans only — never stores actual email addresses, phone numbers, or URLs.
"""

import re
from typing import Dict

# Regex patterns for common contact information
_EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"
)
_PHONE_PATTERN = re.compile(
    r"(?:\+?\d[\d\s\-().]{6,}\d)"  # International/local phone formats
)
_LINKEDIN_PATTERN = re.compile(
    r"linkedin\.com/in/", re.IGNORECASE
)
_GITHUB_PATTERN = re.compile(
    r"github\.com/", re.IGNORECASE
)


def detect_contact(raw_text: str) -> Dict[str, bool]:
    """
    Returns a dict with boolean flags for each contact field type.

    Keys: has_email, has_phone, has_linkedin, has_github
    Values are True/False — actual contact values are NEVER stored.
    """
    return {
        "has_email": bool(_EMAIL_PATTERN.search(raw_text)),
        "has_phone": bool(_PHONE_PATTERN.search(raw_text)),
        "has_linkedin": bool(_LINKEDIN_PATTERN.search(raw_text)),
        "has_github": bool(_GITHUB_PATTERN.search(raw_text)),
    }
