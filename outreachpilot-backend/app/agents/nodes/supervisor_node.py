from app.agents.state import ResearchState


def supervisor_node(state: ResearchState) -> ResearchState:
    purpose = state.get("purpose", "job_outreach")

    final_outputs = ["research_report"]

    if purpose == "job_outreach":
        final_outputs.extend([
            "cold_email",
            "linkedin_message",
            "follow_up_email",
        ])

    elif purpose == "interview_prep":
        final_outputs.extend([
            "interview_prep_notes",
            "questions_to_ask",
            "self_intro",
        ])

    elif purpose == "sales_outreach":
        final_outputs.extend([
            "sales_email",
            "pain_points",
            "follow_up_email",
        ])

    workflow_plan = {
        "run_website_research": True,
        "run_company_research": True,
        "run_employee_research": True,
        "purpose": purpose,
        "final_outputs": final_outputs,
        "safety_rules": [
            "Do not hallucinate private employee details.",
            "Mark uncertain information clearly.",
            "Do not send outreach without user approval.",
            "Use only provided or publicly available information.",
        ],
    }

    return {
        **state,
        "workflow_plan": workflow_plan,
        "errors": state.get("errors", []),
    }