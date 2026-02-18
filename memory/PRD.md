# GOVERN.AI - PRD (Product Requirements Document)

## Problem Statement
Build GOVERN.AI — The compliance-first AI control plane for enterprises. A platform that governs AI agents, workflows and models before compliance, security and audit become a problem. UVP: "Sovereign control plane" for AI agents in highly regulated sectors, combining agent governance with deep European regulatory compliance integration.

## Architecture
- **Frontend**: React + Tailwind CSS + Shadcn/UI (port 3000)
- **Backend**: FastAPI + MongoDB (port 8001)
- **AI Integration**: OpenAI GPT-5.2 via Emergent LLM key
- **Database**: MongoDB (collections: agents, policies, audit_logs, compliance_standards, chat_messages)

## User Personas
- **CTO/CISO**: Needs overview of AI agent landscape and risk posture
- **DPO (Data Protection Officer)**: Monitors GDPR compliance and data governance
- **Compliance Officer**: Tracks regulatory standards (AI Act, ISO, DORA, NIS2)
- **IT Administrator**: Manages agent lifecycle and policy enforcement

## Core Requirements
- Landing page with UVP, features showcase, target sectors
- Dashboard with sidebar navigation
- AI Agents Registry (CRUD) with risk classification
- Policy Engine (CRUD) with regulation mapping
- Audit Trail with search/filter/dense table view
- Compliance Monitor for 6 EU/ISO standards
- AI-powered Compliance Assistant (GPT-5.2)
- Bilingual support (EN/IT)
- Dark mode enterprise aesthetic

## What's Been Implemented (Feb 18, 2026)
- [x] Full landing page (hero, features bento grid, clients, CTA, footer)
- [x] Dashboard with sidebar (Overview, Agents, Policies, Audit, Compliance, Assistant)
- [x] KPI dashboard with real-time data from MongoDB
- [x] AI Agents CRUD (create, read, update, delete) with risk/status management
- [x] Policy Engine CRUD with regulation, severity, enforcement mapping
- [x] Audit Trail with searchable/filterable dense table (25 seeded events)
- [x] Compliance Monitor for 6 standards (AI Act, GDPR, ISO 27001, ISO 42001, DORA, NIS2)
- [x] AI Compliance Assistant with GPT-5.2 (real LLM integration)
- [x] Bilingual toggle (EN/IT)
- [x] Every action creates audit log entry
- [x] Seed data for demo (4 agents, 5 policies, 25 audit logs, 6 compliance standards)

## Prioritized Backlog

### P0 (Next Phase)
- Authentication system (JWT or Google Auth)
- Role-based access control (Admin, DPO, Auditor, Viewer)
- Real-time agent monitoring (websocket)

### P1
- Dashboard data visualizations (charts, trends over time)
- Policy conflict detection engine
- Automated compliance scoring algorithm
- Export audit reports (PDF/CSV)
- Agent activity timeline

### P2
- Integration connectors (IAM, SIEM, ServiceNow, CMDB)
- AI-powered risk auto-classification
- Custom compliance framework builder
- Multi-tenant support
- API key management for external agent registration
- Notification system (email alerts on policy violations)

## Next Tasks
1. Add authentication + RBAC
2. Enhanced dashboard charts (recharts)
3. PDF/CSV export for audit trail and compliance reports
4. Policy conflict detection
5. Real-time agent status monitoring
