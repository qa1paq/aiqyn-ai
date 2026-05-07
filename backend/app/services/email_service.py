import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.config import settings


def send_reset_code(to_email: str, code: str, full_name: str) -> bool:
    if not settings.GMAIL_USER or not settings.GMAIL_APP_PASSWORD:
        print(f"\n{'='*40}")
        print(f"[DEV] Password reset code for {to_email}: {code}")
        print(f"{'='*40}\n")
        return True

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:480px;margin:0 auto;
                background:#0F172A;color:#F8FAFC;padding:32px;border-radius:16px">
      <h1 style="color:#6366F1;margin-bottom:8px">AIQYN AI</h1>
      <p style="color:#94A3B8">Привет, {full_name}!</p>
      <p>Твой код для восстановления пароля:</p>
      <div style="background:#1E293B;border-radius:12px;padding:24px;
                  text-align:center;margin:24px 0">
        <span style="font-size:40px;font-weight:900;letter-spacing:14px;
                     color:#6366F1">{code}</span>
      </div>
      <p style="color:#64748B;font-size:13px">
        Код действителен <strong>15 минут</strong>.<br>
        Если ты не запрашивал восстановление — просто игнорируй это письмо.
      </p>
      <hr style="border-color:#1E293B;margin:24px 0">
      <p style="color:#334155;font-size:12px">AIQYN AI — AI-путеводитель в зарубежные университеты</p>
    </div>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Твой код восстановления: {code}"
    msg["From"] = f"AIQYN AI <{settings.GMAIL_USER}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(settings.GMAIL_USER, settings.GMAIL_APP_PASSWORD)
            server.sendmail(settings.GMAIL_USER, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False
