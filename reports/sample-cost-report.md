# Sample FinOps Cost Analysis Report

> **Synthetic demonstration data only.** Numbers below are example figures and are not an Azure bill.

## Summary

| Metric | Value |
|---|---:|
| Total sample spend | USD 1,135.00 |
| Demonstration budget | USD 1,000.00 |
| Budget utilization | 113.50% |
| Status | OVER_BUDGET |
| Records analyzed | 6 |

## Spend by service

| Service | Cost |
|---|---:|
| Virtual Machines | USD 565.25 |
| App Service | USD 245.70 |
| Azure SQL | USD 180.30 |
| Storage | USD 95.50 |
| Networking | USD 48.25 |

## Governance interpretation

This synthetic dataset is above the supplied demo budget. A real process should verify billing period, currency, credits, forecast versus actual cost, and scope before raising an incident or contacting service owners.

The high-spend service review signal is a prioritization heuristic—not a claim that the cost is unnecessary or that a specific savings amount is possible.

## Recommended review actions

1. Confirm the cost export's scope, period, and currency with the FinOps owner.
2. Check ownership and cost-centre tags for all material services.
3. Ask service owners to review utilization, commitments, schedules, and tier choices.
4. Document the approved action and compare a normalized post-change billing period.
