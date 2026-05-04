from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field


# -----------------------------
# Common Literal Types
# -----------------------------

ResearchStatus = Literal["pending", "running", "completed", "failed"]

ResearchPurpose = Literal[
    "job_outreach",
    "interview_prep",
    "sales_outreach",
]

ApprovalStatus = Literal[
    "pending",
    "approved",
    "rejected",
]

SentStatus = Literal[
    "not_sent",
    "sent",
    "failed",
]


# -----------------------------
# API Request Schemas
# -----------------------------

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


class ActionResponse(BaseModel):
    status: str
    message: str


# -----------------------------
# Agent Structured Output Schemas
# -----------------------------

class WebsiteResearchOutput(BaseModel):
    raw_text_preview: Optional[str] = Field(
        default=None,
        description="Short preview of extracted website text.",
    )

    findings: List[str] = Field(
        default_factory=list,
        description="Useful website findings for outreach, interview prep, or sales research.",
    )

    important_pages: List[str] = Field(
        default_factory=list,
        description="Important website pages used during research.",
    )

    error: Optional[str] = Field(
        default=None,
        description="Website extraction or analysis error, if any.",
    )


class CompanyResearchOutput(BaseModel):
    summary: Optional[str] = Field(
        default=None,
        description="Clear summary of what the company does.",
    )

    industry: Optional[str] = Field(
        default=None,
        description="Company industry or market category.",
    )

    products: List[str] = Field(
        default_factory=list,
        description="Main products, services, or platform offerings.",
    )

    target_customers: List[str] = Field(
        default_factory=list,
        description="Likely target users, customers, or business segments.",
    )

    business_model: Optional[str] = Field(
        default=None,
        description="Business model, if inferable from available information.",
    )

    ai_engineering_relevance: Optional[str] = Field(
        default=None,
        description="Why this company is relevant for AI, backend, cloud, or engineering outreach.",
    )


class EmployeeResearchOutput(BaseModel):
    summary: Optional[str] = Field(
        default=None,
        description="Short summary of the employee based only on provided information.",
    )

    role: Optional[str] = Field(
        default=None,
        description="Employee role/title if available or inferable.",
    )

    seniority: Optional[str] = Field(
        default=None,
        description="Seniority level such as recruiter, engineer, manager, director, founder, etc.",
    )

    department: Optional[str] = Field(
        default=None,
        description="Likely department such as engineering, recruiting, product, sales, etc.",
    )

    likely_responsibilities: List[str] = Field(
        default_factory=list,
        description="Likely responsibilities based only on provided public/profile information.",
    )

    personalization_clues: List[str] = Field(
        default_factory=list,
        description="Useful clues for personalizing outreach to this employee.",
    )


class PersonalizationOutput(BaseModel):
    hooks: List[str] = Field(
        default_factory=list,
        description="Specific personalization hooks that can be used in the message/report.",
    )

    best_angle: Optional[str] = Field(
        default=None,
        description="Best outreach/interview/sales angle based on company, employee, and user profile.",
    )

    skills_to_highlight: List[str] = Field(
        default_factory=list,
        description="User skills or experiences that should be highlighted.",
    )

    things_to_avoid: List[str] = Field(
        default_factory=list,
        description="Claims, assumptions, or tone choices to avoid.",
    )


class EmailDraftOutput(BaseModel):
    recipient_email: Optional[EmailStr] = Field(
        default=None,
        description="Target employee/prospect email address.",
    )

    subject: Optional[str] = Field(
        default=None,
        description="Email subject line.",
    )

    body: Optional[str] = Field(
        default=None,
        description="Main outreach email body.",
    )

    linkedin_message: Optional[str] = Field(
        default=None,
        description="Short LinkedIn connection or DM message.",
    )

    follow_up_email: Optional[str] = Field(
        default=None,
        description="Follow-up email if there is no response.",
    )

    approval_status: ApprovalStatus = Field(
        default="pending",
        description="Approval status. Must remain pending until user approves.",
    )

    sent_status: SentStatus = Field(
        default="not_sent",
        description="Email sending status.",
    )

    sent_at: Optional[str] = Field(
        default=None,
        description="ISO datetime string when email was sent.",
    )

    provider_message_id: Optional[str] = Field(
        default=None,
        description="Email provider message ID after sending.",
    )


class ReviewerOutput(BaseModel):
    feedback: Optional[str] = Field(
        default=None,
        description="Reviewer feedback on report and email draft quality/safety.",
    )

    quality_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=10,
        description="Writing and usefulness quality score from 0 to 10.",
    )

    confidence_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=10,
        description="Factual confidence score from 0 to 10.",
    )

    approved: bool = Field(
        default=False,
        description="Whether the output is safe to show to user. This does not mean send email automatically.",
    )

    issues: List[str] = Field(
        default_factory=list,
        description="Issues, risks, or manual verification notes.",
    )


# Optional: if you later want structured report output too.
# For now, report_generator_node can generate Markdown text directly.
class ReportOutput(BaseModel):
    title: Optional[str] = None
    markdown: Optional[str] = None
    html: Optional[str] = None
    pdf_url: Optional[str] = None


# -----------------------------
# Full DynamoDB Document Schema
# Optional but useful for validation/documentation
# -----------------------------

class CompanyInput(BaseModel):
    name: str
    website: str
    linkedin: Optional[str] = None


class EmployeeInput(BaseModel):
    name: str
    linkedin: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_text: Optional[str] = None


class UserInput(BaseModel):
    email: EmailStr
    profile: Optional[str] = None


class AgentOutputs(BaseModel):
    website_research: WebsiteResearchOutput = Field(
        default_factory=WebsiteResearchOutput
    )

    company_research: CompanyResearchOutput = Field(
        default_factory=CompanyResearchOutput
    )

    employee_research: EmployeeResearchOutput = Field(
        default_factory=EmployeeResearchOutput
    )

    personalization: PersonalizationOutput = Field(
        default_factory=PersonalizationOutput
    )

    reviewer: ReviewerOutput = Field(
        default_factory=ReviewerOutput
    )


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

    agent_outputs: AgentOutputs = Field(default_factory=AgentOutputs)
    report: ReportOutput = Field(default_factory=ReportOutput)
    email_draft: EmailDraftOutput = Field(default_factory=EmailDraftOutput)
    metadata: MetadataOutput = Field(default_factory=MetadataOutput)

    created_at: str
    updated_at: str


# -----------------------------
# Frontend-Compatible Response Schema
# -----------------------------

class ResearchReportResponse(BaseModel):
    report_id: str
    status: ResearchStatus

    company_name: str
    employee_name: str

    company_summary: Optional[str] = None
    employee_summary: Optional[str] = None

    website_findings: List[str] = Field(default_factory=list)
    personalization_hooks: List[str] = Field(default_factory=list)

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