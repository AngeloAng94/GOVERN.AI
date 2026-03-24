import React from "react";
import { useNavigate } from "react-router-dom";
import { useLanguage } from "@/contexts/LanguageContext";
import { Activity, FileText, Link2, AlertTriangle, MessageSquare, Building2, Landmark, Heart, Zap, Phone, ChevronRight, Globe, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import Logo from "@/components/Logo";

const features = [
  { key: "policy", icon: Shield, color: "text-blue-400", border: "border-blue-500/30", bg: "bg-blue-500/10", span: "col-span-2" },
  { key: "audit", icon: Activity, color: "text-amber-400", border: "border-amber-500/30", bg: "bg-amber-500/10", span: "col-span-1" },
  { key: "compliance", icon: FileText, color: "text-emerald-400", border: "border-emerald-500/30", bg: "bg-emerald-500/10", span: "col-span-1" },
  { key: "integration", icon: Link2, color: "text-violet-400", border: "border-violet-500/30", bg: "bg-violet-500/10", span: "col-span-1" },
  { key: "risk", icon: AlertTriangle, color: "text-red-400", border: "border-red-500/30", bg: "bg-red-500/10", span: "col-span-1" },
  { key: "ai", icon: MessageSquare, color: "text-cyan-400", border: "border-cyan-500/30", bg: "bg-cyan-500/10", span: "col-span-2" },
];

const clients = [
  { key: "pa", icon: Landmark },
  { key: "bank", icon: Building2 },
  { key: "insurance", icon: Shield },
  { key: "health", icon: Heart },
  { key: "energy", icon: Zap },
  { key: "telecom", icon: Phone },
];

export default function LandingPage() {
  const navigate = useNavigate();
  const { t, lang, toggleLang } = useLanguage();

  return (
    <div className="min-h-screen bg-[#020617] text-slate-100" data-testid="landing-page">
      {/* Nav */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-slate-800/60 bg-[#020617]/80 backdrop-blur-xl" data-testid="landing-nav">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Logo size="md" variant="full" />
          <div className="hidden md:flex items-center gap-8">
            <a href="#features" className="text-sm text-slate-400 hover:text-white transition-colors duration-200">{t("nav_features")}</a>
            <a href="#clients" className="text-sm text-slate-400 hover:text-white transition-colors duration-200">{t("nav_clients")}</a>
            <a href="#compliance" className="text-sm text-slate-400 hover:text-white transition-colors duration-200">{t("nav_compliance")}</a>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm" onClick={toggleLang} className="text-slate-400 hover:text-white gap-1.5" data-testid="lang-toggle-landing">
              <Globe className="w-4 h-4" />
              {lang.toUpperCase()}
            </Button>
            <Button onClick={() => navigate("/dashboard")} className="bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_15px_rgba(59,130,246,0.3)] rounded-sm text-sm px-5" data-testid="nav-dashboard-btn">
              {t("nav_dashboard")}
              <ChevronRight className="w-4 h-4 ml-1" />
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative pt-32 pb-24 overflow-hidden" data-testid="hero-section">
        <div className="absolute inset-0 grid-texture opacity-40" />
        <div className="absolute inset-0 hero-glow" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl">
            {/* Logo in Hero */}
            <div className="mb-8 animate-fade-up">
              <Logo size="lg" variant="full" showTagline={true} />
            </div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-blue-500/30 bg-blue-500/10 text-blue-400 text-xs font-mono uppercase tracking-widest mb-8 animate-fade-up animate-delay-100">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse-glow" />
              Compliance-First AI Governance
            </div>
            <h1 className="font-['Space_Grotesk'] text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.1] mb-6 animate-fade-up animate-delay-200" data-testid="hero-title">
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">{t("hero_title")}</span>
            </h1>
            <p className="text-lg md:text-xl text-slate-400 leading-relaxed max-w-2xl mb-10 animate-fade-up animate-delay-300" data-testid="hero-subtitle">
              {t("hero_subtitle")}
            </p>
            <div className="flex flex-wrap gap-4 animate-fade-up animate-delay-400">
              <Button
                onClick={() => navigate("/dashboard")}
                className="bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_20px_rgba(59,130,246,0.4)] rounded-sm text-base px-8 py-3 h-auto font-medium"
                data-testid="hero-cta-btn"
              >
                {t("hero_cta")}
                <ChevronRight className="w-5 h-5 ml-2" />
              </Button>
              <Button
                variant="outline"
                onClick={() => document.getElementById("features")?.scrollIntoView({ behavior: "smooth" })}
                className="border-slate-700 hover:border-slate-600 text-slate-300 hover:text-white bg-slate-800/50 rounded-sm text-base px-8 py-3 h-auto font-medium"
                data-testid="hero-secondary-btn"
              >
                {t("hero_cta_secondary")}
              </Button>
            </div>
          </div>
          {/* Stats bar */}
          <div className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-6 animate-fade-up animate-delay-500">
            {[
              { value: "99.9%", label: "Uptime SLA" },
              { value: "< 50ms", label: "Policy Evaluation" },
              { value: "6", label: lang === "it" ? "Normative Coperte" : "Regulations Covered" },
              { value: "100%", label: lang === "it" ? "Tracciabilita Audit" : "Audit Traceability" },
            ].map((stat, i) => (
              <div key={i} className="glass-card rounded-sm p-5 text-center">
                <div className="font-['Space_Grotesk'] text-2xl font-bold text-white">{stat.value}</div>
                <div className="text-xs text-slate-500 font-mono uppercase tracking-wider mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Bento Grid */}
      <section id="features" className="py-24" data-testid="features-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-16">
            <p className="text-xs font-mono uppercase tracking-widest text-blue-400 mb-3">{lang === "it" ? "Funzionalita" : "Capabilities"}</p>
            <h2 className="font-['Space_Grotesk'] text-3xl md:text-5xl font-semibold tracking-tight text-white mb-4">{t("features_title")}</h2>
            <p className="text-base md:text-lg text-slate-400 max-w-xl">{t("features_subtitle")}</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {features.map(({ key, icon: Icon, color, border, bg, span }) => (
              <div
                key={key}
                className={`group relative overflow-hidden glass-card rounded-sm p-6 hover:border-blue-500/40 transition-colors duration-500 cursor-default ${span} md:${span}`}
                data-testid={`feature-${key}`}
              >
                <div className={`inline-flex items-center justify-center w-10 h-10 rounded-sm ${bg} ${border} border mb-4`}>
                  <Icon className={`w-5 h-5 ${color}`} />
                </div>
                <h3 className="font-['Space_Grotesk'] text-lg font-semibold text-white mb-2">{t(`feat_${key}`)}</h3>
                <p className="text-sm text-slate-400 leading-relaxed">{t(`feat_${key}_desc`)}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Clients */}
      <section id="clients" className="py-24 border-t border-slate-800/60" data-testid="clients-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <p className="text-xs font-mono uppercase tracking-widest text-amber-400 mb-3">{lang === "it" ? "Settori Target" : "Target Sectors"}</p>
            <h2 className="font-['Space_Grotesk'] text-3xl md:text-5xl font-semibold tracking-tight text-white mb-4">{t("clients_title")}</h2>
            <p className="text-base md:text-lg text-slate-400 max-w-xl mx-auto">{t("clients_subtitle")}</p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {clients.map(({ key, icon: Icon }) => (
              <div key={key} className="glass-card rounded-sm p-6 text-center hover:border-slate-600 transition-colors duration-300" data-testid={`client-${key}`}>
                <Icon className="w-8 h-8 text-slate-400 mx-auto mb-3" />
                <p className="text-sm text-slate-300 font-medium">{t(`client_${key}`)}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section id="compliance" className="py-24" data-testid="cta-section">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="relative glass-card rounded-sm p-12 md:p-16 text-center overflow-hidden">
            <div className="absolute inset-0 hero-glow opacity-50" />
            <div className="relative">
              <div className="flex justify-center mb-6">
                <Logo size="lg" variant="icon" />
              </div>
              <h2 className="font-['Space_Grotesk'] text-3xl md:text-5xl font-semibold tracking-tight text-white mb-4">
                {lang === "it" ? "Pronto a governare i tuoi agenti AI?" : "Ready to govern your AI agents?"}
              </h2>
              <p className="text-base md:text-lg text-slate-400 max-w-lg mx-auto mb-8">
                {lang === "it"
                  ? "Inizia a controllare, monitorare e garantire la compliance dei tuoi sistemi AI oggi."
                  : "Start controlling, monitoring and ensuring compliance of your AI systems today."}
              </p>
              <Button
                onClick={() => navigate("/dashboard")}
                className="bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_20px_rgba(59,130,246,0.4)] rounded-sm text-base px-10 py-3 h-auto font-medium"
                data-testid="cta-dashboard-btn"
              >
                {t("hero_cta")}
                <ChevronRight className="w-5 h-5 ml-2" />
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800/60 py-12" data-testid="footer">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <Logo size="sm" variant="full" />
            <p className="text-xs text-slate-600 font-mono">
              {lang === "it" ? "Il control plane sovrano per l'AI enterprise" : "The sovereign control plane for enterprise AI"}
            </p>
            <p className="text-xs text-slate-600">&copy; 2026 GOVERN.AI — {lang === "it" ? "Tutti i diritti riservati" : "All rights reserved"}</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
