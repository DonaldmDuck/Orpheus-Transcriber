from fastapi import HTTPException, UploadFile


ALLOWED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a"}
MAX_AUDIO_SIZE_BYTES = 25 * 1024 * 1024


async def read_audio_upload(file: UploadFile) -> bytes:
    """Validate an uploaded audio file and read it within the configured size limit."""
    filename = file.filename or ""
    extension = filename.rpartition(".")[2].lower()
    if not extension or f".{extension}" not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail="Unsupported audio format. Upload an MP3, WAV, or M4A file.",
        )

    content = await file.read(MAX_AUDIO_SIZE_BYTES + 1)
    if not content:
        raise HTTPException(status_code=400, detail="The uploaded audio file is empty.")
    if len(content) > MAX_AUDIO_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Audio file is too large. Maximum size is 25 MiB.",
        )

    return content