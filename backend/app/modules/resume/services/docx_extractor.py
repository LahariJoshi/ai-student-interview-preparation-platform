from pathlib import Path

from docx import Document


def extract_text_from_docx(file_path: str | Path) -> str:
    """
    Extract text from a DOCX resume.

    Args:
        file_path: Path to the DOCX file.

    Returns:
        Extracted text as a single normalized string.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"DOCX file not found: {file_path}")

    document = Document(file_path)

    extracted_parts = []

    # Extract normal paragraphs
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            extracted_parts.append(text)

    # Extract text from tables
    for table in document.tables:
        for row in table.rows:
            row_text = []

            for cell in row.cells:
                cell_text = cell.text.strip()

                if cell_text:
                    row_text.append(cell_text)

            if row_text:
                extracted_parts.append(" | ".join(row_text))

    # Combine all extracted content
    extracted_text = "\n".join(extracted_parts)

    # Normalize line endings and remove null characters
    extracted_text = extracted_text.replace("\r\n", "\n")
    extracted_text = extracted_text.replace("\r", "\n")
    extracted_text = extracted_text.replace("\x00", "")

    return extracted_text.strip()