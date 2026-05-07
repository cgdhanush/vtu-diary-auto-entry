import json
import os
import time

from dotenv import load_dotenv
from openai import OpenAI
from tools.client import VTUClient
from tools.load import load_entries, validate_all_entries
from tools.ai_generator import generate_entries

FILE_PATH = "data/entries.json"

load_dotenv()


if __name__ == "__main__":

    for attempt in range(3):
        try:
            email = input("Enter your email: ")
            password = input("Enter your password: ")

            vtu_client = VTUClient(email=email, password=password)
            vtu_client.login()
            break

        except Exception as e:
            print(f"Login failed (Attempt {attempt + 1}/3): {e}")

            if attempt == 2:
                print("Maximum login attempts reached.")

    internship_response = vtu_client.request(
        "GET", "/student/internship-applys?page=1&status=6"
    )
    internship_id = (
        internship_response.get("data", {}).get("data", [])[0].get("internship_id")
    )

    choice = input("Generate entries using AI? (y/n): ").lower()

    if choice == "y":

        domain = input("Internship domain: ")
        start_date = input("Start date (YYYY-MM-DD): ")
        end_date = input("End date (YYYY-MM-DD): ")
        hours = int(input("Hours per day or default (4): ") or 4)
        skills = input("Skill IDs comma separated or default ([3]-'Python'): ").split(",") or ["3"]


        # OpenRouter client
        ai_client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )

        entries_data = generate_entries(
            client=ai_client,
            internship_domain=domain,
            start_date=start_date,
            end_date=end_date,
            hours_per_day=hours,
            skill_ids=skills,
        )

        with open(FILE_PATH, "w") as f:
            json.dump(entries_data, f, indent=2)

    else:
        entries_data = load_entries()

    # Add internship_id to each entry
    Entries = []
    for entry in entries_data:
        entry["internship_id"] = int(internship_id)
        entry["mood_slider"] = 5
        Entries.append(entry)

    # Validate
    validate_all_entries(entries_data)

    for entry in Entries:
        try:
            response = vtu_client.request(
                "POST", "/student/internship-diaries/store", json=entry
            )

            internship_name = (
                internship_response.get("data", {})
                .get("data", [{}])[0]
                .get("internship_details", {})
                .get("name", "Unknown Internship")
            )

            print("\n" + "=" * 50)
            print(f"Internship : {internship_name}")
            print(f"Date          : {entry.get('date', 'N/A')}")
            print(response.get("message", "No message in response"))
            print("=" * 50)

        except Exception as e:
            print("\n" + "=" * 50)
            print(f"Error processing entry for date: {entry.get('date', 'N/A')}")
            print(f"Error: {str(e)}", extra_info=True)
            print("=" * 50)

        time.sleep(20)
