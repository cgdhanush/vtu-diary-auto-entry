import time
import requests

VTU_API = "https://vtuapi.internyet.in/api/v1"


def sleep(ms):
    time.sleep(ms / 1000)


class VTUClient:
    def __init__(self, email, password, retry_delay=2, max_retries=10):
        self.email = email
        self.password = password
        self.retry_delay = retry_delay
        self.max_retries = max_retries

        self.session = requests.Session()
        self.session_valid = False
        self.access_token = None
        self.refresh_token = None

    def login(self, retries_left=None):
        if retries_left is None:
            retries_left = self.max_retries

        try:
            url = f"{VTU_API}/auth/login"
            payload = {
                "email": self.email,
                "password": self.password
            }

            res = self.session.post(url, json=payload, timeout=30)
            res.raise_for_status()

            data = res.json()
            cookies = self.session.cookies.get_dict()
            self.access_token = cookies.get("access_token")
            self.refresh_token = cookies.get("refresh_token")
            self.session_valid = True

            print("✓ Logged in successfully")
            print(f"Welcome to the VTU Diary Auto Entry Script! {data.get('data', {}).get('name', '')}")
            
            return data

        except requests.exceptions.HTTPError as err:
            status = err.response.status_code if err.response else None

            if retries_left > 0 and status in [500, 503, 429]:
                print(f"[VTU] {status} error — retrying in {self.retry_delay}s...")
                sleep(self.retry_delay * 1000)
                return self.login(retries_left - 1)

            raise

        except Exception as e:
            print("Login failed:", str(e))
            raise

    def request(self, method, endpoint, retries_left=None, **kwargs) -> dict:
        if retries_left is None:
            retries_left = self.max_retries

        if not self.session_valid:
            self.login()

        try:
            url = f"{VTU_API}{endpoint}"

            res = self.session.request(
                method,
                url,
                timeout=30,
                **kwargs   # MUST include json here
            )

            res.raise_for_status()
            return res.json()

        except requests.exceptions.HTTPError as err:
            status = err.response.status_code if err.response else None

            # Token expired / auth issues
            if retries_left > 0 and status in [401, 403, 419]:
                print("[VTU] Session expired — re-logging in...")
                self.session_valid = False
                self.login()
                return self.request(method, endpoint, retries_left - 1, **kwargs)

            # Server overload retry
            if retries_left > 0 and status in [500, 503, 429]:
                print(f"[VTU] {status} — retrying in {self.retry_delay}s...")
                sleep(self.retry_delay * 1000)
                return self.request(method, endpoint, retries_left - 1, **kwargs)

            raise