# ADR-003: Use Batch Processing for Consent Tracking

**Status:** Accepted (supersedes ADR-002)
**Date:** 2024-10-08
**Project:** GDPR Compliance — Health Inc
**Decided by:** Sunita Patel

## Context
Load tests in week 5 failed. The legacy consent database has 200ms query latency; real-time tracking needs under 20ms. After optimization we reached only 4,000 requests per second against the 10,000 required.

## Decision
Process consent changes in batches of 100 records every 5 minutes. The client's Data Protection Officer approved a 5-minute window.

## Consequences
- **Pro:** Works within the legacy system's limits.
- **Pro:** Simple to monitor and retry.
- **Con:** Consent changes take up to 5 minutes to apply.
- **Con:** Project delayed 3 weeks.

## Alternatives considered
- **Keep real-time with caching (rejected):** tried in week 6, still 4,000 requests per second.
- **Replace the legacy database (rejected):** out of scope.
- **Relax the real-time requirement without a batch design (rejected):** not auditable.
