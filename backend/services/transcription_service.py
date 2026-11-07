import os
import tempfile

from basic_pitch.inference import predict


def midi_to_note_name(midi_pitch: int) -> str:
    note_names = ["C", "C#", "D", "D#", "E", "F",
                  "F#", "G", "G#", "A", "A#", "B"]
    octave = (midi_pitch // 12) - 1
    return f"{note_names[midi_pitch % 12]}{octave}"


async def transcribe(file):
    filename = file.filename or "audio.wav"
    suffix = os.path.splitext(filename)[1] or ".wav"
    temp_path = None

    try:
        content = await file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name

        _, midi_data, _ = predict(temp_path)

        notes = []
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                notes.append({
                    "pitch": midi_to_note_name(note.pitch),
                    "midi_pitch": int(note.pitch),
                    "onset": round(float(note.start), 3),
                    "duration": round(float(note.end - note.start), 3),
                    "velocity": int(note.velocity),
                })

        return {
            "status": "success",
            "filename": filename,
            "instrument": "basic_pitch",
            "notes": notes,
            "message": "Audio transcription completed",
        }

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)