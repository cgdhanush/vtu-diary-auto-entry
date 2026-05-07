import json
import re
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


def generate_entries(
    client: OpenAI,
    internship_domain,
    start_date,
    end_date,
    hours_per_day,
    skill_ids,
    tone="student like"
):
    dates = generate_dates(start_date, end_date)

    prompt = f"""
Generate internship diary entries in STRICT JSON format.

RULES:
- One entry per date
- Must be valid JSON array ONLY
- No markdown, no explanation
- No single quotes allowed
- Domain: {internship_domain}
- Tone: {tone}
- skill_ids must be exactly: {json.dumps(skill_ids)}
- Hours per day must be: {hours_per_day}

DATES:
{json.dumps(dates)}

FORMAT:
[
  {{
    "date": "YYYY-MM-DD",
    "description": "short work done",
    "hours": {hours_per_day},
    "skill_ids": {json.dumps(skill_ids)},
    "links": "",
    "blockers": "",
    "learnings": "short learning"
  }}
]
"""

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You output ONLY valid JSON. No markdown. No text.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=1800,

        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    return safe_json_load(content)