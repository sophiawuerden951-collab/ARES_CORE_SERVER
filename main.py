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


class ChatRequest(BaseModel):
    message: str | None = None
    text: str | None = None
    prompt: str | None = None
    input: str | None = None
    query: str | None = None
    apik: str | None = None
    api_key: str | None = None
    master_pin: str | None = None


def text_aus_req(req: ChatRequest) -> str:
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
        key = req.apik or req.api_key or ""

    if not key and x_ares_key:
        key = x_ares_key

    if not key and authorization:
        key = authorization.replace("Bearer ", "").strip()

    pin = req.master_pin if req else None

    if ARES_APIK and key == ARES_APIK:
        return True

    if ARES_MASTER_PIN and pin == ARES_MASTER_PIN:
        return True

    raise HTTPException(status_code=401, detail="Zugriff verweigert")


def ares_antwort(text: str):
    if not text:
        text = "Keine Nachricht erhalten."

    return {
        "answer": "ARES_CORE ist online. Nachricht erhalten: " + text,
        "response": "ARES_CORE ist online. Nachricht erhalten: " + text,
        "message": "ARES_CORE ist online. Nachricht erhalten: " + text,
        "core": "ARES_CORE_4.0.0",
        "owner": "Luna",
        "status": "online"
    }


# ------------------------------------------------------------
# START / HEALTH
# ------------------------------------------------------------

@app.get("/")
def start():
    return {
        "status": "online",
        "name": "ARES_CORE_SERVER",
        "core": "ARES_CORE_4.0.0",
        "owner": "Luna",
        "info": "Nutze /health, /v1/health, /chat oder /v1/process"
    }


@app.get("/health")
def health():
    return {
        "status": "online",
        "name": "ARES_CORE_SERVER",
        "core": "ARES_CORE_4.0.0",
        "owner": "Luna",
        "time": datetime.now().isoformat()
    }


@app.get("/Gesundheit")
def gesundheit():
    return health()


@app.get("/v1/health")
def v1_health():
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


# ------------------------------------------------------------
# AUTH / VERBINDUNG
# ------------------------------------------------------------

@app.post("/auth")
def auth(req: ChatRequest, x_ares_key: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    pruefe_zugang(req, x_ares_key, authorization)
    return {
        "status": "ok",
        "auth": "granted",
        "core": "ARES_CORE_4.0.0",
        "owner": "Luna"
    }


@app.post("/v1/auth")
def v1_auth(req: ChatRequest, x_ares_key: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    return auth(req, x_ares_key, authorization)


@app.get("/connect")
def connect():
    return {
        "status": "ok",
        "connection": "ready",
        "core": "ARES_CORE_4.0.0",
        "owner": "Luna"
    }


@app.get("/v1/connect")
def v1_connect():
    return connect()


@app.post("/connect")
def connect_post(req: ChatRequest, x_ares_key: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    pruefe_zugang(req, x_ares_key, authorization)
    return connect()


@app.post("/v1/connect")
def v1_connect_post(req: ChatRequest, x_ares_key: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    pruefe_zugang(req, x_ares_key, authorization)
    return connect()


# ------------------------------------------------------------
# CHAT / PROCESS
# ------------------------------------------------------------

@app.post("/chat")
def chat(req: ChatRequest, x_ares_key: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    pruefe_zugang(req, x_ares_key, authorization)
    return ares_antwort(text_aus_req(req))


@app.post("/v1/chat")
def v1_chat(req: ChatRequest, x_ares_key: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    return chat(req, x_ares_key, authorization)


@app.post("/process")
def process(req: ChatRequest, x_ares_key: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    return chat(req, x_ares_key, authorization)


@app.post("/v1/process")
def v1_process(req: ChatRequest, x_ares_key: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    return chat(req, x_ares_key, authorization)


@app.post("/api/chat")
def api_chat(req: ChatRequest, x_ares_key: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    return chat(req, x_ares_key, authorization)


@app.post("/api/process")
def api_process(req: ChatRequest, x_ares_key: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    return chat(req, x_ares_key, authorization)


@app.post("/v1/api/chat")
def v1_api_chat(req: ChatRequest, x_ares_key: str | None = Header(default=None), authorization: str | None = Header(default=None)):
    return chat(req, x_ares_key, authorization)


# ------------------------------------------------------------
# FALLBACK: Falls Handy einen unbekannten Pfad abfragt
# ------------------------------------------------------------

@app.api_route("/{full_path:path}", methods=["GET", "POST"])
async def fallback(full_path: str, request: Request):
    return {
        "status": "online",
        "core": "ARES_CORE_4.0.0",
        "owner": "Luna",
        "path_received": "/" + full_path,
        "info": "ARES_CORE_SERVER lebt. Nutze /v1/health, /v1/auth, /v1/process oder /chat."
    }
