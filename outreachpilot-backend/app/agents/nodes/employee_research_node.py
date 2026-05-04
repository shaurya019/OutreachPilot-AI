from app.agents.llm import get_llm
from app.agents.state import ResearchState
from app.schemas.research import EmployeeResearchOutput

def employee_research_node(state:ResearchState) ->ResearchState:
    employee = state.get("employee", {})
    purpose = state.get("purpose", "job_outreach")
    
    try:
        llm = get_llm(temperature=0.2)
        structured_llm = llm.with_structured_output(EmployeeResearchOutput)
        
        prompt ="""
        You are an employee research agent.

        Analyze the provided employee information.

        Rules:
        - Use only provided employee name, email, LinkedIn URL, and profile text.
        - Do not claim private information.
        - If role, seniority, or department is unclear, return null.
        - Generate useful personalization clues.
        - Do not over-personalize from weak data.

        Employee input:
        {employee}

        Purpose:
        {purpose}
        """
        
        result = structured_llm.invoke(prompt)
        return {
            "employee_research": result.model_dump(),
        }
        
    except Exception as error:
        fallback = EmployeeResearchOutput(
            summary=f"{employee.get('name', 'The employee')} is the target contact.",
            role=None,
            seniority=None,
            department=None,
            likely_responsibilities=[],
            personalization_clues=[],
        )
        
        return {
            "employee_research": fallback.model_dump(),
            "errors": [f"employee_research_node failed: {str(error)}"],
        }
        