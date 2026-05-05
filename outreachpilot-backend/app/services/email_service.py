from typing import Any, Dict, Optional

import resend

from app.config import settings


class EmailService:
    def __init__(self):
        resend.api_key = settings.RESEND_API_KEY
        self.email_from = settings.EMAIL_FROM

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        reply_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not to_email:
            raise ValueError("Recipient email is required")

        if not subject:
            raise ValueError("Email subject is required")

        if not body:
            raise ValueError("Email body is required")

        params: Dict[str, Any] = {
            "from": self.email_from,
            "to": [to_email],
            "subject": subject,
            "text": body,
        }

        if reply_to:
            params["reply_to"] = reply_to

        response = resend.Emails.send(params)

        return {
            "status": "sent",
            "provider": "resend",
            "provider_message_id": response.get("id"),
            "raw_response": response,
        }