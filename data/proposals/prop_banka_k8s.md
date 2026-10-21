# Proposal: Kubernetes Migration — Bank A

**Date:** 2024-04-08
**Prepared by:** Priya Sharma
**Client:** Bank A (Finance)
**Project type:** infrastructure
**Duration:** 12 weeks
**Total price:** $200,000

## 1. Background
Bank A runs 14 internal microservices on virtual machines. Deployments are slow and scaling is manual. The bank wants a container platform that passes its security audits.

## 2. Scope
- Move 14 microservices to Kubernetes on AWS
- Build CI/CD pipelines
- Harden security for financial regulatory audits
- Train the bank's platform team

## 3. Approach
1. Assessment (2 weeks)
2. Cluster build (3 weeks)
3. Application migration (5 weeks)
4. Security hardening and training (2 weeks)

## 4. Timeline
Start: 2024-05-06. End: 2024-07-26. Duration: 12 weeks.

## 5. Team
- Vikram Singh (Engineer, Lead)
- Sunita Patel (Tech Lead, architecture review)

## 6. Pricing breakdown
- Assessment: $15,000
- Cluster build: $60,000
- Application migration: $80,000
- Security hardening: $25,000
- Training: $10,000
- Contingency: $10,000
- Total: $200,000

## 7. Risks
- **Resource sizing (medium):** Memory and CPU limits must match real production load, including month-end peaks.
- **Audit evidence (medium):** Every change must be logged for auditors.
- **Platform team new to Kubernetes (low):** Training is included.

## 8. Assumptions
- Bank A provides staging environment with production-like data
- Security team available for weekly review
