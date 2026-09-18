from typing import Any, Dict, List


CORE_SECTIONS = [
    "education",
    "skills",
    "projects",
    "experience",
]


def analyze_formatting(
    raw_text: str,
    sections: Dict[str, bool],
    contact: Dict[str, bool],
    length_analysis: Dict[str, Any],
) -> Dict[str, Any]:

    # ================================================================
    # 1. RESUME LENGTH SCORE — 20 POINTS
    # ================================================================

    length_score = float(length_analysis.get("score", 0.0))

    # Convert the existing 10-point length score
    # into the 20-point ATS formatting contribution.
    length_score = (length_score / 10.0) * 20.0

        # ================================================================
    # 2. CORE SECTION STRUCTURE SCORE — 20 POINTS
    # ================================================================

    section_score = 0.0
    missing_sections: List[str] = []

    points_per_section = 20.0 / len(CORE_SECTIONS)

    for section in CORE_SECTIONS:
        if sections.get(section, False):
            section_score += points_per_section
        else:
            missing_sections.append(section)

    # ================================================================
    # 3. CONTACT INFORMATION SCORE — 15 POINTS
    # ================================================================

    contact_score = 0.0

    if contact.get("has_email", False):
        contact_score += 5.0

    if contact.get("has_phone", False):
        contact_score += 4.0

    if contact.get("has_linkedin", False):
        contact_score += 3.0

    if contact.get("has_github", False):
        contact_score += 3.0

    # ================================================================
    # 4. BULLET / LINE STRUCTURE SCORE — 15 POINTS
    # ================================================================

    lines = [
        line.strip()
        for line in raw_text.splitlines()
        if line.strip()
    ]

    bullet_markers = ("•", "-", "*", "▪", "◦", "‣", "➢")

    bullet_lines = sum(
        1 for line in lines
        if line.startswith(bullet_markers)
    )

    # 7 points for having a reasonable bullet structure.
    if bullet_lines >= 3:
        bullet_score = 7.0
    elif bullet_lines >= 1:
        bullet_score = 4.0
    else:
        bullet_score = 0.0

    # Count reasonably short content lines.
    structured_lines = sum(
        1 for line in lines
        if 20 <= len(line) <= 120
    )

    if structured_lines >= 8:
        line_structure_score = 5.0
    elif structured_lines >= 4:
        line_structure_score = 3.0
    else:
        line_structure_score = 1.0

    # Identify excessively long lines.
    long_lines = sum(
        1 for line in lines
        if len(line) > 180
    )

    if long_lines == 0:
        long_line_score = 3.0
    elif long_lines <= 2:
        long_line_score = 2.0
    else:
        long_line_score = 0.0

    bullet_structure_score = (
        bullet_score
        + line_structure_score
        + long_line_score
    )


    # ================================================================
    # 5. SPECIAL CHARACTER SCORE — 10 POINTS
    # ================================================================

    if not raw_text or not raw_text.strip():
        special_character_score = 0.0
    else:
        allowed_characters = set(
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789"
            " .,;:!?@#$%&*()[]{}+-_/\\|<>='\""
            "•▪◦‣➢"
        )

        total_characters = len(raw_text)
        unusual_characters = sum(
            1 for char in raw_text
            if char not in allowed_characters
            and not char.isspace()
        )

        unusual_character_ratio = (
            unusual_characters / total_characters
        )

        if unusual_character_ratio <= 0.01:
            special_character_score = 10.0
        elif unusual_character_ratio <= 0.03:
            special_character_score = 8.0
        elif unusual_character_ratio <= 0.05:
            special_character_score = 5.0
        else:
            special_character_score = 2.0

    # ================================================================
    # 6. WHITESPACE / READABILITY SCORE — 10 POINTS
    # ================================================================

    if not raw_text or not raw_text.strip():
        whitespace_score = 0.0
    else:
        all_lines = raw_text.splitlines()

        total_lines = len(all_lines)
        blank_lines = sum(
            1 for line in all_lines
            if not line.strip()
        )

        if total_lines == 0:
            blank_line_ratio = 0.0
        else:
            blank_line_ratio = blank_lines / total_lines

        # Penalize excessive blank space.
        if blank_line_ratio <= 0.15:
            blank_space_score = 5.0
        elif blank_line_ratio <= 0.30:
            blank_space_score = 4.0
        elif blank_line_ratio <= 0.45:
            blank_space_score = 2.0
        else:
            blank_space_score = 0.0

        # Check whether the extracted text has enough line structure.
        non_empty_lines = [
            line.strip()
            for line in all_lines
            if line.strip()
        ]

        if len(non_empty_lines) >= 8:
            line_readability_score = 5.0
        elif len(non_empty_lines) >= 4:
            line_readability_score = 3.0
        else:
            line_readability_score = 1.0

        whitespace_score = (
            blank_space_score
            + line_readability_score
        )

    # ================================================================
    # 7. ATS-FRIENDLY TEXT STRUCTURE SCORE — 10 POINTS
    # ================================================================

    # Check whether the resume contains recognizable section headings.
    detected_section_count = sum(
        1 for is_present in sections.values()
        if is_present
    )

    if detected_section_count >= 6:
        heading_score = 4.0
    elif detected_section_count >= 4:
        heading_score = 3.0
    elif detected_section_count >= 2:
        heading_score = 2.0
    else:
        heading_score = 0.0

    # Check the order of important sections when they are present.
    section_order = [
        "contact",
        "summary",
        "education",
        "skills",
        "projects",
        "experience",
        "internships",
        "certifications",
        "achievements",
    ]

    detected_order = [
        section
        for section in section_order
        if sections.get(section, False)
    ]

    correctly_ordered_pairs = 0
    total_ordered_pairs = max(len(detected_order) - 1, 0)

    for i in range(len(detected_order) - 1):
        current_index = section_order.index(detected_order[i])
        next_index = section_order.index(detected_order[i + 1])

        if current_index < next_index:
            correctly_ordered_pairs += 1

    if total_ordered_pairs == 0:
        order_score = 1.0
    elif correctly_ordered_pairs == total_ordered_pairs:
        order_score = 3.0
    elif correctly_ordered_pairs / total_ordered_pairs >= 0.5:
        order_score = 2.0
    else:
        order_score = 1.0

    # Check whether the resume contains meaningful structured content.
    non_empty_lines = [
        line.strip()
        for line in raw_text.splitlines()
        if line.strip()
    ]

    if len(non_empty_lines) >= 10:
        content_structure_score = 3.0
    elif len(non_empty_lines) >= 5:
        content_structure_score = 2.0
    else:
        content_structure_score = 1.0

    ats_structure_score = (
        heading_score
        + order_score
        + content_structure_score
    )

        # ================================================================
    # 8. FORMATTING FEEDBACK
    # ================================================================

    strengths: List[str] = []
    issues: List[str] = []

    # Length feedback
    if length_score >= 17:
        strengths.append("Resume length is appropriate for ATS processing.")
    elif length_score >= 12:
        issues.append("Resume length could be improved for better content balance.")
    else:
        issues.append("Resume is too short and may not contain enough relevant content.")

    # Section feedback
    if not missing_sections:
        strengths.append("All core resume sections are present.")
    else:
        for section in missing_sections:
            display_name = section.replace("_", " ").title()
            issues.append(f"Core section '{display_name}' is missing.")

    # Contact feedback
    if contact_score == 15:
        strengths.append("Complete contact information is detected.")
    elif contact_score >= 9:
        issues.append("Some important contact information is missing.")
    else:
        issues.append("Important contact information is missing.")

    # Bullet / line structure
    if bullet_structure_score >= 12:
        strengths.append("Resume has a clear bullet and line structure.")
    else:
        issues.append("Improve bullet usage and text line structure.")

    # Special characters
    if special_character_score >= 8:
        strengths.append("Text contains few unusual characters.")
    else:
        issues.append("Some unusual characters may affect text-based ATS parsing.")

    # Whitespace
    if whitespace_score >= 8:
        strengths.append("Whitespace and text spacing are reasonably structured.")
    else:
        issues.append("Improve whitespace and text spacing for better readability.")

    # ATS structure
    if ats_structure_score >= 8:
        strengths.append("Resume has an ATS-readable text structure.")
    else:
        issues.append("Improve section structure and ordering for ATS readability.")

    # ================================================================
    # FINAL FORMATTING SCORE
    # ================================================================

    total_score = (
        length_score
        + section_score
        + contact_score
        + bullet_structure_score
        + special_character_score
        + whitespace_score
        + ats_structure_score
    )

    return {
        "score": round(total_score, 2),

        "strengths": strengths,
        "issues": issues,

        "details": {
            "length_score": round(length_score, 2),
            "section_score": round(section_score, 2),
            "contact_score": round(contact_score, 2),
            "bullet_structure_score": round(
                bullet_structure_score, 2
            ),
            "special_character_score": round(
                special_character_score, 2
            ),
            "whitespace_score": round(
                whitespace_score, 2
            ),
            "ats_structure_score": round(
                ats_structure_score, 2
            ),
        },

        "missing_sections": missing_sections,
        "word_count": length_analysis.get("word_count", 0),
        "content_density": length_analysis.get(
            "content_density",
            "unknown",
        ),
    }

