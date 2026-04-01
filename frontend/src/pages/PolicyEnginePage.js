import React, { useEffect, useState, useCallback } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { useAuth } from "@/contexts/AuthContext";
import {
  AlertTriangle, Play, CheckCircle, Lightbulb, Loader2,
  Shield, Zap, Copy, GitMerge, Search,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter,
} from "@/components/ui/dialog";
import { toast } from "sonner";
import axios from "axios";
import SkeletonLoader from "@/components/SkeletonLoader";
import EmptyState from "@/components/EmptyState";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const severityConfig = {
  critical: { color: "text-red-400", bg: "bg-red-950/30 text-red-400 border-red-900/50" },
  high:     { color: "text-orange-400", bg: "bg-orange-950/30 text-orange-400 border-orange-900/50" },
  medium:   { color: "text-amber-400", bg: "bg-amber-950/30 text-amber-400 border-amber-900/50" },
  low:      { color: "text-slate-400", bg: "bg-slate-800/50 text-slate-400 border-slate-700/50" },
};

const typeConfig = {
  action_conflict: { icon: Zap, label: "Action Conflict", labelIt: "Conflitto Azioni", bg: "bg-violet-950/30 text-violet-400 border-violet-900/50" },
  gap:             { icon: Search, label: "Gap", labelIt: "Gap", bg: "bg-red-950/40 text-red-300 border-red-900/50" },
  overlap:         { icon: Copy, label: "Overlap", labelIt: "Sovrapposizione", bg: "bg-blue-950/30 text-blue-400 border-blue-900/50" },
  redundancy:      { icon: GitMerge, label: "Redundancy", labelIt: "Ridondanza", bg: "bg-slate-800/50 text-slate-400 border-slate-700/50" },
};

const RESOLVE_ROLES = ["admin", "dpo"];

export default function PolicyEnginePage() {
  const { t, lang } = useLanguage();
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [firstLoad, setFirstLoad] = useState(true);
  const [filterType, setFilterType] = useState("all");
  const [filterSev, setFilterSev] = useState("all");
  const [showResolved, setShowResolved] = useState(false);
  const [resolvedIds, setResolvedIds] = useState(new Set());
  const [resolveTarget, setResolveTarget] = useState(null);
  const [resolveNote, setResolveNote] = useState("");
  const [resolving, setResolving] = useState(false);

  const canResolve = user && RESOLVE_ROLES.includes(user.role);

  const runScan = useCallback(async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/policy-engine/conflicts`);
      setData(res.data);
      // Load resolved conflicts
      const resolvedDocs = await axios.get(`${API}/policy-engine/scan-history`).catch(() => null);
      // We track resolved IDs client-side from the resolved_conflicts collection
    } catch (err) {
      toast.error(lang === "it" ? "Errore durante lo scan" : "Scan failed");
    } finally {
      setLoading(false);
      setFirstLoad(false);
    }
  }, [lang]);

  useEffect(() => { runScan(); }, [runScan]);

  const handleResolve = async () => {
    if (!resolveTarget) return;
    setResolving(true);
    try {
      await axios.post(`${API}/policy-engine/conflicts/${resolveTarget.id}/resolve`, {
        resolved_by: user?.username || "admin",
        resolution_note: resolveNote,
      });
      setResolvedIds(prev => new Set([...prev, resolveTarget.id]));
      toast.success(lang === "it" ? "Conflitto risolto" : "Conflict resolved");
      setResolveTarget(null);
      setResolveNote("");
    } catch {
      toast.error(lang === "it" ? "Errore" : "Failed to resolve");
    } finally {
      setResolving(false);
    }
  };

  const conflicts = data?.conflicts || [];
  const filtered = conflicts.filter(c => {
    if (filterType !== "all" && c.conflict_type !== filterType) return false;
    if (filterSev !== "all" && c.severity !== filterSev) return false;
    const isResolved = resolvedIds.has(c.id);
    if (!showResolved && isResolved) return false;
    return true;
  });

  const summary = data?.summary || {};

  if (firstLoad && loading) return <SkeletonLoader type="cards" count={4} />;

  return (
    <div className="space-y-6" data-testid="policy-engine-page">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white font-['Space_Grotesk']" data-testid="policy-engine-title">
            {t("pe_title")}
          </h1>
          <p className="text-slate-400 text-sm mt-1">{t("pe_subtitle")}</p>
        </div>
        <div className="flex items-center gap-3">
          {summary.scan_timestamp && (
            <span className="text-xs text-slate-500">
              {lang === "it" ? "Ultimo scan:" : "Last scan:"}{" "}
              {new Date(summary.scan_timestamp).toLocaleTimeString()}
            </span>
          )}
          <Button
            onClick={runScan}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white"
            data-testid="pe-run-scan-btn"
          >
            {loading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Play className="w-4 h-4 mr-2" />}
            {t("pe_run_scan")}
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3" data-testid="pe-summary-cards">
        <SummaryCard
          label={t("pe_total_conflicts")}
          value={summary.total || 0}
          icon={AlertTriangle}
          color="text-white" bg="bg-slate-800/60"
        />
        <SummaryCard
          label="Critical"
          value={summary.by_severity?.critical || 0}
          icon={AlertTriangle}
          color="text-red-400" bg="bg-red-500/10"
        />
        <SummaryCard
          label="High"
          value={summary.by_severity?.high || 0}
          icon={Shield}
          color="text-orange-400" bg="bg-orange-500/10"
        />
        <SummaryCard
          label={t("pe_agents_impacted")}
          value={summary.agents_impacted || 0}
          icon={Zap}
          color="text-violet-400" bg="bg-violet-500/10"
        />
      </div>

      {/* Filters */}
      <div className="flex flex-wrap items-center gap-3" data-testid="pe-filters">
        <select
          value={filterType} onChange={e => setFilterType(e.target.value)}
          className="bg-slate-800 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-white focus:border-blue-500 focus:outline-none"
          data-testid="pe-filter-type"
        >
          <option value="all">{lang === "it" ? "Tutti i tipi" : "All Types"}</option>
          {Object.entries(typeConfig).map(([k, v]) => (
            <option key={k} value={k}>{lang === "it" ? v.labelIt : v.label}</option>
          ))}
        </select>
        <select
          value={filterSev} onChange={e => setFilterSev(e.target.value)}
          className="bg-slate-800 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-white focus:border-blue-500 focus:outline-none"
          data-testid="pe-filter-severity"
        >
          <option value="all">{lang === "it" ? "Tutte le severita" : "All Severities"}</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
        <label className="flex items-center gap-2 text-sm text-slate-400 cursor-pointer">
          <input
            type="checkbox" checked={showResolved}
            onChange={e => setShowResolved(e.target.checked)}
            className="rounded border-slate-600"
            data-testid="pe-show-resolved"
          />
          {lang === "it" ? "Mostra risolti" : "Show Resolved"}
        </label>
      </div>

      {/* Loading overlay */}
      {loading && !firstLoad && (
        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm">
          <CardContent className="p-8 flex flex-col items-center gap-3">
            <Loader2 className="w-8 h-8 text-blue-400 animate-spin" />
            <span className="text-sm text-slate-400">{t("pe_scanning")}</span>
          </CardContent>
        </Card>
      )}

      {/* Conflicts list or empty state */}
      {!loading && filtered.length === 0 && (
        <EmptyState
          icon="CheckCircle"
          title={t("pe_no_conflicts")}
          subtitle={t("pe_no_conflicts_sub")}
        />
      )}

      {!loading && filtered.length > 0 && (
        <div className="space-y-3" data-testid="pe-conflicts-list">
          {filtered.map(conflict => {
            const sev = severityConfig[conflict.severity] || severityConfig.medium;
            const typ = typeConfig[conflict.conflict_type] || typeConfig.gap;
            const TIcon = typ.icon;
            const isResolved = resolvedIds.has(conflict.id);
            return (
              <Card
                key={conflict.id}
                className={`bg-slate-900/50 border-slate-800 backdrop-blur-sm ${isResolved ? "opacity-60" : ""}`}
                data-testid={`pe-conflict-card-${conflict.conflict_type}`}
              >
                <CardContent className="p-4">
                  <div className="flex flex-col gap-3">
                    {/* Header: badges + title */}
                    <div className="flex flex-wrap items-center gap-2">
                      <Badge variant="outline" className={`text-[11px] ${sev.bg}`}>
                        {conflict.severity.toUpperCase()}
                      </Badge>
                      <Badge variant="outline" className={`text-[11px] ${typ.bg}`}>
                        <TIcon className="w-3 h-3 mr-1" />
                        {lang === "it" ? typ.labelIt : typ.label}
                      </Badge>
                      {isResolved && (
                        <Badge variant="outline" className="text-[11px] bg-emerald-950/30 text-emerald-400 border-emerald-900/50">
                          <CheckCircle className="w-3 h-3 mr-1" />
                          {lang === "it" ? "Risolto" : "Resolved"}
                        </Badge>
                      )}
                      {conflict.regulation?.map(r => (
                        <Badge key={r} variant="outline" className="text-[10px] bg-slate-800/50 text-slate-300 border-slate-700">
                          {r}
                        </Badge>
                      ))}
                    </div>

                    {/* Title + description */}
                    <div>
                      <h3 className="text-sm font-semibold text-white">{conflict.title}</h3>
                      <p className="text-xs text-slate-400 mt-1 line-clamp-2">{conflict.description}</p>
                    </div>

                    {/* Pills: policies + agents */}
                    <div className="flex flex-wrap gap-1.5">
                      {conflict.policy_names?.map(pn => (
                        <span key={pn} className="text-[10px] px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-900/30">
                          {pn}
                        </span>
                      ))}
                      {conflict.agent_names?.filter(Boolean).map(an => (
                        <span key={an} className="text-[10px] px-2 py-0.5 rounded-full bg-violet-500/10 text-violet-400 border border-violet-900/30">
                          {an}
                        </span>
                      ))}
                    </div>

                    {/* Recommendation */}
                    {conflict.recommendation && (
                      <div className="flex gap-2 p-2.5 rounded-md bg-slate-800/40 border border-slate-700/30">
                        <Lightbulb className="w-4 h-4 text-amber-400 mt-0.5 shrink-0" />
                        <p className="text-xs text-slate-300">{conflict.recommendation}</p>
                      </div>
                    )}

                    {/* Resolve button */}
                    {canResolve && !isResolved && (
                      <div className="flex justify-end">
                        <Button
                          size="sm" variant="outline"
                          className="border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white text-xs"
                          onClick={() => { setResolveTarget(conflict); setResolveNote(""); }}
                          data-testid={`pe-resolve-btn-${conflict.id.slice(0, 8)}`}
                        >
                          <CheckCircle className="w-3.5 h-3.5 mr-1.5" />
                          {t("pe_mark_resolved")}
                        </Button>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}

      {/* Resolve Dialog */}
      <Dialog open={!!resolveTarget} onOpenChange={open => { if (!open) setResolveTarget(null); }}>
        <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-md" data-testid="pe-resolve-dialog">
          <DialogHeader>
            <DialogTitle className="text-white">{t("pe_resolve_title")}</DialogTitle>
            <DialogDescription className="text-slate-400">
              {resolveTarget?.title}
            </DialogDescription>
          </DialogHeader>
          <div className="py-2">
            <label className="text-xs text-slate-400 mb-1 block">{t("pe_resolution_note")}</label>
            <textarea
              value={resolveNote}
              onChange={e => setResolveNote(e.target.value)}
              placeholder={lang === "it" ? "Descrivi la risoluzione applicata..." : "Describe the resolution applied..."}
              rows={3}
              className="w-full bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-sm text-white placeholder:text-slate-600 focus:border-blue-500 focus:outline-none resize-none"
              data-testid="pe-resolve-note"
            />
          </div>
          <DialogFooter>
            <Button
              onClick={handleResolve}
              disabled={resolving}
              className="bg-emerald-600 hover:bg-emerald-700 text-white"
              data-testid="pe-resolve-confirm-btn"
            >
              {resolving ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <CheckCircle className="w-4 h-4 mr-2" />}
              {t("pe_confirm_resolve")}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}

function SummaryCard({ label, value, icon: Icon, color, bg }) {
  return (
    <Card className={`${bg} border-slate-800 backdrop-blur-sm`}>
      <CardContent className="p-4 flex items-center gap-3">
        <Icon className={`w-5 h-5 ${color}`} />
        <div>
          <p className={`text-xl font-bold font-['Space_Grotesk'] ${color}`}>{value}</p>
          <p className="text-[11px] text-slate-500">{label}</p>
        </div>
      </CardContent>
    </Card>
  );
}
