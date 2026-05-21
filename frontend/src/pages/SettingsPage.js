import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";
import { Shield, Zap, AlertTriangle, CheckCircle2, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { useLanguage } from "@/contexts/LanguageContext";
import { useAuth } from "@/contexts/AuthContext";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function SettingsPage() {
  const { lang } = useLanguage();
  const { user } = useAuth();
  const isAdmin = user?.role === "admin";

  const [state, setState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const tr = (it, en) => (lang === "it" ? it : en);

  const fetchState = useCallback(async () => {
    try {
      const res = await axios.get(`${API}/settings/ai-mode`);
      setState(res.data);
    } catch (e) {
      toast.error(tr("Errore caricamento impostazioni AI", "Failed to load AI settings"));
    } finally {
      setLoading(false);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lang]);

  useEffect(() => { fetchState(); }, [fetchState]);

  const setMode = async (sovereign) => {
    if (!isAdmin) return;
    setSaving(true);
    try {
      const res = await axios.post(`${API}/settings/ai-mode`, { sovereign_mode: sovereign });
      setState(res.data);
      // Notify other parts of the app (sidebar badge)
      window.dispatchEvent(new CustomEvent("ai-mode-changed", { detail: res.data }));
      toast.success(sovereign
        ? tr("Sovereign Mode attivato", "Sovereign Mode enabled")
        : tr("Performance Mode attivato", "Performance Mode enabled"));
    } catch (e) {
      toast.error(tr("Errore aggiornamento", "Update failed"));
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64" data-testid="settings-loading">
        <Loader2 className="w-6 h-6 animate-spin text-slate-500" />
      </div>
    );
  }

  const sovereignActive = state?.current_provider === "sovereign";
  const sovereignRequestedButNotConfigured = state?.sovereign_mode && !state?.sovereign_configured;

  return (
    <div className="max-w-3xl mx-auto" data-testid="settings-page">
      <div className="mb-8">
        <h1 className="text-2xl font-semibold text-white mb-1" data-testid="settings-title">
          {tr("Impostazioni", "Settings")}
        </h1>
        <p className="text-sm text-slate-400">
          {tr("Configura il provider AI utilizzato da ARIA e dal motore di guidance.",
              "Configure the AI provider used by ARIA and the guidance engine.")}
        </p>
      </div>

      <section className="bg-slate-900/40 border border-slate-800 rounded-lg p-6" data-testid="ai-provider-section">
        <div className="flex items-start justify-between mb-5">
          <div>
            <h2 className="text-base font-semibold text-white">{tr("Provider AI", "AI Provider")}</h2>
            <p className="text-xs text-slate-500 mt-1">
              {tr("La modalita sceglie tra LLM sovrano europeo e LLM ad alte prestazioni.",
                  "Mode selects between a sovereign European LLM and a high-performance LLM.")}
            </p>
          </div>
          {sovereignActive ? (
            <Badge className="bg-emerald-950/40 text-emerald-300 border border-emerald-800/60" data-testid="current-mode-badge">
              <Shield className="w-3 h-3 mr-1" /> Sovereign
            </Badge>
          ) : (
            <Badge className="bg-blue-950/40 text-blue-300 border border-blue-800/60" data-testid="current-mode-badge">
              <Zap className="w-3 h-3 mr-1" /> Performance
            </Badge>
          )}
        </div>

        {sovereignRequestedButNotConfigured && (
          <div className="mb-5 flex items-start gap-2 p-3 rounded-md border border-amber-900/50 bg-amber-950/20 text-amber-200 text-xs" data-testid="sovereign-warning">
            <AlertTriangle className="w-4 h-4 mt-0.5 flex-shrink-0" />
            <span>
              {tr("Sovereign Mode richiesto ma PUBLICAI_API_KEY non configurata. ARIA continua a usare GPT-4o come fallback automatico.",
                  "Sovereign Mode requested but PUBLICAI_API_KEY is not configured. ARIA keeps using GPT-4o as automatic fallback.")}
            </span>
          </div>
        )}

        <div className="space-y-3">
          {/* Sovereign card */}
          <button
            type="button"
            onClick={() => setMode(true)}
            disabled={!isAdmin || saving}
            className={`w-full text-left p-4 rounded-md border transition-all
              ${state?.sovereign_mode
                ? "border-emerald-700/70 bg-emerald-950/20"
                : "border-slate-800 bg-slate-900/30 hover:border-slate-700"}
              ${!isAdmin || saving ? "opacity-60 cursor-not-allowed" : "cursor-pointer"}`}
            data-testid="sovereign-mode-card"
          >
            <div className="flex items-start gap-3">
              <div className={`mt-0.5 w-4 h-4 rounded-full border-2 flex-shrink-0
                ${state?.sovereign_mode ? "border-emerald-400 bg-emerald-400" : "border-slate-600"}`}
                data-testid="sovereign-mode-radio"
              >
                {state?.sovereign_mode && <CheckCircle2 className="w-3 h-3 text-emerald-950 -mt-0.5 -ml-0.5" />}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <Shield className="w-4 h-4 text-emerald-400" />
                  <span className="text-sm font-semibold text-white">
                    {tr("Sovereign Mode", "Sovereign Mode")}
                  </span>
                  <Badge className="bg-emerald-950/40 text-emerald-300 border border-emerald-800/60 text-[10px] px-1.5 py-0">
                    Apertus 70B
                  </Badge>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  {tr("Dati europei, AI svizzera, licenza Apache 2.0. Sviluppato da ETH Zurich, EPFL, CSCS. Conforme EU AI Act Art. 13/53, GDPR, DORA, NIS2 by design.",
                      "European data, Swiss AI, Apache 2.0 licensed. Built by ETH Zurich, EPFL, CSCS. EU AI Act Art. 13/53, GDPR, DORA, NIS2 compliant by design.")}
                </p>
              </div>
            </div>
          </button>

          {/* Performance card */}
          <button
            type="button"
            onClick={() => setMode(false)}
            disabled={!isAdmin || saving}
            className={`w-full text-left p-4 rounded-md border transition-all
              ${!state?.sovereign_mode
                ? "border-blue-700/70 bg-blue-950/20"
                : "border-slate-800 bg-slate-900/30 hover:border-slate-700"}
              ${!isAdmin || saving ? "opacity-60 cursor-not-allowed" : "cursor-pointer"}`}
            data-testid="performance-mode-card"
          >
            <div className="flex items-start gap-3">
              <div className={`mt-0.5 w-4 h-4 rounded-full border-2 flex-shrink-0
                ${!state?.sovereign_mode ? "border-blue-400 bg-blue-400" : "border-slate-600"}`}
                data-testid="performance-mode-radio"
              >
                {!state?.sovereign_mode && <CheckCircle2 className="w-3 h-3 text-blue-950 -mt-0.5 -ml-0.5" />}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <Zap className="w-4 h-4 text-blue-400" />
                  <span className="text-sm font-semibold text-white">
                    {tr("Performance Mode", "Performance Mode")}
                  </span>
                  <Badge className="bg-blue-950/40 text-blue-300 border border-blue-800/60 text-[10px] px-1.5 py-0">
                    GPT-4o
                  </Badge>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  {tr("Capacita di reasoning massima per task complessi. Provider: OpenAI (US). Usato anche come fallback automatico se Sovereign fallisce.",
                      "Maximum reasoning capacity for complex tasks. Provider: OpenAI (US). Also used as automatic fallback if Sovereign fails.")}
                </p>
              </div>
            </div>
          </button>
        </div>

        <div className="mt-5 pt-4 border-t border-slate-800 text-xs text-slate-500 space-y-1" data-testid="current-config">
          <div className="flex justify-between">
            <span>{tr("Modello attuale", "Current model")}</span>
            <span className="font-mono text-slate-300">{state?.current_model}</span>
          </div>
          <div className="flex justify-between">
            <span>{tr("Provider attivo", "Active provider")}</span>
            <span className="text-slate-300 capitalize">{state?.current_provider}</span>
          </div>
          {!isAdmin && (
            <div className="mt-3 text-amber-400/80 text-[11px]">
              {tr("Solo gli amministratori possono modificare la modalita AI.",
                  "Only admins can change the AI mode.")}
            </div>
          )}
        </div>
      </section>

      <p className="text-[11px] text-slate-600 mt-6 text-center italic">
        {tr("ANTHERA Systems - European data deserves European AI.",
            "ANTHERA Systems - European data deserves European AI.")}
      </p>
    </div>
  );
}
