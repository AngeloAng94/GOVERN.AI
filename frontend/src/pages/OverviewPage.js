import React, { useEffect, useState, useMemo } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { Bot, FileText, Activity, ShieldCheck, AlertTriangle, ArrowUpRight, PieChart as PieChartIcon, BarChart3, Brain } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import axios from "axios";
import SkeletonLoader from "@/components/SkeletonLoader";
import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from "recharts";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const outcomeColors = {
  allowed: "bg-emerald-950/30 text-emerald-400 border-emerald-900/50",
  blocked: "bg-red-950/30 text-red-400 border-red-900/50",
  logged: "bg-blue-950/30 text-blue-400 border-blue-900/50",
  escalated: "bg-amber-950/30 text-amber-400 border-amber-900/50",
};

const riskColors = {
  low: "text-emerald-400",
  medium: "text-amber-400",
  high: "text-orange-400",
  critical: "text-red-400",
};

// Chart colors
const RISK_CHART_COLORS = {
  critical: "#ef4444",
  high: "#f97316",
  medium: "#eab308",
  low: "#22c55e",
};

const AUDIT_CHART_COLORS = {
  allowed: "#22c55e",
  blocked: "#ef4444",
  escalated: "#f97316",
};

// Custom tooltip for charts
const CustomTooltip = ({ active, payload, label, suffix = "" }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-800 border border-slate-700 rounded-sm px-3 py-2 shadow-lg">
        <p className="text-slate-300 text-sm">
          {payload[0].name || label}: <span className="font-semibold">{payload[0].value}{suffix}</span>
        </p>
      </div>
    );
  }
  return null;
};

// Get bar color based on progress value
const getBarColor = (value) => {
  if (value >= 80) return "#22c55e";
  if (value >= 50) return "#eab308";
  return "#ef4444";
};

export default function OverviewPage() {
  const { t } = useLanguage();
  const [stats, setStats] = useState(null);
  const [compliance, setCompliance] = useState([]);
  const [conflictCount, setConflictCount] = useState(0);
  const [conflictTotal, setConflictTotal] = useState(0);
  const [conflictResolved, setConflictResolved] = useState(0);
  const [govScore, setGovScore] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      axios.get(`${API}/dashboard/stats`),
      axios.get(`${API}/compliance`),
      axios.get(`${API}/policy-engine/conflicts`).catch(() => ({ data: { summary: { by_severity: {} }, conflicts: [] } })),
      axios.get(`${API}/score/overview`).catch(() => ({ data: null })),
    ])
      .then(([statsRes, complianceRes, conflictsRes, scoreRes]) => {
        setStats(statsRes.data);
        setCompliance(complianceRes.data);
        const conflictsData = conflictsRes.data;
        setConflictCount(conflictsData?.summary?.by_severity?.critical || 0);
        setConflictTotal(conflictsData?.summary?.total || 0);
        if (scoreRes.data) setGovScore(scoreRes.data);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  // Prepare chart data
  const riskChartData = useMemo(() => {
    if (!stats?.risk_distribution) return [];
    return Object.entries(stats.risk_distribution).map(([name, value]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      value,
      color: RISK_CHART_COLORS[name] || "#64748b"
    }));
  }, [stats]);

  const auditChartData = useMemo(() => {
    if (!stats?.audit) return [];
    const blocked = stats.audit.blocked || 0;
    const escalated = stats.audit.escalated || 0;
    const allowed = Math.max(0, (stats.audit.total || 0) - blocked - escalated);
    return [
      { name: "Allowed", value: allowed, color: AUDIT_CHART_COLORS.allowed || "#22c55e" },
      { name: "Blocked", value: blocked, color: AUDIT_CHART_COLORS.blocked || "#ef4444" },
      { name: "Escalated", value: escalated, color: AUDIT_CHART_COLORS.escalated || "#f97316" },
    ].filter(item => item.value > 0);
  }, [stats]);

  const complianceChartData = useMemo(() => {
    return compliance.map(std => ({
      name: std.code,
      progress: std.progress,
      fullName: std.name
    }));
  }, [compliance]);

  if (loading) {
    return (
      <div className="space-y-6" data-testid="overview-loading">
        <div>
          <h1 className="font-['Space_Grotesk'] text-2xl font-bold tracking-tight text-white">{t("overview_title")}</h1>
          <p className="text-sm text-slate-500 mt-1 font-mono uppercase tracking-widest">Control Plane Status</p>
        </div>
        <SkeletonLoader type="stat" />
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 animate-pulse">
          <div className="h-80 bg-slate-800 rounded-xl border border-slate-700/50" />
          <div className="h-80 bg-slate-800 rounded-xl border border-slate-700/50" />
        </div>
      </div>
    );
  }

  if (!stats) return null;

  const kpis = [
    { label: t("ic_kpi_governance"), value: govScore ? `${govScore.final_score}%` : "—", sub: govScore ? govScore.score_band.toUpperCase() : "", icon: Brain, color: govScore?.score_band === "critical" ? "text-red-400" : govScore?.score_band === "warning" ? "text-amber-400" : "text-emerald-400", bg: govScore?.score_band === "critical" ? "bg-red-500/10" : govScore?.score_band === "warning" ? "bg-amber-500/10" : "bg-emerald-500/10", link: "/dashboard/intelligence" },
    { label: t("total_agents"), value: stats.agents.total, sub: `${stats.agents.active} ${t("active_agents")}`, icon: Bot, color: "text-blue-400", bg: "bg-blue-500/10" },
    { label: t("total_policies"), value: stats.policies.total, sub: `${stats.policies.active} ${t("active_policies")}`, icon: FileText, color: "text-amber-400", bg: "bg-amber-500/10" },
    { label: t("audit_events"), value: stats.audit.total, sub: `${stats.audit.blocked} ${t("blocked_events")}`, icon: Activity, color: "text-emerald-400", bg: "bg-emerald-500/10" },
    { label: t("compliance_score"), value: `${stats.compliance_avg}%`, sub: `${compliance.length} standards`, icon: ShieldCheck, color: "text-violet-400", bg: "bg-violet-500/10" },
    { label: t("pe_conflicts_kpi"), value: conflictCount, sub: `${conflictTotal} ${conflictTotal === 1 ? "total" : "totali"}`, icon: AlertTriangle, color: conflictCount > 0 ? "text-red-400" : "text-emerald-400", bg: conflictCount > 0 ? "bg-red-500/10" : "bg-emerald-500/10" },
  ];

  return (
    <div className="space-y-6" data-testid="overview-page">
      <div>
        <h1 className="font-['Space_Grotesk'] text-2xl font-bold tracking-tight text-white">{t("overview_title")}</h1>
        <p className="text-sm text-slate-500 mt-1 font-mono uppercase tracking-widest">Control Plane Status</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4" data-testid="kpi-grid">
        {kpis.map((kpi, i) => (
          <Card key={i} className="bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm hover:border-slate-700 transition-colors duration-300" data-testid={`kpi-${i}`}>
            <CardContent className="p-5">
              <div className="flex items-center justify-between mb-3">
                <div className={`w-9 h-9 rounded-sm flex items-center justify-center ${kpi.bg}`}>
                  <kpi.icon className={`w-4 h-4 ${kpi.color}`} />
                </div>
                <ArrowUpRight className="w-4 h-4 text-slate-600" />
              </div>
              <div className="font-['Space_Grotesk'] text-3xl font-bold text-white">{kpi.value}</div>
              <div className="text-sm text-slate-400 mt-1">{kpi.label}</div>
              <div className="text-xs text-slate-600 font-mono mt-0.5">{kpi.sub}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Charts Row 1: Risk Distribution + Audit Outcomes */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4" data-testid="charts-row-1">
        {/* Risk Distribution PieChart */}
        <Card className="bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm" data-testid="chart-risk-distribution">
          <CardHeader className="pb-2">
            <CardTitle className="font-['Space_Grotesk'] text-base font-semibold text-white flex items-center gap-2">
              <PieChartIcon className="w-4 h-4 text-amber-400" />
              {t("chart_risk_title")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div style={{ height: 280 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={riskChartData}
                    cx="50%"
                    cy="45%"
                    innerRadius={50}
                    outerRadius={90}
                    paddingAngle={2}
                    dataKey="value"
                    nameKey="name"
                    isAnimationActive={true}
                  >
                    {riskChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip content={<CustomTooltip suffix=" agents" />} />
                  <Legend
                    verticalAlign="bottom"
                    height={36}
                    formatter={(value) => <span className="text-slate-400 text-xs">{value}</span>}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Audit Outcomes BarChart */}
        <Card className="bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm" data-testid="chart-audit-outcomes">
          <CardHeader className="pb-2">
            <CardTitle className="font-['Space_Grotesk'] text-base font-semibold text-white flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-emerald-400" />
              {t("chart_audit_title")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div style={{ height: 280 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={auditChartData} margin={{ top: 20, right: 20, left: 0, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                  <XAxis
                    dataKey="name"
                    tick={{ fill: '#94a3b8', fontSize: 12 }}
                    axisLine={false}
                    tickLine={false}
                  />
                  <YAxis
                    tick={{ fill: '#94a3b8', fontSize: 12 }}
                    axisLine={false}
                    tickLine={false}
                    allowDecimals={false}
                  />
                  <Tooltip content={<CustomTooltip suffix=" events" />} />
                  <Bar dataKey="value" radius={[4, 4, 0, 0]} isAnimationActive={true}>
                    {auditChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Chart Row 2: Compliance Progress */}
      <Card className="bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm" data-testid="chart-compliance-progress">
        <CardHeader className="pb-2">
          <CardTitle className="font-['Space_Grotesk'] text-base font-semibold text-white flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-violet-400" />
            {t("chart_compliance_title")}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div style={{ height: 320 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={complianceChartData}
                layout="vertical"
                margin={{ top: 10, right: 60, left: 10, bottom: 10 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
                <XAxis
                  type="number"
                  domain={[0, 100]}
                  tick={{ fill: '#94a3b8', fontSize: 11 }}
                  axisLine={false}
                  tickLine={false}
                  tickFormatter={(value) => `${value}%`}
                />
                <YAxis
                  type="category"
                  dataKey="name"
                  tick={{ fill: '#94a3b8', fontSize: 11 }}
                  axisLine={false}
                  tickLine={false}
                  width={80}
                />
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const data = payload[0].payload;
                      return (
                        <div className="bg-slate-800 border border-slate-700 rounded-sm px-3 py-2 shadow-lg">
                          <p className="text-slate-200 text-sm font-semibold">{data.fullName}</p>
                          <p className="text-slate-400 text-xs mt-1">Progress: <span className="text-white">{data.progress}%</span></p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Bar
                  dataKey="progress"
                  radius={[0, 4, 4, 0]}
                  isAnimationActive={true}
                  label={{
                    position: 'right',
                    fill: '#94a3b8',
                    fontSize: 11,
                    formatter: (value) => `${value}%`
                  }}
                >
                  {complianceChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={getBarColor(entry.progress)} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Recent Activity */}
        <Card className="lg:col-span-2 bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm" data-testid="recent-activity">
          <CardHeader className="pb-3">
            <CardTitle className="font-['Space_Grotesk'] text-base font-semibold text-white flex items-center gap-2">
              <Activity className="w-4 h-4 text-blue-400" />
              {t("recent_activity")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {stats.recent_audit.slice(0, 8).map((log, i) => (
                <div key={i} className="flex items-center justify-between py-2 border-b border-slate-800/60 last:border-0">
                  <div className="flex items-center gap-3 min-w-0">
                    <div className={`w-1.5 h-1.5 rounded-full ${
                      log.outcome === "blocked" ? "bg-red-400" :
                      log.outcome === "escalated" ? "bg-amber-400" : "bg-emerald-400"
                    }`} />
                    <div className="min-w-0">
                      <p className="text-sm text-slate-300 truncate">{log.action}</p>
                      <p className="text-xs text-slate-600 font-mono truncate">{log.agent_name} &middot; {log.resource}</p>
                    </div>
                  </div>
                  <Badge className={`${outcomeColors[log.outcome]} border text-[10px] shrink-0`}>
                    {log.outcome}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Risk Distribution (existing) */}
        <Card className="bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm" data-testid="risk-distribution">
          <CardHeader className="pb-3">
            <CardTitle className="font-['Space_Grotesk'] text-base font-semibold text-white flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              {t("risk_distribution")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Object.entries(stats.risk_distribution).map(([level, count]) => (
                <div key={level} className="space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className={`text-sm font-medium capitalize ${riskColors[level] || "text-slate-400"}`}>{level}</span>
                    <span className="text-sm text-slate-500 font-mono">{count}</span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-700 ${
                        level === "critical" ? "bg-red-500" :
                        level === "high" ? "bg-orange-500" :
                        level === "medium" ? "bg-amber-500" : "bg-emerald-500"
                      }`}
                      style={{ width: `${(count / stats.agents.total) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
