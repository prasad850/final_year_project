# Nova Consulting dataset — Sem 1 (41 files)

Fictional company. Folders: proposals(5) pricing(3) clients(3) case_studies(3) design(3) adr(5) post_mortems(3) delivery_notes(4) tickets(5) incidents(3) slack(2 files, 30 messages) hr(2).
Note: the type counts in the plan add up to 41, not 40.

## Fixed facts (keep consistent if you edit anything)
| Project | Client | Lead | Dates | Price |
|---|---|---|---|---|
| ERP Migration | Health Inc | Rahul Verma | 2024-03-01 to 2024-06-07 (14 wk) | $180,000 |
| CRM Migration | Retail Corp | Rahul Verma | 2024-06-03 to 2024-08-09 planned, 11 wk actual | $120,000 |
| GDPR Compliance | Health Inc | Sunita Patel | 2024-08-26, planned 9 wk, actual 12 wk (2024-11-15) | $95,000 |
| Kubernetes Migration | Bank A | Vikram Singh | 2024-05-06 to 2024-07-26 (12 wk) | $200,000 |
| Recommendation Engine | Grocery App | Neha Gupta | 2025-01-13 to 2025-03-21 (10 wk) | $85,000 |
Manufacturing Co appears only as a past reference (ERP, 2023, 10 weeks, led by Rahul) — no project documents.

## Scenarios built in
- Repeated mistake: ADR-004 rejects MongoDB (Retail CRM) -> Neha proposes it again in Slack (2025-02)
- Superseded decision: ADR-002 (real-time consent) superseded by ADR-003 (batch)
- Cross-client reuse: ERP (Health Inc) methodology + parallel validation reused; case studies
- Multi-hop: data quality problems in ERP and CRM, both led by Rahul; Redis/OOM incidents fixed by Sanjay
- Who-knows-what: Vikram = Kubernetes/banking, Sunita = GDPR/healthcare, Sanjay = Redis/incidents, Neha = ML
- Unanswerable (nothing in the data): SOC 2 certification, Azure DevOps, Manufacturing Co pricing, any 2026 project

## Access tags (set these in loader metadata)
proposals, pricing, clients -> team:presales + client:<name> | case_studies, hr -> public
design, adr, delivery_notes, post_mortems (non-anonymized) -> team:delivery + client:<name>
pm_k8s_financial_anonymized -> public | tickets, incidents -> team:support + client:<name> | slack -> per channel

Fixed 2024-10-19: CRM design doc now predates ADR-004 correctly (update note added); ERP proposal now states the AWS hosting decision explicitly.
