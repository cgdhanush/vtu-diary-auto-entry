import { useEffect, useState } from "react";
import LoginForm from "./components/LoginForm";
import EntryGenerator from "./components/EntryGenerator";
import EntriesBox, { type Entry } from "./components/EntriesBox";
import apiClient from "./service/apiClient";
import "./App.css";

type Result = {
  date: string;
  internship: string;
  status: string;
};

function App() {
  const [message, setMessage] = useState("");
  const [entries, setEntries] = useState<Entry[]>([]);
  const [results, setResults] = useState<Result[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [loading, setLoading] = useState(false);

  // LOGIN STATE
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!sessionStorage.getItem("x-user-email"),
  );

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
    if (!isLoggedIn) return;

    try {
      setLoading(true);
      setShowResults(true);

      const response = await apiClient.post("/run-bot");

      setMessage(response.data.message || "Bot executed successfully");
      setResults(response.data.results || []);
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
        <LoginForm
          setMessage={setMessage}
          onLoginSuccess={() => setIsLoggedIn(true)}
        />

        <EntryGenerator
          setMessage={setMessage}
          setEntries={setEntries}
          disabled={!isLoggedIn}
        />
      </div>

      {/* RUN BOT BUTTON */}
      <div className="runbot-container">
        <button
          className="run-btn"
          onClick={handleRunBot}
          disabled={!isLoggedIn || loading}
        >
          {loading ? "Running Bot..." : "🚀 Run Bot"}
        </button>
      </div>

      {/* RESULTS */}
      {showResults && (
        <div className="results-container">
          <h2>Bot Results</h2>

          {results.length === 0 ? (
            <p>No results yet.</p>
          ) : (
            results.map((res, index) => (
              <div key={index} className="result-card">
                <p>
                  <strong>Date:</strong> {res.date}
                </p>
                <p>
                  <strong>Internship:</strong> {res.internship}
                </p>
                <p>
                  <strong>Status:</strong> {res.status}
                </p>
              </div>
            ))
          )}
        </div>
      )}

      {/* MESSAGE */}
      {message && <div className="message-box">{message}</div>}

      {/* ENTRIES */}
      <EntriesBox entries={entries} />
    </div>
  );
}

export default App;
