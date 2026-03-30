import React from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import { useEffect } from "react";
import { LanguageProvider } from "@/contexts/LanguageContext";
import { AuthProvider, useAuth } from "@/contexts/AuthContext";
import { Toaster } from "@/components/ui/sonner";
import LandingPage from "@/pages/LandingPage";
import LoginPage from "@/pages/LoginPage";
import DashboardLayout from "@/pages/DashboardLayout";
import OverviewPage from "@/pages/OverviewPage";
import AgentsPage from "@/pages/AgentsPage";
import PoliciesPage from "@/pages/PoliciesPage";
import AuditPage from "@/pages/AuditPage";
import CompliancePage from "@/pages/CompliancePage";
import AssistantPage from "@/pages/AssistantPage";

const pageTitles = {
  "/": "GOVERN.AI — Sovereign Control Plane",
  "/login": "Login — GOVERN.AI",
  "/dashboard": "Dashboard — GOVERN.AI",
  "/dashboard/agents": "AI Agents — GOVERN.AI",
  "/dashboard/policies": "Policy Engine — GOVERN.AI",
  "/dashboard/audit": "Audit Trail — GOVERN.AI",
  "/dashboard/compliance": "Compliance — GOVERN.AI",
  "/dashboard/assistant": "ARIA Assistant — GOVERN.AI",
};

function PageTitleUpdater() {
  const location = useLocation();
  useEffect(() => {
    document.title = pageTitles[location.pathname] || "GOVERN.AI";
  }, [location.pathname]);
  return null;
}

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();
  if (loading) {
    return (
      <div className="min-h-screen bg-[#020617] flex items-center justify-center">
        <div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <BrowserRouter>
          <PageTitleUpdater />
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/dashboard" element={<ProtectedRoute><DashboardLayout /></ProtectedRoute>}>
              <Route index element={<OverviewPage />} />
              <Route path="agents" element={<AgentsPage />} />
              <Route path="policies" element={<PoliciesPage />} />
              <Route path="audit" element={<AuditPage />} />
              <Route path="compliance" element={<CompliancePage />} />
              <Route path="assistant" element={<AssistantPage />} />
            </Route>
          </Routes>
        </BrowserRouter>
        <Toaster position="top-right" />
      </AuthProvider>
    </LanguageProvider>
  );
}

export default App;
