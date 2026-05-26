import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os
import plotly.graph_objects as go

# ── Page config — MUST be first streamlit call ────────────────────────────────
st.set_page_config(
    page_title="Credit Risk Scorer | Home Credit",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

* { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
    background: #F8FAFC !important; /* Soft light gray/blue background */
    color: #0F172A; /* Deep navy text */
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
    min-width: 320px !important;
}

/* Aggressively force sidebar text to be dark */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div.stMarkdown {
    color: #0F172A !important;
}

/* Sidebar labels specifically */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] label p {
    color: #334155 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1.25rem !important;
}

[data-testid="stSidebar"] .stSlider > div > div > div {
    background: #E2E8F0 !important;
}
[data-testid="stSidebar"] .stSlider > div > div > div > div {
    background: #0F52BA !important; /* Corporate Blue */
}

/* ── Main area ── */
.block-container {
    padding: 1.5rem 2rem 2rem 2rem !important;
    max-width: 1400px !important;
}

/* ── Header ── */
.header-wrap {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    overflow: hidden;
    position: relative;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}
.header-wrap::after {
    content: '';
    position: absolute;
    right: -80px; top: -80px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(15,82,186,0.04) 0%, transparent 65%);
    pointer-events: none;
}
.header-left {}
.header-eyebrow {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #0F52BA;
    margin-bottom: 0.5rem;
}
.header-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #0F172A;
    margin: 0 0 0.4rem;
    letter-spacing: -0.5px;
}
.header-sub {
    color: #475569;
    font-size: 0.95rem;
    font-weight: 400;
    margin: 0;
}
.header-stats {
    display: flex;
    gap: 2.5rem;
    align-items: center;
}
.hstat {
    text-align: center;
}
.hstat-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #0F52BA;
    line-height: 1;
}
.hstat-label {
    font-size: 0.75rem;
    color: #64748B;
    font-weight: 600;
    margin-top: 5px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Score card ── */
.score-wrap {
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    border: 1px solid;
    position: relative;
    overflow: hidden;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}
.score-wrap.low { background: #F0FDF4; border-color: #BBF7D0; }
.score-wrap.medium { background: #FFFBEB; border-color: #FEF08A; }
.score-wrap.high { background: #FEF2F2; border-color: #FECACA; }

.score-eyebrow {
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.low  .score-eyebrow { color: #166534; }
.medium .score-eyebrow { color: #92400E; }
.high .score-eyebrow { color: #991B1B; }

.score-pct {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 4.5rem;
    font-weight: 700;
    line-height: 1;
    margin: 0.3rem 0;
}
.low .score-pct    { color: #16A34A; }
.medium .score-pct { color: #D97706; }
.high .score-pct   { color: #DC2626; }

.score-uncertainty {
    font-size: 0.85rem;
    color: #475569;
    margin-bottom: 1rem;
}
.decision-pill {
    display: inline-block;
    padding: 8px 28px;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.02em;
}
.low    .decision-pill { background: #DCFCE7; color: #166534; border: 1px solid #86EFAC; }
.medium .decision-pill { background: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; }
.high   .decision-pill { background: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }

/* ── Metric grid ── */
.mgrid {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 1rem;
    margin: 1rem 0;
}
.mcard {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    transition: all 0.2s;
    box-shadow: 0 1px 2px rgba(0,0,0,0.01);
}
.mcard:hover { border-color: #CBD5E1; box-shadow: 0 4px 6px rgba(0,0,0,0.03); }
.mlabel {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748B;
    margin-bottom: 6px;
}
.mval {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #0F172A;
}
.mval.danger  { color: #DC2626; }
.mval.warning { color: #D97706; }
.mval.safe    { color: #16A34A; }

/* ── Section label ── */
.sec-label {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #1E293B;
    margin: 1.5rem 0 0.75rem;
    padding-bottom: 8px;
    border-bottom: 2px solid #E2E8F0;
}

/* ── Risk row ── */
.rrow {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    margin-bottom: 8px;
}
.rrow-name { color: #334155; font-size: 0.9rem; font-weight: 600; }
.rrow-right { display: flex; align-items: center; gap: 12px; }
.rrow-note  { font-size: 0.8rem; color: #64748B; }
.rrow-val   { font-size: 0.95rem; font-weight: 700; min-width: 60px; text-align: right; }
.rrow.safe   .rrow-val { color: #16A34A; }
.rrow.warning .rrow-val { color: #D97706; }
.rrow.danger  .rrow-val { color: #DC2626; }

/* ── Info box ── */
.ibox {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin: 1rem 0;
}
.ibox p { color: #1E3A8A; font-size: 0.9rem; margin: 0; line-height: 1.6; }

/* ── Landing ── */
.landing {
    text-align: center;
    padding: 4rem 2rem 3rem;
}
.landing-icon { font-size: 4rem; margin-bottom: 1rem; }
.landing-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0.75rem;
}
.landing-sub { color: #475569; font-size: 1.1rem; max-width: 550px; margin: 0 auto 2.5rem; line-height: 1.6; }

.stat-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 1.25rem; margin-bottom: 2rem; }
.stat-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.5rem 1rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}
.stat-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 6px;
}
.stat-label { font-size: 0.8rem; color: #64748B; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; }

/* ── Sidebar divider ── */
.sdiv {
    height: 1px;
    background: #E2E8F0;
    margin: 1.25rem 0;
}
.ssec {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #0F52BA;
    margin: 1rem 0 0.75rem;
}

/* ── Button ── */
.stButton > button {
    background: #0F52BA !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    width: 100% !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 6px rgba(15,82,186,0.15) !important;
}
.stButton > button:hover {
    background: #0B3D91 !important;
    box-shadow: 0 6px 12px rgba(15,82,186,0.25) !important;
    transform: translateY(-1px) !important;
}

/* hide branding */
#MainMenu, footer, header { visibility: hidden; }

/* ── INPUTS / DROPDOWNS ───────────────────────── */

/* SELECTBOX MAIN */

div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    color: #0F172A !important;
}

/* SELECTED TEXT */

div[data-baseweb="select"] span {
    color: #0F172A !important;
}

/* DROPDOWN ARROW */

div[data-baseweb="select"] svg {
    fill: #0F172A !important;
}

/* NUMBER INPUT */

.stNumberInput input {
    background: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #CBD5E1 !important;
}

/* +/- BUTTONS */

.stNumberInput button {
    background: #FFFFFF !important;
    color: #0F172A !important;
}

/* DROPDOWN POPUP */

ul[role="listbox"] {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
}

/* OPTIONS */

li[role="option"] {
    background: #FFFFFF !important;
    color: #0F172A !important;
}

/* OPTION HOVER */

li[role="option"]:hover {
    background: #EFF6FF !important;
}

/* INPUT LABELS */

.stSelectbox label,
.stNumberInput label,
.stSlider label {
    color: #334155 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Model loading ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading model...")
def load_model():
    model_candidates = [
        'xgb_models_tuned.pkl',
        'models/xgb_models_tuned.pkl',
        './models/xgb_models_tuned.pkl',
    ]
    feat_candidates = [
        'feature_list.csv',
        'features/feature_list.csv',
        './features/feature_list.csv',
    ]
    mp = next((p for p in model_candidates if os.path.exists(p)), None)
    fp = next((p for p in feat_candidates  if os.path.exists(p)), None)

    if mp is None:
        st.error("❌ Model file not found.")
        st.code(f"Searched: {model_candidates}\nFiles here: {os.listdir('.')}")
        return None, None
    if fp is None:
        st.error("❌ feature_list.csv not found.")
        return None, None

    models    = joblib.load(mp)
    feat_cols = pd.read_csv(fp)['Feature'].tolist()
    threshold = 0.317
    return models, feat_cols, threshold


def score_applicant(features, models, feat_cols, threshold=0.317):

    row = np.array(
        [features.get(c, 0) for c in feat_cols],
        dtype=np.float32
    ).reshape(1, -1)

    scores = [
        m.predict_proba(row)[0, 1]
        for m in models
    ]

    prob = float(np.mean(scores))

    std = float(np.std(scores))

    # ---------------------------------------------------
    # BUSINESS RULES
    # ---------------------------------------------------

    credit_income = features.get('APP_CREDIT_INCOME_RATIO', 0)

    annuity_income = features.get('APP_ANNUITY_INCOME_RATIO', 0)

    credit_goods = features.get('APP_CREDIT_TO_GOODS_RATIO', 0)

    age = features.get('APP_AGE_YEARS', 35)

    prev_refused = features.get('PREV_REFUSED_COUNT', 0)

    ext_mean = features.get('APP_EXT_SOURCE_MEAN', 0.5)

    override_reasons = []

    if credit_income > 10:

        override_reasons.append(
            f"Credit-to-income ratio {credit_income:.1f}× exceeds policy limit"
        )

    if annuity_income > 0.60:

        override_reasons.append(
            f"EMI burden {annuity_income*100:.0f}% exceeds policy limit"
        )

    if credit_goods > 2.0:

        override_reasons.append(
            f"Loan-to-value ratio {credit_goods:.1f}× exceeds policy guideline"
        )

    if ext_mean < 0.20:

        override_reasons.append(
            f"Bureau score {ext_mean:.2f} below minimum threshold"
        )

    if age < 21:

        override_reasons.append(
            f"Applicant age {age} below minimum policy age"
        )

    if prev_refused >= 3:

        override_reasons.append(
            f"{prev_refused} previous refusals detected"
        )

    # ---------------------------------------------------
    # POLICY OVERRIDE
    # ---------------------------------------------------

    if len(override_reasons) > 0:

        prob = max(prob, 0.70)

        return (
            prob,
            std,
            "HIGH RISK — REJECT (Policy Override)",
            "high",
            scores,
            override_reasons
        )

    # ---------------------------------------------------
    # NORMAL MODEL DECISION
    # ---------------------------------------------------

    if prob >= threshold:

        if prob >= 0.55:

            risk = "high"

            dec = "HIGH RISK — REJECT"

        else:

            risk = "medium"

            dec = "REVIEW REQUIRED"

    else:

        risk = "low"

        dec = "LOW RISK — APPROVE"

    return (
        prob,
        std,
        dec,
        risk,
        scores,
        []
    )


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-wrap">
  <div class="header-left">
    <div class="header-eyebrow">🏦 Home Credit · Risk Intelligence Platform</div>
    <div class="header-title">Credit Default Risk Scorer</div>
    <p class="header-sub">XGBoost ensemble model · Trained on 307K real loan applications</p>
  </div>
  <div class="header-stats">
    <div class="hstat"><div class="hstat-val">0.796</div><div class="hstat-label">Test AUC</div></div>
    <div class="hstat"><div class="hstat-val">69%</div><div class="hstat-label">Recall</div></div>
    <div class="hstat"><div class="hstat-val">708</div><div class="hstat-label">Features</div></div>
    <div class="hstat"><div class="hstat-val">5×CV</div><div class="hstat-label">Ensemble</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────────────
models, feat_cols, threshold = load_model()
if models is None:
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📋 Applicant Details")
    st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)

    st.markdown('<div class="ssec">👤 Personal</div>', unsafe_allow_html=True)
    age          = st.slider("Age (years)", 18, 70, 35)
    gender       = st.selectbox("Gender", ["Male", "Female"])
    children     = st.slider("Number of children", 0, 10, 0)
    fam_members  = st.slider("Family members", 1, 10, 2)
    education    = st.selectbox("Education level", [
        "Secondary / secondary special", "Higher education",
        "Incomplete higher", "Lower secondary", "Academic degree"])

    st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
    st.markdown('<div class="ssec">💼 Employment</div>', unsafe_allow_html=True)
    income_type      = st.selectbox("Income type", [
        "Working", "Commercial associate", "Pensioner",
        "State servant", "Unemployed"])
    employment_years = st.slider("Years employed", 0, 40, 5)
    income           = st.number_input("Annual income (₹)", 50000, 10000000, 300000, step=10000)

    st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
    st.markdown('<div class="ssec">🏷️ Loan Details</div>', unsafe_allow_html=True)
    credit_amt  = st.number_input("Loan amount (₹)", 50000, 5000000, 500000, step=10000)
    annuity     = st.number_input("Monthly EMI (₹)", 1000, 200000, 20000, step=1000)
    goods_price = st.number_input("Goods price (₹)", 50000, 5000000, 450000, step=10000)
    loan_type   = st.selectbox("Loan type", ["Cash loans", "Revolving loans"])

    st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
    st.markdown('<div class="ssec">📊 Credit Bureau Scores</div>', unsafe_allow_html=True)

    # ---------------------------------------------------
    # NEW TO CREDIT
    # ---------------------------------------------------

    is_ntc = st.checkbox(
        "I am new to credit (No prior loans)",
        value=False
    )

    st.caption("Industry-standard bureau scores (300–900 scale)")

    # ---------------------------------------------------
    # NTC APPLICANTS
    # ---------------------------------------------------

    if is_ntc:

        ext1_raw = 600
        ext2_raw = 600
        ext3_raw = 600


    # ---------------------------------------------------
    # NORMAL APPLICANTS
    # ---------------------------------------------------

    else:

        ext1_raw = st.slider(
            "CRIF Score",
            300,
            900,
            650
        )

        ext2_raw = st.slider(
            "CIBIL Score",
            300,
            900,
            700
        )

        ext3_raw = st.slider(
            "Experian Score",
            300,
            900,
            680
        )

    # ---------------------------------------------------
    # NORMALIZATION FOR MODEL
    # ---------------------------------------------------

    ext1 = (ext1_raw - 300) / 600

    ext2 = (ext2_raw - 300) / 600

    ext3 = (ext3_raw - 300) / 600


    st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
    st.markdown('<div class="ssec">🗂️ Credit History</div>', unsafe_allow_html=True)
    prev_refused = st.slider("Previous loan refusals", 0, 10, 0)

    st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
    score_btn = st.button("🔍  Score This Applicant", use_container_width=True)

# ── Derived features ──────────────────────────────────────────────────────────
eps            = 1e-5
days_birth     = -age * 365
days_employed  = -employment_years * 365 if employment_years > 0 else 365243
emp_anom       = 1 if employment_years == 0 else 0

ext_mean    = float(np.mean([ext1, ext2, ext3]))
ext_std     = float(np.std([ext1, ext2, ext3]))
ext_min     = min(ext1, ext2, ext3)
ext_max     = max(ext1, ext2, ext3)
ext_product = ext1 * ext2 * ext3
ext_weighted = 0.25*ext1 + 0.50*ext2 + 0.25*ext3

credit_income   = credit_amt   / (income + eps)
annuity_income  = annuity * 12 / (income + eps)
credit_term     = credit_amt   / (annuity + eps)
credit_goods    = credit_amt   / (goods_price + eps)
income_per_pers = income       / (fam_members + eps)
employed_age    = days_employed / (days_birth + eps)
# 1. Ensure this logic is right before the applicant dictionary
if 'is_ntc' not in locals():
    is_ntc = False # Fallback if for some reason the variable wasn't created

# ---------------------------------------------------
# NEW TO CREDIT LOGIC
# ---------------------------------------------------

null_val = 1 if is_ntc else 0
applicant = {
    'DAYS_BIRTH'                    : days_birth,
    'DAYS_EMPLOYED'                 : np.log1p(abs(days_employed)) if employment_years > 0 else 0,
    'DAYS_EMPLOYED_ANOM'            : emp_anom,
    'AMT_INCOME_TOTAL'              : np.log1p(income),
    'AMT_CREDIT'                    : np.log1p(credit_amt),
    'AMT_ANNUITY'                   : np.log1p(annuity * 12),
    'AMT_GOODS_PRICE'               : np.log1p(goods_price),
    'CNT_CHILDREN'                  : children,
    'CNT_FAM_MEMBERS'               : fam_members,
    'CODE_GENDER'                   : 1 if gender == "Male" else 0,
    'EXT_SOURCE_1'                  : ext1,
    'EXT_SOURCE_2'                  : ext2,
    'EXT_SOURCE_3'                  : ext3,
    'EXT_SOURCE_1_IS_NULL'          : null_val,
    'EXT_SOURCE_2_IS_NULL'          : null_val,
    'EXT_SOURCE_3_IS_NULL'          : null_val,
    'APP_EXT_SOURCE_MEAN'           : ext_mean,
    'APP_EXT_SOURCE_STD'            : ext_std,
    'APP_EXT_SOURCE_MIN'            : ext_min,
    'APP_EXT_SOURCE_MAX'            : ext_max,
    'APP_EXT_SOURCE_RANGE'          : ext_max - ext_min,
    'APP_EXT_SOURCE_PRODUCT'        : ext_product,
    'APP_EXT_WEIGHTED'              : ext_weighted,
    'APP_EXT2_x_CREDIT_INCOME'      : ext2 * credit_income,
    'APP_EXT3_x_ANNUITY_INCOME'     : ext3 * annuity_income,
    'APP_AGE_YEARS'                 : age,
    'APP_AGE_YEARS_SQUARED'         : age ** 2,
    'APP_EMPLOYMENT_YEARS'          : employment_years,
    'APP_EMPLOYED_TO_AGE_RATIO'     : employed_age,
    'APP_CREDIT_INCOME_RATIO'       : credit_income,
    'APP_INCOME_CREDIT_RATIO'       : income / (credit_amt + eps),
    'APP_ANNUITY_INCOME_RATIO'      : annuity_income,
    'APP_CREDIT_TERM'               : credit_term,
    'APP_CREDIT_TO_GOODS_RATIO'     : credit_goods,
    'APP_GOODS_CREDIT_DIFF'         : goods_price - credit_amt,
    'APP_INCOME_PER_PERSON'         : income_per_pers,
    'APP_ANNUITY_TO_GOODS_RATIO'    : (annuity * 12) / (goods_price + eps),
    'PREV_REFUSAL_RATE'             : prev_refused / 10.0,
    'PREV_REFUSED_COUNT'            : prev_refused,
    'CROSS_REFUSAL_x_CREDIT_INCOME' : (prev_refused / 10.0) * credit_income,
    'EXT_SOURCE_1_IS_NULL'          : 0,
    'EXT_SOURCE_2_IS_NULL'          : 0,
    'EXT_SOURCE_3_IS_NULL'          : 0,
}

# ── Main output ───────────────────────────────────────────────────────────────
if score_btn:
    prob, std, decision, risk, scores, override_reasons = score_applicant(
    applicant,
    models,
    feat_cols,
    threshold
    )
    # SAVE PREDICTION LOG

    log = pd.DataFrame([{
        "age": age,
        "income": income,
        "loan_amount": credit_amt,
        "probability": prob,
        "risk": risk,
        "decision": decision
    }])

    if os.path.exists("data/prediction_logs.csv"):
        old = pd.read_csv("data/prediction_logs.csv")
        log = pd.concat([old, log], ignore_index=True)

    log.to_csv("data\prediction_logs.csv", index=False)
    pct = int(prob * 100)

    col1, col2 = st.columns([1, 1.7], gap="large")

    with col1:
        # Score card
        st.markdown(f"""
        <div class="score-wrap {risk}">
          <div class="score-eyebrow">Default Probability</div>
          <div class="score-pct">{pct}%</div>
          <div class="score-uncertainty">Model uncertainty ±{std*100:.1f}%</div>
          <div class="decision-pill">{decision}</div>
        </div>
        """, unsafe_allow_html=True)

        # Gauge
        bar_color = '#16A34A' if risk=='low' else '#D97706' if risk=='medium' else '#DC2626'
        # ---------------------------------------------------
# POLICY OVERRIDES DISPLAY
# ---------------------------------------------------

    if len(override_reasons) > 0:

        st.warning(
            "Underwriting policy override triggered."
        )

        for reason in override_reasons:

            st.write(f"• {reason}")

    # ---------------------------------------------------
    # GAUGE CHART
    # ---------------------------------------------------
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            number={'suffix':'%','font':{'size':26,'color':'#0F172A','family':'Space Grotesk'}},
            gauge={
                'axis':{'range':[0,100],'tickcolor':'#94A3B8',
                        'tickfont':{'color':'#64748B','size':11},'nticks':6},
                'bar':{'color':bar_color,'thickness':0.28},
                'bgcolor':'#F8FAFC',
                'bordercolor':'#E2E8F0',
                'borderwidth':1,
                'steps':[
                    {'range':[0,31.7], 'color':'rgba(22,163,74,0.1)'},
                    {'range':[31.7,55],'color':'rgba(217,119,6,0.1)'},
                    {'range':[55,100], 'color':'rgba(220,38,38,0.1)'},
                ],
                'threshold':{
                    'line':{'color':'#0F52BA','width':3},
                    'thickness':0.8,'value':31.7
                }
            }
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=210, margin=dict(t=15,b=5,l=15,r=15),
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

        st.markdown("""
        <div class="ibox">
          <p>🎯 <strong>Threshold: 31.7%</strong> — optimised via Youden's J statistic
          on 46K held-out applicants.<br>
          Blue line = decision boundary.</p>
        </div>
        """, unsafe_allow_html=True)

        # Model agreement
        st.markdown('<div class="sec-label">Model Agreement (5 folds)</div>',
                    unsafe_allow_html=True)
        all_scores = [m.predict_proba(
            np.array([applicant.get(c,0) for c in feat_cols],
                     dtype=np.float32).reshape(1,-1)
        )[0,1] for m in models]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=[f'Fold {i+1}' for i in range(len(all_scores))],
            y=[s*100 for s in all_scores],
            marker_color=[bar_color]*len(all_scores),
            marker_opacity=0.85,
            text=[f'{s*100:.1f}%' for s in all_scores],
            textposition='outside',
            textfont={'color':'#475569','size':11},
        ))
        fig2.add_hline(y=31.7, line_dash='dot', line_color='#0F52BA',
                       annotation_text='threshold', annotation_font_color='#0F52BA')
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=175,
            margin=dict(t=20,b=5,l=5,r=5),
            yaxis={'gridcolor':'#E2E8F0','tickcolor':'#CBD5E1',
                   'tickfont':{'color':'#64748B'},'range':[0,max(all_scores)*130]},
            xaxis={'tickcolor':'#CBD5E1','tickfont':{'color':'#64748B'}},
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})

    with col2:
        # Key metrics
        st.markdown('<div class="sec-label">Key Risk Metrics</div>',
                    unsafe_allow_html=True)

        def mc(label, val, cls):
            return f'<div class="mcard"><div class="mlabel">{label}</div><div class="mval {cls}">{val}</div></div>'

        ci_cls  = 'safe' if credit_income < 3 else 'danger' if credit_income > 6 else 'warning'
        ai_cls  = 'safe' if annuity_income < 0.3 else 'danger' if annuity_income > 0.5 else 'warning'
        ext_cls = 'safe' if ext_mean > 0.6 else 'danger' if ext_mean < 0.4 else 'warning'
        ltv_cls = 'safe' if credit_goods < 1.05 else 'danger' if credit_goods > 1.2 else 'warning'

        st.markdown(f"""
        <div class="mgrid">
          {mc('Credit / Income', f'{credit_income:.2f}×', ci_cls)}
          {mc('EMI Burden', f'{annuity_income*100:.1f}%', ai_cls)}
          {mc('Avg Bureau Score', f'{ext_mean:.3f}', ext_cls)}
          {mc('Loan Term', f'{credit_term/12:.1f} yrs', '')}
          {mc('LTV Ratio', f'{credit_goods:.2f}×', ltv_cls)}
          {mc('Income / Person', f'₹{income_per_pers:,.0f}', '')}
        </div>
        """, unsafe_allow_html=True)

        # Risk factors
        st.markdown('<div class="sec-label">Risk Factor Breakdown</div>',
                    unsafe_allow_html=True)

        factors = [
            ('External Bureau Score (avg)',
             f'{ext_mean:.3f}',
             'safe' if ext_mean > 0.6 else 'danger' if ext_mean < 0.4 else 'warning',
             'Strong ↑' if ext_mean > 0.6 else 'Weak ↓' if ext_mean < 0.4 else 'Moderate'),
            ('Credit-to-Income Ratio',
             f'{credit_income:.2f}×',
             'safe' if credit_income < 3 else 'danger' if credit_income > 6 else 'warning',
             'Healthy' if credit_income < 3 else 'Very High ↑' if credit_income > 6 else 'Elevated'),
            ('Monthly Repayment Burden',
             f'{annuity_income*100:.1f}% of income',
             'safe' if annuity_income < 0.3 else 'danger' if annuity_income > 0.5 else 'warning',
             'Comfortable' if annuity_income < 0.3 else 'Strained ↑' if annuity_income > 0.5 else 'Manageable'),
            ('Employment Stability',
             f'{employment_years} yrs',
             'safe' if employment_years >= 3 else 'danger' if employment_years == 0 else 'warning',
             'Stable' if employment_years >= 3 else 'Unemployed ↑' if employment_years == 0 else 'Short tenure'),
            ('Previous Refusals',
             str(prev_refused),
             'safe' if prev_refused == 0 else 'danger' if prev_refused >= 3 else 'warning',
             'None' if prev_refused == 0 else 'High risk ↑' if prev_refused >= 3 else 'Some history'),
            ('Applicant Age',
             f'{age} yrs',
             'danger' if age < 25 else 'safe' if age >= 35 else 'warning',
             'Higher risk cohort' if age < 25 else 'Lower risk' if age >= 35 else 'Moderate'),
            ('Loan-to-Value',
             f'{credit_goods:.2f}×',
             'safe' if credit_goods < 1.05 else 'danger' if credit_goods > 1.2 else 'warning',
             'Normal' if credit_goods < 1.05 else 'Over-borrowing ↑' if credit_goods > 1.2 else 'Slight premium'),
        ]
        for name, val, cls, note in factors:
            st.markdown(f"""
            <div class="rrow {cls}">
              <span class="rrow-name">{name}</span>
              <div class="rrow-right">
                <span class="rrow-note">{note}</span>
                <span class="rrow-val">{val}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Bureau score bars
        st.markdown('<div class="sec-label">Credit Bureau Score Breakdown</div>',
                    unsafe_allow_html=True)
        fig3 = go.Figure()
        bureau_labels = ['CRIF (EXT_1)', 'CIBIL (EXT_2)', 'Experian (EXT_3)']
        bureau_vals   = [ext1_raw, ext2_raw, ext3_raw]
        bureau_colors = ['#0284C7','#4338CA','#7C3AED']
        fig3.add_trace(go.Bar(
        x=bureau_labels,
        y=bureau_vals,
        marker_color=bureau_colors,
        marker_opacity=0.9,
        text=[f'{v}' for v in bureau_vals],
        textposition='outside',
        textfont={
            'color':'#475569',
            'size':12,
            'family':'Space Grotesk'
        },
    ))

    fig3.add_hline(
        y=600,
        line_dash='dash',
        line_color='#DC2626',
        annotation_text='Neutral benchmark (600)',
        annotation_font_color='#DC2626',
        annotation_position='bottom right'
    )

    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=190,
        margin=dict(t=20,b=5,l=5,r=5),

        yaxis={
            'gridcolor':'#E2E8F0',
            'range':[300,900],
            'tickfont':{'color':'#64748B'},
            'tickcolor':'#CBD5E1'
        },

        xaxis={
            'tickfont':{'color':'#64748B'},
            'tickcolor':'#CBD5E1'
        },

        showlegend=False,
        )
    
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar':False})

# ── Landing state ─────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div class="landing">
      <div class="landing-icon">🏦</div>
      <div class="landing-title">Ready to Score</div>
      <p class="landing-sub">
        Enter applicant details in the sidebar and click
        <strong style="color:#0F52BA">Score This Applicant</strong>
        for an instant risk assessment.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-row">
      <div class="stat-card">
        <div class="stat-val" style="color:#0F52BA">0.796</div>
        <div class="stat-label">Test AUC-ROC</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" style="color:#16A34A">307K</div>
        <div class="stat-label">Training applicants</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" style="color:#7C3AED">708</div>
        <div class="stat-label">Engineered features</div>
      </div>
      <div class="stat-card">
        <div class="stat-val" style="color:#D97706">69%</div>
        <div class="stat-label">Defaulter recall</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ibox">
      <p>
      <strong style="color:#0F52BA">Pipeline:</strong>
      17 applicant inputs → 35 engineered features computed automatically
      (credit ratios, bureau score combinations, employment ratios) →
      708-feature vector assembled → 5 XGBoost models score independently →
      averaged probability vs threshold 31.7% → decision rendered in &lt;100ms.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # How it works
    st.markdown('<div class="sec-label">Decision Logic</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="mcard" style="border-color:#86EFAC; padding:1.2rem;">
          <div class="stat-val" style="color:#16A34A; font-size:1.2rem; margin-bottom:6px;">
            ✓ &lt; 31.7%
          </div>
          <div class="mlabel" style="margin-bottom:6px; color:#166534;">LOW RISK — APPROVE</div>
          <div style="color:#475569; font-size:0.8rem; line-height:1.5;">
            Applicant demonstrates strong repayment capability. Auto-approve eligible.
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="mcard" style="border-color:#FCD34D; padding:1.2rem;">
          <div class="stat-val" style="color:#D97706; font-size:1.2rem; margin-bottom:6px;">
            ⚠ 31.7–55%
          </div>
          <div class="mlabel" style="margin-bottom:6px; color:#92400E;">REVIEW REQUIRED</div>
          <div style="color:#475569; font-size:0.8rem; line-height:1.5;">
            Borderline risk. Escalate to loan officer for manual review and additional documents.
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="mcard" style="border-color:#FCA5A5; padding:1.2rem;">
          <div class="stat-val" style="color:#DC2626; font-size:1.2rem; margin-bottom:6px;">
            ✕ &gt; 55%
          </div>
          <div class="mlabel" style="margin-bottom:6px; color:#991B1B;">HIGH RISK — REJECT</div>
          <div style="color:#475569; font-size:0.8rem; line-height:1.5;">
            High probability of default. Application declined. Offer reduced amount or secured product.
          </div>
        </div>
        """, unsafe_allow_html=True)