import numpy as np


def create_features(
    age,
    gender,
    children,
    family_members,
    employment_years,
    income,
    credit_amount,
    annuity,
    goods_price,
    ext1,
    ext2,
    ext3,
    prev_refused
):

    eps = 1e-5

    days_birth = -age * 365
    days_employed = -employment_years * 365 if employment_years > 0 else 365243

    emp_anom = 1 if employment_years == 0 else 0

    ext_mean = float(np.mean([ext1, ext2, ext3]))
    ext_std = float(np.std([ext1, ext2, ext3]))
    ext_min = min(ext1, ext2, ext3)
    ext_max = max(ext1, ext2, ext3)

    ext_product = ext1 * ext2 * ext3
    ext_weighted = 0.25 * ext1 + 0.50 * ext2 + 0.25 * ext3

    credit_income = credit_amount / (income + eps)
    annuity_income = annuity * 12 / (income + eps)
    credit_term = credit_amount / (annuity + eps)
    credit_goods = credit_amount / (goods_price + eps)

    income_per_person = income / (family_members + eps)

    employed_age = days_employed / (days_birth + eps)

    applicant = {

        'DAYS_BIRTH': days_birth,

        'DAYS_EMPLOYED':
            np.log1p(abs(days_employed))
            if employment_years > 0 else 0,

        'DAYS_EMPLOYED_ANOM': emp_anom,

        'AMT_INCOME_TOTAL': np.log1p(income),

        'AMT_CREDIT': np.log1p(credit_amount),

        'AMT_ANNUITY': np.log1p(annuity * 12),

        'AMT_GOODS_PRICE': np.log1p(goods_price),

        'CNT_CHILDREN': children,

        'CNT_FAM_MEMBERS': family_members,

        'CODE_GENDER': 1 if gender == "Male" else 0,

        'EXT_SOURCE_1': ext1,
        'EXT_SOURCE_2': ext2,
        'EXT_SOURCE_3': ext3,

        'APP_EXT_SOURCE_MEAN': ext_mean,
        'APP_EXT_SOURCE_STD': ext_std,
        'APP_EXT_SOURCE_MIN': ext_min,
        'APP_EXT_SOURCE_MAX': ext_max,

        'APP_EXT_SOURCE_RANGE': ext_max - ext_min,

        'APP_EXT_SOURCE_PRODUCT': ext_product,

        'APP_EXT_WEIGHTED': ext_weighted,

        'APP_EXT2_x_CREDIT_INCOME':
            ext2 * credit_income,

        'APP_EXT3_x_ANNUITY_INCOME':
            ext3 * annuity_income,

        'APP_AGE_YEARS': age,

        'APP_AGE_YEARS_SQUARED': age ** 2,

        'APP_EMPLOYMENT_YEARS': employment_years,

        'APP_EMPLOYED_TO_AGE_RATIO': employed_age,

        'APP_CREDIT_INCOME_RATIO': credit_income,

        'APP_INCOME_CREDIT_RATIO':
            income / (credit_amount + eps),

        'APP_ANNUITY_INCOME_RATIO': annuity_income,

        'APP_CREDIT_TERM': credit_term,

        'APP_CREDIT_TO_GOODS_RATIO': credit_goods,

        'APP_GOODS_CREDIT_DIFF':
            goods_price - credit_amount,

        'APP_INCOME_PER_PERSON': income_per_person,

        'APP_ANNUITY_TO_GOODS_RATIO':
            (annuity * 12) / (goods_price + eps),

        'PREV_REFUSAL_RATE':
            prev_refused / 10.0,

        'PREV_REFUSED_COUNT': prev_refused,

        'CROSS_REFUSAL_x_CREDIT_INCOME':
            (prev_refused / 10.0) * credit_income,

        'EXT_SOURCE_1_IS_NULL': 0,
        'EXT_SOURCE_2_IS_NULL': 0,
        'EXT_SOURCE_3_IS_NULL': 0,
    }

    return applicant