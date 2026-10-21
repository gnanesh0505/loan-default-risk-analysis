# Functional Requirements Document (FRD)
## Credit Risk Monitoring Dashboard
### Loan Default Risk Analysis | RISK-2024-001

---

| Field | Details |
|-------|---------|
| **Document ID** | FRD-RISK-2024-001 |
| **Author** | Gnanesh (BA) |
| **Version** | 1.0 |
| **Date** | October 2024 |
| **Linked BRD** | BRD-RISK-2024-001 (BR-04) |

---

## 1. Purpose

This document describes the functional requirements for the Credit Risk Monitoring Dashboard to be delivered to the Risk team at QuickLend Digital Finance. It translates the business requirements in the BRD into specific system behaviors and features.

---

## 2. Dashboard Overview

The dashboard will be built in Power BI (or Tableau). It will provide the Credit Risk team with a self-service view of loan default trends, segment-level breakdowns, and early warning indicators — without requiring them to run SQL queries or wait for ad-hoc reports.

**Primary users:** Credit Risk Lead, Risk Analysts (up to 5 users)
**Secondary users:** CRO (read-only, monthly summary view)
**Data refresh:** Weekly (every Monday, 8:00 AM)

---

## 3. Functional Requirements

### Page 1: Portfolio Overview

| FR ID | Requirement | Priority |
|-------|-------------|----------|
| FR-01 | Display current 90+ DPD default rate as a KPI card, with vs. prior period change (↑/↓ with % change) | Must Have |
| FR-02 | Display current approval rate as a KPI card | Must Have |
| FR-03 | Display NPL ratio as a KPI card | Must Have |
| FR-04 | Display total loans originated in selected period as a KPI card | Must Have |
| FR-05 | Display a line chart showing monthly default rate trend for the past 12 months | Must Have |
| FR-06 | Display an alert banner (amber/red) when default rate exceeds user-defined threshold (default: 6%) | Must Have |
| FR-07 | Allow user to set alert threshold via a settings panel | Should Have |

---

### Page 2: Segment Analysis

| FR ID | Requirement | Priority |
|-------|-------------|----------|
| FR-08 | Display default rate by loan grade (A–G) as a bar chart | Must Have |
| FR-09 | Display default rate by loan purpose as a bar chart (top 10 purposes) | Must Have |
| FR-10 | Display default rate by income band (≤₹3L, ₹3–6L, ₹6–10L, >₹10L annual) as a bar chart | Must Have |
| FR-11 | Display default rate by employment type (salaried / self-employed / other) | Must Have |
| FR-12 | Display default rate by home ownership (rent / own / mortgage) | Should Have |
| FR-13 | All segment charts must show both default rate AND loan count (dual axis or tooltip) to avoid misleading with small samples | Must Have |
| FR-14 | Highlight bars that are ≥2x the portfolio average default rate in red | Should Have |

---

### Page 3: Vintage Analysis

| FR ID | Requirement | Priority |
|-------|-------------|----------|
| FR-15 | Display a heatmap of default rate by origination month (rows) and months-on-book (columns) | Must Have |
| FR-16 | Allow user to select a specific vintage cohort and see its default rate curve over time | Should Have |
| FR-17 | Overlay the festive season origination period (Oct–Dec) as a shaded region on all time-series charts | Could Have |

---

### Page 4: Scenario Analysis

| FR ID | Requirement | Priority |
|-------|-------------|----------|
| FR-18 | Allow user to simulate a DTI cutoff change using a slider (0–50%) and see projected impact on default rate and approval volume | Should Have |
| FR-19 | Allow user to simulate a loan grade exclusion (e.g., exclude Grade F–G) and see impact | Should Have |
| FR-20 | Display scenario results as before/after KPI comparison cards | Should Have |

---

## 4. Filters (Global, apply to all pages)

| FR ID | Filter | Options |
|-------|--------|---------|
| FR-21 | Date range — origination date | Date picker (default: last 12 months) |
| FR-22 | Loan grade | Multi-select: A, B, C, D, E, F, G |
| FR-23 | Loan purpose | Multi-select: all purposes |
| FR-24 | Employment type | Multi-select: Salaried, Self-employed, Other |
| FR-25 | Loan term | Multi-select: 36 months, 60 months |
| FR-26 | Reset filters button | Clears all filters to default |

---

## 5. Non-Functional Requirements

| NFR ID | Requirement |
|--------|------------|
| NFR-01 | Dashboard must load within 5 seconds for a 12-month date range on a standard browser |
| NFR-02 | Data refresh must complete by 8:00 AM every Monday without manual intervention |
| NFR-03 | Role-based access: Risk team can view and interact; CRO has read-only access; no other users |
| NFR-04 | No PII (borrower name, ID, phone number) to appear anywhere in the dashboard |
| NFR-05 | Dashboard must render correctly on Chrome and Edge (desktop) |
| NFR-06 | All charts must be colour-blind accessible (no red/green only distinction) |

---

## 6. Data Requirements

| Field | Source | Used In |
|-------|--------|---------|
| `loan_id` | Loan origination system | Record count |
| `loan_amnt` | Loan origination system | Portfolio value, EL |
| `int_rate` | Loan origination system | Revenue calculation |
| `grade` | Credit model | Segment analysis |
| `annual_inc` | Application form | Income band segmentation |
| `dti` | Application form | DTI analysis |
| `emp_length` | Application form | Employment segmentation |
| `home_ownership` | Application form | Segment analysis |
| `purpose` | Application form | Segment analysis |
| `term` | Loan origination system | Portfolio filter |
| `issue_d` | Loan origination system | Vintage analysis |
| `loan_status` | Collections system | Default flag |
| `last_pymnt_d` | Collections system | Vintage analysis |

---

## 7. Assumptions

- The BI developer will build the dashboard from this specification.
- Data will be made available as a refreshed extract in the agreed format by the Data Engineering team.
- The dashboard is not connected to a live transactional database; it uses a weekly snapshot.

---

## 8. Sign-off

| Role | Name | Decision | Date |
|------|------|----------|------|
| Credit Risk Lead | [Name] | Approved / Pending | _____ |
| BI Developer | [Name] | Accepted for build | _____ |
| BA | Gnanesh | Submitted | Oct 2024 |

---

*FRD Version 1.0 — Gnanesh, October 2024*
