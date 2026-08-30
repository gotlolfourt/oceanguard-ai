from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models import (
    AIModel,
    Alert,
    Camera,
    CleanupMission,
    Detection,
    DetectionClass,
    Device,
    Media,
    MonitoringZone,
    Organization,
    ProcessingJob,
    Role,
    Track,
    TrackPoint,
    User,
)


def _create_roles(db: Session) -> dict[str, Role]:
    roles = {
        "admin": {"manage_users": True},
        "environmental_officer": {"view_alerts": True},
        "field_operator": {"monitor_devices": True},
        "cleanup_team": {"execute_missions": True},
    }
    out = {}
    for name, permissions in roles.items():
        role = db.query(Role).filter(Role.name == name).first()
        if role is None:
            role = Role(name=name, permissions=permissions)
            db.add(role)
            db.flush()
        out[name] = role
    return out


def seed_database(db: Session) -> None:
    if db.query(User).first():
        return

    roles = _create_roles(db)

    org = Organization(name="OceanGuard Inc", location="Pacific Coast")
    db.add(org)
    db.flush()

    demo_users = [
        ("admin@oceanguard.com", "Admin", "User", "admin"),
        ("officer@oceanguard.com", "Env", "Officer", "environmental_officer"),
        ("operator@oceanguard.com", "Field", "Operator", "field_operator"),
        ("cleanup@oceanguard.com", "Cleanup", "Team", "cleanup_team"),
    ]
    users = []
    for email, first, last, role_name in demo_users:
        user = User(
            email=email,
            password_hash=hash_password("password123"),
            first_name=first,
            last_name=last,
            role_id=roles[role_name].id,
            organization_id=org.id,
            is_active=True,
        )
        db.add(user)
        users.append(user)
    db.flush()

    devices = [
        Device(name="Harbor Camera 1", type="camera", location={"lat": 37.7, "lng": -122.4}, status="active", organization_id=org.id),
        Device(name="Harbor Camera 2", type="camera", location={"lat": 37.71, "lng": -122.38}, status="active", organization_id=org.id),
        Device(name="Survey Drone A", type="drone", location={"lat": 37.72, "lng": -122.39}, status="inactive", organization_id=org.id),
    ]
    db.add_all(devices)
    db.flush()

    cameras = [
        Camera(device_id=devices[0].id, rtsp_url="rtsp://camera1", http_url="http://camera1", resolution="1920x1080", fps=30, status="active"),
        Camera(device_id=devices[1].id, rtsp_url="rtsp://camera2", http_url="http://camera2", resolution="1280x720", fps=24, status="active"),
    ]
    db.add_all(cameras)
    db.flush()

    zones = [
        MonitoringZone(name="North Bay", geometry={"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [0, 0]]]}, priority_level="high", organization_id=org.id),
        MonitoringZone(name="South Bay", geometry={"type": "Polygon", "coordinates": [[[1, 1], [1, 2], [2, 2], [1, 1]]]}, priority_level="medium", organization_id=org.id),
    ]
    db.add_all(zones)

    classes = [
        ("plastic", "#3b82f6", 0.7),
        ("bottle", "#0ea5e9", 0.5),
        ("net", "#f97316", 0.9),
        ("rope", "#f59e0b", 0.8),
        ("metal", "#94a3b8", 0.6),
        ("glass", "#10b981", 0.4),
        ("wood", "#a16207", 0.3),
        ("mixed", "#8b5cf6", 0.85),
        ("unknown", "#6b7280", 0.2),
    ]
    detection_classes = [DetectionClass(name=name, color_hex=color, risk_factor=risk) for name, color, risk in classes]
    db.add_all(detection_classes)
    db.flush()

    detections = []
    for i in range(10):
        detections.append(
            Detection(
                detection_class_id=detection_classes[i % len(detection_classes)].id,
                confidence=0.55 + (i * 0.03),
                bbox_coords={"x": 10 + i, "y": 20 + i, "w": 120, "h": 80},
                camera_id=cameras[i % len(cameras)].id,
            )
        )
    db.add_all(detections)
    db.flush()

    tracks = []
    for i in range(5):
        track = Track(device_id=devices[i % len(devices)].id, status="active")
        db.add(track)
        db.flush()
        tracks.append(track)
        db.add(TrackPoint(track_id=track.id, detection_id=detections[i].id, position={"lat": 37.7 + i * 0.01, "lng": -122.4 + i * 0.01}))

    alerts = [
        Alert(detection_id=detections[0].id, status="new", risk_level="high"),
        Alert(detection_id=detections[1].id, status="acknowledged", risk_level="medium"),
        Alert(detection_id=detections[2].id, status="resolved", risk_level="critical"),
    ]
    db.add_all(alerts)
    db.flush()

    missions = [
        CleanupMission(alert_id=alerts[0].id, status="planned", assigned_to=users[3].id, priority="high"),
        CleanupMission(alert_id=alerts[1].id, status="in_progress", assigned_to=users[3].id, priority="medium"),
    ]
    db.add_all(missions)

    model = AIModel(name="MockYOLO", version="1.0.0", model_type="detection", accuracy=0.87, deployment_status="active")
    db.add(model)
    db.flush()

    media = Media(type="image", url="https://example.com/sample.jpg", size=2048, duration=None, organization_id=org.id)
    db.add(media)
    db.flush()

    db.add(ProcessingJob(media_id=media.id, model_id=model.id, status="completed", result={"detections": 2}))

    db.commit()
