from datetime import datetime, timezone
from random import Random

from .interfaces import ClassificationService, DetectionService, TrackingService

_rng = Random(42)


class MockDetectionService(DetectionService):
    async def detect(self, image: bytes) -> list[dict]:
        size_factor = max(1, min(3, len(image) // 1024 + 1))
        detections = []
        for idx in range(size_factor):
            detections.append(
                {
                    "id": idx + 1,
                    "class_name": ["plastic", "bottle", "net"][idx % 3],
                    "confidence": round(0.64 + (_rng.random() * 0.3), 2),
                    "bbox_coords": {"x": 20 + idx * 30, "y": 25 + idx * 20, "w": 120, "h": 90},
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            )
        return detections


class MockClassificationService(ClassificationService):
    async def classify(self, detections: list[dict]) -> list[dict]:
        return [
            {
                "detection_id": detection["id"],
                "debris_type": detection["class_name"],
                "risk_level": "high" if detection["confidence"] > 0.8 else "medium",
            }
            for detection in detections
        ]


class MockTrackingService(TrackingService):
    async def track(self, detections: list[dict]) -> list[dict]:
        return [
            {
                "track_id": detection["id"],
                "status": "active",
                "path": [{"x": detection["bbox_coords"]["x"], "y": detection["bbox_coords"]["y"]}],
            }
            for detection in detections
        ]
