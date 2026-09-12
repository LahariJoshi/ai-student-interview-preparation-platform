from pathlib import Path

import pdfplumber


def extract_text_from_pdf(file_path: str | Path) -> str:
    """
    Extract text from a PDF resume.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Extracted text as a single normalized string.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    extracted_pages = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                extracted_pages.append(text)

    # Combine text from all pages
    extracted_text = "\n\n".join(extracted_pages)

    # Normalize the extracted text
    extracted_text = extracted_text.replace("\r\n", "\n")
    extracted_text = extracted_text.replace("\r", "\n")
    extracted_text = extracted_text.replace("\x00", "")

    # Remove excessive blank lines
    lines = [line.rstrip() for line in extracted_text.split("\n")]

    normalized_lines = []
    blank_line_count = 0

    for line in lines:
        if line.strip():
            normalized_lines.append(line)
            blank_line_count = 0
        else:
            blank_line_count += 1

            # Allow at most one blank line
            if blank_line_count <= 1:
                normalized_lines.append("")

    return "\n".join(normalized_lines).strip()