"""add interview and voice tables

Revision ID: 006
Revises: 005
Create Date: 2026-10-01
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
    # 1. interview_sessions
    op.create_table(
        "interview_sessions",
        sa.Column("id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("target_role", sa.String(length=100), nullable=False),
        sa.Column("interview_type", sa.String(length=50), nullable=False, server_default="Mixed"),
        sa.Column("experience_level", sa.String(length=50), nullable=False, server_default="Fresher"),
        sa.Column("difficulty", sa.String(length=50), nullable=False, server_default="Medium"),
        sa.Column("answer_mode", sa.String(length=50), nullable=False, server_default="Voice + Text"),
        sa.Column("question_count", sa.Integer(), nullable=False, server_default="5"),
        sa.Column("target_company", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("current_question_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("overall_score", sa.Float(), nullable=True),
        sa.Column("technical_score", sa.Float(), nullable=True),
        sa.Column("communication_score", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_interview_sessions_user_id", "interview_sessions", ["user_id"], unique=False)
    op.create_index("ix_interview_sessions_status", "interview_sessions", ["status"], unique=False)

    # 2. interview_questions
    op.create_table(
        "interview_questions",
        sa.Column("id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("session_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("question_order", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False, server_default="technical"),
        sa.Column("topic", sa.String(length=100), nullable=True),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("expected_points", sa.JSON(), nullable=True),
        sa.Column("difficulty", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["interview_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_interview_questions_session_id", "interview_questions", ["session_id"], unique=False)

    # 3. interview_responses
    op.create_table(
        "interview_responses",
        sa.Column("id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("session_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("question_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("transcribed_text", sa.Text(), nullable=False),
        sa.Column("audio_file_path", sa.String(length=500), nullable=True),
        sa.Column("audio_duration_seconds", sa.Float(), nullable=True),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("feedback_text", sa.Text(), nullable=True),
        sa.Column("key_strengths", sa.JSON(), nullable=True),
        sa.Column("missing_concepts", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["interview_sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["question_id"], ["interview_questions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_interview_responses_session_id", "interview_responses", ["session_id"], unique=False)
    op.create_index("ix_interview_responses_question_id", "interview_responses", ["question_id"], unique=False)

    # 4. interview_feedback
    op.create_table(
        "interview_feedback",
        sa.Column("id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("session_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("overall_score", sa.Float(), nullable=False),
        sa.Column("technical_score", sa.Float(), nullable=False),
        sa.Column("communication_score", sa.Float(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("key_strengths", sa.JSON(), nullable=True),
        sa.Column("areas_for_improvement", sa.JSON(), nullable=True),
        sa.Column("actionable_recommendations", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["interview_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_id"),
    )
    op.create_index("ix_interview_feedback_session_id", "interview_feedback", ["session_id"], unique=True)

    # 5. voice_analyses
    op.create_table(
        "voice_analyses",
        sa.Column("id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("response_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("audio_url", sa.String(length=500), nullable=True),
        sa.Column("speaking_rate_wpm", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("filler_word_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("filler_words_detected", sa.JSON(), nullable=True),
        sa.Column("pause_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_pause_duration_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("clarity_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("confidence_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("tone_evaluation", sa.String(length=100), nullable=True),
        sa.Column("communication_feedback", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["response_id"], ["interview_responses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("response_id"),
    )
    op.create_index("ix_voice_analyses_response_id", "voice_analyses", ["response_id"], unique=True)


def downgrade() -> None:
    # 5. voice_analyses
    op.drop_index("ix_voice_analyses_response_id", table_name="voice_analyses")
    op.drop_table("voice_analyses")

    # 4. interview_feedback
    op.drop_index("ix_interview_feedback_session_id", table_name="interview_feedback")
    op.drop_table("interview_feedback")

    # 3. interview_responses
    op.drop_index("ix_interview_responses_question_id", table_name="interview_responses")
    op.drop_index("ix_interview_responses_session_id", table_name="interview_responses")
    op.drop_table("interview_responses")

    # 2. interview_questions
    op.drop_index("ix_interview_questions_session_id", table_name="interview_questions")
    op.drop_table("interview_questions")

    # 1. interview_sessions
    op.drop_index("ix_interview_sessions_status", table_name="interview_sessions")
    op.drop_index("ix_interview_sessions_user_id", table_name="interview_sessions")
    op.drop_table("interview_sessions")
