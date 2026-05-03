import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import CreateResearch from "./pages/CreateResearch";
import ReportDetails from "./pages/ReportDetails";
import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <div className="relative min-h-screen overflow-hidden">
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -left-16 top-10 h-80 w-80 rounded-full bg-brand-500/25 blur-3xl animate-background-flow" />
        <div className="absolute right-0 top-1/4 h-72 w-72 rounded-full bg-slate-400/20 blur-3xl animate-background-flow animation-delay-2000" />
        <div className="absolute left-1/2 top-[60%] h-96 w-96 -translate-x-1/2 rounded-full bg-cyan-300/20 blur-3xl animate-background-flow animation-delay-4000" />
      </div>

      <Navbar />

      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/research/new" element={<CreateResearch />} />
          <Route path="/reports/:reportId" element={<ReportDetails />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
    </div>
  );
}