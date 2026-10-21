# Proposal: Recommendation Engine — Grocery App

**Date:** 2024-12-02
**Prepared by:** Priya Sharma
**Client:** Grocery App (Consumer retail)
**Project type:** ml
**Duration:** 10 weeks
**Total price:** $85,000

## 1. Background
Grocery App is a mobile grocery delivery app with 400,000 monthly users. Users see the same product lists regardless of habits. The client wants personalized recommendations to raise basket size.

## 2. Scope
- Product recommendation API ("recommended for you", "frequently bought together")
- Data pipeline from order history
- A/B test dashboard to measure basket size

## 3. Approach
1. Discovery (1 week)
2. Data pipeline (2 weeks)
3. Model development: collaborative filtering and embeddings (3 weeks)
4. API and app integration (2 weeks)
5. A/B testing and reporting (2 weeks)

## 4. Timeline
Start: 2025-01-13. End: 2025-03-21. Duration: 10 weeks.

## 5. Team
- Neha Gupta (Engineer, Lead)
- Vikram Singh (Engineer, deployment)

## 6. Pricing breakdown
- Discovery: $8,000
- Data pipeline: $17,000
- Model development: $30,000
- API and integration: $15,000
- A/B testing and reporting: $10,000
- Contingency: $5,000
- Total: $85,000

## 7. Risks
- **Cold start for new users (medium):** New users have no history.
- **Data volume (medium):** Order history is large; pipeline must be incremental.

## 8. Assumptions
- Grocery App provides 12 months of anonymized order history
- Mobile team integrates the API
