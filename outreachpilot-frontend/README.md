OutreachPilot AI — Frontend

React + TailwindCSS frontend for OutreachPilot AI, a multi-agent company and employee research assistant.

The frontend allows users to submit company and employee details, trigger a FastAPI + LangGraph research workflow, view the generated report, review outreach drafts, and approve or reject email sending.
⸻
1. Project Overview

OutreachPilot AI helps users generate:

- Company research reports
- Employee/person research summaries
- Personalization hooks
- Cold outreach emails
- LinkedIn messages
- Follow-up emails
- Interview preparation notes
- Sales outreach insights

The frontend communicates with a FastAPI backend that runs the LangGraph multi-agent workflow.
⸻
2. Frontend Tech Stack

- React
- Vite
- TailwindCSS
- React Router DOM
- Axios
- React Hook Form
- Zod
- Lucide React Icons
⸻
3. Core Features

Research Form

Users can submit:

- Company name
- Company website
- Company LinkedIn URL
- Employee name
- Employee LinkedIn URL or profile text
- Employee email
- User email
- User profile/resume summary
- Purpose: job outreach, interview prep, or sales outreach

Report Viewer

The report detail page displays:

- Full generated research report
- Company summary
- Employee summary
- Website findings
- Personalization hooks
- Best outreach angle
- Cold email draft
- LinkedIn message
- Follow-up email
- Reviewer feedback
- Confidence score

Human Approval Flow

The frontend supports:

- Approve outreach
- Reject outreach
- Show sent/rejected status
- Prevent accidental email sending without user action
⸻
4. Folder Structure

frontend/
│
├── src/
│   ├── api/
│   │   └── researchApi.js
│   │
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── TextInput.jsx
│   │   ├── TextArea.jsx
│   │   ├── SelectInput.jsx
│   │   ├── LoadingSpinner.jsx
│   │   ├── StatusBadge.jsx
│   │   ├── ReportSection.jsx
│   │   └── EmptyState.jsx
│   │
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── CreateResearch.jsx
│   │   ├── ReportDetails.jsx
│   │   └── NotFound.jsx
│   │
│   ├── utils/
│   │   └── validators.js
│   │
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
├── .env.example
├── package.json
├── tailwind.config.js
└── README.md

⸻
5. Setup Instructions

Step 1: Clone the repository

git clone <your-repo-url>
cd outreachpilot-frontend


Step 2: Install dependencies

npm install


Step 3: Create environment file

Create a .env file in the frontend root:

VITE_API_BASE_URL=http://localhost:8000


For production:

VITE_API_BASE_URL=https://your-backend-domain.com


Step 4: Start development server

npm run dev


Frontend will run at:

http://localhost:5173

⸻
6. Available Scripts

Start development server

npm run dev


Build for production

npm run build


Preview production build

npm run preview

⸻
7. Backend API Dependency

This frontend expects a FastAPI backend running at:

http://localhost:8000


The backend should expose these APIs:

Start research workflow

POST /research/start


Request body:

{
  "company_name": "MongoDB",
  "company_website": "https://mongodb.com",
  "company_linkedin": "https://linkedin.com/company/mongodb",
  "employee_name": "Rahul Sharma",
  "employee_linkedin": "https://linkedin.com/in/rahul-sharma",
  "employee_email": "rahul@mongodb.com",
  "employee_profile_text": "Engineering Manager at MongoDB...",
  "user_email": "user@gmail.com",
  "user_profile": "Backend engineer with AWS, RAG, LangGraph experience",
  "purpose": "job_outreach"
}


Expected response:

{
  "report_id": "5f85a9a1-8a32-47cc-9810-9e52f441c010",
  "status": "running"
}

⸻
Get research report

GET /research/{report_id}


Expected response:

{
  "report_id": "5f85a9a1-8a32-47cc-9810-9e52f441c010",
  "status": "completed",
  "company_name": "MongoDB",
  "employee_name": "Rahul Sharma",
  "company_summary": "MongoDB provides a developer data platform...",
  "employee_summary": "Rahul appears to be an engineering leader...",
  "website_findings": [
    "MongoDB focuses on developer data platforms.",
    "Atlas is a key cloud product.",
    "The company has strong AI and vector search positioning."
  ],
  "personalization_hooks": [
    "Mention backend and distributed systems experience.",
    "Connect RAG experience with vector search.",
    "Highlight AWS and production AI workflow experience."
  ],
  "best_outreach_angle": "Backend + AI infrastructure + developer data platforms.",
  "report_markdown": "# Research Report: MongoDB + Rahul Sharma\n\n## Executive Summary\n...",
  "cold_email_subject": "Exploring AI/backend engineering opportunities at MongoDB",
  "cold_email_body": "Hi Rahul,\n\nI came across MongoDB's work around Atlas...",
  "linkedin_message": "Hi Rahul, I came across MongoDB's work around Atlas...",
  "follow_up_email": "Hi Rahul,\n\nJust following up on my previous note...",
  "reviewer_feedback": "The draft is specific, professional, and safe to send after verification.",
  "confidence_score": 8.5,
  "approval_status": "pending",
  "sent_status": "not_sent"
}

⸻
Approve outreach email

POST /research/{report_id}/approve


Expected response:

{
  "status": "approved",
  "message": "Outreach email sent successfully"
}

⸻
Reject outreach email

POST /research/{report_id}/reject


Expected response:

{
  "status": "rejected",
  "message": "Outreach email was rejected and not sent"
}

⸻
8. Pages

Home Page

Route:

/


Purpose:

- Explains the project
- Shows key features
- Provides CTA to create a research report
⸻
Create Research Page

Route:

/research/new


Purpose:

- User enters company and employee details
- Form validation with Zod
- Sends data to backend
- Redirects to report page after backend returns report_id
⸻
Report Details Page

Route:

/reports/:reportId


Purpose:

- Fetches generated report
- Shows research results
- Displays outreach drafts
- Allows user to approve or reject sending outreach
⸻
Not Found Page

Route:

/*


Purpose:

- Handles invalid routes
⸻
9. API Layer

The frontend API calls are centralized in:

src/api/researchApi.js


Main functions:

startResearch(payload)
getResearchReport(reportId)
approveOutreach(reportId)
rejectOutreach(reportId)
regenerateReport(reportId)


Example:

import { startResearch } from "../api/researchApi";

const response = await startResearch(payload);

⸻
10. Environment Variables

Create .env:

VITE_API_BASE_URL=http://localhost:8000


Important:

- Vite requires environment variables to start with VITE_
- Restart the dev server after changing .env
⸻
11. Validation Rules

Validation is handled using Zod in:

src/utils/validators.js


Required fields:

- Company name
- Company website
- Employee name
- User email
- User profile
- Purpose

Optional fields:

- Company LinkedIn URL
- Employee LinkedIn URL
- Employee email
- Employee profile text
⸻
12. User Flow

User opens app
↓
Clicks New Research
↓
Fills company and employee details
↓
Submits form
↓
Frontend calls POST /research/start
↓
Backend starts LangGraph workflow
↓
Frontend redirects to /reports/:reportId
↓
User views generated report
↓
User reviews email draft
↓
User approves or rejects outreach

⸻
13. Current MVP Scope

This frontend supports the MVP version without authentication.

Authentication/JWT is intentionally skipped for the first version to focus on:

- Multi-agent orchestration
- Report generation
- Email drafting
- Human approval flow

Production version can later add:

- JWT authentication
- User accounts
- My Reports dashboard
- Protected report access
- Refresh tokens
- Role-based permissions
⸻
14. Design Notes

The UI uses:

- Clean card-based layout
- Tailwind utility classes
- Responsive grid layout
- Clear loading states
- Status badges
- Approval/rejection actions
- Professional SaaS-style design

Primary color:

Blue / brand theme

⸻
15. Error Handling

The frontend handles:

- API failures
- Invalid form inputs
- Missing report data
- Loading states
- Failed approval/rejection actions

Example errors shown to user:

- Failed to start research
- Failed to load report
- Backend did not return report_id
- Failed to approve outreach
- Failed to reject outreach
⸻
16. Security Notes

For MVP:

- Use UUID report IDs
- Do not expose a public “all reports” endpoint
- Do not send outreach emails automatically
- Require explicit approval before sending
- Validate emails on frontend and backend

For production:

- Add JWT authentication
- Store reports by user ID
- Protect report routes
- Use ownership checks on backend
- Add rate limiting
- Add audit logs for email actions
⸻
17. Deployment

Frontend deployment options

Recommended:

- Vercel
- Netlify
- Render Static Site

Build command

npm run build


Output directory

dist


Production environment variable

VITE_API_BASE_URL=https://your-fastapi-backend.com

⸻
18. Demo Script

Use this flow for demo:

1. Open the homepage
2. Click New Research
3. Enter company and employee details
4. Submit form
5. Wait for report generation
6. Open report details page
7. Show company summary
8. Show employee summary
9. Show personalization hooks
10. Show generated cold email
11. Show reviewer feedback
12. Click approve or reject outreach
⸻
19. Future Improvements

Possible frontend improvements:

- JWT login/register
- My Reports page
- Report search/filter
- PDF download button
- Edit email before approval
- Regenerate email button
- Report sharing link
- Dark mode
- Toast notifications
- Streaming progress updates
- Agent execution timeline
- Source citation viewer
- Confidence score visualization
⸻
20. Project Positioning

This frontend is part of a larger AI engineering project demonstrating:

- React frontend development
- FastAPI integration
- LangGraph multi-agent workflow
- OpenAI-based report generation
- Human-in-the-loop approval
- Production-safe email workflow
- AI-powered personalization system
⸻
21. Final Project Description

OutreachPilot AI is a multi-agent company and employee research assistant. It helps users research a target company and person, generate a structured intelligence report, create personalized outreach drafts, and safely send outreach only after user approval.