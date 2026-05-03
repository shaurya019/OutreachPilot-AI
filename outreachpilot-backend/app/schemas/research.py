from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, EmailStr, Field

ResearchStatus = Literal["pending","running", "completed", "failed"]
ResearchPurpose = Literal["job_outreach", "interview_prep", "sales_outreach"]
ApprovalStatus = Literal["pending", "approved", "rejected"]
SentStatus = Literal["not_sent", "sent", "failed"]

class CompanyInput(BaseModel):
    name: str = Field(..., min_length=2)
    website: str = Field(..., min_length=5)
    linkedin: Optional[str] = None
    
class EmployeeInput(BaseModel):
    name: str = Field(..., min_length=2)
    linkedin: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_text: Optional[str] = None
    
class UserInput(BaseModel):
    email: EmailStr
    profile: Optional[str] = None
    
class ResearchStartRequest(BaseModel):
    company_name: str = Field(..., min_length=2)
    company_website: str = Field(..., min_length=5)
    company_linkedin: Optional[str] = None

    employee_name: str = Field(..., min_length=2)
    employee_linkedin: Optional[str] = None
    employee_email: Optional[EmailStr] = None
    employee_profile_text: Optional[str] = None

    user_email: EmailStr
    user_profile: Optional[str] = None

    purpose: ResearchPurpose
    
class ResearchStartResponse(BaseModel):
    report_id: str
    status: ResearchStatus

class WebsiteResearchOutput(BaseModel):
    raw_text_preview: Optional[str] = None
    findings: List[str] = []
    important_pages: List[str] = []
    error: Optional[str] = None


class CompanyResearchOutput(BaseModel):
    summary: Optional[str] = None
    industry: Optional[str] = None
    products: List[str] = []
    target_customers: List[str] = []
    business_model: Optional[str] = None
    ai_engineering_relevance: Optional[str] = None


class EmployeeResearchOutput(BaseModel):
    summary: Optional[str] = None
    role: Optional[str] = None
    seniority: Optional[str] = None
    department: Optional[str] = None
    likely_responsibilities: List[str] = []
    personalization_clues: List[str] = []


class PersonalizationOutput(BaseModel):
    hooks: List[str] = []
    best_angle: Optional[str] = None
    skills_to_highlight: List[str] = []
    things_to_avoid: List[str] = []


class ReviewerOutput(BaseModel):
    feedback: Optional[str] = None
    quality_score: Optional[float] = None
    confidence_score: Optional[float] = None
    approved: bool = False
    issues: List[str] = []


class AgentOutputs(BaseModel):
    website_research: WebsiteResearchOutput = WebsiteResearchOutput()
    company_research: CompanyResearchOutput = CompanyResearchOutput()
    employee_research: EmployeeResearchOutput = EmployeeResearchOutput()
    personalization: PersonalizationOutput = PersonalizationOutput()
    reviewer: ReviewerOutput = ReviewerOutput()


class ReportOutput(BaseModel):
    title: Optional[str] = None
    markdown: Optional[str] = None
    html: Optional[str] = None
    pdf_url: Optional[str] = None


class EmailDraftOutput(BaseModel):
    recipient_email: Optional[EmailStr] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    linkedin_message: Optional[str] = None
    follow_up_email: Optional[str] = None
    approval_status: ApprovalStatus = "pending"
    sent_status: SentStatus = "not_sent"
    sent_at: Optional[str] = None
    provider_message_id: Optional[str] = None


class MetadataOutput(BaseModel):
    model: Optional[str] = None
    tokens_used: Optional[int] = None
    cost_estimate: Optional[float] = None
    workflow_version: str = "v1"
    error_message: Optional[str] = None


class ResearchDocument(BaseModel):
    report_id: str

    status: ResearchStatus
    purpose: ResearchPurpose

    company: CompanyInput
    employee: EmployeeInput
    user: UserInput

    agent_outputs: AgentOutputs = AgentOutputs()
    report: ReportOutput = ReportOutput()
    email_draft: EmailDraftOutput = EmailDraftOutput()
    metadata: MetadataOutput = MetadataOutput()

    created_at: str
    updated_at: str


class ResearchReportResponse(BaseModel):
    report_id: str
    status: ResearchStatus

    company_name: str
    employee_name: str

    company_summary: Optional[str] = None
    employee_summary: Optional[str] = None

    website_findings: List[str] = []
    personalization_hooks: List[str] = []

    best_outreach_angle: Optional[str] = None
    report_markdown: Optional[str] = None

    cold_email_subject: Optional[str] = None
    cold_email_body: Optional[str] = None
    linkedin_message: Optional[str] = None
    follow_up_email: Optional[str] = None

    reviewer_feedback: Optional[str] = None
    confidence_score: Optional[float] = None

    approval_status: ApprovalStatus = "pending"
    sent_status: SentStatus = "not_sent"


class ActionResponse(BaseModel):
    status: str
    message: str