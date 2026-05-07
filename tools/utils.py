import json
import re
from datetime import datetime, timedelta


def ask_required(prompt):
    while (v := input(prompt).strip()) == "":
        print("Required field.")
    return v


def ask_int(prompt, default):
    while True:
        v = input(prompt).strip()
        if not v:
            return default
        if v.isdigit():
            return int(v)
        print("Enter a valid number.")


def ask_skills(prompt, default="3"):
    while True:
        v = input(prompt).strip()
        if not v:
            return [default]

        skills = [s.strip() for s in v.split(",") if s.strip()]
        if skills:
            return skills

        print("Enter at least one skill ID.")
    

def generate_dates(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    dates = []
    while start <= end:
        dates.append(start.strftime("%Y-%m-%d"))
        start += timedelta(days=1)

    return dates


def safe_json_load(content: str):
    """Robust JSON parser fallback"""
    content = content.strip()

    # remove markdown fences
    content = re.sub(r"```(json)?", "", content).replace("```", "").strip()

    # try strict parse first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # fallback: fix common LLM mistakes
    content = content.replace("'", '"')

    return json.loads(content)
