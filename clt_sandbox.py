import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.stats as stats

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CLT Sandbox | INE 311",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0a0c12; color: #c9d1e0; }

[data-testid="stSidebar"] {
    background: #0f1219 !important;
    border-right: 1px solid #1e2535;
}

/* Sidebar labels */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p {
    color: #7a8ba0 !important;
    font-size: 0.8rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* Selectbox */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #161b27 !important;
    border: 1px solid #2a3448 !important;
    border-radius: 6px !important;
    color: #e2e8f0 !important;
}

/* Slider track */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: #3b82f6 !important;
}

/* Headers */
h1 { font-size: 1.5rem !important; font-weight: 700 !important; color: #f1f5f9 !important; letter-spacing: -0.02em; }
h2 { font-size: 1.05rem !important; font-weight: 600 !important; color: #94a3b8 !important; text-transform: uppercase; letter-spacing: 0.08em; }
h3 { font-size: 0.9rem !important; font-weight: 500 !important; color: #64748b !important; }

/* Metric cards */
[data-testid="stMetric"] {
    background: #111827;
    border: 1px solid #1e2d3d;
    border-top: 2px solid #3b82f6;
    border-radius: 8px;
    padding: 1.1rem 1.3rem !important;
}
[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
[data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.9rem !important;
    font-weight: 600 !important;
}

/* Info box */
.stAlert {
    background: #0f1a2e !important;
    border: 1px solid #1e3a5f !important;
    border-left: 3px solid #3b82f6 !important;
    border-radius: 6px !important;
    color: #93c5fd !important;
}

/* Divider */
hr { border-color: #1e2535 !important; margin: 1.2rem 0 !important; }

/* Sidebar title block */
.sidebar-header {
    padding: 0.6rem 0 1rem 0;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #1e2535;
}
.sidebar-header .title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.95rem;
    font-weight: 600;
    color: #3b82f6;
    letter-spacing: 0.04em;
}
.sidebar-header .subtitle {
    font-size: 0.72rem;
    color: #475569;
    margin-top: 2px;
}

/* Distribution badge */
.dist-badge {
    display: inline-block;
    background: #1e3a5f;
    color: #60a5fa;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 4px;
    letter-spacing: 0.06em;
    margin-bottom: 0.5rem;
}

/* Explanation card */
.explanation-card {
    background: #0f1219;
    border: 1px solid #1e2535;
    border-left: 3px solid #10b981;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    margin-top: 0.5rem;
    line-height: 1.7;
    color: #94a3b8;
    font-size: 0.88rem;
}
.explanation-card strong { color: #e2e8f0; }

/* Normal test card */
.normality-card {
    background: #0f1219;
    border: 1px solid #1e2535;
    border-radius: 8px;
    padding: 1rem 1.3rem;
    font-size: 0.82rem;
    color: #94a3b8;
}
.normality-card .stat-row {
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
    border-bottom: 1px solid #1a2030;
}
.normality-card .stat-row:last-child { border-bottom: none; }
.normality-card .stat-label { color: #64748b; }
.normality-card .stat-val { font-family: 'JetBrains Mono', monospace; color: #cbd5e1; font-size: 0.8rem; }

/* Section label */
.section-label {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #3b82f6;
    margin-bottom: 0.6rem;
}

/* Theorem note */
.theorem-note {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #475569;
    background: #0d1117;
    border: 1px solid #1e2535;
    border-radius: 6px;
    padding: 0.7rem 1rem;
    margin-top: 0.8rem;
}
.theorem-note span { color: #60a5fa; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
COLORS = {
    "pop":    "#3b82f6",   # blue
    "sample": "#10b981",   # emerald
    "normal": "#f59e0b",   # amber (overlay curve)
    "grid":   "#1e2535",
    "bg":     "#0a0c12",
    "paper":  "#111827",
    "text":   "#94a3b8",
    "axis":   "#4b5563",
}

DIST_INFO = {
    "Uniform":     {"label": "UNIFORM",     "color": "#8b5cf6", "desc": "All values equally likely between a min and max — strongly non-normal."},
    "Exponential": {"label": "EXPONENTIAL", "color": "#f59e0b", "desc": "Heavy right skew — models waiting times and failure rates."},
    "Normal":      {"label": "NORMAL",      "color": "#3b82f6", "desc": "Already symmetric — confirms CLT is trivially satisfied."},
    "Beta":        {"label": "BETA",        "color": "#ec4899", "desc": "Skewed bounded distribution — useful for proportions and quality metrics."},
    "Log-Normal":  {"label": "LOG-NORMAL",  "color": "#14b8a6", "desc": "Right-skewed multiplicative process — common in manufacturing defect models."},
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="title">📊 CLT SANDBOX</div>
        <div class="subtitle">INE 311 — Quality Engineering</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Population Distribution</div>', unsafe_allow_html=True)
    dist_name = st.selectbox("", list(DIST_INFO.keys()), label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div class="section-label">Simulation Parameters</div>', unsafe_allow_html=True)

    n = st.slider("Sample Size (n)", min_value=2, max_value=200, value=30, step=1,
                  help="Number of observations per sample. Increase to see CLT convergence.")
    num_samples = st.slider("Number of Samples", min_value=100, max_value=5000, value=1000, step=100,
                            help="How many samples to draw from the population.")
    pop_size = 100_000

    st.markdown("---")
    run = st.button("▶  RUN SIMULATION", use_container_width=True)

    info = DIST_INFO[dist_name]
    st.markdown(f"""
    <div style="margin-top:1rem; padding:0.9rem; background:#0d1117; border:1px solid #1e2535; border-radius:6px; font-size:0.78rem; color:#64748b; line-height:1.6;">
        <span style="color:{info['color']}; font-weight:600;">{info['label']}</span><br>{info['desc']}
    </div>
    """, unsafe_allow_html=True)

# ── Data generation ───────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def generate_data(dist_name, n, num_samples, pop_size):
    rng = np.random.default_rng(42)
    if dist_name == "Uniform":
        population = rng.uniform(0, 100, pop_size)
    elif dist_name == "Exponential":
        population = rng.exponential(scale=20, size=pop_size)
    elif dist_name == "Normal":
        population = rng.normal(loc=50, scale=10, size=pop_size)
    elif dist_name == "Beta":
        population = rng.beta(2, 6, pop_size) * 100
    elif dist_name == "Log-Normal":
        population = rng.lognormal(mean=3.5, sigma=0.5, size=pop_size)
    sample_means = np.array([rng.choice(population, size=n, replace=False).mean() for _ in range(num_samples)])
    return population, sample_means

# ── Run simulation ────────────────────────────────────────────────────────────
if "population" not in st.session_state or run:
    with st.spinner("Running simulation…"):
        pop, smeans = generate_data(dist_name, n, num_samples, pop_size)
        st.session_state["population"]   = pop
        st.session_state["sample_means"] = smeans
        st.session_state["dist_name"]    = dist_name
        st.session_state["n"]            = n
        st.session_state["num_samples"]  = num_samples

pop    = st.session_state["population"]
smeans = st.session_state["sample_means"]
dn     = st.session_state["dist_name"]
sn     = st.session_state["n"]
snum   = st.session_state["num_samples"]

# ── Stats ─────────────────────────────────────────────────────────────────────
pop_mean  = pop.mean()
pop_std   = pop.std()
sm_mean   = smeans.mean()
sm_std    = smeans.std()
theo_se   = pop_std / np.sqrt(sn)
_, p_norm = stats.shapiro(smeans[:500])  # limit to 500 for Shapiro

# ── Header ────────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown(f"## Central Limit Theorem Sandbox")
    st.markdown(f'<div class="dist-badge">{DIST_INFO[dn]["label"]} · n = {sn} · {snum:,} samples</div>', unsafe_allow_html=True)
with col_h2:
    st.markdown("<br>", unsafe_allow_html=True)
    convergence_pct = min(100, int((1 - abs(sm_std - theo_se) / (theo_se + 1e-9)) * 100))

st.markdown("---")

# ── Metrics ───────────────────────────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Population Mean (μ)",       f"{pop_mean:.3f}")
m2.metric("Mean of Sample Means",      f"{sm_mean:.3f}")
m3.metric("Population Std Dev (σ)",    f"{pop_std:.3f}")
m4.metric("Std Error — Observed",      f"{sm_std:.3f}")
m5.metric("Std Error — Theoretical (σ/√n)", f"{theo_se:.3f}")

st.markdown("---")

# ── Charts ────────────────────────────────────────────────────────────────────
def make_hist(x, title, xlabel, color, show_normal=False, normal_params=None):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=x,
        nbinsx=60,
        marker_color=color,
        marker_line_color="#0a0c12",
        marker_line_width=0.4,
        opacity=0.85,
        name=xlabel,
    ))
    if show_normal and normal_params:
        mu_n, sigma_n = normal_params
        x_range = np.linspace(mu_n - 4 * sigma_n, mu_n + 4 * sigma_n, 300)
        # scale to histogram
        bin_width = (x.max() - x.min()) / 60
        scale = len(x) * bin_width
        y_norm = stats.norm.pdf(x_range, mu_n, sigma_n) * scale
        fig.add_trace(go.Scatter(
            x=x_range, y=y_norm,
            mode="lines",
            line=dict(color=COLORS["normal"], width=2.5),
            name="Normal fit",
        ))
    fig.update_layout(
        title=dict(text=title, font=dict(family="Inter", size=13, color="#e2e8f0"), x=0, xanchor="left"),
        paper_bgcolor=COLORS["paper"],
        plot_bgcolor="#0d1117",
        font=dict(family="Inter", color=COLORS["text"], size=11),
        margin=dict(l=40, r=20, t=45, b=40),
        showlegend=show_normal,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    bgcolor="rgba(0,0,0,0)", font=dict(size=10, color="#94a3b8")),
        xaxis=dict(
            title=dict(text=xlabel, font=dict(size=11, color="#64748b")),
            gridcolor=COLORS["grid"], gridwidth=1,
            linecolor=COLORS["axis"], tickcolor=COLORS["axis"],
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            title=dict(text="Frequency", font=dict(size=11, color="#64748b")),
            gridcolor=COLORS["grid"], gridwidth=1,
            linecolor=COLORS["axis"], tickcolor=COLORS["axis"],
            tickfont=dict(size=10),
        ),
        bargap=0.03,
    )
    return fig

ch1, ch2 = st.columns(2)

with ch1:
    fig_pop = make_hist(pop, "Original Population Distribution", "Value",
                        DIST_INFO[dn]["color"])
    st.plotly_chart(fig_pop, use_container_width=True, config={"displayModeBar": False})

with ch2:
    fig_sm = make_hist(smeans, "Distribution of Sample Means", "Sample Mean",
                       COLORS["sample"], show_normal=True, normal_params=(sm_mean, sm_std))
    st.plotly_chart(fig_sm, use_container_width=True, config={"displayModeBar": False})

# ── QQ Plot ───────────────────────────────────────────────────────────────────
with st.expander("🔍  Q-Q Plot — Normality Check of Sample Means", expanded=False):
    (osm, osr), (slope, intercept, _) = stats.probplot(smeans)
    qq_line_x = np.array([osm.min(), osm.max()])
    qq_line_y = slope * qq_line_x + intercept

    fig_qq = go.Figure()
    fig_qq.add_trace(go.Scatter(
        x=osm, y=osr,
        mode="markers",
        marker=dict(color=COLORS["sample"], size=4, opacity=0.6),
        name="Sample quantiles",
    ))
    fig_qq.add_trace(go.Scatter(
        x=qq_line_x, y=qq_line_y,
        mode="lines",
        line=dict(color=COLORS["normal"], width=2, dash="dash"),
        name="Reference line",
    ))
    fig_qq.update_layout(
        title=dict(text="Normal Q-Q Plot of Sample Means", font=dict(size=13, color="#e2e8f0")),
        paper_bgcolor=COLORS["paper"],
        plot_bgcolor="#0d1117",
        font=dict(family="Inter", color=COLORS["text"], size=11),
        margin=dict(l=50, r=20, t=45, b=40),
        xaxis=dict(title="Theoretical Quantiles", gridcolor=COLORS["grid"], linecolor=COLORS["axis"]),
        yaxis=dict(title="Sample Quantiles",       gridcolor=COLORS["grid"], linecolor=COLORS["axis"]),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color="#94a3b8")),
        height=350,
    )
    st.plotly_chart(fig_qq, use_container_width=True, config={"displayModeBar": False})

    ncol1, ncol2 = st.columns(2)
    with ncol1:
        norm_status = "✅ Normally Distributed" if p_norm > 0.05 else "⚠️ Departure from Normality"
        st.markdown(f"""
        <div class="normality-card">
            <div class="stat-row"><span class="stat-label">Shapiro-Wilk p-value</span><span class="stat-val">{p_norm:.4f}</span></div>
            <div class="stat-row"><span class="stat-label">Significance (α = 0.05)</span><span class="stat-val">{'p > 0.05 → Normal' if p_norm > 0.05 else 'p ≤ 0.05 → Non-normal'}</span></div>
            <div class="stat-row"><span class="stat-label">Verdict</span><span class="stat-val">{norm_status}</span></div>
        </div>
        """, unsafe_allow_html=True)

# ── Explanation ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## Explanation")

skewness = float(abs(smeans.mean() - np.median(smeans)) / (smeans.std() + 1e-9))

if sn < 10:
    convergence_msg = f"With <strong>n = {sn}</strong>, the sample size is still small — the distribution of sample means may not yet appear fully normal."
elif sn < 30:
    convergence_msg = f"With <strong>n = {sn}</strong>, the distribution of sample means is beginning to converge toward normality as predicted by the CLT."
else:
    convergence_msg = f"With <strong>n = {sn}</strong>, the distribution of sample means is approximately normal — the Central Limit Theorem is clearly in effect."

st.markdown(f"""
<div class="explanation-card">
    <strong>Central Limit Theorem (CLT):</strong> As the sample size <em>n</em> increases,
    the distribution of the <em>sample mean</em> approaches a normal distribution regardless
    of the shape of the underlying population, provided the population has a finite mean and variance.<br><br>
    {convergence_msg}<br><br>
    The <strong>theoretical standard error</strong> is σ/√n = {pop_std:.3f}/√{sn} = <strong>{theo_se:.3f}</strong>.
    The observed standard deviation of sample means is <strong>{sm_std:.3f}</strong> — 
    {"closely matching theory ✅" if abs(sm_std - theo_se) / (theo_se + 1e-9) < 0.05 else "slightly deviating due to sampling variability."}
    <br><br>
    <strong>Relevance to Quality Engineering:</strong> The CLT justifies using X̄ control charts
    even when individual measurements are non-normal. It underpins hypothesis testing, confidence
    intervals, and process capability analyses used throughout quality engineering practice.
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="theorem-note">
    <span>CLT Statement:</span>  X̄ ~ N(μ, σ²/n)  as  n → ∞  &nbsp;|&nbsp;
    μ = {pop_mean:.3f} &nbsp;|&nbsp; σ = {pop_std:.3f} &nbsp;|&nbsp;
    σ/√n = {theo_se:.3f} &nbsp;|&nbsp; n = {sn}
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="text-align:center; font-size:0.72rem; color:#334155; letter-spacing:0.08em;">'
    'INE 311 — Quality Engineering · Central Limit Theorem Sandbox · Built with Python & Streamlit'
    '</p>',
    unsafe_allow_html=True
)
