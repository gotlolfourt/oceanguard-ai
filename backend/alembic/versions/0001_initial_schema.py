"""Initial OceanGuard schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-08-30
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("roles", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(length=64), nullable=False), sa.Column("permissions", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_index("ix_roles_name", "roles", ["name"], unique=True)

    op.create_table("organizations", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(length=255), nullable=False), sa.Column("location", sa.String(length=255)), sa.Column("created_at", sa.DateTime(), nullable=False))

    op.create_table("users", sa.Column("id", sa.String(length=36), primary_key=True), sa.Column("email", sa.String(length=255), nullable=False), sa.Column("password_hash", sa.String(length=255), nullable=False), sa.Column("first_name", sa.String(length=120), nullable=False), sa.Column("last_name", sa.String(length=120), nullable=False), sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False), sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False))
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table("devices", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(length=255), nullable=False), sa.Column("type", sa.String(length=32), nullable=False), sa.Column("location", sa.JSON()), sa.Column("status", sa.String(length=32), nullable=False), sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("cameras", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("device_id", sa.Integer(), sa.ForeignKey("devices.id"), nullable=False), sa.Column("rtsp_url", sa.Text()), sa.Column("http_url", sa.Text()), sa.Column("resolution", sa.String(length=64)), sa.Column("fps", sa.Integer()), sa.Column("status", sa.String(length=32), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_unique_constraint("uq_cameras_device_id", "cameras", ["device_id"])

    op.create_table("monitoring_zones", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(length=255), nullable=False), sa.Column("geometry", sa.JSON(), nullable=False), sa.Column("priority_level", sa.String(length=32), nullable=False), sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))

    op.create_table("detection_classes", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(length=64), nullable=False), sa.Column("color_hex", sa.String(length=7), nullable=False), sa.Column("risk_factor", sa.Float(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_unique_constraint("uq_detection_classes_name", "detection_classes", ["name"])

    op.create_table("detections", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("detection_class_id", sa.Integer(), sa.ForeignKey("detection_classes.id"), nullable=False), sa.Column("confidence", sa.Float(), nullable=False), sa.Column("bbox_coords", sa.JSON(), nullable=False), sa.Column("camera_id", sa.Integer(), sa.ForeignKey("cameras.id"), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("processed_at", sa.DateTime()))

    op.create_table("tracks", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("device_id", sa.Integer(), sa.ForeignKey("devices.id"), nullable=False), sa.Column("status", sa.String(length=32), nullable=False), sa.Column("start_time", sa.DateTime(), nullable=False), sa.Column("end_time", sa.DateTime()), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("track_points", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("track_id", sa.Integer(), sa.ForeignKey("tracks.id"), nullable=False), sa.Column("detection_id", sa.Integer(), sa.ForeignKey("detections.id"), nullable=False), sa.Column("position", sa.JSON(), nullable=False), sa.Column("timestamp", sa.DateTime(), nullable=False))

    op.create_table("alerts", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("detection_id", sa.Integer(), sa.ForeignKey("detections.id"), nullable=False), sa.Column("status", sa.String(length=32), nullable=False), sa.Column("risk_level", sa.String(length=32), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("acknowledged_at", sa.DateTime()))
    op.create_table("cleanup_missions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("alert_id", sa.Integer(), sa.ForeignKey("alerts.id"), nullable=False), sa.Column("status", sa.String(length=32), nullable=False), sa.Column("assigned_to", sa.String(length=36), sa.ForeignKey("users.id")), sa.Column("priority", sa.String(length=32), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("completed_at", sa.DateTime()))
    op.create_table("cleanup_evidence", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("mission_id", sa.Integer(), sa.ForeignKey("cleanup_missions.id"), nullable=False), sa.Column("photo_url", sa.Text(), nullable=False), sa.Column("notes", sa.Text()), sa.Column("created_at", sa.DateTime(), nullable=False))

    op.create_table("ai_models", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(length=255), nullable=False), sa.Column("version", sa.String(length=64), nullable=False), sa.Column("model_type", sa.String(length=64), nullable=False), sa.Column("accuracy", sa.Float(), nullable=False), sa.Column("deployment_status", sa.String(length=64), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))

    op.create_table("media", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("type", sa.String(length=32), nullable=False), sa.Column("url", sa.Text(), nullable=False), sa.Column("size", sa.Integer(), nullable=False), sa.Column("duration", sa.Float()), sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))

    op.create_table("processing_jobs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("media_id", sa.Integer(), sa.ForeignKey("media.id"), nullable=False), sa.Column("model_id", sa.Integer(), sa.ForeignKey("ai_models.id"), nullable=False), sa.Column("status", sa.String(length=32), nullable=False), sa.Column("result", sa.JSON()), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("completed_at", sa.DateTime()))


def downgrade() -> None:
    for table in [
        "processing_jobs",
        "media",
        "ai_models",
        "cleanup_evidence",
        "cleanup_missions",
        "alerts",
        "track_points",
        "tracks",
        "detections",
        "detection_classes",
        "monitoring_zones",
        "cameras",
        "devices",
        "users",
        "organizations",
        "roles",
    ]:
        op.drop_table(table)
