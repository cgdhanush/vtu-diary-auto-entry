import {
  FaGithub,
  FaRocket,
  FaUserCircle,
  FaRobot,
} from "react-icons/fa";

import "./NavBar.css"

interface Props {
  isLoggedIn: boolean;
  isBotRunning: boolean;
}

function Navbar({ isLoggedIn, isBotRunning }: Props) {
  return (
    <nav className="navbar">

      {/* LEFT - APP NAME */}
      <div className="nav-left">
        <h2>VTU Diary Auto Entry</h2>
      </div>

      {/* CENTER - STATUS */}
      <div className="nav-center">

        {/* LOGIN STATUS */}
        <div className={`status-box ${isLoggedIn ? "ok" : "bad"}`}>
          <FaUserCircle />
          <span>{isLoggedIn ? "Logged In" : "Not Logged In"}</span>
        </div>

        {/* BOT STATUS */}
        <div className={`status-box ${isBotRunning ? "run" : "idle"}`}>
          <FaRobot />
          <span>{isBotRunning ? "Bot Running" : "Idle"}</span>
        </div>

      </div>

      {/* RIGHT - ACTIONS */}
      <div className="nav-right">

        <a
          href="https://github.com/cgdhanush/vtu-diary-auto-entry.git"
          target="_blank"
          rel="noreferrer"
          className="icon-btn"
        >
          <FaGithub />
        </a>

        <a
          href="https://github.com/cgdhanush/vtu-diary-auto-entry.git"
          target="_blank"
          rel="noreferrer"
          className="start-btn"
        >
          <FaRocket /> Start Project
        </a>

      </div>

    </nav>
  );
}

export default Navbar;