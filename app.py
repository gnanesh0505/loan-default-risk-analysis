import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Loan Default Risk Analysis", layout="wide")

DATA_PATH = "loan_sample.csv"   # small cleaned sample committed to the repo (<10 MB)
MAX_ROWS = 20000                # keep CPU/memory low on free hosting


@st.cache_data(show_spinner="Loading data...")
def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        if len(df) > MAX_ROWS:
            df = df.sample(MAX_ROWS, random_state=42)
        return df, False
    # Fallback demo data so the app never crashes if the CSV is missing
    rng = np.random.default_rng(42)
    n = 5000
    grades = rng.choice(list("ABCDEFG"), n, p=[.2, .25, .25, .15, .08, .05, .02])
    base = {"A": .03, "B": .06, "C": .10, "D": .15, "E": .21, "F": .28, "G": .35}
    p = np.array([base[g] for g in grades])
    df = pd.DataFrame({
        "grade": grades,
        "loan_amnt": rng.integers(50000, 500000, n),
        "annual_inc": rng.normal(600000, 200000, n).clip(150000),
        "dti": rng.normal(18, 7, n).clip(0, 45),
        "purpose": rng.choice(["debt_consolidation", "credit_card", "home", "other"], n),
        "default": (rng.random(n) < p).astype(int),
    })
    return df, True


@st.cache_data
def default_rate_by(df, col):
    return df.groupby(col)["default"].mean().mul(100).round(2).sort_index()


@st.cache_data
def make_bar(series_dict, title):
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.bar(list(series_dict.keys()), list(series_dict.values()))
    ax.set_title(title)
    ax.set_ylabel("Default rate (%)")
    fig.tight_layout()
    return fig


df, is_demo = load_data()

st.title("🏦 Loan Default Risk Analysis")
if is_demo:
    st.warning("Showing demo data. Add `loan_sample.csv` (with a `default` column of 0/1) to the repo to use real data.")

if "default" not in df.columns and "loan_status" in df.columns:
    df["default"] = (df["loan_status"] == "Charged Off").astype(int)

c1, c2, c3 = st.columns(3)
c1.metric("Loans", f"{len(df):,}")
c2.metric("Default rate", f"{df['default'].mean() * 100:.2f}%")
if "loan_amnt" in df.columns:
    c3.metric("Avg loan", f"₹{df['loan_amnt'].mean():,.0f}")

cat_cols = [c for c in ["grade", "purpose", "home_ownership", "term", "emp_length"] if c in df.columns]
if cat_cols:
    col = st.selectbox("Segment by", cat_cols)
    rates = default_rate_by(df, col)
    st.pyplot(make_bar(rates.to_dict(), f"Default rate by {col}"))
    plt.close("all")
    st.dataframe(rates.rename("Default rate (%)"))

with st.expander("Preview data"):
    st.dataframe(df.head(100))
