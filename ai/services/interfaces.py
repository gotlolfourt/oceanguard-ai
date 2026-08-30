from abc import ABC, abstractmethod
from typing import Any


class DetectionService(ABC):
    @abstractmethod
    async def detect(self, image: bytes) -> list[dict[str, Any]]:
        raise NotImplementedError


class ClassificationService(ABC):
    @abstractmethod
    async def classify(self, detections: list[dict[str, Any]]) -> list[dict[str, Any]]:
        raise NotImplementedError


class TrackingService(ABC):
    @abstractmethod
    async def track(self, detections: list[dict[str, Any]]) -> list[dict[str, Any]]:
        raise NotImplementedError
