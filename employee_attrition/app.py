import time

import pandas as pd
import streamlit as st

import charts
from components import (
    apply_css,
    content_card,
    empty_assessment,
    footer,
    hero,
    kpi_card,
    loading_sequence,
    risk_summary,
    section_title,
    topbar,
)
from styles import APP_CSS
from utils import (
    chart_path,
    default_employee_values,
    format_percent,
    load_data,
    load_model_bundle,
    metric_lookup,
    predict_attrition,
)


MODEL_NAME = "Gradient Boosting"
ORG_NAME = "Enterprise HR Analytics"


st.set_page_config(
    page_title="Employee Attrition Intelligence",
    page_icon="HR",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_css(APP_CSS)

df = load_data()
model, scaler, artifacts = load_model_bundle()
metrics = metric_lookup(artifacts)

loading_sequence()
topbar(MODEL_NAME, artifacts["threshold"])


def sidebar_navigation():
    st.sidebar.markdown("## Workforce Intelligence")
    st.sidebar.caption("Enterprise attrition risk console")
    page = st.sidebar.radio(
        "Navigation",
        [
            "Executive Overview",
            "Risk Assessment",
            "Workforce Analytics",
            "Feature Insights",
            "Model Performance",
            "Governance",
        ],
    )
    st.sidebar.markdown("---")
    st.sidebar.caption(f"Model: {MODEL_NAME}")
    st.sidebar.caption(f"Risk threshold: {artifacts['threshold']:.2f}")
    st.sidebar.caption("Status: Online")
    return page


def employee_profile_sidebar():
    defaults = default_employee_values(df, artifacts)
    options = artifacts["raw_feature_options"]
    st.sidebar.markdown("### Employee Profile")
    st.sidebar.caption("Complete the profile to generate a risk assessment.")

    with st.sidebar.expander("Personal Information", expanded=True):
        age = st.number_input("Age", 18, 65, int(defaults["Age"]))
        gender = st.selectbox("Gender", options["Gender"], index=options["Gender"].index(defaults["Gender"]))
        marital = st.selectbox(
            "Marital Status",
            options["MaritalStatus"],
            index=options["MaritalStatus"].index(defaults["MaritalStatus"]),
        )
        education = st.number_input("Education", 1, 5, int(defaults["Education"]))
        education_field = st.selectbox(
            "Education Field",
            options["EducationField"],
            index=options["EducationField"].index(defaults["EducationField"]),
        )

    with st.sidebar.expander("Job Information", expanded=True):
        department = st.selectbox(
            "Department",
            options["Department"],
            index=options["Department"].index(defaults["Department"]),
        )
        job_role = st.selectbox(
            "Job Role",
            options["JobRole"],
            index=options["JobRole"].index(defaults["JobRole"]),
        )
        job_level = st.number_input("Job Level", 1, 5, int(defaults["JobLevel"]))
        job_involvement = st.number_input("Job Involvement", 1, 4, int(defaults["JobInvolvement"]))
        job_satisfaction = st.number_input("Job Satisfaction", 1, 4, int(defaults["JobSatisfaction"]))

    with st.sidebar.expander("Compensation", expanded=False):
        daily_rate = st.number_input("Daily Rate", 100, 1600, int(defaults["DailyRate"]))
        hourly_rate = st.number_input("Hourly Rate", 30, 100, int(defaults["HourlyRate"]))
        monthly_income = st.number_input("Monthly Income", 1000, 25000, int(defaults["MonthlyIncome"]))
        monthly_rate = st.number_input("Monthly Rate", 2000, 30000, int(defaults["MonthlyRate"]))
        percent_hike = st.number_input("Percent Salary Hike", 10, 25, int(defaults["PercentSalaryHike"]))
        stock = st.number_input("Stock Option Level", 0, 3, int(defaults["StockOptionLevel"]))

    with st.sidebar.expander("Work Environment", expanded=False):
        business_travel = st.selectbox(
            "Business Travel",
            options["BusinessTravel"],
            index=options["BusinessTravel"].index(defaults["BusinessTravel"]),
        )
        overtime = st.selectbox("Over Time", options["OverTime"], index=options["OverTime"].index(defaults["OverTime"]))
        distance = st.number_input("Distance From Home", 1, 30, int(defaults["DistanceFromHome"]))
        environment_satisfaction = st.number_input(
            "Environment Satisfaction",
            1,
            4,
            int(defaults["EnvironmentSatisfaction"]),
        )
        relationship_satisfaction = st.number_input(
            "Relationship Satisfaction",
            1,
            4,
            int(defaults["RelationshipSatisfaction"]),
        )
        work_life_balance = st.number_input("Work Life Balance", 1, 4, int(defaults["WorkLifeBalance"]))

    with st.sidebar.expander("Performance and Tenure", expanded=False):
        performance = st.number_input("Performance Rating", 3, 4, int(defaults["PerformanceRating"]))
        companies = st.number_input("Num Companies Worked", 0, 9, int(defaults["NumCompaniesWorked"]))
        total_years = st.number_input("Total Working Years", 0, 40, int(defaults["TotalWorkingYears"]))
        training = st.number_input("Training Times Last Year", 0, 6, int(defaults["TrainingTimesLastYear"]))
        years_company = st.number_input("Years At Company", 0, 40, int(defaults["YearsAtCompany"]))
        years_role = st.number_input("Years In Current Role", 0, 18, int(defaults["YearsInCurrentRole"]))
        years_promo = st.number_input(
            "Years Since Last Promotion",
            0,
            15,
            int(defaults["YearsSinceLastPromotion"]),
        )
        years_manager = st.number_input(
            "Years With Current Manager",
            0,
            17,
            int(defaults["YearsWithCurrManager"]),
        )

    profile = {
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
    submitted = st.sidebar.button("Generate Risk Assessment", use_container_width=True)
    return profile, submitted


def executive_kpis():
    attrition_rate = (df["Attrition"] == "Yes").mean()
    departments = df["Department"].nunique()
    confidence = max(metrics["Precision"], metrics["Recall"])
    high_risk_baseline = int((df["Attrition"] == "Yes").sum())

    cols = st.columns(6)
    kpis = [
        ("Employees Analyzed", f"{df.shape[0]:,}", "Historical workforce records", "EA", "Live"),
        ("Average Attrition Risk", format_percent(attrition_rate), "Observed workforce baseline", "AR", "Tracked"),
        ("Departments", f"{departments}", "Business units represented", "DP", "Mapped"),
        ("Prediction Confidence", format_percent(confidence), "Operational confidence signal", "PC", "Model"),
        ("Model Accuracy", f"{metrics['Accuracy']:.3f}", "Validation performance", "MA", "Approved"),
        ("High Risk Employees", f"{high_risk_baseline}", "Historical attrition cases", "HR", "Watch"),
    ]
    for col, item in zip(cols, kpis):
        with col:
            kpi_card(*item)


def executive_overview_page():
    hero(
        "Employee Attrition Intelligence Platform",
        "Executive workforce risk monitoring for retention planning, operational continuity, and talent strategy.",
        actions=["Review executive KPIs", "Assess employee risk", "Monitor risk drivers"],
    )
    executive_kpis()

    overview_tab, impact_tab, workflow_tab = st.tabs(["Executive KPIs", "Business Impact", "Scoring Workflow"])

    with overview_tab:
        section_title(
            "Workforce Risk Snapshot",
            "Current workforce composition and attrition concentration across the historical employee population.",
            "Overview",
        )
        left, right = st.columns([1.05, 1])
        with left:
            st.plotly_chart(charts.attrition_distribution(df), use_container_width=True)
        with right:
            st.plotly_chart(charts.department_risk(df), use_container_width=True)

    with impact_tab:
        section_title(
            "Business Decision Context",
            "Retention intelligence for HR Business Partners, workforce planning, and leadership review.",
            "Decision Support",
        )
        c1, c2, c3 = st.columns(3)
        with c1:
            content_card(
                "Operational Continuity",
                "Early attrition risk visibility supports succession planning, workload continuity, and targeted manager interventions.",
            )
        with c2:
            content_card(
                "Retention Prioritization",
                "Risk signals help HR teams focus engagement, development, and compensation reviews where historical patterns indicate higher exposure.",
            )
        with c3:
            content_card(
                "Workforce Planning",
                "Department and role-level trends support hiring forecasts, internal mobility planning, and leadership workforce reviews.",
            )

    with workflow_tab:
        section_title(
            "Approved Scoring Workflow",
            "The operational flow preserves the validated preprocessing and model scoring sequence.",
            "Governed Pipeline",
        )
        st.graphviz_chart(
            """
            digraph {
                rankdir=LR;
                graph [bgcolor="transparent"];
                node [shape=box, style="rounded,filled", fillcolor="#FFFDF9", color="#D4A017", fontname="Inter", fontcolor="#102A43"];
                A [label="Historical Workforce Data"];
                B [label="Field Standardization"];
                C [label="Categorical Encoding"];
                D [label="Numeric Standardization"];
                E [label="Risk Driver Selection"];
                F [label="Model Benchmarking"];
                G [label="Gradient Boosting Scoring"];
                H [label="Risk Assessment"];
                A -> B -> C -> D -> E -> F -> G -> H;
            }
            """
        )


def risk_assessment_page():
    hero(
        "Employee Risk Assessment",
        "Generate an attrition risk assessment from the employee profile maintained in the sidebar.",
        eyebrow="Predictive Workforce Review",
        actions=["Complete profile", "Generate assessment", "Review recommendation"],
    )
    profile, submitted = employee_profile_sidebar()

    if submitted:
        with st.spinner("Generating attrition risk assessment..."):
            time.sleep(0.45)
            prediction, probability, confidence = predict_attrition(profile, model, scaler, artifacts)
        st.session_state["last_assessment"] = {
            "prediction": prediction,
            "probability": probability,
            "confidence": confidence,
            "profile": profile,
        }

    left, right = st.columns([1.08, 0.92])
    with left:
        section_title(
            "Prediction Summary",
            "Risk score, confidence, retention priority, and recommended HR action.",
            "Assessment Outcome",
        )
        assessment = st.session_state.get("last_assessment")
        if assessment:
            risk_summary(
                assessment["probability"],
                assessment["confidence"],
                artifacts["threshold"],
            )
        else:
            empty_assessment()

    with right:
        section_title(
            "Risk Visualization",
            "Gauge and confidence indicators calibrated to the operational threshold.",
            "Probability Meter",
        )
        assessment = st.session_state.get("last_assessment")
        if assessment:
            st.plotly_chart(
                charts.risk_gauge(assessment["probability"], artifacts["threshold"]),
                use_container_width=True,
            )
            st.plotly_chart(charts.confidence_meter(assessment["confidence"]), use_container_width=True)
        else:
            content_card(
                "No Assessment Generated",
                "Use the sidebar profile sections to prepare the employee record and generate the first risk assessment.",
            )

    section_title(
        "Employee Profile Review",
        "Submitted profile values are shown for HR review and audit context.",
        "Profile Context",
    )
    if st.session_state.get("last_assessment"):
        profile_df = pd.DataFrame([st.session_state["last_assessment"]["profile"]]).T.reset_index()
        profile_df.columns = ["Attribute", "Value"]
        st.dataframe(profile_df, use_container_width=True, hide_index=True)


def workforce_analytics_page():
    hero(
        "Workforce Analytics",
        "Interactive workforce views across attrition outcomes, departments, roles, compensation, age, tenure, and overtime exposure.",
        eyebrow="People Analytics",
        actions=["Analyze distribution", "Compare departments", "Review compensation signals"],
    )
    section_title(
        "Executive Analytics Workspace",
        "Interactive views support filtering, hover inspection, and detailed workforce trend review.",
        "Interactive Visualizations",
    )

    tab1, tab2, tab3, tab4 = st.tabs(["Workforce Overview", "Department Analysis", "Compensation Trends", "Governed Outputs"])
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(charts.attrition_distribution(df), use_container_width=True)
        with c2:
            st.plotly_chart(charts.age_distribution(df), use_container_width=True)
        st.plotly_chart(charts.role_breakdown(df), use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(charts.department_risk(df), use_container_width=True)
        with c2:
            st.plotly_chart(charts.overtime_impact(df), use_container_width=True)
        st.plotly_chart(charts.tenure_risk(df), use_container_width=True)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(charts.income_distribution(df), use_container_width=True)
        with c2:
            st.plotly_chart(charts.salary_band_analysis(df), use_container_width=True)

    with tab4:
        section_title(
            "Validated Notebook Visuals",
            "Original analysis outputs are retained for continuity with the approved analytical record.",
            "Source Visuals",
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
        ]
        for index in range(0, len(chart_groups), 2):
            cols = st.columns(2)
            for col, (title, filename) in zip(cols, chart_groups[index : index + 2]):
                with col:
                    st.subheader(title)
                    st.image(str(chart_path(filename)), use_container_width=True)


def feature_insights_page():
    hero(
        "Feature Insights",
        "Risk driver analysis for understanding which employee attributes most influence attrition scoring.",
        eyebrow="Model Explainability",
        actions=["Review drivers", "Inspect correlations", "Monitor risk indicators"],
    )
    c1, c2 = st.columns([1, 1])
    with c1:
        section_title(
            "Risk Driver Analysis",
            "Top attributes contributing to Gradient Boosting attrition scoring.",
            "Feature Importance",
        )
        st.plotly_chart(charts.feature_importance(artifacts["feature_importance"]), use_container_width=True)
    with c2:
        section_title(
            "Risk Indicator Summary",
            "Primary workforce signals observed across the historical population.",
            "Business Signals",
        )
        content_card(
            "High-impact Factors",
            "Monthly income, age, total working years, overtime, number of companies worked, tenure with current manager, and distance from home are prominent attrition risk drivers.",
        )
        content_card(
            "Retention Levers",
            "Compensation review, workload monitoring, manager enablement, engagement planning, and early-tenure support are the most relevant HR response areas.",
        )

    section_title(
        "Correlation Heatmap",
        "Numeric workforce relationships for broader analytical review.",
        "Workforce Signals",
    )
    st.plotly_chart(charts.correlation_heatmap(df), use_container_width=True)


def model_performance_page():
    hero(
        "Model Performance",
        "Validation metrics, benchmark comparison, and retained evaluation outputs for the operational attrition model.",
        eyebrow="Model Governance",
        actions=["Review metrics", "Compare models", "Monitor threshold"],
    )
    cols = st.columns(5)
    metric_items = [
        ("Accuracy", f"{metrics['Accuracy']:.3f}", "Overall validation performance", "AC", "Metric"),
        ("Precision", f"{metrics['Precision']:.3f}", "Positive risk identification quality", "PR", "Metric"),
        ("Recall", f"{metrics['Recall']:.3f}", "Attrition class capture rate", "RC", "Metric"),
        ("F1 Score", f"{metrics['F1 Score']:.3f}", "Precision and recall balance", "F1", "Metric"),
        ("ROC-AUC", f"{metrics['ROC-AUC']:.3f}", "Risk discrimination strength", "RA", "Metric"),
    ]
    for col, item in zip(cols, metric_items):
        with col:
            kpi_card(*item)

    section_title(
        "Benchmark Summary",
        "Model comparison across precision, recall, F1 score, and ROC-AUC.",
        "Model Comparison",
    )
    st.dataframe(artifacts["comparison"].round(3), use_container_width=True, hide_index=True)
    st.plotly_chart(charts.model_comparison(artifacts["comparison"]), use_container_width=True)

    tab1, tab2, tab3 = st.tabs(["Classification Outcomes", "Risk Discrimination", "Threshold Sensitivity"])
    with tab1:
        st.image(str(chart_path("Confusion_matrix.png")), use_container_width=True)
    with tab2:
        st.image(str(chart_path("ROC_Curve.png")), use_container_width=True)
    with tab3:
        st.image(str(chart_path("Decision_Threshold.png")), use_container_width=True)


def governance_page():
    hero(
        "Governance",
        "Model lineage, deployment assets, and data handling notes for operational HR analytics review.",
        eyebrow="Platform Administration",
        actions=["Review lineage", "Validate artifacts", "Confirm controls"],
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        content_card(
            "Scoring Methodology",
            "The workflow removes identifier and constant fields, maps attrition outcomes, applies drop-first one-hot encoding, standardizes numeric attributes, and scores the selected feature set.",
        )
    with c2:
        content_card(
            "Operational Model",
            "Gradient Boosting at a 0.25 threshold delivered the strongest F1 performance across benchmarked models for attrition-risk identification.",
        )
    with c3:
        content_card(
            "Artifact Control",
            "Runtime scoring loads the serialized model, scaler, feature schema, selected drivers, benchmark results, and performance metrics directly.",
        )

    section_title(
        "Deployment Assets",
        "Application files retained for production packaging and technical review.",
        "Asset Register",
    )
    st.code(
        """employee_attrition/
|-- app.py
|-- components.py
|-- styles.py
|-- charts.py
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
    section_title(
        "Data Security Notice",
        "Workforce data is confidential and intended for authorized HR analytics, HR Business Partner, and leadership workforce planning use.",
        "Controls",
    )


page = sidebar_navigation()

if page == "Executive Overview":
    executive_overview_page()
elif page == "Risk Assessment":
    risk_assessment_page()
elif page == "Workforce Analytics":
    workforce_analytics_page()
elif page == "Feature Insights":
    feature_insights_page()
elif page == "Model Performance":
    model_performance_page()
else:
    governance_page()

footer(MODEL_NAME, artifacts["threshold"])
