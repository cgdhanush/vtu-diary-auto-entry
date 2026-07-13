import { useState } from "react";
import apiClient from "../service/apiClient";
import axios from "axios";

interface Props {
  setMessage: (msg: string) => void;
}

function OpenRouterApiKeyForm({ setMessage }: Props) {
  const [apiKey, setApiKey] = useState(
    () => localStorage.getItem("openrouter-api-key") || ""
  );
  const [error, setError] = useState<string | null>(null);

  const handleSaveApiKey = async () => {
    if (!apiKey.trim()) {
      setError("Please enter your OpenRouter API key.");
      return;
    }

    try {
      // Save in browser for future use
      localStorage.setItem("openrouter-api-key", apiKey.trim());

      // Save in backend (optional)
      await apiClient.post("/api-key", {
        api_key: apiKey.trim(),
      });

      setError(null);
      setMessage("OpenRouter API key saved successfully.");
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.detail || "Failed to save API key.");
      } else {
        setError("Failed to save API key.");
      }
    }
  };

  return (
    <div className="form-section">
      <h2>OpenRouter API Key</h2>

      <input
        type="password"
        placeholder="Enter OpenRouter API Key"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
        autoComplete="off"
      />

      <button onClick={handleSaveApiKey}>Save API Key</button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default OpenRouterApiKeyForm;