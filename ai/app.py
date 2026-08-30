from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

from services.factory import get_classification_service, get_detection_service, get_tracking_service

app = FastAPI(title="OceanGuard AI Service", description="Detection and Classification Engine", version="0.1.0")


def success_response(data: object, status: int = 200):
    return {"data": data, "status": status}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "oceanguard-ai"}


@app.get("/")
async def root():
    return {"message": "OceanGuard AI Service v0.1.0"}


@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    image_bytes = await file.read()
    detections = await get_detection_service().detect(image_bytes)
    return success_response({"detections": detections})


class DetectionPayload(BaseModel):
    detections: list[dict]


@app.post("/classify")
async def classify(payload: DetectionPayload):
    classifications = await get_classification_service().classify(payload.detections)
    return success_response({"classifications": classifications})


@app.post("/track")
async def track(payload: DetectionPayload):
    tracks = await get_tracking_service().track(payload.detections)
    return success_response({"tracks": tracks})
