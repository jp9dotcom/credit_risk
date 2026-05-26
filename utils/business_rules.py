def apply_business_rules(prob, features, threshold):

    """
    Hard underwriting rules.
    These override ML predictions when lending standards are violated.
    """

    credit_income = features.get('APP_CREDIT_INCOME_RATIO', 0)

    annuity_income = features.get('APP_ANNUITY_INCOME_RATIO', 0)

    credit_goods = features.get('APP_CREDIT_TO_GOODS_RATIO', 0)

    age = features.get('APP_AGE_YEARS', 35)

    prev_refused = features.get('PREV_REFUSED_COUNT', 0)

    ext_mean = features.get('APP_EXT_SOURCE_MEAN', 0.5)

    overrides = []

    # ---------------------------------------------------
    # RULE 1
    # ---------------------------------------------------

    if credit_income > 10:

        overrides.append(
            f"Credit-to-income {credit_income:.1f}× exceeds policy limit (10×)"
        )

    # ---------------------------------------------------
    # RULE 2
    # ---------------------------------------------------

    if annuity_income > 0.60:

        overrides.append(
            f"EMI burden {annuity_income*100:.0f}% exceeds maximum allowed (60%)"
        )

    # ---------------------------------------------------
    # RULE 3
    # ---------------------------------------------------

    if credit_goods > 2.0:

        overrides.append(
            f"Loan-to-value {credit_goods:.1f}× exceeds policy guideline"
        )

    # ---------------------------------------------------
    # RULE 4
    # ---------------------------------------------------

    if ext_mean < 0.20:

        overrides.append(
            f"Average bureau score {ext_mean:.3f} below minimum threshold"
        )

    # ---------------------------------------------------
    # RULE 5
    # ---------------------------------------------------

    if age < 21:

        overrides.append(
            f"Applicant age {age} below minimum requirement"
        )

    # ---------------------------------------------------
    # RULE 6
    # ---------------------------------------------------

    if prev_refused >= 3:

        overrides.append(
            f"{prev_refused} previous refusals — mandatory manual review"
        )

    # ---------------------------------------------------
    # FINAL OVERRIDE
    # ---------------------------------------------------

    if len(overrides) > 0:

        forced_prob = max(prob, 0.70)

        return (
            forced_prob,
            "HIGH RISK — REJECT (Policy Override)",
            "high",
            overrides
        )

    return (
        prob,
        None,
        None,
        []
    )