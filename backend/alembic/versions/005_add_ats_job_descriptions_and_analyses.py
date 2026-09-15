"""add ATS job descriptions and analyses

Revision ID: 005
Revises: 004
Create Date: 2026-09-15
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "job_descriptions",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "company_name",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "description_text",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_job_descriptions_user_id",
        "job_descriptions",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "ats_analyses",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "resume_id",
            sa.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "job_description_id",
            sa.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "analysis_status",
            sa.String(length=50),
            nullable=False,
            server_default="pending",
        ),
        sa.Column(
            "ats_score",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "formatting_score",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "keyword_match_score",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "semantic_similarity_score",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "action_impact_score",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "matched_skills_json",
            sa.JSON(),
            nullable=True,
        ),
        sa.Column(
            "missing_skills_json",
            sa.JSON(),
            nullable=True,
        ),
        sa.Column(
            "jd_requirements_json",
            sa.JSON(),
            nullable=True,
        ),
        sa.Column(
            "analysis_details_json",
            sa.JSON(),
            nullable=True,
        ),
        sa.Column(
            "analyzed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["resume_id"],
            ["resumes.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["job_description_id"],
            ["job_descriptions.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_ats_analyses_user_id",
        "ats_analyses",
        ["user_id"],
        unique=False,
    )

    op.create_index(
        "ix_ats_analyses_resume_id",
        "ats_analyses",
        ["resume_id"],
        unique=False,
    )

    op.create_index(
        "ix_ats_analyses_job_description_id",
        "ats_analyses",
        ["job_description_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_ats_analyses_job_description_id",
        table_name="ats_analyses",
    )

    op.drop_index(
        "ix_ats_analyses_resume_id",
        table_name="ats_analyses",
    )

    op.drop_index(
        "ix_ats_analyses_user_id",
        table_name="ats_analyses",
    )

    op.drop_table("ats_analyses")

    op.drop_index(
        "ix_job_descriptions_user_id",
        table_name="job_descriptions",
    )

    op.drop_table("job_descriptions")