from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Orpheus Transcriber")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.services.audio_service import read_audio_upload

app = FastAPI(title="Orpheus Transcriber")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    instrument: str = Form(...)
):
    content = await read_audio_upload(file)

    return {
        "status": "success",
        "filename": file.filename,
        "instrument": instrument,
        "notes": [
            {"pitch": "C4", "duration": 0.5},
            {"pitch": "E4", "duration": 0.5},
            {"pitch": "G4", "duration": 0.5},
        ],
        "message": "Mock transcription result"
    }