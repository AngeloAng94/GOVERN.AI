import React from "react";
import { Bot } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import CrudPage, { CrudCardActions } from "@/components/CrudPage";

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
  name: "",
  description: "",
  model_type: "GPT-5.2",
  risk_level: "medium",
  status: "active",
  allowed_actions: [],
  restricted_domains: [],
  data_classification: "internal",
  owner: ""
};

const fields = [
  { name: "name", label: "agent_name", type: "text", fullWidth: true },
  { name: "description", label: "agent_description", type: "text", fullWidth: true },
  { 
    name: "model_type", 
    label: "agent_model", 
    type: "select",
    options: [
      { value: "GPT-5.2" },
      { value: "GPT-4o" },
      { value: "Claude-Sonnet" },
      { value: "Gemini-3" },
      { value: "Llama-4" },
      { value: "Custom" }
    ]
  },
  { 
    name: "risk_level", 
    label: "agent_risk", 
    type: "select",
    options: [
      { value: "low" },
      { value: "medium" },
      { value: "high" },
      { value: "critical" }
    ]
  },
  { 
    name: "status", 
    label: "agent_status", 
    type: "select",
    options: [
      { value: "active" },
      { value: "suspended" },
      { value: "inactive" }
    ]
  },
  { 
    name: "data_classification", 
    label: "agent_data_class", 
    type: "select",
    options: [
      { value: "public" },
      { value: "internal" },
      { value: "confidential" },
      { value: "restricted" }
    ]
  },
  { name: "owner", label: "agent_owner", type: "text", fullWidth: true },
  { 
    name: "allowed_actions", 
    label: "agent_actions", 
    type: "array",
    placeholder: "read_data, create_ticket, send_email"
  },
  { 
    name: "restricted_domains", 
    label: "agent_restricted", 
    type: "array",
    placeholder: "financial_data, medical_records"
  }
];

const renderAgentCard = (agent, { onEdit, onDelete, t }) => (
  <Card
    key={agent.id}
    className="bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm hover:border-slate-700 transition-colors duration-300"
    data-testid={`agent-card-${agent.id}`}
  >
    <CardHeader className="pb-2">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-sm bg-blue-500/10 flex items-center justify-center">
            <Bot className="w-4 h-4 text-blue-400" />
          </div>
          <div>
            <CardTitle className="font-['Space_Grotesk'] text-base font-semibold text-white">
              {agent.name}
            </CardTitle>
            <p className="text-xs text-slate-500 font-mono">{agent.model_type}</p>
          </div>
        </div>
        <CrudCardActions 
          onEdit={onEdit} 
          onDelete={onDelete} 
          testIdPrefix="agent"
          itemId={agent.id}
        />
      </div>
    </CardHeader>
    <CardContent className="pt-0">
      <p className="text-sm text-slate-400 mb-3">{agent.description}</p>
      <div className="flex flex-wrap gap-2 mb-3">
        <Badge className={`${statusBadge[agent.status]} border text-[10px]`}>
          {agent.status}
        </Badge>
        <Badge className={`${riskBadge[agent.risk_level]} border text-[10px]`}>
          {agent.risk_level} risk
        </Badge>
        <Badge className="bg-slate-800/50 text-slate-400 border-slate-700 border text-[10px]">
          {agent.data_classification}
        </Badge>
      </div>
      {agent.owner && (
        <p className="text-xs text-slate-600 font-mono">
          {t("agent_owner")}: {agent.owner}
        </p>
      )}
    </CardContent>
  </Card>
);

export default function AgentsPage() {
  return (
    <CrudPage
      entityName="agents"
      entityLabel="sidebar_agents"
      titleKey="agents_title"
      subtitleKey="agents_subtitle"
      newButtonKey="new_agent"
      icon={Bot}
      iconColor="bg-blue-500/10"
      iconTextColor="text-blue-400"
      fields={fields}
      emptyForm={emptyForm}
      renderCard={renderAgentCard}
      listLayout="grid"
      testIdPrefix="agent"
    />
  );
}
