# Stakeholder Register
## Loan Default Risk Analysis | RISK-2024-001

---

| Version | Date | Author |
|---------|------|--------|
| 1.0 | October 2024 | Gnanesh (BA) |

---

## Stakeholder Matrix

| # | Name/Role | Department | Interest | Influence | Engagement Strategy | Communication Preference | Availability |
|---|-----------|------------|----------|-----------|---------------------|--------------------------|--------------|
| 1 | Chief Risk Officer (CRO) | Risk | High — owns default KPIs and policy decisions | High — final sign-off authority | Manage closely; weekly updates; escalation point | Weekly status email + milestone presentations | Bi-weekly |
| 2 | Credit Risk Lead | Risk & Analytics | High — day-to-day owner of approval rules | High — primary technical reviewer | Collaborate; involve in all analysis reviews | Slack + weekly meeting | Daily |
| 3 | Data Engineering Lead | Technology | Medium — provides data extracts | Medium — controls data access | Keep informed; formal data request process | Email + JIRA tickets | Weekly |
| 4 | Compliance Officer | Legal & Compliance | High — ensures RBI guideline adherence | High — can block recommendations | Consult early; include in requirements sign-off | Formal email; meeting minutes shared | As needed |
| 5 | Collections Manager | Collections | High — knows defaulter behavior patterns | Medium — key SME | Keep informed; interview in Week 1 | Slack + interview notes shared back | Weekly |
| 6 | Product Manager | Product | Medium — concerned about approval rate drop | Medium — represents customer experience | Keep informed; share trade-off options | Weekly status meeting | Weekly |
| 7 | Sales Head | Sales | Low-Medium — concerned about loan volume | Medium — revenue pressure | Monitor; share final recommendations | Monthly summary email | Monthly |
| 8 | BI / Dashboard Developer | Technology | Low — executes dashboard build | Low — implements BA specification | Keep informed; provide detailed specs | Confluence spec + Slack | During UAT |

---

## Stakeholder Interest-Influence Grid

```
HIGH INFLUENCE
     |
     |  [CRO]          [Credit Risk Lead]
     |  [Compliance]
     |
     |  [Collections]  [Product Manager]
     |  [Data Eng]
     |
     |  [Sales Head]   [BI Developer]
     |
LOW INFLUENCE
     +--------------------------------
     LOW INTEREST        HIGH INTEREST
```

**Quadrant strategy:**
- High Influence / High Interest → **Manage closely** (CRO, Credit Risk Lead, Compliance)
- High Influence / Low Interest → **Keep satisfied** (Data Eng Lead)
- Low Influence / High Interest → **Keep informed** (Collections, Product, BI Dev)
- Low Influence / Low Interest → **Monitor** (Sales Head)

---

## Key Stakeholder Interview Notes (Summary)

### CRO — Interview Week 1
**Question asked:** What does success look like for this project?
**Response (assumed):** "I want to bring the default rate below 5% by Q1 next year without killing our approval numbers. We have a growth target — I can't tell sales to slow down without data to back it."

**BA Note:** Competing objectives (reduce risk AND maintain volume) is the central tension of this project. All recommendations must show both levers.

---

### Credit Risk Lead — Interview Week 1
**Question asked:** What do you believe is driving the increase in defaults?
**Response (assumed):** "My gut says it's the Grade D–E borrowers with high DTI that we started approving more of last year when we loosened the criteria for the festive season campaign. But I don't have data to prove it yet."

**BA Note:** This is a hypothesis to test in Phase 5. Festive-season vintage cohort analysis should be a specific analysis task.

---

### Collections Manager — Interview Week 2
**Question asked:** Are there early warning signals that predict default before 90 DPD?
**Response (assumed):** "Yes — borrowers who miss their first EMI are extremely likely to default eventually. Also, self-employed borrowers with income not verified through salary slip — their actual income seems lower than declared."

**BA Note:** Early warning signal (first EMI miss) and income verification quality are new requirements to add to the data analysis scope.

---

### Compliance Officer — Interview Week 1
**Question asked:** What constraints apply to our recommendations?
**Response (assumed):** "Any policy tightening must be explainable at an individual level. We cannot use gender, religion, or caste in any decision rule. And every rejection must have a documented reason the customer can receive."

**BA Note:** Explainability and fairness are hard constraints. Log as non-functional requirements in the BRD.

---

## RACI Matrix

| Deliverable | BA (Gnanesh) | CRO | Credit Risk Lead | Data Eng | Compliance | Product |
|-------------|-------------|-----|-----------------|----------|------------|---------|
| Project Charter | R | A | C | I | C | I |
| Stakeholder Register | R | A | C | I | I | I |
| BRD | R | A | C | C | C | C |
| Data Quality Report | R | I | A | C | I | I |
| EDA / Analysis | R | I | A | C | I | I |
| Recommendation Memo | R | A | C | I | C | C |
| Dashboard Design | R | I | A | I | I | C |
| UAT Sign-off | C | A | R | I | C | I |
| Final Presentation | R | A | C | I | I | C |

**R** = Responsible | **A** = Accountable | **C** = Consulted | **I** = Informed

---

## Communication Plan

| Communication | Audience | Frequency | Format | Owner |
|---------------|----------|-----------|--------|-------|
| Project status update | All stakeholders | Weekly | Email (RAG status) | BA |
| Working session | Credit Risk Lead + BA | Weekly | 30-min meeting | BA |
| Risk & issue review | CRO + Risk Lead | Bi-weekly | 15-min standup | BA |
| Requirements workshop | Risk, Compliance, Product | Week 2 (one-time) | 90-min meeting | BA |
| Analysis review | Credit Risk Lead | Week 4 (one-time) | 60-min walkthrough | BA |
| UAT session | Risk team users | Week 5 (one-time) | 60-min hands-on | BA |
| Final presentation | CRO + all stakeholders | Week 6 (one-time) | 30-min deck | BA |

---

*Document Owner: Gnanesh | Version 1.0 | October 2024*
