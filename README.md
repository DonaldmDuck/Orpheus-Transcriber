AI Audio Transcription MVP

This project is a small full-stack application for uploading an audio file and receiving a transcription-style result. It is designed as an MVP to test the full flow: upload, process, and return structured output.

What it does:

Frontend lets the user choose an audio file
Backend accepts the file through an API
The app returns a JSON response with transcription-like notes
The current version works with piano only
The response is mocked for now, but the app structure is ready for a real transcription model later
Stack:

Frontend: React + Vite
Backend: FastAPI
Languages: Python, JavaScript
Project structure: project-root/ ├── backend/ │ └── app.py ├── frontend/ │ ├── src/ │ ├── package.json │ └── ... ├── README.md ├── requirements.txt └── .gitignore

How to run:

Backend: From the project root: uvicorn app:app --reload

If the backend is stored in a backend folder: uvicorn backend.app:app --reload

Frontend: From the frontend folder: npm install npm run dev

Then open: http://localhost:5173

API: POST /api/transcribe

This endpoint accepts:

an audio file
instrument = piano
Example response: { "status": "success", "filename": "example.mp3", "instrument": "piano", "notes": [ { "pitch": "C4", "duration": 0.5 }, { "pitch": "E4", "duration": 0.5 }, { "pitch": "G4", "duration": 0.5 } ] }

Current status: This is a working MVP version. It demonstrates:

file upload flow
frontend-backend communication
structured result handling
The next step is to replace the mocked notes with a real transcription model.

Future improvements:

real AI transcription
support for more instruments
improved UI
better error handling
tests
deployment
Notes: This project is intended as a working prototype for demonstration and further development.
