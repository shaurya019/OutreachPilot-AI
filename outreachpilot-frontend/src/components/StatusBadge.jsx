const styles = {
  pending: "bg-amber-50 text-amber-700 ring-amber-200",
  running: "bg-blue-50 text-blue-700 ring-blue-200",
  completed: "bg-emerald-50 text-emerald-700 ring-emerald-200",
  failed: "bg-red-50 text-red-700 ring-red-200",
  approved: "bg-emerald-50 text-emerald-700 ring-emerald-200",
  rejected: "bg-red-50 text-red-700 ring-red-200",
  sent: "bg-indigo-50 text-indigo-700 ring-indigo-200",
  not_sent: "bg-slate-50 text-slate-700 ring-slate-200",
};

export default function StatusBadge({ status }) {
  const normalized = status || "pending";

  return (
    <span
      className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold capitalize ring-1 ${
        styles[normalized] || styles.pending
      }`}
    >
      {normalized.replaceAll("_", " ")}
    </span>
  );
}