from datetime import datetime

import streamlit as st


def apply_css(css):
    st.markdown(css, unsafe_allow_html=True)


def loading_sequence():
    if st.session_state.get("platform_loaded"):
        return
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(
            """
            <div class="empty-card">
                <div>
                    <div class="empty-visual">HR</div>
                    <h2>Initializing Workforce Intelligence</h2>
                    <p>Loading prediction models, workforce metrics, and feature analytics.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        progress = st.progress(0, text="Preparing enterprise analytics workspace...")
        for value, text in [
            (25, "Loading prediction models..."),
            (55, "Preparing workforce intelligence..."),
            (78, "Loading feature analytics..."),
            (100, "Ready for decision support."),
        ]:
            progress.progress(value, text=text)
    placeholder.empty()
    st.session_state["platform_loaded"] = True


def topbar(model_name, threshold):
    current_date = datetime.now().strftime("%d %b %Y")
    st.markdown(
        f"""
        <div class="topbar">
            <div class="brand">
                <div class="brand-mark">HR</div>
                <div>
                    <div class="brand-title">Workforce Intelligence Console</div>
                    <div class="brand-subtitle">Attrition risk monitoring and people analytics</div>
                </div>
            </div>
            <div class="status-row">
                <span class="status-pill">{current_date}</span>
                <span class="status-pill status-live">System Online</span>
                <span class="status-pill">{model_name}</span>
                <span class="status-pill">Threshold {threshold:.2f}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title, subtitle, eyebrow="Executive Workforce Analytics", actions=None):
    actions = actions or ["Review workforce risk", "Generate assessment", "Monitor model performance"]
    chips = "".join([f"<span class='action-chip'>{item}</span>" for item in actions])
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
            <div class="action-row">{chips}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title, subtitle="", eyebrow=""):
    eyebrow_markup = f"<div class='eyebrow'>{eyebrow}</div>" if eyebrow else ""
    st.markdown(
        f"""
        <div class="section-title">
            {eyebrow_markup}
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label, value, subtitle, icon="HR", trend="Active"):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-trend">{trend}</div>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def content_card(title, body):
    st.markdown(
        f"""
        <div class="content-card">
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_assessment():
    st.markdown(
        """
        <div class="empty-card">
            <div>
                <div class="empty-visual">RA</div>
                <h2>Ready to Analyze Employee Risk</h2>
                <p>Complete the employee profile in the sidebar and generate an attrition risk assessment.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def risk_category(probability):
    if probability >= 0.5:
        return "High Attrition Risk", "risk-high", "#B83232", "Critical retention review"
    if probability >= 0.25:
        return "Elevated Attrition Risk", "risk-medium", "#B7791F", "Targeted retention review"
    return "Low Attrition Risk", "risk-low", "#0E8F5A", "Standard engagement monitoring"


def risk_summary(probability, confidence, threshold):
    label, css_class, color, priority = risk_category(probability)
    recommendation = (
        "Review engagement, compensation, tenure, workload, and manager support signals in line with retention policy."
        if probability >= threshold
        else "Maintain standard engagement monitoring and include the profile in routine workforce planning reviews."
    )
    st.markdown(
        f"""
        <div class="risk-card">
            <span class="risk-badge {css_class}">{label.upper()}</span>
            <div class="risk-score">{probability * 100:.1f}%</div>
            <p>Attrition risk probability</p>
            <div class="progress-track">
                <div class="progress-fill" style="width: {probability * 100:.1f}%; background: {color};"></div>
            </div>
            <div class="priority-grid">
                <div class="mini-panel">
                    <div class="mini-label">Assessment Confidence</div>
                    <div class="mini-value">{confidence * 100:.1f}%</div>
                </div>
                <div class="mini-panel">
                    <div class="mini-label">Retention Priority</div>
                    <div class="mini-value">{priority}</div>
                </div>
                <div class="mini-panel">
                    <div class="mini-label">Risk Threshold</div>
                    <div class="mini-value">{threshold:.2f}</div>
                </div>
                <div class="mini-panel">
                    <div class="mini-label">Recommended HR Action</div>
                    <div class="mini-value">Policy-led review</div>
                </div>
            </div>
            <p style="margin-top: 1rem;"><strong>Business recommendation:</strong> {recommendation}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer(model_name, threshold):
    st.markdown(
        f"""
        <div class="footer">
            <span>Employee Attrition Intelligence | Version 2.0</span>
            <span>Model: {model_name} | Threshold: {threshold:.2f}</span>
            <span>Last updated: {datetime.now().strftime("%d %b %Y")}</span>
            <span>Confidential workforce data. Authorized HR use only.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
