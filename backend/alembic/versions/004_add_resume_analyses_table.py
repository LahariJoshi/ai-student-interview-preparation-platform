"""add_resume_analyses_table

Revision ID: 004
Revises: 003
Create Date: 2026-09-13 14:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004'
down_revision: Union[str, None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'resume_analyses',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            'resume_id',
            sa.UUID(as_uuid=True),
            sa.ForeignKey('resumes.id', ondelete='CASCADE'),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            'user_id',
            sa.UUID(as_uuid=True),
            sa.ForeignKey('users.id', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('analysis_status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('quality_score', sa.Float(), nullable=True),
        sa.Column('sections_json', sa.JSON(), nullable=True),
        sa.Column('skills_json', sa.JSON(), nullable=True),
        sa.Column('gaps_json', sa.JSON(), nullable=True),
        sa.Column('quality_details_json', sa.JSON(), nullable=True),
        sa.Column('analyzed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_resume_analyses_resume_id', 'resume_analyses', ['resume_id'], unique=True)
    op.create_index('ix_resume_analyses_user_id', 'resume_analyses', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_resume_analyses_user_id', table_name='resume_analyses')
    op.drop_index('ix_resume_analyses_resume_id', table_name='resume_analyses')
    op.drop_table('resume_analyses')
