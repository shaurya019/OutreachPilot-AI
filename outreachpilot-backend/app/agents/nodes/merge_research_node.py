from app.agents.llm import get_llm
from app.agents.state import ResearchState
from app.schemas.research import PersonalizationOutput


def personalization_node(state: ResearchState) -> ResearchState:
    try:
        llm = get_llm(temperature=0.3)
        structured_llm = llm.with_structured_output(PersonalizationOutput)

        prompt = f"""
You are a personalization agent.

Connect company research, employee research, website findings, and user profile.
Generate useful personalization hooks and a strong outreach/interview/sales angle.

Purpose:
{state.get("purpose", "job_outreach")}

Company:
{state.get("company", {})}

Employee:
{state.get("employee", {})}

User:
{state.get("user", {})}

Website Research:
{state.get("website_research", {})}

Company Research:
{state.get("company_research", {})}

Employee Research:
{state.get("employee_research", {})}

Rules:
- Make hooks specific but factual.
- Avoid unsupported claims.
- Explain what skills to highlight.
- Explain what to avoid.
- Keep output useful for the selected purpose.
"""

        result = structured_llm.invoke(prompt)

        return {
            "personalization": result.model_dump(),
        }

    except Exception as exc:
        fallback = PersonalizationOutput(
            hooks=[
                "Mention the company's product or engineering direction.",
                "Connect the user's backend and AI experience with company needs.",
                "Keep the message specific and concise.",
            ],
            best_angle="Backend engineering + AI systems + production LLM experience.",
            skills_to_highlight=[
                "FastAPI",
                "LangGraph",
                "OpenAI",
                "AWS",
                "RAG",
            ],
            things_to_avoid=[
                "Avoid unsupported claims.",
                "Avoid over-personalizing based on uncertain information.",
            ],
        )

        return {
            "personalization": fallback.model_dump(),
            "errors": [f"personalization_node failed: {str(exc)}"],
        }