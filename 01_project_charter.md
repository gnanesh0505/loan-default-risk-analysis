# Project Charter
## Loan Default Risk Analysis

---

| Field | Details |
|-------|---------|
| **Project Name** | Loan Default Risk Analysis |
| **Project ID** | RISK-2024-001 |
| **Business Sponsor** | Chief Risk Officer (CRO) |
| **Project Manager** | Risk Analytics Lead |
| **Business Analyst** | Gnanesh |
| **Date Created** | October 2024 |
| **Version** | 1.0 |
| **Status** | Approved |

---

## 1. Business Problem

QuickLend Digital Finance (assumed company) offers unsecured personal loans ranging from ₹50,000 to ₹5,00,000 to salaried and self-employed borrowers across Tier 1 and Tier 2 Indian cities.

Over the past two quarters (Q2 and Q3 FY2024), the company's 90+ day past due (DPD) default rate has increased from **5.1% to 6.5%**, representing an estimated additional ₹3.8 crore in credit losses. The current approval policy — a rules engine with a minimum CIBIL score of 680 plus a debt-to-income (DTI) limit of 40% — has not been reviewed in 18 months.

The business needs to understand which borrower segments are driving the increase in defaults and what specific changes to the approval policy can reduce losses without materially impacting loan volume.

---

## 2. Project Objectives

1. Identify the top 3–5 borrower segments with the highest default rates and quantify their contribution to total credit losses.
2. Determine whether the current approval criteria (CIBIL cutoff, DTI limit) are correctly calibrated.
3. Recommend at least two evidence-based policy changes with projected impact on default rate, approval volume, and revenue.
4. Design a Credit Risk monitoring dashboard that allows the Risk team to track default trends weekly.

---

## 3. Success Criteria

| Criterion | Target |
|-----------|--------|
| Default rate reduction | From 6.5% to ≤5.0% within two quarters post-implementation |
| Approval volume impact | ≤10% reduction in monthly approvals |
| Dashboard delivery | Delivered and signed off by end of Week 6 |
| Stakeholder sign-off | 100% of required approvals obtained |
| Policy recommendation | At least one recommendation approved by CRO |

---

## 4. Scope

### In Scope
- Analysis of 12 months of originated loan data
- Borrower segmentation by grade, income, DTI, employment type, loan purpose, and tenure
- KPI definition and baseline measurement
- Approval policy review and recommendations
- Credit Risk monitoring dashboard design and delivery
- Business Requirements Document (BRD) and supporting BA artifacts

### Out of Scope
- Building a production machine learning model
- Redesigning the collections or recovery process
- Changes to the credit bureau integration or CIBIL scoring methodology
- Customer-facing communications or product pricing changes
- Analysis of rejected applications (data not available)

---

## 5. Assumptions

1. 12 months of loan origination data (~80,000 records) is available and extractable.
2. The dataset includes loan outcome (repaid, defaulted, current) for all originated loans.
3. Rejected application data is not available; analysis will be limited to approved loans.
4. Default is defined as 90+ days past due (Charged Off status).
5. Regulatory constraints follow RBI Digital Lending Guidelines (August 2022).
6. No material changes to the product or target market occurred during the analysis period.
7. All required stakeholders are available for interviews within the first two weeks.

---

## 6. Constraints

- Analysis must be explainable and auditable (no black-box models in production).
- Recommendations must comply with RBI fair lending guidelines (no discrimination on protected attributes).
- Dashboard must be accessible to non-technical Risk team members.
- Project must be delivered within 6 weeks.
- Budget: Analytics team time only; no third-party tools to be purchased.

---

## 7. Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Data quality issues (missing income, employment) | High | High | Data profiling in Week 2; imputation or exclusion rules to be agreed with Data team |
| Stakeholder unavailability | Medium | Medium | Schedule interviews in Week 1; use async questionnaire as fallback |
| Selection bias (approved loans only) | High | Medium | Document limitation explicitly; caveat all recommendations |
| Scope creep (request to build ML model) | Medium | High | Agree scope with sponsor in Week 1; use change request process |
| Conflicting priorities (Risk vs. Sales) | Medium | High | Escalation path via CRO; present trade-off options clearly |

---

## 8. Team and Roles

| Name | Role | Responsibility |
|------|------|----------------|
| CRO (sponsor) | Business Sponsor | Final sign-off, resolves escalations |
| Credit Risk Lead | Subject Matter Expert | Provides domain knowledge, reviews recommendations |
| Data Engineering Lead | Data Owner | Provides data extract, confirms field definitions |
| Compliance Officer | Reviewer | Reviews for regulatory compliance |
| Collections Manager | SME | Provides early warning signal insights |
| Product Manager | Stakeholder | Represents customer experience and approval volume targets |
| Gnanesh | Business Analyst | Requirements, analysis, documentation, dashboard spec |

---

## 9. Timeline

| Phase | Duration | End Date |
|-------|----------|----------|
| Initiation | Week 1 | Oct 7, 2024 |
| Discovery & Requirements | Weeks 1–2 | Oct 14, 2024 |
| Data Preparation | Weeks 2–3 | Oct 21, 2024 |
| Analysis | Weeks 3–4 | Oct 28, 2024 |
| Recommendations & Dashboard | Week 4 | Nov 4, 2024 |
| Testing (UAT) | Week 5 | Nov 11, 2024 |
| Delivery & Closure | Week 6 | Nov 18, 2024 |

---

## 10. Budget

| Item | Estimate |
|------|---------|
| BA effort | 30 person-days |
| Data Engineer effort | 5 person-days |
| Risk SME review time | 4 person-days |
| Dashboard development | 3 person-days |
| **Total** | **~42 person-days** |

---

## 11. Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Business Sponsor (CRO) | [Name] | _________ | _____ |
| Risk Analytics Lead | [Name] | _________ | _____ |
| Business Analyst | Gnanesh | _________ | _____ |

---

*Version History: v1.0 — Initial draft (October 2024)*
