from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

from app.services.email_service import EmailService


mcp = FastMCP("outreachpilot-email-tools")


@mcp.tool()
def send_approved_outreach_email(
    recipient_email: str,
    subject: str,
    body: str,
    reply_to: Optional[str] = None,
    approval_status: str = "pending",
) -> Dict[str, Any]:
    """
    Send an outreach email only after explicit user approval.

    Safety rule:
    - This tool must only send when approval_status is exactly 'approved'.
    - It should be called only from the approve endpoint after the user clicks approve.
    """

    if approval_status != "approved":
        raise ValueError(
            "Email cannot be sent because approval_status is not approved."
        )

    if not recipient_email:
        raise ValueError("recipient_email is required")

    if not subject:
        raise ValueError("subject is required")

    if not body:
        raise ValueError("body is required")

    email_service = EmailService()

    result = email_service.send_email(
        to_email=recipient_email,
        subject=subject,
        body=body,
        reply_to=reply_to,
    )

    return {
        "status": "sent",
        "provider": result.get("provider"),
        "provider_message_id": result.get("provider_message_id"),
        "message": "Approved outreach email sent successfully.",
    }


@mcp.tool()
def send_report_email_to_user(
    user_email: str,
    subject: str,
    body: str,
    pdf_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send the generated research report summary to the user.

    This does not send outreach to the employee.
    It only sends the report information to the user.
    """

    if not user_email:
        raise ValueError("user_email is required")

    if not subject:
        raise ValueError("subject is required")

    if not body:
        raise ValueError("body is required")

    final_body = body

    if pdf_url:
        final_body += f"\n\nPDF Report:\n{pdf_url}"

    email_service = EmailService()

    result = email_service.send_email(
        to_email=user_email,
        subject=subject,
        body=final_body,
    )

    return {
        "status": "sent",
        "provider": result.get("provider"),
        "provider_message_id": result.get("provider_message_id"),
        "message": "Research report email sent to user successfully.",
    }


if __name__ == "__main__":
    mcp.run()