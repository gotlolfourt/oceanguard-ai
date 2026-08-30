from config import settings
from services.mock_services import MockClassificationService, MockDetectionService, MockTrackingService


def get_detection_service():
    # Placeholder for future real implementation selection.
    if settings.USE_MOCK_MODE:
        return MockDetectionService()
    return MockDetectionService()


def get_classification_service():
    if settings.USE_MOCK_MODE:
        return MockClassificationService()
    return MockClassificationService()


def get_tracking_service():
    if settings.USE_MOCK_MODE:
        return MockTrackingService()
    return MockTrackingService()
