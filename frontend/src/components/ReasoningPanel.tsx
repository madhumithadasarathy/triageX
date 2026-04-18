"use client";
import { motion } from "framer-motion";
import { ChevronDown, ChevronUp, Lightbulb, AlertCircle, CheckCircle, Info } from "lucide-react";
import { useState } from "react";

interface TriggeredRule {
  rule_id: string;
  rule_name: string;
  description: string;
  severity_contribution: number;
  matched_symptoms: string[];
}

interface ReasoningPanelProps {
  reasoning: string;
  triggeredRules: TriggeredRule[];
  keyFactors: string[];
}

export default function ReasoningPanel({ reasoning, triggeredRules, keyFactors }: ReasoningPanelProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card p-6"
    >
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between"
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-50 dark:bg-indigo-500/10 flex items-center justify-center">
            <Lightbulb className="w-5 h-5 text-indigo-500" />
          </div>
          <div className="text-left">
            <h3 className="font-semibold text-slate-800 dark:text-white">AI Reasoning</h3>
            <p className="text-xs text-slate-500">Why this result was generated</p>
          </div>
        </div>
        {expanded ? (
          <ChevronUp className="w-5 h-5 text-slate-400" />
        ) : (
          <ChevronDown className="w-5 h-5 text-slate-400" />
        )}
      </button>

      {expanded && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          className="mt-5 space-y-4"
        >
          {/* Key Factors */}
          {keyFactors.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2 flex items-center gap-2">
                <Info className="w-4 h-4 text-blue-500" />
                Key Factors
              </h4>
              <div className="space-y-1.5">
                {keyFactors.map((factor, i) => (
                  <div key={i} className="flex items-start gap-2 text-sm text-slate-600 dark:text-slate-400">
                    <span className="text-blue-500 mt-0.5">•</span>
                    {factor}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Triggered Rules */}
          {triggeredRules.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-amber-500" />
                Triggered Rules ({triggeredRules.length})
              </h4>
              <div className="space-y-2">
                {triggeredRules.map((rule) => (
                  <div
                    key={rule.rule_id}
                    className="bg-slate-50 dark:bg-slate-800/50 rounded-xl p-3 border border-slate-100 dark:border-slate-700"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                        [{rule.rule_id}] {rule.rule_name}
                      </span>
                      <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                        rule.severity_contribution >= 60
                          ? "bg-red-100 text-red-600 dark:bg-red-500/10 dark:text-red-400"
                          : rule.severity_contribution >= 30
                          ? "bg-amber-100 text-amber-600 dark:bg-amber-500/10 dark:text-amber-400"
                          : "bg-green-100 text-green-600 dark:bg-green-500/10 dark:text-green-400"
                      }`}>
                        {rule.severity_contribution}/100
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 dark:text-slate-400 mb-1.5">{rule.description}</p>
                    <div className="flex flex-wrap gap-1">
                      {rule.matched_symptoms.map((s) => (
                        <span
                          key={s}
                          className="text-[11px] bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400 px-2 py-0.5 rounded-full"
                        >
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {triggeredRules.length === 0 && (
            <div className="flex items-center gap-2 text-sm text-slate-500">
              <CheckCircle className="w-4 h-4 text-green-500" />
              No critical clinical rules were triggered. Assessment is based on general symptom analysis.
            </div>
          )}
        </motion.div>
      )}
    </motion.div>
  );
}
