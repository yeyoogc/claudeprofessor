"""
Email notification for @claudeprofessor preview approval.
Sends HTML email with slide previews + caption to the reviewer.
"""

import yagmail

import config


APPROVAL_SERVER = "http://localhost:5001"


def send_preview_email(topic: str, hosted_urls: list[str], caption: str) -> None:
    slides_html = "\n".join(
        f"""
        <div style="margin-bottom:24px;">
          <p style="margin:0 0 8px;font-size:13px;color:#8B6F4E;font-weight:600;">SLIDE {i}</p>
          <img src="{url}" style="width:100%;max-width:540px;border-radius:12px;display:block;" />
        </div>
        """
        for i, url in enumerate(hosted_urls, 1)
    )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                 background:#FAF9F7;margin:0;padding:32px;">
      <div style="max-width:600px;margin:0 auto;background:#fff;
                  border-radius:20px;padding:40px;box-shadow:0 4px 40px rgba(0,0,0,0.08);">

        <div style="text-align:center;margin-bottom:32px;">
          <div style="font-size:36px;margin-bottom:4px;">✳️</div>
          <div style="color:#D97757;font-size:13px;font-weight:700;
                      letter-spacing:0.08em;text-transform:uppercase;">@claudeprofessor</div>
        </div>

        <h1 style="font-size:20px;color:#1A1816;margin:0 0 8px;">Nuevo carrusel listo para revisar</h1>
        <p style="color:#8B6F4E;font-size:15px;margin:0 0 32px;">
          <strong>Tema:</strong> {topic}
        </p>

        {slides_html}

        <div style="background:#FAF9F7;border-radius:12px;padding:20px;margin-top:32px;">
          <p style="font-size:13px;font-weight:700;color:#1A1816;margin:0 0 8px;">CAPTION</p>
          <p style="font-size:14px;color:#555;line-height:1.6;margin:0;white-space:pre-wrap;">{caption}</p>
        </div>

        <div style="margin-top:32px;padding-top:24px;border-top:1px solid #eee;text-align:center;">
          <p style="font-size:14px;color:#8B6F4E;margin:0 0 12px;">
            El navegador se abre automaticamente para aprobar.
          </p>
          <p style="font-size:13px;color:#aaa;margin:0;">
            Si no: abre <strong>localhost:5001/review</strong> en tu navegador.
          </p>
        </div>

      </div>
    </body>
    </html>
    """

    yag = yagmail.SMTP(config.EMAIL_FROM, config.EMAIL_APP_PASSWORD.replace(" ", ""))
    yag.send(
        to=config.EMAIL_TO,
        subject=f"[ClaudeProfessor] Preview: {topic[:50]}",
        contents=html,
    )
    print(f"Preview email sent to {config.EMAIL_TO}")
