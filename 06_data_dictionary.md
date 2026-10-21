# Data Dictionary
## Loan Default Risk Analysis | RISK-2024-001

---

| Document ID | DD-RISK-2024-001 |
|-------------|-----------------|
| Author | Gnanesh (BA) |
| Data Source | Lending Club (adapted for case study) |
| Version | 1.0 |
| Date | October 2024 |

---

## Overview

This data dictionary defines every field used in the analysis. It is the single source of truth for field names, definitions, and business rules. Any discrepancy between this document and the actual dataset must be raised with the Data Engineering Lead before analysis proceeds.

---

## Primary Analysis Fields

| Field Name | Data Type | Description | Business Definition | Sample Values | Notes |
|------------|-----------|-------------|---------------------|---------------|-------|
| `loan_id` | String | Unique identifier for each loan | Primary key; assigned at origination | "1234567" | Do not expose in reports (PII risk) |
| `loan_amnt` | Float | The loan amount applied for by the borrower | Total principal disbursed in INR | 50000, 150000, 500000 | In the Lending Club dataset, denominated in USD — treat as relative values |
| `funded_amnt` | Float | Actual amount funded (may differ from applied amount) | Use `loan_amnt` for disbursement figures unless told otherwise | — | Usually equal to `loan_amnt` for accepted loans |
| `term` | String | Number of months in the loan | Loan repayment tenure | "36 months", "60 months" | Two values only. Strip " months" for numeric use |
| `int_rate` | Float | Interest rate on the loan (%) | Annual percentage rate charged to borrower | 6.5, 13.4, 22.1 | Stored as "6.50%" string in raw data — strip % and convert |
| `installment` | Float | Monthly payment due | Fixed EMI amount | 430.15 | Used to verify DTI calculation |
| `grade` | String (A–G) | LC-assigned loan grade | Risk grade assigned by credit model; A = lowest risk, G = highest | "A", "B", "C", "D", "E", "F", "G" | Key segmentation variable |
| `sub_grade` | String | Sub-category within grade | More granular risk tier | "A1", "B3", "D5" | Use `grade` for analysis; `sub_grade` for deep dives |
| `emp_title` | String | Borrower's job title | Employment role as stated by applicant | "Manager", "Engineer" | High cardinality; not used in main analysis |
| `emp_length` | String | Years of employment | Employment tenure bucket | "< 1 year", "2 years", "10+ years" | Convert to ordinal: 0=<1yr, 1=1yr… 10=10+yrs |
| `home_ownership` | String | Borrower's housing status | Whether borrower rents, owns, or has a mortgage | "RENT", "OWN", "MORTGAGE", "OTHER" | Merge "ANY" and "OTHER" into "OTHER" |
| `annual_inc` | Float | Borrower's self-reported annual income | Gross annual income in INR/USD | 60000, 120000 | Subject to verification issues; outliers >99th percentile to be capped |
| `verification_status` | String | Income verification status | Whether income was verified by LC | "Verified", "Source Verified", "Not Verified" | Use as a data quality indicator |
| `issue_d` | String (date) | Loan origination month | Month and year loan was issued | "Jan-2017", "Oct-2018" | Convert to datetime for vintage analysis |
| `loan_status` | String | Current status of the loan | **Primary target variable** — defines default | "Fully Paid", "Charged Off", "Current", "Late (31-120 days)", "Default" | See Default Flag definition below |
| `purpose` | String | Stated reason for the loan | Borrower-stated loan purpose category | "debt_consolidation", "credit_card", "home_improvement", "small_business" | 14 categories in dataset |
| `dti` | Float | Debt-to-income ratio | Monthly debt obligations ÷ monthly income × 100 | 15.2, 32.8 | Key policy variable; higher = higher risk |
| `delinq_2yrs` | Integer | Number of 30+ DPD delinquencies in past 2 years | Credit history indicator | 0, 1, 2 | 0 is by far the most common |
| `earliest_cr_line` | String (date) | Date of earliest credit account | Credit age proxy | "Jun-1990", "Mar-2010" | Convert to "years of credit history" |
| `fico_range_low` | Integer | Low end of FICO score range at origination | Credit score (substitute for CIBIL in Indian context) | 650, 720, 780 | Use (fico_range_low + fico_range_high) / 2 |
| `fico_range_high` | Integer | High end of FICO score range at origination | See above | 654, 724, 784 | — |
| `open_acc` | Integer | Number of open credit lines | Credit utilisation breadth indicator | 3, 8, 15 | — |
| `pub_rec` | Integer | Number of derogatory public records | Bankruptcy, liens, judgements | 0, 1 | Flag borrowers with pub_rec > 0 |
| `revol_bal` | Float | Total revolving credit balance | Outstanding revolving debt | 5000, 22000 | — |
| `revol_util` | Float | Revolving line utilisation rate (%) | Outstanding revolving balance ÷ total revolving credit limit | 25.4, 68.0 | High utilisation (>75%) is a risk signal |
| `total_acc` | Integer | Total number of credit lines ever opened | Credit history depth | 10, 25 | — |
| `last_pymnt_d` | String (date) | Most recent payment date | Used for collections status analysis | "Nov-2018" | Missing for defaulted or current loans in many cases |

---

## Derived/Calculated Fields

| Field Name | Formula | Description |
|------------|---------|-------------|
| `default_flag` | `1 if loan_status in ['Charged Off', 'Default'] else 0` | Binary target variable: 1 = defaulted, 0 = did not default |
| `fico_avg` | `(fico_range_low + fico_range_high) / 2` | Single FICO score estimate |
| `credit_age_years` | `(issue_d - earliest_cr_line).years` | Years of credit history at origination |
| `income_band` | `cut(annual_inc, bins=[0, 50000, 100000, 150000, inf], labels=['Low','Medium','High','Very High'])` | Income segmentation (adjust bins for INR context) |
| `issue_year` | `issue_d.year` | Year of origination for vintage analysis |
| `issue_month` | `issue_d.month` | Month of origination for vintage analysis |
| `dti_band` | `cut(dti, bins=[0, 15, 25, 35, 45, 100])` | DTI segmentation for policy analysis |

---

## Target Variable Definition

### `default_flag`

| Value | Meaning | `loan_status` Values Included |
|-------|---------|-------------------------------|
| `1` (Default) | Loan reached 90+ days past due or was written off | `Charged Off`, `Default` |
| `0` (No Default) | Loan repaid or current (not yet matured) | `Fully Paid` |
| **Excluded** | Ambiguous/ongoing | `Current`, `Late (16-30 days)`, `Late (31-120 days)`, `In Grace Period` |

**Rationale:** Loans in `Current` or `Late` status have not yet resolved. Including them as non-defaults would understate the true default rate. Excluding them is the conservative and standard approach for vintage analysis.

---

## Data Quality Flags

| Field | Known Issue | Handling |
|-------|-------------|---------|
| `annual_inc` | Self-reported; outliers up to $9M | Cap at 99th percentile for analysis; flag `verification_status = 'Not Verified'` separately |
| `emp_length` | 5.7% missing | Impute as "Unknown" category; do not impute a numeric value |
| `dti` | ~0.05% missing | Drop rows where DTI is NULL (too few to matter) |
| `last_pymnt_d` | Missing for ~18% of records | Only used for vintage analysis; acceptable |
| `revol_util` | ~0.5% NULL | Impute with median for regression; leave as NULL for EDA |
| `pub_rec_bankruptcies` | ~0.7% NULL | Treat NULL as 0 for analysis |

---

## Excluded Fields

The following fields are excluded from this analysis due to data quality, leakage, or irrelevance:

| Field | Reason for Exclusion |
|-------|---------------------|
| `member_id` | PII — borrower identifier |
| `url` | LC loan listing URL — not analytically useful |
| `desc` | Free-text loan description — not used in quantitative analysis |
| `title` | Free-text loan title — redundant with `purpose` |
| `zip_code` | Partially redacted in dataset; geography not in scope |
| `addr_state` | Out of scope (US state; irrelevant for Indian context) |
| `out_prncp` | Outstanding principal — leakage (post-origination) |
| `total_pymnt` | Total payment received — leakage |
| `recoveries` | Post-default recovery amount — leakage |

---

*Data Dictionary v1.0 — Gnanesh, October 2024*
*Review and sign-off required from Data Engineering Lead before analysis begins.*
