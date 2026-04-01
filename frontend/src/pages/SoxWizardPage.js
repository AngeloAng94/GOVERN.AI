import React, { useEffect, useState, useCallback } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { useAuth } from "@/contexts/AuthContext";
import {
  Shield, Database, Settings, Lock, Server,
  FileDown, Loader2, CheckCircle, XCircle, Clock,
  AlertTriangle, MinusCircle, ChevronDown, ChevronRight,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter,
} from "@/components/ui/dialog";
import { toast } from "sonner";
import axios from "axios";
import SkeletonLoader from "@/components/SkeletonLoader";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const domainIcons = {
  "Access Control": Lock,
  "Change Management": Settings,
  "IT Operations": Server,
  "Data Integrity": Database,
  "Security": Shield,
};

const statusConfig = {
  completed:      { icon: CheckCircle,    color: "text-emerald-400", bg: "bg-emerald-500/10", badge: "bg-emerald-950/30 text-emerald-400 border-emerald-900/50", label: "Completed",      labelIt: "Completato" },
  in_progress:    { icon: Clock,          color: "text-amber-400",   bg: "bg-amber-500/10",   badge: "bg-amber-950/30 text-amber-400 border-amber-900/50",     label: "In Progress",    labelIt: "In Corso" },
  not_started:    { icon: MinusCircle,    color: "text-slate-400",   bg: "bg-slate-500/10",   badge: "bg-slate-800/50 text-slate-400 border-slate-700/50",      label: "Not Started",    labelIt: "Non Iniziato" },
  failed:         { icon: XCircle,        color: "text-red-400",     bg: "bg-red-500/10",     badge: "bg-red-950/30 text-red-400 border-red-900/50",            label: "Failed",         labelIt: "Fallito" },
  not_applicable: { icon: MinusCircle,    color: "text-slate-500",   bg: "bg-slate-500/5",    badge: "bg-slate-800/30 text-slate-500 border-slate-700/30",      label: "N/A",            labelIt: "N/A" },
};

const riskConfig = {
  critical: "bg-red-950/30 text-red-400 border-red-900/50",
  high:     "bg-orange-950/30 text-orange-400 border-orange-900/50",
  medium:   "bg-amber-950/30 text-amber-400 border-amber-900/50",
  low:      "bg-emerald-950/30 text-emerald-400 border-emerald-900/50",
};

const EXPORT_ROLES = ["admin", "dpo"];
const EDIT_ROLES   = ["admin", "dpo", "auditor"];

export default function SoxWizardPage() {
  const { t, lang } = useLanguage();
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);
  const [expandedDomains, setExpandedDomains] = useState({});
  const [editControl, setEditControl] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [saving, setSaving] = useState(false);

  const canExport = user && EXPORT_ROLES.includes(user.role);
  const canEdit   = user && EDIT_ROLES.includes(user.role);

  const fetchControls = useCallback(() => {
    axios.get(`${API}/sox/controls`)
      .then(res => {
        setData(res.data);
        if (Object.keys(expandedDomains).length === 0) {
          const exp = {};
          res.data.domains.forEach(d => { exp[d.name] = true; });
          setExpandedDomains(exp);
        }
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => { fetchControls(); }, [fetchControls]);

  const toggleDomain = (name) => {
    setExpandedDomains(prev => ({ ...prev, [name]: !prev[name] }));
  };

  const openEdit = (control) => {
    setEditControl(control);
    setEditForm({
      status: control.status,
      evidence: control.evidence || "",
      assignee: control.assignee || "",
      due_date: control.due_date ? control.due_date.split("T")[0] : "",
    });
  };

  const handleSave = async () => {
    if (!editControl) return;
    setSaving(true);
    try {
      await axios.patch(`${API}/sox/controls/${editControl.id}`, editForm);
      toast.success(t("sox_control_updated"));
      setEditControl(null);
      fetchControls();
    } catch (err) {
      toast.error(t("sox_update_failed"));
    } finally {
      setSaving(false);
    }
  };

  const handleExportPdf = async () => {
    setExporting(true);
    try {
      const res = await axios.get(`${API}/sox/report/pdf`, { responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `SOX_404_Report_${new Date().toISOString().split("T")[0]}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success(lang === "it" ? "Report PDF scaricato" : "PDF Report downloaded");
    } catch {
      toast.error(lang === "it" ? "Errore durante l'export" : "Export failed");
    } finally {
      setExporting(false);
    }
  };

  const isDuePast = (d) => {
    if (!d) return false;
    return new Date(d) < new Date();
  };

  if (loading) return <SkeletonLoader type="cards" count={5} />;
  if (!data) return null;

  const overallPct = data.overall_pct;
  const overallLabel = overallPct >= 80
    ? t("sox_ready")
    : overallPct >= 50
    ? t("sox_in_progress_status")
    : t("sox_not_ready");
  const overallColor = overallPct >= 80
    ? "text-emerald-400"
    : overallPct >= 50
    ? "text-amber-400"
    : "text-red-400";

  return (
    <div className="space-y-6" data-testid="sox-wizard-page">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white font-['Space_Grotesk']" data-testid="sox-wizard-title">
            {t("sox_title")}
          </h1>
          <p className="text-slate-400 text-sm mt-1">{t("sox_subtitle")}</p>
        </div>
        {canExport && (
          <Button
            onClick={handleExportPdf}
            disabled={exporting}
            variant="outline"
            className="border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white"
            data-testid="sox-export-pdf-btn"
          >
            {exporting ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <FileDown className="w-4 h-4 mr-2" />}
            {t("sox_export_pdf")}
          </Button>
        )}
      </div>

      {/* Global progress */}
      <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm">
        <CardContent className="p-5">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm text-slate-400">{t("sox_overall_progress")}</span>
            <span className={`text-lg font-bold font-['Space_Grotesk'] ${overallColor}`} data-testid="sox-overall-pct">
              {data.completed}/{data.total} {t("sox_controls_completed")} — {overallPct}% {t("sox_ready_audit")}
            </span>
          </div>
          <Progress
            value={overallPct}
            className="h-3 bg-slate-800"
            data-testid="sox-overall-progress"
          />
        </CardContent>
      </Card>

      {/* Domain Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3" data-testid="sox-domain-cards">
        {data.domains.map(domain => {
          const DIcon = domainIcons[domain.name] || Shield;
          const pct = domain.completion_pct;
          const cardBorder = pct >= 75 ? "border-emerald-500/30" : pct >= 25 ? "border-amber-500/30" : "border-red-500/30";
          const pctColor   = pct >= 75 ? "text-emerald-400"      : pct >= 25 ? "text-amber-400"      : "text-red-400";
          const done = domain.controls.filter(c => c.status === "completed").length;
          return (
            <Card
              key={domain.name}
              className={`bg-slate-900/50 backdrop-blur-sm cursor-pointer hover:bg-slate-800/60 transition-colors ${cardBorder}`}
              onClick={() => toggleDomain(domain.name)}
              data-testid={`sox-domain-card-${domain.name.replace(/\s/g, "-").toLowerCase()}`}
            >
              <CardContent className="p-4 flex flex-col items-center text-center gap-2">
                <DIcon className={`w-6 h-6 ${pctColor}`} />
                <span className="text-xs font-medium text-slate-300">{domain.name}</span>
                <span className={`text-xl font-bold font-['Space_Grotesk'] ${pctColor}`}>{pct}%</span>
                <span className="text-[11px] text-slate-500">{done}/{domain.controls.length} completed</span>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Controls Accordion by Domain */}
      <div className="space-y-3" data-testid="sox-controls-list">
        {data.domains.map(domain => {
          const DIcon = domainIcons[domain.name] || Shield;
          const expanded = expandedDomains[domain.name];
          return (
            <Card key={domain.name} className="bg-slate-900/50 border-slate-800 backdrop-blur-sm overflow-hidden">
              <button
                onClick={() => toggleDomain(domain.name)}
                className="w-full flex items-center gap-3 p-4 text-left hover:bg-slate-800/40 transition-colors"
                data-testid={`sox-accordion-${domain.name.replace(/\s/g, "-").toLowerCase()}`}
              >
                {expanded ? <ChevronDown className="w-4 h-4 text-slate-400" /> : <ChevronRight className="w-4 h-4 text-slate-400" />}
                <DIcon className="w-4 h-4 text-blue-400" />
                <span className="text-sm font-semibold text-white flex-1">{domain.name}</span>
                <Badge variant="outline" className="text-xs bg-slate-800/50 text-slate-400 border-slate-700">
                  {domain.completion_pct}%
                </Badge>
              </button>
              {expanded && (
                <div className="border-t border-slate-800">
                  {/* Table header */}
                  <div className="grid grid-cols-12 gap-2 px-4 py-2 text-[11px] text-slate-500 uppercase tracking-wider border-b border-slate-800/50">
                    <div className="col-span-1">ID</div>
                    <div className="col-span-4">Title</div>
                    <div className="col-span-2">{t("sox_status")}</div>
                    <div className="col-span-1">Risk</div>
                    <div className="col-span-2">{t("sox_assignee")}</div>
                    <div className="col-span-1">{t("sox_due_date")}</div>
                    <div className="col-span-1"></div>
                  </div>
                  {domain.controls.map(control => {
                    const sc = statusConfig[control.status] || statusConfig.not_started;
                    const SIcon = sc.icon;
                    const duePast = control.status !== "completed" && isDuePast(control.due_date);
                    return (
                      <div
                        key={control.id}
                        className="grid grid-cols-12 gap-2 px-4 py-2.5 items-center border-b border-slate-800/30 last:border-0 hover:bg-slate-800/20 transition-colors"
                        data-testid={`sox-control-row-${control.control_id}`}
                      >
                        <div className="col-span-1">
                          <code className="text-xs text-blue-400 font-mono">{control.control_id}</code>
                        </div>
                        <div className="col-span-4">
                          <span className="text-sm text-slate-200 leading-tight">{control.title}</span>
                        </div>
                        <div className="col-span-2">
                          <Badge variant="outline" className={`text-[11px] ${sc.badge}`}>
                            <SIcon className="w-3 h-3 mr-1" />
                            {lang === "it" ? sc.labelIt : sc.label}
                          </Badge>
                        </div>
                        <div className="col-span-1">
                          <Badge variant="outline" className={`text-[11px] ${riskConfig[control.risk_level] || ""}`}>
                            {control.risk_level}
                          </Badge>
                        </div>
                        <div className="col-span-2">
                          <span className="text-xs text-slate-400">{control.assignee}</span>
                        </div>
                        <div className="col-span-1">
                          <span className={`text-xs ${duePast ? "text-red-400 font-medium" : "text-slate-400"}`}>
                            {control.due_date ? new Date(control.due_date).toLocaleDateString() : "-"}
                          </span>
                        </div>
                        <div className="col-span-1 text-right">
                          {canEdit && (
                            <Button
                              size="sm"
                              variant="ghost"
                              className="h-7 px-2 text-xs text-slate-400 hover:text-white hover:bg-slate-700"
                              onClick={() => openEdit(control)}
                              data-testid={`sox-edit-btn-${control.control_id}`}
                            >
                              {lang === "it" ? "Modifica" : "Update"}
                            </Button>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </Card>
          );
        })}
      </div>

      {/* Auditor Summary Panel */}
      <Card className="bg-slate-800/40 border-slate-700 backdrop-blur-sm" data-testid="sox-auditor-summary">
        <CardContent className="p-5">
          <h3 className="text-sm font-semibold text-white mb-4">{t("sox_auditor_summary")}</h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
            <div>
              <span className="text-xs text-slate-500">{t("sox_fiscal_year")}</span>
              <p className="text-sm text-white font-medium">{new Date().getFullYear()}</p>
            </div>
            <div>
              <span className="text-xs text-slate-500">{t("sox_overall_status")}</span>
              <p className={`text-sm font-bold ${overallColor}`} data-testid="sox-overall-status">{overallLabel}</p>
            </div>
            <div>
              <span className="text-xs text-slate-500">{t("sox_overall_progress")}</span>
              <p className="text-sm text-white font-medium">{data.completed}/{data.total} ({overallPct}%)</p>
            </div>
          </div>
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pt-3 border-t border-slate-700">
            <p className="text-[11px] text-slate-500 italic">{t("sox_legal_note")}</p>
            {canExport && (
              <Button
                onClick={handleExportPdf}
                disabled={exporting}
                size="sm"
                className="bg-blue-600 hover:bg-blue-700 text-white"
                data-testid="sox-generate-report-btn"
              >
                {exporting ? <Loader2 className="w-3.5 h-3.5 mr-1.5 animate-spin" /> : <FileDown className="w-3.5 h-3.5 mr-1.5" />}
                {t("sox_generate_report")}
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Edit Control Dialog */}
      <Dialog open={!!editControl} onOpenChange={(open) => { if (!open) setEditControl(null); }}>
        <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-md" data-testid="sox-edit-dialog">
          <DialogHeader>
            <DialogTitle className="text-white">
              {editControl && <code className="text-blue-400 mr-2">{editControl.control_id}</code>}
              {editControl?.title}
            </DialogTitle>
            <DialogDescription className="text-slate-400">
              {editControl?.description}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-2">
            {/* Status select */}
            <div>
              <label className="text-xs text-slate-400 mb-1 block">{t("sox_status")}</label>
              <select
                value={editForm.status || ""}
                onChange={(e) => setEditForm(prev => ({ ...prev, status: e.target.value }))}
                className="w-full bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-sm text-white focus:border-blue-500 focus:outline-none"
                data-testid="sox-edit-status-select"
              >
                {Object.entries(statusConfig).map(([val, cfg]) => (
                  <option key={val} value={val}>{lang === "it" ? cfg.labelIt : cfg.label}</option>
                ))}
              </select>
            </div>
            {/* Evidence */}
            <div>
              <label className="text-xs text-slate-400 mb-1 block">{t("sox_evidence")}</label>
              <textarea
                value={editForm.evidence || ""}
                onChange={(e) => setEditForm(prev => ({ ...prev, evidence: e.target.value }))}
                placeholder={t("sox_evidence_placeholder")}
                rows={3}
                className="w-full bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-sm text-white placeholder:text-slate-600 focus:border-blue-500 focus:outline-none resize-none"
                data-testid="sox-edit-evidence"
              />
            </div>
            {/* Assignee */}
            <div>
              <label className="text-xs text-slate-400 mb-1 block">{t("sox_assignee")}</label>
              <input
                type="text"
                value={editForm.assignee || ""}
                onChange={(e) => setEditForm(prev => ({ ...prev, assignee: e.target.value }))}
                className="w-full bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-sm text-white focus:border-blue-500 focus:outline-none"
                data-testid="sox-edit-assignee"
              />
            </div>
            {/* Due date */}
            <div>
              <label className="text-xs text-slate-400 mb-1 block">{t("sox_due_date")}</label>
              <input
                type="date"
                value={editForm.due_date || ""}
                onChange={(e) => setEditForm(prev => ({ ...prev, due_date: e.target.value }))}
                className="w-full bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-sm text-white focus:border-blue-500 focus:outline-none"
                data-testid="sox-edit-due-date"
              />
            </div>
          </div>
          <DialogFooter>
            <Button
              onClick={handleSave}
              disabled={saving}
              className="bg-blue-600 hover:bg-blue-700 text-white"
              data-testid="sox-edit-save-btn"
            >
              {saving ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : null}
              {t("sox_save")}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
