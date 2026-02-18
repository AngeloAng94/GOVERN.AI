import React, { useEffect, useState } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { FileText, Plus, Pencil, Trash2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { toast } from "sonner";
import axios from "axios";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const severityBadge = {
  low: "bg-emerald-950/30 text-emerald-400 border-emerald-900/50",
  medium: "bg-amber-950/30 text-amber-400 border-amber-900/50",
  high: "bg-orange-950/30 text-orange-400 border-orange-900/50",
  critical: "bg-red-950/30 text-red-400 border-red-900/50",
};

const enforcementBadge = {
  block: "bg-red-950/30 text-red-400 border-red-900/50",
  log: "bg-blue-950/30 text-blue-400 border-blue-900/50",
  throttle: "bg-amber-950/30 text-amber-400 border-amber-900/50",
  auto: "bg-violet-950/30 text-violet-400 border-violet-900/50",
};

const emptyForm = {
  name: "", description: "", agent_id: "", rule_type: "restriction",
  conditions: [], actions: [], severity: "medium", regulation: "GDPR", enforcement: "block"
};

export default function PoliciesPage() {
  const { t } = useLanguage();
  const [policies, setPolicies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ ...emptyForm });
  const [condInput, setCondInput] = useState("");
  const [actInput, setActInput] = useState("");

  const fetchPolicies = () => {
    axios.get(`${API}/policies`).then(res => setPolicies(res.data)).catch(console.error).finally(() => setLoading(false));
  };

  useEffect(() => { fetchPolicies(); }, []);

  const openCreate = () => {
    setEditing(null);
    setForm({ ...emptyForm });
    setCondInput("");
    setActInput("");
    setOpen(true);
  };

  const openEdit = (policy) => {
    setEditing(policy);
    setForm({
      name: policy.name, description: policy.description, agent_id: policy.agent_id || "",
      rule_type: policy.rule_type, conditions: policy.conditions || [], actions: policy.actions || [],
      severity: policy.severity, regulation: policy.regulation, enforcement: policy.enforcement
    });
    setCondInput((policy.conditions || []).join(", "));
    setActInput((policy.actions || []).join(", "));
    setOpen(true);
  };

  const handleSave = async () => {
    const payload = {
      ...form,
      conditions: condInput.split(",").map(s => s.trim()).filter(Boolean),
      actions: actInput.split(",").map(s => s.trim()).filter(Boolean),
    };
    try {
      if (editing) {
        await axios.put(`${API}/policies/${editing.id}`, payload);
        toast.success("Policy updated");
      } else {
        await axios.post(`${API}/policies`, payload);
        toast.success("Policy created");
      }
      setOpen(false);
      fetchPolicies();
    } catch (e) {
      toast.error("Error saving policy");
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API}/policies/${id}`);
      toast.success("Policy deleted");
      fetchPolicies();
    } catch (e) {
      toast.error("Error deleting policy");
    }
  };

  return (
    <div className="space-y-6" data-testid="policies-page">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-['Space_Grotesk'] text-2xl font-bold tracking-tight text-white">{t("policies_title")}</h1>
          <p className="text-sm text-slate-500 mt-1">{t("policies_subtitle")}</p>
        </div>
        <Button onClick={openCreate} className="bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_15px_rgba(59,130,246,0.3)] rounded-sm gap-2" data-testid="new-policy-btn">
          <Plus className="w-4 h-4" />
          {t("new_policy")}
        </Button>
      </div>

      {loading ? (
        <div className="flex justify-center py-16"><div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" /></div>
      ) : policies.length === 0 ? (
        <Card className="bg-slate-900/40 border-slate-800 rounded-sm"><CardContent className="p-12 text-center text-slate-500">{t("no_data")}</CardContent></Card>
      ) : (
        <div className="space-y-3" data-testid="policies-list">
          {policies.map((policy) => (
            <Card key={policy.id} className="bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm hover:border-slate-700 transition-colors duration-300" data-testid={`policy-card-${policy.id}`}>
              <CardContent className="p-5">
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3 min-w-0">
                    <div className="w-9 h-9 rounded-sm bg-amber-500/10 flex items-center justify-center shrink-0 mt-0.5">
                      <FileText className="w-4 h-4 text-amber-400" />
                    </div>
                    <div className="min-w-0">
                      <h3 className="font-['Space_Grotesk'] text-sm font-semibold text-white">{policy.name}</h3>
                      <p className="text-xs text-slate-400 mt-0.5">{policy.description}</p>
                      <div className="flex flex-wrap gap-1.5 mt-2">
                        <Badge className={`${severityBadge[policy.severity]} border text-[10px]`}>{policy.severity}</Badge>
                        <Badge className="bg-blue-950/30 text-blue-400 border-blue-900/50 border text-[10px]">{policy.regulation}</Badge>
                        <Badge className={`${enforcementBadge[policy.enforcement]} border text-[10px]`}>{policy.enforcement}</Badge>
                        <Badge className="bg-slate-800/50 text-slate-400 border-slate-700 border text-[10px]">{policy.rule_type}</Badge>
                      </div>
                      {policy.conditions?.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          {policy.conditions.map((c, i) => (
                            <span key={i} className="text-[10px] font-mono text-slate-600 bg-slate-800/50 px-1.5 py-0.5 rounded">{c}</span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-1 shrink-0">
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-500 hover:text-white" onClick={() => openEdit(policy)} data-testid={`edit-policy-${policy.id}`}>
                      <Pencil className="w-3.5 h-3.5" />
                    </Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-500 hover:text-red-400" onClick={() => handleDelete(policy.id)} data-testid={`delete-policy-${policy.id}`}>
                      <Trash2 className="w-3.5 h-3.5" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Create/Edit Dialog */}
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="bg-slate-900 border-slate-800 rounded-sm max-w-lg" data-testid="policy-dialog">
          <DialogHeader>
            <DialogTitle className="font-['Space_Grotesk'] text-white">{editing ? t("edit") : t("create")} Policy</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 mt-2">
            <div className="space-y-1.5">
              <Label className="text-slate-400 text-xs">{t("policy_name")}</Label>
              <Input className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm" value={form.name} onChange={e => setForm({...form, name: e.target.value})} data-testid="policy-name-input" />
            </div>
            <div className="space-y-1.5">
              <Label className="text-slate-400 text-xs">{t("policy_description")}</Label>
              <Input className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm" value={form.description} onChange={e => setForm({...form, description: e.target.value})} data-testid="policy-desc-input" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <Label className="text-slate-400 text-xs">{t("policy_type")}</Label>
                <Select value={form.rule_type} onValueChange={v => setForm({...form, rule_type: v})}>
                  <SelectTrigger className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm" data-testid="policy-type-select"><SelectValue /></SelectTrigger>
                  <SelectContent className="bg-slate-900 border-slate-800">
                    {["restriction", "logging", "rate_limit", "approval", "retention"].map(t => <SelectItem key={t} value={t}>{t}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1.5">
                <Label className="text-slate-400 text-xs">{t("policy_severity")}</Label>
                <Select value={form.severity} onValueChange={v => setForm({...form, severity: v})}>
                  <SelectTrigger className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm" data-testid="policy-severity-select"><SelectValue /></SelectTrigger>
                  <SelectContent className="bg-slate-900 border-slate-800">
                    {["low", "medium", "high", "critical"].map(s => <SelectItem key={s} value={s} className="capitalize">{s}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <Label className="text-slate-400 text-xs">{t("policy_regulation")}</Label>
                <Select value={form.regulation} onValueChange={v => setForm({...form, regulation: v})}>
                  <SelectTrigger className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm" data-testid="policy-reg-select"><SelectValue /></SelectTrigger>
                  <SelectContent className="bg-slate-900 border-slate-800">
                    {["GDPR", "EU-AI-ACT", "ISO-27001", "ISO-42001", "DORA", "NIS2"].map(r => <SelectItem key={r} value={r}>{r}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1.5">
                <Label className="text-slate-400 text-xs">{t("policy_enforcement")}</Label>
                <Select value={form.enforcement} onValueChange={v => setForm({...form, enforcement: v})}>
                  <SelectTrigger className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm" data-testid="policy-enf-select"><SelectValue /></SelectTrigger>
                  <SelectContent className="bg-slate-900 border-slate-800">
                    {["block", "log", "throttle", "auto"].map(e => <SelectItem key={e} value={e}>{e}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="space-y-1.5">
              <Label className="text-slate-400 text-xs">{t("policy_conditions")} (comma separated)</Label>
              <Input className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm font-mono text-xs" value={condInput} onChange={e => setCondInput(e.target.value)} placeholder="data_contains_pii, agent_risk_level_high" data-testid="policy-cond-input" />
            </div>
            <div className="space-y-1.5">
              <Label className="text-slate-400 text-xs">{t("policy_actions")} (comma separated)</Label>
              <Input className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm font-mono text-xs" value={actInput} onChange={e => setActInput(e.target.value)} placeholder="block_access, log_attempt, notify_dpo" data-testid="policy-act-input" />
            </div>
            <div className="flex justify-end gap-2 pt-2">
              <Button variant="ghost" onClick={() => setOpen(false)} className="text-slate-400 rounded-sm" data-testid="policy-cancel-btn">{t("cancel")}</Button>
              <Button onClick={handleSave} className="bg-blue-600 hover:bg-blue-500 text-white rounded-sm" data-testid="policy-save-btn">{t("save")}</Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
