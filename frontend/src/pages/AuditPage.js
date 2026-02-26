import React, { useEffect, useState, useCallback } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { Activity, Search } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import axios from "axios";

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

export default function AuditPage() {
  const { t } = useLanguage();
  const [logs, setLogs] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [outcome, setOutcome] = useState("all");
  const [risk, setRisk] = useState("all");

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

  return (
    <div className="space-y-6" data-testid="audit-page">
      <div>
        <h1 className="font-['Space_Grotesk'] text-2xl font-bold tracking-tight text-white">{t("audit_title")}</h1>
        <p className="text-sm text-slate-500 mt-1">{t("audit_subtitle")}</p>
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
            <div className="flex justify-center py-16"><div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" /></div>
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
