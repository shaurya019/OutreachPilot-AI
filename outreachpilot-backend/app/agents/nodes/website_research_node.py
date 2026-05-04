import json
from typing import Any, Dict

from app.agents.llm import get_llm
from app.agents.state import ResearchState
from app.services.website_extractor import extract_company_website_context



def safe_json_loads(content: str) -> Dict[str, Any]:
    try:
        content = content.strip()

        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()

        return json.loads(content)
    except Exception:
        return {}
    
def website_research_node(state: ResearchState) -> ResearchState:
    company = state.get("company",{})
    company_website = company.get("website")
    
    if not company_website:
        return {
            "website_research": {
                "raw_text_preview": None,
                "findings": [],
                "important_pages": [],
                "error": "Company website is missing.",
            }
        }
    
    website_context = extract_company_website_context(company_website)
    llm = get_llm(temperature=0.1)
    
    prompt = f"""
    You are a website research agent.
    Analyze the company website text and extract useful finding for outreach or interview preparation.
    Return ONLY valid JSON with this shape:
    {{
        "raw_text_preview": "short preview of the website content",
        "findings": ["finding 1", "finding 2", "finding 3"],
        "important_pages": ["url 1", "url 2"],
        "error": null
    }}
    
    Company : {company}
    
    Website text:
    {website_context.get("combined_text", "")[:10000]}

    Important pages:
    {website_context.get("important_pages", [])}

    Errors:
    {website_context.get("errors", [])}
    """
    
    response = llm.invoke(prompt)
    parsed = safe_json_loads(response.content)
    
    if not parsed:
        parsed = {
            "raw_text_preview": website_context.get("combined_text", "")[:500],
            "findings": [
                "Website content was extracted but structured analysis failed."
            ],
            "important_pages": website_context.get("important_pages", []),
            "error": None,
        }
        
    return {
        "website_research": parsed
    }