import json
from openai import OpenAI

from .utils import safe_json_load



def generate_entries(
    client: OpenAI,
    internship_domain,
    dates,
    hours_per_day,
    skill_ids,
    tone="student like"
):

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
    "description": "short two line work done",
    "hours": {hours_per_day},
    "skill_ids": {json.dumps(skill_ids)},
    "links": "",
    "blockers": "",
    "learnings": "short one line learning"
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