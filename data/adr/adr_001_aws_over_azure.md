# ADR-001: Use AWS Instead of Azure for ERP Hosting

**Status:** Accepted
**Date:** 2024-03-05
**Project:** ERP Migration — Health Inc
**Decided by:** Rahul Verma

## Context
Health Inc must host its migrated ERP in the cloud. The client already holds AWS credits and our delivery team has more AWS experience.

## Decision
We will host the ERP on AWS (us-east-1, multi-AZ).

## Consequences
- **Pro:** Client AWS credits reduce hosting cost.
- **Pro:** Team already knows AWS tools such as DMS and RDS.
- **Con:** Locks the client into AWS for this system.

## Alternatives considered
- **Azure (rejected):** no credits, team less experienced.
- **Keep on-premise (rejected):** the legacy platform is end-of-life.
