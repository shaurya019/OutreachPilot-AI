from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.schemas.research import (
    ActionResponse,
    ResearchReportResponse,
    ResearchStartRequest,
    ResearchStartResponse,
)
from app.services.research_service import ResearchService


router = APIRouter()


@router.post("/start", response_model=ResearchStartResponse)
def start_research(
    payload: ResearchStartRequest,
    background_tasks: BackgroundTasks,
):
    service = ResearchService()

    result = service.start_research(payload)

    background_tasks.add_task(
        service.run_langgraph_research_workflow,
        result["report_id"],
    )

    return result


@router.get("/{report_id}", response_model=ResearchReportResponse)
def get_research_report(report_id: str):
    service = ResearchService()

    report = service.get_report_response(report_id)

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return report


@router.post("/{report_id}/approve", response_model=ActionResponse)
def approve_research_outreach(report_id: str):
    service = ResearchService()

    result = service.approve_outreach(report_id)

    if not result:
        raise HTTPException(status_code=404, detail="Email draft not found")

    return result


@router.post("/{report_id}/reject", response_model=ActionResponse)
def reject_research_outreach(report_id: str):
    service = ResearchService()

    result = service.reject_outreach(report_id)

    if not result:
        raise HTTPException(status_code=404, detail="Email draft not found")

    return result