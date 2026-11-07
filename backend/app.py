import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.services.transcription_service import transcribe as run_transcription


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
    instrument: str = Form(...),
):
    return await run_transcription(file)


@app.get("/api/download/{filename}")
async def download_midi(filename: str):
    safe_filename = Path(filename).name

    if safe_filename != filename or not safe_filename.lower().endswith(".mid"):
        raise HTTPException(status_code=400, detail="Invalid MIDI filename")

    midi_path = Path(tempfile.gettempdir()) / "orpheus_transcriber" / safe_filename

    if not midi_path.is_file():
        raise HTTPException(status_code=404, detail="MIDI file not found")

    return FileResponse(
        path=midi_path,
        media_type="audio/midi",
        filename=safe_filename,
    )