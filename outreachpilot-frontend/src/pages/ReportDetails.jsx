import { useEffect, useMemo, useState } from "react";
import { useParams, Link } from "react-router-dom";
import {
  CheckCircle2,
  FileText,
  Mail,
  RefreshCcw,
  Send,
  XCircle,
} from "lucide-react";

import {
  approveOutreach,
  getResearchReport,
  rejectOutreach,
} from "../api/researchApi";

import LoadingSpinner from "../components/LoadingSpinner";
import StatusBadge from "../components/StatusBadge";
import ReportSection from "../components/ReportSection";
import EmptyState from "../components/EmptyState";

function normalizeReportPayload(data) {
  return {
    report_id: data.report_id || data.id,
    status: data.status || "pending",

    company_name: data.company_name || data.request?.company_name || "",
    employee_name: data.employee_name || data.request?.employee_name || "",

    company_summary:
      data.company_summary ||
      data.report?.company_summary ||
      data.report?.companyOverview ||
      "",

    employee_summary:
      data.employee_summary ||
      data.report?.employee_summary ||
      data.report?.employeeSummary ||
      "",

    website_findings:
      data.website_findings ||
      data.report?.website_findings ||
      data.report?.websiteFindings ||
      [],

    personalization_hooks:
      data.personalization_hooks ||
      data.report?.personalization_hooks ||
      data.report?.personalizationHooks ||
      [],

    best_outreach_angle:
      data.best_outreach_angle ||
      data.report?.best_outreach_angle ||
      data.report?.bestOutreachAngle ||
      "",

    report_markdown:
      data.report_markdown ||
      data.report?.report_markdown ||
      data.report?.markdown ||
      "",

    pdf_url:
      data.pdf_url ||
      data.report?.pdf_url ||
      "",

    cold_email_subject:
      data.cold_email_subject ||
      data.email_draft?.subject ||
      data.email?.subject ||
      "",

    cold_email_body:
      data.cold_email_body ||
      data.email_draft?.body ||
      data.email?.body ||
      "",

    linkedin_message:
      data.linkedin_message ||
      data.email_draft?.linkedin_message ||
      data.linkedinMessage ||
      "",

    follow_up_email:
      data.follow_up_email ||
      data.email_draft?.follow_up_email ||
      data.followUpEmail ||
      "",

    reviewer_feedback:
      data.reviewer_feedback ||
      data.report?.reviewer_feedback ||
      "",

    confidence_score:
      data.confidence_score ||
      data.report?.confidence_score ||
      null,

    approval_status:
      data.approval_status ||
      data.email_draft?.approval_status ||
      "pending",

    sent_status:
      data.sent_status ||
      data.email_draft?.sent_status ||
      "not_sent",

    error_message:
      data.error_message ||
      data.metadata?.error_message ||
      "",
  };
}

function MarkdownLikeRenderer({ content }) {
  if (!content) {
    return (
      <p className="text-sm text-slate-500">
        No report markdown was returned by the backend yet.
      </p>
    );
  }

  const html = content
    .replace(/^### (.*$)/gim, "<h3>$1</h3>")
    .replace(/^## (.*$)/gim, "<h2>$1</h2>")
    .replace(/^# (.*$)/gim, "<h1>$1</h1>")
    .replace(/\*\*(.*?)\*\*/gim, "<strong>$1</strong>")
    .replace(/\n- (.*)/gim, "<ul><li>$1</li></ul>")
    .replace(/\n/gim, "<br />");

  return (
    <div
      className="prose-report text-slate-700"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

export default function ReportDetails() {
  const { reportId } = useParams();

  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState("");
  const [error, setError] = useState("");
  const [actionMessage, setActionMessage] = useState("");

  async function loadReport() {
    setError("");

    try {
      const data = await getResearchReport(reportId);
      setReport(normalizeReportPayload(data));
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          err?.message ||
          "Failed to load report."
      );
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    setIsLoading(true);
    loadReport();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [reportId]);

  // Poll backend while background LangGraph workflow is still running.
  useEffect(() => {
    if (!report) return;

    const shouldPoll =
      report.status === "running" ||
      report.status === "pending";

    if (!shouldPoll) return;

    const intervalId = setInterval(() => {
      loadReport();
    }, 3000);

    return () => clearInterval(intervalId);

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [report?.status, reportId]);

  async function handleApprove() {
    setActionLoading("approve");
    setActionMessage("");

    try {
      const data = await approveOutreach(reportId);
      setActionMessage(
        data.message || "Outreach email approved and sent successfully."
      );
      await loadReport();
    } catch (err) {
      setActionMessage(
        err?.response?.data?.detail ||
          err?.message ||
          "Failed to approve outreach."
      );
    } finally {
      setActionLoading("");
    }
  }

  async function handleReject() {
    setActionLoading("reject");
    setActionMessage("");

    try {
      const data = await rejectOutreach(reportId);
      setActionMessage(data.message || "Outreach email rejected.");
      await loadReport();
    } catch (err) {
      setActionMessage(
        err?.response?.data?.detail ||
          err?.message ||
          "Failed to reject outreach."
      );
    } finally {
      setActionLoading("");
    }
  }

  const canApprove = useMemo(() => {
    if (!report) return false;

    return (
      report.status === "completed" &&
      report.approval_status !== "approved" &&
      report.sent_status !== "sent"
    );
  }, [report]);

  const isProcessing =
    report?.status === "running" || report?.status === "pending";

  const isFailed = report?.status === "failed";

  if (isLoading) {
    return (
      <div className="mx-auto max-w-5xl px-5 py-10">
        <LoadingSpinner label="Loading research report..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto max-w-5xl px-5 py-10">
        <div className="rounded-2xl border border-red-200 bg-red-50 p-6 text-red-700">
          <h2 className="text-lg font-bold">Unable to load report</h2>
          <p className="mt-2 text-sm">{error}</p>

          <button
            onClick={loadReport}
            className="mt-5 inline-flex items-center gap-2 rounded-xl bg-red-600 px-4 py-2 text-sm font-bold text-white hover:bg-red-700"
          >
            <RefreshCcw size={16} />
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="mx-auto max-w-5xl px-5 py-10">
        <EmptyState />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl px-5 py-10">
      <div className="mb-8 flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <Link
            to="/research/new"
            className="text-sm font-semibold text-brand-700 hover:text-brand-900"
          >
            ← Create another research report
          </Link>

          <h1 className="mt-3 text-3xl font-black tracking-tight text-slate-950">
            Research Report
          </h1>

          <p className="mt-2 text-slate-600">
            {report.company_name || "Company"} +{" "}
            {report.employee_name || "Employee"}
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <StatusBadge status={report.status} />
          <StatusBadge status={report.approval_status} />
          <StatusBadge status={report.sent_status} />
        </div>
      </div>

      {isProcessing && (
        <div className="mb-6 rounded-2xl border border-blue-200 bg-blue-50 p-5">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="font-bold text-blue-900">
                Research is still processing
              </h2>
              <p className="mt-1 text-sm text-blue-700">
                The LangGraph workflow is running in the background. This page
                refreshes automatically every few seconds.
              </p>
            </div>

            <button
              onClick={loadReport}
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-2 text-sm font-bold text-white hover:bg-blue-700"
            >
              <RefreshCcw size={16} />
              Refresh
            </button>
          </div>
        </div>
      )}

      {isFailed && (
        <div className="mb-6 rounded-2xl border border-red-200 bg-red-50 p-5">
          <h2 className="font-bold text-red-900">
            Research workflow failed
          </h2>

          <p className="mt-1 text-sm text-red-700">
            {report.error_message ||
              "Something went wrong during report generation."}
          </p>

          <button
            onClick={loadReport}
            className="mt-4 inline-flex items-center justify-center gap-2 rounded-xl bg-red-600 px-4 py-2 text-sm font-bold text-white hover:bg-red-700"
          >
            <RefreshCcw size={16} />
            Retry Fetch
          </button>
        </div>
      )}

      {actionMessage && (
        <div className="mb-6 rounded-2xl border border-slate-200 bg-white p-4 text-sm font-semibold text-slate-700 shadow-sm">
          {actionMessage}
        </div>
      )}

      {report.pdf_url && (
        <section className="mb-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div className="mb-2 flex items-center gap-2">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-50 text-brand-700">
                  <FileText size={20} />
                </div>

                <h2 className="text-lg font-bold text-slate-900">
                  PDF Report
                </h2>
              </div>

              <p className="text-sm text-slate-600">
                View or download the generated PDF report from S3. This link is
                temporary and may expire.
              </p>
            </div>

            <a
              href={report.pdf_url}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center justify-center rounded-xl bg-brand-600 px-5 py-3 text-sm font-bold text-white hover:bg-brand-700"
            >
              View PDF Report
            </a>
          </div>
        </section>
      )}

      <div className="grid gap-6 lg:grid-cols-[1.4fr_0.8fr]">
        <div className="space-y-6">
          <ReportSection title="Full Research Report">
            <MarkdownLikeRenderer content={report.report_markdown} />
          </ReportSection>

          <ReportSection title="Company Summary">
            <p>{report.company_summary || "No company summary available yet."}</p>
          </ReportSection>

          <ReportSection title="Employee Summary">
            <p>{report.employee_summary || "No employee summary available yet."}</p>
          </ReportSection>

          <ReportSection title="Website Findings">
            {report.website_findings?.length ? (
              <ul className="list-disc space-y-2 pl-5">
                {report.website_findings.map((item, index) => (
                  <li key={`${item}-${index}`}>{item}</li>
                ))}
              </ul>
            ) : (
              <p>No website findings available yet.</p>
            )}
          </ReportSection>
        </div>

        <aside className="space-y-6">
          <ReportSection title="Personalization Hooks">
            {report.personalization_hooks?.length ? (
              <ul className="list-disc space-y-2 pl-5">
                {report.personalization_hooks.map((item, index) => (
                  <li key={`${item}-${index}`}>{item}</li>
                ))}
              </ul>
            ) : (
              <p>No personalization hooks available yet.</p>
            )}
          </ReportSection>

          <ReportSection title="Best Outreach Angle">
            <p>
              {report.best_outreach_angle ||
                "No outreach angle returned by backend yet."}
            </p>
          </ReportSection>

          <ReportSection title="Cold Email Draft">
            <div className="rounded-xl bg-slate-50 p-4">
              <p className="mb-3 text-sm font-bold text-slate-900">
                Subject:{" "}
                <span className="font-semibold">
                  {report.cold_email_subject || "No subject generated yet"}
                </span>
              </p>

              <pre className="whitespace-pre-wrap rounded-xl bg-white p-4 text-sm leading-6 text-slate-700 ring-1 ring-slate-200">
                {report.cold_email_body || "No cold email generated yet."}
              </pre>
            </div>
          </ReportSection>

          <ReportSection title="LinkedIn Message">
            <pre className="whitespace-pre-wrap rounded-xl bg-slate-50 p-4 text-sm leading-6 text-slate-700">
              {report.linkedin_message || "No LinkedIn message generated yet."}
            </pre>
          </ReportSection>

          <ReportSection title="Follow-up Email">
            <pre className="whitespace-pre-wrap rounded-xl bg-slate-50 p-4 text-sm leading-6 text-slate-700">
              {report.follow_up_email || "No follow-up email generated yet."}
            </pre>
          </ReportSection>

          <ReportSection title="Reviewer Feedback">
            <p>
              {report.reviewer_feedback ||
                "No reviewer feedback returned by backend yet."}
            </p>

            {report.confidence_score !== null && (
              <p className="mt-4 rounded-xl bg-slate-50 p-3 text-sm font-semibold text-slate-700">
                Confidence Score: {report.confidence_score}
              </p>
            )}
          </ReportSection>

          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-bold text-slate-900">
              Outreach Approval
            </h2>

            <p className="mt-2 text-sm leading-6 text-slate-600">
              The outreach email will only be sent to the employee after you
              approve it.
            </p>

            <div className="mt-5 grid gap-3">
              <button
                onClick={handleApprove}
                disabled={!canApprove || actionLoading === "approve"}
                className="inline-flex items-center justify-center gap-2 rounded-xl bg-emerald-600 px-5 py-3 text-sm font-bold text-white hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {actionLoading === "approve" ? (
                  <>
                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />
                    Sending...
                  </>
                ) : (
                  <>
                    <Send size={17} />
                    Approve & Send Outreach
                  </>
                )}
              </button>

              <button
                onClick={handleReject}
                disabled={
                  report.approval_status === "rejected" ||
                  report.sent_status === "sent" ||
                  actionLoading === "reject"
                }
                className="inline-flex items-center justify-center gap-2 rounded-xl border border-red-200 bg-red-50 px-5 py-3 text-sm font-bold text-red-700 hover:bg-red-100 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {actionLoading === "reject" ? (
                  <>
                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-red-300 border-t-red-700" />
                    Rejecting...
                  </>
                ) : (
                  <>
                    <XCircle size={17} />
                    Reject Outreach
                  </>
                )}
              </button>
            </div>

            <div className="mt-5 rounded-xl bg-slate-50 p-4 text-sm text-slate-600">
              <p className="flex items-center gap-2 font-semibold text-slate-800">
                <Mail size={16} />
                Safety Note
              </p>
              <p className="mt-1">
                Review the generated report and draft before approving. In the
                next step, approval can trigger an MCP/email tool to send the
                outreach email.
              </p>
            </div>

            {report.sent_status === "sent" && (
              <div className="mt-4 flex items-center gap-2 rounded-xl bg-emerald-50 p-4 text-sm font-semibold text-emerald-700">
                <CheckCircle2 size={18} />
                Outreach email has been sent.
              </div>
            )}
          </section>
        </aside>
      </div>
    </div>
  );
}