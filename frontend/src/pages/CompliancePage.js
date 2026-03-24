import React, { useEffect, useState } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { useAuth } from "@/contexts/AuthContext";
import { ShieldCheck, AlertTriangle, CheckCircle, XCircle, Clock, FileDown, Loader2 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { toast } from "sonner";
import axios from "axios";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const statusConfig = {
  compliant: { icon: CheckCircle, color: "text-emerald-400", bg: "bg-emerald-500/10", border: "border-emerald-500/30", badge: "bg-emerald-950/30 text-emerald-400 border-emerald-900/50", label: "Compliant", labelIt: "Conforme" },
  in_progress: { icon: Clock, color: "text-amber-400", bg: "bg-amber-500/10", border: "border-amber-500/30", badge: "bg-amber-950/30 text-amber-400 border-amber-900/50", label: "In Progress", labelIt: "In Corso" },
  non_compliant: { icon: XCircle, color: "text-red-400", bg: "bg-red-500/10", border: "border-red-500/30", badge: "bg-red-950/30 text-red-400 border-red-900/50", label: "Non-Compliant", labelIt: "Non Conforme" },
};

const categoryBadge = {
  regulation: "bg-blue-950/30 text-blue-400 border-blue-900/50",
  standard: "bg-violet-950/30 text-violet-400 border-violet-900/50",
  directive: "bg-cyan-950/30 text-cyan-400 border-cyan-900/50",
};

// Roles that can export
const EXPORT_ROLES = ["admin", "dpo", "auditor"];

export default function CompliancePage() {
  const { t, lang } = useLanguage();
  const { user } = useAuth();
  const [standards, setStandards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);

  // Check if user can export
  const canExport = user && EXPORT_ROLES.includes(user.role);

  useEffect(() => {
    axios.get(`${API}/compliance`)
      .then(res => setStandards(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleExportPdf = async () => {
    setExporting(true);
    
    try {
      const response = await axios.get(`${API}/compliance/export/pdf`, {
        responseType: "blob",
      });
      
      // Extract filename from header or generate one
      const contentDisposition = response.headers["content-disposition"];
      let filename = `compliance_report_${new Date().toISOString().slice(0,10)}.pdf`;
      if (contentDisposition) {
        const match = contentDisposition.match(/filename=([^;]+)/);
        if (match) filename = match[1].replace(/"/g, "");
      }
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data], { type: "application/pdf" }));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success("Compliance report exported successfully");
    } catch (error) {
      console.error("Export failed:", error);
      toast.error(t("export_failed"));
    } finally {
      setExporting(false);
    }
  };

  const overallProgress = standards.length > 0
    ? Math.round(standards.reduce((sum, s) => sum + s.progress, 0) / standards.length)
    : 0;

  const compliantCount = standards.filter(s => s.status === "compliant").length;
  const inProgressCount = standards.filter(s => s.status === "in_progress").length;
  const nonCompliantCount = standards.filter(s => s.status === "non_compliant").length;

  return (
    <div className="space-y-6" data-testid="compliance-page">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="font-['Space_Grotesk'] text-2xl font-bold tracking-tight text-white">{t("compliance_title")}</h1>
          <p className="text-sm text-slate-500 mt-1">{t("compliance_subtitle")}</p>
        </div>
        
        {/* Export Button */}
        {canExport && (
          <Button
            variant="outline"
            className="border-slate-700 bg-slate-900/50 text-slate-300 hover:bg-slate-800 hover:text-white rounded-sm gap-2"
            onClick={handleExportPdf}
            disabled={exporting}
            data-testid="export-compliance-btn"
          >
            {exporting ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <FileDown className="w-4 h-4" />
            )}
            {exporting ? t("exporting") : t("export_compliance_report")}
          </Button>
        )}
      </div>

      {loading ? (
        <div className="flex justify-center py-16"><div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" /></div>
      ) : (
        <>
          {/* Summary Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4" data-testid="compliance-summary">
            <Card className="bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm" data-testid="overall-score-card">
              <CardContent className="p-5">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-9 h-9 rounded-sm bg-blue-500/10 flex items-center justify-center">
                    <ShieldCheck className="w-4 h-4 text-blue-400" />
                  </div>
                  <span className="text-xs text-slate-500 font-mono uppercase tracking-widest">
                    {lang === "it" ? "Punteggio Totale" : "Overall Score"}
                  </span>
                </div>
                <div className="font-['Space_Grotesk'] text-4xl font-bold text-white">{overallProgress}%</div>
                <Progress value={overallProgress} className="mt-3 h-1.5 bg-slate-800" />
              </CardContent>
            </Card>
            {[
              { count: compliantCount, config: statusConfig.compliant, key: "compliant" },
              { count: inProgressCount, config: statusConfig.in_progress, key: "in_progress" },
              { count: nonCompliantCount, config: statusConfig.non_compliant, key: "non_compliant" },
            ].map(({ count, config, key }) => (
              <Card key={key} className="bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm" data-testid={`compliance-stat-${key}`}>
                <CardContent className="p-5">
                  <div className="flex items-center gap-3 mb-3">
                    <div className={`w-9 h-9 rounded-sm ${config.bg} flex items-center justify-center`}>
                      <config.icon className={`w-4 h-4 ${config.color}`} />
                    </div>
                    <span className="text-xs text-slate-500 font-mono uppercase tracking-widest">
                      {lang === "it" ? config.labelIt : config.label}
                    </span>
                  </div>
                  <div className="font-['Space_Grotesk'] text-4xl font-bold text-white">{count}</div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Standards List */}
          <div className="space-y-3" data-testid="compliance-standards-list">
            {standards.map((standard) => {
              const config = statusConfig[standard.status] || statusConfig.in_progress;
              return (
                <Card key={standard.id} className="bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm hover:border-slate-700 transition-colors duration-300" data-testid={`compliance-card-${standard.code}`}>
                  <CardContent className="p-5">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-start gap-4 min-w-0 flex-1">
                        <div className={`w-10 h-10 rounded-sm ${config.bg} ${config.border} border flex items-center justify-center shrink-0`}>
                          <config.icon className={`w-5 h-5 ${config.color}`} />
                        </div>
                        <div className="min-w-0 flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <h3 className="font-['Space_Grotesk'] text-base font-semibold text-white">{standard.name}</h3>
                            <Badge className={`${config.badge} border text-[10px]`}>{lang === "it" ? config.labelIt : config.label}</Badge>
                            <Badge className={`${categoryBadge[standard.category]} border text-[10px]`}>{standard.category}</Badge>
                          </div>
                          <p className="text-xs text-slate-400 mb-3">{standard.description}</p>
                          <div className="flex items-center gap-4">
                            <div className="flex-1 max-w-xs">
                              <div className="flex items-center justify-between mb-1">
                                <span className="text-[10px] font-mono text-slate-500 uppercase tracking-widest">
                                  {lang === "it" ? "Progresso" : "Progress"}
                                </span>
                                <span className="text-xs font-mono text-slate-400">{standard.progress}%</span>
                              </div>
                              <Progress value={standard.progress} className="h-1.5 bg-slate-800" />
                            </div>
                            <div className="text-xs text-slate-500 font-mono">
                              {standard.requirements_met}/{standard.requirements_total} {lang === "it" ? "requisiti" : "requirements"}
                            </div>
                          </div>
                        </div>
                      </div>
                      <div className="text-right shrink-0">
                        <p className="text-[10px] font-mono text-slate-600 uppercase tracking-widest">{lang === "it" ? "Prossima Revisione" : "Next Review"}</p>
                        <p className="text-xs font-mono text-slate-400">
                          {standard.next_review ? new Date(standard.next_review).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" }) : "—"}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
}
