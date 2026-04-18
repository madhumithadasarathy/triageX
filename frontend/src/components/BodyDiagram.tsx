"use client";
import { motion } from "framer-motion";
import { useState } from "react";

interface AffectedRegion {
  region: string;
  display_name?: string;
  severity: string;
  color: string;
  symptoms: string[];
  svg_id?: string;
}

interface BodyDiagramProps {
  affectedRegions: AffectedRegion[];
  view?: "front" | "back";
}

const REGION_PATHS: Record<string, { d: string; cx?: number; cy?: number }> = {
  head: { cx: 200, cy: 52 },
  chest: { cx: 200, cy: 150 },
  abdomen: { cx: 200, cy: 220 },
  left_arm: { cx: 138, cy: 180 },
  right_arm: { cx: 262, cy: 180 },
  left_leg: { cx: 175, cy: 340 },
  right_leg: { cx: 225, cy: 340 },
  back: { cx: 200, cy: 170 },
  full_body: { cx: 200, cy: 200 },
};

export default function BodyDiagram({ affectedRegions, view = "front" }: BodyDiagramProps) {
  const [hoveredRegion, setHoveredRegion] = useState<string | null>(null);

  const getRegionColor = (regionKey: string) => {
    const region = affectedRegions.find((r) => r.region === regionKey);
    if (!region) return "transparent";
    return region.color;
  };

  const getRegionData = (regionKey: string) => {
    return affectedRegions.find((r) => r.region === regionKey);
  };

  const isAffected = (regionKey: string) => {
    return affectedRegions.some((r) => r.region === regionKey || r.region === "full_body");
  };

  return (
    <div className="relative">
      <svg viewBox="0 0 400 460" className="w-full max-w-sm mx-auto" xmlns="http://www.w3.org/2000/svg">
        {/* Background subtle grid */}
        <defs>
          <radialGradient id="bodyGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#2563EB" stopOpacity="0.03" />
            <stop offset="100%" stopColor="#2563EB" stopOpacity="0" />
          </radialGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="4" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <rect width="400" height="460" fill="url(#bodyGlow)" rx="20" />

        {/* HEAD */}
        <motion.ellipse
          cx="200" cy="52" rx="30" ry="35"
          fill={isAffected("head") ? getRegionColor("head") : "#CBD5E1"}
          fillOpacity={isAffected("head") ? 0.35 : 0.2}
          stroke={isAffected("head") ? getRegionColor("head") : "#94A3B8"}
          strokeWidth="2"
          onMouseEnter={() => setHoveredRegion("head")}
          onMouseLeave={() => setHoveredRegion(null)}
          className="cursor-pointer transition-all duration-300"
          whileHover={{ scale: 1.05 }}
          filter={isAffected("head") ? "url(#glow)" : "none"}
        />

        {/* NECK */}
        <rect x="190" y="85" width="20" height="18" rx="4" fill="#CBD5E1" fillOpacity="0.2" stroke="#94A3B8" strokeWidth="1.5" />

        {/* CHEST/TORSO */}
        <motion.path
          d="M155 103 Q155 98 165 98 L235 98 Q245 98 245 103 L250 185 Q250 190 245 190 L155 190 Q150 190 150 185 Z"
          fill={isAffected("chest") ? getRegionColor("chest") : "#CBD5E1"}
          fillOpacity={isAffected("chest") ? 0.35 : 0.2}
          stroke={isAffected("chest") ? getRegionColor("chest") : "#94A3B8"}
          strokeWidth="2"
          onMouseEnter={() => setHoveredRegion("chest")}
          onMouseLeave={() => setHoveredRegion(null)}
          className="cursor-pointer transition-all duration-300"
          whileHover={{ scale: 1.02 }}
          filter={isAffected("chest") ? "url(#glow)" : "none"}
        />

        {/* ABDOMEN */}
        <motion.path
          d="M155 190 L245 190 L240 270 Q240 275 235 275 L165 275 Q160 275 160 270 Z"
          fill={isAffected("abdomen") ? getRegionColor("abdomen") : "#CBD5E1"}
          fillOpacity={isAffected("abdomen") ? 0.35 : 0.2}
          stroke={isAffected("abdomen") ? getRegionColor("abdomen") : "#94A3B8"}
          strokeWidth="2"
          onMouseEnter={() => setHoveredRegion("abdomen")}
          onMouseLeave={() => setHoveredRegion(null)}
          className="cursor-pointer transition-all duration-300"
          whileHover={{ scale: 1.02 }}
          filter={isAffected("abdomen") ? "url(#glow)" : "none"}
        />

        {/* LEFT ARM */}
        <motion.path
          d="M155 103 L130 108 L110 170 L100 240 L115 242 L128 180 L140 140 L150 115"
          fill="none"
          stroke={isAffected("left_arm") ? getRegionColor("left_arm") : "#94A3B8"}
          strokeWidth={isAffected("left_arm") ? 14 : 10}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeOpacity={isAffected("left_arm") ? 0.6 : 0.3}
          onMouseEnter={() => setHoveredRegion("left_arm")}
          onMouseLeave={() => setHoveredRegion(null)}
          className="cursor-pointer transition-all duration-300"
          filter={isAffected("left_arm") ? "url(#glow)" : "none"}
        />

        {/* RIGHT ARM */}
        <motion.path
          d="M245 103 L270 108 L290 170 L300 240 L285 242 L272 180 L260 140 L250 115"
          fill="none"
          stroke={isAffected("right_arm") ? getRegionColor("right_arm") : "#94A3B8"}
          strokeWidth={isAffected("right_arm") ? 14 : 10}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeOpacity={isAffected("right_arm") ? 0.6 : 0.3}
          onMouseEnter={() => setHoveredRegion("right_arm")}
          onMouseLeave={() => setHoveredRegion(null)}
          className="cursor-pointer transition-all duration-300"
          filter={isAffected("right_arm") ? "url(#glow)" : "none"}
        />

        {/* LEFT LEG */}
        <motion.path
          d="M170 275 L165 340 L160 400 L155 435 L175 435 L178 400 L180 340 L185 280"
          fill="none"
          stroke={isAffected("left_leg") ? getRegionColor("left_leg") : "#94A3B8"}
          strokeWidth={isAffected("left_leg") ? 14 : 10}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeOpacity={isAffected("left_leg") ? 0.6 : 0.3}
          onMouseEnter={() => setHoveredRegion("left_leg")}
          onMouseLeave={() => setHoveredRegion(null)}
          className="cursor-pointer transition-all duration-300"
          filter={isAffected("left_leg") ? "url(#glow)" : "none"}
        />

        {/* RIGHT LEG */}
        <motion.path
          d="M230 275 L235 340 L240 400 L245 435 L225 435 L222 400 L220 340 L215 280"
          fill="none"
          stroke={isAffected("right_leg") ? getRegionColor("right_leg") : "#94A3B8"}
          strokeWidth={isAffected("right_leg") ? 14 : 10}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeOpacity={isAffected("right_leg") ? 0.6 : 0.3}
          onMouseEnter={() => setHoveredRegion("right_leg")}
          onMouseLeave={() => setHoveredRegion(null)}
          className="cursor-pointer transition-all duration-300"
          filter={isAffected("right_leg") ? "url(#glow)" : "none"}
        />

        {/* Highlight dots for affected regions */}
        {affectedRegions.map((region) => {
          const pos = REGION_PATHS[region.region];
          if (!pos || !pos.cx) return null;
          return (
            <motion.circle
              key={region.region}
              cx={pos.cx}
              cy={pos.cy}
              r="6"
              fill={region.color}
              className="pulse-dot"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              filter="url(#glow)"
            />
          );
        })}

        {/* View Label */}
        <text x="200" y="455" textAnchor="middle" className="fill-slate-400 text-xs" fontSize="11">
          {view === "front" ? "Front View" : "Back View"}
        </text>
      </svg>

      {/* Hover tooltip */}
      {hoveredRegion && getRegionData(hoveredRegion) && (
        <motion.div
          initial={{ opacity: 0, y: 5 }}
          animate={{ opacity: 1, y: 0 }}
          className="absolute top-4 right-4 glass-card p-3 min-w-48 z-10"
        >
          <div className="flex items-center gap-2 mb-2">
            <div
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: getRegionData(hoveredRegion)!.color }}
            />
            <span className="font-semibold text-sm">
              {getRegionData(hoveredRegion)!.display_name || hoveredRegion}
            </span>
            <span className={`severity-badge ${getRegionData(hoveredRegion)!.severity.toLowerCase()}`}>
              {getRegionData(hoveredRegion)!.severity}
            </span>
          </div>
          <div className="flex flex-wrap gap-1">
            {getRegionData(hoveredRegion)!.symptoms.map((s) => (
              <span key={s} className="text-xs bg-slate-100 dark:bg-slate-700 px-2 py-0.5 rounded-full text-slate-600 dark:text-slate-300">
                {s}
              </span>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}
