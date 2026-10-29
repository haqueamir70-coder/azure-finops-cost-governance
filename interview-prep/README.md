# Azure FinOps & Cloud Cost Governance — Senior Interview Guide

**Target:** Senior Cloud / DevOps / Platform Engineer (around 8 years' experience)  
**Style:** Simple answers first, practical steps second. Use your real experience; do not claim work you have not done.

> Senior answer pattern: clarify business impact → investigate with evidence → act safely → verify cost and reliability → prevent recurrence.

FinOps is continuous collaboration between engineering, finance, product, and business teams. The lifecycle is Inform → Optimize → Operate. References: [Microsoft FinOps Framework](https://learn.microsoft.com/en-us/cloud-computing/finops/framework/finops-framework) · [Azure cost optimization principles](https://learn.microsoft.com/en-us/azure/well-architected/cost-optimization/principles).

## A repeatable scenario framework: C-I-A-V

1. **Clarify:** scope, time period, business impact, production/non-production, SLO.
2. **Investigate:** Cost Analysis, metrics, logs, tags, resource inventory, release/change history.
3. **Act safely:** owner, approval, expected benefit, risk, rollback.
4. **Verify:** compare equivalent cost periods and confirm performance/availability; document prevention.

---

## Part 1 — Core concepts

### Q1. What is FinOps?
**Easy answer:** FinOps helps engineering, finance, and business teams understand cloud spending and make better cost decisions without damaging reliability or business value.

### Q2. What are the three FinOps phases?
**Easy answer:** Inform makes costs visible; Optimize finds and implements worthwhile improvements; Operate measures results and makes the process continuous.

### Q3. Budget versus alert?
**Easy answer:** A budget is a spending target for a scope and period. An alert notifies people when a threshold is reached. A budget alert does not automatically stop spending.

### Q4. Showback versus chargeback?
**Easy answer:** Showback reports costs to a team. Chargeback assigns those costs to the team's financial budget or ledger.

### Q5. How do you allocate Azure costs to teams?
**Easy answer:** Use subscription/resource-group structure and consistent tags such as owner, application, environment, and cost-center. Show unallocated spend separately.

### Q6. Cost optimization versus cost cutting?
**Easy answer:** Optimization improves value per dollar while respecting performance, availability, security, and business needs. Blind cost cutting can make services unreliable.

### Q7. What is Azure Advisor?
**Easy answer:** It gives recommendations based on supported configuration and usage signals. I validate impact and business context before acting on a recommendation.

### Q8. What is a unit-cost metric?
**Easy answer:** Cost per business outcome, such as cost per transaction or active user. It helps show whether the service becomes more efficient as usage grows.

---

## Part 2 — Senior scenario questions

### Q9. Azure bill increased by 40%. What do you do first?
**Answer:** Confirm billing scope, period, and currency. Compare equivalent periods, then group costs by service, resource, subscription, region, and tags. Check usage changes, deployments, pricing, commitments, logs, and anomalies. Prioritize the biggest verified drivers, agree safe actions with owners, then verify cost and SLOs after the change.

**Senior signal:** Do not assume the increase is waste. It may be legitimate traffic growth, a new launch, or a billing/credit timing difference.

### Q10. Leadership wants 25% savings in 90 days without customer impact.
**Answer:** Establish a cost and reliability baseline. First fix obvious waste and improve allocation. Then validate rightsizing, non-production schedules, storage tiers, autoscaling, licensing, and commitments. Each action needs an owner, risk, expected range, approval, and rollback. Report verified savings alongside latency and availability.

### Q11. A production VM looks oversized. Resize immediately?
**Answer:** No. Review CPU, memory, disk I/O, network, and peak periods over a representative window. Test a smaller SKU in a controlled window, confirm rollback, then compare performance and cost. Low average CPU alone is not enough evidence.

### Q12. Non-production VMs run 24/7.
**Answer:** Identify owners and working hours. Schedule stop/deallocate for eligible VMs using an approved automation process. Exclude shared services and workloads with 24/7 dependencies. Track exceptions and confirm savings; stopped VMs may still incur storage/network charges.

### Q13. How do you evaluate Reservations or Savings Plans?
**Answer:** Analyze stable historical usage, workload lifetime, flexibility, utilization risk, and break-even. Compare on-demand costs with commitment costs and check applicable exchange/cancellation terms. Commit only to a conservative stable baseline and review utilization regularly.

### Q14. Teams are not tagging resources.
**Answer:** Define a small taxonomy with clear values and owners. Discover existing gaps, assign remediation, and provide reusable Terraform modules. Start Azure Policy in audit mode, measure impact, then enforce gradually with a documented exemption process.

### Q15. Shared platform costs cannot be assigned to one app.
**Answer:** Separate directly attributable costs from shared costs. Choose a fair allocation driver such as requests, compute time, storage, or team usage. Document the method and show unallocated costs transparently instead of silently spreading them.

### Q16. Forecast says the team will exceed budget.
**Answer:** Validate the forecast period and trends, identify the cost drivers, and contact owners early. Present options with cost, delivery, performance, and risk trade-offs. Set alert thresholds and escalation ownership. An alert is not an automatic spending cap.

### Q17. A team wants a three-year commitment for an uncertain workload.
**Answer:** Do not decide based only on discount percentage. Review demand history, roadmap, utilization risk, and break-even. Compare shorter commitments or a partial stable baseline and get finance approval.

### Q18. Log Analytics cost doubled in a week.
**Answer:** Compare ingestion by table, resource, and time. Check diagnostic settings, recent deployments, duplicate logs, and debug verbosity. Coordinate with security and service owners before reducing data. Tune filters/retention only where appropriate, then verify required telemetry still exists.

### Q19. AKS cost is high.
**Answer:** Break down compute, disks, load balancers, networking, and logs. Review node utilization, requests/limits, autoscaler settings, node pools, scheduling, and non-production hours. Test changes against latency, availability, and pod-disruption needs. Never reduce replicas blindly.

### Q20. Storage costs unexpectedly increased.
**Answer:** Check capacity growth, access tiers, transaction volume, replication, snapshots, versioning, soft delete, and retrieval patterns. Verify recovery/compliance requirements before changing retention or tier. Test a lifecycle policy on suitable data and measure storage plus retrieval costs.

### Q21. Finance says the cloud bill is wrong.
**Answer:** Confirm billing account, invoice period, currency, credits, taxes, scope, amortization view, and export freshness. Reconcile Cost Analysis with the invoice/export. If the discrepancy remains, open a billing case with evidence.

### Q22. Engineering wants performance; Finance wants lower costs.
**Answer:** Define measurable constraints: SLOs, budget, and unit cost. Present evidence-based options and trade-offs, test the safest change, and get accountable owner approval. Do not treat cost and reliability as opposing goals without data.

### Q23. How do you prevent expensive Terraform changes?
**Answer:** Use pull requests, format/validate, security and policy checks, reviewed plans, environment separation, least privilege, and production approval gates. Protect remote state and never expose credentials in logs. Add cost checks where practical.

### Q24. Terraform plan wants to replace a production resource.
**Answer:** Stop and inspect the plan, immutable attributes, provider/version changes, state drift, and configuration differences. Confirm intent with the owner, test in non-production, and prepare rollback. Do not apply until replacement and downtime impact are understood.

### Q25. Budget alert fired but nobody acted.
**Answer:** Check scope, threshold, recipients, delivery, and alert configuration. Assign an owner and escalation schedule, then test end to end. A dashboard without a response process is not enough.

### Q26. What belongs on a FinOps dashboard?
**Answer:** Total spend, month-over-month change, forecast versus budget, cost by subscription/service/team, tag coverage, top cost drivers, anomalies, and optimization status. Show billing period and refresh time; give executives decisions and engineers resource-level detail.

### Q27. How do you prove savings were real?
**Answer:** Record the baseline, time period, workload volume, pricing/commitment effects, and change. Compare equivalent post-change periods and normalize for traffic where possible. Check SLOs and shifted costs. Report realized savings separately from estimates.

### Q28. A cost anomaly started after a deployment.
**Answer:** Correlate timing with release history, usage, metrics, and per-service costs. If customer or budget risk is high, follow incident procedure and consider rollback after confirming the likely link. Preserve evidence and add a regression guardrail.

### Q29. How would you roll out governance across 20 subscriptions?
**Answer:** Inventory subscriptions and owners, establish management-group boundaries, define a tag/policy baseline, and pilot on a representative subscription. Start with audit and visibility, measure exceptions, then enforce in stages. Use reusable Terraform, least privilege, central reporting, and an exception process.

### Q30. The cheapest design is less resilient. What do you choose?
**Answer:** Compare the saving with downtime impact, recovery objectives, and business criticality. Preserve required availability for critical production systems and find safer savings elsewhere. A development workload may accept lower availability if its owner approves.

### Q31. How do you handle unallocated spend?
**Answer:** Create an explicit unallocated category, find the largest gaps, and work with owners to map them. Enforce defaults for new resources and report allocation coverage. Never silently distribute unknown spend without an agreed rule.

### Q32. What would you do in your first 30/60/90 days?
**Answer:** **30 days:** understand billing scopes, stakeholders, cost drivers, and reliability constraints. **60 days:** deliver allocation, budget alerts, top optimization actions, and ownership. **90 days:** automate repeatable controls, measure verified outcomes, and establish regular finance/engineering reviews. Adjust the plan to environment size and access.

---

## Troubleshooting checklist

1. Validate billing scope, period, currency, credits, and export freshness.
2. Identify which service/resource/region/tag caused the delta.
3. Check usage, pricing, deployments, and configuration changes.
4. Review idle/oversized resources, logs, storage retention, network transfer, and commitments.
5. Assign an owner; document risk, benefit, approval, and rollback.
6. Verify cost and SLOs after the change and prevent recurrence.

## Simple terms

- **Rightsizing:** match capacity to measured demand.
- **Autoscaling:** change capacity with load within safe limits.
- **Forecast:** estimate future spend from current/historical patterns and assumptions.
- **Anomaly:** spend that differs from the expected baseline.
- **Commitment discount:** lower rate in exchange for a commitment; unused commitment is a risk.
- **Tag coverage:** share of cost/resources with required allocation metadata.
- **Unit economics:** cost per business outcome.
- **Guardrail:** preventive or detective control for agreed boundaries.
- **SLO:** target reliability/performance; cost changes must respect it.

## How to speak in interviews

Keep the first answer to 30–60 seconds. If asked for depth, add evidence, metrics, risk, trade-off, and validation. Use real examples from your work and label lab projects honestly.

## References

- [Microsoft FinOps Framework](https://learn.microsoft.com/en-us/cloud-computing/finops/framework/finops-framework)
- [Azure cost optimization principles](https://learn.microsoft.com/en-us/azure/well-architected/cost-optimization/principles)
- [Microsoft FinOps iteration guidance](https://learn.microsoft.com/ar-sa/cloud-computing/finops/conduct-iteration)
