APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #102A43;
    --navy-2: #243B53;
    --ink: #1F2933;
    --muted: #66788A;
    --warm-white: #FAF8F5;
    --beige: #F5F1EA;
    --card: #FFFDF9;
    --line: #E5DED4;
    --gold: #D4A017;
    --orange: #E67E22;
    --green: #0E8F5A;
    --amber: #B7791F;
    --red: #B83232;
    --shadow: 0 18px 45px rgba(16, 42, 67, 0.08);
}

html, body, [class*="css"] {
    font-family: 'Inter', 'IBM Plex Sans', 'Segoe UI', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(212, 160, 23, 0.12), transparent 34rem),
        linear-gradient(180deg, var(--warm-white) 0%, #F7F3EC 100%);
    color: var(--ink);
}

.main .block-container {
    padding: 1.1rem 2.1rem 2rem;
    max-width: 1480px;
}

h1, h2, h3, h4 {
    color: var(--navy);
    letter-spacing: 0;
}

h1 { font-size: 2.35rem !important; font-weight: 800 !important; }
h2 { font-size: 1.35rem !important; font-weight: 760 !important; }
h3 { font-size: 1.05rem !important; font-weight: 720 !important; }

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102A43 0%, #1D3D5C 100%);
}

div[data-testid="stSidebar"] * {
    color: #F8F4EA !important;
}

div[data-testid="stSidebar"] .stRadio label {
    color: #F8F4EA !important;
}

div[data-testid="stSidebar"] [role="radiogroup"] label {
    border-radius: 12px;
    padding: .42rem .5rem;
}

div[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(250, 248, 245, 0.10);
}

div[data-testid="stSidebar"] details {
    border: 1px solid rgba(250, 248, 245, 0.16);
    border-radius: 14px;
    padding: .2rem .35rem;
    background: rgba(250, 248, 245, 0.06);
    margin-bottom: .7rem;
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: .9rem 1.05rem;
    border: 1px solid var(--line);
    border-radius: 18px;
    background: rgba(255, 253, 249, 0.86);
    box-shadow: var(--shadow);
    margin-bottom: 1.2rem;
    backdrop-filter: blur(12px);
}

.brand {
    display: flex;
    align-items: center;
    gap: .8rem;
}

.brand-mark {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    background: linear-gradient(135deg, var(--navy), #315B7C);
    color: #FAF8F5;
    display: grid;
    place-items: center;
    font-weight: 800;
    box-shadow: 0 10px 22px rgba(16, 42, 67, .22);
}

.brand-title {
    color: var(--navy);
    font-weight: 800;
    font-size: 1.05rem;
}

.brand-subtitle {
    color: var(--muted);
    font-size: .82rem;
    margin-top: .05rem;
}

.status-row {
    display: flex;
    align-items: center;
    gap: .65rem;
    flex-wrap: wrap;
    justify-content: flex-end;
}

.status-pill {
    border: 1px solid var(--line);
    background: var(--beige);
    color: var(--navy);
    padding: .45rem .68rem;
    border-radius: 999px;
    font-size: .8rem;
    font-weight: 650;
}

.status-live {
    background: rgba(14, 143, 90, .10);
    color: var(--green);
    border-color: rgba(14, 143, 90, .28);
}

.hero-card {
    position: relative;
    border-radius: 24px;
    background: linear-gradient(135deg, #102A43 0%, #1E486A 58%, #E67E22 145%);
    color: #FAF8F5;
    padding: 2rem;
    margin-bottom: 1.2rem;
    overflow: hidden;
    box-shadow: 0 24px 65px rgba(16, 42, 67, .18);
    animation: fadeUp .52s ease both;
}

.hero-card:after {
    content: "";
    position: absolute;
    width: 420px;
    height: 420px;
    border: 1px solid rgba(250, 248, 245, .16);
    border-radius: 999px;
    right: -160px;
    top: -170px;
}

.hero-eyebrow {
    color: #F3DCA3;
    font-size: .78rem;
    letter-spacing: .08em;
    text-transform: uppercase;
    font-weight: 800;
    margin-bottom: .6rem;
}

.hero-card h1 {
    color: #FAF8F5 !important;
    font-size: 2.65rem !important;
    line-height: 1.05;
    max-width: 860px;
    margin: 0;
}

.hero-card p {
    color: rgba(250, 248, 245, .82);
    max-width: 850px;
    font-size: 1.02rem;
    margin: .8rem 0 1.2rem;
}

.action-row {
    display: flex;
    gap: .7rem;
    flex-wrap: wrap;
}

.action-chip {
    background: rgba(250, 248, 245, .12);
    border: 1px solid rgba(250, 248, 245, .2);
    color: #FAF8F5;
    border-radius: 999px;
    padding: .56rem .82rem;
    font-weight: 700;
    font-size: .86rem;
}

.section-title {
    margin: 1.4rem 0 .85rem;
}

.section-title .eyebrow {
    color: var(--orange);
    font-size: .76rem;
    letter-spacing: .08em;
    text-transform: uppercase;
    font-weight: 800;
}

.section-title h2 {
    margin: .15rem 0 .1rem;
}

.section-title p {
    margin: 0;
    color: var(--muted);
    font-size: .94rem;
}

.kpi-card, .content-card, .risk-card, .empty-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 20px;
    box-shadow: var(--shadow);
    padding: 1.05rem;
    animation: fadeUp .5s ease both;
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}

.kpi-card:hover, .content-card:hover, .risk-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 22px 56px rgba(16, 42, 67, 0.12);
    border-color: rgba(212, 160, 23, .42);
}

.kpi-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: .8rem;
}

.kpi-icon {
    width: 38px;
    height: 38px;
    border-radius: 12px;
    display: grid;
    place-items: center;
    background: #F5E9D5;
    color: var(--navy);
    font-weight: 800;
    font-size: .78rem;
}

.kpi-trend {
    color: var(--green);
    background: rgba(14, 143, 90, .09);
    border: 1px solid rgba(14, 143, 90, .20);
    border-radius: 999px;
    padding: .22rem .48rem;
    font-size: .72rem;
    font-weight: 760;
}

.kpi-value {
    color: var(--navy);
    font-size: 1.8rem;
    font-weight: 820;
    margin-top: .75rem;
}

.kpi-label {
    color: var(--muted);
    font-size: .84rem;
    font-weight: 650;
    margin-top: .12rem;
}

.kpi-subtitle {
    color: #7D8A97;
    font-size: .78rem;
    margin-top: .5rem;
}

.content-card h3, .risk-card h3 {
    margin-top: 0;
    margin-bottom: .35rem;
}

.content-card p, .risk-card p {
    color: var(--muted);
    line-height: 1.55;
}

.risk-card {
    padding: 1.3rem;
}

.risk-badge {
    display: inline-flex;
    align-items: center;
    border-radius: 999px;
    padding: .5rem .75rem;
    font-size: .8rem;
    font-weight: 850;
    letter-spacing: .04em;
}

.risk-low {
    background: rgba(14, 143, 90, .11);
    color: var(--green);
    border: 1px solid rgba(14, 143, 90, .22);
}

.risk-medium {
    background: rgba(183, 121, 31, .12);
    color: var(--amber);
    border: 1px solid rgba(183, 121, 31, .24);
}

.risk-high {
    background: rgba(184, 50, 50, .11);
    color: var(--red);
    border: 1px solid rgba(184, 50, 50, .23);
}

.risk-score {
    font-size: 3.15rem;
    line-height: 1;
    color: var(--navy);
    font-weight: 850;
    margin: .85rem 0 .25rem;
}

.progress-track {
    width: 100%;
    height: 12px;
    background: #EEE4D7;
    border-radius: 999px;
    overflow: hidden;
    margin: .9rem 0 .35rem;
}

.progress-fill {
    height: 100%;
    border-radius: 999px;
    animation: growBar .75s ease both;
}

.priority-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: .75rem;
    margin-top: 1rem;
}

.mini-panel {
    border: 1px solid var(--line);
    background: #FBF7EF;
    border-radius: 16px;
    padding: .82rem;
}

.mini-label {
    color: var(--muted);
    font-size: .77rem;
    font-weight: 700;
}

.mini-value {
    color: var(--navy);
    font-size: 1.12rem;
    font-weight: 800;
    margin-top: .25rem;
}

.empty-card {
    min-height: 345px;
    display: grid;
    place-items: center;
    text-align: center;
    background:
        linear-gradient(135deg, rgba(250, 248, 245, .96), rgba(245, 241, 234, .96));
}

.empty-visual {
    width: 120px;
    height: 120px;
    border-radius: 34px;
    background: linear-gradient(135deg, rgba(212,160,23,.16), rgba(230,126,34,.12));
    border: 1px solid rgba(212,160,23,.28);
    display: grid;
    place-items: center;
    margin: 0 auto 1rem;
    color: var(--navy);
    font-size: 2rem;
    font-weight: 850;
}

.footer {
    display: flex;
    justify-content: space-between;
    gap: .8rem;
    flex-wrap: wrap;
    border-top: 1px solid var(--line);
    color: var(--muted);
    margin-top: 2rem;
    padding: 1rem .2rem 0;
    font-size: .82rem;
}

.stButton > button {
    background: linear-gradient(135deg, var(--navy), #254D70) !important;
    color: #FAF8F5 !important;
    border: 1px solid rgba(16, 42, 67, .18) !important;
    border-radius: 14px !important;
    min-height: 3rem;
    font-weight: 800 !important;
    box-shadow: 0 14px 30px rgba(16, 42, 67, .18);
    transition: transform .16s ease, box-shadow .16s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 38px rgba(16, 42, 67, .22);
}

div[data-testid="stMetric"] {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: .85rem;
    box-shadow: var(--shadow);
}

.stTabs [data-baseweb="tab-list"] {
    gap: .35rem;
}

.stTabs [data-baseweb="tab"] {
    background: #FBF7EF;
    border: 1px solid var(--line);
    border-radius: 999px;
    padding: .55rem .95rem;
}

.stDataFrame {
    border: 1px solid var(--line);
    border-radius: 18px;
    overflow: hidden;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes growBar {
    from { width: 0; }
}

@media (max-width: 900px) {
    .main .block-container { padding: .9rem 1rem 1.5rem; }
    .topbar { align-items: flex-start; flex-direction: column; }
    .hero-card { padding: 1.4rem; }
    .hero-card h1 { font-size: 2rem !important; }
    .priority-grid { grid-template-columns: 1fr; }
}
</style>
"""
