import httpx
from app.core.config import settings


def send_reset_code(to_email: str, code: str, full_name: str) -> bool:
    if not settings.MAILJET_API_KEY or not settings.MAILJET_SECRET_KEY:
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

    try:
        response = httpx.post(
            "https://api.mailjet.com/v3.1/send",
            auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY),
            json={
                "Messages": [
                    {
                        "From": {"Email": "aiqynaii@gmail.com", "Name": "AIQYN AI"},
                        "To": [{"Email": to_email}],
                        "Subject": f"Твой код восстановления: {code}",
                        "HTMLPart": html,
                    }
                ]
            },
            timeout=15,
        )
        if response.status_code == 200:
            return True
        print(f"Mailjet error: {response.status_code} — {response.text}")
        return False
    except Exception as e:
        print(f"Email error: {e}")
        return False
