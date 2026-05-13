from tqdm import tqdm
from backend.vtu_client import VTUClient
from datetime import datetime, timedelta
from weasyprint import HTML


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


def clean(text):
    if not text:
        return ""
    return (
        str(text)
        .replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("—", "-")
        .replace("–", "-")
    )


def to_pdf(diary, filename="diary.pdf"):

    rows = ""

    for d in diary:
        rows += f"""
        <tr>
            <td>{clean(d.get('date', ''))}</td>
            <td>{clean(d.get('description', ''))}</td>
            <td>{clean(d.get('learnings', ''))}</td>
            <td>{clean(d.get('status', ''))}</td>
            <td>{clean(d.get('internship', {}).get('name', ''))}</td>
        </tr>
        """

    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial;
                margin: 20px;
            }}

            h2 {{
                text-align: center;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 12px;
            }}

            th, td {{
                border: 1px solid black;
                padding: 6px;
                vertical-align: top;
                word-wrap: break-word;
            }}

            th {{
                background-color: #4a4a4a;
                color: white;
            }}
        </style>
    </head>

    <body>
        <h2>Internship Diaries</h2>

        <table>
            <tr>
                <th>Date</th>
                <th>Description</th>
                <th>Learnings</th>
                <th>Status</th>
                <th>Internship</th>
            </tr>
            {rows}
        </table>

    </body>
    </html>
    """

    HTML(string=html_content).write_pdf(filename)


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
