"""Initial schema

Revision ID: 0001
Revises:
Create Date: 2026-04-27 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("grade", sa.Integer(), nullable=True),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("native_language", sa.String(), nullable=True),
        sa.Column("english_level", sa.String(), nullable=True),
        sa.Column("target_country", sa.String(), nullable=True),
        sa.Column("budget_usd", sa.Integer(), nullable=True),
        sa.Column("preferred_study_language", sa.String(), nullable=True),
        sa.Column("interests", sa.JSON(), nullable=True),
        sa.Column("about", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_profiles_id", "profiles", ["id"])

    op.create_table(
        "assessment_results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("raw_scores", sa.JSON(), nullable=False),
        sa.Column("normalized_scores", sa.JSON(), nullable=False),
        sa.Column("top_categories", sa.JSON(), nullable=False),
        sa.Column("recommended_majors", sa.JSON(), nullable=False),
        sa.Column("profile_summary", sa.Text(), nullable=True),
        sa.Column("answers", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_assessment_results_id", "assessment_results", ["id"])

    op.create_table(
        "universities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("website", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("ranking", sa.Integer(), nullable=True),
        sa.Column("tuition_min_usd", sa.Integer(), nullable=True),
        sa.Column("tuition_max_usd", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_universities_id", "universities", ["id"])
    op.create_index("ix_universities_name", "universities", ["name"])
    op.create_index("ix_universities_country", "universities", ["country"])

    op.create_table(
        "majors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("university_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("degree_level", sa.String(), nullable=False),
        sa.Column("language", sa.String(), nullable=False),
        sa.Column("tuition_usd", sa.Integer(), nullable=True),
        sa.Column("duration_years", sa.Float(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["university_id"], ["universities.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_majors_id", "majors", ["id"])
    op.create_index("ix_majors_name", "majors", ["name"])
    op.create_index("ix_majors_category", "majors", ["category"])

    op.create_table(
        "user_university_choices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("university_id", sa.Integer(), nullable=False),
        sa.Column("major_id", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["major_id"], ["majors.id"]),
        sa.ForeignKeyConstraint(["university_id"], ["universities.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_university_choices_id", "user_university_choices", ["id"])
    op.create_index("ix_user_university_choices_user_id", "user_university_choices", ["user_id"])

    op.create_table(
        "match_actions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("target_user_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("match_score", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["target_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_match_actions_id", "match_actions", ["id"])
    op.create_index("ix_match_actions_user_id", "match_actions", ["user_id"])
    op.create_index("ix_match_actions_target_user_id", "match_actions", ["target_user_id"])

    op.create_table(
        "roadmaps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("target_major", sa.String(), nullable=False),
        sa.Column("target_country", sa.String(), nullable=False),
        sa.Column("roadmap_title", sa.String(), nullable=False),
        sa.Column("roadmap_summary", sa.Text(), nullable=True),
        sa.Column("duration_months", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_roadmaps_id", "roadmaps", ["id"])
    op.create_index("ix_roadmaps_user_id", "roadmaps", ["user_id"])

    op.create_table(
        "roadmap_steps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("roadmap_id", sa.Integer(), nullable=False),
        sa.Column("month_number", sa.Integer(), nullable=False),
        sa.Column("week_number", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("tasks", sa.JSON(), nullable=True),
        sa.Column("xp_reward", sa.Integer(), nullable=True),
        sa.Column("is_completed", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["roadmap_id"], ["roadmaps.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_roadmap_steps_id", "roadmap_steps", ["id"])
    op.create_index("ix_roadmap_steps_roadmap_id", "roadmap_steps", ["roadmap_id"])

    op.create_table(
        "user_gamification",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("total_xp", sa.Integer(), nullable=True),
        sa.Column("level", sa.Integer(), nullable=True),
        sa.Column("current_streak", sa.Integer(), nullable=True),
        sa.Column("longest_streak", sa.Integer(), nullable=True),
        sa.Column("last_active_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_user_gamification_id", "user_gamification", ["id"])

    op.create_table(
        "achievements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("xp_reward", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_achievements_id", "achievements", ["id"])
    op.create_index("ix_achievements_code", "achievements", ["code"], unique=True)

    op.create_table(
        "user_achievements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("achievement_id", sa.Integer(), nullable=False),
        sa.Column("unlocked_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["achievement_id"], ["achievements.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_user_achievements_id", "user_achievements", ["id"])
    op.create_index("ix_user_achievements_user_id", "user_achievements", ["user_id"])


def downgrade() -> None:
    op.drop_table("user_achievements")
    op.drop_table("achievements")
    op.drop_table("user_gamification")
    op.drop_table("roadmap_steps")
    op.drop_table("roadmaps")
    op.drop_table("match_actions")
    op.drop_table("user_university_choices")
    op.drop_table("majors")
    op.drop_table("universities")
    op.drop_table("assessment_results")
    op.drop_table("profiles")
    op.drop_table("users")
