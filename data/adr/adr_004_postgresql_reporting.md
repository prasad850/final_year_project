# ADR-004: Use PostgreSQL, Not MongoDB, for Reporting

**Status:** Accepted
**Date:** 2024-06-24
**Project:** CRM Migration — Retail Corp
**Decided by:** Rahul Verma

## Context
Marketing needs loyalty dashboards over 1.2M customers and about 8M orders. In week 4 we tested MongoDB because setup was fast and the schema is flexible.

## Decision
Use PostgreSQL materialized views for reporting.

## Consequences
- **Pro:** Loyalty reports load in about 3 seconds.
- **Pro:** Team knows SQL well; Metabase connects natively.
- **Con:** Views need a refresh schedule.

## Alternatives considered
- **MongoDB (rejected):** aggregation pipelines took 40+ seconds for loyalty reports.
- **Elasticsearch (rejected):** overkill for this reporting need.
- **Redshift (rejected):** extra cost not justified at this data size.

## Lesson
Benchmark reporting queries with real data volume before choosing a store.
