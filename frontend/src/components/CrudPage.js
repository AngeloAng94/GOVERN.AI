import React, { useEffect, useState, useMemo } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { Plus, Pencil, Trash2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { toast } from "sonner";
import axios from "axios";
import EmptyState from "@/components/EmptyState";
import SkeletonLoader from "@/components/SkeletonLoader";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

/**
 * CrudPage - Generic CRUD component for Agents and Policies
 * 
 * Props:
 * - entityName: string (e.g., "agents", "policies")
 * - entityLabel: string (translation key for display)
 * - icon: React component
 * - iconColor: string (Tailwind classes for icon background)
 * - fields: array of field definitions
 * - emptyForm: object with default form values
 * - renderCard: function(item, { onEdit, onDelete, t }) => JSX
 * - listLayout: "grid" | "list"
 * - testIdPrefix: string for data-testid
 */
export default function CrudPage({
  entityName,
  entityLabel,
  titleKey,
  subtitleKey,
  newButtonKey,
  icon: Icon,
  iconColor = "bg-blue-500/10",
  iconTextColor = "text-blue-400",
  fields,
  emptyForm,
  renderCard,
  listLayout = "grid",
  testIdPrefix,
  emptyStateProps,
}) {
  const { t } = useLanguage();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ ...emptyForm });
  const [arrayInputs, setArrayInputs] = useState({});

  // Initialize array inputs from emptyForm
  useEffect(() => {
    const initArrayInputs = {};
    fields.forEach(f => {
      if (f.type === "array") {
        initArrayInputs[f.name] = "";
      }
    });
    setArrayInputs(initArrayInputs);
  }, [fields]);

  const fetchItems = () => {
    setLoading(true);
    axios.get(`${API}/${entityName}`)
      .then(res => setItems(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchItems(); }, [entityName]);

  const openCreate = () => {
    setEditing(null);
    setForm({ ...emptyForm });
    const resetArrayInputs = {};
    fields.forEach(f => {
      if (f.type === "array") {
        resetArrayInputs[f.name] = "";
      }
    });
    setArrayInputs(resetArrayInputs);
    setOpen(true);
  };

  const openEdit = (item) => {
    setEditing(item);
    const newForm = { ...emptyForm };
    const newArrayInputs = {};
    
    fields.forEach(f => {
      if (f.type === "array") {
        newForm[f.name] = item[f.name] || [];
        newArrayInputs[f.name] = (item[f.name] || []).join(", ");
      } else {
        newForm[f.name] = item[f.name] ?? emptyForm[f.name];
      }
    });
    
    setForm(newForm);
    setArrayInputs(newArrayInputs);
    setOpen(true);
  };

  const handleSave = async () => {
    const payload = { ...form };
    
    // Convert array inputs
    fields.forEach(f => {
      if (f.type === "array") {
        payload[f.name] = arrayInputs[f.name]
          .split(",")
          .map(s => s.trim())
          .filter(Boolean);
      }
    });

    try {
      if (editing) {
        await axios.put(`${API}/${entityName}/${editing.id}`, payload);
        toast.success(t("updated") || "Updated successfully");
      } else {
        await axios.post(`${API}/${entityName}`, payload);
        toast.success(t("created") || "Created successfully");
      }
      setOpen(false);
      fetchItems();
    } catch (e) {
      toast.error(t("error_saving") || "Error saving");
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API}/${entityName}/${id}`);
      toast.success(t("deleted") || "Deleted successfully");
      fetchItems();
    } catch (e) {
      toast.error(t("error_deleting") || "Error deleting");
    }
  };

  const updateField = (fieldName, value) => {
    setForm(prev => ({ ...prev, [fieldName]: value }));
  };

  const updateArrayInput = (fieldName, value) => {
    setArrayInputs(prev => ({ ...prev, [fieldName]: value }));
  };

  const renderField = (field) => {
    switch (field.type) {
      case "select":
        return (
          <div key={field.name} className="space-y-1.5">
            <Label className="text-slate-400 text-xs">{t(field.label) || field.label}</Label>
            <Select value={form[field.name]} onValueChange={v => updateField(field.name, v)}>
              <SelectTrigger className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm" data-testid={`${testIdPrefix}-${field.name}-select`}>
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-900 border-slate-800">
                {field.options.map(opt => (
                  <SelectItem key={opt.value} value={opt.value} className="capitalize">
                    {opt.label || opt.value}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        );
      
      case "array":
        return (
          <div key={field.name} className="space-y-1.5">
            <Label className="text-slate-400 text-xs">{t(field.label) || field.label} (comma separated)</Label>
            <Input
              className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm font-mono text-xs"
              value={arrayInputs[field.name] || ""}
              onChange={e => updateArrayInput(field.name, e.target.value)}
              placeholder={field.placeholder}
              data-testid={`${testIdPrefix}-${field.name}-input`}
            />
          </div>
        );
      
      default: // text
        return (
          <div key={field.name} className="space-y-1.5">
            <Label className="text-slate-400 text-xs">{t(field.label) || field.label}</Label>
            <Input
              className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm"
              value={form[field.name] || ""}
              onChange={e => updateField(field.name, e.target.value)}
              placeholder={field.placeholder}
              data-testid={`${testIdPrefix}-${field.name}-input`}
            />
          </div>
        );
    }
  };

  // Group fields for two-column layout
  const groupedFields = useMemo(() => {
    const result = [];
    let currentGroup = [];
    
    fields.forEach((field, index) => {
      if (field.fullWidth || field.type === "array") {
        if (currentGroup.length > 0) {
          result.push({ type: "row", fields: currentGroup });
          currentGroup = [];
        }
        result.push({ type: "full", field });
      } else {
        currentGroup.push(field);
        if (currentGroup.length === 2) {
          result.push({ type: "row", fields: currentGroup });
          currentGroup = [];
        }
      }
    });
    
    if (currentGroup.length > 0) {
      result.push({ type: "row", fields: currentGroup });
    }
    
    return result;
  }, [fields]);

  return (
    <div className="space-y-6" data-testid={`${testIdPrefix}-page`}>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-['Space_Grotesk'] text-2xl font-bold tracking-tight text-white">
            {t(titleKey)}
          </h1>
          <p className="text-sm text-slate-500 mt-1">{t(subtitleKey)}</p>
        </div>
        <Button
          onClick={openCreate}
          className="bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_15px_rgba(59,130,246,0.3)] rounded-sm gap-2"
          data-testid={`new-${testIdPrefix}-btn`}
        >
          <Plus className="w-4 h-4" />
          {t(newButtonKey)}
        </Button>
      </div>

      {loading ? (
        <SkeletonLoader rows={listLayout === "grid" ? 6 : 5} type={listLayout === "grid" ? "card" : "table"} />
      ) : items.length === 0 ? (
        emptyStateProps ? (
          <EmptyState
            icon={emptyStateProps.icon}
            title={emptyStateProps.title}
            subtitle={emptyStateProps.subtitle}
            action={emptyStateProps.action ? { label: emptyStateProps.action, onClick: openCreate } : undefined}
          />
        ) : (
          <Card className="bg-slate-900/40 border-slate-800 rounded-sm">
            <CardContent className="p-12 text-center text-slate-500">
              {t("no_data")}
            </CardContent>
          </Card>
        )
      ) : (
        <div
          className={listLayout === "grid" ? "grid grid-cols-1 lg:grid-cols-2 gap-4" : "space-y-3"}
          data-testid={`${testIdPrefix}-list`}
        >
          {items.map((item) => renderCard(item, {
            onEdit: () => openEdit(item),
            onDelete: () => handleDelete(item.id),
            t,
            Icon,
            iconColor,
            iconTextColor
          }))}
        </div>
      )}

      {/* Create/Edit Dialog */}
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="bg-slate-900 border-slate-800 rounded-sm max-w-lg" data-testid={`${testIdPrefix}-dialog`}>
          <DialogHeader>
            <DialogTitle className="font-['Space_Grotesk'] text-white">
              {editing ? t("edit") : t("create")} {t(entityLabel)}
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4 mt-2">
            {groupedFields.map((group, idx) => {
              if (group.type === "full") {
                return renderField(group.field);
              }
              return (
                <div key={idx} className={group.fields.length === 2 ? "grid grid-cols-2 gap-3" : ""}>
                  {group.fields.map(f => renderField(f))}
                </div>
              );
            })}
            <div className="flex justify-end gap-2 pt-2">
              <Button
                variant="ghost"
                onClick={() => setOpen(false)}
                className="text-slate-400 rounded-sm"
                data-testid={`${testIdPrefix}-cancel-btn`}
              >
                {t("cancel")}
              </Button>
              <Button
                onClick={handleSave}
                className="bg-blue-600 hover:bg-blue-500 text-white rounded-sm"
                data-testid={`${testIdPrefix}-save-btn`}
              >
                {t("save")}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}

// Export helper components for card rendering
export const CrudCardActions = ({ onEdit, onDelete, testIdPrefix, itemId }) => (
  <div className="flex items-center gap-1 shrink-0">
    <Button
      variant="ghost"
      size="icon"
      className="h-8 w-8 text-slate-500 hover:text-white"
      onClick={onEdit}
      data-testid={`edit-${testIdPrefix}-${itemId}`}
    >
      <Pencil className="w-3.5 h-3.5" />
    </Button>
    <Button
      variant="ghost"
      size="icon"
      className="h-8 w-8 text-slate-500 hover:text-red-400"
      onClick={onDelete}
      data-testid={`delete-${testIdPrefix}-${itemId}`}
    >
      <Trash2 className="w-3.5 h-3.5" />
    </Button>
  </div>
);
