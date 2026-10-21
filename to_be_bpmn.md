# To-Be Process Map: Loan Origination & Default Management
## Future State (After Recommended Policy Changes)

---

## Changes from As-Is to To-Be

| Change | Addresses Pain Point | Expected Impact |
|--------|---------------------|-----------------|
| DTI cutoff tightened: 40% → 35% | P-03 | Reduces high-DTI approvals; projects default rate to ~5.4% |
| Grade F–G originations suspended | P-02 | Removes highest-risk segment; projects 18% fewer defaults |
| Income verification mandatory for loans >₹1 lakh | P-01 | Reduces "Not Verified" approvals; targets festive-season-type risk |
| Early Warning dashboard at first EMI miss | P-04 | Enables proactive collections before 30 DPD |
| Standardised rejection reason codes | P-05 | Improves compliance audit trail |

---

## BPMN Swimlane Description (To-Be)

*Changes from As-Is are marked with 🔄 NEW / CHANGED*

---

### Swimlanes (same as As-Is)
1. Borrower
2. Sales / Digital Channel
3. Underwriting / Risk Engine
4. Credit Risk Team (Manual Review)
5. Operations (Disbursement & Servicing)
6. Collections / Early Warning

---

### Process Flow

```
START
  │
  ▼
[Borrower] Submits application online
  │
  ▼
[Sales/Digital] System validates completeness
  │
  ▼
[Sales/Digital] Soft credit bureau pull
  │
  ▼
[Underwriting/Risk Engine] Automated rules check
  │  Rule 1: CIBIL score ≥ 680? (unchanged)
  │  Rule 2: DTI ≤ 35%? 🔄 CHANGED (was 40%)
  │  Rule 3: No active delinquency? (unchanged)
  │  Rule 4: Minimum income threshold met? (unchanged)
  │  Rule 5: Grade is A–E? 🔄 NEW (F–G suspended)
  │
  │── Any rule fails ──► AUTO-REJECT
  │                       ► 🔄 Rejection reason from standardised code list
  │                       ► [Borrower] Rejection notice with reason code
  │
  ▼ All rules pass
[Underwriting/Risk Engine] Grade assigned (A–G)
  │
  │── Grade F or G ──► 🔄 AUTO-REJECT (originations suspended)
  │                     ► Rejection reason: "Grade below current policy threshold"
  │
  │── Grade A–C ──► AUTO-APPROVE
  │
  │── Grade D–E ──► [Credit Risk Team] MANUAL REVIEW
  │                  ├── 🔄 Income verification MANDATORY if loan >₹1 lakh
  │                  ├── Employment verification (salaried: salary slip + bank statement)
  │                  ├── Re-calculate DTI from verified income (not declared income)
  │                  │     └── If verified DTI > 35%: REJECT
  │                  └── Decision: Approve / Reject
  │
  ▼ Approved
[Operations] Loan agreement and disbursement (same as As-Is)
  │
  ▼
[Borrower] Makes monthly EMI payments
  │
  │── On time ──► Continue; loan closed when fully paid
  │
  │── 🔄 FIRST EMI MISSED ──► [Collections/Early Warning] 🔄 PROACTIVE ALERT
  │                              ├── System flags: "First EMI miss — high default predictor"
  │                              ├── Collections agent assigned within 24 hours
  │                              └── Soft contact (call + WhatsApp) within 48 hours
  │
  │── 1–29 DPD ──► [Operations] Standard reminder (unchanged)
  │
  │── 30 DPD ──► [Collections] Soft collections
  │
  │── 60 DPD ──► [Collections] Hard collections
  │
  │── 90 DPD ──► NPA / Charged Off (same as As-Is)
  │
END
```

---

## Process Metrics (Projected To-Be)

| Metric | Current (As-Is) | Projected (To-Be) | Change |
|--------|----------------|-------------------|--------|
| Average approval-to-disbursement time | 3.2 days | 3.6 days | +0.4 days (income verification adds time) |
| Auto-approval rate | 51% | 51% | Unchanged (Grade A–C unaffected) |
| Manual review rate | 41% | 41% | Unchanged |
| Grade F–G approval rate | 8% of volume | 0% | Suspended |
| Overall approval rate | 68% | ~60% | ~12% reduction |
| 90+ DPD default rate | 6.5% | ~4.8% (projected) | −1.7 pp |
| First EMI miss → proactive contact | Not tracked | <48 hours | New metric |

---

## Change Impact Summary

| Stakeholder | Impact | Sentiment |
|-------------|--------|-----------|
| Credit Risk Lead | Default rate reduced; more consistent review process | Positive |
| Collections Team | Proactive alert means earlier, easier recovery | Positive |
| Product Manager | Approval rate drops ~12% — volume pressure | Concerned |
| Sales Head | Fewer disbursals in Grade F–G segment | Negative |
| Compliance Officer | Standardised rejections; income verification mandatory | Very Positive |
| Borrowers (Grade F–G) | Will be declined; directed to other products | Neutral — legally compliant |

---

*To-Be map v1.0 — Gnanesh, November 2024*
