import React, { useEffect, useState } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { Bot, FileText, Activity, ShieldCheck, AlertTriangle, ArrowUpRight } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import axios from "axios";

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

export default function OverviewPage() {
  const { t } = useLanguage();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API}/dashboard/stats`)
      .then(res => setStats(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64" data-testid="overview-loading">
        <div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!stats) return null;

  const kpis = [
    { label: t("total_agents"), value: stats.agents.total, sub: `${stats.agents.active} ${t("active_agents")}`, icon: Bot, color: "text-blue-400", bg: "bg-blue-500/10" },
    { label: t("total_policies"), value: stats.policies.total, sub: `${stats.policies.active} ${t("active_policies")}`, icon: FileText, color: "text-amber-400", bg: "bg-amber-500/10" },
    { label: t("audit_events"), value: stats.audit.total, sub: `${stats.audit.blocked} ${t("blocked_events")}`, icon: Activity, color: "text-emerald-400", bg: "bg-emerald-500/10" },
    { label: t("compliance_score"), value: `${stats.compliance_avg}%`, sub: "6 standards", icon: ShieldCheck, color: "text-violet-400", bg: "bg-violet-500/10" },
  ];

  return (
    <div className="space-y-6" data-testid="overview-page">
      <div>
        <h1 className="font-['Space_Grotesk'] text-2xl font-bold tracking-tight text-white">{t("overview_title")}</h1>
        <p className="text-sm text-slate-500 mt-1 font-mono uppercase tracking-widest">Control Plane Status</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" data-testid="kpi-grid">
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
              {stats.recent_audit.map((log, i) => (
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

        {/* Risk Distribution */}
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
