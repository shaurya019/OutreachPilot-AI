import uuid
from typing import Any, Dict, Optional

from app.agents.graph import run_research_graph
from app.repositories.report_repository import ReportRepository
from app.schemas.research import ResearchStartRequest
from app.utils.time import utc_now_iso


class ResearchService:
    def __init__(self):
        self.repository = ReportRepository()

    def start_research(self, payload: ResearchStartRequest) -> Dict[str, Any]:
        report_id = str(uuid.uuid4())
        now = utc_now_iso()

        item = {
            "report_id": report_id,
            "status": "running",
            "purpose": payload.purpose,
            "company": {
                "name": payload.company_name,
                "website": payload.company_website,
                "linkedin": payload.company_linkedin,
            },
            "employee": {
                "name": payload.employee_name,
                "linkedin": payload.employee_linkedin,
                "email": str(payload.employee_email) if payload.employee_email else None,
                "profile_text": payload.employee_profile_text,
            },
            "user": {
                "email": str(payload.user_email),
                "profile": payload.user_profile,
            },
            "agent_outputs": {},
            "report": {},
            "email_draft": {
                "recipient_email": str(payload.employee_email) if payload.employee_email else None,
                "subject": None,
                "body": None,
                "linkedin_message": None,
                "follow_up_email": None,
                "approval_status": "pending",
                "sent_status": "not_sent",
                "sent_at": None,
                "provider_message_id": None,
            },
            "metadata": {
                "model": None,
                "tokens_used": None,
                "cost_estimate": None,
                "workflow_version": "v1",
                "error_message": None,
            },
            "created_at": now,
            "updated_at": now,
        }

        self.repository.create_report_item(item)

        return {
            "report_id": report_id,
            "status": "running",
        }

    def run_langgraph_research_workflow(self, report_id: str) -> None:
        item = self.repository.get_report_by_id(report_id)

        if not item:
            return

        try:
            initial_state = {
                "report_id": item["report_id"],
                "purpose": item["purpose"],
                "company": item["company"],
                "employee": item["employee"],
                "user": item["user"],
                "workflow_plan": {},
                "website_research": {},
                "company_research": {},
                "employee_research": {},
                "merged_research": {},
                "personalization": {},
                "report": {},
                "email_draft": item.get("email_draft", {}),
                "reviewer": {},
                "metadata": {},
                "errors": [],
            }

            final_state = run_research_graph(initial_state)

            agent_outputs = {
                "website_research": final_state.get("website_research", {}),
                "company_research": final_state.get("company_research", {}),
                "employee_research": final_state.get("employee_research", {}),
                "personalization": final_state.get("personalization", {}),
                "reviewer": final_state.get("reviewer", {}),
            }

            report = final_state.get("report", {})
            email_draft = final_state.get("email_draft", {})
            metadata = final_state.get("metadata", {})

            errors = final_state.get("errors", [])

            if errors:
                metadata["error_message"] = "; ".join(errors)

            self.repository.save_workflow_result(
                report_id=report_id,
                agent_outputs=agent_outputs,
                report=report,
                email_draft=email_draft,
                metadata=metadata,
            )

        except Exception as exc:
            self.repository.update_report_status(
                report_id=report_id,
                status="failed",
                error_message=str(exc),
            )

    def get_report_response(self, report_id: str) -> Optional[Dict[str, Any]]:
        item = self.repository.get_report_by_id(report_id)

        if not item:
            return None

        return self.map_dynamodb_item_to_response(item)

    def approve_outreach(self, report_id: str) -> Optional[Dict[str, str]]:
        updated_item = self.repository.approve_outreach(report_id)

        if not updated_item:
            return None

        return {
            "status": "approved",
            "message": "Outreach email approved. Mock email sent successfully.",
        }

    def reject_outreach(self, report_id: str) -> Optional[Dict[str, str]]:
        updated_item = self.repository.reject_outreach(report_id)

        if not updated_item:
            return None

        return {
            "status": "rejected",
            "message": "Outreach email rejected and was not sent.",
        }

    @staticmethod
    def map_dynamodb_item_to_response(item: Dict[str, Any]) -> Dict[str, Any]:
        agent_outputs = item.get("agent_outputs", {})

        company_research = agent_outputs.get("company_research", {})
        employee_research = agent_outputs.get("employee_research", {})
        website_research = agent_outputs.get("website_research", {})
        personalization = agent_outputs.get("personalization", {})
        reviewer = agent_outputs.get("reviewer", {})

        report = item.get("report", {})
        email_draft = item.get("email_draft", {})

        company = item.get("company", {})
        employee = item.get("employee", {})

        return {
            "report_id": item.get("report_id"),
            "status": item.get("status", "pending"),

            "company_name": company.get("name", ""),
            "employee_name": employee.get("name", ""),

            "company_summary": company_research.get("summary"),
            "employee_summary": employee_research.get("summary"),

            "website_findings": website_research.get("findings", []),
            "personalization_hooks": personalization.get("hooks", []),

            "best_outreach_angle": personalization.get("best_angle"),
            "report_markdown": report.get("markdown"),

            "cold_email_subject": email_draft.get("subject"),
            "cold_email_body": email_draft.get("body"),
            "linkedin_message": email_draft.get("linkedin_message"),
            "follow_up_email": email_draft.get("follow_up_email"),

            "reviewer_feedback": reviewer.get("feedback"),
            "confidence_score": reviewer.get("confidence_score"),

            "approval_status": email_draft.get("approval_status", "pending"),
            "sent_status": email_draft.get("sent_status", "not_sent"),
        }