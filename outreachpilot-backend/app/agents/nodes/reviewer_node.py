from app.agents.llm import get_llm
from app.agents.state import ResearchState
from app.schemas.research import ReviewerOutput

def reviewer_node(state: ResearchState) -> ResearchState:
    
    try:
        
        llm = get_llm(temperature=0.1)
        structured_llm = llm.with_structured_output(ReviewerOutput)
        
        prompt = """
        You are a reviewer and safety guardrail agent.

        Review the generated report and outreach draft.

        Check:
        1. Is the message professional?
        2. Is it too generic?
        3. Are there unsupported claims?
        4. Are uncertain facts clearly handled?
        5. Is it safe to show to the user?
        6. Should the user verify anything before sending?

        Report:
        {state.get("report", {})}

        Email Draft:
        {state.get("email_draft", {})}

        Personalization:
        {state.get("personalization", {})}

        Website Research:
        {state.get("website_research", {})}

        Employee Research:
        {state.get("employee_research", {})}

        Rules:
        - approved should mean safe to show to user, not automatically safe to send.
        - Always include issues if manual verification is needed.
        - confidence_score should reflect factual confidence.
        - quality_score should reflect writing quality.
        
        """
        
        
        response = structured_llm.invoke(prompt)
        metadata = {
            "model": "gpt-4o-mini",
            "tokens_used": None,
            "cost_estimate": None,
            "workflow_version": "v1",
            "error_message": None,
        }

        return {
            "reviewer": response.model_dump(),
            "metadata": metadata,
        }
        
    except Exception as exc:
        fallback = ReviewerOutput(
            feedback="Reviewer failed. Manual review is recommended.",
            quality_score=6.0,
            confidence_score=5.0,
            approved=False,
            issues=[
                "Reviewer node failed.",
                str(exc),
            ],
        )

        metadata = {
            "model": "gpt-4o-mini",
            "tokens_used": None,
            "cost_estimate": None,
            "workflow_version": "v1",
            "error_message": str(exc),
        }

        return {
            "reviewer": fallback.model_dump(),
            "metadata": metadata,
            "errors": [f"reviewer_node failed: {str(exc)}"],
        }
        