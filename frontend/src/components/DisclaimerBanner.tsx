"use client";
import { motion } from "framer-motion";
import { AlertTriangle } from "lucide-react";

export default function DisclaimerBanner() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full bg-amber-50 dark:bg-amber-500/10 border border-amber-200 dark:border-amber-500/20 rounded-xl p-3 flex items-center gap-3"
    >
      <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0" />
      <p className="text-xs text-amber-700 dark:text-amber-400">
        <strong>Disclaimer:</strong> TriageX is not a diagnostic tool. Always consult a medical professional for proper diagnosis and treatment.
      </p>
    </motion.div>
  );
}
