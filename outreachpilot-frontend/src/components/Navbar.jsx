import { Link, NavLink } from "react-router-dom";
import { Bot, PlusCircle } from "lucide-react";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/90 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4">
        <Link to="/" className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-brand-600 text-white shadow-sm">
            <Bot size={22} />
          </div>

          <div>
            <h1 className="text-lg font-bold tracking-tight text-slate-900">
              OutreachPilot AI
            </h1>
            <p className="text-xs text-slate-500">
              Multi-Agent Research Assistant
            </p>
          </div>
        </Link>

        <nav className="flex items-center gap-3">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `hidden rounded-xl px-4 py-2 text-sm font-medium sm:inline-flex ${
                isActive
                  ? "bg-slate-100 text-slate-900"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`
            }
          >
            Home
          </NavLink>

          <Link
            to="/research/new"
            className="inline-flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700"
          >
            <PlusCircle size={18} />
            New Research
          </Link>
        </nav>
      </div>
    </header>
  );
}