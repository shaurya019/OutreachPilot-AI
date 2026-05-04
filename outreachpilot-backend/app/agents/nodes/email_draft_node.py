from app.agents.llm import get_llm
from app.agents.state import ResearchState
from app.schemas.research import EmailDraftOutput


def email_draft_node(state: ResearchState) -> ResearchState:
    company = state.get("company", {})
    employee = state.get("employee", {})
    purpose = state.get("purpose", "job_outreach")

    try:
        llm = get_llm(temperature=0.4)
        structured_llm = llm.with_structured_output(EmailDraftOutput)

        prompt = f"""
You are an outreach drafting agent.

Generate message drafts based on the selected purpose.

Purpose:
{purpose}

Company:
{company}

Employee:
{employee}

User:
{state.get("user", {})}

Company Research:
{state.get("company_research", {})}

Employee Research:
{state.get("employee_research", {})}

Personalization:
{state.get("personalization", {})}

Rules:
- Keep the email concise.
- Do not overclaim.
- Do not mention unverified private facts.
- Make it personalized using the research.
- Use a professional but natural tone.
- approval_status must be pending.
- sent_status must be not_sent.
- sent_at must be null.
- provider_message_id must be null.
"""

        result = structured_llm.invoke(prompt)
        output = result.model_dump()

        output["recipient_email"] = employee.get("email")
        output["approval_status"] = "pending"
        output["sent_status"] = "not_sent"
        output["sent_at"] = None
        output["provider_message_id"] = None

        return {
            "email_draft": output,
        }

    except Exception as exc:
        fallback = EmailDraftOutput(
            recipient_email=employee.get("email"),
            subject=f"Exploring opportunities at {company.get('name', 'your company')}",
            body=f"""Hi {employee.get('name', '')},

I came across {company.get('name', 'your company')} and wanted to reach out.

I have experience in backend systems, AI workflows, LangGraph, OpenAI, and cloud-based applications. I thought this background could be relevant to your team.

Would you be open to a quick conversation?

Best,
Shaurya""",
            linkedin_message=f"Hi {employee.get('name', '')}, I came across {company.get('name', 'your company')} and would love to connect.",
            follow_up_email=f"""Hi {employee.get('name', '')},

Just following up on my previous note. Happy to connect if my background is relevant.

Best,
Shaurya""",
            approval_status="pending",
            sent_status="not_sent",
            sent_at=None,
            provider_message_id=None,
        )

        return {
            "email_draft": fallback.model_dump(),
            "errors": [f"email_draft_node failed: {str(exc)}"],
        }