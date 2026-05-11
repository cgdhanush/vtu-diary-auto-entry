import { useState } from "react";
import apiClient from "../service/apiClient";
import axios from "axios";
import type { Entry } from "./EntriesBox";

interface Props {
  setMessage: (msg: string) => void;
  setEntries: (entries: Entry[]) => void;
}

type Mode = "range" | "list";

interface GenerateRequest {
  domain: string;
  mode: Mode;
  start_date?: string;
  end_date?: string;
  dates?: string[];
  skills?: string[];
}

function EntryGenerator({ setMessage, setEntries }: Props) {
  const [domain, setDomain] = useState("");
  const [mode, setMode] = useState<Mode>("range");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [dates, setDates] = useState("");
  const [skills, setSkills] = useState("");

  const handleGenerate = async () => {
    try {
      const requestData: GenerateRequest = {
        domain,
        mode,
      };

      if (mode === "range") {
        requestData.start_date = startDate;
        requestData.end_date = endDate;
      } else {
        requestData.dates = dates
          .split(",")
          .map((d) => d.trim())
          .filter(Boolean);
      }

      if (skills.trim()) {
        requestData.skills = skills
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean);
      }

      const response = await apiClient.post("/generate", requestData);

      setMessage(response.data.message);
      setEntries(response.data.entries);
    } catch (err: unknown) {
      let message = "Generation failed";

      if (axios.isAxiosError(err)) {
        message = err.response?.data?.detail || message;
      } else if (err instanceof Error) {
        message = err.message;
      }

      setMessage(message);
    }
  };

  return (
    <div className="form-section">
      <h2>Generate Entries</h2>

      <input
        type="text"
        placeholder="Internship Domain"
        value={domain}
        onChange={(e) => setDomain(e.target.value)}
      />

      <select
        value={mode}
        onChange={(e) => setMode(e.target.value as Mode)}
      >
        <option value="range">Date Range</option>
        <option value="list">Date List</option>
      </select>

      {mode === "range" ? (
        <>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />

          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </>
      ) : (
        <input
          type="text"
          placeholder="YYYY-MM-DD, comma separated"
          value={dates}
          onChange={(e) => setDates(e.target.value)}
        />
      )}

      <input
        type="text"
        placeholder="Skills (comma separated)"
        value={skills}
        onChange={(e) => setSkills(e.target.value)}
      />

      <button onClick={handleGenerate}>Generate Entries</button>
    </div>
  );
}

export default EntryGenerator;