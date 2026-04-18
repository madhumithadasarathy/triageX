"use client";
import { motion } from "framer-motion";
import { Siren, Phone } from "lucide-react";

export default function EmergencyAlert() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="w-full bg-red-50 dark:bg-red-500/10 border-2 border-red-400 dark:border-red-500/40 rounded-2xl p-5"
    >
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-xl bg-red-100 dark:bg-red-500/20 flex items-center justify-center shrink-0">
          <Siren className="w-6 h-6 text-red-600 dark:text-red-400 pulse-dot" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-red-700 dark:text-red-400 mb-1">
            ⚠️ Emergency Alert
          </h3>
          <p className="text-sm text-red-600 dark:text-red-300 mb-3">
            Based on your symptoms, this may require <strong>immediate medical attention</strong>.
            Please contact emergency services or visit the nearest emergency room.
          </p>
          <a
            href="tel:112"
            className="inline-flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-5 py-2.5 rounded-xl text-sm font-semibold transition-colors"
          >
            <Phone className="w-4 h-4" />
            Call Emergency (112)
          </a>
        </div>
      </div>
    </motion.div>
  );
}
