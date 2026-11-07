import os
import tempfile
from pathlib import Path

from basic_pitch.inference import predict


def midi_to_note_name(midi_pitch: int) -> str:
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = (midi_pitch // 12) - 1
    return f"{note_names[midi_pitch % 12]}{octave}"


def note_name_to_midi(note_name: str) -> int:
    note_map = {
        "C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5,
        "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11
    }

    value = note_name[:-1]
    octave = int(note_name[-1])

    return note_map[value] + (octave + 1) * 12


def save_basic_pitch_midi(midi_data, stem: str) -> str:
    output_dir = Path(tempfile.gettempdir()) / "orpheus_transcriber"
    output_dir.mkdir(parents=True, exist_ok=True)

    midi_path = output_dir / f"{stem}_transcribed.mid"

    if hasattr(midi_data, "write"):
        try:
            midi_data.write(str(midi_path))
            return str(midi_path)
        except Exception:
            pass

    if hasattr(midi_data, "save"):
        try:
            midi_data.save(str(midi_path))
            return str(midi_path)
        except Exception:
            pass

    raise TypeError("Unsupported Basic Pitch MIDI object. The library returned an unexpected MIDI structure.")


def extract_notes_from_basic_pitch(note_events) -> list:
    if not note_events:
        return []

    notes = []

    for event in note_events:
        try:
            pitch = getattr(event, "pitch", None)
            start = getattr(event, "start", None)
            end = getattr(event, "end", None)
            velocity = getattr(event, "velocity", 100)

            if pitch is None or start is None or end is None:
                continue

            notes.append({
                "pitch": midi_to_note_name(int(pitch)),
                "midi_pitch": int(pitch),
                "onset": round(float(start), 3),
                "duration": round(float(end - start), 3),
                "velocity": int(velocity),
            })
        except Exception:
            continue

    return notes


async def transcribe(file):
    original_filename = file.filename or "audio.wav"
    stem = Path(original_filename).stem or "audio"
    suffix = Path(original_filename).suffix or ".wav"

    temp_path = None

    try:
        content = await file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name

        _, midi_data, note_events = predict(temp_path)

        midi_path = save_basic_pitch_midi(midi_data, stem)
        midi_filename = Path(midi_path).name

        notes = extract_notes_from_basic_pitch(note_events)

        return {
            "status": "success",
            "filename": original_filename,
            "midi_filename": midi_filename,
            "midi_url": f"/api/download/{midi_filename}",
            "instrument": "basic_pitch",
            "notes": notes,
            "message": "Audio transcription completed",
        }

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)