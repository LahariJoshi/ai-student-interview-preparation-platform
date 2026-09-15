import re
from typing import Dict


SECTION_ALIASES = {
    "contact": {
        "contact",
        "contact information",
        "personal information",
    },
    "summary": {
        "summary",
        "professional summary",
        "profile",
        "professional profile",
        "objective",
        "career objective",
        "about me",
    },
    "education": {
        "education",
        "academic background",
        "academics",
        "qualifications",
    },
    "skills": {
        "skills",
        "technical skills",
        "technical skill",
        "core competencies",
        "key skills",
        "technologies",
    },
    "projects": {
        "projects",
        "academic projects",
        "personal projects",
        "key projects",
    },
    "experience": {
        "experience",
        "work experience",
        "professional experience",
        "employment",
    },
    "internships": {
        "internships",
        "internship",
        "training",
    },
    "certifications": {
        "certifications",
        "certificates",
        "licenses",
    },
    "achievements": {
        "achievements",
        "awards",
        "honors",
    },
    "publications": {
        "publications",
        "research",
        "papers",
    },
    "extracurricular": {
        "extracurricular",
        "activities",
        "clubs",
        "volunteering",
        "co-curricular",
        "leadership",
    },
}


def _normalise_heading(line: str) -> str:
    """
    Normalize a possible section heading.
    """

    line = line.strip()

    # Remove markdown heading markers.
    line = re.sub(r"^#+\s*", "", line)

    # Remove common decoration.
    line = line.strip(":-|•* ")

    # Collapse repeated whitespace.
    line = re.sub(r"\s+", " ", line)

    return line.lower()


def _heading_to_section(line: str) -> str | None:
    """
    Return the canonical section name for a heading.
    """

    normalized = _normalise_heading(line)

    for section, aliases in SECTION_ALIASES.items():
        if normalized in aliases:
            return section

    return None


def extract_sections(text: str) -> Dict[str, str]:
    """
    Extract the text belonging to each recognized resume section.

    Only heading-like lines matching known section aliases are used
    as section boundaries.

    Returns:
        Dictionary mapping canonical section names to their text.
    """

    sections: Dict[str, str] = {}

    if not text or not text.strip():
        return sections

    lines = text.splitlines()

    current_section: str | None = None
    current_content: list[str] = []

    def save_current_section() -> None:
        if current_section is None:
            return

        content = "\n".join(current_content).strip()

        if content:
            sections[current_section] = content

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if current_section is not None:
                current_content.append("")
            continue

        section = _heading_to_section(stripped)

        if section is not None:
            save_current_section()

            current_section = section
            current_content = []
            continue

        if current_section is not None:
            current_content.append(stripped)

    save_current_section()

    return sections