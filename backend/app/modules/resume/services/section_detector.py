"""
Section Detector — detects resume sections using heading-aware matching.

The detector primarily looks for section headings rather than searching
the entire resume body. This reduces false positives such as detecting
"education" simply because words like "degree" or "college" appear in
a project description.
"""

import re
from typing import Dict, List


# Maps canonical section names to possible heading variants.
SECTION_KEYWORDS: Dict[str, List[str]] = {
    "contact": [
        "contact",
        "contact information",
        "contact details",
        "personal information",
        "personal details",
        "personal info",
    ],
    "summary": [
        "summary",
        "professional summary",
        "career summary",
        "objective",
        "career objective",
        "professional objective",
        "profile",
        "about me",
        "about",
        "overview",
    ],
    "education": [
        "education",
        "educational background",
        "academic background",
        "academic qualifications",
        "qualifications",
        "academics",
        "educational qualifications",
    ],
    "skills": [
        "skills",
        "technical skills",
        "core competencies",
        "competencies",
        "expertise",
        "technologies",
        "tools",
        "key skills",
        "skill set",
        "technical expertise",
    ],
    "projects": [
        "projects",
        "personal projects",
        "academic projects",
        "project work",
        "notable projects",
        "key projects",
        "side projects",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
        "career history",
        "job experience",
    ],
    "internships": [
        "internships",
        "internship",
        "internship experience",
        "trainee",
        "traineeships",
        "industrial training",
        "summer internship",
    ],
    "certifications": [
        "certifications",
        "certification",
        "certificates",
        "certificate",
        "licenses",
        "credentials",
        "professional certifications",
    ],
    "achievements": [
        "achievements",
        "accomplishments",
        "honors",
        "awards",
        "recognition",
        "accolades",
        "distinctions",
    ],
    "publications": [
        "publications",
        "research work",
        "papers",
        "articles",
        "journals",
        "research papers",
    ],
    "extracurricular": [
        "extracurricular",
        "extracurricular activities",
        "activities",
        "clubs",
        "organizations",
        "volunteering",
        "volunteer work",
        "co-curricular",
        "hobbies",
        "interests",
        "leadership",
    ],
}


def _normalise_heading(line: str) -> str:
    """
    Normalize a possible heading.

    Removes common heading decorations such as:
      - leading/trailing whitespace
      - bullets
      - markdown-style hashes
      - trailing colon
      - repeated spaces

    Example:
        "  ### TECHNICAL SKILLS:  "
        becomes
        "technical skills"
    """
    heading = line.strip().lower()

    # Remove common heading prefixes.
    heading = re.sub(r"^[#*\-•▪◦]+\s*", "", heading)

    # Remove trailing punctuation.
    heading = re.sub(r"[:\-–—]+$", "", heading)

    # Collapse repeated whitespace.
    heading = re.sub(r"\s+", " ", heading)

    return heading.strip()


def _is_heading_like(line: str) -> bool:
    """
    Determine whether a line looks like a resume section heading.

    A heading is generally:
      - short
      - not a normal sentence
      - mostly alphabetic
      - optionally written in uppercase
    """
    stripped = line.strip()

    if not stripped:
        return False

    # Very long lines are unlikely to be section headings.
    if len(stripped) > 60:
        return False

    normalised = _normalise_heading(stripped)

    if not normalised:
        return False

    # A heading should not contain sentence-like punctuation.
    if any(char in normalised for char in [".", ",", ";"]):
        return False

    words = normalised.split()

    # Avoid treating long sentences as headings.
    if len(words) > 5:
        return False

    return True


def detect_sections(raw_text: str) -> Dict[str, bool]:
    """
    Detect resume sections using heading-aware matching.

    Section names are matched against individual heading-like lines
    instead of arbitrary words appearing anywhere in the resume.

    Returns:
        Dict mapping canonical section name -> detected/not detected.
    """

    if not raw_text or not raw_text.strip():
        return {
            section: False
            for section in SECTION_KEYWORDS
        }

    lines = raw_text.splitlines()

    detected: Dict[str, bool] = {
        section: False
        for section in SECTION_KEYWORDS
    }

    for line in lines:
        if not _is_heading_like(line):
            continue

        heading = _normalise_heading(line)

        for section, keywords in SECTION_KEYWORDS.items():
            if detected[section]:
                continue

            for keyword in keywords:
                if heading == keyword.lower():
                    detected[section] = True
                    break

    return detected