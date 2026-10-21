# Proposal: CRM Migration — Retail Corp

**Date:** 2024-05-06
**Prepared by:** Priya Sharma
**Client:** Retail Corp (Retail)
**Project type:** data_migration
**Duration:** 10 weeks
**Total price:** $120,000

## 1. Background
Retail Corp runs 180 stores and keeps customer, order and loyalty data in a custom-built on-premise CRM. The vendor ends support this year. The CRM holds about 1.2 million customer records.

## 2. Scope
- Migrate customer, order and loyalty data to a cloud CRM hosted on AWS
- Build reporting dashboards for the marketing and loyalty teams
- Retire the old CRM after cutover
- Hand over to Nova Support after go-live

## 3. Approach
1. Discovery (1 week)
2. Data mapping and duplicate-handling design (2 weeks)
3. Migration (4 weeks)
4. Reporting dashboards (1 week)
5. Testing and cutover (2 weeks)

## 4. Timeline
Start: 2024-06-03. End: 2024-08-09. Duration: 10 weeks.

## 5. Team
- Rahul Verma (Senior Engineer, Lead)
- Vikram Singh (Engineer)
- Sanjay Rao (Support Engineer, handover)

## 6. Pricing breakdown
- Discovery: $12,000
- Data mapping: $24,000
- Migration: $48,000
- Reporting: $16,000
- Testing and cutover: $12,000
- Contingency: $8,000
- Total: $120,000

## 7. Risks
- **Duplicate and inconsistent customer records (high):** Legacy data was entered by stores with no validation. We expect data quality work, as on the Health Inc ERP project.
- **Reporting performance (medium):** Dashboards must run on 1.2M customers and millions of orders.
- **Holiday freeze (low):** No cutover after 2024-10-15.

## 8. Assumptions
- Retail Corp provides read access to the legacy database in week 1
- Store staff available for 2 days of user testing
