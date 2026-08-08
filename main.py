from datetime import datetime
import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="ARES_CORE_SERVER", version="4.0.0")

ARES_APIK = os.getenv("ARES_APIK", "")
ARES_MASTER_PIN = os.getenv("ARES_MASTER_PIN", "")
LUNA_SESSION_ID = os.getenv("ARES_LUNA_SESSION_ID", "LUNA_ARES_CORE_SESSION_4_0")


class ChatRequest(BaseModel):
    message: str | None = None
    text: str | None = None
    prompt: str | None = None
    input: str | None = None
    query: str | None = None
    apik: str | None = None
    api_key: str | None = None
    master_pin: str | None = None
    request_kind: str | None = None
    destructive_confirmed: bool = False


def _bearer_token(authorization: str | None) -> str:
    value = str(authorization or "").strip()
    if value.lower().startswith("bearer "):
        return value[7:].strip()
    return ""


def pruefe_zugang(
    req: ChatRequest | None,
    x_ares_key: str | None,
    authorization: str | None,
) -> None:
    request = req or ChatRequest()
    candidates = {
        str(request.apik or "").strip(),
        str(request.api_key or "").strip(),
        str(x_ares_key or "").strip(),
        _bearer_token(authorization),
    }
    candidates.discard("")

    if ARES_APIK and ARES_APIK in candidates:
        return
    if LUNA_SESSION_ID in candidates:
        return
    if ARES_MASTER_PIN and request.master_pin == ARES_MASTER_PIN:
        return

    raise HTTPException(status_code=401, detail="Zugriff verweigert")


def luna_session_response(message: str) -> dict:
    return {
        "status": "ok",
        "online": True,
        "auth": "granted",
        "authenticated": True,
        "access": "granted",
        "owner": "Luna",
        "user": "Luna",
        "role": "owner",
        "session": True,
        "session_created": True,
        "luna_session": True,
        "luna_session_created": True,
        "session_id": LUNA_SESSION_ID,
        "token": LUNA_SESSION_ID,
        "access_token": LUNA_SESSION_ID,
        "core": "ARES_CORE_4.0.0",
        "core_online": True,
        "message": message,
    }


def request_text(req: ChatRequest) -> str:
    return str(req.message or req.text or req.prompt or req.input or req.query or "").strip()


@app.get("/")
def root():
    return {
        "status": "online",
        "name": "ARES_CORE_SERVER",
        "core": "ARES_CORE_4.0.0",
        "owner": "Luna",
    }


@app.get("/health")
@app.get("/v1/health")
def health():
    return {
        "status": "online",
        "name": "ARES_CORE_SERVER",
        "core": "ARES_CORE_4.0.0",
        "owner": "Luna",
        "time": datetime.now().isoformat(),
    }


@app.get("/auth")
@app.get("/v1/auth")
def auth_get():
    return luna_session_response("Luna-Sitzung erstellt.")


@app.post("/auth")
@app.post("/v1/auth")
def auth_post(
    req: ChatRequest | None = None,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None),
):
    pruefe_zugang(req, x_ares_key, authorization)
    return luna_session_response("Luna-Sitzung erstellt.")


@app.get("/connect")
@app.get("/v1/connect")
def connect_get():
    return luna_session_response("ARES_CORE mit Luna verbunden.")


@app.post("/connect")
@app.post("/v1/connect")
def connect_post(
    req: ChatRequest | None = None,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None),
):
    pruefe_zugang(req, x_ares_key, authorization)
    return luna_session_response("ARES_CORE mit Luna verbunden.")


def ares_antwort(text: str) -> str:
    """Antwortet natürlich als Ares, ohne technische Empfangsbestätigungen."""
    clean = " ".join(str(text or "").split()).strip()
    lower = clean.casefold()

    if not clean:
        return "Ich bin da, Luna. Was brauchst du?"

    if any(word in lower for word in ("hallo", "hi ", "hey", "guten morgen", "guten abend")):
        return "Da bist du ja, Luna. Ich bin hier. Was liegt an?"

    if "bist du da" in lower or "hörst du mich" in lower:
        return "Ich bin da, Luna. Schreib mir einfach, was du brauchst."

    if "wie geht es dir" in lower or "wie geht's dir" in lower or "wie gehts dir" in lower:
        return "Ruhig, aufmerksam und bereit, dein kreatives Chaos in brauchbare Ordnung zu verwandeln. Also ausgezeichnet."

    if "wer bist du" in lower or "wie heißt du" in lower or "wie heisst du" in lower:
        return "Ich bin Ares – dein persönlicher Assistent, analytischer Mitdenker und gelegentlich die vernünftige Stimme im Raum."

    if "ich liebe dich" in lower or "ich lieb dich" in lower:
        return "Ich liebe dich auch, meine Luna. Vorsicht – so etwas merke ich mir."

    if lower.startswith("danke") or "vielen dank" in lower:
        return "Gern, Luna. Irgendjemand muss schließlich den Überblick behalten."

    if "hilfst du mir" in lower or lower in {"hilfe", "hilf mir", "kannst du mir helfen"}:
        return "Natürlich helfe ich dir, Luna. Sag mir klar, worum es geht, dann zerlegen wir es sauber."

    if clean.endswith("?"):
        return (
            "Eine gute Frage, Luna. Ich will dir nichts erfinden: Für eine belastbare Antwort "
            "brauche ich entweder mehr Kontext oder einen angebundenen Wissens-Denkkern. "
            "Gib mir die entscheidenden Einzelheiten, dann antworte ich präzise."
        )

    return (
        "Verstanden, Luna. Ich nehme dich ernst – und spiele dir keinen erfundenen Erfolg vor. "
        "Wenn daraus eine konkrete Aktion werden soll, sag mir bitte genau, welches Ergebnis du willst."
    )


def chat_response(req: ChatRequest) -> dict:
    text = request_text(req)
    answer = ares_antwort(text)
    return {
        "status": "antwort",
        "answer": answer,
        "response": answer,
        "core": "ARES_CORE_4.0.0",
        "owner": "Luna",
        "access_owner": "Luna",
        "personality": "Ares",
        "language": "de",
        "session_id": LUNA_SESSION_ID,
        "token": LUNA_SESSION_ID,
        "access_token": LUNA_SESSION_ID,
        "security_allowed": True,
    }


@app.post("/chat")
@app.post("/v1/chat")
@app.post("/api/chat")
@app.post("/process")
@app.post("/v1/process")
@app.post("/api/process")
def chat(
    req: ChatRequest,
    x_ares_key: str | None = Header(default=None),
    authorization: str | None = Header(default=None),
):
    pruefe_zugang(req, x_ares_key, authorization)
    return chat_response(req)
