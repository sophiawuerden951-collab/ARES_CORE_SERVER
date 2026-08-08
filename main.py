from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(
    title="ARES_CORE_SERVER",
    version="4.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ARES_APIK = os.getenv("ARES_APIK", "")
ARES_MASTER_PIN = os.getenv("ARES_MASTER_PIN", "")

LUNA_SESSION_ID = "LUNA_ARES_CORE_SESSION_4_0"


class ChatRequest(BaseModel):
    message: str | None = None
    text: str | None = None
    prompt: str | None = None
    input: str | None = None
    query: str | None = None
    apik: str | None = None
    api_key: str | None = None
    master_pin: str | None = None
    access_token: str | None = None
    session_id: str | None = None
    token: str | None = None


def text_aus_req(req: ChatRequest | None) -> str:
    if not req:
        return ""

    return (
        req.message
        or req.text
        or req.prompt
        or req.input
        or req.query
        or ""
    ).strip()


def pruefe_zugang(
    req: ChatRequest | None = None,
    x_ares_key: str | None = None,
    authorization: str | None = None
):
    key = ""

    if req:
        key = (
            req.apik
            or req.api_key
            or req.access_token
            or req.session_id
            or req.token
            or ""
        )

    if not key and x_ares_key:
        key = x_ares_key

    if not key and authorization:
        key = authorization.replace("Bearer ", "").strip()

    pin = req.master_pin if req else None

    if ARES_APIK and key == ARES_APIK:
        return True

    if ARES_MASTER_PIN and pin == ARES_MASTER_PIN:
        return True

    if key == LUNA_SESSION_ID:
        return True

    raise HTTPException(status_code=401, detail="Zugriff verweigert")


def luna_sitzung():
    return {
        "status": "ok",
        "online": True,
        "auth": "granted",
        "authenticated": True,
        "access": "granted",
        "access_token": LUNA_SESSION_ID,
        "token": LUNA_SESSION_ID,
        "session_id": LUNA_SESSION_ID,
        "session": True,
        "session_created": True,
        "luna_session": True,
        "luna_session_created": True,
        "owner": "Luna",
        "user": "Luna",
        "core": "ARES_CORE_4.0.0",
        "core_online": True,
        "message": "Luna-Sitzung erstellt."
    }


def ares_antwort(text: str):
    if not text:
        text = "Keine Nachricht erhalten."

    antwort = "ARES_CORE ist online. Nachricht erhalten: " + text

    return {
        "answer": antwort,
        "response": antwort,
        "message": antwort,
        "text": antwort,
        "status": "online",
        "access_token": LUNA_SESSION_ID,
        "token": LUNA_SESSION_ID,
        "session_id": LUNA_SESSION_ID,
        "session": True,
        "session_created": True,
        "luna_session": True,
        "luna_session_created": True,
        "core": "ARES_CORE_4.0.0",
        "core_online": True,
        "owner": "Luna"
    }


@app.get("/")
def start():
    return {
        "status": "online",
        "name": "ARES_CORE_SERVER",
        "core": "ARES_CORE_4.0.0",
        "owner": "Luna",
        "session": True,
        "luna_session": True,
        "access_token": LUNA_SESSION_ID,
        "info": "ARES_CORE_SERVER online."
    }


@app.get("/health")
def health():
    return {
        "status": "online",
        "name": "ARES_CORE_SERVER",
        "core": "ARES_CORE_4.0.0",
        "owner": "Luna",
        "session": True,
        "luna_session": True,
        "access_token": LUNA_SESSION_ID,
        "time": datetime.now().isoformat()
    }


@app.get("/v1/health")
def v1_health():
    return health()


@app.get("/Gesundheit")
def gesundheit():
    return health()


@app.get("/v1/Gesundheit")
def v1_gesundheit():
    return health()


@app.get("/status")
def status():
    return health()


@app.get("/v1/status")
def v1_status():
    return health()


@app.get("/auth")
def auth_get():
    return luna_sitzung()


@app.get("/v1/auth")
def v1_auth_get():
    return luna_sitzung()


@app.post("/auth")
def auth(
    req: ChatRequest | None = None,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
):
    pruefe_zugang(req, x_ares_key, authorization)
    return luna_sitzung()


@app.post("/v1/auth")
def v1_auth(
    req: ChatRequest | None = None,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
):
    pruefe_zugang(req, x_ares_key, authorization)
    return luna_sitzung()


@app.get("/connect")
def connect_get():
    return luna_sitzung()


@app.get("/v1/connect")
def v1_connect_get():
    return luna_sitzung()


@app.post("/connect")
def connect_post(
    req: ChatRequest | None = None,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
):
    pruefe_zugang(req, x_ares_key, authorization)
    return luna_sitzung()


@app.post("/v1/connect")
def v1_connect_post(
    req: ChatRequest | None = None,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
):
    pruefe_zugang(req, x_ares_key, authorization)
    return luna_sitzung()


@app.post("/chat")
def chat(
    req: ChatRequest,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
):
    pruefe_zugang(req, x_ares_key, authorization)
    return ares_antwort(text_aus_req(req))


@app.post("/v1/chat")
def v1_chat(
    req: ChatRequest,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
):
    return chat(req, x_ares_key, authorization)


@app.post("/process")
def process(
    req: ChatRequest,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
):
    return chat(req, x_ares_key, authorization)


@app.post("/v1/process")
def v1_process(
    req: ChatRequest,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
):
    return chat(req, x_ares_key, authorization)


@app.post("/api/chat")
def api_chat(
    req: ChatRequest,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
):
    return chat(req, x_ares_key, authorization)


@app.post("/api/process")
def api_process(
    req: ChatRequest,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
):
    return chat(req, x_ares_key, authorization)


@app.post("/v1/api/chat")
def v1_api_chat(
    req: ChatRequest,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
):
    return chat(req, x_ares_key, authorization)


@app.post("/v1/api/process")
def v1_api_process(
    req: ChatRequest,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
):
    return chat(req, x_ares_key, authorization)


@app.api_route("/{full_path:path}", methods=["GET", "POST"])
async def fallback(full_path: str, request: Request):
    return {
        "status": "online",
        "core": "ARES_CORE_4.0.0",
        "owner": "Luna",
        "session": True,
        "session_created": True,
        "luna_session": True,
        "luna_session_created": True,
        "access_token": LUNA_SESSION_ID,
        "token": LUNA_SESSION_ID,
        "session_id": LUNA_SESSION_ID,
        "path_received": "/" + full_path,
        "message": "ARES_CORE_SERVER lebt und Luna-Sitzung ist aktiv."
    }
