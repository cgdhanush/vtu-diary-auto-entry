import json
from datetime import datetime, timedelta

from openai import OpenAI


def generate_dates(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    dates = []
    while start <= end:
        dates.append(start.strftime("%Y-%m-%d"))
        start += timedelta(days=1)

    return dates


def generate_entries(
    client: OpenAI,
    internship_domain,
    start_date,
    end_date,
    hours_per_day,
    skill_ids,
    tone="student-like",
):
    dates = generate_dates(start_date, end_date)

    prompt = f"""
Generate internship diary entries in STRICT JSON format.

RULES:
- One entry per date
- Each entry must be unique and progressive (no repetition)
- Keep description and learnings short (1–2 lines)
- Domain: {internship_domain}
- Tone: {tone}
- Hours per day: {hours_per_day} do not change this
- skill_ids: {skill_ids} do not change these

RETURN ONLY VALID JSON ARRAY. NO MARKDOWN.

FORMAT:
[
  {{
    "date": "YYYY-MM-DD",
    "description": "short work done",
    "hours": {hours_per_day},
    "skill_ids": {skill_ids},
    "links": "",
    "blockers": "",
    "learnings": "short learning"
  }}
]

DATES:
{dates}
"""

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a strict JSON generator for internship diaries.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=min(len(dates) * 120, 1800),
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown if model adds it
    if "```" in content:
        content = content.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON returned by model:\n{content}")