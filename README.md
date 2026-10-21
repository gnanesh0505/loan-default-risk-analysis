# 🏦 Loan Default Risk Analysis
**Business Analyst Case Study | Fintech Domain | Junior BA Portfolio Project**

---

## 📌 Business Problem

A digital lender offering unsecured personal loans (₹50,000 – ₹5,00,000) has seen its **90+ day default rate rise from 5.1% to 6.5%** over two consecutive quarters. Leadership needs to understand which borrower segments drive defaults and what changes to make in the approval policy — without significantly reducing loan volume.

---

## 🎯 Objectives

- Identify borrower segments with disproportionately high default rates
- Quantify the business impact of defaults (loss exposure by segment)
- Recommend approval policy changes with expected impact on default rate and volume
- Design a monitoring dashboard for the Credit Risk team

---

## 📊 Key Results

| Metric | Before | After (Recommended) |
|--------|--------|----------------------|
| Default Rate (90+ DPD) | 6.5% | ~5.1% (projected) |
| Approval Rate | Baseline | ~4% reduction |
| High-risk segments flagged | — | 3 segments identified |
| Annual loss reduction (est.) | — | ₹2.4 Cr |

> Numbers are derived from Lending Club dataset analysis. Real-world results will vary.

---

## 👤 My Role

**Business Analyst** — This project covers end-to-end BA responsibilities:
- Stakeholder interviews and requirements elicitation
- As-is and to-be process mapping (BPMN)
- Business Requirements Document (BRD) and Functional Requirements Document (FRD)
- User stories with acceptance criteria
- Data profiling, cleaning, and exploratory analysis
- KPI definition and segmentation
- Policy recommendations with cost-benefit analysis
- Dashboard design and UAT

---

## 🗂️ Project Phases

```
Phase 0: Assumptions & Scope
Phase 1: Initiation & Project Charter
Phase 2: Stakeholder Discovery & Requirements Elicitation
Phase 3: Requirements Definition (BRD, FRD, User Stories)
Phase 4: Data Understanding & Preparation
Phase 5: Exploratory Data Analysis & Segmentation
Phase 6: Solution Design & Recommendations
Phase 7: Validation & Testing (UAT)
Phase 8: Delivery & Sign-off
Phase 9: Closure & Retrospective
```

---

## 📁 Repository Guide

| Folder | Contents |
|--------|----------|
| [`docs/`](docs/) | All BA documents: charter, BRD, FRD, user stories, data dictionary, recommendation memo |
| [`process/`](process/) | As-is and to-be BPMN process map descriptions |
| [`notebooks/`](notebooks/) | Python notebooks: data profiling, cleaning, EDA, segmentation |
| [`sql/`](sql/) | SQL queries for analysis |
| [`dashboard/`](dashboard/) | Dashboard mockup descriptions and Power BI file |
| [`reports/`](reports/) | Final presentation and scenario analysis |
| [`src/`](src/) | Reusable Python cleaning script |
| [`data/`](data/) | Download instructions only (no raw data committed) |

---

## 📦 Dataset

**Lending Club Loan Data (2007–2018 Q4)**
- Source: [Kaggle — wordsforthewise/lending-club](https://www.kaggle.com/datasets/wordsforthewise/lending-club)
- Records used: ~100,000 rows (sample)
- Key fields: `loan_amnt`, `int_rate`, `grade`, `annual_inc`, `dti`, `emp_length`, `home_ownership`, `purpose`, `term`, `loan_status`
- See [`data/README.md`](data/README.md) for download instructions

---

## ⚠️ Assumptions & Limitations

- Dataset contains **accepted loans only** — rejected applications are excluded, causing **selection bias**
- Default is defined as **`loan_status = 'Charged Off'`** (90+ days past due)
- Stakeholders are **simulated** (case study; not a real company)
- Regulatory constraints follow **RBI Digital Lending Guidelines** (adapted from Lending Club US context)
- 12 months of loan vintage data used for analysis

---

## 🛠️ Tools Used

| Category | Tool |
|----------|------|
| Data Analysis | Python (pandas, numpy, matplotlib, seaborn) |
| Query | SQL (SQLite / PostgreSQL compatible) |
| Dashboard | Power BI / Tableau |
| Process Mapping | draw.io / Bizagi (BPMN) |
| Documentation | Markdown, MS Word |
| Version Control | Git / GitHub |

---

## ▶️ How to Run

```bash
# 1. Clone the repository
git clone https://github.com/your-username/loan-default-risk-analysis.git
cd loan-default-risk-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download dataset
# Follow instructions in data/README.md

# 4. Run notebooks in order
jupyter notebook notebooks/
```

---

## 📅 Timeline

| Week | Phase | Key Output |
|------|-------|-----------|
| 0 | Assumptions | Scope statement |
| 1 | Initiation | Charter, RACI, stakeholder register |
| 2 | Discovery & Data | Interview notes, as-is map, data quality report |
| 3 | Requirements & EDA | BRD, FRD, user stories, data profiling |
| 4 | Analysis & Recommendations | Segmentation, recommendation memo, dashboard design |
| 5 | Testing | Test cases, UAT sign-off |
| 6 | Delivery & Closure | Final deck, closure report |

---

## 📬 Contact

**Gnanesh**
📧 gnaneshreddy17520@gmail.com


---

*This is a case study project for portfolio purposes. All company names and stakeholder details are fictional.*

