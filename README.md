# 🤖 VTU AI Internship Diary Automator

An AI tool that automatically generates and uploads VTU internship diary entries using OpenRouter AI.

No manual form filling. No repetitive work. Just run and relax ☕️

---

## 🚀 Quick Start (Run in 3 Steps)

### 1. Clone the repository

```bash
git clone https://github.com/cgdhanush/vtu-diary-auto-entry.git
```

### 2. Move into the project folder

```bash
cd vtu-diary-auto-entry
```

### 3. Run the application

```bash
python main.py
```

That’s it. The web server will start automatically.

Then open:

```
http://127.0.0.1:8000
```

---

## ✨ Features

* 🤖 AI-generated internship diary entries
* 📅 Custom date range generation
* 🎯 Domain-specific diary creation (Cyber Security, Web Dev, etc.)
* 🔐 Secure login using email & password
* 📤 Auto-submit multiple internship diary entries
* 🛡️ Error handling (one failure won’t stop the process)
* ⏳ Built-in delay between requests (rate-safe)
* 📊 Clean console logs for tracking progress

---

## 📦 Installation (Alternative)

If dependencies are not installed:

```bash
pip install -r requirements.txt
```

---

## 🔑 Setup

Create a `.env` file:

```env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

Get API key:
[https://openrouter.ai/keys](https://openrouter.ai/keys)

---

## 🧠 How It Works

1. Login to VTU portal
2. Select AI generation mode
3. Enter:

   * Internship domain
   * Date range
   * Hours per day
   * Skill IDs
4. AI generates entries
5. Entries are validated
6. Automatically uploaded to VTU

---

## 📝 Run Command Summary

```bash
git clone https://github.com/cgdhanush/vtu-diary-auto-entry.git
cd vtu-diary-auto-entry
pip install -r requirements.txt
python main.py
```

---

## 🧑‍💻 Author

* **Dhanush C G**
* GitHub: [https://github.com/cgdhanush](https://github.com/cgdhanush)
* Built with Python 🐍 to eliminate boring manual work

