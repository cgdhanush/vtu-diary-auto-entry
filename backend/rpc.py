import json
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

from .vtu_client import VTUClient
from .load import load_entries, validate_all_entries
from .ai_generator import generate_entries
from .utils import generate_dates

load_dotenv()


class VTURPC:
    """
    RPC-style service class that handles:
    - login
    - internship fetch
    - entry generation
    - validation
    - submission
    """

    def __init__(self):
        self.vtu_client = None
        self.internship_id = None
        self.internship_name = None


    # AUTH
    def login(self, email:str, password: str):
        self.vtu_client = VTUClient(email=email, password=password)
        self.vtu_client.login()
        return {"message": "Login successful"}


    # FETCH INTERNSHIP
    def fetch_internship(self):
        response = self.vtu_client.request(
            "GET", "/student/internship-applys?page=1&status=6"
        )

        data = response.get("data", {}).get("data", [])
        if not data:
            raise Exception("No internship found")

        self.internship_id = data[0].get("internship_id")
        self.internship_name = (
            data[0].get("internship_details", {}).get("name", "Unknown Internship")
        )

        return {
            "internship_id": self.internship_id,
            "internship_name": self.internship_name,
        }


    # GENERATE ENTRIES
    def generate(
        self,
        domain: str,
        mode: str,
        start_date=None,
        end_date=None,
        dates=None,
        skills=None,
    ):

        if mode == "range":
            dates = generate_dates(start_date, end_date)
        elif mode == "list":
            dates = dates
        else:
            raise Exception("Invalid mode")

        ai_client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )

        entries = generate_entries(
            vtu_client=ai_client,
            internship_domain=domain,
            dates=dates,
            hours_per_day=4,
            skill_ids=skills or [],
        )

        enriched = []
        for entry in entries:
            entry["internship_id"] = int(self.internship_id)
            entry["mood_slider"] = 5
            enriched.append(entry)

        os.makedirs("data", exist_ok=True)

        with open("data/entries.json", "w") as f:
            json.dump(enriched, f, indent=2)

        return entries


    # LOAD + VALIDATE
    def load_and_validate(self):
        data = load_entries()
        entries = data.get("entries", [])
        
        validate_all_entries(entries)
        return entries


    # SUBMIT ENTRIES (BOT RUN)
    def run_bot(self):
        entries = self.load_and_validate()

        results = []

        for entry in entries:
            try:
                response = self.vtu_client.request(
                    "POST",
                    "/student/internship-diaries/store",
                    json=entry,
                )

                results.append(
                    {
                        "date": entry.get("date"),
                        "status": response.get("message", "success"),
                    }
                )

                time.sleep(2)  # reduced delay for API usage

            except Exception as e:
                results.append(
                    {
                        "date": entry.get("date"),
                        "status": f"failed: {str(e)}",
                    }
                )

        return {
            "message": "Bot execution completed",
            "internship": self.internship_name,
            "results": results,
        }
