
# 🚀 Internship Diary Auto Uploader

A simple Python automation script to automatically submit internship diary entries to the VTU portal using a logged-in client session.

No manual form filling. No repetitive work. Just run and relax ☕️

---

## ✨ Features

- 🔐 Secure login using email & password
- 📤 Auto-submit multiple internship diary entries
- 🛡️ Error handling so one failure won’t stop the whole run
- ⏳ Built-in delay between requests (rate-safe)
- 📊 Clean console output for tracking submissions

---

## 🧠 How It Works

1. Logs into VTU using your credentials
2. Iterates through your `Entries` list
3. Submits each diary entry via API
4. Prints response status for each entry
5. Waits before sending the next request

---

## 📦 Requirements

Make sure you have:

```bash
pip install requests
````

(And your `VTUClient` module properly set up)

## 🚀 Usage

Clone the repository:

```bash
git clone https://github.com/cgdhanush/vtu-diary-auto-entry.git
````

Move into the project directory:

```bash
cd vtu-diary-auto-entry
```

Run the script:

```bash
python main.py
```

## ⚠️ Notes

* Keep your login credentials safe 🔐
* Do not reduce delay too much (avoid API blocking)
* Ensure `Entries` is properly formatted before running

---

## 💡 Future Ideas

* 🔁 Auto retry failed entries
* 📝 Save logs to file
* 📊 Progress dashboard
* ⚡ Async submission for speed

---

## 🧑‍💻 Author
- Name: Dhanush C G
- GitHub: https://github.com/cgdhanush
- Built with Python 🐍 to kill boring manual work.
