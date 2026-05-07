import time
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



### Chnage the entries as per your requirements. You can add multiple entries to the list and they will be processed sequentially with a delay of 20 seconds between each entry to avoid hitting rate limits. Make sure to update the "internship_id" field with the correct ID from your internship applications. The "date" field should be in the format "YYYY-MM-DD". Adjust the "description", "hours", "learnings", and other fields as needed for each diary entry.
### Note: The "skill_ids" field should contain a list of skill IDs that you want to associate with the diary entry. You can find the skill IDs from the VTU platform or API documentation.

Entries = [
    {
        "internship_id": int(internship_id),
        "date": "2026-04-13",
        "description": "Learned the stages involved in the Vulnerability Assessment lifecycle from discovery to remediation",
        "hours": 4,
        "links": "",
        "blockers": "",
        "learnings": "Understood how to identify, assess, prioritize, and manage security vulnerabilities effectively.",
        "mood_slider": 5,
        "skill_ids": ["3"],
    },
]



### Change ENDS Here

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