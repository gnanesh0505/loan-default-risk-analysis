"""
Loan Default Risk Analysis — Streamlit Dashboard
Project: RISK-2024-001
Author: Gnanesh

Run locally:
    streamlit run app.py

Deploy on Streamlit Cloud:
    Push to GitHub → go to share.streamlit.io → connect repo → set app.py as main file
"""

import streamlit as st

# ── Page config (MUST be first Streamlit call) ──────────────────
st.set_page_config(
    page_title="Loan Default Risk Analysis",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Custom CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1a3a5c;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #666;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }
    .kpi-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 5px solid #4e79a7;
        margin-bottom: 0.5rem;
    }
    .kpi-box-red   { border-left-color: #d62728; background: #fff5f5; }
    .kpi-box-green { border-left-color: #2ca02c; background: #f5fff5; }
    .kpi-label { font-size: 0.8rem; color: #888; font-weight: 600; text-transform: uppercase; }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #1a3a5c; }
    .kpi-delta { font-size: 0.85rem; margin-top: -4px; }
    .alert-red    { background:#ffeaea; border:1px solid #d62728; border-radius:8px;
                    padding:0.7rem 1rem; color:#d62728; font-weight:600; margin-bottom:1rem; }
    .alert-amber  { background:#fff8e1; border:1px solid #f28e2b; border-radius:8px;
                    padding:0.7rem 1rem; color:#b36b00; font-weight:600; margin-bottom:1rem; }
    .insight-box  { background:#e8f4f8; border-radius:8px; padding:0.6rem 1rem;
                    font-size:0.9rem; color:#1a3a5c; margin-top:0.5rem; }
    .section-title { font-size:1.1rem; font-weight:700; color:#1a3a5c;
                     border-bottom:2px solid #4e79a7; padding-bottom:4px; margin-bottom:1rem; }
</style>
""", unsafe_allow_html=True)

# ── Colour constants ─────────────────────────────────────────────
C_BLUE   = "#4e79a7"
C_RED    = "#d62728"
C_AMBER  = "#f28e2b"
C_GREY   = "#9e9e9e"
C_GREEN  = "#2ca02c"

# ════════════════════════════════════════════════════════════════
# DATA GENERATION  (synthetic data that mirrors Lending Club stats)
# Replace generate_data() with: df = pd.read_csv("loans_clean.csv")
# if you have the real cleaned file.
# ════════════════════════════════════════════════════════════════
@st.cache_data
def generate_data(n=80000, seed=42):
    rng = np.random.default_rng(seed)

    grades = list("ABCDEFG")
    grade_weights = [0.18, 0.25, 0.20, 0.15, 0.10, 0.07, 0.05]
    grade_default = {"A":0.03,"B":0.06,"C":0.10,"D":0.16,"E":0.24,"F":0.31,"G":0.36}

    grade_arr  = rng.choice(grades, size=n, p=grade_weights)
    base_pd    = np.array([grade_default[g] for g in grade_arr])

    dti        = rng.normal(22, 9, n).clip(0, 70)
    dti_mult   = 1 + 0.015 * (dti - 20).clip(0)
    annual_inc = rng.lognormal(np.log(65000), 0.55, n).clip(18000, 290000)
    inc_mult   = 1 - 0.0003 * (annual_inc - 65000).clip(None, 0) / 1000

    issue_year  = rng.choice(range(2016, 2019), n,
                             p=[0.28, 0.38, 0.34])
    issue_month = rng.integers(1, 13, n)
    festive     = (issue_month >= 10).astype(int)
    fest_mult   = 1 + 0.35 * festive

    purpose_list = ["debt_consolidation","credit_card","home_improvement",
                    "other","small_business","medical","car","vacation",
                    "moving","house"]
    purpose_w    = [0.32,0.20,0.12,0.10,0.08,0.07,0.04,0.03,0.02,0.02]
    purpose_def  = {"debt_consolidation":1.1,"credit_card":1.0,
                    "home_improvement":0.8,"other":1.0,"small_business":1.5,
                    "medical":1.2,"car":0.7,"vacation":1.3,
                    "moving":1.1,"house":0.9}
    purpose_arr  = rng.choice(purpose_list, n, p=purpose_w)
    pur_mult     = np.array([purpose_def[p] for p in purpose_arr])

    ver_list = ["Verified","Source Verified","Not Verified"]
    ver_w    = [0.40, 0.35, 0.25]
    ver_mult_map = {"Verified":0.75,"Source Verified":0.90,"Not Verified":1.45}
    ver_arr  = rng.choice(ver_list, n, p=ver_w)
    ver_mult = np.array([ver_mult_map[v] for v in ver_arr])

    home_list = ["RENT","OWN","MORTGAGE"]
    home_arr  = rng.choice(home_list, n, p=[0.48,0.14,0.38])

    emp_list = ["< 1 year","1 year","2 years","3 years","4 years",
                "5 years","6 years","7 years","8 years","9 years",
                "10+ years","Unknown"]
    emp_arr  = rng.choice(emp_list, n,
               p=[0.08,0.06,0.07,0.07,0.06,0.08,0.06,0.06,0.06,0.05,0.30,0.05])

    loan_amnt = rng.integers(5000, 35001, n).astype(float)
    term      = rng.choice([36, 60], n, p=[0.60, 0.40])
    int_rate  = (np.array([{"A":6,"B":9,"C":13,"D":17,"E":21,"F":25,"G":28}[g]
                            for g in grade_arr])
                 + rng.normal(0, 1.5, n)).clip(5, 35)

    final_pd  = (base_pd * dti_mult * inc_mult * fest_mult * pur_mult * ver_mult).clip(0, 0.95)
    default_flag = (rng.random(n) < final_pd).astype(int)

    income_band = pd.cut(annual_inc,
                         bins=[0,50000,100000,150000,np.inf],
                         labels=["Low (≤₹3L)","Medium (₹3–6L)",
                                 "High (₹6–10L)","Very High (>₹10L)"])
    dti_band = pd.cut(dti,
                      bins=[0,15,25,35,45,100],
                      labels=["0–15","15–25","25–35","35–45","45+"])

    df = pd.DataFrame({
        "grade":grade_arr, "dti":dti, "annual_inc":annual_inc,
        "issue_year":issue_year, "issue_month":issue_month,
        "is_festive":festive, "purpose":purpose_arr,
        "verification_status":ver_arr, "home_ownership":home_arr,
        "emp_length":emp_arr, "loan_amnt":loan_amnt,
        "term":term, "int_rate":int_rate,
        "default_flag":default_flag,
        "income_band":income_band, "dti_band":dti_band,
    })
    return df

df_full = generate_data()

# ════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    st.image("https://img.icons8.com/color/96/bank-building.png", width=60)
    st.markdown("### 🏦 Loan Default Risk")
    st.markdown("**RISK-2024-001** | QuickLend Finance")
    st.markdown("---")

    page = st.radio("📂 Navigate to",
                    ["🏠 Portfolio Overview",
                     "📊 Segment Analysis",
                     "📅 Vintage Analysis",
                     "🔮 Scenario Analysis",
                     "📁 BA Documents"])

    st.markdown("---")
    st.markdown("**Global Filters**")
    grade_filter = st.multiselect("Loan Grade",
                                  options=list("ABCDEFG"),
                                  default=list("ABCDEFG"))
    year_filter  = st.multiselect("Origination Year",
                                  options=sorted(df_full["issue_year"].unique()),
                                  default=sorted(df_full["issue_year"].unique()))
    purpose_filter = st.multiselect("Loan Purpose",
                                    options=sorted(df_full["purpose"].unique()),
                                    default=sorted(df_full["purpose"].unique()))

    st.markdown("---")
    st.caption("Data refreshed: Synthetic demo data\n\nAuthor: **Gnanesh**")

# Apply filters
df = df_full[
    (df_full["grade"].isin(grade_filter)) &
    (df_full["issue_year"].isin(year_filter)) &
    (df_full["purpose"].isin(purpose_filter))
].copy()

PORTFOLIO_AVG = df["default_flag"].mean() * 100 if len(df) else 0

# ════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════════
def default_by_col(df, col, min_count=100, sort_by_rate=True, top_n=None):
    g = (df.groupby(col)
           .agg(loan_count=("default_flag","count"),
                defaults=("default_flag","sum"))
           .reset_index())
    g["default_rate"] = g["defaults"] / g["loan_count"] * 100
    g["pct_portfolio"] = g["loan_count"] / g["loan_count"].sum() * 100
    g = g[g["loan_count"] >= min_count]
    if sort_by_rate:
        g = g.sort_values("default_rate", ascending=False)
    if top_n:
        g = g.head(top_n)
    return g

def bar_chart(grp, col, title, xlabel="Default Rate (%)"):
    colors = [C_RED if r >= 2*PORTFOLIO_AVG else C_BLUE
              for r in grp["default_rate"]]
    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax1.barh(grp[col].astype(str), grp["default_rate"],
             color=colors, edgecolor="white", height=0.6)
    ax1.axvline(PORTFOLIO_AVG, color="black", linestyle="--",
                linewidth=1.2, label=f"Portfolio avg ({PORTFOLIO_AVG:.1f}%)")
    ax1.set_xlabel(xlabel)
    ax1.xaxis.set_major_formatter(mtick.PercentFormatter())
    ax1.legend(fontsize=8)
    ax2 = ax1.twiny()
    ax2.plot(grp["loan_count"], grp[col].astype(str),
             "o--", color=C_GREY, markersize=4, linewidth=1, label="Loan count")
    ax2.set_xlabel("Loan Count", color=C_GREY)
    ax2.tick_params(axis="x", labelcolor=C_GREY)
    ax2.legend(fontsize=8, loc="lower right")
    ax1.set_title(title, fontsize=12, pad=10)
    ax1.invert_yaxis()
    plt.tight_layout()
    return fig

def insight(text):
    st.markdown(f'<div class="insight-box">💡 <b>Insight:</b> {text}</div>',
                unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 1 — PORTFOLIO OVERVIEW
# ════════════════════════════════════════════════════════════════
if page == "🏠 Portfolio Overview":
    st.markdown('<p class="main-header">🏦 Loan Default Risk Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">QuickLend Digital Finance · RISK-2024-001 · Analyst: Gnanesh</p>', unsafe_allow_html=True)

    if len(df) == 0:
        st.warning("No data matches the selected filters.")
        st.stop()

    # Alert threshold
    alert_threshold = st.slider("⚙️ Alert threshold (%)", 4.0, 10.0, 6.0, 0.1)

    if PORTFOLIO_AVG >= alert_threshold + 1:
        st.markdown(f'<div class="alert-red">🚨 Default rate ({PORTFOLIO_AVG:.1f}%) is critically elevated — exceeds threshold by more than 1%.</div>', unsafe_allow_html=True)
    elif PORTFOLIO_AVG >= alert_threshold:
        st.markdown(f'<div class="alert-amber">⚠️ Default rate ({PORTFOLIO_AVG:.1f}%) has exceeded your alert threshold ({alert_threshold:.1f}%).</div>', unsafe_allow_html=True)

    # KPI row
    total_loans    = len(df)
    total_defaults = df["default_flag"].sum()
    approval_rate  = 68.2   # assumed
    npl_ratio      = PORTFOLIO_AVG * 0.63  # approx

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        color = "red" if PORTFOLIO_AVG > alert_threshold else "green"
        arrow = "▲" if PORTFOLIO_AVG > alert_threshold else "▼"
        st.markdown(f"""<div class="kpi-box kpi-box-{color}">
            <div class="kpi-label">90+ DPD Default Rate</div>
            <div class="kpi-value">{PORTFOLIO_AVG:.1f}%</div>
            <div class="kpi-delta" style="color:{'#d62728' if color=='red' else '#2ca02c'}">{arrow} vs prior period</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-label">Approval Rate</div>
            <div class="kpi-value">{approval_rate:.1f}%</div>
            <div class="kpi-delta" style="color:#d62728">▼ 1.2% vs prior</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-label">NPL Ratio</div>
            <div class="kpi-value">{npl_ratio:.1f}%</div>
            <div class="kpi-delta" style="color:#d62728">▲ trend</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-label">Total Loans (filtered)</div>
            <div class="kpi-value">{total_loans:,}</div>
            <div class="kpi-delta" style="color:#888">Defaults: {total_defaults:,}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Trend line
    st.markdown('<p class="section-title">📈 Monthly Default Rate Trend</p>', unsafe_allow_html=True)
    monthly = (df.groupby(["issue_year","issue_month"])
                 .agg(loans=("default_flag","count"), defaults=("default_flag","sum"))
                 .reset_index())
    monthly["default_rate"] = monthly["defaults"] / monthly["loans"] * 100
    monthly["period"] = monthly["issue_year"].astype(str) + "-" + monthly["issue_month"].astype(str).str.zfill(2)
    monthly = monthly.sort_values(["issue_year","issue_month"])

    fig, ax = plt.subplots(figsize=(12, 3.5))
    ax.plot(monthly["period"], monthly["default_rate"],
            color=C_BLUE, linewidth=2, marker="o", markersize=4)
    ax.fill_between(monthly["period"], monthly["default_rate"],
                    alpha=0.12, color=C_BLUE)
    ax.axhline(PORTFOLIO_AVG, color=C_RED, linestyle="--",
               linewidth=1.2, label=f"Portfolio avg ({PORTFOLIO_AVG:.1f}%)")
    ax.axhline(alert_threshold, color=C_AMBER, linestyle=":",
               linewidth=1.2, label=f"Alert threshold ({alert_threshold:.1f}%)")
    ax.set_ylabel("Default Rate (%)")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.legend(fontsize=9)
    step = max(1, len(monthly)//12)
    ax.set_xticks(range(0, len(monthly), step))
    ax.set_xticklabels(monthly["period"].iloc[::step], rotation=45, ha="right", fontsize=8)
    ax.set_title("Monthly Default Rate by Origination Cohort", fontsize=11)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    insight("Look for months where the line crosses the amber/red threshold — those cohorts need urgent portfolio review.")

    # Grade donut
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">🥧 Portfolio Composition by Grade</p>', unsafe_allow_html=True)
    grade_comp = df["grade"].value_counts().sort_index()
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    colors_pie = [C_GREEN, C_BLUE, "#76b7b2", C_AMBER, "#e15759", C_RED, "#7b4173"]
    wedges, texts, autotexts = ax2.pie(
        grade_comp.values, labels=grade_comp.index,
        autopct="%1.1f%%", colors=colors_pie,
        startangle=90, pctdistance=0.82)
    for at in autotexts: at.set_fontsize(8)
    ax2.set_title("Loan Volume by Grade", fontsize=11)
    centre = plt.Circle((0,0), 0.60, fc="white")
    ax2.add_patch(centre)
    st.pyplot(fig2)
    plt.close()

# ════════════════════════════════════════════════════════════════
# PAGE 2 — SEGMENT ANALYSIS
# ════════════════════════════════════════════════════════════════
elif page == "📊 Segment Analysis":
    st.markdown('<p class="main-header">📊 Segment Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Identify which borrower segments drive defaults</p>', unsafe_allow_html=True)

    if len(df) == 0:
        st.warning("No data matches the selected filters.")
        st.stop()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["By Grade","By DTI Band","By Income Band","By Purpose","By Verification"])

    with tab1:
        grp = default_by_col(df, "grade", sort_by_rate=False)
        st.pyplot(bar_chart(grp, "grade", "Default Rate by Loan Grade  (Red = ≥2× portfolio avg)"))
        plt.close()
        insight(f"Grade F and G default rates are {grp[grp['grade']=='F']['default_rate'].values[0]:.1f}% and {grp[grp['grade']=='G']['default_rate'].values[0]:.1f}% respectively — far above the {PORTFOLIO_AVG:.1f}% portfolio average.")
        st.dataframe(grp.style.format({"default_rate":"{:.1f}%","pct_portfolio":"{:.1f}%"}), use_container_width=True)

    with tab2:
        grp = default_by_col(df, "dti_band", sort_by_rate=False)
        st.pyplot(bar_chart(grp, "dti_band", "Default Rate by DTI Band"))
        plt.close()
        insight("Borrowers with DTI above 35% default at nearly double the rate of those under 25%. Current policy allows DTI up to 40%.")
        st.dataframe(grp.style.format({"default_rate":"{:.1f}%","pct_portfolio":"{:.1f}%"}), use_container_width=True)

    with tab3:
        grp = default_by_col(df, "income_band", sort_by_rate=False)
        st.pyplot(bar_chart(grp, "income_band", "Default Rate by Income Band"))
        plt.close()
        insight("Low-income borrowers carry the highest default risk. Income band alone is weaker than DTI as a predictor.")
        st.dataframe(grp.style.format({"default_rate":"{:.1f}%","pct_portfolio":"{:.1f}%"}), use_container_width=True)

    with tab4:
        grp = default_by_col(df, "purpose", top_n=10)
        st.pyplot(bar_chart(grp, "purpose", "Default Rate by Loan Purpose (Top 10)"))
        plt.close()
        insight("Small business and vacation loans show the highest default rates. Debt consolidation is high volume but moderate risk.")
        st.dataframe(grp.style.format({"default_rate":"{:.1f}%","pct_portfolio":"{:.1f}%"}), use_container_width=True)

    with tab5:
        grp = default_by_col(df, "verification_status")
        st.pyplot(bar_chart(grp, "verification_status", "Default Rate by Income Verification Status"))
        plt.close()
        insight("Not Verified income borrowers default at ~2× the rate of Verified borrowers. Mandatory verification is a key recommendation.")
        st.dataframe(grp.style.format({"default_rate":"{:.1f}%","pct_portfolio":"{:.1f}%"}), use_container_width=True)

# ════════════════════════════════════════════════════════════════
# PAGE 3 — VINTAGE ANALYSIS
# ════════════════════════════════════════════════════════════════
elif page == "📅 Vintage Analysis":
    st.markdown('<p class="main-header">📅 Vintage Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Default rate by loan origination cohort</p>', unsafe_allow_html=True)

    if len(df) == 0:
        st.warning("No data matches the selected filters.")
        st.stop()

    # Heatmap — default rate by year × month
    pivot = (df.groupby(["issue_year","issue_month"])
               .agg(loans=("default_flag","count"), defaults=("default_flag","sum"))
               .reset_index())
    pivot["default_rate"] = pivot["defaults"] / pivot["loans"] * 100
    heat = pivot.pivot(index="issue_year", columns="issue_month", values="default_rate")
    heat.columns = ["Jan","Feb","Mar","Apr","May","Jun",
                    "Jul","Aug","Sep","Oct","Nov","Dec"][:heat.shape[1]]

    st.markdown('<p class="section-title">🌡️ Default Rate Heatmap (Year × Month)</p>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(13, 3.5))
    sns.heatmap(heat, annot=True, fmt=".1f", cmap="YlOrRd",
                linewidths=0.4, linecolor="white",
                annot_kws={"size":8}, ax=ax)
    ax.set_title("Default Rate % by Origination Year × Month  (★ = Festive Season Oct–Dec)", fontsize=11)
    ax.set_xlabel("Month")
    ax.set_ylabel("Year")
    # Mark festive season columns
    for col_idx, col_name in enumerate(heat.columns):
        if col_name in ["Oct","Nov","Dec"]:
            ax.add_patch(plt.Rectangle((col_idx, 0), 1, heat.shape[0],
                         fill=False, edgecolor="#d62728", lw=2.5))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    insight("Red-bordered columns (Oct–Dec) show the festive-season effect — these cohorts consistently default at higher rates due to relaxed approval criteria during campaign periods.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Festive vs non-festive bar
    st.markdown('<p class="section-title">📦 Festive Season vs Rest of Year</p>', unsafe_allow_html=True)
    seasonal = (df.groupby("is_festive")
                  .agg(loans=("default_flag","count"), defaults=("default_flag","sum"))
                  .reset_index())
    seasonal["default_rate"] = seasonal["defaults"] / seasonal["loans"] * 100
    seasonal["period"] = seasonal["is_festive"].map({0:"Non-Festive (Jan–Sep)", 1:"Festive (Oct–Dec)"})

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    colors = [C_BLUE, C_RED]
    bars = ax2.bar(seasonal["period"], seasonal["default_rate"],
                   color=colors, edgecolor="white", width=0.4)
    ax2.axhline(PORTFOLIO_AVG, color="black", linestyle="--", linewidth=1.2)
    ax2.set_ylabel("Default Rate (%)")
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax2.set_title("Default Rate: Festive Season vs Rest of Year", fontsize=11)
    for bar, val in zip(bars, seasonal["default_rate"]):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                 f"{val:.1f}%", ha="center", fontweight="bold", fontsize=12)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

    # Year-wise breakdown table
    st.markdown('<p class="section-title">📋 Year-on-Year Default Rate</p>', unsafe_allow_html=True)
    yoy = (df.groupby("issue_year")
             .agg(loans=("default_flag","count"), defaults=("default_flag","sum"))
             .reset_index())
    yoy["default_rate"] = (yoy["defaults"] / yoy["loans"] * 100).round(2)
    yoy["total_loan_value"] = df.groupby("issue_year")["loan_amnt"].sum().values
    st.dataframe(yoy.rename(columns={
        "issue_year":"Year","loans":"Loans","defaults":"Defaults",
        "default_rate":"Default Rate (%)","total_loan_value":"Total Disbursed ($)"
    }).style.format({"Default Rate (%)":"{:.2f}%",
                     "Total Disbursed ($)":"${:,.0f}"}), use_container_width=True)

# ════════════════════════════════════════════════════════════════
# PAGE 4 — SCENARIO ANALYSIS
# ════════════════════════════════════════════════════════════════
elif page == "🔮 Scenario Analysis":
    st.markdown('<p class="main-header">🔮 Scenario Analysis — Policy Impact Simulator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Simulate the effect of approval policy changes on default rate and loan volume</p>', unsafe_allow_html=True)

    st.info("⚠️ Projections assume borrower behaviour does not change. Actual impact may vary. Use these numbers to inform a decision, not to make it automatically.")

    if len(df) == 0:
        st.warning("No data matches the selected filters.")
        st.stop()

    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        dti_cutoff = st.slider("📐 DTI cutoff (%)", 20, 50, 40, 1,
                               help="Current policy: 40%. Try 35% to see impact.")
        st.caption(f"Current policy: 40% | You selected: {dti_cutoff}%")

    with col_ctrl2:
        exclude_grades = st.multiselect("🚫 Suspend originations for grades",
                                        options=list("ABCDEFG"),
                                        default=[],
                                        help="Recommended: suspend F and G")
        mandatory_ver  = st.checkbox("✅ Mandate income verification (all loans)",
                                     value=False)

    # Compute scenarios
    def scenario(df_in, max_dti=None, excl_grades=None, mandate_ver=False):
        f = df_in.copy()
        if max_dti is not None:
            f = f[f["dti"] <= max_dti]
        if excl_grades:
            f = f[~f["grade"].isin(excl_grades)]
        if mandate_ver:
            f = f[f["verification_status"].isin(["Verified","Source Verified"])]
        dr  = f["default_flag"].mean() * 100 if len(f) else 0
        vol = len(f)
        return dr, vol

    base_dr, base_vol = scenario(df)
    new_dr,  new_vol  = scenario(df, dti_cutoff, exclude_grades, mandatory_ver)

    dr_diff  = new_dr  - base_dr
    vol_diff = new_vol - base_vol
    vol_pct  = vol_diff / base_vol * 100 if base_vol else 0

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">📊 Before vs After Comparison</p>', unsafe_allow_html=True)

    col_b, col_a, col_d = st.columns(3)
    with col_b:
        st.metric("Default Rate — BEFORE", f"{base_dr:.2f}%")
        st.metric("Loan Volume — BEFORE",  f"{base_vol:,}")
    with col_a:
        st.metric("Default Rate — AFTER",  f"{new_dr:.2f}%",
                  delta=f"{dr_diff:+.2f}%",
                  delta_color="inverse")
        st.metric("Loan Volume — AFTER",   f"{new_vol:,}",
                  delta=f"{vol_pct:+.1f}%",
                  delta_color="inverse")
    with col_d:
        savings_est = (base_dr - new_dr) / 100 * df["loan_amnt"].mean() * 0.60 * base_vol
        st.metric("Est. Loss Reduction", f"${savings_est:,.0f}",
                  help="Estimated reduction in credit losses = (rate reduction) × avg loan × LGD(60%) × volume")
        target_met = "✅ Yes" if new_dr <= 5.0 else "❌ Not yet"
        st.metric("Target (≤5.0%) Met?", target_met)

    # Visual comparison
    st.markdown("<br>", unsafe_allow_html=True)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Default rate bar
    axes[0].bar(["Before", "After"], [base_dr, new_dr],
                color=[C_AMBER, C_GREEN if new_dr < base_dr else C_RED],
                edgecolor="white", width=0.5)
    axes[0].axhline(5.0, color="black", linestyle="--", linewidth=1.2, label="Target (5.0%)")
    axes[0].set_ylabel("Default Rate (%)")
    axes[0].set_title("Default Rate: Before vs After", fontsize=11)
    axes[0].yaxis.set_major_formatter(mtick.PercentFormatter())
    axes[0].legend(fontsize=9)
    for bar, val in zip(axes[0].patches, [base_dr, new_dr]):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                     f"{val:.2f}%", ha="center", fontweight="bold", fontsize=12)

    # Volume bar
    axes[1].bar(["Before", "After"], [base_vol, new_vol],
                color=[C_BLUE, C_BLUE if vol_pct >= -10 else C_RED],
                edgecolor="white", width=0.5, alpha=0.85)
    axes[1].set_ylabel("Number of Loans")
    axes[1].set_title("Loan Volume: Before vs After", fontsize=11)
    for bar, val in zip(axes[1].patches, [base_vol, new_vol]):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                     f"{val:,}", ha="center", fontweight="bold", fontsize=11)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    if vol_pct < -10:
        st.warning(f"⚠️ Volume reduction is {vol_pct:.1f}% — exceeds the 10% guardrail. Consider a phased rollout: apply DTI change in Month 1, grade suspension in Month 2.")

    # Predefined options comparison table
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">📋 All Policy Options Side-by-Side</p>', unsafe_allow_html=True)

    options = [
        ("Baseline (no change)",        40, [],         False),
        ("Option A: DTI ≤ 35%",         35, [],         False),
        ("Option B: Suspend F & G",      40, ["F","G"], False),
        ("Option C: A + B combined",     35, ["F","G"], False),
        ("Option D: + Verify income",    35, ["F","G"], True),
    ]
    rows = []
    for label, dti_c, excl, ver in options:
        dr, vol = scenario(df, dti_c, excl, ver)
        rows.append({
            "Scenario": label,
            "Default Rate": f"{dr:.2f}%",
            "Loans": f"{vol:,}",
            "Vol. Reduction": f"{(1-vol/base_vol)*100:.1f}%" if base_vol else "—",
            "Target Met": "✅" if dr <= 5.0 else "❌",
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

# ════════════════════════════════════════════════════════════════
# PAGE 5 — BA DOCUMENTS
# ════════════════════════════════════════════════════════════════
elif page == "📁 BA Documents":
    st.markdown('<p class="main-header">📁 BA Documents</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">All project documentation — Project RISK-2024-001</p>', unsafe_allow_html=True)

    doc = st.selectbox("Choose a document to view", [
        "Project Charter",
        "Stakeholder Register & RACI",
        "Business Requirements Document (BRD)",
        "Functional Requirements Document (FRD)",
        "User Stories",
        "Data Dictionary",
        "Recommendation Memo",
        "Assumptions & Limitations",
        "Project Timeline",
    ])

    if doc == "Project Charter":
        st.markdown("""
## Project Charter — RISK-2024-001

| Field | Value |
|-------|-------|
| **Project Name** | Loan Default Risk Analysis |
| **Sponsor** | Chief Risk Officer (CRO) |
| **BA** | Gnanesh |
| **Timeline** | 6 weeks |
| **Status** | ✅ Approved |

### Business Problem
QuickLend Digital Finance's 90+ DPD default rate increased from **5.1% → 6.5%** over Q2–Q3 FY2024, adding an estimated ₹3.8 crore in quarterly credit losses.

### Objectives
1. Identify borrower segments driving defaults
2. Quantify the business impact of defaults by segment
3. Recommend evidence-based approval policy changes
4. Deliver a Credit Risk monitoring dashboard

### Success Criteria
- Default rate ≤ 5.0% within 2 quarters post-implementation
- Approval volume reduction < 10%
- Dashboard signed off and in weekly use by Credit Risk team
""")

    elif doc == "Stakeholder Register & RACI":
        st.markdown("### Stakeholders")
        data = {
            "Role":["CRO","Credit Risk Lead","Data Eng Lead","Compliance Officer","Collections Mgr","Product Manager"],
            "Interest":["High","High","Medium","High","High","Medium"],
            "Influence":["High","High","Medium","High","Medium","Medium"],
            "Strategy":["Manage closely","Collaborate","Keep informed","Consult early","Keep informed","Keep informed"],
        }
        st.dataframe(pd.DataFrame(data), use_container_width=True)
        st.markdown("### RACI Matrix")
        raci = {
            "Deliverable":["Project Charter","BRD","Data Quality Report","Analysis","Recommendation","Dashboard","UAT Sign-off"],
            "BA (Gnanesh)":["R","R","R","R","R","R","C"],
            "CRO":["A","A","I","I","A","I","A"],
            "Risk Lead":["C","C","A","A","C","A","R"],
            "Compliance":["C","C","I","I","C","I","C"],
        }
        st.dataframe(pd.DataFrame(raci), use_container_width=True)
        st.caption("R=Responsible · A=Accountable · C=Consulted · I=Informed")

    elif doc == "Business Requirements Document (BRD)":
        st.markdown("""
### Business Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| BR-01 | Identify and rank borrower segments by default rate; each segment must include size, default rate, and contribution to total losses | Must Have |
| BR-02 | Define and baseline all KPIs (default rate, approval rate, NPL ratio, EL) | Must Have |
| BR-03 | Provide ≥2 policy change options each with projected default rate, volume, and revenue impact | Must Have |
| BR-04 | Deliver a self-service dashboard with weekly data refresh and segment-level filters | Must Have |
| BR-05 | Scenario analysis showing impact of each policy option | Should Have |
| BR-06 | Vintage analysis by origination month | Should Have |
| BR-07 | Data quality documentation | Should Have |

### KPI Definitions

| KPI | Definition | Baseline | Target |
|-----|-----------|---------|--------|
| 90+ DPD Default Rate | Charged Off loans ÷ total originated | 6.5% | ≤ 5.0% |
| Approval Rate | Approved ÷ applied | ~68% | < 10% reduction |
| NPL Ratio | Non-performing ÷ total book | ~4.1% | Reducing |

### Constraints
- All recommendations must be explainable (no black-box models)
- No protected attributes (gender, religion, caste) in any rule
- RBI Digital Lending Guidelines must be adhered to
""")

    elif doc == "Functional Requirements Document (FRD)":
        st.markdown("""
### Dashboard Functional Requirements

| Page | FR ID | Requirement | Priority |
|------|-------|-------------|----------|
| Overview | FR-01 | Default rate KPI card with vs prior period delta | Must Have |
| Overview | FR-02 | Approval rate KPI card | Must Have |
| Overview | FR-03 | 12-month default rate trend line | Must Have |
| Overview | FR-04 | Alert banner when rate exceeds threshold | Must Have |
| Segment | FR-05 | Default rate by grade bar chart | Must Have |
| Segment | FR-06 | Bars ≥2× avg highlighted in red | Should Have |
| Segment | FR-07 | Default rate by purpose (top 10) | Must Have |
| Segment | FR-08 | Default rate by income band | Must Have |
| Vintage | FR-09 | Heatmap by origination year × month | Must Have |
| Vintage | FR-10 | Festive season months marked | Should Have |
| Scenario | FR-11 | DTI cutoff slider with before/after KPIs | Should Have |
| Scenario | FR-12 | Grade exclusion selector | Should Have |
| Access | FR-13 | Data refresh timestamp visible | Must Have |
| Access | FR-14 | No PII on any page | Must Have |

### Non-Functional Requirements
- Dashboard loads within 5 seconds
- Weekly data refresh (Mondays 8 AM)
- Role-based access: Risk team, CRO read-only
""")

    elif doc == "User Stories":
        stories = [
            ("US-01","Credit Risk Lead","see the current default rate on the dashboard","know immediately if the portfolio is improving or worsening","Must Have"),
            ("US-02","Credit Risk Lead","receive an alert when default rate exceeds a threshold","not be caught off guard by spikes","Must Have"),
            ("US-03","Risk Analyst","see a 12-month default rate trend line","identify whether the increase is gradual or sudden","Must Have"),
            ("US-04","Credit Risk Lead","see default rate by grade","identify which grades need policy action","Must Have"),
            ("US-05","Risk Analyst","see default rate by loan purpose","assess whether certain uses carry higher risk","Must Have"),
            ("US-06","Risk Analyst","simulate a DTI cutoff change","see the trade-off before committing to a policy change","Should Have"),
            ("US-07","CRO","view a high-level monthly default trend","prepare board reporting","Must Have"),
        ]
        for us_id, persona, want, so_that, priority in stories:
            with st.expander(f"**{us_id}** — As a {persona}, I want to {want}"):
                st.markdown(f"**So that:** {so_that}  \n**Priority:** {priority}")

    elif doc == "Data Dictionary":
        fields = {
            "Field":["loan_amnt","int_rate","grade","annual_inc","dti","emp_length",
                     "home_ownership","purpose","term","issue_d","loan_status","default_flag"],
            "Type":["Float","Float","String","Float","Float","String","String","String","Int","Date","String","Int"],
            "Description":["Loan amount disbursed","Annual interest rate (%)","Risk grade A–G (A=lowest risk)",
                           "Borrower self-reported annual income","Debt-to-income ratio (%)","Employment tenure bucket",
                           "RENT/OWN/MORTGAGE","Stated loan purpose","36 or 60 months","Origination month/year",
                           "Current loan status","1=Defaulted, 0=Fully Paid"],
            "Notes":["No outlier cap needed","Strip % from string","Key segmentation variable",
                    "Cap at 99th percentile","Cap at 100; policy variable","'Unknown' for missing",
                    "Merge ANY/OTHER → OTHER","14 categories","Two values only","Convert to datetime",
                    "Filter to Fully Paid/Charged Off only","Derived from loan_status"],
        }
        st.dataframe(pd.DataFrame(fields), use_container_width=True)

    elif doc == "Recommendation Memo":
        st.markdown("""
### To: Chief Risk Officer | From: Gnanesh, BA

---

#### Finding 1: Grade D–G drives 61% of defaults at only 28% of volume
Grades F and G have default rates of 28–33% — more than 4× the portfolio average — yet represent only 6% of loan volume.

#### Finding 2: DTI >35% is the strongest predictor of default
Borrowers with DTI 35–40% default at 21% (1 in 5). The current policy allows up to 40%.

#### Finding 3: Festive-season cohort (Oct–Dec) shows elevated defaults
The festive-season lending campaign relaxed approval criteria. This cohort is the primary driver of the Q2–Q3 default spike.

#### Finding 4: Not-verified income = 2.1× default rate of verified borrowers

---

### Recommendations

| Option | Default Rate → | Volume ↓ | Net Benefit/Mo |
|--------|---------------|----------|----------------|
| A: DTI ≤ 35% | 6.5% → 5.4% | ~9% | +₹26L |
| B: Suspend F & G | 6.5% → 5.8% | ~6% | +₹24L |
| **C: A + B (Recommended)** | **6.5% → 4.8%** | **~12%** | **+₹41L** |
| D: Mandate verification | 6.5% → 5.7% | ~4% | +₹18L |

**Implement Option C (phased over 2 months) + Option D.**
""")

    elif doc == "Assumptions & Limitations":
        st.markdown("""
### Key Assumptions
1. 12 months of loan origination data (~80,000 records) available
2. Default = 90+ DPD (Charged Off status in the system)
3. Stakeholders are simulated (case study)
4. RBI Digital Lending Guidelines apply

### Critical Limitations

#### ⚠️ Selection Bias (Most Important)
The dataset contains **approved loans only**. Rejected applications are excluded.
Any predictor of default identified here is conditional on a borrower having been approved. This means:
- The true population of risky borrowers is larger than what we can see
- Policy changes may have different effects in practice than projected

#### ⚠️ Synthetic Data (This Dashboard)
This Streamlit demo uses **synthetically generated data** that mirrors Lending Club's statistical patterns. Replace `generate_data()` in `app.py` with `pd.read_csv("loans_clean.csv")` to use real data.

#### ⚠️ Income is Self-Reported
Annual income is not verified for all borrowers. Declared income may overstate actual income.
""")

    elif doc == "Project Timeline":
        timeline = {
            "Week":["0","1","1–2","2–3","3–4","4","5","6"],
            "Phase":["Assumptions","Initiation","Discovery","Data Prep","Analysis",
                     "Recommendations","Testing (UAT)","Delivery & Closure"],
            "Key Output":["Scope statement","Charter, RACI","Interview notes, As-is process map",
                         "BRD, Data dictionary, Clean dataset","EDA, Segmentation analysis",
                         "Options analysis, Recommendation memo","Test cases, UAT sign-off",
                         "Final deck, Dashboard, Closure report"],
            "Status":["✅","✅","✅","✅","✅","✅","✅","✅"],
        }
        st.dataframe(pd.DataFrame(timeline), use_container_width=True)
