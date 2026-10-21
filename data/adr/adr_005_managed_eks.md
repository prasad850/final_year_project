# ADR-005: Use Managed EKS Instead of Self-Managed Kubernetes

**Status:** Accepted
**Date:** 2024-05-20
**Project:** Kubernetes Migration — Bank A
**Author:** Vikram Singh

## Context
Bank A's platform team is small and new to Kubernetes. Security audits require patched, supported infrastructure.

## Decision
Use AWS EKS with managed node groups.

## Consequences
- **Pro:** AWS handles control-plane upgrades and patching.
- **Pro:** Fewer operations tasks for the bank's team.
- **Con:** Higher cost than raw EC2 nodes.

## Alternatives considered
- **Self-managed kubeadm on EC2 (rejected):** heavy patching and upgrade burden.
- **Amazon ECS (rejected):** the bank wants portability across clouds.
- **OpenShift (rejected):** licensing about $90K per year.
