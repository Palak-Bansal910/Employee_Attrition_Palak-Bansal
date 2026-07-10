import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


NAVY = "#102A43"
GOLD = "#D4A017"
ORANGE = "#E67E22"
GREEN = "#0E8F5A"
AMBER = "#B7791F"
RED = "#B83232"
BEIGE = "#F5F1EA"
CARD = "#FFFDF9"


def enterprise_layout(fig, height=420):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=CARD,
        font={"family": "Inter, IBM Plex Sans, Segoe UI, sans-serif", "color": NAVY},
        margin={"l": 24, "r": 24, "t": 50, "b": 24},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "bgcolor": "rgba(255,253,249,.8)",
        },
        transition={"duration": 450, "easing": "cubic-in-out"},
    )
    fig.update_xaxes(showgrid=False, linecolor="#E5DED4", tickfont={"color": "#66788A"})
    fig.update_yaxes(gridcolor="#EFE7DC", linecolor="#E5DED4", tickfont={"color": "#66788A"})
    return fig


def attrition_distribution(df):
    counts = df["Attrition"].value_counts().rename_axis("Attrition").reset_index(name="Employees")
    fig = px.pie(
        counts,
        names="Attrition",
        values="Employees",
        hole=0.64,
        color="Attrition",
        color_discrete_map={"No": GREEN, "Yes": RED},
    )
    fig.update_traces(textposition="inside", textinfo="percent+label", hovertemplate="%{label}: %{value}<extra></extra>")
    fig.update_layout(title="Workforce Distribution by Attrition Outcome")
    return enterprise_layout(fig, 390)


def department_risk(df):
    data = (
        df.assign(AttritionFlag=(df["Attrition"] == "Yes").astype(int))
        .groupby("Department", as_index=False)
        .agg(AttritionRate=("AttritionFlag", "mean"), Employees=("AttritionFlag", "size"))
        .sort_values("AttritionRate", ascending=False)
    )
    fig = px.bar(
        data,
        x="Department",
        y="AttritionRate",
        color="AttritionRate",
        text=data["AttritionRate"].map(lambda value: f"{value * 100:.1f}%"),
        color_continuous_scale=[[0, GREEN], [0.55, AMBER], [1, RED]],
        hover_data={"Employees": True, "AttritionRate": ":.1%"},
    )
    fig.update_traces(textposition="outside", hovertemplate="%{x}<br>Risk: %{y:.1%}<br>Employees: %{customdata[0]}<extra></extra>")
    fig.update_layout(title="Department-wise Attrition Risk", coloraxis_showscale=False)
    fig.update_yaxes(tickformat=".0%")
    return enterprise_layout(fig)


def role_breakdown(df):
    data = (
        df.groupby(["JobRole", "Attrition"], as_index=False)
        .size()
        .rename(columns={"size": "Employees"})
    )
    fig = px.bar(
        data,
        y="JobRole",
        x="Employees",
        color="Attrition",
        orientation="h",
        color_discrete_map={"No": GREEN, "Yes": RED},
        hover_data={"Employees": True},
    )
    fig.update_layout(title="Job Role Breakdown", yaxis={"categoryorder": "total ascending"})
    return enterprise_layout(fig, 560)


def income_distribution(df):
    fig = px.box(
        df,
        x="Attrition",
        y="MonthlyIncome",
        color="Attrition",
        points="outliers",
        color_discrete_map={"No": GREEN, "Yes": RED},
    )
    fig.update_layout(title="Monthly Income by Attrition Outcome")
    return enterprise_layout(fig)


def age_distribution(df):
    fig = px.histogram(
        df,
        x="Age",
        color="Attrition",
        nbins=24,
        marginal="box",
        color_discrete_map={"No": GREEN, "Yes": RED},
        opacity=0.82,
    )
    fig.update_layout(title="Age Distribution and Attrition Mix", bargap=0.05)
    return enterprise_layout(fig)


def tenure_risk(df):
    data = (
        df.assign(AttritionFlag=(df["Attrition"] == "Yes").astype(int))
        .groupby("YearsAtCompany", as_index=False)
        .agg(AttritionRate=("AttritionFlag", "mean"), Employees=("AttritionFlag", "size"))
    )
    fig = px.line(
        data,
        x="YearsAtCompany",
        y="AttritionRate",
        markers=True,
        hover_data={"Employees": True, "AttritionRate": ":.1%"},
    )
    fig.update_traces(line={"color": ORANGE, "width": 3}, marker={"size": 8, "color": GOLD})
    fig.update_layout(title="Tenure Risk Profile")
    fig.update_yaxes(tickformat=".0%")
    return enterprise_layout(fig)


def overtime_impact(df):
    data = (
        df.assign(AttritionFlag=(df["Attrition"] == "Yes").astype(int))
        .groupby("OverTime", as_index=False)
        .agg(AttritionRate=("AttritionFlag", "mean"), Employees=("AttritionFlag", "size"))
    )
    fig = px.bar(
        data,
        x="OverTime",
        y="AttritionRate",
        text=data["AttritionRate"].map(lambda value: f"{value * 100:.1f}%"),
        color="OverTime",
        color_discrete_sequence=[GREEN, RED],
        hover_data={"Employees": True, "AttritionRate": ":.1%"},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(title="Overtime Impact", showlegend=False)
    fig.update_yaxes(tickformat=".0%")
    return enterprise_layout(fig, 380)


def correlation_heatmap(df):
    numeric = df.select_dtypes(include=["int64", "float64"])
    corr = numeric.corr()
    fig = px.imshow(
        corr,
        color_continuous_scale=[[0, "#315B7C"], [0.5, "#FAF8F5"], [1, ORANGE]],
        zmin=-1,
        zmax=1,
        aspect="auto",
    )
    fig.update_layout(title="Workforce Correlation Heatmap")
    return enterprise_layout(fig, 620)


def feature_importance(importance):
    data = importance.head(15).sort_values("Importance")
    fig = px.bar(
        data,
        x="Importance",
        y="Feature",
        orientation="h",
        color="Importance",
        color_continuous_scale=[[0, "#F5E6C8"], [1, ORANGE]],
    )
    fig.update_layout(title="Top Attrition Risk Drivers", coloraxis_showscale=False)
    return enterprise_layout(fig, 540)


def model_comparison(comparison):
    long_data = comparison.melt(id_vars="Model", var_name="Metric", value_name="Score")
    fig = px.bar(
        long_data,
        x="Model",
        y="Score",
        color="Metric",
        barmode="group",
        color_discrete_sequence=[NAVY, GREEN, GOLD, RED],
    )
    fig.update_layout(title="Model Benchmark Performance")
    fig.update_yaxes(range=[0, 1])
    return enterprise_layout(fig)


def risk_gauge(probability, threshold):
    color = RED if probability >= 0.5 else AMBER if probability >= threshold else GREEN
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            number={"suffix": "%", "font": {"size": 44, "color": NAVY}},
            title={"text": "Attrition Risk Score", "font": {"size": 18, "color": NAVY}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#66788A"},
                "bar": {"color": color, "thickness": 0.28},
                "bgcolor": "#FBF7EF",
                "borderwidth": 1,
                "bordercolor": "#E5DED4",
                "steps": [
                    {"range": [0, threshold * 100], "color": "rgba(14,143,90,.13)"},
                    {"range": [threshold * 100, 50], "color": "rgba(183,121,31,.15)"},
                    {"range": [50, 100], "color": "rgba(184,50,50,.14)"},
                ],
                "threshold": {
                    "line": {"color": NAVY, "width": 3},
                    "thickness": 0.75,
                    "value": threshold * 100,
                },
            },
        )
    )
    return enterprise_layout(fig, 360)


def confidence_meter(confidence):
    fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=confidence * 100,
            number={"suffix": "%", "font": {"size": 46, "color": NAVY}},
            delta={"reference": 75, "relative": False, "valueformat": ".1f"},
            title={"text": "Assessment Confidence", "font": {"size": 18, "color": NAVY}},
        )
    )
    return enterprise_layout(fig, 250)


def salary_band_analysis(df):
    bins = pd.cut(
        df["MonthlyIncome"],
        bins=[0, 3000, 6000, 9000, 13000, 20000],
        labels=["<3K", "3K-6K", "6K-9K", "9K-13K", "13K+"],
        include_lowest=True,
    )
    data = (
        df.assign(SalaryBand=bins, AttritionFlag=(df["Attrition"] == "Yes").astype(int))
        .groupby("SalaryBand", observed=False, as_index=False)
        .agg(AttritionRate=("AttritionFlag", "mean"), Employees=("AttritionFlag", "size"))
    )
    fig = px.bar(
        data,
        x="SalaryBand",
        y="AttritionRate",
        color="AttritionRate",
        text=data["AttritionRate"].map(lambda value: f"{value * 100:.1f}%"),
        color_continuous_scale=[[0, GREEN], [0.55, AMBER], [1, RED]],
        hover_data={"Employees": True},
    )
    fig.update_traces(textposition="outside")
    fig.update_yaxes(tickformat=".0%")
    fig.update_layout(title="Salary Band Analysis", coloraxis_showscale=False)
    return enterprise_layout(fig, 390)
