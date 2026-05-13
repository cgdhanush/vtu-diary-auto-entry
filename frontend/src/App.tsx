import { useCallback, useEffect, useState } from "react";
import LoginForm from "./components/LoginForm";
import EntryGenerator from "./components/EntryGenerator";
import EntriesBox, { type Entry } from "./components/EntriesBox";
import apiClient from "./service/apiClient";
import "./App.css";
import Navbar from "./components/Navbar";

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
  const [isBotRunning, setIsBotRunning] = useState(false);

  // LOGIN STATE
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!sessionStorage.getItem("x-user-email"),
  );

  // FETCH ENTRIES ON LOAD
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

  // FETCH RESULTS
  const fetchResult = useCallback(async () => {
    try {
      const res = await apiClient.get("/results");

      setResults(res.data || []);

      // stop polling if completed
      if (res.data?.status === "completed") {
        setIsBotRunning(false);
        setLoading(false);
      }
    } catch (err) {
      console.log("Failed to fetch results:", err);
    }
  }, []);

  // RUN BOT
  const handleRunBot = async () => {
    // LOGIN CHECK
    if (!isLoggedIn) {
      setMessage("Please login first");
      return;
    }

    try {
      setLoading(true);
      setShowResults(true);
      setMessage("");

      const response = await apiClient.post("/run-bot");

      setMessage(response.data.message || "Bot executed successfully");

      // START POLLING
      setIsBotRunning(true);

      // INITIAL FETCH
      fetchResult();
    } catch (error: any) {
      setMessage(error.response?.data?.detail || "Bot failed");
      setLoading(false);
    }
  };

  // POLLING
  useEffect(() => {
    if (!isBotRunning) return;

    const interval = setInterval(() => {
      fetchResult();
    }, 2000);

    return () => clearInterval(interval);
  }, [isBotRunning, fetchResult]);

  return (
    <div className="app">

      <Navbar isLoggedIn={isLoggedIn} isBotRunning={isBotRunning} />
      <h1>VTU Diary Auto Entry</h1>

      {/* TOP SECTION */}
      <div className="top-section">

        {/* LOGIN CARD */}
        <div className="section-card">
          <h2>Login</h2>

          <LoginForm
            setMessage={setMessage}
            onLoginSuccess={() => setIsLoggedIn(true)}
          />
        </div>

        {/* ENTRY GENERATOR CARD */}
        <div className="section-card">
          <h2>Generate Entries</h2>

          <EntryGenerator
            setMessage={setMessage}
            setEntries={setEntries}
            disabled={!isLoggedIn}
          />
        </div>

      </div>

      {/* RUN BOT */}
      <div className="runbot-container">
        <button
          className="run-btn"
          onClick={handleRunBot}
          disabled={loading}
        >
          {loading ? "Running Bot..." : "🚀 Run Bot"}
        </button>

        {/* PROGRESS BAR */}
        {loading && (
          <div className="progress-wrapper">
            <div className="progress-bar"></div>
          </div>
        )}
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