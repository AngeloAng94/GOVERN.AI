import React, { useEffect, useState, useCallback } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { useAuth } from "@/contexts/AuthContext";
import { Activity, Search, FileText, FileDown, FileSearch, Loader2 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { toast } from "sonner";
import axios from "axios";
import EmptyState from "@/components/EmptyState";
import SkeletonLoader from "@/components/SkeletonLoader";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const outcomeColors = {
  allowed: "bg-emerald-950/30 text-emerald-400 border-emerald-900/50",
  blocked: "bg-red-950/30 text-red-400 border-red-900/50",
  logged: "bg-blue-950/30 text-blue-400 border-blue-900/50",
  escalated: "bg-amber-950/30 text-amber-400 border-amber-900/50",
};

const riskColors = {
  low: "bg-emerald-950/30 text-emerald-400 border-emerald-900/50",
  medium: "bg-amber-950/30 text-amber-400 border-amber-900/50",
  high: "bg-orange-950/30 text-orange-400 border-orange-900/50",
  critical: "bg-red-950/30 text-red-400 border-red-900/50",
};

// Roles that can export
const EXPORT_ROLES = ["admin", "dpo", "auditor"];

export default function AuditPage() {
  const { t } = useLanguage();
  const { user } = useAuth();
  const [logs, setLogs] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [outcome, setOutcome] = useState("all");
  const [risk, setRisk] = useState("all");
  const [exportingCsv, setExportingCsv] = useState(false);
  const [exportingPdf, setExportingPdf] = useState(false);

  // Check if user can export
  const canExport = user && EXPORT_ROLES.includes(user.role);

  // Fix 1.6: Debounce search input (300ms)
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
    }, 300);
    return () => clearTimeout(timer);
  }, [search]);

  const fetchLogs = useCallback(() => {
    setLoading(true);
    const params = new URLSearchParams();
    if (debouncedSearch) params.append("search", debouncedSearch);
    if (outcome !== "all") params.append("outcome", outcome);
    if (risk !== "all") params.append("risk_level", risk);
    params.append("limit", "50");

    axios.get(`${API}/audit?${params.toString()}`)
      .then(res => {
        setLogs(res.data.logs);
        setTotal(res.data.total);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [debouncedSearch, outcome, risk]);

  useEffect(() => { fetchLogs(); }, [fetchLogs]);

  const formatTimestamp = (ts) => {
    try {
      const d = new Date(ts);
      return d.toLocaleString("en-GB", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit", second: "2-digit" });
    } catch { return ts; }
  };

  const buildExportParams = () => {
    const params = new URLSearchParams();
    if (debouncedSearch) params.append("search", debouncedSearch);
    if (outcome !== "all") params.append("outcome", outcome);
    if (risk !== "all") params.append("risk_level", risk);
    return params.toString();
  };

  const handleExport = async (type) => {
    const setExporting = type === "csv" ? setExportingCsv : setExportingPdf;
    const endpoint = type === "csv" ? "/audit/export/csv" : "/audit/export/pdf";
    const mimeType = type === "csv" ? "text/csv" : "application/pdf";
    
    setExporting(true);
    
    try {
      const params = buildExportParams();
      const response = await axios.get(`${API}${endpoint}?${params}`, {
        responseType: "blob",
      });
      
      // Extract filename from Content-Disposition header or generate one
      const contentDisposition = response.headers["content-disposition"];
      let filename = `audit_export_${new Date().toISOString().slice(0,10)}.${type}`;
      if (contentDisposition) {
        const match = contentDisposition.match(/filename=([^;]+)/);
        if (match) filename = match[1].replace(/"/g, "");
      }
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data], { type: mimeType }));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success(type === "csv" ? "CSV exported successfully" : "PDF exported successfully");
    } catch (error) {
      console.error("Export failed:", error);
      toast.error(t("export_failed"));
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="space-y-6" data-testid="audit-page">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="font-['Space_Grotesk'] text-2xl font-bold tracking-tight text-white">{t("audit_title")}</h1>
          <p className="text-sm text-slate-500 mt-1">{t("audit_subtitle")}</p>
        </div>
        
        {/* Export Buttons */}
        {canExport && (
          <div className="flex gap-2" data-testid="export-buttons">
            <Button
              variant="outline"
              className="border-slate-700 bg-slate-900/50 text-slate-300 hover:bg-slate-800 hover:text-white rounded-sm gap-2"
              onClick={() => handleExport("csv")}
              disabled={exportingCsv || exportingPdf}
              data-testid="export-csv-btn"
            >
              {exportingCsv ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <FileText className="w-4 h-4" />
              )}
              {exportingCsv ? t("exporting") : t("export_csv")}
            </Button>
            <Button
              variant="outline"
              className="border-slate-700 bg-slate-900/50 text-slate-300 hover:bg-slate-800 hover:text-white rounded-sm gap-2"
              onClick={() => handleExport("pdf")}
              disabled={exportingCsv || exportingPdf}
              data-testid="export-pdf-btn"
            >
              {exportingPdf ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <FileDown className="w-4 h-4" />
              )}
              {exportingPdf ? t("exporting") : t("export_pdf")}
            </Button>
          </div>
        )}
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3" data-testid="audit-filters">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-600" />
          <Input
            className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm pl-9 font-mono text-sm"
            placeholder={t("audit_search")}
            value={search}
            onChange={e => setSearch(e.target.value)}
            data-testid="audit-search-input"
          />
        </div>
        <Select value={outcome} onValueChange={setOutcome}>
          <SelectTrigger className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm w-44" data-testid="audit-outcome-filter">
            <SelectValue placeholder={t("audit_filter_outcome")} />
          </SelectTrigger>
          <SelectContent className="bg-slate-900 border-slate-800">
            <SelectItem value="all">{t("all")}</SelectItem>
            <SelectItem value="allowed">Allowed</SelectItem>
            <SelectItem value="blocked">Blocked</SelectItem>
            <SelectItem value="logged">Logged</SelectItem>
            <SelectItem value="escalated">Escalated</SelectItem>
          </SelectContent>
        </Select>
        <Select value={risk} onValueChange={setRisk}>
          <SelectTrigger className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm w-44" data-testid="audit-risk-filter">
            <SelectValue placeholder={t("audit_filter_risk")} />
          </SelectTrigger>
          <SelectContent className="bg-slate-900 border-slate-800">
            <SelectItem value="all">{t("all")}</SelectItem>
            <SelectItem value="low">Low</SelectItem>
            <SelectItem value="medium">Medium</SelectItem>
            <SelectItem value="high">High</SelectItem>
            <SelectItem value="critical">Critical</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <p className="text-xs text-slate-600 font-mono">{total} {t("audit_events").toLowerCase()}</p>

      {/* Audit Table */}
      <Card className="bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm overflow-hidden" data-testid="audit-table-card">
        <CardContent className="p-0">
          {loading ? (
            <div className="p-4"><SkeletonLoader rows={8} type="table" /></div>
          ) : logs.length === 0 ? (
            <EmptyState
              icon={FileSearch}
              title={t("empty_audit_title")}
              subtitle={t("empty_audit_subtitle")}
            />
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="border-slate-800 hover:bg-transparent">
                    <TableHead className="text-slate-500 font-mono text-[10px] uppercase tracking-widest">Timestamp</TableHead>
                    <TableHead className="text-slate-500 font-mono text-[10px] uppercase tracking-widest">Agent</TableHead>
                    <TableHead className="text-slate-500 font-mono text-[10px] uppercase tracking-widest">Action</TableHead>
                    <TableHead className="text-slate-500 font-mono text-[10px] uppercase tracking-widest">Resource</TableHead>
                    <TableHead className="text-slate-500 font-mono text-[10px] uppercase tracking-widest">Outcome</TableHead>
                    <TableHead className="text-slate-500 font-mono text-[10px] uppercase tracking-widest">Risk</TableHead>
                    <TableHead className="text-slate-500 font-mono text-[10px] uppercase tracking-widest">User</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {logs.map((log, i) => (
                    <TableRow key={log.id || i} className="border-slate-800/60 hover:bg-slate-800/30" data-testid={`audit-row-${i}`}>
                      <TableCell className="font-mono text-xs text-slate-500 whitespace-nowrap">{formatTimestamp(log.timestamp)}</TableCell>
                      <TableCell className="text-sm text-slate-300">{log.agent_name || "—"}</TableCell>
                      <TableCell className="font-mono text-xs text-slate-400">{log.action}</TableCell>
                      <TableCell className="font-mono text-xs text-slate-500 max-w-[150px] truncate">{log.resource}</TableCell>
                      <TableCell><Badge className={`${outcomeColors[log.outcome]} border text-[10px]`}>{log.outcome}</Badge></TableCell>
                      <TableCell><Badge className={`${riskColors[log.risk_level]} border text-[10px]`}>{log.risk_level}</Badge></TableCell>
                      <TableCell className="font-mono text-xs text-slate-500">{log.user}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
