# Lessons Learned Log
## Loan Default Risk Analysis | RISK-2024-001

---

| Document ID | LL-RISK-2024-001 |
|-------------|-----------------|
| Author | Gnanesh (BA) |
| Date | November 2024 |
| Session Attendees | Gnanesh (BA), Credit Risk Lead, Data Engineering Lead |

---

## 1. What Went Well

| # | Observation | Impact |
|---|-------------|--------|
| 1 | **Stakeholder interviews in Week 1 surfaced the festive-season hypothesis early.** This gave the analysis a clear testable hypothesis and saved time on unfocused EDA. | High — directed analysis and saved ~3 days |
| 2 | **Defining the target variable (default flag) before analysis started** prevented ambiguity later. The team agreed upfront that "Charged Off" = default, and "Current" loans would be excluded. | High — no rework needed |
| 3 | **Weekly status emails with RAG status** kept the CRO informed and prevented surprise escalations. The bi-weekly 15-minute risk review was efficient. | Medium |
| 4 | **BRD version control** (tracking changes from v1.0 to v1.1 after compliance interview) demonstrated professional BA practice and gave an audit trail. | Medium |
| 5 | **Framing recommendations as options with trade-off tables** made the CRO's decision easy. The data was trusted because the methodology was documented. | High |

---

## 2. What Could Be Improved

| # | Observation | Root Cause | Recommendation |
|---|-------------|-----------|----------------|
| 1 | **Data extract was delayed by 3 days** because the data request lacked a formal specification. | No standard data request template. | Create a Data Request Template with required fields, format, and lineage requirements. Use for all future analytics projects. |
| 2 | **Income band definition was changed after EDA had started.** Credit Risk Lead wanted a different bucketing than what was in the data dictionary. | Income bands were defined without Credit Risk Lead input. | Include domain SME in KPI/definition workshops before analysis starts. |
| 3 | **UAT took longer than planned.** Business users needed more guidance on the scenario analysis page. | No user training planned as part of delivery. | Add a 30-minute "dashboard walkthrough" session before formal UAT for all non-technical users. |
| 4 | **Selection bias was documented late** (Week 4 rather than Week 1). | BA was not aware of this limitation at project start. | Add "selection bias check" as a standard item on the project initiation checklist for all lending analytics projects. |
| 5 | **Requirements Traceability Matrix (RTM) was maintained inconsistently.** Some FRs were not linked back to BRs until Week 5. | RTM updates were an afterthought, not a workflow habit. | Update RTM every time a new requirement or story is written. Treat it as a living document, not a sign-off artifact. |

---

## 3. Open Items at Project Close

| # | Item | Owner | Due Date |
|---|------|-------|----------|
| 1 | D-001 Dashboard defect: Grade G bar not highlighted red | BI Developer | Sprint +1 |
| 2 | Income verification process update (Operations) | Operations Lead | Month 2 |
| 3 | Month 1 policy review meeting (check actual volume impact) | Credit Risk Lead | Month 1 post-go-live |
| 4 | RTM to be finalised and filed with BRD | Gnanesh | This week |

---

## 4. Recommendations for Future Projects

1. **Always interview the Collections team first.** They have the best real-world knowledge of what defaulters look like. Their insights (first EMI miss pattern, income verification issues) shaped two of the four recommendations.

2. **State limitations in the project charter, not just the final report.** The selection bias limitation was known from the start but only formally documented in Week 4. Stakeholders should understand limitations before analysis begins.

3. **Build the scenario analysis early.** Business stakeholders engage much more readily with a "slider and outcome" view than with a table of numbers. Having a basic scenario tool in Week 3 would have accelerated stakeholder buy-in.

4. **Distinguish BA deliverables from data science deliverables clearly.** There was brief confusion in Week 3 about whether this project would produce a predictive model. The scope boundary should be agreed in the charter and re-stated at the requirements workshop.

---

## 5. Project Summary Scorecard

| Criterion | Target | Actual | Status |
|-----------|--------|--------|--------|
| Default rate reduction (projected) | ≤5.0% | ~4.8% (projected) | ✅ Met |
| Approval volume impact | <10% reduction | ~12% (phased) | ⚠️ Slightly above; mitigated by phasing |
| Dashboard delivery | Week 6 | Week 6 | ✅ On time |
| Timeline | 6 weeks | 6 weeks | ✅ On time |
| Stakeholder sign-off (all required) | 100% | 100% | ✅ Met |
| Compliance approval | Required | Obtained | ✅ Met |

---

*Lessons Learned v1.0 — Gnanesh, November 2024*
