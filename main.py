from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(
    title="ARES_CORE_SERVER",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

ARES_APIK = os.getenv("ARES_APIK", "")
ARES_MASTER_PIN = os.getenv("ARES_MASTER_PIN", "")

class ChatRequest(BaseModel):
    message: str
    apik: str | None = None
    master_pin: str | None = None

def pruefe_zugang(req: ChatRequest, header_key: str | None):
    key = req.apik or header_key or ""

    if ARES_APIK and key == ARES_APIK:
        return True

    if ARES_MASTER_PIN and req.master_pin == ARES_MASTER_PIN:
        return True

    raise HTTPException(status_code=401, detail="Zugriff verweigert")

@app.get("/")
def start():
    return {
        "status": "online",
        "name": "ARES_CORE_SERVER",
        "info": "Nutze /health oder /chat"
    }

@app.get("/health")
def health():
    return {
        "status": "online",
        "name": "ARES_CORE_SERVER",
        "version": "1.0.0",
        "zeit": datetime.now().isoformat()
    }

@app.post("/chat")
def chat(req: ChatRequest, x_ares_key: str | None = Header(default=None)):
    pruefe_zugang(req, x_ares_key)

    return {
        "answer": "ARES_CORE ist online. Nachricht erhalten: " + req.message,
        "core": "ARES_CORE_4.0.0",
        "owner": "Luna"
    }
    
