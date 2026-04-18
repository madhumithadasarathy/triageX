"use client";
import { motion } from "framer-motion";
import { useEffect, useState } from "react";

interface SeverityGaugeProps {
  score: number;
  urgencyLevel: string;
  size?: number;
}

export default function SeverityGauge({ score, urgencyLevel, size = 220 }: SeverityGaugeProps) {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => setAnimatedScore(score), 300);
    return () => clearTimeout(timer);
  }, [score]);

  const radius = (size - 30) / 2;
  const circumference = Math.PI * radius; // half circle
  const progress = (animatedScore / 100) * circumference;

  const getColor = () => {
    if (animatedScore >= 61) return "#EF4444";
    if (animatedScore >= 31) return "#EAB308";
    return "#22C55E";
  };

  const getGradientId = () => {
    if (animatedScore >= 61) return "gaugeGradientHigh";
    if (animatedScore >= 31) return "gaugeGradientMedium";
    return "gaugeGradientLow";
  };

  const getLabel = () => {
    if (urgencyLevel === "HIGH") return "High Risk";
    if (urgencyLevel === "MEDIUM") return "Moderate";
    return "Low Risk";
  };

  const center = size / 2;
  const startAngle = Math.PI;
  const endAngle = 2 * Math.PI;

  // Build arc path for background
  const bgArc = describeArc(center, center + 10, radius, 180, 360);
  const fgAngle = 180 + (animatedScore / 100) * 180;
  const fgArc = describeArc(center, center + 10, radius, 180, fgAngle);

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size * 0.65} viewBox={`0 0 ${size} ${size * 0.65}`}>
        <defs>
          <linearGradient id="gaugeGradientLow" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#22C55E" />
            <stop offset="100%" stopColor="#4ADE80" />
          </linearGradient>
          <linearGradient id="gaugeGradientMedium" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#EAB308" />
            <stop offset="100%" stopColor="#FACC15" />
          </linearGradient>
          <linearGradient id="gaugeGradientHigh" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#EF4444" />
            <stop offset="100%" stopColor="#F87171" />
          </linearGradient>
          <filter id="gaugeGlow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Background arc */}
        <path
          d={bgArc}
          fill="none"
          stroke="#E2E8F0"
          strokeWidth="14"
          strokeLinecap="round"
          className="dark:stroke-slate-700"
        />

        {/* Tick marks */}
        {[0, 25, 50, 75, 100].map((tick) => {
          const angle = 180 + (tick / 100) * 180;
          const rad = (angle * Math.PI) / 180;
          const x1 = center + (radius - 18) * Math.cos(rad);
          const y1 = center + 10 + (radius - 18) * Math.sin(rad);
          const x2 = center + (radius + 8) * Math.cos(rad);
          const y2 = center + 10 + (radius + 8) * Math.sin(rad);
          return (
            <line
              key={tick}
              x1={x1} y1={y1} x2={x2} y2={y2}
              stroke="#94A3B8"
              strokeWidth="1.5"
              className="dark:stroke-slate-600"
            />
          );
        })}

        {/* Progress arc */}
        <motion.path
          d={fgArc}
          fill="none"
          stroke={`url(#${getGradientId()})`}
          strokeWidth="14"
          strokeLinecap="round"
          filter="url(#gaugeGlow)"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 1.5, ease: "easeOut" }}
        />

        {/* Center score text */}
        <motion.text
          x={center}
          y={center - 5}
          textAnchor="middle"
          className="fill-slate-800 dark:fill-white font-bold"
          fontSize="36"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          {Math.round(animatedScore)}
        </motion.text>

        <text
          x={center}
          y={center + 16}
          textAnchor="middle"
          className="fill-slate-400 dark:fill-slate-500"
          fontSize="12"
        >
          / 100
        </text>
      </svg>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="text-center -mt-2"
      >
        <span
          className="severity-badge text-sm"
          style={{
            background: `${getColor()}15`,
            color: getColor(),
          }}
        >
          {getLabel()}
        </span>
      </motion.div>
    </div>
  );
}

// Helper to describe an SVG arc
function describeArc(cx: number, cy: number, r: number, startAngle: number, endAngle: number): string {
  const start = polarToCartesian(cx, cy, r, endAngle);
  const end = polarToCartesian(cx, cy, r, startAngle);
  const largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
  return `M ${start.x} ${start.y} A ${r} ${r} 0 ${largeArcFlag} 0 ${end.x} ${end.y}`;
}

function polarToCartesian(cx: number, cy: number, r: number, angleDeg: number) {
  const angleRad = ((angleDeg - 0) * Math.PI) / 180;
  return {
    x: cx + r * Math.cos(angleRad),
    y: cy + r * Math.sin(angleRad),
  };
}
