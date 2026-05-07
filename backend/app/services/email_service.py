import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def send_reset_code(to_email: str, code: str, full_name: str) -> bool:
    """Send password reset code via email. Returns True on success."""
    if not settings.SMTP_HOST or not settings.SMTP_USER:
        # Dev mode: just print the code to console
        print(f"\n{'='*40}")
        print(f"[DEV] Password reset code for {to_email}: {code}")
        print(f"{'='*40}\n")
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "AIQYN AI — Код восстановления пароля"
        msg["From"] = settings.SMTP_USER
        msg["To"] = to_email

        html = f"""
        <div style="font-family:Arial,sans-serif;max-width:480px;margin:0 auto;background:#0F172A;color:#F8FAFC;padding:32px;border-radius:16px">
          <h1 style="color:#6366F1;margin-bottom:8px">AIQYN AI</h1>
          <p style="color:#94A3B8">Привет, {full_name}!</p>
          <p>Твой код для восстановления пароля:</p>
          <div style="background:#1E293B;border-radius:12px;padding:24px;text-align:center;margin:24px 0">
            <span style="font-size:36px;font-weight:900;letter-spacing:12px;color:#6366F1">{code}</span>
          </div>
          <p style="color:#64748B;font-size:13px">Код действителен 15 минут.<br>Если ты не запрашивал восстановление — просто игнорируй это письмо.</p>
        </div>
        """

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, to_email, msg.as_string())
        return True

    except Exception as e:
        print(f"Email error: {e}")
        return False
