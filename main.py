import json
import os
import time

from dotenv import load_dotenv
from openai import OpenAI
from tools.client import VTUClient
from tools.load import load_entries, validate_all_entries
from tools.ai_generator import generate_entries
from tools.utils import ask_int, ask_required, ask_skills, generate_dates

FILE_PATH = "data/entries.json"

load_dotenv()


if __name__ == "__main__":

    for attempt in range(3):
        try:
            email = ask_required("Enter your email: ")
            password = ask_required("Enter your password: ")

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

        domain = ask_required("Internship domain: ")

        mode = ask_required("Choose input mode (range / list): ").strip().lower()

        if mode == "range":
            start_date = ask_required("Start date (YYYY-MM-DD): ")
            end_date = ask_required("End date (YYYY-MM-DD): ")
            dates = generate_dates(start_date, end_date)

        elif mode == "list":
            raw = ask_required("Enter dates (comma-separated YYYY-MM-DD): ")
            dates = [d.strip() for d in raw.split(",") if d.strip()]

        else:
            raise ValueError("Invalid mode. Choose 'range' or 'list'.")
        
        hours = ask_int("Hours per day (default 4): ", 4)
        skills = ask_skills("Skill IDs (default 3): ")

        # OpenRouter client
        ai_client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )

        generated_data = generate_entries(
            client=ai_client,
            internship_domain=domain,
            dates=dates,
            hours_per_day=hours,
            skill_ids=skills,
        )

        with open(FILE_PATH, "w") as f:
            json.dump(generated_data, f, indent=2)
            
    entries_data = load_entries()

    # Add internship_id to each entry
    Entries = []
    for entry in entries_data["entries"]:
        entry["internship_id"] = int(internship_id)
        entry["mood_slider"] = 5
        Entries.append(entry)

    # Validate
    validate_all_entries(Entries)

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
            print(f"Error: {str(e)}")
            print("=" * 50)

        time.sleep(20)
