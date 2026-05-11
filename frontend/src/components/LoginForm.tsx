import { useState } from "react";
import apiClient from "../service/apiClient";
import axios from "axios";

interface Props {
  setMessage: (msg: string) => void;
}

function LoginForm({ setMessage }: Props) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async () => {
    try {
      const response = await apiClient.post("/login", {
        email,
        password,
      });

      setMessage(response.data.message);
      setError(null);
    } catch (err: unknown) {
      let message = "Login failed";

      if (axios.isAxiosError(err)) {
        message = err.response?.data?.detail || message;
      } else if (err instanceof Error) {
        message = err.message;
      }

      setError(message);
      setMessage(message);
    }
  };

  return (
    <div className="form-section">
      <h2>Login</h2>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleLogin}>Login</button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default LoginForm;