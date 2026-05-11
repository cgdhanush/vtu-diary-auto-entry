import { useEffect, useState } from "react";
import LoginForm from "./components/LoginForm";
import EntryGenerator from "./components/EntryGenerator";
import EntriesBox, { type Entry } from "./components/EntriesBox";
import apiClient from "./service/apiClient";
import "./App.css";


function App() {
  const [message, setMessage] = useState("");
  const [entries, setEntries] = useState<Entry[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchEntries = async () => {
      try {
        const res = await apiClient.get("/entries");
        setEntries(res.data || []);
      } catch (err: any) {
        console.log("Failed to fetch entries:", err);
      }
    };

    fetchEntries();
  }, []);

  const handleRunBot = async () => {
    try {
      setLoading(true);

      const response = await apiClient.post("/run-bot");

      setMessage(response.data.message || "Bot executed successfully");
      setEntries(response.data.entries || []);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || "Bot failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>VTU Diary Auto Entry</h1>

      {/* Top section */}
      <div className="top-section">
        <LoginForm setMessage={setMessage} />

        <EntryGenerator setMessage={setMessage} setEntries={setEntries} />
      </div>

      {/* 🔥 RUN BOT BUTTON (separate) */}
      <div className="runbot-container">
        <button className="run-btn" onClick={handleRunBot} disabled={loading}>
          {loading ? "Running Bot..." : "🚀 Run Bot"}
        </button>
      </div>

      {message && <div className="message-box">{message}</div>}

      <EntriesBox entries={entries} />
    </div>
  );
}

export default App;
