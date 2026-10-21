# Dashboard Mockup Specification
## Credit Risk Monitoring Dashboard — Power BI
### Loan Default Risk Analysis | RISK-2024-001

---

Use this spec to recreate the dashboard mockup in Figma, PowerPoint, or directly in Power BI.

---

## Page 1: Portfolio Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  QUICKLEND CREDIT RISK DASHBOARD                    [Filters ▼] │
│  Data refreshed: Monday 04 Nov 2024 08:00 AM                    │
├──────────┬──────────┬──────────┬──────────────────────────────  │
│ 🔴 ALERT │          │          │                                 │
│ Default  │ Approval │  NPL     │  Default Rate Trend (12M)       │
│ Rate     │ Rate     │  Ratio   │  ━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│  6.5% ▲  │  68.2%   │  4.1%   │  [Line chart: monthly]         │
│ +0.3% vs │  -1.2%   │ +0.5%   │  - - - Portfolio avg (5.8%)    │
│ prior    │          │          │                                 │
├──────────┴──────────┴──────────┴──────────────────────────────  │
│  Total Loans: 6,521 this month  |  Total Disbursed: ₹118.4 Cr  │
└─────────────────────────────────────────────────────────────────┘

KPI Card Colours:
- Default rate rising → Red card border
- Default rate falling → Green card border
- Neutral/stable → Grey card border

Alert Banner (when triggered):
- Amber: "⚠️ Default rate (6.5%) has exceeded your alert threshold (6.0%)"
- Red:   "🚨 Default rate (7.2%) is critically elevated. Immediate review recommended."
```

---

## Page 2: Segment Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│  SEGMENT ANALYSIS                              [Global filters] │
├──────────────────────────┬──────────────────────────────────── │
│  Default Rate by Grade   │  Default Rate by Purpose (Top 10)   │
│                          │                                      │
│  G ████████████████ 33%  │  small_business ██████████ 28%      │
│  F ██████████████  28%   │  debt_consolidation ███████ 20%     │
│  E ████████        22%   │  credit_card  █████████   18%       │
│  D ██████          14%   │  ...                                 │
│  C ████             8%   │                                      │
│  B ███              5%   │  [Red bars = ≥2x portfolio avg]     │
│  A ██               3%   │                                      │
│                          │                                      │
│  Grey line = o  Loan cnt │                                      │
├──────────────────────────┴──────────────────────────────────── │
│  Default Rate by Income Band    │  Default Rate by Verification │
│  Low     █████████████    24%   │  Not Verified ████████  21%  │
│  Medium  ████████         16%   │  Source Ver   █████     12%  │
│  High    ████              9%   │  Verified     ████      10%  │
│  V.High  ███               7%   │                              │
└──────────────────────────────────────────────────────────────── │
```

---

## Page 3: Vintage Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│  VINTAGE ANALYSIS (Default Rate by Origination Cohort)          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  HEATMAP:                                                        │
│                                                                  │
│  Origination │  3 MoB  │  6 MoB  │  9 MoB  │  12 MoB │ 18 MoB │
│  ──────────────────────────────────────────────────────────────  │
│  Jan-24      │  2.1%   │  4.3%   │  6.8%   │  9.1%   │ 11.2%  │
│  Feb-24      │  1.9%   │  4.1%   │  6.4%   │  8.8%   │  -     │
│  ...         │  ...    │  ...    │  ...    │  ...    │  -     │
│ ★Oct-23      │  3.4%   │  7.2%   │ 14.8%   │ 21.6%   │ 25.1%  │ ← RED
│ ★Nov-23      │  3.1%   │  6.9%   │ 14.1%   │ 20.4%   │ 24.6%  │ ← RED
│ ★Dec-23      │  3.3%   │  7.0%   │ 14.4%   │ 20.9%   │  -     │ ← RED
│  Jan-23      │  2.0%   │  4.2%   │  7.1%   │  9.5%   │ 11.8%  │
│                                                                  │
│  ★ = Festive season months   Colour: Darker = Higher default    │
│  Colour scale: ░░░░ (low) → ████ (high)                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Page 4: Scenario Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│  SCENARIO ANALYSIS — POLICY IMPACT SIMULATOR                    │
├──────────────────────────────────────────────────────────────── │
│                                                                  │
│  DTI Cutoff Slider:  [──────────|──────────]  35%               │
│  (Current: 40%)        20%            50%                       │
│                                                                  │
│  Grade Exclusion: [☑ Exclude F] [☑ Exclude G] [☐ Exclude E]    │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│         BEFORE (current)          AFTER (simulated)             │
│         ─────────────────         ──────────────────            │
│         Default Rate: 6.5%        Default Rate: 4.8%  ↓        │
│         Approvals: 6,521/mo       Approvals: 5,738/mo  ↓12%    │
│         Est. Loss: ₹6.2 Cr        Est. Loss: ₹4.4 Cr  ↓        │
│                                                                  │
│  ⚠️ Projections assume borrower behaviour does not change.      │
│     Actual impact may vary.                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Colour Palette

| Colour | Hex | Use |
|--------|-----|-----|
| Primary Blue | `#4e79a7` | Normal bars, main KPI |
| Alert Red | `#d62728` | High-risk segments, critical alerts |
| Warning Amber | `#f28e2b` | Amber alerts, moderate risk |
| Neutral Grey | `#9e9e9e` | Secondary data, loan count line |
| White | `#ffffff` | Background |
| Light Grey | `#f5f5f5` | Card backgrounds |

---

## Notes for BI Developer

1. Use Power BI's conditional formatting to colour bars red when default rate ≥ 2x portfolio average (portfolio average is a DAX measure, not a static number).
2. The alert threshold on Page 1 should be stored as a user-editable parameter (What-if parameter in Power BI).
3. The heatmap on Page 3 is best built as a Matrix visual with background colour formatting.
4. The scenario sliders on Page 4 use What-if parameters.
5. All percentage KPIs should use the format `0.0%` (one decimal place).
6. The "Data last refreshed" label should pull from the dataset's last updated timestamp, not a static text box.

---

*Dashboard spec v1.0 — Gnanesh, November 2024*
