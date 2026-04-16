"""
@claudeprofessor — comment automation server.

Endpoints:
  GET  /webhook          Meta webhook verification handshake
  POST /webhook          Receives Instagram comment/follow events
  GET  /verificar        "Ya te sigo" verification page
  POST /verificar        AJAX check: is user a follower? sends vault link if yes.
  GET  /health           Uptime check
"""

import os
import hashlib
import hmac
import secrets
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Query, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from dotenv import load_dotenv

import database as db
import instagram_api as ig

load_dotenv()

VERIFY_TOKEN = os.environ["WEBHOOK_VERIFY_TOKEN"]
TOKEN_SECRET = os.environ["TOKEN_SECRET"]
BASE_URL = os.environ["BASE_URL"].rstrip("/")
VAULT_URL = os.environ["VAULT_URL"]
TRIGGER = os.environ.get("TRIGGER_KEYWORD", "profesor").lower()

signer = URLSafeTimedSerializer(TOKEN_SECRET)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init()
    yield


app = FastAPI(lifespan=lifespan)


# ── Webhook handshake ──────────────────────────────────────────────────────────

@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    return JSONResponse({"error": "forbidden"}, status_code=403)


# ── Webhook events ─────────────────────────────────────────────────────────────

@app.post("/webhook")
async def receive_webhook(request: Request, background: BackgroundTasks):
    # Verify X-Hub-Signature-256 (optional but recommended)
    body = await request.body()
    background.add_task(process_events, body.decode())
    return {"status": "ok"}


async def process_events(raw: str):
    import json
    try:
        payload = json.loads(raw)
    except Exception:
        return

    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            field = change.get("field")
            value = change.get("value", {})

            if field == "comments":
                await handle_comment(value)

            elif field == "followers":
                # Fires when someone follows @claudeprofessor
                await handle_new_follower(value)


async def handle_comment(value: dict):
    text = value.get("text", "").lower()
    if TRIGGER not in text:
        return

    ig_user_id = value.get("from", {}).get("id")
    ig_username = value.get("from", {}).get("username", "")
    media_id = value.get("media", {}).get("id", "")

    if not ig_user_id:
        return

    # One DM per user per post
    if db.already_dm_sent(ig_user_id, media_id):
        return

    # Generate signed token (expires in 7 days)
    token = signer.dumps(ig_user_id)
    db.add_pending(ig_user_id, token, ig_username)
    db.log_dm(ig_user_id, media_id)

    verify_url = f"{BASE_URL}/verificar?t={token}"
    message = (
        f"¡Hey! 👋 He visto que has comentado en mi publicación.\n\n"
        f"Para desbloquear la bóveda de recursos de Claude AI, "
        f"primero sígueme en Instagram.\n\n"
        f"Cuando lo hayas hecho, haz clic aquí:\n"
        f"🔓 {verify_url}\n\n"
        f"¡Te espero dentro! 🧡"
    )

    try:
        await ig.send_dm(ig_user_id, message)
    except Exception as e:
        # Fallback: public comment reply (works without DM permission)
        comment_id = value.get("id", "")
        if comment_id:
            try:
                await ig.reply_to_comment(
                    comment_id,
                    f"@{ig_username} ¡Te acabo de mandar un DM con el acceso! 👀📬",
                )
            except Exception:
                pass
        print(f"DM error for {ig_user_id}: {e}")


async def handle_new_follower(value: dict):
    """
    When someone follows @claudeprofessor, check if they have a pending
    verification and automatically send the vault link.
    """
    ig_user_id = value.get("id")
    if not ig_user_id:
        return

    record = db.get_by_user_id(ig_user_id)
    if record and not record["verified"]:
        await _send_vault_link(ig_user_id)


# ── Verification page ──────────────────────────────────────────────────────────

VERIFY_PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verificar acceso — ClaudeProfessor</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #FAF9F7;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }}
    .card {{
      background: #fff;
      border-radius: 20px;
      padding: 48px 40px;
      max-width: 420px;
      width: 100%;
      text-align: center;
      box-shadow: 0 4px 40px rgba(0,0,0,0.08);
    }}
    .logo {{
      font-size: 40px;
      margin-bottom: 8px;
    }}
    .brand {{
      color: #D97757;
      font-size: 14px;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 32px;
    }}
    h1 {{
      font-size: 22px;
      color: #1A1816;
      font-weight: 700;
      line-height: 1.3;
      margin-bottom: 12px;
    }}
    p {{
      color: #8B6F4E;
      font-size: 15px;
      line-height: 1.6;
      margin-bottom: 32px;
    }}
    .btn {{
      display: inline-block;
      background: #D97757;
      color: #fff;
      border: none;
      border-radius: 12px;
      padding: 16px 32px;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      width: 100%;
      transition: background 0.2s;
    }}
    .btn:hover {{ background: #c4694a; }}
    .btn:disabled {{ background: #ccc; cursor: not-allowed; }}
    .status {{
      margin-top: 20px;
      font-size: 14px;
      color: #8B6F4E;
      min-height: 24px;
    }}
    .success {{ color: #2d7d46; font-weight: 600; }}
    .error   {{ color: #c0392b; }}
    .vault-link {{
      display: none;
      margin-top: 24px;
      padding: 20px;
      background: #FAF9F7;
      border-radius: 12px;
      border: 2px solid #D97757;
    }}
    .vault-link a {{
      color: #D97757;
      font-weight: 700;
      font-size: 18px;
      text-decoration: none;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">✳️</div>
    <div class="brand">@claudeprofessor</div>
    <h1>¡Ya casi tienes acceso a la bóveda!</h1>
    <p>Sigue a @claudeprofessor en Instagram y luego haz clic en el botón para verificar tu acceso.</p>
    <button class="btn" id="verifyBtn" onclick="verify()">
      ✓ Ya te sigo
    </button>
    <div class="status" id="status"></div>
    <div class="vault-link" id="vaultBox">
      <p style="margin-bottom:8px;color:#1A1816;font-weight:600;">🔓 ¡Acceso desbloqueado!</p>
      <a href="{vault_url}" id="vaultLink" target="_blank">Entrar a la bóveda →</a>
    </div>
  </div>

  <script>
    const token = new URLSearchParams(window.location.search).get('t');

    async function verify() {{
      const btn = document.getElementById('verifyBtn');
      const status = document.getElementById('status');
      btn.disabled = true;
      btn.textContent = 'Verificando...';
      status.textContent = '';

      try {{
        const r = await fetch('/verificar', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ token }})
        }});
        const data = await r.json();

        if (data.verified) {{
          status.className = 'status success';
          status.textContent = '¡Verificado! Preparando tu acceso...';
          document.getElementById('vaultBox').style.display = 'block';
          document.getElementById('vaultLink').href = data.vault_url;
          btn.style.display = 'none';
        }} else if (data.not_following) {{
          status.className = 'status error';
          status.textContent = 'Parece que aún no me sigues. Sígueme en Instagram y vuelve a intentarlo.';
          btn.disabled = false;
          btn.textContent = '✓ Ya te sigo';
        }} else {{
          status.className = 'status error';
          status.textContent = data.error || 'Error inesperado. Inténtalo de nuevo.';
          btn.disabled = false;
          btn.textContent = '✓ Ya te sigo';
        }}
      }} catch(e) {{
        status.className = 'status error';
        status.textContent = 'Error de conexión. Inténtalo de nuevo.';
        btn.disabled = false;
        btn.textContent = '✓ Ya te sigo';
      }}
    }}
  </script>
</body>
</html>"""


@app.get("/verificar", response_class=HTMLResponse)
async def verify_page(t: str = Query(...)):
    # Validate token exists (don't reveal details if invalid)
    try:
        signer.loads(t, max_age=604800)  # 7 days
    except (BadSignature, SignatureExpired):
        return HTMLResponse("<h2>Enlace inválido o expirado. Comenta de nuevo en el reel.</h2>", status_code=400)
    return VERIFY_PAGE.format(vault_url=VAULT_URL)


@app.post("/verificar")
async def verify_follow(request: Request):
    body = await request.json()
    token = body.get("token", "")

    try:
        ig_user_id = signer.loads(token, max_age=604800)
    except SignatureExpired:
        return JSONResponse({"error": "Enlace expirado. Comenta de nuevo en el reel."})
    except BadSignature:
        return JSONResponse({"error": "Enlace inválido."})

    record = db.get_pending(token)
    if not record:
        # Already verified — resend
        existing = db.get_by_user_id(ig_user_id)
        if existing and existing["verified"]:
            return JSONResponse({"verified": True, "vault_url": VAULT_URL})
        return JSONResponse({"error": "Registro no encontrado. Comenta de nuevo."})

    following = await ig.is_follower(ig_user_id)
    if not following:
        return JSONResponse({"verified": False, "not_following": True})

    db.mark_verified(ig_user_id)
    await _send_vault_link(ig_user_id)
    return JSONResponse({"verified": True, "vault_url": VAULT_URL})


async def _send_vault_link(ig_user_id: str):
    message = (
        "🔓 ¡Acceso desbloqueado!\n\n"
        "Ya eres parte de la comunidad de @claudeprofessor. "
        "Aquí tienes el enlace a la bóveda con todos los recursos:\n\n"
        f"👉 {VAULT_URL}\n\n"
        "¡Guárdalo! Y si te ha gustado, comparte el reel con alguien "
        "que también quiera aprender a usar Claude 🧡"
    )
    try:
        await ig.send_dm(ig_user_id, message)
    except Exception as e:
        print(f"Failed to send vault DM to {ig_user_id}: {e}")


# ── Health ─────────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "account": "@claudeprofessor"}
