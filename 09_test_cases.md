# Test Cases & UAT Sign-off
## Credit Risk Dashboard | RISK-2024-001

---

| Document ID | TC-RISK-2024-001 |
|-------------|-----------------|
| Author | Gnanesh (BA) |
| Environment | UAT |
| Version | 1.0 |
| Date | November 2024 |

---

## Test Approach

**UAT Session:** 60 minutes, facilitated by BA, with 3 Risk team users
**Test Types:**
- Functional testing: does the feature do what the user story says?
- Data accuracy testing: do dashboard numbers match SQL source?
- Usability testing: can a non-technical user operate the dashboard?

**Pass Criteria:** All P1 (Critical) and P2 (High) test cases must pass. P3 (Medium) defects may remain with owner and fix date agreed.

---

## Test Cases

### Page 1: Portfolio Overview

| TC ID | User Story | Test Scenario | Test Steps | Expected Result | Priority | Status | Notes |
|-------|-----------|--------------|------------|-----------------|----------|--------|-------|
| TC-01 | US-01 | Default rate KPI displays correctly | 1. Open dashboard. 2. View Page 1. | KPI card shows "6.5%" with "▲0.3% vs prior period" in red | P1 | PASS / FAIL | |
| TC-02 | US-01 | Default rate matches SQL | 1. Run `analysis_queries.sql` query 1. 2. Compare to dashboard KPI. | Dashboard value ≤0.1% difference from SQL result | P1 | PASS / FAIL | |
| TC-03 | US-02 | Amber alert at 6.0% threshold | 1. Set alert threshold to 6.0%. 2. Check banner. | Amber banner appears with text "Default rate (6.5%) exceeds threshold (6.0%)" | P1 | PASS / FAIL | |
| TC-04 | US-02 | Red alert at 7.0% default rate | 1. Temporarily filter to Grade F–G only (simulates high-risk subset). 2. Check banner. | Red banner appears | P2 | PASS / FAIL | |
| TC-05 | US-03 | Trend line shows 12 months | 1. Open Page 1. 2. Inspect trend chart. | 12 monthly data points; x-axis labelled by month; hover tooltip shows rate + count | P1 | PASS / FAIL | |
| TC-06 | US-03 | Trend line responds to date filter | 1. Change date range to last 6 months. 2. Inspect chart. | Chart updates to show only 6 data points | P2 | PASS / FAIL | |

---

### Page 2: Segment Analysis

| TC ID | User Story | Test Scenario | Test Steps | Expected Result | Priority | Status | Notes |
|-------|-----------|--------------|------------|-----------------|----------|--------|-------|
| TC-07 | US-04 | Default rate by grade shows all 7 grades | 1. Open Page 2. 2. Inspect grade chart. | 7 bars (A–G); default rates increase from A to G | P1 | PASS / FAIL | |
| TC-08 | US-04 | High-risk grades highlighted in red | 1. Inspect grade chart. | Grades with rate ≥2x portfolio average are shown in red | P2 | PASS / FAIL | |
| TC-09 | US-04 | Grade chart shows loan count | 1. Hover over grade D bar. | Tooltip shows: Grade D, Default Rate 14.3%, Loan Count [n] | P1 | PASS / FAIL | |
| TC-10 | US-04 | Clicking grade filters all charts | 1. Click on Grade E bar. | All charts on Page 2 filter to Grade E loans | P2 | PASS / FAIL | |
| TC-11 | US-05 | Purpose chart shows top 10 purposes | 1. Open Page 2. 2. Inspect purpose chart. | 10 bars, sorted by default rate descending; "Other" category if applicable | P2 | PASS / FAIL | |
| TC-12 | US-06 | Income band chart shows 4 bands | 1. Inspect income band chart. | 4 bars: ≤₹3L, ₹3–6L, ₹6–10L, >₹10L | P1 | PASS / FAIL | |

---

### Page 3: Vintage Analysis

| TC ID | User Story | Test Scenario | Test Steps | Expected Result | Priority | Status | Notes |
|-------|-----------|--------------|------------|-----------------|----------|--------|-------|
| TC-13 | US-07 | Heatmap renders correctly | 1. Open Page 3. | Heatmap displays with origination months on rows, months-on-book on columns; darker = higher default rate | P1 | PASS / FAIL | |
| TC-14 | US-07 | Oct–Dec months are labelled | 1. Inspect heatmap row labels for Oct, Nov, Dec. | Star icon or label next to festive season months | P3 | PASS / FAIL | |
| TC-15 | US-07 | Hovering shows tooltip | 1. Hover on Jan 2023, 9 months on book. | Tooltip shows: "Jan-23 | 9 months | Default rate: X% | n loans" | P1 | PASS / FAIL | |

---

### Page 4: Scenario Analysis

| TC ID | User Story | Test Scenario | Test Steps | Expected Result | Priority | Status | Notes |
|-------|-----------|--------------|------------|-----------------|----------|--------|-------|
| TC-16 | US-08 | DTI slider at 35% shows correct impact | 1. Open Page 4. 2. Move slider to 35%. | "After" KPI shows lower default rate and lower approval volume vs "Before" | P2 | PASS / FAIL | |
| TC-17 | US-08 | Disclaimer is visible | 1. Open Page 4. | Text reads: "Projections assume borrower behaviour does not change. Actual impact may vary." | P2 | PASS / FAIL | |

---

### Access & Data Refresh

| TC ID | User Story | Test Scenario | Test Steps | Expected Result | Priority | Status | Notes |
|-------|-----------|--------------|------------|-----------------|----------|--------|-------|
| TC-18 | US-09 | Refresh date is shown | 1. Open any page. 2. Check header. | "Data last refreshed: [date]" is visible | P1 | PASS / FAIL | |
| TC-19 | US-10 | CRO role cannot see Pages 2 and 4 | 1. Log in as CRO test account. 2. Check navigation. | Pages 2 (Segment) and 4 (Scenario) are hidden or access-restricted | P1 | PASS / FAIL | |
| TC-20 | US-10 | No PII visible on any page | 1. Check all pages, all tooltips, all drill-throughs. | No borrower names, IDs, phone numbers, or emails are visible | P1 | PASS / FAIL | |

---

## Defect Log

| Defect ID | TC ID | Description | Severity | Assigned To | Status | Fix Date |
|-----------|-------|-------------|----------|-------------|--------|----------|
| D-001 | TC-08 | Grade G bar not highlighted red (rate = 33.4%, should be red) | P2 | BI Developer | Open | _____ |
| D-002 | TC-14 | Star icon not showing on Oct row in heatmap | P3 | BI Developer | Open | _____ |

---

## UAT Sign-off

| Tester | Role | Test Date | P1 Cases Pass | P2 Cases Pass | Signature |
|--------|------|-----------|---------------|---------------|-----------|
| [Name 1] | Risk Analyst | Nov 2024 | Yes / No | Yes / No | _____ |
| [Name 2] | Risk Analyst | Nov 2024 | Yes / No | Yes / No | _____ |
| [Name 3] | Credit Risk Lead | Nov 2024 | Yes / No | Yes / No | _____ |

**Overall UAT Decision:** PASS / PASS WITH CONDITIONS / FAIL

**Conditions (if any):** D-001 to be fixed before go-live. D-002 acceptable for go-live with fix in next sprint.

---

*TC v1.0 — Gnanesh, November 2024*
