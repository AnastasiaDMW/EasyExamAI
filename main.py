import shutil
import os

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from agents.orchestrator_agent import orchestrator
from models.question import Question
from monitoring.middleware import metrics_middleware
from prometheus_client import generate_latest
from fastapi.responses import Response
from monitoring.logger import logger

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title="EasyExamAI",
    description="Multi-agent AI system for exam preparation",
    version="1.0.0"
)

app.middleware("http")(metrics_middleware)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.post("/ask")
def ask(data: Question):
    logger.info(f"API /ask received question: {data.question}")
    result = orchestrator(user_input=data.question)

    return {
        "task": result["task"],
        "agent": result["agent"],
        "response": result["response"]
    }

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    logger.info(f"Uploading file: {file.filename}")
    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = orchestrator(
        task="DOCUMENT",
        payload=path
    )

    return result