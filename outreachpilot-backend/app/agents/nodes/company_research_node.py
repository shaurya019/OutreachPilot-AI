from app.agents.llm import get_llm
from app.agents.state import ResearchState
from app.schemas.research import CompanyResearchOutput


def company_research_node(state: ResearchState) -> ResearchState:
    company = state.get("company", {})
    purpose = state.get("purpose", "job_outreach")

    try:
        llm = get_llm(temperature=0.2)
        structured_llm = llm.with_structured_output(CompanyResearchOutput)

        prompt = f"""
            You are a company research agent.

            Infer a clear company summary from the provided company information.

            Rules:
            - Do not invent private facts.
            - If something is uncertain, keep it generic or null.
            - Focus on what is useful for the selected purpose.
            - Extract product, industry, customer, business model, and AI/backend relevance where possible.

            Company input:
            {company}

            Purpose:
            {purpose}
        """

        result = structured_llm.invoke(prompt)

        return {
            "company_research": result.model_dump(),
        }

    except Exception as exc:
        fallback = CompanyResearchOutput(
            summary=f"{company.get('name', 'The company')} is being researched for {purpose}.",
            industry=None,
            products=[],
            target_customers=[],
            business_model=None,
            ai_engineering_relevance=None,
        )

        return {
            "company_research": fallback.model_dump(),
            "errors": [f"company_research_node failed: {str(exc)}"],
        }