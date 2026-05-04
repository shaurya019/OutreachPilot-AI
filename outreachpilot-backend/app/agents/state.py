import operator
from typing import Annotated, Any, Dict, List, TypedDict


class ResearchState(TypedDict, total=False):
    report_id: str
    purpose: str

    company: Dict[str, Any]
    employee: Dict[str, Any]
    user: Dict[str, Any]

    workflow_plan: Dict[str, Any]

    website_research: Dict[str, Any]
    company_research: Dict[str, Any]
    employee_research: Dict[str, Any]
    merged_research: Dict[str, Any]

    personalization: Dict[str, Any]
    report: Dict[str, Any]
    email_draft: Dict[str, Any]
    reviewer: Dict[str, Any]

    metadata: Dict[str, Any]

    errors: Annotated[List[str], operator.add]