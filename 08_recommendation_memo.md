# Recommendation Memo
## Loan Default Risk Analysis
### To: Chief Risk Officer | From: Gnanesh, Business Analyst

---

| Field | Details |
|-------|---------|
| **Document ID** | REC-RISK-2024-001 |
| **Date** | November 2024 |
| **Classification** | Internal — Confidential |
| **Version** | 1.0 |

---

## 1. Problem Recap

QuickLend Digital Finance's 90+ DPD default rate increased from **5.1% to 6.5%** over Q2–Q3 FY2024, resulting in an estimated additional ₹3.8 crore in quarterly credit losses. This memo presents the key findings from the 6-week analysis and recommends two policy changes.

---

## 2. Key Findings

### Finding 1: Grade D–G borrowers account for 61% of all defaults but only 28% of loan volume

| Grade | Default Rate | % of Portfolio | % of Total Defaults |
|-------|-------------|----------------|---------------------|
| A | 3.1% | 22% | 7% |
| B | 5.2% | 31% | 16% |
| C | 7.8% | 19% | 15% |
| D | 14.3% | 14% | 20% |
| E | 21.6% | 8% | 17% |
| F | 28.1% | 4% | 11% |
| G | 33.4% | 2% | 7% |

**Insight:** Grades F and G have default rates more than 4x the portfolio average. Their combined volume is only 6% of the book, but they contribute 18% of defaults. Tightening criteria for these grades offers the best risk-to-volume trade-off.

---

### Finding 2: High DTI is the single strongest predictor of default

| DTI Band | Default Rate |
|----------|-------------|
| 0–15% | 8.4% |
| 15–25% | 11.2% |
| 25–35% | 16.8% |
| 35–40% | 21.4% |
| 40%+ | 27.9% |

**Insight:** Borrowers with DTI between 35–40% default at 21.4% — nearly 1 in 5. The current policy allows DTI up to 40%. Borrowers above 35% DTI represent 19% of originations but 32% of defaults.

---

### Finding 3: The festive-season cohort (Oct–Dec 2023) shows significantly elevated default rates

Vintage analysis reveals that loans originated in October–December 2023 (festive season lending campaign) are defaulting at a rate of **22.6%** at 9 months on book — compared to **14.1%** for loans originated in the same months of the prior year.

**Insight:** The campaign approval criteria were relaxed to increase volume. This cohort is likely the primary driver of the Q2–Q3 FY2024 default spike.

---

### Finding 4: Not-verified income borrowers default at 2.1x the rate of verified borrowers

| Verification Status | Default Rate |
|--------------------|-------------|
| Verified | 9.8% |
| Source Verified | 12.4% |
| Not Verified | 20.6% |

**Insight:** Income verification quality is a strong predictor. The festive-season campaign deprioritised verification in the interest of speed. This should be a mandatory step for all loans above a threshold amount.

---

## 3. Options Analysis

### Option A: Tighten DTI cutoff from 40% to 35%
**Rule change:** Reject applications where DTI > 35% (all grades)

| Impact | Estimate |
|--------|---------|
| Default rate reduction | ~6.5% → ~5.4% |
| Approval volume reduction | ~9% (approximately 580 fewer approvals/month) |
| Monthly revenue impact | −₹42 lakhs (net interest income) |
| Monthly loss reduction | +₹68 lakhs (reduced credit losses) |
| **Net monthly benefit** | **+₹26 lakhs** |
| Compliance risk | Low — DTI is a standard, non-discriminatory criterion |

---

### Option B: Suspend new originations in Grade F and G
**Rule change:** Decline all applications scoring Grade F or G until further review

| Impact | Estimate |
|--------|---------|
| Default rate reduction | ~6.5% → ~5.8% |
| Approval volume reduction | ~6% (approximately 390 fewer approvals/month) |
| Monthly revenue impact | −₹28 lakhs |
| Monthly loss reduction | +₹52 lakhs |
| **Net monthly benefit** | **+₹24 lakhs** |
| Compliance risk | Low — grade is an internally assigned risk score; no protected attribute |

---

### Option C (Recommended): Combine Options A and B

Apply both changes simultaneously:
- Reject DTI > 35% (all grades)
- Suspend Grade F and G originations

| Impact | Estimate |
|--------|---------|
| Default rate reduction | ~6.5% → ~4.8% (below the 5.0% target) |
| Approval volume reduction | ~12% — slightly above the 10% guardrail |
| Monthly revenue impact | −₹61 lakhs |
| Monthly loss reduction | +₹102 lakhs |
| **Net monthly benefit** | **+₹41 lakhs** |
| Compliance risk | Low |

**Note on volume:** The 12% volume reduction is slightly above the CRO's 10% guardrail. We recommend phasing this over two months: implement Option A in Month 1, and Option B in Month 2, to monitor the actual impact on approvals before the second change takes effect.

---

### Option D: Mandate income verification for all loans above ₹1 lakh
**Rule change:** Any application for ₹1 lakh or more must have `verification_status = Verified` before approval

| Impact | Estimate |
|--------|---------|
| Default rate reduction | ~0.8% (partial, as this addresses one root cause) |
| Approval volume impact | ~4% slower processing (verification adds 1–2 days) |
| Compliance benefit | High — strengthens RBI KYC compliance posture |

**Recommendation:** Implement Option D alongside Option C as it targets a root cause, not a symptom.

---

## 4. Recommendation

**Implement Option C (DTI ≤35% + Grade F/G suspension) phased over 2 months, combined with Option D (mandatory income verification above ₹1 lakh).**

**Rationale:**
- Combined net benefit of ₹41 lakhs/month exceeds the revenue cost.
- Phased rollout keeps volume impact within the CRO's guardrail.
- All criteria are explainable and RBI-compliant.
- Income verification (Option D) addresses the root cause of the festive-season cohort's elevated defaults.

---

## 5. Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Actual volume drop exceeds 12% | Medium | High | Monthly review after Month 1; rollback clause if drop exceeds 15% |
| Competitor gains share in Grade D–E segment | Medium | Medium | Accept as trade-off; growth can resume once default rate stabilises |
| Compliance challenge to grade exclusion | Low | Medium | Document business rationale; credit grade is internally assigned and non-discriminatory |
| Operational delay in verification | Medium | Medium | Work with Ops to reduce verification TAT from 2 days to 1 day using automated bureau pull |

---

## 6. Next Steps

| Action | Owner | Due Date |
|--------|-------|----------|
| CRO approves recommendation | CRO | Week 6 |
| Compliance sign-off on Options A, B, D | Compliance Officer | Week 6 |
| Rules engine change request raised | Product Manager | Week 7 |
| Income verification process updated | Operations Lead | Week 8 |
| Month 1 policy review meeting scheduled | Credit Risk Lead | Week 10 |

---

## 7. Sign-off Required

| Role | Name | Decision | Date |
|------|------|----------|------|
| CRO | [Name] | Approved / Rejected / Escalated | _____ |
| Compliance Officer | [Name] | Approved / Rejected | _____ |
| Credit Risk Lead | [Name] | Noted | _____ |

---

*Memo prepared by Gnanesh (BA) | November 2024 | Internal — Confidential*
