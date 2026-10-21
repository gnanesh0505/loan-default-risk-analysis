-- ============================================================
-- Loan Default Risk Analysis — SQL Queries
-- Project: RISK-2024-001
-- Author: Gnanesh (BA)
-- Dataset: Lending Club (adapted)
-- ============================================================
-- These queries assume the cleaned dataset is loaded into a
-- table called `loans` with the schema defined in the
-- Data Dictionary (docs/06_data_dictionary.md)
-- ============================================================


-- ============================================================
-- SECTION 1: BASELINE KPIs
-- ============================================================

-- Query 1: Overall default rate
SELECT
    COUNT(*) AS total_loans,
    SUM(default_flag) AS total_defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct,
    ROUND(AVG(loan_amnt), 0) AS avg_loan_amount,
    SUM(loan_amnt) AS total_portfolio_value
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off');


-- Query 2: Monthly default rate trend (last 12 months)
SELECT
    issue_year,
    issue_month,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
  AND issue_d >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '12 months'
GROUP BY issue_year, issue_month
ORDER BY issue_year, issue_month;


-- ============================================================
-- SECTION 2: SEGMENTATION ANALYSIS
-- ============================================================

-- Query 3: Default rate by loan grade
SELECT
    grade,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct,
    ROUND(SUM(default_flag) * 100.0 / SUM(SUM(default_flag)) OVER (), 2) AS pct_of_total_defaults,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_portfolio
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
GROUP BY grade
ORDER BY grade;


-- Query 4: Default rate by DTI band
SELECT
    CASE
        WHEN dti <= 15 THEN '0–15%'
        WHEN dti <= 25 THEN '15–25%'
        WHEN dti <= 35 THEN '25–35%'
        WHEN dti <= 40 THEN '35–40%'
        ELSE '40%+'
    END AS dti_band,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct,
    ROUND(AVG(loan_amnt), 0) AS avg_loan_amount
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
  AND dti IS NOT NULL
GROUP BY dti_band
ORDER BY MIN(dti);


-- Query 5: Default rate by loan purpose
SELECT
    purpose,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_portfolio
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
GROUP BY purpose
HAVING COUNT(*) >= 50
ORDER BY default_rate_pct DESC
LIMIT 10;


-- Query 6: Default rate by income band
SELECT
    CASE
        WHEN annual_inc <= 50000  THEN 'Low (≤₹3L equiv)'
        WHEN annual_inc <= 100000 THEN 'Medium (₹3–6L equiv)'
        WHEN annual_inc <= 150000 THEN 'High (₹6–10L equiv)'
        ELSE 'Very High (>₹10L equiv)'
    END AS income_band,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct,
    ROUND(AVG(loan_amnt), 0) AS avg_loan_amount
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
  AND annual_inc IS NOT NULL
  AND annual_inc <= 290000  -- 99th percentile cap
GROUP BY income_band
ORDER BY MIN(annual_inc);


-- Query 7: Default rate by employment length
SELECT
    emp_length,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
GROUP BY emp_length
ORDER BY emp_length;


-- Query 8: Default rate by home ownership
SELECT
    home_ownership,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
  AND home_ownership IN ('RENT', 'OWN', 'MORTGAGE')
GROUP BY home_ownership
ORDER BY default_rate_pct DESC;


-- Query 9: Default rate by income verification status
SELECT
    verification_status,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
GROUP BY verification_status
ORDER BY default_rate_pct DESC;


-- ============================================================
-- SECTION 3: VINTAGE ANALYSIS
-- ============================================================

-- Query 10: Default rate by origination year
SELECT
    issue_year,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct,
    ROUND(SUM(loan_amnt), 0) AS total_disbursed
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
GROUP BY issue_year
ORDER BY issue_year;


-- Query 11: Festive season cohort analysis
-- Compare Oct–Dec default rates across years
SELECT
    issue_year,
    issue_month,
    CASE WHEN issue_month IN (10, 11, 12) THEN 'Festive Season'
         ELSE 'Non-Festive' END AS season,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
GROUP BY issue_year, issue_month
ORDER BY issue_year, issue_month;


-- Query 12: Average default rate — festive vs non-festive months
SELECT
    CASE WHEN issue_month IN (10, 11, 12) THEN 'Festive Season (Oct–Dec)'
         ELSE 'Rest of Year' END AS period,
    COUNT(*) AS loan_count,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
GROUP BY period;


-- ============================================================
-- SECTION 4: SCENARIO ANALYSIS
-- ============================================================

-- Query 13: Impact of tightening DTI from 40% to 35%
-- Shows how many loans and defaults would be excluded
SELECT
    'Approved under current policy (DTI ≤ 40%)' AS scenario,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
  AND dti <= 40

UNION ALL

SELECT
    'Approved under new policy (DTI ≤ 35%)' AS scenario,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
  AND dti <= 35

UNION ALL

SELECT
    'Excluded by DTI change (35% < DTI ≤ 40%)' AS scenario,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
  AND dti > 35 AND dti <= 40;


-- Query 14: Impact of suspending Grade F and G
SELECT
    'All grades (current policy)' AS scenario,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')

UNION ALL

SELECT
    'Excluding Grade F and G (new policy)' AS scenario,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
  AND grade NOT IN ('F', 'G')

UNION ALL

SELECT
    'Grade F and G only (excluded loans)' AS scenario,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
  AND grade IN ('F', 'G');


-- Query 15: Combined scenario (DTI ≤ 35% AND Grade A–E only)
SELECT
    'Combined policy (DTI ≤ 35% + Grade A–E)' AS scenario,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct,
    ROUND((1 - COUNT(*) * 1.0 /
        (SELECT COUNT(*) FROM loans
         WHERE loan_status IN ('Fully Paid', 'Charged Off'))) * 100, 2) AS pct_volume_reduction
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
  AND dti <= 35
  AND grade NOT IN ('F', 'G');


-- ============================================================
-- SECTION 5: HIGH-RISK SEGMENT SUMMARY
-- ============================================================

-- Query 16: Identify borrower segments with default rate ≥ 2x portfolio average
-- Portfolio average ~14% in this dataset (Charged Off / (Charged Off + Fully Paid))
WITH portfolio_avg AS (
    SELECT ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS avg_rate
    FROM loans
    WHERE loan_status IN ('Fully Paid', 'Charged Off')
)
SELECT
    grade,
    purpose,
    CASE
        WHEN dti <= 25 THEN 'Low DTI'
        WHEN dti <= 35 THEN 'Medium DTI'
        ELSE 'High DTI'
    END AS dti_category,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS defaults,
    ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) AS default_rate_pct,
    (SELECT avg_rate FROM portfolio_avg) AS portfolio_avg_rate
FROM loans
WHERE loan_status IN ('Fully Paid', 'Charged Off')
GROUP BY grade, purpose, dti_category
HAVING COUNT(*) >= 200
   AND ROUND(SUM(default_flag) * 100.0 / COUNT(*), 2) >= 2 * (SELECT avg_rate FROM portfolio_avg)
ORDER BY default_rate_pct DESC
LIMIT 10;


-- ============================================================
-- END OF SCRIPT
-- ============================================================
-- Notes:
-- 1. Replace CURRENT_DATE with the relevant analysis end date
-- 2. Adjust income band thresholds if converting USD→INR
-- 3. The `default_flag` column must be created during cleaning:
--    default_flag = 1 if loan_status = 'Charged Off' else 0
--    (Exclude 'Current', 'Late', 'In Grace Period' rows from analysis)
-- ============================================================
