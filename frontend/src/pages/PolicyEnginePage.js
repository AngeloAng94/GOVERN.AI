import React, { useEffect, useState, useCallback } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { useAuth } from "@/contexts/AuthContext";
import {
  AlertTriangle, Play, CheckCircle, Lightbulb, Loader2,
  Shield, Zap, Copy, GitMerge, Search, ChevronDown, ChevronUp,
  Info, Eye, User,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter,
} from "@/components/ui/dialog";
import {
  Sheet, SheetContent, SheetHeader, SheetTitle,
} from "@/components/ui/sheet";
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
  action_conflict: { icon: Zap, label: "Action Conflict", labelIt: "Conflitto Azioni", badgeBg: "bg-red-950/40 text-red-300 border-red-900/50" },
  gap:             { icon: Search, label: "Gap", labelIt: "Gap", badgeBg: "bg-orange-950/40 text-orange-300 border-orange-900/50" },
  overlap:         { icon: Copy, label: "Overlap", labelIt: "Sovrapposizione", badgeBg: "bg-amber-950/40 text-amber-300 border-amber-900/50" },
  redundancy:      { icon: GitMerge, label: "Redundancy", labelIt: "Ridondanza", badgeBg: "bg-slate-800/50 text-slate-400 border-slate-700/50" },
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
  const [resolvedMap, setResolvedMap] = useState({});
  const [resolveTarget, setResolveTarget] = useState(null);
  const [resolveNote, setResolveNote] = useState("");
  const [resolving, setResolving] = useState(false);
  const [detailConflict, setDetailConflict] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [expanded, setExpanded] = useState({});

  const canResolve = user && RESOLVE_ROLES.includes(user.role);

  const runScan = useCallback(async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/policy-engine/conflicts`);
      setData(res.data);
    } catch (err) {
      toast.error(lang === "it" ? "Errore durante lo scan" : "Scan failed");
    } finally {
      setLoading(false);
      setFirstLoad(false);
    }
  }, [lang]);

  useEffect(() => { runScan(); }, [runScan]);

  const toggleExpand = (id, section) => {
    setExpanded(prev => ({ ...prev, [`${id}_${section}`]: !prev[`${id}_${section}`] }));
  };

  const openDetail = async (conflict) => {
    setDetailConflict(conflict);
    setDetailLoading(true);
    try {
      const res = await axios.get(`${API}/policy-engine/conflicts/${conflict.id}/guidance`);
      setDetailConflict(res.data);
    } catch {
      setDetailConflict({ ...conflict, resolved: resolvedMap[conflict.id]?.resolved || false });
    } finally {
      setDetailLoading(false);
    }
  };

  const handleResolve = async () => {
    if (!resolveTarget || resolveNote.length < 10) return;
    setResolving(true);
    try {
      await axios.post(`${API}/policy-engine/conflicts/${resolveTarget.id}/resolve`, {
        resolved_by: user?.username || "admin",
        resolution_notes: resolveNote,
      });
      setResolvedMap(prev => ({ ...prev, [resolveTarget.id]: { resolved: true, resolved_by: user?.username, resolution_notes: resolveNote } }));
      toast.success(lang === "it" ? "Conflitto risolto e registrato nell'audit trail" : "Conflict resolved and logged to audit trail");
      setResolveTarget(null);
      setResolveNote("");
    } catch (err) {
      const msg = err?.response?.status === 422
        ? (lang === "it" ? "Le note devono avere almeno 10 caratteri" : "Notes must be at least 10 characters")
        : (lang === "it" ? "Errore" : "Failed to resolve");
      toast.error(msg);
    } finally {
      setResolving(false);
    }
  };

  const conflicts = data?.conflicts || [];
  const resolvedCount = Object.values(resolvedMap).filter(v => v.resolved).length;
  const filtered = conflicts.filter(c => {
    if (filterType !== "all" && c.conflict_type !== filterType) return false;
    if (filterSev !== "all" && c.severity !== filterSev) return false;
    const isResolved = resolvedMap[c.id]?.resolved;
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
        <SummaryCard label={t("pe_total_conflicts")} value={summary.total || 0} icon={AlertTriangle} color="text-white" bg="bg-slate-800/60" />
        <SummaryCard label="Critical" value={summary.by_severity?.critical || 0} icon={AlertTriangle} color="text-red-400" bg="bg-red-500/10" />
        <SummaryCard label="High" value={summary.by_severity?.high || 0} icon={Shield} color="text-orange-400" bg="bg-orange-500/10" />
        <SummaryCard label={t("pe_agents_impacted")} value={summary.agents_impacted || 0} icon={Zap} color="text-violet-400" bg="bg-violet-500/10" />
      </div>

      {/* Filters */}
      <div className="flex flex-wrap items-center gap-3" data-testid="pe-filters">
        <select value={filterType} onChange={e => setFilterType(e.target.value)} className="bg-slate-800 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-white focus:border-blue-500 focus:outline-none" data-testid="pe-filter-type">
          <option value="all">{lang === "it" ? "Tutti i tipi" : "All Types"}</option>
          {Object.entries(typeConfig).map(([k, v]) => (
            <option key={k} value={k}>{lang === "it" ? v.labelIt : v.label}</option>
          ))}
        </select>
        <select value={filterSev} onChange={e => setFilterSev(e.target.value)} className="bg-slate-800 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-white focus:border-blue-500 focus:outline-none" data-testid="pe-filter-severity">
          <option value="all">{lang === "it" ? "Tutte le severita" : "All Severities"}</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
        <label className="flex items-center gap-2 text-sm text-slate-400 cursor-pointer">
          <input type="checkbox" checked={showResolved} onChange={e => setShowResolved(e.target.checked)} className="rounded border-slate-600" data-testid="pe-show-resolved" />
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

      {/* Empty state */}
      {!loading && filtered.length === 0 && (
        <EmptyState icon="CheckCircle" title={t("pe_no_conflicts")} subtitle={t("pe_no_conflicts_sub")} />
      )}

      {/* Conflicts list */}
      {!loading && filtered.length > 0 && (
        <div className="space-y-3" data-testid="pe-conflicts-list">
          {filtered.map(conflict => {
            const sev = severityConfig[conflict.severity] || severityConfig.medium;
            const typ = typeConfig[conflict.conflict_type] || typeConfig.gap;
            const TIcon = typ.icon;
            const isResolved = resolvedMap[conflict.id]?.resolved;
            const impactOpen = expanded[`${conflict.id}_impact`];
            const guidanceOpen = expanded[`${conflict.id}_guidance`];
            return (
              <Card
                key={conflict.id}
                className={`bg-slate-900/50 border-slate-800 backdrop-blur-sm ${isResolved ? "opacity-60" : ""}`}
                data-testid={`pe-conflict-card-${conflict.conflict_type}`}
              >
                <CardContent className="p-4">
                  <div className="flex flex-col gap-3">
                    {/* Badges row */}
                    <div className="flex flex-wrap items-center gap-2">
                      <Badge variant="outline" className={`text-[11px] ${sev.bg}`}>{conflict.severity.toUpperCase()}</Badge>
                      <Badge variant="outline" className={`text-[11px] ${typ.badgeBg}`}>
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
                        <Badge key={r} variant="outline" className="text-[10px] bg-slate-800/50 text-slate-300 border-slate-700">{r}</Badge>
                      ))}
                    </div>

                    {/* Title + description */}
                    <div>
                      <h3 className="text-sm font-semibold text-white">{conflict.title}</h3>
                      <p className="text-xs text-slate-400 mt-1 line-clamp-2">{conflict.description}</p>
                    </div>

                    {/* Policy/Agent pills */}
                    <div className="flex flex-wrap gap-1.5">
                      {conflict.policy_names?.map(pn => (
                        <span key={pn} className="text-[10px] px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-900/30">{pn}</span>
                      ))}
                      {conflict.agent_names?.filter(Boolean).map(an => (
                        <span key={an} className="text-[10px] px-2 py-0.5 rounded-full bg-violet-500/10 text-violet-400 border border-violet-900/30">{an}</span>
                      ))}
                    </div>

                    {/* Collapsible: Impact */}
                    {conflict.impact_description && (
                      <div>
                        <button
                          onClick={() => toggleExpand(conflict.id, "impact")}
                          className="flex items-center gap-1.5 text-xs text-amber-400 hover:text-amber-300 transition-colors"
                          data-testid={`pe-impact-toggle-${conflict.id.slice(0, 8)}`}
                        >
                          <AlertTriangle className="w-3.5 h-3.5" />
                          <span className="font-medium">{lang === "it" ? "Impatto" : "Impact"}</span>
                          {impactOpen ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                        </button>
                        {impactOpen && (
                          <div className="mt-2 p-2.5 rounded-md bg-amber-950/20 border border-amber-900/30 text-xs text-slate-300" data-testid={`pe-impact-content-${conflict.id.slice(0, 8)}`}>
                            {conflict.impact_description}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Collapsible: Guidance */}
                    {conflict.guidance && (
                      <div>
                        <button
                          onClick={() => toggleExpand(conflict.id, "guidance")}
                          className="flex items-center gap-1.5 text-xs text-blue-400 hover:text-blue-300 transition-colors"
                          data-testid={`pe-guidance-toggle-${conflict.id.slice(0, 8)}`}
                        >
                          <Lightbulb className="w-3.5 h-3.5" />
                          <span className="font-medium">{lang === "it" ? "Raccomandazione" : "Recommendation"}</span>
                          {guidanceOpen ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                        </button>
                        {guidanceOpen && (
                          <div className="mt-2 p-2.5 rounded-md bg-blue-950/20 border border-blue-900/30 text-xs text-slate-300" data-testid={`pe-guidance-content-${conflict.id.slice(0, 8)}`}>
                            {conflict.guidance}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Actions: Detail + Resolve */}
                    <div className="flex justify-end gap-2">
                      <Button
                        size="sm" variant="outline"
                        className="border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white text-xs"
                        onClick={() => openDetail(conflict)}
                        data-testid={`pe-detail-btn-${conflict.id.slice(0, 8)}`}
                      >
                        <Eye className="w-3.5 h-3.5 mr-1.5" />
                        {lang === "it" ? "Dettaglio" : "Detail"}
                      </Button>
                      {canResolve && !isResolved && (
                        <Button
                          size="sm" variant="outline"
                          className="border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white text-xs"
                          onClick={() => { setResolveTarget(conflict); setResolveNote(""); }}
                          data-testid={`pe-resolve-btn-${conflict.id.slice(0, 8)}`}
                        >
                          <CheckCircle className="w-3.5 h-3.5 mr-1.5" />
                          {t("pe_mark_resolved")}
                        </Button>
                      )}
                    </div>
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
            <DialogDescription className="text-slate-400">{resolveTarget?.title}</DialogDescription>
          </DialogHeader>
          <div className="space-y-3 py-2">
            <div>
              <label className="text-xs text-slate-400 mb-1 block">{lang === "it" ? "Responsabile" : "Responsible"}</label>
              <div className="flex items-center gap-2 px-3 py-2 bg-slate-800/60 border border-slate-700 rounded-md text-sm text-slate-300" data-testid="pe-resolve-user">
                <User className="w-3.5 h-3.5 text-slate-500" />
                {user?.username || "admin"}
              </div>
            </div>
            <div>
              <label className="text-xs text-slate-400 mb-1 block">
                {lang === "it" ? "Note di risoluzione" : "Resolution notes"} *
              </label>
              <textarea
                value={resolveNote}
                onChange={e => setResolveNote(e.target.value)}
                placeholder={lang === "it" ? "Descrivi la decisione presa e le motivazioni. Minimo 10 caratteri." : "Describe the decision and reasoning. Minimum 10 characters."}
                rows={4}
                className="w-full bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-sm text-white placeholder:text-slate-600 focus:border-blue-500 focus:outline-none resize-none"
                data-testid="pe-resolve-note"
              />
              <p className={`text-[11px] mt-1 ${resolveNote.length >= 10 ? "text-emerald-500" : "text-slate-600"}`}>
                {resolveNote.length}/10 {lang === "it" ? "min" : "min"}
              </p>
            </div>
          </div>
          <DialogFooter>
            <Button
              onClick={handleResolve}
              disabled={resolving || resolveNote.length < 10}
              className="bg-emerald-600 hover:bg-emerald-700 text-white disabled:opacity-50"
              data-testid="pe-resolve-confirm-btn"
            >
              {resolving ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <CheckCircle className="w-4 h-4 mr-2" />}
              {t("pe_confirm_resolve")}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Detail Sheet */}
      <Sheet open={!!detailConflict} onOpenChange={open => { if (!open) setDetailConflict(null); }}>
        <SheetContent className="bg-slate-900 border-slate-700 text-white w-full sm:max-w-lg overflow-y-auto" data-testid="pe-detail-sheet">
          <SheetHeader>
            <SheetTitle className="text-white text-lg">{lang === "it" ? "Dettaglio Conflitto" : "Conflict Detail"}</SheetTitle>
          </SheetHeader>
          {detailLoading ? (
            <div className="flex items-center justify-center py-12"><Loader2 className="w-6 h-6 text-blue-400 animate-spin" /></div>
          ) : detailConflict && (
            <div className="space-y-4 mt-4">
              {/* Type + Severity */}
              <div className="flex flex-wrap gap-2">
                <Badge variant="outline" className={`text-[11px] ${severityConfig[detailConflict.severity]?.bg || ""}`}>
                  {(detailConflict.severity || "").toUpperCase()}
                </Badge>
                <Badge variant="outline" className={`text-[11px] ${typeConfig[detailConflict.conflict_type]?.badgeBg || ""}`}>
                  {lang === "it" ? typeConfig[detailConflict.conflict_type]?.labelIt : typeConfig[detailConflict.conflict_type]?.label}
                </Badge>
              </div>

              <h3 className="text-base font-semibold text-white">{detailConflict.title}</h3>
              <p className="text-sm text-slate-400">{detailConflict.description}</p>

              {/* Policies involved */}
              {detailConflict.policy_names?.length > 0 && (
                <div>
                  <p className="text-xs text-slate-500 mb-1">{lang === "it" ? "Policy coinvolte" : "Policies involved"}</p>
                  <div className="flex flex-wrap gap-1.5">
                    {detailConflict.policy_names.map(pn => (
                      <Badge key={pn} variant="outline" className="text-xs bg-blue-500/10 text-blue-400 border-blue-900/30">{pn}</Badge>
                    ))}
                  </div>
                </div>
              )}

              {/* Agents */}
              {detailConflict.agent_names?.filter(Boolean).length > 0 && (
                <div>
                  <p className="text-xs text-slate-500 mb-1">{lang === "it" ? "Agenti coinvolti" : "Agents involved"}</p>
                  <div className="flex flex-wrap gap-1.5">
                    {detailConflict.agent_names.filter(Boolean).map(an => (
                      <Badge key={an} variant="outline" className="text-xs bg-violet-500/10 text-violet-400 border-violet-900/30">{an}</Badge>
                    ))}
                  </div>
                </div>
              )}

              {/* Resolved box */}
              {(detailConflict.resolved || resolvedMap[detailConflict.id]?.resolved) ? (
                <div className="p-3 rounded-md bg-emerald-950/20 border border-emerald-900/40" data-testid="pe-detail-resolved-box">
                  <div className="flex items-center gap-2 mb-2">
                    <CheckCircle className="w-4 h-4 text-emerald-400" />
                    <span className="text-sm font-medium text-emerald-400">{lang === "it" ? "Risoluzione documentata" : "Documented Resolution"}</span>
                  </div>
                  <div className="space-y-1 text-xs text-slate-300">
                    <p><span className="text-slate-500">{lang === "it" ? "Responsabile:" : "Resolved by:"}</span> {detailConflict.resolved_by || resolvedMap[detailConflict.id]?.resolved_by}</p>
                    {detailConflict.resolved_at && <p><span className="text-slate-500">{lang === "it" ? "Data:" : "Date:"}</span> {new Date(detailConflict.resolved_at).toLocaleString()}</p>}
                    <p className="mt-2 text-slate-200">{detailConflict.resolution_notes || resolvedMap[detailConflict.id]?.resolution_notes}</p>
                  </div>
                </div>
              ) : (
                <>
                  {/* Impact */}
                  {detailConflict.impact_description && (
                    <div className="p-3 rounded-md bg-amber-950/20 border border-amber-900/30" data-testid="pe-detail-impact">
                      <div className="flex items-center gap-2 mb-1.5">
                        <AlertTriangle className="w-4 h-4 text-amber-400" />
                        <span className="text-xs font-medium text-amber-400">{lang === "it" ? "Impatto" : "Impact"}</span>
                      </div>
                      <p className="text-xs text-slate-300">{detailConflict.impact_description}</p>
                    </div>
                  )}
                  {/* Guidance */}
                  {detailConflict.guidance && (
                    <div className="p-3 rounded-md bg-blue-950/20 border border-blue-900/30" data-testid="pe-detail-guidance">
                      <div className="flex items-center gap-2 mb-1.5">
                        <Lightbulb className="w-4 h-4 text-blue-400" />
                        <span className="text-xs font-medium text-blue-400">{lang === "it" ? "Raccomandazione" : "Recommendation"}</span>
                      </div>
                      <p className="text-xs text-slate-300">{detailConflict.guidance}</p>
                    </div>
                  )}
                </>
              )}
            </div>
          )}
        </SheetContent>
      </Sheet>
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
