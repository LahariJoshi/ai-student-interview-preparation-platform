"""add_resume_extraction_fields

Revision ID: 003
Revises: 002
Create Date: 2026-09-12 11:35:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('resumes', sa.Column('raw_text', sa.Text(), nullable=True))
    op.add_column('resumes', sa.Column('extraction_status', sa.String(length=50), nullable=False, server_default='pending'))
    op.add_column('resumes', sa.Column('character_count', sa.Integer(), nullable=True))
    op.add_column('resumes', sa.Column('word_count', sa.Integer(), nullable=True))
    op.add_column('resumes', sa.Column('extracted_at', sa.DateTime(timezone=True), nullable=True))
    op.create_index(op.f('ix_resumes_extraction_status'), 'resumes', ['extraction_status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_resumes_extraction_status'), table_name='resumes')
    op.drop_column('resumes', 'extracted_at')
    op.drop_column('resumes', 'word_count')
    op.drop_column('resumes', 'character_count')
    op.drop_column('resumes', 'extraction_status')
    op.drop_column('resumes', 'raw_text')
