from fpdf import FPDF
from tqdm import tqdm
from client import VTUClient
from datetime import datetime, timedelta


def get_all_diaries(client: VTUClient):
    links_res = client.request("GET", f"/student/internship-diaries")

    seen = set()
    links = [
        x
        for x in links_res["data"]["links"]
        if x.get("url") and not (x["url"] in seen or seen.add(x["url"]))
    ]

    diary = []

    for link in tqdm(links, desc="Fetching diaries"):
        if link["url"] is not None and link["label"] != "Next":
            page_num = link["page"]
            response = client.request(
                "GET", f"/student/internship-diaries?page={page_num}"
            )
            diary.extend(response["data"]["data"])

    return diary


def to_pdf(diary, filename="diary.pdf"):

    class PDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 14)
            self.cell(0, 10, "Internship Diaries", ln=True, align="C")
            self.ln(5)

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)

    headers = ["Date", "Description", "Hours", "Mood", "Status", "Internship"]
    col_widths = [25, 70, 15, 15, 15, 50]

    pdf.set_font("Helvetica", "B", 10)
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 8, h, border=1)
    pdf.ln()

    pdf.set_font("Helvetica", size=9)

    for d in diary:
        pdf.cell(col_widths[0], 8, str(d.get("date", "")), border=1)
        pdf.cell(col_widths[1], 8, str(d.get("description", ""))[:40], border=1)
        pdf.cell(col_widths[2], 8, str(d.get("hours", "")), border=1)
        pdf.cell(col_widths[3], 8, str(d.get("mood_slider", "")), border=1)
        pdf.cell(col_widths[4], 8, str(d.get("status", "")), border=1)

        internship = d.get("internship", {}).get("name", "")
        pdf.cell(col_widths[5], 8, internship, border=1)

        pdf.ln()

    pdf.output(filename)


def missing_dates(diary):

    existing_dates = set(item["date"] for item in diary)

    # Date range
    start_date = datetime.strptime(input("Enter start date (YYYY-MM-DD): "), "%Y-%m-%d")
    end_date = datetime.strptime(input("Enter end date (YYYY-MM-DD): "), "%Y-%m-%d")

    # Generate all dates in range
    all_dates = []
    current = start_date

    while current <= end_date:
        all_dates.append(current)
        current += timedelta(days=1)

    # A) Missing dates (including weekends)
    missing_all = [
        d.strftime("%Y-%m-%d")
        for d in all_dates
        if d.strftime("%Y-%m-%d") not in existing_dates
    ]

    # B) Missing dates (excluding Saturdays and Sundays)
    missing_weekdays = [
        d.strftime("%Y-%m-%d")
        for d in all_dates
        if d.strftime("%Y-%m-%d") not in existing_dates
        and d.weekday() < 5  # 0=Mon ... 6=Sun
    ]

    # Output
    print(f"Missing Dates (All) Total : {len(missing_all)}")
    print(missing_all)

    print(f"\nMissing Dates (Weekdays only) Total : {len(missing_weekdays)}")
    print(missing_weekdays)


if __name__ == "__main__":

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

    diary = get_all_diaries(client)

    while True:
        choice = int(
            input("1) Diaries to pdf \n2) Check missing dates\n3) Exit\nEnter choice: ")
        )

        if choice == 1:
            to_pdf(diary)

        elif choice == 2:
            missing_dates(diary)

        elif choice == 3:
            print("Exiting...")
            break

        else:
            print("Invalid choice.")
