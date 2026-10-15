"""add interview tables

Revision ID: 007
Revises: 006
Create Date: 2026-10-13
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "007"
down_revision: Union[str, None] = "006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. interview_sessions
    op.create_table(
        "interview_sessions",
        sa.Column("id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("resume_id", sa.UUID(as_uuid=True), nullable=True),
        sa.Column("interview_type", sa.String(length=50), nullable=False, server_default="mixed"),
        sa.Column("target_role", sa.String(length=100), nullable=False, server_default="Software Developer"),
        sa.Column("experience_level", sa.String(length=50), nullable=False, server_default="Beginner"),
        sa.Column("duration_minutes", sa.Integer(), nullable=False, server_default="15"),
        sa.Column("custom_skills", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="in_progress"),
        sa.Column("total_questions", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("current_question_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("overall_score", sa.Float(), nullable=True),
        sa.Column("technical_score", sa.Float(), nullable=True),
        sa.Column("communication_score", sa.Float(), nullable=True),
        sa.Column("strengths", sa.JSON(), nullable=True, server_default="[]"),
        sa.Column("weaknesses", sa.JSON(), nullable=True, server_default="[]"),
        sa.Column("recommendations", sa.JSON(), nullable=True, server_default="[]"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["resume_id"], ["resumes.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_interview_sessions_user_id", "interview_sessions", ["user_id"], unique=False)
    op.create_index("ix_interview_sessions_resume_id", "interview_sessions", ["resume_id"], unique=False)
    op.create_index("ix_interview_sessions_status", "interview_sessions", ["status"], unique=False)

    # 2. interview_questions
    op.create_table(
        "interview_questions",
        sa.Column("id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("session_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False, server_default="technical"),
        sa.Column("difficulty", sa.String(length=50), nullable=False, server_default="Beginner"),
        sa.Column("topic_or_skill", sa.String(length=100), nullable=True),
        sa.Column("expected_key_points", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("reference_answer", sa.Text(), nullable=True),
        sa.Column("evaluation_rubric", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["interview_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_interview_questions_session_id", "interview_questions", ["session_id"], unique=False)

    # 3. interview_answers
    op.create_table(
        "interview_answers",
        sa.Column("id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("session_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("question_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("answer_text", sa.Text(), nullable=False),
        sa.Column("is_voice_response", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("audio_file_path", sa.String(length=512), nullable=True),
        sa.Column("duration_seconds", sa.Float(), nullable=True),
        sa.Column("delivery_metrics", sa.JSON(), nullable=True, server_default="{}"),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("relevance_score", sa.Float(), nullable=True),
        sa.Column("technical_accuracy_score", sa.Float(), nullable=True),
        sa.Column("completeness_score", sa.Float(), nullable=True),
        sa.Column("clarity_score", sa.Float(), nullable=True),
        sa.Column("detailed_feedback", sa.Text(), nullable=True),
        sa.Column("improvement_tips", sa.JSON(), nullable=True, server_default="[]"),
        sa.Column("concepts_to_revise", sa.JSON(), nullable=True, server_default="[]"),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["session_id"], ["interview_sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["question_id"], ["interview_questions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_interview_answers_session_id", "interview_answers", ["session_id"], unique=False)
    op.create_index("ix_interview_answers_question_id", "interview_answers", ["question_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_interview_answers_question_id", table_name="interview_answers")
    op.drop_index("ix_interview_answers_session_id", table_name="interview_answers")
    op.drop_table("interview_answers")

    op.drop_index("ix_interview_questions_session_id", table_name="interview_questions")
    op.drop_table("interview_questions")

    op.drop_index("ix_interview_sessions_status", table_name="interview_sessions")
    op.drop_index("ix_interview_sessions_resume_id", table_name="interview_sessions")
    op.drop_index("ix_interview_sessions_user_id", table_name="interview_sessions")
    op.drop_table("interview_sessions")
