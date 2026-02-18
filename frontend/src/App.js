import React from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LanguageProvider } from "@/contexts/LanguageContext";
import { Toaster } from "@/components/ui/sonner";
import LandingPage from "@/pages/LandingPage";
import DashboardLayout from "@/pages/DashboardLayout";
import OverviewPage from "@/pages/OverviewPage";
import AgentsPage from "@/pages/AgentsPage";
import PoliciesPage from "@/pages/PoliciesPage";
import AuditPage from "@/pages/AuditPage";
import CompliancePage from "@/pages/CompliancePage";
import AssistantPage from "@/pages/AssistantPage";

function App() {
  return (
    <LanguageProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/dashboard" element={<DashboardLayout />}>
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
    </LanguageProvider>
  );
}

export default App;
