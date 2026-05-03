export default function LoadingSpinner({ label = "Loading..." }) {
  return (
    <div className="flex items-center justify-center gap-3 rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
      <div className="h-6 w-6 animate-spin rounded-full border-2 border-slate-200 border-t-brand-600" />
      <p className="text-sm font-medium text-slate-600">
        {label}
      </p>
    </div>
  );
}