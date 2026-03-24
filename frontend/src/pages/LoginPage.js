import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { useLanguage } from "@/contexts/LanguageContext";
import { Loader2, AlertCircle, Globe } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import Logo from "@/components/Logo";

export default function LoginPage() {
  const { login } = useAuth();
  const { t, lang, toggleLang } = useLanguage();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || (lang === "it" ? "Credenziali non valide" : "Invalid credentials"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#020617] flex items-center justify-center p-4 relative" data-testid="login-page">
      <div className="absolute inset-0 grid-texture opacity-20" />
      <div className="absolute inset-0 hero-glow" />

      <Button
        variant="ghost" size="sm" onClick={toggleLang}
        className="absolute top-4 right-4 text-slate-400 hover:text-white gap-1.5 z-10"
        data-testid="lang-toggle-login"
      >
        <Globe className="w-4 h-4" /> {lang.toUpperCase()}
      </Button>

      <Card className="relative w-full max-w-sm bg-slate-900/60 backdrop-blur-xl border-slate-800 rounded-sm" data-testid="login-card">
        <CardContent className="p-8">
          {/* Logo */}
          <div className="flex justify-center mb-6">
            <Logo size="lg" variant="full" showTagline={true} />
          </div>

          <p className="text-xs font-mono text-center text-slate-500 uppercase tracking-widest mb-6">
            {lang === "it" ? "Accesso al Control Plane" : "Control Plane Access"}
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-1.5">
              <Label className="text-slate-400 text-xs">Username</Label>
              <Input
                className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                value={username}
                onChange={e => setUsername(e.target.value)}
                autoComplete="username"
                data-testid="login-username-input"
              />
            </div>
            <div className="space-y-1.5">
              <Label className="text-slate-400 text-xs">Password</Label>
              <Input
                type="password"
                className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                value={password}
                onChange={e => setPassword(e.target.value)}
                autoComplete="current-password"
                data-testid="login-password-input"
              />
            </div>

            {error && (
              <div className="flex items-center gap-2 text-red-400 text-xs bg-red-950/30 border border-red-900/50 rounded-sm p-2.5" data-testid="login-error">
                <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                {error}
              </div>
            )}

            <Button
              type="submit"
              disabled={loading || !username || !password}
              className="w-full bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_15px_rgba(59,130,246,0.3)] rounded-sm"
              data-testid="login-submit-btn"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : (lang === "it" ? "Accedi" : "Sign In")}
            </Button>
          </form>

          <p className="text-[10px] font-mono text-center text-slate-700 mt-6">
            ANTHERA Systems &copy; 2026
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
