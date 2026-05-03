import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="mx-auto flex min-h-[70vh] max-w-3xl flex-col items-center justify-center px-5 text-center">
      <h1 className="text-6xl font-black text-slate-950">
        404
      </h1>

      <p className="mt-4 text-lg font-semibold text-slate-700">
        Page not found
      </p>

      <p className="mt-2 text-slate-500">
        The page you are looking for does not exist.
      </p>

      <Link
        to="/"
        className="mt-6 rounded-xl bg-brand-600 px-5 py-3 text-sm font-bold text-white hover:bg-brand-700"
      >
        Go Home
      </Link>
    </div>
  );
}