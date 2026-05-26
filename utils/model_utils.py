import joblib
import pandas as pd
import numpy as np
import streamlit as st
from utils.business_rules import apply_business_rules

@st.cache_resource
def load_model():

    obj = joblib.load("models/xgb_models_tuned.pkl")

    # MODEL LIST
    if isinstance(obj, dict):

        models = obj["models"]

        feat_cols = obj["features"]

    else:

        models = obj

        feat_cols = pd.read_csv(
            "features/feature_list.csv"
        )["feature"].tolist()

    # LOAD THRESHOLD
    with open("threshold.txt", "r") as f:

        threshold = float(f.read().strip())

    return models, feat_cols, threshold

def score_applicant(features, models, feat_cols, threshold):

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
    # APPLY BUSINESS RULES
    # ---------------------------------------------------

    prob, override_decision, override_risk, override_reasons = \
        apply_business_rules(
            prob,
            features,
            threshold
        )

    # ---------------------------------------------------
    # OVERRIDE DECISION
    # ---------------------------------------------------

    if override_decision:

        return (
            prob,
            std,
            override_decision,
            override_risk,
            scores,
            override_reasons
        )

    # ---------------------------------------------------
    # NORMAL MODEL DECISION
    # ---------------------------------------------------

    if prob >= threshold:

        if prob >= 0.55:

            risk = "high"

            decision = "HIGH RISK — REJECT"

        else:

            risk = "medium"

            decision = "REVIEW REQUIRED"

    else:

        risk = "low"

        decision = "LOW RISK — APPROVE"

    return (
        prob,
        std,
        decision,
        risk,
        scores,
        []
    )