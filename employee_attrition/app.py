import time

import pandas as pd
import plotly.express as px
import streamlit as st

from utils import (
    chart_path,
    default_employee_values,
    format_percent,
    load_data,
    load_model_bundle,
    metric_lookup,
    predict_attrition,
)


st.set_page_config(
    page_title="Employee Attrition Intelligence",
    page_icon="HR",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    :root {
        --ink: #17212b;
        --muted: #5c6875;
        --line: #d9e2ec;
        --green: #107c41;
        --red: #c43b3b;
        --blue: #1f5eff;
        --panel: #ffffff;
        --soft: #f5f8fb;
    }
    .main .block-container {
        padding-top: 1.7rem;
        padding-bottom: 1.2rem;
    }
    h1, h2, h3 {
        color: var(--ink);
        letter-spacing: 0;
    }
    .hero {
        border: 1px solid var(--line);
        background: linear-gradient(135deg, #ffffff 0%, #f5f8fb 55%, #eaf2ff 100%);
        padding: 1.35rem 1.45rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .hero h1 {
        margin: 0 0 .35rem 0;
        font-size: 2.05rem;
    }
    .hero p {
        color: var(--muted);
        margin: 0;
        max-width: 980px;
    }
    .metric-card {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--panel);
        padding: 1rem;
        min-height: 108px;
    }
    .metric-label {
        color: var(--muted);
        font-size: .88rem;
        margin-bottom: .35rem;
    }
    .metric-value {
        color: var(--ink);
        font-size: 1.65rem;
        font-weight: 700;
    }
    .section-note {
        color: var(--muted);
        font-size: .96rem;
        margin-bottom: .7rem;
    }
    .result-stay {
        border: 1px solid #b9dfc9;
        background: #effaf3;
        color: #0b5f31;
        padding: 1rem;
        border-radius: 8px;
        font-weight: 700;
    }
    .result-leave {
        border: 1px solid #efb8b8;
        background: #fff2f2;
        color: #9f2424;
        padding: 1rem;
        border-radius: 8px;
        font-weight: 700;
    }
    .footer {
        border-top: 1px solid var(--line);
        color: var(--muted);
        margin-top: 2rem;
        padding-top: .8rem;
        font-size: .9rem;
    }
    div[data-testid="stSidebar"] {
        background: #f7fafc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


df = load_data()
model, scaler, artifacts = load_model_bundle()
metrics = metric_lookup(artifacts)

st.sidebar.title("Workforce Intelligence")
page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Workforce Analytics",
        "Risk Assessment",
        "Model Performance",
        "Governance",
    ],
)
st.sidebar.markdown("---")
st.sidebar.caption("Scoring model: Gradient Boosting")
st.sidebar.caption(f"Risk threshold: {artifacts['threshold']:.2f}")


def hero(title, text):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_footer():
    st.markdown(
        "<div class='footer'>Employee Attrition Intelligence | Workforce analytics and attrition risk monitoring</div>",
        unsafe_allow_html=True,
    )


def home_page():
    hero(
        "Employee Attrition Intelligence Platform",
        "Centralized workforce risk monitoring for retention planning, talent strategy, and executive people decisions.",
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Workforce Records", f"{df.shape[0]:,}")
    with c2:
        metric_card("Profile Attributes", f"{df.shape[1] - 1}")
    with c3:
        metric_card("Observed Attrition", format_percent((df["Attrition"] == "Yes").mean()))
    with c4:
        metric_card("ROC-AUC", f"{metrics['ROC-AUC']:.3f}")

    st.subheader("Problem Statement")
    st.write(
        "Employee turnover affects workforce stability, operational continuity, and hiring costs. This platform identifies employees with elevated attrition risk using historical workforce data, enabling HR teams to prioritize retention actions and support workforce planning."
    )

    left, right = st.columns([1.1, 1])
    with left:
        st.subheader("Workforce Data Summary")
        st.dataframe(
            pd.DataFrame(
                {
                    "Item": ["Data Source", "Records", "Attributes", "Outcome Field", "Population Mix"],
                    "Details": [
                        "Historical IBM HR workforce records",
                        f"{df.shape[0]:,}",
                        f"{df.shape[1]}",
                        "Attrition: Yes / No",
                        "Retention-heavy workforce distribution",
                    ],
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
    with right:
        st.subheader("Platform Components")
        st.write("Python, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Plotly, Streamlit")
        st.subheader("Model Benchmarks")
        st.write("Logistic Regression, Random Forest, Gradient Boosting")
        st.subheader("Operational Scoring Model")
        st.write("Gradient Boosting Classifier with a 0.25 risk threshold, selected for the strongest F1 performance across benchmarked models.")

    st.subheader("Scoring Workflow")
    st.graphviz_chart(
        """
        digraph {
            rankdir=LR;
            node [shape=box, style="rounded,filled", fillcolor="#f5f8fb", color="#9fb2c8", fontname="Arial"];
            A [label="Historical Workforce Data"];
            B [label="Field Standardization"];
            C [label="Categorical Encoding"];
            D [label="Numeric Standardization"];
            E [label="Risk Driver Selection"];
            F [label="Model Benchmarking"];
            G [label="Gradient Boosting Scoring"];
            H [label="Attrition Risk Assessment"];
            A -> B -> C -> D -> E -> F -> G -> H;
        }
        """
    )


def data_analysis_page():
    hero(
        "Workforce Analytics",
        "Historical workforce patterns, attrition concentration, and retention signals across organizational, demographic, and compensation dimensions.",
    )
    chart_groups = [
        ("Workforce Distribution", "Employee_Attrition_Distribution.png"),
        ("Department-wise Risk", "Attrition_by_Department.png"),
        ("Role-based Attrition View", "Attrition_by_JobROle.png"),
        ("Compensation Trends", "MonthlyIncome_Vs_Attrition.png"),
        ("Demographic Insights", "Age_Distribution.png"),
        ("Tenure Risk Profile", "yearsAtCompany_vs_Attrition.png"),
        ("Work-Life Balance Indicators", "WorkLifeBalance_vs_Attrition.png"),
        ("Engagement Indicators", "JobSatisfaction_vs_Attrition.png"),
        ("Workforce Correlation Matrix", "Correlation_Matrix.png"),
    ]
    for i in range(0, len(chart_groups), 2):
        cols = st.columns(2)
        for col, (title, filename) in zip(cols, chart_groups[i : i + 2]):
            with col:
                st.subheader(title)
                st.image(str(chart_path(filename)), use_container_width=True)

    st.subheader("Key Workforce Signals")
    st.write(
        "Attrition risk is concentrated in Sales, with Sales Representatives and Laboratory Technicians showing elevated turnover patterns. Lower monthly income, shorter tenure, and weaker work-life balance indicators are also associated with higher attrition."
    )


def prediction_page():
    hero(
        "Risk Assessment",
        "Enter the employee profile to generate an attrition risk assessment aligned to the approved scoring pipeline.",
    )

    defaults = default_employee_values(df, artifacts)
    options = artifacts["raw_feature_options"]

    with st.form("prediction_form"):
        st.subheader("Employee Profile")
        profile_a, profile_b, profile_c = st.columns(3)
        with profile_a:
            age = st.number_input("Age", 18, 65, int(defaults["Age"]))
            gender = st.selectbox("Gender", options["Gender"], index=options["Gender"].index(defaults["Gender"]))
            marital = st.selectbox("Marital Status", options["MaritalStatus"], index=options["MaritalStatus"].index(defaults["MaritalStatus"]))
            education = st.number_input("Education", 1, 5, int(defaults["Education"]))
            education_field = st.selectbox("Education Field", options["EducationField"], index=options["EducationField"].index(defaults["EducationField"]))
        with profile_b:
            department = st.selectbox("Department", options["Department"], index=options["Department"].index(defaults["Department"]))
            job_role = st.selectbox("Job Role", options["JobRole"], index=options["JobRole"].index(defaults["JobRole"]))
            job_level = st.number_input("Job Level", 1, 5, int(defaults["JobLevel"]))
            job_involvement = st.number_input("Job Involvement", 1, 4, int(defaults["JobInvolvement"]))
            job_satisfaction = st.number_input("Job Satisfaction", 1, 4, int(defaults["JobSatisfaction"]))
        with profile_c:
            business_travel = st.selectbox("Business Travel", options["BusinessTravel"], index=options["BusinessTravel"].index(defaults["BusinessTravel"]))
            overtime = st.selectbox("Over Time", options["OverTime"], index=options["OverTime"].index(defaults["OverTime"]))
            environment_satisfaction = st.number_input("Environment Satisfaction", 1, 4, int(defaults["EnvironmentSatisfaction"]))
            relationship_satisfaction = st.number_input("Relationship Satisfaction", 1, 4, int(defaults["RelationshipSatisfaction"]))
            work_life_balance = st.number_input("Work Life Balance", 1, 4, int(defaults["WorkLifeBalance"]))

        st.subheader("Compensation and Work History")
        work_a, work_b, work_c = st.columns(3)
        with work_a:
            daily_rate = st.number_input("Daily Rate", 100, 1600, int(defaults["DailyRate"]))
            hourly_rate = st.number_input("Hourly Rate", 30, 100, int(defaults["HourlyRate"]))
            monthly_income = st.number_input("Monthly Income", 1000, 25000, int(defaults["MonthlyIncome"]))
            monthly_rate = st.number_input("Monthly Rate", 2000, 30000, int(defaults["MonthlyRate"]))
        with work_b:
            distance = st.number_input("Distance From Home", 1, 30, int(defaults["DistanceFromHome"]))
            percent_hike = st.number_input("Percent Salary Hike", 10, 25, int(defaults["PercentSalaryHike"]))
            performance = st.number_input("Performance Rating", 3, 4, int(defaults["PerformanceRating"]))
            stock = st.number_input("Stock Option Level", 0, 3, int(defaults["StockOptionLevel"]))
        with work_c:
            companies = st.number_input("Num Companies Worked", 0, 9, int(defaults["NumCompaniesWorked"]))
            total_years = st.number_input("Total Working Years", 0, 40, int(defaults["TotalWorkingYears"]))
            training = st.number_input("Training Times Last Year", 0, 6, int(defaults["TrainingTimesLastYear"]))

        st.subheader("Tenure Profile")
        t1, t2, t3, t4 = st.columns(4)
        with t1:
            years_company = st.number_input("Years At Company", 0, 40, int(defaults["YearsAtCompany"]))
        with t2:
            years_role = st.number_input("Years In Current Role", 0, 18, int(defaults["YearsInCurrentRole"]))
        with t3:
            years_promo = st.number_input("Years Since Last Promotion", 0, 15, int(defaults["YearsSinceLastPromotion"]))
        with t4:
            years_manager = st.number_input("Years With Current Manager", 0, 17, int(defaults["YearsWithCurrManager"]))

        submitted = st.form_submit_button("Generate Risk Assessment", use_container_width=True)

    employee_input = {
        "Age": age,
        "BusinessTravel": business_travel,
        "DailyRate": daily_rate,
        "Department": department,
        "DistanceFromHome": distance,
        "Education": education,
        "EducationField": education_field,
        "EnvironmentSatisfaction": environment_satisfaction,
        "Gender": gender,
        "HourlyRate": hourly_rate,
        "JobInvolvement": job_involvement,
        "JobLevel": job_level,
        "JobRole": job_role,
        "JobSatisfaction": job_satisfaction,
        "MaritalStatus": marital,
        "MonthlyIncome": monthly_income,
        "MonthlyRate": monthly_rate,
        "NumCompaniesWorked": companies,
        "OverTime": overtime,
        "PercentSalaryHike": percent_hike,
        "PerformanceRating": performance,
        "RelationshipSatisfaction": relationship_satisfaction,
        "StockOptionLevel": stock,
        "TotalWorkingYears": total_years,
        "TrainingTimesLastYear": training,
        "WorkLifeBalance": work_life_balance,
        "YearsAtCompany": years_company,
        "YearsInCurrentRole": years_role,
        "YearsSinceLastPromotion": years_promo,
        "YearsWithCurrManager": years_manager,
    }

    if submitted:
        with st.spinner("Generating attrition risk assessment..."):
            time.sleep(0.4)
            prediction, probability, confidence = predict_attrition(
                employee_input, model, scaler, artifacts
            )

        result_class = "result-leave" if prediction == 1 else "result-stay"
        result_text = "Elevated Attrition Risk" if prediction == 1 else "Low Attrition Risk"
        st.subheader("Assessment Outcome")
        st.markdown(f"<div class='{result_class}'>{result_text}</div>", unsafe_allow_html=True)

        r1, r2, r3 = st.columns(3)
        with r1:
            st.metric("Attrition Risk Probability", format_percent(probability))
        with r2:
            st.metric("Assessment Confidence", format_percent(confidence))
        with r3:
            st.metric("Risk Threshold", f"{artifacts['threshold']:.2f}")

        st.subheader("Business Interpretation")
        if prediction == 1:
            st.error(
                "This profile exhibits characteristics historically associated with higher voluntary turnover. HR teams may review engagement, compensation, tenure, workload, and manager support signals in line with retention policy."
            )
        else:
            st.success(
                "This profile is aligned with lower-risk historical workforce patterns. Continue standard engagement monitoring and workforce planning review cycles."
            )


def model_performance_page():
    hero(
        "Model Performance Metrics",
        "Performance indicators for the approved attrition risk scoring model and benchmarked alternatives.",
    )
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        metric_card("Accuracy", f"{metrics['Accuracy']:.3f}")
    with m2:
        metric_card("Precision", f"{metrics['Precision']:.3f}")
    with m3:
        metric_card("Recall", f"{metrics['Recall']:.3f}")
    with m4:
        metric_card("F1 Score", f"{metrics['F1 Score']:.3f}")
    with m5:
        metric_card("ROC-AUC", f"{metrics['ROC-AUC']:.3f}")

    st.subheader("Benchmark Summary")
    comparison = artifacts["comparison"].copy()
    st.dataframe(comparison.round(3), use_container_width=True, hide_index=True)
    comparison_long = comparison.melt(id_vars="Model", var_name="Metric", value_name="Score")
    fig = px.bar(
        comparison_long,
        x="Model",
        y="Score",
        color="Metric",
        barmode="group",
        template="plotly_white",
        color_discrete_sequence=["#1f5eff", "#0f9d58", "#f4b400", "#c43b3b"],
    )
    fig.update_layout(legend_title_text="", yaxis_range=[0, 1])
    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Classification Outcomes")
        st.image(str(chart_path("Confusion_matrix.png")), use_container_width=True)
    with right:
        st.subheader("Risk Discrimination Curve")
        st.image(str(chart_path("ROC_Curve.png")), use_container_width=True)

    st.subheader("Risk Driver Analysis")
    importance = artifacts["feature_importance"].head(15)
    fig_imp = px.bar(
        importance.sort_values("Importance"),
        x="Importance",
        y="Feature",
        orientation="h",
        template="plotly_white",
        color="Importance",
        color_continuous_scale=["#dce9f9", "#1f5eff"],
    )
    fig_imp.update_layout(coloraxis_showscale=False, height=520)
    st.plotly_chart(fig_imp, use_container_width=True)
    st.image(str(chart_path("Feature_Importance.png")), use_container_width=True)

    st.subheader("Threshold Sensitivity")
    st.image(str(chart_path("Decision_Threshold.png")), use_container_width=True)


def about_page():
    hero(
        "Governance",
        "Implementation notes for model lineage, scoring methodology, and deployment assets.",
    )
    st.subheader("Scoring Methodology")
    st.write(
        "The scoring workflow removes identifier and constant fields, maps Attrition to binary outcomes, applies drop-first one-hot encoding, uses stratified sampling, standardizes numeric attributes, selects the top 25 risk drivers using Random Forest importance, and benchmarks Logistic Regression, Random Forest, and Gradient Boosting."
    )
    st.subheader("Operational Model Selection")
    st.write(
        "Gradient Boosting at a 0.25 threshold delivered the strongest F1 performance across benchmarked models, balancing precision and recall for attrition-risk identification."
    )
    st.subheader("Artifact Governance")
    st.write(
        "Serialized artifacts retain the approved Gradient Boosting model, scaler, feature schema, selected drivers, benchmark results, and performance metrics. Runtime scoring loads these artifacts directly and does not retrain."
    )
    st.subheader("Deployment Assets")
    st.code(
        """employee_attrition/
|-- app.py
|-- utils.py
|-- model.pkl
|-- scaler.pkl
|-- artifacts.pkl
|-- assets/charts/
|-- notebook.ipynb
|-- IBM-HR-Employee-Attrition.csv
|-- requirements.txt
|-- README.md""",
        language="text",
    )


if page == "Executive Overview":
    home_page()
elif page == "Workforce Analytics":
    data_analysis_page()
elif page == "Risk Assessment":
    prediction_page()
elif page == "Model Performance":
    model_performance_page()
else:
    about_page()

show_footer()
