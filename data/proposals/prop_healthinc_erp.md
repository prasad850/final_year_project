# Proposal: ERP Migration — Health Inc

**Date:** 2024-02-15
**Prepared by:** Priya Sharma
**Client:** Health Inc (Healthcare)
**Project type:** data_migration
**Duration:** 14 weeks
**Total price:** $180,000

## 1. Background
Health Inc currently runs a legacy SAP ERP system on-premise. The system is end-of-life. They need migration to a cloud-based system within 6 months.

## 2. Scope
- Migrate finance, HR, and supply chain modules to AWS
- Preserve 12 years of historical data
- Maintain compliance with healthcare data regulations

## 3. Approach
We will use the standard Nova ERP migration methodology:
1. Discovery and assessment (2 weeks)
2. Data mapping (3 weeks)
3. Migration (6 weeks)
4. Testing and cutover (3 weeks)

Hosting decision: we will host the new ERP on AWS because Health Inc already has AWS credits. (Decided by Priya Sharma, 2024-02-15.)

We have used this methodology before for Manufacturing Co (2023, 10 weeks, led by Rahul Verma).

## 4. Timeline
Start: 2024-03-01. End: 2024-06-07. Duration: 14 weeks.

## 5. Team
- Rahul Verma (Senior Engineer, Lead)
- Neha Gupta (Engineer)
- Vikram Singh (Engineer)
- Sunita Patel (Tech Lead, architecture review)

## 6. Pricing breakdown
- Discovery: $20,000
- Migration (data mapping + migration): $120,000
- Testing: $30,000
- Contingency: $10,000
- Total: $180,000

## 7. Risks
- **Data quality issues (high):** In similar past projects, data quality added 2–3 weeks. We have allocated contingency for this.
- **Legacy system compatibility (medium):** SAP has custom modifications that may not translate cleanly.
- **Timeline pressure (low):** Client wants delivery in 6 months.

## 8. Assumptions
- Client provides data access within 1 week of start
- AWS credits available (client confirmed)
- No custom SAP modules beyond finance/HR/supply chain
