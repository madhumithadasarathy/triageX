"use client";
import { motion } from "framer-motion";
import Link from "next/link";
import {
  Brain, MessageSquare, Eye, FileText, Shield, Activity,
  ArrowRight, Sparkles, Heart, Zap, Globe
} from "lucide-react";
import DisclaimerBanner from "@/components/DisclaimerBanner";

const features = [
  {
    icon: Brain,
    title: "Smart Symptom Analysis",
    desc: "Advanced NLP-powered symptom extraction and intelligent categorization using rule-based AI",
    color: "from-blue-500 to-indigo-500",
    bg: "bg-blue-50 dark:bg-blue-500/10",
  },
  {
    icon: Eye,
    title: "Visual Body Mapping",
    desc: "Interactive SVG body diagrams that highlight affected areas with severity color-coding",
    color: "from-emerald-500 to-teal-500",
    bg: "bg-emerald-50 dark:bg-emerald-500/10",
  },
  {
    icon: Sparkles,
    title: "Explainable AI",
    desc: "Full transparency — see exactly which rules triggered and why each decision was made",
    color: "from-violet-500 to-purple-500",
    bg: "bg-violet-50 dark:bg-violet-500/10",
  },
  {
    icon: FileText,
    title: "Doctor Reports",
    desc: "Generate structured clinical PDF reports with embedded visuals and AI reasoning",
    color: "from-orange-500 to-red-500",
    bg: "bg-orange-50 dark:bg-orange-500/10",
  },
];

const stats = [
  { value: "25+", label: "Clinical Rules" },
  { value: "10+", label: "Symptom Categories" },
  { value: "9", label: "Body Regions" },
  { value: "2", label: "Languages" },
];

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-24 pb-20 md:pt-32 md:pb-28">
        {/* Background decoration */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl" />
          <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-indigo-500/5 rounded-full blur-3xl" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-blue-500/3 to-indigo-500/3 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-4xl mx-auto">
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="inline-flex items-center gap-2 bg-blue-50 dark:bg-blue-500/10 border border-blue-200 dark:border-blue-500/20 rounded-full px-4 py-1.5 mb-8"
            >
              <Activity className="w-4 h-4 text-blue-500" />
              <span className="text-sm font-medium text-blue-700 dark:text-blue-400">
                AI-Powered Medical Triage
              </span>
            </motion.div>

            {/* Title */}
            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6"
            >
              <span className="gradient-text">TriageX</span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15 }}
              className="text-xl md:text-2xl font-medium text-slate-500 dark:text-slate-400 mb-4"
            >
              Explain. Assess. Act.
            </motion.p>

            <motion.p
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-base md:text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed"
            >
              Intelligent symptom assessment with visual explanations.
              Get instant severity evaluation, interactive body mapping,
              and personalized clinical guidance — powered by transparent AI.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="flex flex-col sm:flex-row items-center justify-center gap-4"
            >
              <Link href="/chat">
                <button className="btn-primary flex items-center gap-2 text-base px-8 py-3.5">
                  <MessageSquare className="w-5 h-5" />
                  Start Assessment
                  <ArrowRight className="w-4 h-4" />
                </button>
              </Link>
              <Link href="/admin">
                <button className="btn-secondary flex items-center gap-2 text-base px-8 py-3.5">
                  View Dashboard
                </button>
              </Link>
            </motion.div>
          </div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto"
          >
            {stats.map((stat, i) => (
              <div key={i} className="text-center glass-card p-4">
                <div className="text-2xl md:text-3xl font-bold gradient-text">{stat.value}</div>
                <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 bg-white/50 dark:bg-slate-900/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-slate-800 dark:text-white mb-4">
              Intelligent Triage, <span className="gradient-text">Visualized</span>
            </h2>
            <p className="text-slate-500 dark:text-slate-400 max-w-2xl mx-auto">
              TriageX combines rule-based clinical logic with NLP to deliver transparent,
              explainable medical triage assessments.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-6">
            {features.map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                whileHover={{ y: -4 }}
                className="glass-card p-8 group cursor-default"
              >
                <div className={`w-14 h-14 rounded-2xl ${feature.bg} flex items-center justify-center mb-5 group-hover:scale-110 transition-transform`}>
                  <feature.icon className={`w-7 h-7 bg-gradient-to-r ${feature.color} bg-clip-text`} style={{ color: feature.color.includes("blue") ? "#3B82F6" : feature.color.includes("emerald") ? "#10B981" : feature.color.includes("violet") ? "#8B5CF6" : "#F97316" }} />
                </div>
                <h3 className="text-xl font-bold text-slate-800 dark:text-white mb-2">{feature.title}</h3>
                <p className="text-slate-500 dark:text-slate-400 leading-relaxed">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-slate-800 dark:text-white mb-4">
              How It <span className="gradient-text">Works</span>
            </h2>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {[
              { step: "01", title: "Describe Symptoms", desc: "Chat with our AI assistant and describe what you're experiencing", icon: MessageSquare },
              { step: "02", title: "AI Analysis", desc: "Our engine extracts symptoms, applies clinical rules, and scores severity", icon: Brain },
              { step: "03", title: "Visual Results", desc: "See body mapping, severity gauge, reasoning, and get a clinical report", icon: Eye },
            ].map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15 }}
                className="text-center"
              >
                <div className="w-16 h-16 rounded-2xl gradient-bg flex items-center justify-center mx-auto mb-5 shadow-lg shadow-blue-500/20">
                  <item.icon className="w-7 h-7 text-white" />
                </div>
                <div className="text-xs font-bold text-blue-500 mb-2">STEP {item.step}</div>
                <h3 className="text-lg font-bold text-slate-800 dark:text-white mb-2">{item.title}</h3>
                <p className="text-sm text-slate-500 dark:text-slate-400">{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Disclaimer + Footer */}
      <section className="pb-12">
        <div className="max-w-3xl mx-auto px-4">
          <DisclaimerBanner />
        </div>
      </section>

      <footer className="py-8 border-t border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-2 mb-3">
            <Activity className="w-5 h-5 text-blue-500" />
            <span className="font-bold gradient-text">TriageX</span>
          </div>
          <p className="text-xs text-slate-400">
            © 2024 TriageX. AI-Powered Medical Triage Assistant. Not a diagnostic tool.
          </p>
        </div>
      </footer>
    </div>
  );
}
