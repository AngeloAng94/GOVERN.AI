import React, { useState, useEffect } from "react";
import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useLanguage } from "@/contexts/LanguageContext";
import { useAuth } from "@/contexts/AuthContext";
import { LayoutDashboard, Bot, FileText, Activity, CheckCircle, MessageSquare, Globe, ArrowLeft, LogOut, User, Menu, X, ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import Logo from "@/components/Logo";

const navItems = [
  { path: "/dashboard", icon: LayoutDashboard, labelKey: "sidebar_overview", end: true },
  { path: "/dashboard/agents", icon: Bot, labelKey: "sidebar_agents" },
  { path: "/dashboard/policies", icon: FileText, labelKey: "sidebar_policies" },
  { path: "/dashboard/audit", icon: Activity, labelKey: "sidebar_audit" },
  { path: "/dashboard/compliance", icon: CheckCircle, labelKey: "sidebar_compliance" },
  { path: "/dashboard/assistant", icon: MessageSquare, labelKey: "sidebar_assistant" },
];

const roleBadge = {
  admin: "bg-red-950/30 text-red-400 border-red-900/50",
  dpo: "bg-amber-950/30 text-amber-400 border-amber-900/50",
  auditor: "bg-blue-950/30 text-blue-400 border-blue-900/50",
  viewer: "bg-slate-800/50 text-slate-400 border-slate-700",
};

export default function DashboardLayout() {
  const { t, lang, toggleLang } = useLanguage();
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  
  // Mobile sidebar state
  const [sidebarOpen, setSidebarOpen] = useState(false);
  // Desktop collapsed state
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  
  // Close sidebar on mobile by default
  useEffect(() => {
    const isMobile = window.innerWidth < 768;
    if (isMobile) setSidebarOpen(false);
    
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        setSidebarOpen(false);
      }
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };
  
  const handleNavClick = () => {
    // Close mobile sidebar on navigation
    if (window.innerWidth < 768) {
      setSidebarOpen(false);
    }
  };

  return (
    <div className="w-full h-screen flex overflow-hidden bg-[#020617]" data-testid="dashboard-layout">
      {/* Mobile hamburger button */}
      <button
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="md:hidden fixed top-4 left-4 z-50 p-2 rounded-lg bg-slate-800/80 backdrop-blur-sm border border-slate-700 text-slate-400 hover:text-white transition-all duration-200"
        data-testid="mobile-menu-btn"
      >
        {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </button>
      
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div 
          className="md:hidden fixed inset-0 z-40 bg-black/60 backdrop-blur-sm transition-opacity duration-200"
          onClick={() => setSidebarOpen(false)}
          data-testid="mobile-overlay"
        />
      )}
      
      {/* Sidebar */}
      <aside 
        className={`
          fixed md:relative left-0 top-0 h-full z-50 md:z-auto
          flex-shrink-0 border-r border-slate-800 bg-[#020617] flex flex-col
          transition-all duration-300 ease-in-out
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
          ${sidebarCollapsed ? 'md:w-16 w-72' : 'md:w-64 w-72'}
        `}
        data-testid="dashboard-sidebar"
      >
        {/* Logo */}
        <div className={`h-16 flex items-center border-b border-slate-800 ${sidebarCollapsed ? 'justify-center px-2' : 'px-5'}`}>
          {sidebarCollapsed ? (
            <Logo size="sm" variant="icon" />
          ) : (
            <Logo size="md" variant="full" />
          )}
        </div>
        
        {/* Navigation */}
        <ScrollArea className="flex-1 py-4">
          <nav className="space-y-1 px-3">
            {navItems.map(({ path, icon: Icon, labelKey, end }) => (
              <NavLink
                key={path}
                to={path}
                end={end}
                onClick={handleNavClick}
                title={sidebarCollapsed ? t(labelKey) : undefined}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-sm text-sm font-medium transition-colors duration-200 ${
                    isActive
                      ? "bg-blue-600/15 text-blue-400 border-l-2 border-blue-500"
                      : "text-slate-400 hover:text-white hover:bg-slate-800/50 border-l-2 border-transparent"
                  } ${sidebarCollapsed ? 'justify-center' : ''}`
                }
                data-testid={`nav-${labelKey}`}
              >
                <Icon className="w-4 h-4 shrink-0" />
                {!sidebarCollapsed && <span>{t(labelKey)}</span>}
              </NavLink>
            ))}
          </nav>
        </ScrollArea>

        {/* Bottom section */}
        <div className="p-3 border-t border-slate-800 space-y-2">
          {/* Collapse button - desktop only */}
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="hidden md:flex w-full justify-center text-slate-500 hover:text-white"
            data-testid="sidebar-collapse-btn"
          >
            {sidebarCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </Button>
          
          {/* User info */}
          {user && !sidebarCollapsed && (
            <div className="flex items-center gap-2.5 px-2 py-2" data-testid="sidebar-user-info">
              <div className="w-8 h-8 rounded-sm bg-slate-800 flex items-center justify-center">
                <User className="w-4 h-4 text-slate-400" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-xs font-medium text-slate-300 truncate" data-testid="sidebar-username">{user.username}</p>
                <Badge className={`${roleBadge[user.role] || roleBadge.viewer} border text-[9px] px-1.5 py-0`} data-testid="sidebar-user-role">{user.role.toUpperCase()}</Badge>
              </div>
            </div>
          )}
          
          {/* Collapsed user icon */}
          {user && sidebarCollapsed && (
            <div className="flex justify-center py-2" title={`${user.username} (${user.role})`}>
              <div className="w-8 h-8 rounded-sm bg-slate-800 flex items-center justify-center">
                <User className="w-4 h-4 text-slate-400" />
              </div>
            </div>
          )}
          
          {!sidebarCollapsed && <Separator className="bg-slate-800" />}
          
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleLang}
            className={`w-full text-slate-400 hover:text-white gap-2 ${sidebarCollapsed ? 'justify-center' : 'justify-start'}`}
            title={sidebarCollapsed ? `${t("language")}: ${lang.toUpperCase()}` : undefined}
            data-testid="lang-toggle-dashboard"
          >
            <Globe className="w-4 h-4" />
            {!sidebarCollapsed && <span>{t("language")}: {lang.toUpperCase()}</span>}
          </Button>
          
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate("/")}
            className={`w-full text-slate-500 hover:text-white gap-2 ${sidebarCollapsed ? 'justify-center' : 'justify-start'}`}
            title={sidebarCollapsed ? t("back_to_site") : undefined}
            data-testid="back-to-site-btn"
          >
            <ArrowLeft className="w-4 h-4" />
            {!sidebarCollapsed && <span>{t("back_to_site")}</span>}
          </Button>
          
          <Button
            variant="ghost"
            size="sm"
            onClick={handleLogout}
            className={`w-full text-red-400/70 hover:text-red-400 hover:bg-red-950/20 gap-2 ${sidebarCollapsed ? 'justify-center' : 'justify-start'}`}
            title={sidebarCollapsed ? (lang === "it" ? "Esci" : "Logout") : undefined}
            data-testid="logout-btn"
          >
            <LogOut className="w-4 h-4" />
            {!sidebarCollapsed && <span>{lang === "it" ? "Esci" : "Logout"}</span>}
          </Button>
        </div>
      </aside>

      {/* Main content */}
      <main 
        className={`
          flex-1 overflow-y-auto bg-[#020617] p-6
          transition-all duration-300
          md:ml-0 ml-0
        `}
        data-testid="dashboard-main"
      >
        {/* Mobile top padding to account for hamburger */}
        <div className="md:hidden h-12" />
        <Outlet />
      </main>
    </div>
  );
}
