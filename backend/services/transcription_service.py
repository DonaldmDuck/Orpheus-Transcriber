import os
import tempfile
from pathlib import Path

from basic_pitch.inference import predict
import mido
from mido import MidiFile, MidiTrack, Message


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

    midi = note_map[value] + (octave + 1) * 12
    return midi


def generate_midi_file(notes: list, filename: str) -> str:
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    for note in notes:
        note_name = note["pitch"]
        midi_pitch = note["midi_pitch"]

        if isinstance(note_name, str):
            midi_pitch = note_name_to_midi(note_name)

        velocity = int(note.get("velocity", 100))
        onset = float(note.get("onset", 0.0))
        duration = float(note.get("duration", 0.5))

        start_ticks = int(onset * 480)
        end_ticks = int((onset + duration) * 480)

        track.append(Message("note_on", note=midi_pitch, velocity=velocity, time=start_ticks))
        track.append(Message("note_off", note=midi_pitch, velocity=0, time=end_ticks - start_ticks))

    output_dir = Path(tempfile.gettempdir()) / "orpheus_transcriber"
    output_dir.mkdir(exist_ok=True)

    file_path = output_dir / filename
    mid.save(file_path)
    return str(file_path)


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
                midi_pitch = int(note.pitch)
                notes.append({
                    "pitch": midi_to_note_name(midi_pitch),
                    "midi_pitch": midi_pitch,
                    "onset": round(float(note.start), 3),
                    "duration": round(float(note.end - note.start), 3),
                    "velocity": int(note.velocity),
                })

        midi_filename = f"{os.path.splitext(filename)[0]}_transcribed.mid"
        midi_path = generate_midi_file(notes, midi_filename)

        return {
            "status": "success",
            "filename": filename,
            "midi_filename": os.path.basename(midi_path),
            "midi_url": f"/api/download/{os.path.basename(midi_path)}",
            "instrument": "basic_pitch",
            "notes": notes,
            "message": "Audio transcription completed",
        }

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)