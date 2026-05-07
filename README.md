# 🤖 VTU AI Internship Diary Automator

An AI tool that auto-generates and uploads VTU internship diary entries using OpenRouter AI.

No manual form filling. No repetitive work. Just run and relax ☕️


## ✨ Features

- 🤖 AI-generated internship diary entries
- 📅 Custom date range generation
- 🎯 Domain-specific diary creation (Cyber Security, Web Dev, etc.)
- 🔐 Secure login using email & password
- 📤 Auto-submit multiple internship diary entries
- 🛡️ Error handling so one failure won’t stop the whole run
- ⏳ Built-in delay between requests (rate-safe)
- 📊 Clean console output for tracking submissions


## 🚀 Usage

Clone the repository:

```bash
git clone https://github.com/cgdhanush/vtu-diary-auto-entry.git
```

Move into the project directory:

```bash
cd vtu-diary-auto-entry
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Setup

### Create a `.env` file:

```env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

Get API key from:
[OpenRouter API Keys](https://openrouter.ai/keys)

Run the script:

```bash
python main.py
```

## 🧠 How It Works

1. User logs into VTU portal
2. Selects AI generation mode
3. Inputs:
   - Internship domain
   - Start & end date
   - Hours per day
   - Skills ID( see skills.md)

4. AI generates structured diary entries
5. Entries are validated
6. Entries are automatically uploaded to VTU

## 📝 Example Entry Format

```json
[
  {
    "date": "2026-04-13",
    "description": "Worked on vulnerability assessment lifecycle and analysis",
    "hours": 4,
    "links": "",
    "blockers": "",
    "learnings": "Understood vulnerability identification and prioritization",
    "internship_id": 12345
  }
]
```

## Internship Diary Tool

### ▶️ How to Run

Run the script:

```bash
python diary.py
```

### 📋 Menu Options

After login:

```
1) Diaries to pdf
2) Check missing dates
3) Exit
```

## ⚠️ Notes

- Keep your login credentials safe 🔐
- Do not reduce delay too much (avoid API blocking)
- Ensure `Entries` is properly formatted before running

## 💡 Future Ideas

- 📊 Progress dashboard

## 🧑‍💻 Author

- Name: Dhanush C G
- GitHub: https://github.com/cgdhanush
- Built with Python 🐍 to kill boring manual work.
