import { FileSearch } from "lucide-react";
import { Link } from "react-router-dom";

export default function EmptyState() {
  return (
    <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center">
      <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-100 text-slate-600">
        <FileSearch size={28} />
      </div>

      <h3 className="text-lg font-bold text-slate-900">
        No report found
      </h3>

      <p className="mx-auto mt-2 max-w-md text-sm text-slate-500">
        Start a new company and employee research workflow to generate a report.
      </p>

      <Link
        to="/research/new"
        className="mt-6 inline-flex rounded-xl bg-brand-600 px-5 py-3 text-sm font-semibold text-white hover:bg-brand-700"
      >
        Create Research Report
      </Link>
    </div>
  );
}