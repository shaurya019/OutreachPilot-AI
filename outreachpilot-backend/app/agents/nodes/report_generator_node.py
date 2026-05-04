from app.agents.llm import get_llm
from app.agents.state import ResearchState

def report_generator_node(state: ResearchState) -> ResearchState:
    company = state.get("company", {})
    employee = state.get("employee", {})
    purpose = state.get("purpose", "job_outreach")

    title = f"Research Report: {company.get('name', 'Company')} + {employee.get('name', 'Employee')}"
    
    try:
        llm = get_llm(temperature=0.3)
        
        prompt = """
            You are a professional report generation agent.
            Create a clean markdown research report for the user.
            
            The report should include:
            
            1. Executive Summary
            2. Company Overview
            3. Website Findings
            4. Employee/Profile Summary
            5. Personalization Hooks
            6. Best Outreach Angle
            7. Suggested Strategy
            8. Suggested Message Direction
            9. Verification Notes
            
            Important:
            - Do not hallucinate facts.
            - Mark uncertain details clearly.
            - Keep the report useful for {purpose}.
            - Use clear headings and bullet points.
            - Mention that outreach should only be sent after user approval.
            
            Company:
            {company}

            Employee:
            {employee}

            User:
            {state.get("user", {})}

            Website Research:
            {state.get("website_research", {})}

            Company Research:
            {state.get("company_research", {})}

            Employee Research:
            {state.get("employee_research", {})}

            Personalization:
            {state.get("personalization", {})}
        """
        
        response = llm.invoke(prompt)
        
        report = {
            "title": title,
            "markdown": response.content,
            "html": None,
            "pdf_url": None,
        }
        return {
           "report" :  report
        }
        
    except Exception as error:
        fallback_report = {
            "title": title,
            "markdown": f"""
        # {title}

        ## Executive Summary

        The report generation step failed.

        ## Error

        {str(exc)}

        ## Available Research

        Company research:
        {state.get("company_research", {})}

        Employee research:
        {state.get("employee_research", {})}
        """.strip(),
                    "html": None,
                    "pdf_url": None,
                }

        return {
            "report": fallback_report,
            "errors": [f"report_generator_node failed: {str(exc)}"],
        }