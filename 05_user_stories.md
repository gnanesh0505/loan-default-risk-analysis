# User Stories with Acceptance Criteria
## Loan Default Risk Analysis | RISK-2024-001

---

| Document ID | US-RISK-2024-001 |
|-------------|-----------------|
| Author | Gnanesh (BA) |
| Version | 1.0 |
| Date | October 2024 |

---

## Personas

| Persona | Role | Goal |
|---------|------|------|
| **Priya** | Credit Risk Lead | Wants to quickly see which segments are driving defaults and act on them |
| **Arjun** | Risk Analyst | Wants to run deep-dive segment analysis without writing SQL |
| **Ramesh** | CRO (Sponsor) | Wants a high-level view of default trends to inform board reporting |
| **Compliance Officer** | Reviewer | Wants to verify that recommendations are RBI-compliant |

---

## Epic 1: Portfolio Overview Dashboard

### US-01: View current default rate
**As a** Credit Risk Lead (Priya),
**I want to** see the current 90+ DPD default rate on the dashboard homepage,
**so that** I can immediately know if the portfolio is improving or worsening.

**Acceptance Criteria:**
- [ ] Default rate KPI card is visible on Page 1 without scrolling
- [ ] Card shows current rate (e.g., 6.5%) and delta vs. prior period (e.g., ▲0.3%)
- [ ] Delta is shown in red if rate increased, green if decreased
- [ ] Rate is calculated as: loans in Charged Off status ÷ total loans originated in the same vintage
- [ ] Card updates with every weekly data refresh

**Priority:** Must Have
**Story Points:** 3

---

### US-02: Receive alert when default rate is critical
**As a** Credit Risk Lead (Priya),
**I want to** see a visible alert banner when the default rate exceeds a threshold,
**so that** I am not caught off guard by a spike between my regular check-ins.

**Acceptance Criteria:**
- [ ] Amber banner appears when default rate is between 6.0% and 6.9%
- [ ] Red banner appears when default rate is ≥7.0%
- [ ] Banner includes the current rate and the threshold it exceeded
- [ ] I can set my own threshold value in a settings panel
- [ ] No banner appears when rate is below my threshold

**Priority:** Must Have
**Story Points:** 5

---

### US-03: View 12-month default rate trend
**As a** Risk Analyst (Arjun),
**I want to** see a monthly default rate trend line for the past 12 months,
**so that** I can see whether the increase is gradual or was triggered by a specific month.

**Acceptance Criteria:**
- [ ] Line chart shows one data point per month for the past 12 months
- [ ] X-axis = origination month; Y-axis = default rate (%)
- [ ] Hovering on a data point shows exact rate and loan count
- [ ] Chart is responsive to the date range filter
- [ ] Chart includes a reference line at the portfolio-average default rate

**Priority:** Must Have
**Story Points:** 3

---

## Epic 2: Segment Analysis

### US-04: Identify highest-risk loan grades
**As a** Credit Risk Lead (Priya),
**I want to** see the default rate broken down by loan grade (A–G),
**so that** I can identify which grades carry the most risk and consider grade-based policy changes.

**Acceptance Criteria:**
- [ ] Bar chart shows default rate per grade (A, B, C, D, E, F, G)
- [ ] Each bar also shows the loan count (dual axis or tooltip)
- [ ] Bars for grades with default rate ≥2x portfolio average are highlighted in red
- [ ] Clicking a grade filters all other charts to that grade
- [ ] Grades with fewer than 100 loans in the period are labelled "Low volume — interpret with caution"

**Priority:** Must Have
**Story Points:** 5

---

### US-05: Analyse default rate by loan purpose
**As a** Risk Analyst (Arjun),
**I want to** see the default rate by loan purpose (debt consolidation, home improvement, etc.),
**so that** I can identify whether certain loan uses carry systematically higher risk.

**Acceptance Criteria:**
- [ ] Bar chart shows the top 10 purposes by loan volume
- [ ] Each bar shows default rate AND loan count
- [ ] Chart is sorted by default rate descending by default
- [ ] Tooltip shows: purpose name, default rate %, loan count, % of total portfolio
- [ ] Purposes with <50 loans are grouped as "Other"

**Priority:** Must Have
**Story Points:** 3

---

### US-06: Analyse default rate by income band
**As a** Risk Analyst (Arjun),
**I want to** see default rates across income bands (low / medium / high / very high),
**so that** I can assess whether income is a reliable predictor of default in our portfolio.

**Acceptance Criteria:**
- [ ] Income bands: ≤₹3L, ₹3–6L, ₹6–10L, >₹10L (annual)
- [ ] Bar chart shows default rate per band with loan count
- [ ] Analysis excludes rows where income = NULL or income > ₹1Cr (assumed outlier)
- [ ] Tooltip shows band, rate, count, and average loan amount in band

**Priority:** Must Have
**Story Points:** 3

---

## Epic 3: Vintage Analysis

### US-07: Identify which origination cohorts have high default rates
**As a** Credit Risk Lead (Priya),
**I want to** see a vintage analysis heatmap of default rate by origination month,
**so that** I can determine whether the default increase is linked to a specific lending campaign or time period.

**Acceptance Criteria:**
- [ ] Heatmap shows origination months (rows) vs. months-on-book (columns)
- [ ] Cell colour intensity represents default rate (darker = higher)
- [ ] Hovering on a cell shows: cohort, months-on-book, default rate, loan count
- [ ] Festive season months (October, November, December) are labelled with a star icon
- [ ] Heatmap covers the last 12 origination months

**Priority:** Must Have
**Story Points:** 8

---

## Epic 4: Scenario Analysis

### US-08: Simulate the impact of a DTI cutoff change
**As a** Credit Risk Lead (Priya),
**I want to** simulate the effect of tightening the DTI cutoff (e.g., from 40% to 35%),
**so that** I can assess how much risk we reduce and how many approvals we lose before committing to the policy change.

**Acceptance Criteria:**
- [ ] Slider allows selection of DTI threshold from 20% to 50% in 1% increments
- [ ] Default position is current policy (40%)
- [ ] Moving slider updates two KPI cards: projected default rate and projected approval rate
- [ ] Results show "before" and "after" side by side
- [ ] Calculations are based on the currently filtered date range
- [ ] Page includes disclaimer: "Projections assume borrower behaviour does not change. Actual impact may vary."

**Priority:** Should Have
**Story Points:** 8

---

## Epic 5: Data Refresh and Access

### US-09: Access fresh data every Monday
**As a** Credit Risk Lead (Priya),
**I want to** know the dashboard uses data updated as of last Monday,
**so that** I can trust the numbers I am acting on.

**Acceptance Criteria:**
- [ ] Dashboard header shows "Data last refreshed: [date and time]"
- [ ] Refresh occurs automatically every Monday at 8:00 AM
- [ ] If refresh fails, an amber banner reads "Data refresh pending — figures may be outdated"
- [ ] BA confirms refresh schedule with Data Engineering team before go-live

**Priority:** Must Have
**Story Points:** 3

---

### US-10: Access dashboard securely
**As a** CRO (Ramesh),
**I want to** view a read-only summary version of the dashboard,
**so that** I can review portfolio health for board reporting without accidentally changing filters.

**Acceptance Criteria:**
- [ ] CRO role cannot modify filters or settings
- [ ] CRO view shows Page 1 (Portfolio Overview) and Page 3 (Vintage Analysis) only
- [ ] Risk Analyst role has full access to all pages and filters
- [ ] No borrower-level PII appears on any page visible to any role

**Priority:** Must Have
**Story Points:** 5

---

## Story Summary

| Epic | Stories | Total Points |
|------|---------|--------------|
| Portfolio Overview | US-01, US-02, US-03 | 11 |
| Segment Analysis | US-04, US-05, US-06 | 11 |
| Vintage Analysis | US-07 | 8 |
| Scenario Analysis | US-08 | 8 |
| Data & Access | US-09, US-10 | 8 |
| **Total** | **10** | **46** |

---

## Definition of Done (DoD)

A user story is complete when:
1. The feature is built and deployed in the UAT environment
2. All acceptance criteria are verified and checked off
3. A Risk team user has tested the story in UAT and confirmed it passes
4. No open P1 or P2 defects exist on this story
5. Data matches the underlying SQL query output (spot-checked by BA)

---

*Document Owner: Gnanesh | Version 1.0 | October 2024*
