import os
from typing import Any, Dict, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class EmailMCPClient:
    def __init__(self):
        self.server_params = StdioServerParameters(
            command="python",
            args=["-m", "app.mcp.email_mcp_server"],
            env=os.environ.copy(),
        )

    async def send_approved_outreach_email(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        reply_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "send_approved_outreach_email",
                    arguments={
                        "recipient_email": recipient_email,
                        "subject": subject,
                        "body": body,
                        "reply_to": reply_to,
                        "approval_status": "approved",
                    },
                )

                return self._extract_tool_result(result)

    async def send_report_email_to_user(
        self,
        user_email: str,
        subject: str,
        body: str,
        pdf_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "send_report_email_to_user",
                    arguments={
                        "user_email": user_email,
                        "subject": subject,
                        "body": body,
                        "pdf_url": pdf_url,
                    },
                )

                return self._extract_tool_result(result)

    @staticmethod
    def _extract_tool_result(result: Any) -> Dict[str, Any]:
        """
        MCP SDK tool results can contain structuredContent or content blocks
        depending on SDK/client version. This normalizes the response.
        """

        if hasattr(result, "structuredContent") and result.structuredContent:
            return result.structuredContent

        if hasattr(result, "structured_content") and result.structured_content:
            return result.structured_content

        if hasattr(result, "content") and result.content:
            first = result.content[0]

            if hasattr(first, "text"):
                return {
                    "status": "sent",
                    "message": first.text,
                    "provider_message_id": None,
                }

            return {
                "status": "sent",
                "message": str(first),
                "provider_message_id": None,
            }

        return {
            "status": "sent",
            "message": "Tool executed successfully.",
            "provider_message_id": None,
        }