import React, { useEffect, useState, useMemo } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import {
  Shield, AlertTriangle, TrendingUp, TrendingDown, Minus, ChevronDown,
  ChevronUp, Activity, Lightbulb, Zap, FileText, Target, Info,
  ArrowRight, Lock,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { PieChart, Pie, Cell, ResponsiveContainer, RadialBarChart, RadialBar } from "recharts";
import { toast } from "sonner";
import axios from "axios";
import SkeletonLoader from "@/components/SkeletonLoader";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const BAND_CONFIG = {
  excellent: { color: "text-emerald-400", bg: "bg-emerald-500/10", border: "border-emerald-900/40", ring: "#22c55e" },
  strong:   { color: "text-blue-400", bg: "bg-blue-500/10", border: "border-blue-900/40", ring: "#3b82f6" },
  warning:  { color: "text-amber-400", bg: "bg-amber-500/10", border: "border-amber-900/40", ring: "#f59e0b" },
  critical: { color: "text-red-400", bg: "bg-red-500/10", border: "border-red-900/40", ring: "#ef4444" },
};

const SEV_BADGE = {
  critical: "bg-red-950/40 text-red-300 border-red-900/50",
  high: "bg-orange-950/40 text-orange-300 border-orange-900/50",
  medium: "bg-amber-950/40 text-amber-300 border-amber-900/50",
  low: "bg-slate-800/50 text-slate-400 border-slate-700/50",
  info: "bg-blue-950/40 text-blue-300 border-blue-900/50",
};

const TrendIcon = ({ dir }) => {
  if (dir === "up") return <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />;
  if (dir === "down") return <TrendingDown className="w-3.5 h-3.5 text-red-400" />;
  return <Minus className="w-3.5 h-3.5 text-slate-500" />;
};

export default function IntelligenceCenterPage() {
  const { t, lang } = useLanguage();
  const [overview, setOverview] = useState(null);
  const [agents, setAgents] = useState([]);
  const [standards, setStandards] = useState([]);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [openSections, setOpenSections] = useState({ risks: true, remediations: true });

  useEffect(() => {
    Promise.all([
      axios.get(`${API}/score/overview`),
      axios.get(`${API}/score/agents`),
      axios.get(`${API}/score/standards`),
      axios.get(`${API}/score/insights`),
    ])
      .then(([ov, ag, st, ins]) => {
        setOverview(ov.data);
        setAgents(ag.data.agents || []);
        setStandards(st.data.standards || []);
        setInsights(ins.data);
      })
      .catch(() => toast.error(lang === "it" ? "Errore caricamento dati" : "Failed to load data"))
      .finally(() => setLoading(false));
  }, [lang]);

  const bandCfg = BAND_CONFIG[overview?.score_band] || BAND_CONFIG.warning;

  const radialData = useMemo(() => {
    if (!overview) return [];
    return [{ name: "Score", value: overview.final_score, fill: bandCfg.ring }];
  }, [overview, bandCfg]);

  const agentDistData = useMemo(() => {
    const bands = { excellent: 0, strong: 0, warning: 0, critical: 0 };
    agents.forEach(a => { bands[a.score_band] = (bands[a.score_band] || 0) + 1; });
    return Object.entries(bands).filter(([, v]) => v > 0).map(([k, v]) => ({ name: k, value: v, fill: BAND_CONFIG[k]?.ring || "#64748b" }));
  }, [agents]);

  if (loading) return <SkeletonLoader type="cards" count={6} />;
  if (!overview) return null;

  const topAgents = [...agents].sort((a, b) => a.final_score - b.final_score).slice(0, 6);
  const topStandards = [...standards].sort((a, b) => a.final_score - b.final_score);

  return (
    <div className="space-y-6" data-testid="intelligence-center-page">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white font-['Space_Grotesk']" data-testid="ic-title">
          {t("ic_title")}
        </h1>
        <p className="text-slate-400 text-sm mt-1">{t("ic_subtitle")}</p>
      </div>

      {/* ── HEADLINE SCORE ─────────────────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Main Score Ring */}
        <Card className={`bg-slate-900/40 backdrop-blur-md ${bandCfg.border} border col-span-1 lg:col-span-1`} data-testid="ic-main-score">
          <CardContent className="p-6 flex flex-col items-center justify-center">
            <div className="relative w-40 h-40">
              <ResponsiveContainer width="100%" height="100%">
                <RadialBarChart cx="50%" cy="50%" innerRadius="70%" outerRadius="100%" startAngle={90} endAngle={-270} data={radialData} barSize={12}>
                  <RadialBar background={{ fill: "#1e293b" }} dataKey="value" cornerRadius={6} />
                </RadialBarChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className={`text-4xl font-bold font-['Space_Grotesk'] ${bandCfg.color}`} data-testid="ic-score-value">
                  {overview.final_score}
                </span>
                <span className="text-xs text-slate-500">/100</span>
              </div>
            </div>
            <Badge variant="outline" className={`mt-3 text-xs ${bandCfg.bg} ${bandCfg.color} ${bandCfg.border}`} data-testid="ic-score-band">
              {overview.score_band.toUpperCase()}
            </Badge>
            {overview.delta_score !== 0 && overview.delta_score != null && (
              <div className="flex items-center gap-1.5 mt-2">
                <TrendIcon dir={overview.trend_direction} />
                <span className={`text-xs ${overview.delta_score > 0 ? "text-emerald-400" : "text-red-400"}`}>
                  {overview.delta_score > 0 ? "+" : ""}{overview.delta_score} pts
                </span>
              </div>
            )}
            <p className="text-[10px] text-slate-600 mt-2 font-mono">
              {lang === "it" ? "Ultimo calcolo" : "Last calculated"}: {new Date(overview.last_calculated_at).toLocaleTimeString()}
            </p>
          </CardContent>
        </Card>

        {/* Score Breakdown */}
        <Card className="bg-slate-900/40 backdrop-blur-md border-slate-800 col-span-1 lg:col-span-2" data-testid="ic-breakdown">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-semibold text-white font-['Space_Grotesk'] flex items-center gap-2">
              <Shield className="w-4 h-4 text-blue-400" />
              {lang === "it" ? "Composizione Score" : "Score Composition"}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <MiniKPI label={lang === "it" ? "Media Agenti" : "Agent Avg"} value={`${overview.agent_avg_score}%`} color="text-blue-400" />
              <MiniKPI label={lang === "it" ? "Media Standard" : "Standard Avg"} value={`${overview.standard_avg_score}%`} color="text-violet-400" />
              <MiniKPI label={lang === "it" ? "Conflitti aperti" : "Open Conflicts"} value={overview.unresolved_conflicts} color={overview.unresolved_conflicts > 0 ? "text-red-400" : "text-emerald-400"} />
              <MiniKPI label={lang === "it" ? "Standard monitorati" : "Standards Monitored"} value={overview.total_standards} color="text-slate-300" />
            </div>

            {/* Explanation */}
            <div className="p-3 rounded-md bg-slate-800/40 border border-slate-700/50">
              <div className="flex items-start gap-2">
                <Info className="w-4 h-4 text-slate-500 mt-0.5 shrink-0" />
                <div>
                  <p className="text-xs text-slate-300">{overview.explanation?.explanation_summary}</p>
                  <p className="text-[10px] text-slate-600 mt-1 font-mono">{overview.explanation?.methodology_note}</p>
                </div>
              </div>
            </div>

            {/* Score factors */}
            <div className="flex flex-wrap gap-2">
              <FactorPill icon={TrendingUp} label={lang === "it" ? "Positivo" : "Strongest +"} value={overview.explanation?.strongest_positive_factor} color="text-emerald-400" />
              <FactorPill icon={AlertTriangle} label={lang === "it" ? "Negativo" : "Strongest -"} value={overview.explanation?.strongest_negative_factor} color="text-red-400" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* ── AGENT SCORES + DISTRIBUTION ─────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Agent Distribution Pie */}
        <Card className="bg-slate-900/40 backdrop-blur-md border-slate-800" data-testid="ic-agent-distribution">
          <CardHeader className="pb-1">
            <CardTitle className="text-sm font-semibold text-white font-['Space_Grotesk']">
              {lang === "it" ? "Distribuzione Agenti" : "Agent Distribution"}
            </CardTitle>
          </CardHeader>
          <CardContent className="flex justify-center">
            <div className="w-40 h-40">
              <ResponsiveContainer>
                <PieChart>
                  <Pie data={agentDistData} dataKey="value" cx="50%" cy="50%" innerRadius={35} outerRadius={60} strokeWidth={0}>
                    {agentDistData.map((e, i) => <Cell key={i} fill={e.fill} />)}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
          <div className="px-4 pb-3 flex flex-wrap gap-2 justify-center">
            {agentDistData.map(d => (
              <span key={d.name} className="text-[10px] flex items-center gap-1">
                <span className="w-2 h-2 rounded-full" style={{ background: d.fill }} />
                <span className="text-slate-400">{d.name}: {d.value}</span>
              </span>
            ))}
          </div>
        </Card>

        {/* Agent Ranking */}
        <Card className="bg-slate-900/40 backdrop-blur-md border-slate-800 col-span-1 lg:col-span-2" data-testid="ic-agent-ranking">
          <CardHeader className="pb-1">
            <CardTitle className="text-sm font-semibold text-white font-['Space_Grotesk'] flex items-center gap-2">
              <Target className="w-4 h-4 text-blue-400" />
              {lang === "it" ? "Score Agenti (dal piu basso)" : "Agent Scores (lowest first)"}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-1.5">
            {topAgents.map(a => {
              const bc = BAND_CONFIG[a.score_band] || BAND_CONFIG.warning;
              return (
                <div key={a.agent_id} className="flex items-center gap-3 py-1.5 px-2 rounded-md hover:bg-slate-800/40 transition-colors" data-testid={`ic-agent-row-${a.agent_id?.slice(0, 8)}`}>
                  <div className="w-10 text-right">
                    <span className={`text-sm font-bold font-['Space_Grotesk'] ${bc.color}`}>{a.final_score}</span>
                  </div>
                  <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full rounded-full transition-all" style={{ width: `${a.final_score}%`, background: bc.ring }} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-white truncate">{a.agent_name}</p>
                    <p className="text-[10px] text-slate-600">{a.risk_level}</p>
                  </div>
                  <Badge variant="outline" className={`text-[10px] ${bc.bg} ${bc.color} ${bc.border}`}>{a.score_band}</Badge>
                  {a.delta_score != null && a.delta_score !== 0 && (
                    <div className="flex items-center gap-0.5">
                      <TrendIcon dir={a.trend_direction} />
                      <span className={`text-[10px] ${a.delta_score > 0 ? "text-emerald-400" : "text-red-400"}`}>{a.delta_score > 0 ? "+" : ""}{a.delta_score}</span>
                    </div>
                  )}
                </div>
              );
            })}
          </CardContent>
        </Card>
      </div>

      {/* ── STANDARD SCORES ───────────────────────────────────────── */}
      <Card className="bg-slate-900/40 backdrop-blur-md border-slate-800" data-testid="ic-standard-scores">
        <CardHeader className="pb-1">
          <CardTitle className="text-sm font-semibold text-white font-['Space_Grotesk'] flex items-center gap-2">
            <FileText className="w-4 h-4 text-violet-400" />
            {lang === "it" ? "Score per Standard Normativo" : "Score by Regulatory Standard"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {topStandards.map(s => {
              const bc = BAND_CONFIG[s.score_band] || BAND_CONFIG.warning;
              return (
                <div key={s.code} className={`p-3 rounded-md border ${bc.border} ${bc.bg}`} data-testid={`ic-std-${s.code}`}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-semibold text-white">{s.code}</span>
                    <span className={`text-lg font-bold font-['Space_Grotesk'] ${bc.color}`}>{s.final_score}</span>
                  </div>
                  <div className="h-1 bg-slate-800 rounded-full mb-1.5 overflow-hidden">
                    <div className="h-full rounded-full" style={{ width: `${s.final_score}%`, background: bc.ring }} />
                  </div>
                  <p className="text-[10px] text-slate-500 truncate">{s.standard_name}</p>
                  <p className="text-[10px] text-slate-600">{s.requirements_met}/{s.requirements_total} req. | {s.policies_count} policies</p>
                  {s.delta_score != null && s.delta_score !== 0 && (
                    <div className="flex items-center gap-1 mt-1">
                      <TrendIcon dir={s.trend_direction} />
                      <span className={`text-[10px] ${s.delta_score > 0 ? "text-emerald-400" : "text-red-400"}`}>{s.delta_score > 0 ? "+" : ""}{s.delta_score}</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* ── INSIGHTS + RISKS + REMEDIATIONS ───────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Insights / Alerts */}
        {insights?.insights?.length > 0 && (
          <Card className="bg-slate-900/40 backdrop-blur-md border-slate-800" data-testid="ic-insights">
            <CardHeader className="pb-1">
              <CardTitle className="text-sm font-semibold text-white font-['Space_Grotesk'] flex items-center gap-2">
                <Zap className="w-4 h-4 text-amber-400" />
                {lang === "it" ? "Insight Attivi" : "Active Insights"}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {insights.insights.map((ins, i) => (
                <div key={i} className="flex items-start gap-2 p-2 rounded-md bg-slate-800/30 border border-slate-700/30">
                  <Badge variant="outline" className={`text-[10px] mt-0.5 shrink-0 ${SEV_BADGE[ins.severity] || SEV_BADGE.info}`}>{ins.severity}</Badge>
                  <div className="min-w-0">
                    <p className="text-xs font-medium text-white">{ins.title}</p>
                    <p className="text-[10px] text-slate-500 truncate">{ins.detail}</p>
                    <p className="text-[10px] text-blue-400 mt-0.5 flex items-center gap-1">
                      <ArrowRight className="w-3 h-3" />{ins.action}
                    </p>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        )}

        {/* Priority Remediations */}
        <Card className="bg-slate-900/40 backdrop-blur-md border-slate-800" data-testid="ic-remediations">
          <Collapsible open={openSections.remediations} onOpenChange={o => setOpenSections(p => ({ ...p, remediations: o }))}>
            <CardHeader className="pb-1">
              <CollapsibleTrigger className="flex items-center justify-between w-full">
                <CardTitle className="text-sm font-semibold text-white font-['Space_Grotesk'] flex items-center gap-2">
                  <Lightbulb className="w-4 h-4 text-emerald-400" />
                  {lang === "it" ? "Remediation Prioritarie" : "Priority Remediations"}
                </CardTitle>
                {openSections.remediations ? <ChevronUp className="w-4 h-4 text-slate-500" /> : <ChevronDown className="w-4 h-4 text-slate-500" />}
              </CollapsibleTrigger>
            </CardHeader>
            <CollapsibleContent>
              <CardContent className="space-y-1.5">
                {overview.priority_remediations?.slice(0, 6).map((r, i) => (
                  <div key={i} className="flex items-start gap-2 py-1.5">
                    <span className="text-[10px] text-slate-600 font-mono w-4 shrink-0 mt-0.5">#{i + 1}</span>
                    <div className="min-w-0">
                      <p className="text-xs text-slate-300">{r.action}</p>
                      <p className="text-[10px] text-slate-600">{r.entity} ({r.entity_type})</p>
                    </div>
                    <div className="shrink-0">
                      <div className="w-8 h-1 bg-slate-800 rounded-full overflow-hidden">
                        <div className="h-full rounded-full bg-emerald-500" style={{ width: `${r.impact}%` }} />
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </CollapsibleContent>
          </Collapsible>
        </Card>
      </div>

      {/* ── TOP RISKS ──────────────────────────────────────────────── */}
      {overview.top_risks?.length > 0 && (
        <Card className="bg-slate-900/40 backdrop-blur-md border-slate-800" data-testid="ic-top-risks">
          <Collapsible open={openSections.risks} onOpenChange={o => setOpenSections(p => ({ ...p, risks: o }))}>
            <CardHeader className="pb-1">
              <CollapsibleTrigger className="flex items-center justify-between w-full">
                <CardTitle className="text-sm font-semibold text-white font-['Space_Grotesk'] flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-red-400" />
                  {lang === "it" ? "Rischi Principali" : "Top Risks"}
                </CardTitle>
                {openSections.risks ? <ChevronUp className="w-4 h-4 text-slate-500" /> : <ChevronDown className="w-4 h-4 text-slate-500" />}
              </CollapsibleTrigger>
            </CardHeader>
            <CollapsibleContent>
              <CardContent>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2">
                  {overview.top_risks.slice(0, 8).map((r, i) => (
                    <div key={i} className="p-2.5 rounded-md bg-slate-800/30 border border-slate-700/30">
                      <div className="flex items-center gap-1.5 mb-1">
                        <Lock className="w-3 h-3 text-red-400" />
                        <span className="text-[10px] font-medium text-white">{r.entity}</span>
                      </div>
                      <p className="text-[10px] text-slate-400">{r.detail}</p>
                      <Badge variant="outline" className={`text-[9px] mt-1 ${SEV_BADGE[r.type === "conflict" ? "critical" : "high"]}`}>{r.type}</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </CollapsibleContent>
          </Collapsible>
        </Card>
      )}

      {/* Missing Controls */}
      {overview.missing_controls?.length > 0 && (
        <Card className="bg-slate-900/40 backdrop-blur-md border-slate-800" data-testid="ic-missing-controls">
          <CardHeader className="pb-1">
            <CardTitle className="text-sm font-semibold text-white font-['Space_Grotesk'] flex items-center gap-2">
              <Shield className="w-4 h-4 text-amber-400" />
              {lang === "it" ? "Controlli Mancanti" : "Missing Controls"}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-1">
            {overview.missing_controls.slice(0, 6).map((mc, i) => (
              <div key={i} className="flex items-center gap-2 py-1">
                <AlertTriangle className="w-3 h-3 text-amber-500 shrink-0" />
                <p className="text-xs text-slate-400">{mc}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function MiniKPI({ label, value, color }) {
  return (
    <div className="text-center p-2 rounded-md bg-slate-800/30 border border-slate-700/30">
      <p className={`text-lg font-bold font-['Space_Grotesk'] ${color}`}>{value}</p>
      <p className="text-[10px] text-slate-500">{label}</p>
    </div>
  );
}

function FactorPill({ icon: Icon, label, value, color }) {
  if (!value) return null;
  return (
    <div className="flex items-start gap-2 p-2 rounded-md bg-slate-800/20 border border-slate-700/30 flex-1 min-w-[200px]">
      <Icon className={`w-3.5 h-3.5 ${color} shrink-0 mt-0.5`} />
      <div>
        <p className="text-[10px] text-slate-500">{label}</p>
        <p className="text-xs text-slate-300">{value}</p>
      </div>
    </div>
  );
}
