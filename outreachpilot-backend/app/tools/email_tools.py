from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr, Field

from app.services.email_service import EmailService


class SendApprovedOutreachInput(BaseModel):
    recipient_email: EmailStr
    subject: str = Field(..., min_length=2)
    body: str = Field(..., min_length=5)
    reply_to: Optional[EmailStr] = None
    approval_status: str


class SendApprovedOutreachResult(BaseModel):
    status: str
    provider: str
    provider_message_id: Optional[str] = None
    message: str


class EmailTools:
    def __init__(self):
        self.email_service = EmailService()

    def send_approved_outreach_email(
        self,
        payload: SendApprovedOutreachInput,
    ) -> SendApprovedOutreachResult:
        if payload.approval_status != "approved":
            raise PermissionError(
                "Outreach email cannot be sent without approval_status = approved"
            )

        result = self.email_service.send_email(
            to_email=str(payload.recipient_email),
            subject=payload.subject,
            body=payload.body,
            reply_to=str(payload.reply_to) if payload.reply_to else None,
        )

        return SendApprovedOutreachResult(
            status="sent",
            provider=result["provider"],
            provider_message_id=result.get("provider_message_id"),
            message="Approved outreach email sent successfully.",
        )