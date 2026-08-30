from fastapi import FastAPI, UploadFile, File

app = FastAPI(
    title="OceanGuard AI Service",
    description="Detection and Classification Engine",
    version="0.1.0",
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "oceanguard-ai"}

@app.get("/")
async def root():
    return {"message": "OceanGuard AI Service v0.1.0"}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    return {"detections": [], "confidence": 0.0}

@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    return {"classifications": [], "primary_class": None}