from typing import Any, Dict, Optional

from botocore.exceptions import ClientError

from app.db.dynamodb import get_reports_table
from app.utils.time import utc_now_iso


class ReportRepository:
    def __init__(self):
        self.table = get_reports_table()

    def create_report_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        self.table.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(report_id)",
        )
        return item

    def get_report_by_id(self, report_id: str) -> Optional[Dict[str, Any]]:
        response = self.table.get_item(
            Key={"report_id": report_id}
        )
        return response.get("Item")

    def update_report_status(
        self,
        report_id: str,
        status: str,
        error_message: Optional[str] = None,
    ) -> Dict[str, Any]:
        updated_at = utc_now_iso()

        update_expression = "SET #status = :status, updated_at = :updated_at"
        expression_attribute_names = {
            "#status": "status",
        }
        expression_attribute_values = {
            ":status": status,
            ":updated_at": updated_at,
        }

        if error_message:
            update_expression += ", metadata.error_message = :error_message"
            expression_attribute_values[":error_message"] = error_message

        response = self.table.update_item(
            Key={"report_id": report_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW",
        )

        return response["Attributes"]

    def save_workflow_result(
        self,
        report_id: str,
        agent_outputs: Dict[str, Any],
        report: Dict[str, Any],
        email_draft: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        updated_at = utc_now_iso()

        response = self.table.update_item(
            Key={"report_id": report_id},
            UpdateExpression="""
                SET 
                    #status = :status,
                    agent_outputs = :agent_outputs,
                    report = :report,
                    email_draft = :email_draft,
                    metadata = :metadata,
                    updated_at = :updated_at
            """,
            ExpressionAttributeNames={
                "#status": "status",
            },
            ExpressionAttributeValues={
                ":status": "completed",
                ":agent_outputs": agent_outputs,
                ":report": report,
                ":email_draft": email_draft,
                ":metadata": metadata or {},
                ":updated_at": updated_at,
            },
            ReturnValues="ALL_NEW",
        )

        return response["Attributes"]

    def mark_outreach_sent(
        self,
        report_id: str,
        provider_message_id: Optional[str],
    ) -> Optional[Dict[str, Any]]:
        updated_at = utc_now_iso()

        try:
            response = self.table.update_item(
                Key={"report_id": report_id},
                UpdateExpression="""
                    SET 
                        email_draft.approval_status = :approval_status,
                        email_draft.sent_status = :sent_status,
                        email_draft.sent_at = :sent_at,
                        email_draft.provider_message_id = :provider_message_id,
                        updated_at = :updated_at
                """,
                ExpressionAttributeValues={
                    ":approval_status": "approved",
                    ":sent_status": "sent",
                    ":sent_at": updated_at,
                    ":provider_message_id": provider_message_id,
                    ":updated_at": updated_at,
                },
                ConditionExpression="attribute_exists(report_id)",
                ReturnValues="ALL_NEW",
            )

            return response["Attributes"]

        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return None
            raise

    def mark_outreach_failed(
        self,
        report_id: str,
        error_message: str,
    ) -> Optional[Dict[str, Any]]:
        updated_at = utc_now_iso()

        try:
            response = self.table.update_item(
                Key={"report_id": report_id},
                UpdateExpression="""
                    SET 
                        email_draft.approval_status = :approval_status,
                        email_draft.sent_status = :sent_status,
                        metadata.error_message = :error_message,
                        updated_at = :updated_at
                """,
                ExpressionAttributeValues={
                    ":approval_status": "approved",
                    ":sent_status": "failed",
                    ":error_message": error_message,
                    ":updated_at": updated_at,
                },
                ConditionExpression="attribute_exists(report_id)",
                ReturnValues="ALL_NEW",
            )

            return response["Attributes"]

        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return None
            raise

    def reject_outreach(self, report_id: str) -> Optional[Dict[str, Any]]:
        updated_at = utc_now_iso()

        try:
            response = self.table.update_item(
                Key={"report_id": report_id},
                UpdateExpression="""
                    SET 
                        email_draft.approval_status = :approval_status,
                        email_draft.sent_status = :sent_status,
                        updated_at = :updated_at
                """,
                ExpressionAttributeValues={
                    ":approval_status": "rejected",
                    ":sent_status": "not_sent",
                    ":updated_at": updated_at,
                },
                ConditionExpression="attribute_exists(report_id)",
                ReturnValues="ALL_NEW",
            )

            return response["Attributes"]

        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return None
            raise