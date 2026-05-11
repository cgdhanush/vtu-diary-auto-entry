from fastapi import FastAPI, HTTPException, Depends, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from threading import Lock

from .rpc import VTURPC
from .web_ui import router_ui

app = FastAPI(
    title="VTU Bot RPC API", 
    # docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_ui, prefix="")

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

class UserRequest(BaseModel):
    email: str

class BotRequest(BaseModel):
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


# Proper FastAPI dependency wrapper
def get_rpc(email: str = Query(...)) -> VTURPC:
    return get_session(email)


def get_rpc_unauth():
    return VTURPC()


# -------------------------
# LOGIN
# -------------------------
@app.post("/api/auth/login")
async def login(req: LoginRequest):
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
async def generate(req: BotRequest, email: str = Header(...)):
    rpc = get_session(email)

    try:
        entries = rpc.generate(
            domain=req.domain,
            mode=req.mode,
            start_date=req.start_date,
            end_date=req.end_date,
            dates=req.dates,
            skills=req.skills,
        )

        return {"message": "Generation Success", "entries": entries}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# RUN BOT (USES SESSION)
# -------------------------
@app.post("/api/run-bot")
async def run_bot(email: str = Header(...)):
    rpc = get_session(email)

    try:
        return rpc.run_bot()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------
# GET ENTRIES
# -------------------------
@app.get("/api/entries")
async def get_entries():
    rpc = get_rpc_unauth()

    try:
        return rpc.load_and_validate()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
