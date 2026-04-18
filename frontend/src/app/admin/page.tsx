"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import {
  LayoutDashboard, Activity, AlertTriangle, AlertCircle,
  CheckCircle, Siren, Search, Filter, Eye, Clock,
  TrendingUp, Users, ChevronRight
} from "lucide-react";
import { adminApi } from "@/services/api";

interface CaseItem {
  id: number;
  session_id: string;
  symptoms_raw: string;
  urgency_level: string;
  severity_score: number;
  recommended_action: string;
  is_emergency: number;
  created_at: string;
  username?: string;
}

interface Stats {
  total_cases: number;
  high_severity: number;
  medium_severity: number;
  low_severity: number;
  emergencies: number;
  recent_cases: CaseItem[];
}

export default function AdminPage() {
  const router = useRouter();
  const [stats, setStats] = useState<Stats | null>(null);
  const [cases, setCases] = useState<CaseItem[]>([]);
  const [filter, setFilter] = useState<string>("all");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    fetchCases();
  }, [filter, search]);

  const fetchData = async () => {
    try {
      const data = await adminApi.getStats();
      setStats(data);
      setCases(data.recent_cases);
    } catch {
      console.error("Failed to fetch stats");
    } finally {
      setLoading(false);
    }
  };

  const fetchCases = async () => {
    try {
      const params: any = { limit: 50 };
      if (filter !== "all") params.severity = filter;
      if (search) params.search = search;
      const data = await adminApi.getCases(params);
      setCases(data.cases);
    } catch {
      // fall back to stats data
    }
  };

  const statCards = [
    { label: "Total Cases", value: stats?.total_cases ?? 0, icon: Users, color: "text-blue-500", bg: "bg-blue-50 dark:bg-blue-500/10" },
    { label: "High Severity", value: stats?.high_severity ?? 0, icon: AlertTriangle, color: "text-red-500", bg: "bg-red-50 dark:bg-red-500/10" },
    { label: "Medium", value: stats?.medium_severity ?? 0, icon: AlertCircle, color: "text-amber-500", bg: "bg-amber-50 dark:bg-amber-500/10" },
    { label: "Low Severity", value: stats?.low_severity ?? 0, icon: CheckCircle, color: "text-green-500", bg: "bg-green-50 dark:bg-green-500/10" },
    { label: "Emergencies", value: stats?.emergencies ?? 0, icon: Siren, color: "text-red-600", bg: "bg-red-50 dark:bg-red-500/10" },
  ];

  const getSeverityBadge = (level: string) => {
    switch (level) {
      case "HIGH": return "severity-badge high";
      case "MEDIUM": return "severity-badge medium";
      default: return "severity-badge low";
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen pt-24 flex items-center justify-center">
        <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: "linear" }}>
          <Activity className="w-8 h-8 text-blue-500" />
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-20 pb-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <div className="flex items-center gap-3 mb-1">
            <div className="w-10 h-10 rounded-xl gradient-bg flex items-center justify-center">
              <LayoutDashboard className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-slate-800 dark:text-white">Admin Dashboard</h1>
          </div>
          <p className="text-sm text-slate-500 ml-13">Monitor and manage all triage cases</p>
        </motion.div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          {statCards.map((card, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="glass-card p-5"
            >
              <div className="flex items-center justify-between mb-3">
                <div className={`w-10 h-10 rounded-xl ${card.bg} flex items-center justify-center`}>
                  <card.icon className={`w-5 h-5 ${card.color}`} />
                </div>
              </div>
              <div className="text-2xl font-bold text-slate-800 dark:text-white">{card.value}</div>
              <div className="text-xs text-slate-500 mt-0.5">{card.label}</div>
            </motion.div>
          ))}
        </div>

        {/* Filters */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }} className="glass-card p-4 mb-6">
          <div className="flex flex-col sm:flex-row gap-4">
            {/* Search */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search symptoms..."
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-sm outline-none focus:border-blue-400 transition-colors"
              />
            </div>

            {/* Filter buttons */}
            <div className="flex gap-2">
              {["all", "HIGH", "MEDIUM", "LOW"].map((f) => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                    filter === f
                      ? "gradient-bg text-white shadow-md"
                      : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700"
                  }`}
                >
                  {f === "all" ? "All" : f}
                </button>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Cases Table */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="glass-card overflow-hidden">
          <div className="p-5 border-b border-slate-100 dark:border-slate-700">
            <h2 className="font-semibold text-slate-800 dark:text-white flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-blue-500" />
              Triage Cases
              <span className="text-xs bg-slate-100 dark:bg-slate-700 px-2 py-0.5 rounded-full text-slate-500">
                {cases.length}
              </span>
            </h2>
          </div>

          {cases.length === 0 ? (
            <div className="p-12 text-center text-slate-400">
              <Activity className="w-10 h-10 mx-auto mb-3 opacity-30" />
              <p>No triage cases found.</p>
              <p className="text-xs mt-1">Start an assessment to see cases here.</p>
            </div>
          ) : (
            <div className="divide-y divide-slate-100 dark:divide-slate-700">
              {cases.map((c, i) => (
                <motion.div
                  key={c.session_id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: i * 0.03 }}
                  className="p-4 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors cursor-pointer group"
                  onClick={() => router.push(`/results?session=${c.session_id}`)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-1">
                        <span className={getSeverityBadge(c.urgency_level)}>
                          {c.urgency_level}
                        </span>
                        {c.is_emergency === 1 && (
                          <span className="text-[10px] bg-red-100 text-red-600 dark:bg-red-500/10 dark:text-red-400 px-2 py-0.5 rounded-full font-bold flex items-center gap-1">
                            <Siren className="w-3 h-3" />
                            EMERGENCY
                          </span>
                        )}
                        <span className="text-xs text-slate-400">
                          Score: {c.severity_score?.toFixed(0) ?? "—"}
                        </span>
                      </div>
                      <p className="text-sm text-slate-700 dark:text-slate-300 line-clamp-1">
                        {c.symptoms_raw}
                      </p>
                      <div className="flex items-center gap-3 mt-1.5 text-xs text-slate-400">
                        <span className="flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {c.created_at ? new Date(c.created_at).toLocaleString() : "—"}
                        </span>
                        {c.username && <span>User: {c.username}</span>}
                      </div>
                    </div>
                    <ChevronRight className="w-5 h-5 text-slate-300 group-hover:text-blue-500 transition-colors" />
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
