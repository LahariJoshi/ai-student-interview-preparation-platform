"""add coding assessment tables

Revision ID: 006
Revises: 005
Create Date: 2026-09-30
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "006"
down_revision: Union[str, None] = "005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. coding_questions
    op.create_table(
        "coding_questions",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "slug",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "difficulty",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "topic",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "constraints",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "hints",
            sa.JSON(),
            nullable=True,
        ),
        sa.Column(
            "starter_code",
            sa.JSON(),
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
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_coding_questions_slug",
        "coding_questions",
        ["slug"],
        unique=True,
    )
    op.create_index(
        "ix_coding_questions_difficulty",
        "coding_questions",
        ["difficulty"],
        unique=False,
    )
    op.create_index(
        "ix_coding_questions_topic",
        "coding_questions",
        ["topic"],
        unique=False,
    )

    # 2. coding_test_cases
    op.create_table(
        "coding_test_cases",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "question_id",
            sa.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "input_data",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "expected_output",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "is_sample",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "explanation",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "order_index",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["coding_questions.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_coding_test_cases_question_id",
        "coding_test_cases",
        ["question_id"],
        unique=False,
    )

    # 3. coding_submissions
    op.create_table(
        "coding_submissions",
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
            "question_id",
            sa.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "language",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "code",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            server_default="pending",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["coding_questions.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_coding_submissions_user_id",
        "coding_submissions",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_coding_submissions_question_id",
        "coding_submissions",
        ["question_id"],
        unique=False,
    )

    # 4. coding_results
    op.create_table(
        "coding_results",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "submission_id",
            sa.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "verdict",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "score",
            sa.Float(),
            server_default=sa.text("0.0"),
            nullable=False,
        ),
        sa.Column(
            "passed_test_cases",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "total_test_cases",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "execution_time_ms",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "memory_kb",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "error_message",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "test_case_results_json",
            sa.JSON(),
            nullable=True,
        ),
        sa.Column(
            "evaluated_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["submission_id"],
            ["coding_submissions.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_coding_results_submission_id",
        "coding_results",
        ["submission_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_coding_results_submission_id",
        table_name="coding_results",
    )
    op.drop_table("coding_results")

    op.drop_index(
        "ix_coding_submissions_question_id",
        table_name="coding_submissions",
    )
    op.drop_index(
        "ix_coding_submissions_user_id",
        table_name="coding_submissions",
    )
    op.drop_table("coding_submissions")

    op.drop_index(
        "ix_coding_test_cases_question_id",
        table_name="coding_test_cases",
    )
    op.drop_table("coding_test_cases")

    op.drop_index(
        "ix_coding_questions_topic",
        table_name="coding_questions",
    )
    op.drop_index(
        "ix_coding_questions_difficulty",
        table_name="coding_questions",
    )
    op.drop_index(
        "ix_coding_questions_slug",
        table_name="coding_questions",
    )
    op.drop_table("coding_questions")
