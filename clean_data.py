"""
Loan Default Risk Analysis — Data Cleaning Script
Project: RISK-2024-001
Author: Gnanesh (BA)
Dataset: Lending Club accepted loans

Usage:
    python src/clean_data.py --input data/raw/accepted_loans.csv --output data/clean/loans_clean.csv

Description:
    Applies all cleaning and transformation steps documented in
    docs/07_data_quality_report.md and docs/06_data_dictionary.md
"""

import argparse
import pandas as pd
import numpy as np
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# STEP 1: LOAD DATA
# ─────────────────────────────────────────────
def load_data(input_path: str, sample_size: int = None) -> pd.DataFrame:
    """Load raw Lending Club CSV file."""
    logger.info(f"Loading data from: {input_path}")

    df = pd.read_csv(
        input_path,
        low_memory=False,
        nrows=sample_size  # Set sample_size=100000 to load a subset
    )

    logger.info(f"Loaded {len(df):,} rows and {len(df.columns)} columns.")
    return df


# ─────────────────────────────────────────────
# STEP 2: SELECT RELEVANT COLUMNS
# ─────────────────────────────────────────────
COLUMNS_TO_KEEP = [
    'loan_amnt', 'funded_amnt', 'term', 'int_rate', 'installment',
    'grade', 'sub_grade', 'emp_length', 'home_ownership', 'annual_inc',
    'verification_status', 'issue_d', 'loan_status', 'purpose', 'dti',
    'delinq_2yrs', 'earliest_cr_line', 'fico_range_low', 'fico_range_high',
    'open_acc', 'pub_rec', 'revol_bal', 'revol_util', 'total_acc',
    'pub_rec_bankruptcies'
]

def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only analysis-relevant columns."""
    available = [c for c in COLUMNS_TO_KEEP if c in df.columns]
    missing = [c for c in COLUMNS_TO_KEEP if c not in df.columns]

    if missing:
        logger.warning(f"Columns not found in dataset: {missing}")

    df = df[available].copy()
    logger.info(f"Kept {len(available)} columns.")
    return df


# ─────────────────────────────────────────────
# STEP 3: FILTER TARGET VARIABLE
# ─────────────────────────────────────────────
# Only keep loans with a resolved outcome (exclude Current, Late, In Grace Period)
INCLUDE_STATUSES = ['Fully Paid', 'Charged Off']

def filter_resolved_loans(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only loans with resolved outcomes (Fully Paid or Charged Off)."""
    original_count = len(df)
    df = df[df['loan_status'].isin(INCLUDE_STATUSES)].copy()
    excluded = original_count - len(df)
    logger.info(
        f"Filtered to resolved loans: {len(df):,} kept, "
        f"{excluded:,} excluded (Current/Late/ambiguous)."
    )
    return df


# ─────────────────────────────────────────────
# STEP 4: CREATE TARGET VARIABLE
# ─────────────────────────────────────────────
def create_default_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Create binary default_flag: 1 = Charged Off, 0 = Fully Paid."""
    df['default_flag'] = (df['loan_status'] == 'Charged Off').astype(int)
    logger.info(
        f"Default flag created. "
        f"Default rate: {df['default_flag'].mean()*100:.2f}% "
        f"({df['default_flag'].sum():,} defaults out of {len(df):,} loans)"
    )
    return df


# ─────────────────────────────────────────────
# STEP 5: REMOVE DUPLICATES
# ─────────────────────────────────────────────
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows (no loan_id in cleaned dataset — deduplicate on key fields)."""
    original_count = len(df)
    df = df.drop_duplicates(
        subset=['loan_amnt', 'issue_d', 'annual_inc', 'grade'],
        keep='first'
    )
    removed = original_count - len(df)
    if removed > 0:
        logger.warning(f"Removed {removed} duplicate rows.")
    return df


# ─────────────────────────────────────────────
# STEP 6: TYPE CONVERSIONS
# ─────────────────────────────────────────────
def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert string columns to correct data types."""

    # Interest rate: strip % and convert to float
    if 'int_rate' in df.columns:
        df['int_rate'] = df['int_rate'].astype(str).str.replace('%', '').str.strip().astype(float)

    # Revolving utilisation: strip % and convert to float
    if 'revol_util' in df.columns:
        df['revol_util'] = df['revol_util'].astype(str).str.replace('%', '').str.strip()
        df['revol_util'] = pd.to_numeric(df['revol_util'], errors='coerce')

    # Term: strip " months" and convert to integer
    if 'term' in df.columns:
        df['term'] = df['term'].astype(str).str.replace(' months', '').str.strip().astype(int)

    # Issue date: convert to datetime
    if 'issue_d' in df.columns:
        df['issue_d'] = pd.to_datetime(df['issue_d'], format='%b-%Y', errors='coerce')
        df['issue_year']  = df['issue_d'].dt.year
        df['issue_month'] = df['issue_d'].dt.month

    # Earliest credit line: convert to datetime
    if 'earliest_cr_line' in df.columns:
        df['earliest_cr_line'] = pd.to_datetime(df['earliest_cr_line'], format='%b-%Y', errors='coerce')

    logger.info("Type conversions complete.")
    return df


# ─────────────────────────────────────────────
# STEP 7: DERIVED FIELDS
# ─────────────────────────────────────────────
def create_derived_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Create calculated fields for analysis."""

    # Average FICO score
    if 'fico_range_low' in df.columns and 'fico_range_high' in df.columns:
        df['fico_avg'] = (df['fico_range_low'] + df['fico_range_high']) / 2

    # Credit age in years at origination
    if 'issue_d' in df.columns and 'earliest_cr_line' in df.columns:
        df['credit_age_years'] = (
            (df['issue_d'] - df['earliest_cr_line']).dt.days / 365.25
        ).round(1)

    # Income band
    if 'annual_inc' in df.columns:
        df['income_band'] = pd.cut(
            df['annual_inc'],
            bins=[0, 50000, 100000, 150000, float('inf')],
            labels=['Low', 'Medium', 'High', 'Very High'],
            right=True
        )

    # DTI band
    if 'dti' in df.columns:
        df['dti_band'] = pd.cut(
            df['dti'],
            bins=[0, 15, 25, 35, 45, 100],
            labels=['0–15', '15–25', '25–35', '35–45', '45+'],
            right=True
        )

    # Festive season flag (Oct–Dec)
    if 'issue_month' in df.columns:
        df['is_festive_season'] = df['issue_month'].isin([10, 11, 12]).astype(int)

    logger.info("Derived fields created: fico_avg, credit_age_years, income_band, dti_band, is_festive_season")
    return df


# ─────────────────────────────────────────────
# STEP 8: HANDLE MISSING VALUES
# ─────────────────────────────────────────────
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Apply missing value handling per Data Quality Report."""

    # emp_length: treat missing as "Unknown" category
    if 'emp_length' in df.columns:
        df['emp_length'] = df['emp_length'].fillna('Unknown')

    # revol_util: impute with median for model use
    if 'revol_util' in df.columns:
        median_revol = df['revol_util'].median()
        df['revol_util'] = df['revol_util'].fillna(median_revol)
        logger.info(f"Imputed revol_util NULLs with median: {median_revol:.1f}")

    # pub_rec_bankruptcies: treat NULL as 0
    if 'pub_rec_bankruptcies' in df.columns:
        df['pub_rec_bankruptcies'] = df['pub_rec_bankruptcies'].fillna(0)

    # Drop rows with NULL in critical fields
    critical_fields = ['dti', 'annual_inc', 'grade', 'loan_amnt']
    available_critical = [f for f in critical_fields if f in df.columns]
    original_count = len(df)
    df = df.dropna(subset=available_critical)
    dropped = original_count - len(df)
    if dropped > 0:
        logger.info(f"Dropped {dropped} rows with NULL in critical fields: {available_critical}")

    return df


# ─────────────────────────────────────────────
# STEP 9: HANDLE OUTLIERS
# ─────────────────────────────────────────────
def handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Cap outliers per Data Quality Report."""

    # Annual income: cap at 99th percentile
    if 'annual_inc' in df.columns:
        cap_99 = df['annual_inc'].quantile(0.99)
        df['annual_inc'] = df['annual_inc'].clip(upper=cap_99)
        logger.info(f"annual_inc capped at 99th percentile: {cap_99:,.0f}")

    # DTI: cap at 100 (economically implausible above this)
    if 'dti' in df.columns:
        high_dti = (df['dti'] > 100).sum()
        df['dti'] = df['dti'].clip(upper=100)
        if high_dti > 0:
            logger.info(f"DTI capped at 100 for {high_dti} rows.")

    return df


# ─────────────────────────────────────────────
# STEP 10: EMP_LENGTH ORDINAL ENCODING
# ─────────────────────────────────────────────
EMP_LENGTH_MAP = {
    '< 1 year': 0, '1 year': 1, '2 years': 2, '3 years': 3,
    '4 years': 4, '5 years': 5, '6 years': 6, '7 years': 7,
    '8 years': 8, '9 years': 9, '10+ years': 10, 'Unknown': -1
}

def encode_emp_length(df: pd.DataFrame) -> pd.DataFrame:
    """Convert emp_length to ordinal numeric (keep original string column too)."""
    if 'emp_length' in df.columns:
        df['emp_length_num'] = df['emp_length'].map(EMP_LENGTH_MAP)
    return df


# ─────────────────────────────────────────────
# STEP 11: SAVE CLEAN DATA
# ─────────────────────────────────────────────
def save_data(df: pd.DataFrame, output_path: str) -> None:
    """Save cleaned dataset to CSV."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Clean dataset saved: {output_path} ({len(df):,} rows, {len(df.columns)} columns)")


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────
def clean_pipeline(input_path: str, output_path: str, sample_size: int = None) -> pd.DataFrame:
    """Run the full cleaning pipeline."""
    logger.info("=" * 60)
    logger.info("Starting Loan Default Risk — Data Cleaning Pipeline")
    logger.info("=" * 60)

    df = load_data(input_path, sample_size)
    df = select_columns(df)
    df = filter_resolved_loans(df)
    df = remove_duplicates(df)
    df = create_default_flag(df)
    df = convert_types(df)
    df = create_derived_fields(df)
    df = handle_missing_values(df)
    df = handle_outliers(df)
    df = encode_emp_length(df)
    save_data(df, output_path)

    logger.info("=" * 60)
    logger.info("Pipeline complete.")
    logger.info(f"Final dataset: {len(df):,} rows")
    logger.info(f"Default rate:  {df['default_flag'].mean()*100:.2f}%")
    logger.info("=" * 60)

    return df


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean and transform Lending Club loan data for default risk analysis."
    )
    parser.add_argument(
        "--input", type=str,
        default="data/raw/accepted_loans.csv",
        help="Path to raw CSV file"
    )
    parser.add_argument(
        "--output", type=str,
        default="data/clean/loans_clean.csv",
        help="Path to save cleaned CSV file"
    )
    parser.add_argument(
        "--sample", type=int, default=None,
        help="Number of rows to load (omit for full dataset)"
    )

    args = parser.parse_args()
    clean_pipeline(args.input, args.output, args.sample)
