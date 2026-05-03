export default function ReportSection({ title, children, action }) {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex items-start justify-between gap-4">
        <h2 className="text-lg font-bold text-slate-900">
          {title}
        </h2>

        {action}
      </div>

      <div className="text-sm leading-7 text-slate-700">
        {children}
      </div>
    </section>
  );
}