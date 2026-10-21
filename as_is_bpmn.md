# As-Is Process Map: Loan Origination & Default Management
## Current State (Before Policy Changes)

---

## BPMN Swimlane Description

*Build this diagram in draw.io or Bizagi using the description below.*

---

### Swimlanes (Left to Right)
1. **Borrower**
2. **Sales / Digital Channel**
3. **Underwriting / Risk Engine**
4. **Credit Risk Team (Manual Review)**
5. **Operations (Disbursement & Servicing)**
6. **Collections**

---

### Process Flow

```
START
  │
  ▼
[Borrower] Submits application online
  │ (Application form: personal details, income, loan amount, purpose)
  ▼
[Sales/Digital] System validates completeness
  │── Incomplete ──► [Borrower] Notified to re-submit ──► Loop back
  │
  ▼ Complete
[Sales/Digital] Soft credit bureau pull (no impact on score)
  │
  ▼
[Underwriting/Risk Engine] Automated rules check
  │  Rule 1: CIBIL score ≥ 680?
  │  Rule 2: DTI ≤ 40%?
  │  Rule 3: No active delinquency?
  │  Rule 4: Minimum income threshold met?
  │
  │── Any rule fails ──► AUTO-REJECT ──► [Borrower] Rejection notice sent
  │                                       ► (Rejection reason documented)
  │
  ▼ All rules pass
[Underwriting/Risk Engine] Grade assigned (A–G via scoring model)
  │
  │── Grade A–C ──► AUTO-APPROVE (no manual review)
  │
  │── Grade D–E ──► [Credit Risk Team] MANUAL REVIEW
  │                  ├── Review income documents
  │                  ├── Verify employment (if salaried)
  │                  ├── Check for fraud flags
  │                  └── Decision: Approve / Reject / Modify terms
  │
  │── Grade F–G ──► [Credit Risk Team] SENIOR REVIEW
  │                  ├── All Grade D–E checks PLUS
  │                  ├── 2nd senior sign-off required
  │                  └── Decision: Approve / Reject
  │
  ▼ Approved
[Operations] Loan agreement generated and sent to borrower
  │
  ▼
[Borrower] Reviews and signs agreement (e-sign)
  │── No sign in 48hrs ──► Auto-cancel
  │
  ▼ Signed
[Operations] Disbursement initiated (T+1 same bank / T+2 other bank)
  │
  ▼
[Operations] EMI schedule created; repayment reminders set up
  │
  ▼
[Borrower] Makes monthly EMI payments via auto-debit
  │
  │── On time ──► Continue repayment cycle ──► [Operations] Loan Closed (Fully Paid)
  │
  │── 1–29 DPD ──► [Operations] SMS/email reminder sent
  │
  │── 30 DPD ──► [Collections] Soft collections (call + email)
  │
  │── 60 DPD ──► [Collections] Hard collections (field agent)
  │
  │── 90 DPD ──► [Collections] NPA classification
  │               ├── Legal notice sent
  │               └── Loan marked Charged Off in system
  │
END
```

---

## Pain Points Identified (Current State)

| # | Pain Point | Where in Process | Business Impact |
|---|-----------|-----------------|-----------------|
| P-01 | Income verification is inconsistent — some approvers skip it during high-volume periods (e.g., festive season) | Manual review step | High — "Not Verified" income borrowers default at 2.1x the rate |
| P-02 | Grade F–G loans require senior sign-off but are still approved in volume — senior reviewer is bottlenecked | Senior review step | High — F/G grades contribute 18% of defaults at 6% of volume |
| P-03 | DTI is calculated at approval but not re-verified if income document is submitted later | Rules check step | Medium — declared DTI may be understated |
| P-04 | No early warning signal dashboard — collections only act at 30 DPD | Collections step | Medium — first EMI miss predicts default but is not tracked proactively |
| P-05 | Rejection reason is documented in the system but not standardised — hard to audit | Rejection step | Low-Medium — compliance risk |

---

## Process Metrics (Current State)

| Metric | Value |
|--------|-------|
| Average application-to-disbursement time | 3.2 days |
| Auto-approval rate (Grade A–C) | 51% |
| Manual review rate (Grade D–E) | 41% |
| Senior review rate (Grade F–G) | 8% |
| Overall approval rate | 68% |
| 90+ DPD default rate | 6.5% |

---

*As-Is map v1.0 — Gnanesh, October 2024*
*Build in draw.io: File → New → Extras → Edit Diagram → paste BPMN XML (to be added)*
