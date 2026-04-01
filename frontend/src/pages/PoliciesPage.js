import React from "react";
import { FileText, Shield } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useLanguage } from "@/contexts/LanguageContext";
import CrudPage, { CrudCardActions } from "@/components/CrudPage";

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
  name: "",
  description: "",
  agent_id: "",
  rule_type: "restriction",
  conditions: [],
  actions: [],
  severity: "medium",
  regulation: "GDPR",
  enforcement: "block"
};

const fields = [
  { name: "name", label: "policy_name", type: "text", fullWidth: true },
  { name: "description", label: "policy_description", type: "text", fullWidth: true },
  { 
    name: "rule_type", 
    label: "policy_type", 
    type: "select",
    options: [
      { value: "restriction" },
      { value: "logging" },
      { value: "rate_limit" },
      { value: "approval" },
      { value: "retention" }
    ]
  },
  { 
    name: "severity", 
    label: "policy_severity", 
    type: "select",
    options: [
      { value: "low" },
      { value: "medium" },
      { value: "high" },
      { value: "critical" }
    ]
  },
  { 
    name: "regulation", 
    label: "policy_regulation", 
    type: "select",
    options: [
      { value: "GDPR" },
      { value: "EU-AI-ACT" },
      { value: "ISO-27001" },
      { value: "ISO-42001" },
      { value: "DORA" },
      { value: "NIS2" },
      { value: "SOX" }
    ]
  },
  { 
    name: "enforcement", 
    label: "policy_enforcement", 
    type: "select",
    options: [
      { value: "block" },
      { value: "log" },
      { value: "throttle" },
      { value: "auto" }
    ]
  },
  { 
    name: "conditions", 
    label: "policy_conditions", 
    type: "array",
    placeholder: "data_contains_pii, agent_risk_level_high"
  },
  { 
    name: "actions", 
    label: "policy_actions", 
    type: "array",
    placeholder: "block_access, log_attempt, notify_dpo"
  }
];

const renderPolicyCard = (policy, { onEdit, onDelete, t }) => (
  <Card
    key={policy.id}
    className="bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm hover:border-slate-700 transition-colors duration-300"
    data-testid={`policy-card-${policy.id}`}
  >
    <CardContent className="p-5">
      <div className="flex items-start justify-between">
        <div className="flex items-start gap-3 min-w-0">
          <div className="w-9 h-9 rounded-sm bg-amber-500/10 flex items-center justify-center shrink-0 mt-0.5">
            <FileText className="w-4 h-4 text-amber-400" />
          </div>
          <div className="min-w-0">
            <h3 className="font-['Space_Grotesk'] text-sm font-semibold text-white">
              {policy.name}
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">{policy.description}</p>
            <div className="flex flex-wrap gap-1.5 mt-2">
              <Badge className={`${severityBadge[policy.severity]} border text-[10px]`}>
                {policy.severity}
              </Badge>
              <Badge className="bg-blue-950/30 text-blue-400 border-blue-900/50 border text-[10px]">
                {policy.regulation}
              </Badge>
              <Badge className={`${enforcementBadge[policy.enforcement]} border text-[10px]`}>
                {policy.enforcement}
              </Badge>
              <Badge className="bg-slate-800/50 text-slate-400 border-slate-700 border text-[10px]">
                {policy.rule_type}
              </Badge>
            </div>
            {policy.conditions?.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-2">
                {policy.conditions.map((c, i) => (
                  <span
                    key={i}
                    className="text-[10px] font-mono text-slate-600 bg-slate-800/50 px-1.5 py-0.5 rounded"
                  >
                    {c}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
        <CrudCardActions 
          onEdit={onEdit} 
          onDelete={onDelete} 
          testIdPrefix="policy"
          itemId={policy.id}
        />
      </div>
    </CardContent>
  </Card>
);

export default function PoliciesPage() {
  const { t } = useLanguage();
  return (
    <CrudPage
      entityName="policies"
      entityLabel="sidebar_policies"
      titleKey="policies_title"
      subtitleKey="policies_subtitle"
      newButtonKey="new_policy"
      icon={FileText}
      iconColor="bg-amber-500/10"
      iconTextColor="text-amber-400"
      fields={fields}
      emptyForm={emptyForm}
      renderCard={renderPolicyCard}
      listLayout="list"
      testIdPrefix="policy"
      emptyStateProps={{
        icon: Shield,
        title: t("empty_policies_title"),
        subtitle: t("empty_policies_subtitle"),
        action: t("empty_policies_action"),
      }}
    />
  );
}
