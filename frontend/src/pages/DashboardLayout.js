import React from "react";
import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useLanguage } from "@/contexts/LanguageContext";
import { Shield, LayoutDashboard, Bot, FileText, Activity, CheckCircle, MessageSquare, Globe, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

const navItems = [
  { path: "/dashboard", icon: LayoutDashboard, labelKey: "sidebar_overview", end: true },
  { path: "/dashboard/agents", icon: Bot, labelKey: "sidebar_agents" },
  { path: "/dashboard/policies", icon: FileText, labelKey: "sidebar_policies" },
  { path: "/dashboard/audit", icon: Activity, labelKey: "sidebar_audit" },
  { path: "/dashboard/compliance", icon: CheckCircle, labelKey: "sidebar_compliance" },
  { path: "/dashboard/assistant", icon: MessageSquare, labelKey: "sidebar_assistant" },
];

export default function DashboardLayout() {
  const { t, lang, toggleLang } = useLanguage();
  const navigate = useNavigate();

  return (
    <div className="w-full h-screen flex overflow-hidden bg-[#020617]" data-testid="dashboard-layout">
      {/* Sidebar */}
      <aside className="w-64 flex-shrink-0 border-r border-slate-800 bg-[#020617] flex flex-col" data-testid="dashboard-sidebar">
        <div className="h-16 flex items-center gap-3 px-5 border-b border-slate-800">
          <Shield className="w-6 h-6 text-blue-500" />
          <span className="font-['Space_Grotesk'] text-lg font-bold tracking-tight">GOVERN<span className="text-blue-500">.AI</span></span>
        </div>
        <ScrollArea className="flex-1 py-4">
          <nav className="space-y-1 px-3">
            {navItems.map(({ path, icon: Icon, labelKey, end }) => (
              <NavLink
                key={path}
                to={path}
                end={end}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-sm text-sm font-medium transition-colors duration-200 ${
                    isActive
                      ? "bg-blue-600/15 text-blue-400 border-l-2 border-blue-500"
                      : "text-slate-400 hover:text-white hover:bg-slate-800/50 border-l-2 border-transparent"
                  }`
                }
                data-testid={`nav-${labelKey}`}
              >
                <Icon className="w-4 h-4" />
                {t(labelKey)}
              </NavLink>
            ))}
          </nav>
        </ScrollArea>
        <div className="p-3 border-t border-slate-800 space-y-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleLang}
            className="w-full justify-start text-slate-400 hover:text-white gap-2"
            data-testid="lang-toggle-dashboard"
          >
            <Globe className="w-4 h-4" />
            {t("language")}: {lang.toUpperCase()}
          </Button>
          <Separator className="bg-slate-800" />
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate("/")}
            className="w-full justify-start text-slate-500 hover:text-white gap-2"
            data-testid="back-to-site-btn"
          >
            <ArrowLeft className="w-4 h-4" />
            {t("back_to_site")}
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto bg-[#020617] p-6" data-testid="dashboard-main">
        <Outlet />
      </main>
    </div>
  );
}
