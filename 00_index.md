# Document Index
## Loan Default Risk Analysis | RISK-2024-001

---

Read these documents in this order to understand the project from start to finish.

| # | Document | File | Phase | Purpose |
|---|----------|------|-------|---------|
| 0 | Document Index (this file) | `00_index.md` | — | Navigation guide |
| 1 | Project Charter | `01_project_charter.md` | Initiation | Problem, objectives, scope, timeline, sign-off |
| 2 | Stakeholder Register | `02_stakeholder_register.md` | Initiation | Who the stakeholders are, RACI, communication plan |
| 3 | Business Requirements Document | `03_BRD.md` | Requirements | What the business needs; KPIs; constraints |
| 4 | Functional Requirements Document | `04_FRD.md` | Requirements | Dashboard features and technical requirements |
| 5 | User Stories | `05_user_stories.md` | Requirements | How users will use the dashboard; acceptance criteria |
| 6 | Data Dictionary | `06_data_dictionary.md` | Data | Field definitions, derived fields, exclusions |
| 7 | Data Quality Report | `07_data_quality_report.md` | Data | Missing values, outliers, handling decisions |
| 8 | Recommendation Memo | `08_recommendation_memo.md` | Delivery | Findings, options, recommendation, next steps |
| 9 | Test Cases & UAT Sign-off | `09_test_cases.md` | Testing | How the dashboard was tested and verified |
| 10 | Lessons Learned | `10_lessons_learned.md` | Closure | What worked, what didn't, recommendations |

---

## Supporting Files

| File | Location | Description |
|------|----------|-------------|
| As-is Process Map | `process/as_is_bpmn.md` | Loan lifecycle before policy changes |
| To-be Process Map | `process/to_be_bpmn.md` | Loan lifecycle after recommended changes |
| Data Profiling Notebook | `notebooks/01_data_profiling.ipynb` | EDA and data quality checks |
| Data Cleaning Notebook | `notebooks/02_cleaning.ipynb` | Cleaning and transformation steps |
| EDA Notebook | `notebooks/03_eda.ipynb` | Exploratory analysis and charts |
| Segmentation Notebook | `notebooks/04_segmentation.ipynb` | Borrower segmentation and default drivers |
| SQL Queries | `sql/analysis_queries.sql` | All analysis queries |
| Cleaning Script | `src/clean_data.py` | Reusable Python cleaning script |

---

*Index v1.0 — Gnanesh, November 2024*
