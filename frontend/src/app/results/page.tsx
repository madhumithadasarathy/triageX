"use client";
import { useEffect, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  Activity, ArrowLeft, Download, RefreshCw, Stethoscope,
  HeartPulse, Shield, FileText, AlertCircle, CheckCircle, Clock
} from "lucide-react";
import SeverityGauge from "@/components/SeverityGauge";
import BodyDiagram from "@/components/BodyDiagram";
import ReasoningPanel from "@/components/ReasoningPanel";
import EmergencyAlert from "@/components/EmergencyAlert";
import DisclaimerBanner from "@/components/DisclaimerBanner";
import { triageApi, reportApi } from "@/services/api";

interface TriageResult {
  session_id: string;
  urgency_level: string;
  severity_score: number;
  recommended_action: string;
  is_emergency: boolean;
  symptoms_extracted: string[];
  symptom_categories: string[];
  triggered_rules: any[];
  reasoning: string;
  key_factors: string[];
  affected_regions: any[];
  condition_images: any[];
  clinical_summary: string;
  patient_summary: string;
}

function ResultsContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const sessionId = searchParams.get("session");
  const [result, setResult] = useState<TriageResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    if (sessionId) fetchResult();
  }, [sessionId]);

  const fetchResult = async () => {
    try {
      setLoading(true);
      const data = await triageApi.getResult(sessionId!);
      setResult(data);
    } catch {
      console.error("Failed to fetch result");
    } finally {
      setLoading(false);
    }
  };

  const downloadPdf = async () => {
    if (!sessionId) return;
    setDownloading(true);
    try {
      const blob = await reportApi.downloadPdf(sessionId);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `triagex_report_${sessionId}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      alert("Failed to download report. Please try again.");
    } finally {
      setDownloading(false);
    }
  };

  const getActionConfig = (action: string) => {
    switch (action) {
      case "emergency":
        return { label: "Seek Emergency Care", icon: AlertCircle, color: "text-red-600", bg: "bg-red-50 dark:bg-red-500/10", border: "border-red-200 dark:border-red-500/20" };
      case "consult-doctor":
        return { label: "Consult a Doctor", icon: Stethoscope, color: "text-amber-600", bg: "bg-amber-50 dark:bg-amber-500/10", border: "border-amber-200 dark:border-amber-500/20" };
      default:
        return { label: "Self-Care at Home", icon: CheckCircle, color: "text-green-600", bg: "bg-green-50 dark:bg-green-500/10", border: "border-green-200 dark:border-green-500/20" };
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

  if (!result) {
    return (
      <div className="min-h-screen pt-24 flex flex-col items-center justify-center gap-4">
        <p className="text-slate-500">No results found. Start a new assessment.</p>
        <button onClick={() => router.push("/chat")} className="btn-primary">
          Start Assessment
        </button>
      </div>
    );
  }

  const actionConfig = getActionConfig(result.recommended_action);

  return (
    <div className="min-h-screen pt-20 pb-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <button onClick={() => router.push("/chat")} className="p-2 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
              <ArrowLeft className="w-5 h-5 text-slate-500" />
            </button>
            <div>
              <h1 className="text-xl font-bold text-slate-800 dark:text-white">Triage Results</h1>
              <p className="text-xs text-slate-500">Session: {result.session_id.slice(0, 8)}...</p>
            </div>
          </div>
          <div className="flex gap-2">
            <button onClick={downloadPdf} disabled={downloading} className="btn-secondary flex items-center gap-2 text-sm px-4 py-2">
              {downloading ? <Activity className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
              PDF Report
            </button>
            <button onClick={() => router.push("/chat")} className="btn-primary flex items-center gap-2 text-sm px-4 py-2">
              <RefreshCw className="w-4 h-4" />
              New
            </button>
          </div>
        </motion.div>

        {/* Emergency Alert */}
        {result.is_emergency && <div className="mb-6"><EmergencyAlert /></div>}

        {/* Main Grid */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* Severity + Action Row */}
            <div className="grid md:grid-cols-2 gap-6">
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6 flex flex-col items-center">
                <SeverityGauge score={result.severity_score} urgencyLevel={result.urgency_level} />
              </motion.div>

              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="space-y-4">
                {/* Recommended Action */}
                <div className={`${actionConfig.bg} ${actionConfig.border} border rounded-2xl p-5`}>
                  <div className="flex items-center gap-3 mb-2">
                    <actionConfig.icon className={`w-6 h-6 ${actionConfig.color}`} />
                    <h3 className={`font-bold ${actionConfig.color}`}>{actionConfig.label}</h3>
                  </div>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    {result.recommended_action === "emergency"
                      ? "Your symptoms indicate a potentially serious condition. Please seek immediate medical attention."
                      : result.recommended_action === "consult-doctor"
                      ? "We recommend scheduling an appointment with your healthcare provider."
                      : "Your symptoms appear manageable with rest and self-care. Monitor for changes."}
                  </p>
                </div>

                {/* Symptoms */}
                <div className="glass-card p-5">
                  <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3 flex items-center gap-2">
                    <HeartPulse className="w-4 h-4 text-pink-500" />
                    Symptoms Detected
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {result.symptoms_extracted.map((s) => (
                      <span key={s} className="text-xs bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400 px-3 py-1.5 rounded-full font-medium">
                        {s}
                      </span>
                    ))}
                  </div>
                  {result.symptom_categories.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-1.5">
                      {result.symptom_categories.map((c) => (
                        <span key={c} className="text-[11px] bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400 px-2 py-0.5 rounded-full">
                          {c}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            </div>

            {/* Reasoning Panel */}
            <ReasoningPanel
              reasoning={result.reasoning}
              triggeredRules={result.triggered_rules}
              keyFactors={result.key_factors}
            />

            {/* Patient Summary */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="glass-card p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-500/10 flex items-center justify-center">
                  <FileText className="w-5 h-5 text-emerald-500" />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-800 dark:text-white">Patient Summary</h3>
                  <p className="text-xs text-slate-500">Easy-to-understand explanation</p>
                </div>
              </div>
              <div className="bg-slate-50 dark:bg-slate-800/50 rounded-xl p-4 text-sm text-slate-600 dark:text-slate-400 whitespace-pre-line leading-relaxed">
                {result.patient_summary}
              </div>
            </motion.div>
          </div>

          {/* Right Column — Body Diagram */}
          <div className="space-y-6">
            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }} className="glass-card p-6">
              <h3 className="font-semibold text-slate-800 dark:text-white mb-4 flex items-center gap-2">
                <Shield className="w-5 h-5 text-blue-500" />
                Affected Body Areas
              </h3>
              <BodyDiagram affectedRegions={result.affected_regions} />

              {/* Legend */}
              <div className="flex items-center justify-center gap-4 mt-4 text-xs">
                <div className="flex items-center gap-1.5">
                  <div className="w-3 h-3 rounded-full bg-green-500" />
                  <span className="text-slate-500">Low</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-3 h-3 rounded-full bg-yellow-500" />
                  <span className="text-slate-500">Medium</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-3 h-3 rounded-full bg-red-500" />
                  <span className="text-slate-500">High</span>
                </div>
              </div>
            </motion.div>

            {/* Condition Images */}
            {result.condition_images.length > 0 && (
              <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }} className="glass-card p-6">
                <h3 className="font-semibold text-slate-800 dark:text-white mb-3">Condition Illustrations</h3>
                <div className="space-y-3">
                  {result.condition_images.map((img: any, i: number) => (
                    <div key={i} className="bg-slate-50 dark:bg-slate-800/50 rounded-xl p-3">
                      <div className="font-medium text-sm text-slate-700 dark:text-slate-300">{img.label}</div>
                      <div className="text-xs text-slate-500 mt-0.5">{img.description}</div>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}

            <DisclaimerBanner />
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ResultsPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen pt-24 flex items-center justify-center">
        <Activity className="w-8 h-8 text-blue-500 animate-spin" />
      </div>
    }>
      <ResultsContent />
    </Suspense>
  );
}
