"""
Local approval server for @claudeprofessor.

Endpoints:
  POST /preview   — generate + upload + email + open review page
  GET  /review    — review page with slides + approve/reject buttons
  GET  /approve   — publish the last previewed carousel
  GET  /reject    — discard and delete the pending preview
  GET  /status    — check if a preview is pending
"""

import json
import os
import threading
import webbrowser

from flask import Flask, jsonify

PREVIEW_FILE = ".last_preview.json"
PORT = 5001

app = Flask(__name__)
_lock = threading.Lock()


def _run_preview():
    from run import run
    try:
        run(dry_run=False, preview=True)
        # Auto-open review page when done
        webbrowser.open(f"http://localhost:{PORT}/review")
    except Exception as e:
        print(f"[approval_server] Preview error: {e}")


@app.route("/preview", methods=["POST", "GET"])
def preview():
    if _lock.locked():
        return jsonify({"status": "busy", "message": "Preview already running"}), 429
    thread = threading.Thread(target=_run_preview, daemon=True)
    thread.start()
    return jsonify({"status": "started", "message": "Generating preview..."})


@app.route("/review")
def review():
    if not os.path.exists(PREVIEW_FILE):
        return """
        <html><body style="font-family:sans-serif;text-align:center;padding:60px;background:#FAF9F7;">
          <h2 style="color:#1A1816">No hay preview pendiente</h2>
          <p style="color:#8B6F4E">Espera a que termine la generación.</p>
        </body></html>
        """, 404

    with open(PREVIEW_FILE) as f:
        data = json.load(f)

    topic = data.get("topic", "")
    urls = data.get("urls", [])
    caption = data.get("caption", "")

    slides_html = "\n".join(
        f'<img src="{url}" style="width:320px;height:320px;object-fit:cover;border-radius:12px;display:block;margin:0 auto 16px;" />'
        for url in urls
    )

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>ClaudeProfessor — Revisar carrusel</title>
    </head>
    <body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                 background:#FAF9F7;margin:0;padding:32px;">
      <div style="max-width:400px;margin:0 auto;">

        <div style="text-align:center;margin-bottom:24px;">
          <div style="color:#D97757;font-size:13px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;">
            @claudeprofessor
          </div>
          <h1 style="font-size:18px;color:#1A1816;margin:8px 0 0;">{topic}</h1>
        </div>

        {slides_html}

        <div style="background:#fff;border-radius:12px;padding:16px;margin:24px 0;
                    box-shadow:0 2px 12px rgba(0,0,0,0.06);">
          <p style="font-size:11px;font-weight:700;color:#8B6F4E;margin:0 0 8px;
                    text-transform:uppercase;letter-spacing:0.08em;">Caption</p>
          <p style="font-size:13px;color:#333;line-height:1.6;margin:0;
                    white-space:pre-wrap;">{caption}</p>
        </div>

        <div style="display:flex;gap:12px;margin-top:8px;">
          <a href="/approve"
             style="flex:1;display:block;background:#D97757;color:#fff;font-weight:700;
                    font-size:15px;padding:16px;border-radius:10px;text-decoration:none;
                    text-align:center;">
            ✅ Publicar
          </a>
          <a href="/reject"
             style="flex:1;display:block;background:#eee;color:#555;font-weight:600;
                    font-size:15px;padding:16px;border-radius:10px;text-decoration:none;
                    text-align:center;">
            🗑️ Descartar
          </a>
        </div>

      </div>
    </body>
    </html>
    """


@app.route("/approve")
def approve():
    if not os.path.exists(PREVIEW_FILE):
        return "<h2>No hay preview pendiente.</h2>", 404
    try:
        from run import publish_last
        publish_last()
        return """
        <html><body style="font-family:sans-serif;text-align:center;padding:60px;background:#FAF9F7;">
          <div style="font-size:64px;margin-bottom:16px;">✅</div>
          <h2 style="color:#1A1816;margin:0 0 8px;">Publicado en Instagram</h2>
          <p style="color:#8B6F4E;margin:0;">El carrusel ya está en @claudeprofessor.</p>
        </body></html>
        """
    except Exception as e:
        return f"<h2>Error: {e}</h2>", 500


@app.route("/reject")
def reject():
    if os.path.exists(PREVIEW_FILE):
        with open(PREVIEW_FILE) as f:
            data = json.load(f)
        topic = data.get("topic", "?")
        os.remove(PREVIEW_FILE)
        return f"""
        <html><body style="font-family:sans-serif;text-align:center;padding:60px;background:#FAF9F7;">
          <div style="font-size:64px;margin-bottom:16px;">🗑️</div>
          <h2 style="color:#1A1816;margin:0 0 8px;">Preview descartado</h2>
          <p style="color:#8B6F4E;margin:0;">{topic}</p>
        </body></html>
        """
    return "<h2>No hay preview pendiente.</h2>", 404


@app.route("/status")
def status():
    if os.path.exists(PREVIEW_FILE):
        with open(PREVIEW_FILE) as f:
            data = json.load(f)
        return jsonify({"pending": True, "topic": data.get("topic")})
    return jsonify({"pending": False})


if __name__ == "__main__":
    print(f"[ClaudeProfessor] Approval server on http://localhost:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
