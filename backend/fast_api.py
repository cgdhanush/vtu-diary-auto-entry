from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from threading import Lock

from .rpc import VTURPC

app = FastAPI(title="VTU Bot RPC API", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# SESSION STORE (THREAD-SAFE)
# -------------------------
SESSIONS: Dict[str, VTURPC] = {}
SESSION_LOCK = Lock()


# -------------------------
# MODELS
# -------------------------
class LoginRequest(BaseModel):
    email: str
    password: str


class BotRequest(BaseModel):
    email: str
    domain: str
    mode: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    dates: Optional[List[str]] = None
    skills: Optional[List[str]] = None


# -------------------------
# DEPENDENCY
# -------------------------
def get_session(email: str) -> VTURPC:
    with SESSION_LOCK:
        rpc = SESSIONS.get(email)

    if not rpc:
        raise HTTPException(status_code=401, detail="Not logged in")

    return rpc

def get_rpc():
    return VTURPC()

# -------------------------
# LOGIN
# -------------------------
@app.post("/api/auth/login")
def login(req: LoginRequest):
    try:
        rpc = VTURPC()
        rpc.login(req.email, req.password)

        with SESSION_LOCK:
            SESSIONS[req.email] = rpc

        return {"message": "Login successful"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# GENERATE
# -------------------------
@app.post("/api/generate")
def generate(req: BotRequest, rpc: VTURPC = Depends(get_rpc)):
    try:
        rpc.fetch_internship()

        entries = rpc.generate(
            domain=req.domain,
            mode=req.mode,
            start_date=req.start_date,
            end_date=req.end_date,
            dates=req.dates,
            skills=req.skills,
        )

        return {"entries": entries}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# RUN BOT (USES SESSION)
# -------------------------
@app.post("/api/run-bot")
def run_bot(req: BotRequest):
    try:
        rpc = get_session(req.email)

        rpc.generate(
            domain=req.domain,
            mode=req.mode,
            start_date=req.start_date,
            end_date=req.end_date,
            dates=req.dates,
            skills=req.skills,
        )

        return rpc.run_bot()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# GET ENTRIES (USES SESSION)
# -------------------------
@app.get("/api/entries")
def get_entries(rpc: VTURPC = Depends(get_rpc)):
    try:
        return rpc.load_and_validate()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# LOGOUT
# -------------------------
@app.post("/api/auth/logout")
def logout(req: LoginRequest):
    with SESSION_LOCK:
        SESSIONS.pop(req.email, None)

    return {"message": "Logged out successfully"}


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/api/ping")
def health():
    return {"status": "running"}