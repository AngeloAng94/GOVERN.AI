import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";
import { Shield, Zap } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

/**
 * Small badge shown in the sidebar telling which AI provider is active.
 * Listens to the global "ai-mode-changed" event dispatched by SettingsPage.
 */
export default function AIModeBadge({ collapsed = false }) {
  const [state, setState] = useState(null);

  const fetchState = useCallback(async () => {
    try {
      const res = await axios.get(`${API}/settings/ai-mode`);
      setState(res.data);
    } catch (_e) {
      // silent
    }
  }, []);

  useEffect(() => {
    fetchState();
    const handler = (e) => setState(e.detail);
    window.addEventListener("ai-mode-changed", handler);
    return () => window.removeEventListener("ai-mode-changed", handler);
  }, [fetchState]);

  if (!state) return null;

  const sovereign = state.current_provider === "sovereign";

  if (collapsed) {
    return (
      <div className="flex justify-center" title={sovereign ? "Sovereign Mode (Apertus)" : "Performance Mode (GPT-4o)"}
           data-testid="ai-mode-badge-collapsed">
        {sovereign
          ? <Shield className="w-4 h-4 text-emerald-400" />
          : <Zap className="w-4 h-4 text-blue-400" />}
      </div>
    );
  }

  return sovereign ? (
    <Badge className="bg-emerald-950/40 text-emerald-300 border border-emerald-800/60 text-[10px] px-1.5 py-0 gap-1"
           data-testid="ai-mode-badge">
      <Shield className="w-3 h-3" /> Sovereign
    </Badge>
  ) : (
    <Badge className="bg-blue-950/40 text-blue-300 border border-blue-800/60 text-[10px] px-1.5 py-0 gap-1"
           data-testid="ai-mode-badge">
      <Zap className="w-3 h-3" /> Performance
    </Badge>
  );
}
