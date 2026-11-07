import { useState } from "react";

export default function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("instrument", "piano");

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/api/transcribe", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        setResult({ error: data.detail || "Transcription failed" });
        return;
      }

      setResult(data);
    } catch (error) {
      console.error("Upload failed:", error);
      setResult({ error: "Request failed. Check that the backend is running." });
    } finally {
      setLoading(false);
    }
  };

  const midiUrl = result?.midi_url
    ? `http://localhost:8000${result.midi_url}`
    : null;

  return (
    <div
      style={{
        padding: 32,
        fontFamily: "sans-serif",
        maxWidth: 700,
        margin: "0 auto",
      }}
    >
      <h2>AI Audio Transcription</h2>

      <div style={{ marginTop: 20 }}>
        <strong>Instrument:</strong> piano
      </div>

      <div style={{ marginTop: 20 }}>
        <input
          type="file"
          accept=".mp3,.wav,.m4a"
          onChange={(event) => setFile(event.target.files?.[0] || null)}
        />
      </div>

      <button
        onClick={handleSubmit}
        disabled={loading || !file}
        style={{
          marginTop: 20,
          padding: "10px 18px",
          cursor: loading || !file ? "not-allowed" : "pointer",
        }}
      >
        {loading ? "Processing..." : "Transcribe"}
      </button>

      {midiUrl && (
        <div style={{ marginTop: 20 }}>
          <a href={midiUrl} download>
            Скачать MIDI
          </a>
        </div>
      )}

      {result && (
        <div style={{ marginTop: 30 }}>
          <h3>Result</h3>
          <pre
            style={{
              background: "#f4f4f4",
              padding: 12,
              overflow: "auto",
            }}
          >
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}