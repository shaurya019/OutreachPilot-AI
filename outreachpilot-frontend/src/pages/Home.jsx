import { Link } from "react-router-dom";
import {
  ArrowRight,
  Building2,
  MailCheck,
  ShieldCheck,
  UserSearch,
  Workflow,
} from "lucide-react";

const features = [
  {
    icon: Building2,
    title: "Company Research",
    description:
      "Analyze company website, products, positioning, and useful business signals.",
  },
  {
    icon: UserSearch,
    title: "Employee Intelligence",
    description:
      "Summarize employee role, seniority, relevance, and possible personalization hooks.",
  },
  {
    icon: Workflow,
    title: "LangGraph Multi-Agent Flow",
    description:
      "Separate agents for research, personalization, report generation, email drafting, and review.",
  },
  {
    icon: MailCheck,
    title: "Report + Outreach Draft",
    description:
      "Generate a structured research report, cold email, LinkedIn note, and follow-up.",
  },
  {
    icon: ShieldCheck,
    title: "Human Approval",
    description:
      "Outreach email is sent only after explicit approval from the user.",
  },
];

export default function Home() {
  return (
    <div>
      <section className="border-b border-slate-200 bg-white">
        <div className="mx-auto grid max-w-7xl gap-10 px-5 py-20 lg:grid-cols-2 lg:items-center">
          <div>
            <div className="mb-5 inline-flex rounded-full bg-brand-50 px-4 py-2 text-sm font-semibold text-brand-700 ring-1 ring-brand-100">
              AI Research + Outreach Automation
            </div>

            <h1 className="max-w-3xl text-4xl font-black tracking-tight text-slate-950 sm:text-5xl">
              Multi-agent company and employee research assistant.
            </h1>

            <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-600">
              OutreachPilot AI researches a company and employee, generates a
              professional report, creates personalized outreach drafts, and
              sends emails only after approval.
            </p>

            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                to="/research/new"
                className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-6 py-3 text-sm font-bold text-black shadow-sm hover:bg-brand-700"
              >
                Start Research
                <ArrowRight size={18} />
              </Link>

              <a
                href="#features"
                className="inline-flex items-center rounded-xl border border-slate-200 bg-white px-6 py-3 text-sm font-bold text-slate-700 shadow-sm hover:bg-slate-50"
              >
                View Features
              </a>
            </div>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5 shadow-sm">
            <div className="rounded-2xl bg-white p-6 shadow-sm">
              <p className="text-sm font-semibold text-slate-500">
                Example Workflow
              </p>

              <div className="mt-5 space-y-3">
                {[
                  "Submit company + employee details",
                  "Research agents collect insights",
                  "Personalization agent creates hooks",
                  "Report generator builds final report",
                  "Reviewer checks safety and quality",
                  "User approves before outreach is sent",
                ].map((item, index) => (
                  <div
                    key={item}
                    className="flex items-center gap-3 rounded-xl border border-slate-100 bg-slate-50 p-3"
                  >
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-brand-600 text-sm font-bold text-white">
                      {index + 1}
                    </div>
                    <p className="text-sm font-medium text-slate-700">
                      {item}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="features" className="mx-auto max-w-7xl px-5 py-16">
        <div className="mb-8">
          <h2 className="text-2xl font-black text-slate-950">
            Core Features
          </h2>
          <p className="mt-2 text-slate-600">
            Built for a strong AI Engineer portfolio project.
          </p>
        </div>

        <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {features.map((feature) => {
            const Icon = feature.icon;

            return (
              <div
                key={feature.title}
                className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
              >
                <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-brand-50 text-brand-700">
                  <Icon size={22} />
                </div>

                <h3 className="text-base font-bold text-slate-900">
                  {feature.title}
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-600">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}