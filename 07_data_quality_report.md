# Data Quality Report
## Loan Default Risk Analysis | RISK-2024-001

---

| Document ID | DQR-RISK-2024-001 |
|-------------|------------------|
| Author | Gnanesh (BA) |
| Dataset | Lending Club 2007–2018 Q4 (sample: 100,000 rows) |
| Version | 1.0 |
| Date | October 2024 |

---

## 1. Executive Summary

A data profiling exercise was conducted on a 100,000-row sample of the Lending Club accepted loan dataset. The dataset is broadly fit for purpose with the following caveats:
- **Income data is self-reported** and has extreme outliers that must be capped before use.
- **Employment length has ~5.7% missing values** — handled as a separate "Unknown" category.
- **Target variable exclusions** (Current, Late loans) reduce the analysable pool by approximately 18%.
- **Selection bias is a structural limitation** — the dataset contains only approved loans, not applications.

All issues are documented below with the handling decision applied.

---

## 2. Dataset Overview

| Dimension | Value |
|-----------|-------|
| Total rows (sample) | 100,000 |
| Total columns | 150 |
| Columns used in analysis | 22 |
| Date range (issue_d) | Jan 2007 – Dec 2018 |
| Rows with `default_flag = 1` (Charged Off) | ~14,000 (14%) |
| Rows with `loan_status = Fully Paid` | ~68,000 (68%) |
| Rows excluded (Current / Late / ambiguous) | ~18,000 (18%) |
| **Final analysis dataset** | **~82,000 rows** |

---

## 3. Missing Value Analysis

| Field | Missing Count | Missing % | Severity | Handling Decision |
|-------|--------------|-----------|----------|-------------------|
| `emp_length` | 5,680 | 5.7% | Medium | Treat as "Unknown" category; do not impute numerically |
| `revol_util` | 502 | 0.5% | Low | Impute with dataset median (47.3%) for model; leave NULL for EDA |
| `last_pymnt_d` | 18,200 | 18.2% | Low | Used only for vintage analysis; missing acceptable |
| `pub_rec_bankruptcies` | 697 | 0.7% | Low | Treat NULL as 0 |
| `dti` | 48 | 0.05% | Negligible | Drop rows |
| `annual_inc` | 4 | <0.01% | Negligible | Drop rows |
| `title` | 1,012 | 1.0% | N/A | Field excluded from analysis |

---

## 4. Outlier Analysis

### 4.1 Annual Income

| Statistic | Value |
|-----------|-------|
| Minimum | $1,896 |
| 25th percentile | $45,000 |
| Median | $65,000 |
| 75th percentile | $90,000 |
| 95th percentile | $155,000 |
| 99th percentile | $290,000 |
| Maximum | $9,500,000 |

**Finding:** The maximum income of $9.5M is almost certainly a data entry error (likely $95,000 with a misplaced decimal). The 99th percentile at $290,000 is plausible for a US dataset but may still distort mean-based calculations.

**Decision:** Cap `annual_inc` at the 99th percentile ($290,000) for all analysis. Flag `verification_status = 'Not Verified'` as a separate category of concern.

### 4.2 DTI (Debt-to-Income Ratio)

| Statistic | Value |
|-----------|-------|
| Minimum | 0.0 |
| Median | 17.9 |
| 95th percentile | 38.1 |
| Maximum | 999.0 |

**Finding:** DTI values above 100 are economically implausible and likely data errors.

**Decision:** Cap DTI at 100 for analysis. Rows with DTI > 100 represent 0.3% of records.

### 4.3 Loan Amount

| Statistic | Value |
|-----------|-------|
| Minimum | $500 |
| Median | $12,000 |
| Maximum | $40,000 |

**Finding:** Distribution is right-skewed but within expected range for personal loans. No outlier capping required.

---

## 5. Data Consistency Checks

| Check | Result | Action |
|-------|--------|--------|
| `funded_amnt` ≤ `loan_amnt` in all rows | PASS — funded ≤ applied in 99.8% of rows | Accept |
| `loan_status` values are one of the known set | PASS — no unexpected values found | Accept |
| `issue_d` is within expected range (2007–2018) | PASS | Accept |
| `grade` is A–G only | PASS | Accept |
| `term` is "36 months" or "60 months" only | PASS | Accept |
| `int_rate` aligns with `grade` (higher grade = lower rate) | PASS — strong negative correlation (r = −0.94) | Accept |
| `fico_range_low` < `fico_range_high` in all rows | PASS | Accept |
| Duplicate `loan_id` | FAIL — 23 duplicate IDs found | Deduplicate: keep first occurrence |

---

## 6. Class Balance (Target Variable)

| Class | Count | % |
|-------|-------|---|
| 0 — No Default (Fully Paid) | 68,142 | 82.9% |
| 1 — Default (Charged Off) | 13,858 | 17.1% |
| **Total (after exclusions)** | **82,000** | 100% |

**Finding:** The dataset is moderately imbalanced (~5:1 ratio). For descriptive analysis and segmentation, this is acceptable. If a predictive model were built in future, class balancing (oversampling or weighted loss) would be required.

---

## 7. Selection Bias — Key Limitation

**Critical finding:** The Lending Club dataset contains only **accepted loan applications**. Rejected applications are published in a separate file (not used here).

**Implication:** Any analysis of default predictors is conditional on the borrower having been approved. If the approval model has already filtered out the riskiest borrowers, the predictors of default in this dataset may not generalise to the broader applicant pool.

**Mitigation:** All recommendations must explicitly acknowledge this limitation. Policy changes should be validated against a holdout sample from a different time period before production rollout.

---

## 8. Data Lineage

```
Source: Kaggle (wordsforthewise/lending-club)
    └── Raw file: accepted_2007_to_2018Q4.csv.gz (~2.6M rows)
        └── Sampled: 100,000 rows (stratified by year)
            └── notebooks/01_data_profiling.ipynb (profiling)
                └── notebooks/02_cleaning.ipynb (cleaning & transformation)
                    └── data/clean/loans_clean.csv (analysis-ready file)
                        └── notebooks/03_eda.ipynb
                        └── notebooks/04_segmentation.ipynb
                        └── sql/analysis_queries.sql
```

---

## 9. Sign-off

| Role | Name | Decision | Date |
|------|------|----------|------|
| Data Engineering Lead | [Name] | Approved / Pending | _____ |
| Credit Risk Lead | [Name] | Reviewed | _____ |
| BA | Gnanesh | Submitted | Oct 2024 |

---

*DQR v1.0 — Gnanesh, October 2024*
