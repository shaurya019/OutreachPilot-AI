# OutreachPilot AI — Backend Design & Workflow

A production-style FastAPI backend for **OutreachPilot AI**, a LangGraph-based multi-agent company and employee research assistant.

The backend accepts company and employee details, runs a multi-agent research workflow, generates a structured report and outreach draft, stores workflow state in DynamoDB, uploads a PDF report to S3, and sends outreach email only after explicit approval through a real MCP email tool.

---

## 1. Project Summary

**OutreachPilot AI** helps users research a target company and employee/person, then generate:

- Company research summary
- Website findings
- Employee/person profile summary
- Personalization hooks
- Best outreach angle
- Research report
- PDF report
- Cold email draft
- LinkedIn message
- Follow-up email
- Reviewer feedback and confidence score

The system is designed around a safe workflow:

```txt
Research first
↓
Generate report and draft
↓
Show output to user
↓
User approves
↓
MCP email tool sends outreach
↓
DynamoDB updates sent status
```

The system does **not** send outreach email automatically.

---

## 2. Core Problem It Solves

Manual outreach and interview preparation are time-consuming because users need to:

- Research the company website
- Understand company products and positioning
- Review the target employee/person
- Find personalization hooks
- Write a professional email
- Create a follow-up message
- Verify that the message is safe and not generic

OutreachPilot AI automates this process through a multi-agent workflow and generates a professional report that can be reviewed before any email is sent.

---

## 3. Why This Project Is Unique

This project is not just a cold email generator.

It combines:

- Multi-agent orchestration with LangGraph
- Parallel research agents
- Pydantic structured outputs
- DynamoDB workflow persistence
- S3 PDF report storage
- Human approval before outreach
- Real MCP email tool integration
- Reviewer/guardrail agent
- Production-friendly AWS architecture

The system follows a **research-first and approval-first design**, making it safer and more useful than generic AI outreach tools.

---

## 4. Selected Tech Stack

### Frontend

- React
- TailwindCSS
- Axios
- React Router
- React Hook Form
- Zod

### Backend

- FastAPI
- Pydantic
- LangGraph
- LangChain OpenAI
- OpenAI
- Boto3
- MCP Python SDK

### Database and Storage

- DynamoDB for workflow/report metadata
- S3 for generated PDF reports

### Email and Tooling

- Resend for email provider
- MCP server for email tools

---

## 5. High-Level Architecture

```txt
React Frontend
    ↓
FastAPI Backend
    ↓
DynamoDB initial report item
    ↓
Background LangGraph workflow
    ↓
Parallel research agents
    ↓
Report + email draft generation
    ↓
PDF generation
    ↓
Upload PDF to S3
    ↓
Save final output to DynamoDB
    ↓
Frontend fetches report and PDF URL
    ↓
User approves outreach
    ↓
FastAPI calls MCP email client
    ↓
MCP email server calls email provider
    ↓
DynamoDB updates sent status
```

---

## 6. Complete Workflow

### Step 1: User submits research request

Frontend calls:

```http
POST /research/start
```

Request body:

```json
{
  "company_name": "MongoDB",
  "company_website": "https://mongodb.com",
  "company_linkedin": "https://linkedin.com/company/mongodb",
  "employee_name": "Rahul Sharma",
  "employee_linkedin": "https://linkedin.com/in/rahul-sharma",
  "employee_email": "rahul@example.com",
  "employee_profile_text": "Engineering Manager working on backend systems.",
  "user_email": "user@gmail.com",
  "user_profile": "Backend engineer with AWS, RAG, LangGraph, OpenAI and DynamoDB experience.",
  "purpose": "job_outreach"
}
```

### Step 2: Backend creates DynamoDB item

FastAPI creates a new `report_id` and saves an initial item:

```json
{
  "report_id": "uuid",
  "status": "running",
  "purpose": "job_outreach",
  "company": {},
  "employee": {},
  "user": {},
  "agent_outputs": {},
  "report": {},
  "email_draft": {},
  "metadata": {},
  "created_at": "...",
  "updated_at": "..."
}
```

The API immediately returns:

```json
{
  "report_id": "uuid",
  "status": "running"
}
```

### Step 3: Background task runs LangGraph

The FastAPI route uses `BackgroundTasks` so the frontend does not wait for the full OpenAI/LangGraph workflow.

```txt
POST /research/start
↓
Create DynamoDB item
↓
Return report_id immediately
↓
Run LangGraph in background
```

### Step 4: LangGraph agents run

The workflow uses a supervisor node and parallel research nodes.

```txt
START
  ↓
supervisor
  ↓
 ┌─────────────────┬─────────────────┬──────────────────┐
 ↓                 ↓                 ↓
website_research  company_research   employee_research
 └─────────────────┴─────────────────┴──────────────────┘
                    ↓
              merge_research
                    ↓
              personalization
                    ↓
              report_generator
                    ↓
              email_draft
                    ↓
              reviewer
                    ↓
                  END
```

### Step 5: PDF is generated and uploaded to S3

After the report is generated:

```txt
report.markdown
↓
PDF service converts markdown to PDF
↓
S3 service uploads PDF
↓
DynamoDB stores pdf_s3_key
```

The system stores the S3 key permanently:

```json
{
  "report": {
    "pdf_s3_key": "reports/{report_id}.pdf"
  }
}
```

The backend generates a temporary pre-signed URL when the frontend requests the report.

### Step 6: Frontend shows report

Frontend calls:

```http
GET /research/{report_id}
```

The backend maps the DynamoDB item to a frontend-friendly response:

```json
{
  "report_id": "uuid",
  "status": "completed",
  "company_name": "MongoDB",
  "employee_name": "Rahul Sharma",
  "company_summary": "...",
  "employee_summary": "...",
  "website_findings": [],
  "personalization_hooks": [],
  "best_outreach_angle": "...",
  "report_markdown": "...",
  "pdf_url": "https://s3-presigned-url...",
  "cold_email_subject": "...",
  "cold_email_body": "...",
  "linkedin_message": "...",
  "follow_up_email": "...",
  "reviewer_feedback": "...",
  "confidence_score": 8.0,
  "approval_status": "pending",
  "sent_status": "not_sent"
}
```

### Step 7: User approves outreach

Frontend calls:

```http
POST /research/{report_id}/approve
```

### Step 8: FastAPI calls real MCP email tool

The approve endpoint calls the MCP client:

```txt
FastAPI approve endpoint
↓
ResearchService.approve_outreach()
↓
EmailMCPClient
↓
MCP stdio connection
↓
email_mcp_server.py
↓
MCP tool: send_approved_outreach_email
↓
EmailService
↓
Resend
```

### Step 9: DynamoDB updates email status

If MCP email sending succeeds:

```json
{
  "email_draft": {
    "approval_status": "approved",
    "sent_status": "sent",
    "sent_at": "...",
    "provider_message_id": "resend_message_id"
  }
}
```

If email sending fails:

```json
{
  "email_draft": {
    "approval_status": "approved",
    "sent_status": "failed"
  },
  "metadata": {
    "error_message": "provider error..."
  }
}
```

---

## 7. LangGraph Agent Responsibilities

### 7.1 Supervisor Node

File:

```txt
app/agents/nodes/supervisor_node.py
```

Responsibilities:

- Decide workflow plan
- Understand selected purpose
- Define expected final outputs
- Apply safety rules

### 7.2 Website Research Node

File:

```txt
app/agents/nodes/website_research_node.py
```

Responsibilities:

- Fetch company website content
- Discover important internal pages
- Extract useful website findings
- Return structured output

Uses:

```txt
app/services/website_extractor.py
```

Output schema:

```txt
WebsiteResearchOutput
```

### 7.3 Company Research Node

File:

```txt
app/agents/nodes/company_research_node.py
```

Responsibilities:

- Summarize company
- Identify industry
- Identify products/services
- Identify target customers
- Explain AI/backend/cloud relevance

Output schema:

```txt
CompanyResearchOutput
```

### 7.4 Employee Research Node

File:

```txt
app/agents/nodes/employee_research_node.py
```

Responsibilities:

- Analyze provided employee information
- Identify role/seniority if available
- Extract likely responsibilities
- Extract personalization clues
- Avoid private or unsupported claims

Output schema:

```txt
EmployeeResearchOutput
```

### 7.5 Merge Research Node

File:

```txt
app/agents/nodes/merge_research_node.py
```

Responsibilities:

- Combine outputs from parallel research nodes
- Add warnings/errors if any research branch failed
- Prepare state for personalization

### 7.6 Personalization Node

File:

```txt
app/agents/nodes/personalization_node.py
```

Responsibilities:

- Connect company needs, employee context, and user profile
- Generate personalization hooks
- Choose best outreach angle
- Recommend skills to highlight
- List things to avoid

Output schema:

```txt
PersonalizationOutput
```

### 7.7 Report Generator Node

File:

```txt
app/agents/nodes/report_generator_node.py
```

Responsibilities:

- Generate final Markdown report
- Include executive summary
- Include company and employee insights
- Include personalization hooks
- Include verification notes

### 7.8 Email Draft Node

File:

```txt
app/agents/nodes/email_draft_node.py
```

Responsibilities:

- Generate cold email
- Generate LinkedIn message
- Generate follow-up email
- Keep status pending until approval

Output schema:

```txt
EmailDraftOutput
```

### 7.9 Reviewer Node

File:

```txt
app/agents/nodes/reviewer_node.py
```

Responsibilities:

- Check message quality
- Check hallucination risks
- Check unsupported claims
- Add verification notes
- Assign quality and confidence scores

Output schema:

```txt
ReviewerOutput
```

---

## 8. Pydantic Structured Outputs

The project uses Pydantic schemas with:

```python
llm.with_structured_output(...)
```

This is better than asking the model to return raw JSON manually.

Benefits:

- Validated output shape
- Cleaner node code
- Fewer parsing failures
- Easier DynamoDB persistence
- Easier frontend rendering

Important schemas:

```txt
WebsiteResearchOutput
CompanyResearchOutput
EmployeeResearchOutput
PersonalizationOutput
EmailDraftOutput
ReviewerOutput
```

Long-form report generation remains Markdown text because report content is easier to produce naturally as Markdown.

---

## 9. DynamoDB Design

### Table Name

```txt
OutreachPilotReports
```

### Primary Key

```txt
report_id — String
```

### Why one table?

The MVP access patterns are simple:

| API | Access Pattern |
|---|---|
| POST /research/start | Create item by report_id |
| GET /research/{report_id} | Get item by report_id |
| POST /research/{report_id}/approve | Update item by report_id |
| POST /research/{report_id}/reject | Update item by report_id |

### Example Item

```json
{
  "report_id": "uuid",
  "status": "completed",
  "purpose": "job_outreach",
  "company": {
    "name": "MongoDB",
    "website": "https://mongodb.com",
    "linkedin": "https://linkedin.com/company/mongodb"
  },
  "employee": {
    "name": "Rahul Sharma",
    "linkedin": "https://linkedin.com/in/rahul-sharma",
    "email": "rahul@example.com",
    "profile_text": "Engineering Manager..."
  },
  "user": {
    "email": "user@gmail.com",
    "profile": "Backend engineer..."
  },
  "agent_outputs": {
    "website_research": {},
    "company_research": {},
    "employee_research": {},
    "personalization": {},
    "reviewer": {}
  },
  "report": {
    "title": "Research Report...",
    "markdown": "# Research Report...",
    "html": null,
    "pdf_s3_key": "reports/uuid.pdf",
    "pdf_url": null
  },
  "email_draft": {
    "recipient_email": "rahul@example.com",
    "subject": "...",
    "body": "...",
    "linkedin_message": "...",
    "follow_up_email": "...",
    "approval_status": "pending",
    "sent_status": "not_sent",
    "sent_at": null,
    "provider_message_id": null
  },
  "metadata": {
    "model": "gpt-4o-mini",
    "tokens_used": null,
    "cost_estimate": null,
    "workflow_version": "v1",
    "error_message": null
  },
  "created_at": "...",
  "updated_at": "..."
}
```

### Future GSI

When authentication or “My Reports” is added:

```txt
GSI: UserEmailCreatedAtIndex
Partition key: user_email
Sort key: created_at
```

---

## 10. S3 PDF Design

### Bucket

```txt
outreachpilot-reports
```

### Key Format

```txt
reports/{report_id}.pdf
```

### Why store S3 key instead of URL?

Pre-signed URLs expire, so DynamoDB should store the permanent S3 key:

```json
{
  "pdf_s3_key": "reports/{report_id}.pdf"
}
```

When frontend fetches the report, backend generates a temporary URL:

```txt
S3 key
↓
generate_presigned_url()
↓
temporary pdf_url
```

---

## 11. MCP Email Tool Design

The project includes a real MCP server.

### MCP Server File

```txt
app/mcp/email_mcp_server.py
```

### MCP Client File

```txt
app/mcp/email_mcp_client.py
```

### Exposed MCP Tools

```txt
send_approved_outreach_email
send_report_email_to_user
```

### MCP Tool: send_approved_outreach_email

Purpose:

- Send outreach email only after explicit approval

Safety rule:

```txt
approval_status must be "approved"
```

Inputs:

```json
{
  "recipient_email": "rahul@example.com",
  "subject": "Exploring opportunities at MongoDB",
  "body": "Hi Rahul...",
  "reply_to": "user@gmail.com",
  "approval_status": "approved"
}
```

Output:

```json
{
  "status": "sent",
  "provider": "resend",
  "provider_message_id": "message_id",
  "message": "Approved outreach email sent successfully."
}
```

### Why MCP?

MCP gives a controlled tool boundary between the agent/backend and external actions.

Instead of directly calling email APIs everywhere:

```txt
FastAPI → Resend
```

The system uses:

```txt
FastAPI → MCP Client → MCP Server Tool → EmailService → Resend
```

This makes the email action reusable, auditable, and safer.

---

## 12. API Design

### Start Research

```http
POST /research/start
```

Starts research workflow.

Response:

```json
{
  "report_id": "uuid",
  "status": "running"
}
```

### Get Report

```http
GET /research/{report_id}
```

Returns frontend-compatible report response.

### Approve Outreach

```http
POST /research/{report_id}/approve
```

Calls MCP email tool and updates DynamoDB after successful sending.

### Reject Outreach

```http
POST /research/{report_id}/reject
```

Marks outreach as rejected and does not send email.

---

## 13. Backend Folder Structure

```txt
backend/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── api/
│   │   └── research.py
│   │
│   ├── agents/
│   │   ├── state.py
│   │   ├── llm.py
│   │   ├── graph.py
│   │   └── nodes/
│   │       ├── supervisor_node.py
│   │       ├── website_research_node.py
│   │       ├── company_research_node.py
│   │       ├── employee_research_node.py
│   │       ├── merge_research_node.py
│   │       ├── personalization_node.py
│   │       ├── report_generator_node.py
│   │       ├── email_draft_node.py
│   │       └── reviewer_node.py
│   │
│   ├── db/
│   │   └── dynamodb.py
│   │
│   ├── mcp/
│   │   ├── email_mcp_server.py
│   │   └── email_mcp_client.py
│   │
│   ├── repositories/
│   │   └── report_repository.py
│   │
│   ├── schemas/
│   │   └── research.py
│   │
│   ├── services/
│   │   ├── research_service.py
│   │   ├── website_extractor.py
│   │   ├── pdf_service.py
│   │   ├── s3_service.py
│   │   └── email_service.py
│   │
│   └── utils/
│       └── time.py
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## 14. Environment Variables

```env
APP_NAME=OutreachPilot AI
APP_ENV=development

AWS_REGION=ap-south-1
DYNAMODB_REPORTS_TABLE=OutreachPilotReports
S3_REPORTS_BUCKET=outreachpilot-reports

OPENAI_API_KEY=your_openai_api_key_here

RESEND_API_KEY=your_resend_api_key_here
EMAIL_FROM=OutreachPilot AI <onboarding@resend.dev>

FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000
```

For AWS credentials, use one of:

```txt
aws configure
```

or environment variables:

```env
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=ap-south-1
```

---

## 15. Setup Instructions

### Step 1: Create virtual environment

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Create DynamoDB table

```bash
aws dynamodb create-table \
  --table-name OutreachPilotReports \
  --attribute-definitions AttributeName=report_id,AttributeType=S \
  --key-schema AttributeName=report_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ap-south-1
```

### Step 4: Create S3 bucket

```bash
aws s3 mb s3://outreachpilot-reports --region ap-south-1
```

Keep public access blocked. The app uses pre-signed URLs.

### Step 5: Create `.env`

```bash
cp .env.example .env
```

Update values.

### Step 6: Run FastAPI backend

```bash
uvicorn app.main:app --reload
```

Open:

```txt
http://localhost:8000/docs
```

---

## 16. MCP Server Testing

Run MCP server manually:

```bash
python -m app.mcp.email_mcp_server
```

Or inspect with MCP dev tools:

```bash
mcp dev app/mcp/email_mcp_server.py
```

Expected tools:

```txt
send_approved_outreach_email
send_report_email_to_user
```

---

## 17. End-to-End Test

### Start Research

```bash
curl -X POST http://localhost:8000/research/start \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "MongoDB",
    "company_website": "https://mongodb.com",
    "company_linkedin": "https://linkedin.com/company/mongodb",
    "employee_name": "Rahul Sharma",
    "employee_linkedin": "https://linkedin.com/in/rahul-sharma",
    "employee_email": "your-test-email@example.com",
    "employee_profile_text": "Engineering Manager working on backend systems.",
    "user_email": "user@gmail.com",
    "user_profile": "Backend engineer with AWS, RAG, LangGraph, OpenAI and DynamoDB experience.",
    "purpose": "job_outreach"
  }'
```

Response:

```json
{
  "report_id": "uuid",
  "status": "running"
}
```

### Get Report

```bash
curl http://localhost:8000/research/{report_id}
```

Wait until:

```json
{
  "status": "completed"
}
```

### Approve and Send Outreach

```bash
curl -X POST http://localhost:8000/research/{report_id}/approve
```

Expected response:

```json
{
  "status": "approved",
  "message": "Approved outreach email sent successfully."
}
```

---

## 18. Frontend Integration

The frontend uses these APIs:

```txt
POST /research/start
GET /research/{report_id}
POST /research/{report_id}/approve
POST /research/{report_id}/reject
```

The report details page should:

- Poll while status is running
- Show report markdown
- Show PDF report button
- Show email draft
- Show approve/reject buttons
- Refresh after approval

---

## 19. Security and Safety Rules

Current MVP safety:

- Outreach is not sent automatically
- Approval endpoint is required
- MCP tool checks `approval_status = approved`
- Employee facts are based only on provided/public data
- Reviewer agent flags uncertain or risky claims
- S3 uses pre-signed URLs instead of public files

Production improvements:

- JWT authentication
- User ownership checks
- Rate limiting
- Audit logs
- Email domain verification
- SQS/Step Functions instead of FastAPI BackgroundTasks
- Separate MCP server deployment
- S3 encryption and lifecycle rules

---

## 20. Current Limitations

The MVP intentionally avoids:

- Direct LinkedIn scraping
- Full CRM integration
- User authentication
- Full retry queue
- Complex multi-tenant access control
- Vector database/RAG over historical reports

These can be added in later versions.

---

## 21. Future Enhancements

Recommended next features:

1. JWT authentication
2. My Reports dashboard
3. Edit email draft before approval
4. Regenerate report endpoint
5. Send report email to user automatically
6. AWS SES instead of Resend
7. SQS + worker for background jobs
8. Step Functions for workflow orchestration
9. Pinecone/OpenSearch for RAG over website chunks
10. Source citation viewer
11. Report PDF template customization
12. Cost and token tracking
13. Agent execution timeline
14. Audit logs for email actions

---

## 22. Interview Pitch

You can describe the project like this:

> OutreachPilot AI is a LangGraph-based multi-agent research assistant. It takes a company website, company LinkedIn, employee details, and a purpose such as job outreach, interview prep, or sales outreach. The backend creates a workflow item in DynamoDB and runs a background LangGraph workflow. A supervisor node coordinates parallel website, company, and employee research agents. The system then generates personalization hooks, a Markdown report, a PDF report uploaded to S3, an outreach draft, and reviewer feedback. The frontend displays the report and PDF. Outreach emails are only sent after explicit approval through a real MCP email tool, and DynamoDB is updated with the sent status and provider message ID.

---

## 23. Final System Flow

```txt
User submits research form
↓
FastAPI creates DynamoDB item
↓
Background LangGraph workflow starts
↓
Supervisor creates workflow plan
↓
Website, company, employee agents run in parallel
↓
Research outputs are merged
↓
Personalization agent creates hooks
↓
Report generator creates Markdown report
↓
Email draft agent creates outreach messages
↓
Reviewer agent checks quality and risks
↓
PDF service creates report PDF
↓
S3 service uploads PDF
↓
DynamoDB stores final output and S3 key
↓
Frontend shows report, PDF, and draft
↓
User approves outreach
↓
FastAPI calls MCP email client
↓
MCP email server sends outreach
↓
DynamoDB updates sent status
```

---

## 24. Production Architecture Upgrade

Current MVP:

```txt
FastAPI BackgroundTasks
DynamoDB
S3
MCP stdio server started by client
Resend
```

Production upgrade:

```txt
API Gateway / FastAPI
↓
DynamoDB initial item
↓
SQS message
↓
Worker / Lambda
↓
LangGraph workflow
↓
S3 PDF upload
↓
DynamoDB update
↓
Frontend polling / WebSocket
↓
Approval endpoint
↓
Long-running MCP server / AWS SES
↓
Audit log
```

This is the scalable version for real users.
