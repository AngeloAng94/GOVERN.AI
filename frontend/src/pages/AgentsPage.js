import React, { useEffect, useState } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { Bot, Plus, Pencil, Trash2 } from "lucide-react";
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

const riskBadge = {
  low: "bg-emerald-950/30 text-emerald-400 border-emerald-900/50",
  medium: "bg-amber-950/30 text-amber-400 border-amber-900/50",
  high: "bg-orange-950/30 text-orange-400 border-orange-900/50",
  critical: "bg-red-950/30 text-red-400 border-red-900/50",
};

const statusBadge = {
  active: "bg-emerald-950/30 text-emerald-400 border-emerald-900/50",
  suspended: "bg-amber-950/30 text-amber-400 border-amber-900/50",
  inactive: "bg-slate-800/50 text-slate-400 border-slate-700",
};

const emptyForm = {
  name: "", description: "", model_type: "GPT-5.2", risk_level: "medium",
  status: "active", allowed_actions: [], restricted_domains: [],
  data_classification: "internal", owner: ""
};

export default function AgentsPage() {
  const { t } = useLanguage();
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ ...emptyForm });
  const [actionsInput, setActionsInput] = useState("");
  const [domainsInput, setDomainsInput] = useState("");

  const fetchAgents = () => {
    axios.get(`${API}/agents`).then(res => setAgents(res.data)).catch(console.error).finally(() => setLoading(false));
  };

  useEffect(() => { fetchAgents(); }, []);

  const openCreate = () => {
    setEditing(null);
    setForm({ ...emptyForm });
    setActionsInput("");
    setDomainsInput("");
    setOpen(true);
  };

  const openEdit = (agent) => {
    setEditing(agent);
    setForm({
      name: agent.name, description: agent.description, model_type: agent.model_type,
      risk_level: agent.risk_level, status: agent.status,
      allowed_actions: agent.allowed_actions || [], restricted_domains: agent.restricted_domains || [],
      data_classification: agent.data_classification || "internal", owner: agent.owner || ""
    });
    setActionsInput((agent.allowed_actions || []).join(", "));
    setDomainsInput((agent.restricted_domains || []).join(", "));
    setOpen(true);
  };

  const handleSave = async () => {
    const payload = {
      ...form,
      allowed_actions: actionsInput.split(",").map(s => s.trim()).filter(Boolean),
      restricted_domains: domainsInput.split(",").map(s => s.trim()).filter(Boolean),
    };
    try {
      if (editing) {
        await axios.put(`${API}/agents/${editing.id}`, payload);
        toast.success("Agent updated");
      } else {
        await axios.post(`${API}/agents`, payload);
        toast.success("Agent created");
      }
      setOpen(false);
      fetchAgents();
    } catch (e) {
      toast.error("Error saving agent");
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API}/agents/${id}`);
      toast.success("Agent deleted");
      fetchAgents();
    } catch (e) {
      toast.error("Error deleting agent");
    }
  };

  return (
    <div className="space-y-6" data-testid="agents-page">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-['Space_Grotesk'] text-2xl font-bold tracking-tight text-white">{t("agents_title")}</h1>
          <p className="text-sm text-slate-500 mt-1">{t("agents_subtitle")}</p>
        </div>
        <Button onClick={openCreate} className="bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_15px_rgba(59,130,246,0.3)] rounded-sm gap-2" data-testid="new-agent-btn">
          <Plus className="w-4 h-4" />
          {t("new_agent")}
        </Button>
      </div>

      {loading ? (
        <div className="flex justify-center py-16"><div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" /></div>
      ) : agents.length === 0 ? (
        <Card className="bg-slate-900/40 border-slate-800 rounded-sm"><CardContent className="p-12 text-center text-slate-500">{t("no_data")}</CardContent></Card>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4" data-testid="agents-grid">
          {agents.map((agent) => (
            <Card key={agent.id} className="bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm hover:border-slate-700 transition-colors duration-300" data-testid={`agent-card-${agent.id}`}>
              <CardHeader className="pb-2">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-sm bg-blue-500/10 flex items-center justify-center">
                      <Bot className="w-4 h-4 text-blue-400" />
                    </div>
                    <div>
                      <CardTitle className="font-['Space_Grotesk'] text-base font-semibold text-white">{agent.name}</CardTitle>
                      <p className="text-xs text-slate-500 font-mono">{agent.model_type}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-1">
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-500 hover:text-white" onClick={() => openEdit(agent)} data-testid={`edit-agent-${agent.id}`}>
                      <Pencil className="w-3.5 h-3.5" />
                    </Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-500 hover:text-red-400" onClick={() => handleDelete(agent.id)} data-testid={`delete-agent-${agent.id}`}>
                      <Trash2 className="w-3.5 h-3.5" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="pt-0">
                <p className="text-sm text-slate-400 mb-3">{agent.description}</p>
                <div className="flex flex-wrap gap-2 mb-3">
                  <Badge className={`${statusBadge[agent.status]} border text-[10px]`}>{agent.status}</Badge>
                  <Badge className={`${riskBadge[agent.risk_level]} border text-[10px]`}>{agent.risk_level} risk</Badge>
                  <Badge className="bg-slate-800/50 text-slate-400 border-slate-700 border text-[10px]">{agent.data_classification}</Badge>
                </div>
                {agent.owner && <p className="text-xs text-slate-600 font-mono">{t("agent_owner")}: {agent.owner}</p>}
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Create/Edit Dialog */}
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="bg-slate-900 border-slate-800 rounded-sm max-w-lg" data-testid="agent-dialog">
          <DialogHeader>
            <DialogTitle className="font-['Space_Grotesk'] text-white">{editing ? t("edit") : t("create")} {t("sidebar_agents")}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 mt-2">
            <div className="space-y-1.5">
              <Label className="text-slate-400 text-xs">{t("agent_name")}</Label>
              <Input className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm" value={form.name} onChange={e => setForm({...form, name: e.target.value})} data-testid="agent-name-input" />
            </div>
            <div className="space-y-1.5">
              <Label className="text-slate-400 text-xs">{t("agent_description")}</Label>
              <Input className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm" value={form.description} onChange={e => setForm({...form, description: e.target.value})} data-testid="agent-desc-input" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <Label className="text-slate-400 text-xs">{t("agent_model")}</Label>
                <Select value={form.model_type} onValueChange={v => setForm({...form, model_type: v})}>
                  <SelectTrigger className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm" data-testid="agent-model-select"><SelectValue /></SelectTrigger>
                  <SelectContent className="bg-slate-900 border-slate-800">
                    {["GPT-5.2", "GPT-4o", "Claude-Sonnet", "Gemini-3", "Llama-4", "Custom"].map(m => <SelectItem key={m} value={m}>{m}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1.5">
                <Label className="text-slate-400 text-xs">{t("agent_risk")}</Label>
                <Select value={form.risk_level} onValueChange={v => setForm({...form, risk_level: v})}>
                  <SelectTrigger className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm" data-testid="agent-risk-select"><SelectValue /></SelectTrigger>
                  <SelectContent className="bg-slate-900 border-slate-800">
                    {["low", "medium", "high", "critical"].map(r => <SelectItem key={r} value={r} className="capitalize">{r}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <Label className="text-slate-400 text-xs">{t("agent_status")}</Label>
                <Select value={form.status} onValueChange={v => setForm({...form, status: v})}>
                  <SelectTrigger className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm" data-testid="agent-status-select"><SelectValue /></SelectTrigger>
                  <SelectContent className="bg-slate-900 border-slate-800">
                    {["active", "suspended", "inactive"].map(s => <SelectItem key={s} value={s} className="capitalize">{s}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1.5">
                <Label className="text-slate-400 text-xs">{t("agent_data_class")}</Label>
                <Select value={form.data_classification} onValueChange={v => setForm({...form, data_classification: v})}>
                  <SelectTrigger className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm"><SelectValue /></SelectTrigger>
                  <SelectContent className="bg-slate-900 border-slate-800">
                    {["public", "internal", "confidential", "restricted"].map(d => <SelectItem key={d} value={d} className="capitalize">{d}</SelectItem>)}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="space-y-1.5">
              <Label className="text-slate-400 text-xs">{t("agent_owner")}</Label>
              <Input className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm" value={form.owner} onChange={e => setForm({...form, owner: e.target.value})} data-testid="agent-owner-input" />
            </div>
            <div className="space-y-1.5">
              <Label className="text-slate-400 text-xs">{t("agent_actions")} (comma separated)</Label>
              <Input className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm font-mono text-xs" value={actionsInput} onChange={e => setActionsInput(e.target.value)} placeholder="read_data, create_ticket, send_email" data-testid="agent-actions-input" />
            </div>
            <div className="space-y-1.5">
              <Label className="text-slate-400 text-xs">{t("agent_restricted")} (comma separated)</Label>
              <Input className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm font-mono text-xs" value={domainsInput} onChange={e => setDomainsInput(e.target.value)} placeholder="financial_data, medical_records" data-testid="agent-domains-input" />
            </div>
            <div className="flex justify-end gap-2 pt-2">
              <Button variant="ghost" onClick={() => setOpen(false)} className="text-slate-400 rounded-sm" data-testid="agent-cancel-btn">{t("cancel")}</Button>
              <Button onClick={handleSave} className="bg-blue-600 hover:bg-blue-500 text-white rounded-sm" data-testid="agent-save-btn">{t("save")}</Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
