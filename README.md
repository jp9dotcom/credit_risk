# credit_risk

# 🏦 AI-Powered Credit Risk Prediction System

A production-style end-to-end Machine Learning application built on the **Home Credit Default Risk** dataset to predict the probability of loan default using advanced feature engineering, business-driven analytics, and explainable risk scoring.

This project combines:

* 📊 Advanced Exploratory Data Analysis
* ⚙️ Enterprise-grade Feature Engineering
* 🤖 Gradient Boosting ML Models
* 📈 Business Intelligence Dashboards
* 🎯 Credit Risk Segmentation
* 🌐 Interactive Streamlit Web Application

---

# 🚀 Project Overview

Financial institutions face a major challenge while approving loans:

> How can lenders identify potentially risky applicants without rejecting financially capable customers?

This project solves that problem by building a complete AI-driven credit risk pipeline capable of:

* Predicting customer default probability
* Segmenting borrowers into risk groups
* Visualizing important financial drivers
* Providing business-level lending insights
* Supporting explainable decision-making

The system is designed to simulate a real-world credit underwriting workflow used in fintech and banking industries.

---

# ✨ Key Features

## 🔍 Advanced Data Pipeline

* Multi-file relational dataset processing
* Missing value analysis & treatment
* Anomaly detection
* Leakage-safe preprocessing
* Feature scaling & encoding
* Business-rule-based transformations

## 🧠 Intelligent Feature Engineering

* Bureau history aggregation
* Previous loan behavior analysis
* Installment payment trends
* Credit utilization metrics
* Debt-to-income features
* EXT_SOURCE interaction features
* Customer-level aggregated statistics

## 📉 Dimensionality Reduction

* Per-block PCA implementation
* Noise reduction strategy
* Importance-based feature filtering
* Memory-efficient training pipeline

## 🤖 Machine Learning Modeling

* XGBoost-based classification pipeline
* Hyperparameter tuning with Optuna
* Stratified K-Fold Cross Validation
* Out-of-Fold validation strategy
* Threshold optimization using Youden’s J Statistic
* Probability-based risk prediction

## 📊 Interactive Dashboard

Built using Streamlit with:

* Real-time credit scoring
* Business KPI dashboards
* Customer segmentation analysis
* Feature importance visualization
* Risk probability explanations
* Portfolio-level analytics

---

# 🛠️ Tech Stack

| Category            | Technologies                  |
| ------------------- | ----------------------------- |
| Programming         | Python                        |
| ML Libraries        | Scikit-learn, XGBoost, Optuna |
| Data Processing     | Pandas, NumPy                 |
| Visualization       | Plotly, Matplotlib, Seaborn   |
| Web App             | Streamlit                     |
| Model Serialization | Joblib                        |
| Version Control     | Git & GitHub                  |

---

# 📂 Project Structure

```bash
credit-risk/
│
├── app.py                         # Main Streamlit application
├── requirements.txt
├── LICENSE
├── README.md
│
├── notebooks/
│   ├── data_understanding.ipynb
│   ├── eda.ipynb
│   ├── preprocessing.ipynb
│   ├── feature_engineering.ipynb
│   ├── business_insights.ipynb
│   └── pca.ipynb
│
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Customer_Segments.py
│   └── 3_Model_Insights.py
│
├── utils/
│   ├── business_rules.py
│   ├── feature_engineering.py
│   ├── model_utils.py
│   ├── segmentation.py
│   └── styles.py
│
├── features/
├── models/
└── logs/
```

---

# 📊 Dataset

Dataset used: **Home Credit Default Risk**

The dataset contains customer-level financial, behavioral, and historical credit information from multiple relational tables.

### Key Data Sources

* Application Data
* Bureau Credit History
* Previous Applications
* Installment Payments
* POS Cash Balance
* Credit Card Balance

The objective is binary classification:

| Target | Meaning                                     |
| ------ | ------------------------------------------- |
| 0      | Customer repaid loan successfully           |
| 1      | Customer faced payment difficulties/default |

---

# 🧪 ML Pipeline Workflow

## Phase 1 — Data Understanding

* Schema inspection
* Join-key validation
* Missing value profiling
* Target imbalance analysis
* Column categorization

## Phase 2 — Exploratory Data Analysis

* Numeric distributions
* Categorical frequency analysis
* Bivariate target analysis
* Outlier inspection
* EXT_SOURCE feature investigation

## Phase 3 — Preprocessing

* High-null column removal
* Missingness flags
* Median/Mode imputation
* Anomaly correction
* Leakage-safe transformations

## Phase 4 — Feature Engineering

* Bureau-level aggregations
* Installment behavior patterns
* Credit-to-income ratios
* Cross-feature interactions
* Temporal aggregation features

## Phase 5 — PCA & Dimensionality Reduction

* Per-block PCA strategy
* Feature importance filtering
* Variance preservation
* Dimensionality optimization

## Phase 6 — Model Training & Optimization

* Stratified K-Fold validation
* XGBoost classifier training
* Optuna hyperparameter tuning
* Threshold optimization
* Probability calibration

---

# 📈 Business Insights

The project goes beyond prediction and focuses heavily on business understanding.

### Included Business Analytics

* Default rate by income group
* Employment-type risk analysis
* Education-level segmentation
* Age-band default patterns
* Credit-to-income interaction analysis
* Customer risk clustering

These insights help financial institutions:

* Improve underwriting quality
* Reduce non-performing loans
* Optimize approval strategies
* Understand customer behavior patterns

---

# 🌐 Streamlit Application

The application provides an enterprise-style UI for:

✅ Credit Risk Prediction
✅ Portfolio Monitoring
✅ Customer Segmentation
✅ Model Explainability
✅ Risk Visualization
✅ Interactive Analytics

### Main Application Pages

| Page              | Description                         |
| ----------------- | ----------------------------------- |
| Dashboard         | Main credit scoring interface       |
| Customer Segments | Risk segmentation & analysis        |
| Model Insights    | Feature importance & model behavior |

---

# ⚡ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/jp9dotcom/credit_risk.git
cd credit_risk
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Run Streamlit App

```bash
streamlit run app.py
```

---

# 📌 Important ML Concepts Used

This project implements several industry-standard ML techniques:

* Stratified K-Fold Cross Validation
* Out-of-Fold (OOF) Validation
* Optuna Hyperparameter Optimization
* Threshold Tuning with Youden’s J Statistic
* Feature Importance Analysis
* PCA-based Dimensionality Reduction
* Probability-based Classification
* Business-driven Feature Engineering

---

# 🎯 Real-World Applications

This system can be adapted for:

* Banking Loan Approval
* Fintech Lending Platforms
* Credit Card Risk Assessment
* BNPL (Buy Now Pay Later) Systems
* Insurance Risk Modeling
* Customer Financial Profiling

---

# 🔮 Future Improvements

Potential enhancements:

* SHAP explainability integration
* Real-time API deployment
* Docker containerization
* Cloud deployment (AWS/GCP/Azure)
* Deep Learning ensemble models
* Drift monitoring pipeline
* Automated retraining workflow

---

# 👨‍💻 Author

## Jay Patil

Machine Learning & AI Enthusiast

Special interests:

* Machine Learning
* Credit Risk Modeling
* Explainable AI
* MLOps
* Data Science
* Business Intelligence

---

# 📜 License

This project is licensed under the MIT License.

---

# ⭐ Acknowledgements

* Home Credit Group
* Kaggle Home Credit Default Risk Competition
* Open-source Python ML ecosystem
* Streamlit Community

---

# 💡 Final Note

This project was built with a strong focus on:

* Real-world ML pipeline design
* Business interpretability
* Enterprise-style analytics
* Production-oriented architecture
* Explainable risk scoring

The goal was not just to train a model, but to create a complete AI-powered credit risk intelligence system similar to workflows used in modern fintech organizations.
