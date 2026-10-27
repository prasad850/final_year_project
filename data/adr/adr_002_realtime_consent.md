# ADR-002: Track GDPR Consent in Real Time

**Status:** Superseded by ADR-003
**Date:** 2024-09-09
**Project:** GDPR Compliance — Health Inc
**Decided by:** Sunita Patel

## Context
Patients can withdraw consent at any time. The client wants withdrawals to take effect immediately. Expected load: 10,000 requests per second at peak.

## Decision
Build a real-time consent tracking module that checks the legacy consent database on every request.

## Consequences
- **Pro:** Consent changes apply instantly.
- **Con:** Depends on the legacy database performing at peak load. Not yet benchmarked.

## Alternatives considered
- **Batch processing (rejected at the time):** client asked for immediate effect.
- **Replace legacy consent database (rejected):** out of scope and budget.
