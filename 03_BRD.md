# Business Requirements Document (BRD)
## Loan Default Risk Analysis

---

| Field | Details |
|-------|---------|
| **Document ID** | BRD-RISK-2024-001 |
| **Project** | Loan Default Risk Analysis |
| **Author** | Gnanesh (Business Analyst) |
| **Reviewed By** | Credit Risk Lead, Compliance Officer |
| **Approved By** | CRO |
| **Version** | 1.1 |
| **Date** | October 2024 |

---

## 1. Executive Summary

QuickLend Digital Finance has experienced a 1.4 percentage point increase in the 90+ day default rate over the past two quarters. This document captures the business requirements for an analytical project to identify the root causes of this increase, define actionable policy changes, and deliver a monitoring dashboard for ongoing tracking.

---

## 2. Business Context

### 2.1 Current State
- Approval policy: rules engine with minimum CIBIL score 680 and maximum DTI 40%
- Policy last reviewed: 18 months ago
- Current 90+ DPD default rate: 6.5% (up from 5.1% two quarters ago)
- Monthly loan disbursals: ~6,500 loans, average ticket size ₹1.8 lakh
- Estimated additional credit loss from rate increase: ₹3.8 crore per quarter

### 2.2 Problem Statement
The business does not currently have visibility into which specific borrower segments are driving the default increase, nor does it have a data-driven framework for evaluating policy adjustments and their trade-offs.

### 2.3 Opportunity
By identifying the 3–5 highest-risk segments and quantifying the cost of approving them, the business can make targeted policy changes that reduce default losses while minimising the impact on approval volume and revenue.

---

## 3. Business Objectives

| ID | Objective | Measure | Target |
|----|-----------|---------|--------|
| BO-01 | Reduce the 90+ DPD default rate | Default rate % | ≤5.0% within 2 quarters |
| BO-02 | Maintain loan volume | Monthly approvals | <10% drop from current baseline |
| BO-03 | Provide Risk team with ongoing default visibility | Dashboard uptime and adoption | Weekly refresh; used by ≥5 team members |
| BO-04 | Ensure all recommendations are RBI-compliant | Compliance sign-off | 100% approval from Compliance Officer |

---

## 4. Scope

### 4.1 In Scope
- Borrower segmentation analysis using 12 months of loan origination data
- KPI definition, calculation, and baseline measurement
- Approval policy review and recommendations
- Scenario analysis (impact of policy changes on default rate and volume)
- Credit Risk monitoring dashboard design and delivery
- All BA documentation (BRD, FRD, user stories, data dictionary, recommendation memo)

### 4.2 Out of Scope
- Production ML model development
- Collections or recovery process redesign
- Credit bureau integration changes
- Analysis of rejected applications
- Customer communication or product repricing

---

## 5. Assumptions

| ID | Assumption |
|----|-----------|
| A-01 | 12 months of loan origination data (~80,000 records) is available |
| A-02 | Loan outcome data (repaid, defaulted, current) is available for all originated loans |
| A-03 | Rejected application data is not available |
| A-04 | Default = 90+ days past due (loan_status = Charged Off) |
| A-05 | No material changes to the target market or product occurred in the analysis period |
| A-06 | Required stakeholders are available for interviews in Weeks 1–2 |
| A-07 | The BI team will build the dashboard from the BA's specification |

---

## 6. Constraints

| ID | Constraint |
|----|-----------|
| C-01 | All recommendations must be explainable at the individual borrower level |
| C-02 | No protected attributes (gender, religion, caste) may be used in any decision rule |
| C-03 | Every loan rejection must have a documented, communicable reason |
| C-04 | Project timeline: 6 weeks |
| C-05 | No new third-party tools or licenses to be purchased |
| C-06 | RBI Digital Lending Guidelines (August 2022) must be adhered to |

---

## 7. Business Requirements

### BR-01: Default Segmentation
**Priority:** Must Have
The business requires an analysis that identifies and ranks borrower segments by default rate. Each segment must include:
- Segment definition (e.g., Grade D–E, DTI >35%, self-employed)
- Default rate within segment
- Segment size as % of total portfolio
- Estimated contribution to total credit losses

**Acceptance Criteria:** At least 3 segments identified with default rate ≥2x the portfolio average and volume >500 loans in the analysis period.

---

### BR-02: KPI Definitions and Baseline
**Priority:** Must Have
The business requires a formal, agreed KPI framework covering:
- 90+ DPD default rate (by vintage, by segment)
- Approval rate
- Non-Performing Loan (NPL) ratio
- Estimated Expected Loss (EL) = PD × LGD × EAD

Each KPI must have a clear definition, a baseline value, and a target.

**Acceptance Criteria:** KPI definitions signed off by Credit Risk Lead and CRO before analysis begins.

---

### BR-03: Policy Recommendations
**Priority:** Must Have
The business requires at least two policy change options, each with:
- Specific rule change (e.g., "reduce maximum DTI from 40% to 35% for Grade D borrowers")
- Projected impact on default rate
- Projected impact on approval volume
- Projected revenue impact
- Compliance assessment

**Acceptance Criteria:** At least one option approved by CRO and signed off by Compliance Officer.

---

### BR-04: Credit Risk Monitoring Dashboard
**Priority:** Must Have
The Risk team requires a self-service dashboard with:
- Default rate trend (weekly/monthly, by vintage)
- Segment-level breakdown (grade, purpose, income band, employment type)
- Alert indicator when default rate exceeds threshold
- Filter by loan grade, product type, origination period

**Acceptance Criteria:** Dashboard UAT passed by 3 business users; data refreshes at least weekly.

---

### BR-05: Scenario Analysis
**Priority:** Should Have
The business requires a scenario analysis showing the projected effect of each policy option on:
- Monthly approval volume
- Monthly default rate
- Monthly revenue (net interest income after expected loss)

**Acceptance Criteria:** Scenarios reviewed and accepted by CRO and Credit Risk Lead.

---

### BR-06: Vintage Analysis
**Priority:** Should Have
The business requires a vintage analysis showing default rates by loan origination month, to identify whether the increase is concentrated in a specific cohort (e.g., festive-season loans).

**Acceptance Criteria:** Vintage chart delivered as part of EDA report; key findings narrated in the recommendation memo.

---

### BR-07: Data Quality Documentation
**Priority:** Should Have
The business requires documentation of data quality issues discovered during the project, including fields with high missing rates and any imputation or exclusion decisions made.

**Acceptance Criteria:** Data Quality Report reviewed and accepted by Data Engineering Lead.

---

### BR-08: Lessons Learned Log
**Priority:** Could Have
A lessons learned log to be completed at project close, capturing what worked, what did not, and recommendations for future analytics projects.

---

## 8. Key Performance Indicators

| KPI | Definition | Baseline | Target | Frequency |
|-----|-----------|---------|--------|-----------|
| 90+ DPD Default Rate | Loans reaching 90+ DPD ÷ loans originated in same vintage | 6.5% | ≤5.0% | Monthly |
| Approval Rate | Approved applications ÷ total applications | [Baseline TBD] | <10% reduction | Monthly |
| NPL Ratio | Non-performing loans ÷ total outstanding loan book | [Baseline TBD] | Reducing trend | Monthly |
| Expected Loss | PD × LGD × EAD (portfolio level) | [Baseline TBD] | Reducing trend | Quarterly |
| Portfolio at Risk (PAR 30) | Loans 30+ DPD ÷ total book | [Baseline TBD] | Monitoring | Weekly |

---

## 9. Non-Functional Requirements

| ID | Requirement |
|----|------------|
| NFR-01 | Dashboard must load within 5 seconds for a standard date range query |
| NFR-02 | All analysis must be reproducible (documented code and methodology) |
| NFR-03 | No personally identifiable information (PII) to be included in any shared report |
| NFR-04 | Dashboard access restricted to Risk team and CRO (role-based access control) |
| NFR-05 | All policy recommendations must include a fairness check |

---

## 10. Sign-off

| Role | Name | Decision | Date |
|------|------|----------|------|
| CRO (Sponsor) | [Name] | Approved / Rejected / Pending | _____ |
| Credit Risk Lead | [Name] | Approved / Rejected / Pending | _____ |
| Compliance Officer | [Name] | Approved / Rejected / Pending | _____ |
| BA | Gnanesh | Submitted | Oct 2024 |

---

## 11. Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Week 1 | Gnanesh | Initial draft |
| 1.1 | Week 2 | Gnanesh | Added BR-06 (vintage analysis) based on Credit Risk Lead interview; added NFR-05 (fairness check) based on Compliance Officer interview |

---

*This document is controlled. Any scope changes require a formal Change Request approved by the Business Sponsor.*
