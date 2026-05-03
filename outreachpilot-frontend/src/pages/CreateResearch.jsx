import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Sparkles } from "lucide-react";

import { researchFormSchema } from "../utils/validators";
import { startResearch } from "../api/researchApi";
import TextInput from "../components/TextInput";
import TextArea from "../components/TextArea";
import SelectInput from "../components/SelectInput";

const defaultValues = {
  company_name: "",
  company_website: "",
  company_linkedin: "",
  employee_name: "",
  employee_linkedin: "",
  employee_email: "",
  employee_profile_text: "",
  user_email: "",
  user_profile:
    "Software Engineer with experience in backend systems, AWS, Node.js, TypeScript, RAG pipelines, LangGraph workflows, and production LLM systems.",
  purpose: "job_outreach",
};

export default function CreateResearch() {
  const navigate = useNavigate();
  const [serverError, setServerError] = useState("");
  const [isSubmittingForm, setIsSubmittingForm] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(researchFormSchema),
    defaultValues,
  });

  async function onSubmit(values) {
    setServerError("");
    setIsSubmittingForm(true);

    try {
      const payload = {
        ...values,
        company_linkedin: values.company_linkedin || null,
        employee_linkedin: values.employee_linkedin || null,
        employee_email: values.employee_email || null,
        employee_profile_text: values.employee_profile_text || null,
      };

      const data = await startResearch(payload);

      const reportId = data.report_id || data.id;

      if (!reportId) {
        throw new Error("Backend did not return report_id");
      }

      navigate(`/reports/${reportId}`);
    } catch (error) {
      const message =
        error?.response?.data?.detail ||
        error?.message ||
        "Something went wrong while starting research.";

      setServerError(message);
    } finally {
      setIsSubmittingForm(false);
    }
  }

  return (
    <div className="mx-auto max-w-5xl px-5 py-10">
      <div className="mb-8">
        <div className="mb-3 inline-flex rounded-full bg-brand-50 px-4 py-2 text-sm font-semibold text-brand-700 ring-1 ring-brand-100">
          New Research Workflow
        </div>

        <h1 className="text-3xl font-black tracking-tight text-slate-950">
          Create company and employee research report
        </h1>

        <p className="mt-2 max-w-2xl text-slate-600">
          Enter company, employee, and user profile details. The backend
          LangGraph workflow will generate a report and outreach drafts.
        </p>
      </div>

      <form
        onSubmit={handleSubmit(onSubmit)}
        className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"
      >
        {serverError && (
          <div className="mb-6 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-700">
            {serverError}
          </div>
        )}

        <div className="grid gap-6 md:grid-cols-2">
          <TextInput
            label="Company Name"
            name="company_name"
            register={register}
            error={errors.company_name}
            placeholder="MongoDB"
            required
          />

          <TextInput
            label="Company Website"
            name="company_website"
            register={register}
            error={errors.company_website}
            placeholder="https://mongodb.com"
            required
          />

          <TextInput
            label="Company LinkedIn URL"
            name="company_linkedin"
            register={register}
            error={errors.company_linkedin}
            placeholder="https://linkedin.com/company/mongodb"
          />

          <SelectInput
            label="Purpose"
            name="purpose"
            register={register}
            error={errors.purpose}
            required
            options={[
              { label: "Job Outreach", value: "job_outreach" },
              { label: "Interview Preparation", value: "interview_prep" },
              { label: "Sales Outreach", value: "sales_outreach" },
            ]}
          />

          <TextInput
            label="Employee Name"
            name="employee_name"
            register={register}
            error={errors.employee_name}
            placeholder="Rahul Sharma"
            required
          />

          <TextInput
            label="Employee Email"
            name="employee_email"
            register={register}
            error={errors.employee_email}
            placeholder="rahul@company.com"
            type="email"
          />

          <TextInput
            label="Employee LinkedIn URL"
            name="employee_linkedin"
            register={register}
            error={errors.employee_linkedin}
            placeholder="https://linkedin.com/in/rahul-sharma"
          />

          <TextInput
            label="Your Email"
            name="user_email"
            register={register}
            error={errors.user_email}
            placeholder="you@gmail.com"
            type="email"
            required
          />
        </div>

        <div className="mt-6 grid gap-6">
          <TextArea
            label="Employee Profile Text"
            name="employee_profile_text"
            register={register}
            error={errors.employee_profile_text}
            placeholder="Paste public LinkedIn summary, role, experience, or notes here..."
            rows={5}
          />

          <TextArea
            label="Your Profile / Resume Summary"
            name="user_profile"
            register={register}
            error={errors.user_profile}
            placeholder="Backend engineer with AWS, RAG, LangGraph, OpenAI, PostgreSQL experience..."
            rows={5}
            required
          />
        </div>

        <div className="mt-8 flex flex-col gap-3 border-t border-slate-100 pt-6 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-sm text-slate-500">
            Outreach email will not be sent unless you approve it later.
          </p>

          <button
            type="submit"
            disabled={isSubmittingForm}
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-brand-600 px-6 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSubmittingForm ? (
              <>
                <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />
                Starting Research...
              </>
            ) : (
              <>
                <Sparkles size={18} />
                <p className="text-black">Generate Research Report</p>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}