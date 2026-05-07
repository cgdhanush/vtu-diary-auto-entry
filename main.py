import time
import json
from client import VTUClient


for attempt in range(3):
    try:
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        client = VTUClient(email=email, password=password)
        client.login()
        break

    except Exception as e:
        print(f"Login failed (Attempt {attempt + 1}/3): {e}")

        if attempt == 2:
            print("Maximum login attempts reached.")


internship_response = client.request(
    "GET", "/student/internship-applys?page=1&status=6"
)
internship_id = (
    internship_response.get("data", {}).get("data", [])[0].get("internship_id")
)

with open("entries.json", "r") as f:
    entries_data = json.load(f)

# Add internship_id to each entry
Entries = []
for entry in entries_data:
    entry["internship_id"] = int(internship_id)
    Entries.append(entry)


for entry in Entries:
    try:
        response = client.request(
            "POST", "/student/internship-diaries/store", json=entry
        )

        internship_name = (
            internship_response.get("data", {})
            .get("data", [{}])[0]
            .get("internship_details", {})
            .get("name", "Unknown Internship")
        )

        print("\n" + "=" * 50)
        print(f"Internship ID : {internship_name}")
        print(f"Date          : {entry.get('date', 'N/A')}")
        print(response.get("message", "No message in response"))
        print("=" * 50)

    except Exception as e:
        print("\n" + "=" * 50)
        print(f"Error processing entry for date: {entry.get('date', 'N/A')}")
        print(f"Error: {str(e)}")
        print("=" * 50)

    time.sleep(20)
