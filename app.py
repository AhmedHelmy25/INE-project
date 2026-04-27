import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
import io

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Packing Line QC Portal",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Syne:wght@700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #0a0e1a;
    color: #e2e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1220 0%, #0a0e1a 100%);
    border-right: 1px solid rgba(99,179,237,0.15);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #63b3ed;
    font-family: 'Syne', sans-serif;
}

/* ── Main area background ── */
.main .block-container {
    background: #0a0e1a;
    padding-top: 2rem;
}

/* ── Tab bar ── */
[data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(99,179,237,0.2) !important;
    gap: 0 !important;
}
[data-baseweb="tab"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #718096 !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.7rem 1.2rem !important;
    background: transparent !important;
    transition: all 0.2s ease !important;
}
[data-baseweb="tab"]:hover {
    color: #63b3ed !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    color: #63b3ed !important;
    border-bottom: 2px solid #63b3ed !important;
    background: transparent !important;
}
[data-baseweb="tab-highlight"] { display: none !important; }
[data-baseweb="tab-border"] { display: none !important; }

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(135deg, #111827 0%, #1a2035 100%);
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: rgba(99,179,237,0.4); }
.metric-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #718096;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #e2e8f0;
    line-height: 1;
}
.metric-unit {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #63b3ed;
    margin-top: 0.2rem;
}

/* ── Status banners ── */
.status-ok    { background: rgba(72,187,120,0.12); border: 1px solid rgba(72,187,120,0.35); border-radius:10px; padding:1rem 1.4rem; color:#68d391; }
.status-warn  { background: rgba(246,173,85,0.10); border: 1px solid rgba(246,173,85,0.35); border-radius:10px; padding:1rem 1.4rem; color:#f6ad55; }
.status-bad   { background: rgba(252,129,129,0.10); border: 1px solid rgba(252,129,129,0.35); border-radius:10px; padding:1rem 1.4rem; color:#fc8181; }

/* ── Section headings ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #e2e8f0;
    margin-bottom: 0.2rem;
}
.section-sub {
    font-size: 0.82rem;
    color: #718096;
    margin-bottom: 1.6rem;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0d1220 0%, #111827 40%, #0d1a2e 100%);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 16px;
    padding: 2.5rem 2.8rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,179,237,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #e2e8f0;
    line-height: 1.1;
    margin-bottom: 0.6rem;
}
.hero-sub {
    font-size: 0.95rem;
    color: #718096;
    max-width: 520px;
    line-height: 1.6;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,179,237,0.12);
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #63b3ed;
    margin-bottom: 1rem;
}

/* ── Feature grid ── */
.feature-card {
    background: #111827;
    border: 1px solid rgba(99,179,237,0.12);
    border-radius: 12px;
    padding: 1.4rem;
    height: 100%;
}
.feature-icon { font-size: 1.6rem; margin-bottom: 0.6rem; }
.feature-title { font-family:'Syne',sans-serif; font-weight:800; font-size:0.95rem; color:#e2e8f0; margin-bottom:0.3rem; }
.feature-desc  { font-size:0.78rem; color:#718096; line-height:1.5; }

/* ── Table ── */
.stDataFrame { background: #111827 !important; }

/* ── Number input / slider ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: #111827 !important;
    border: 1px solid rgba(99,179,237,0.25) !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stSlider"] > div > div { background: rgba(99,179,237,0.2) !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #2b6cb0, #3182ce) !important;
    border: none !important;
    color: #fff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.6rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── Divider ── */
hr { border-color: rgba(99,179,237,0.15) !important; }

/* ── Checkbox / DMAIC ── */
[data-testid="stCheckbox"] label { color: #a0aec0 !important; font-size:0.85rem !important; }

/* ── Selectbox ── */
[data-baseweb="select"] > div {
    background: #111827 !important;
    border-color: rgba(99,179,237,0.25) !important;
    color: #e2e8f0 !important;
}

/* ── Expander ── */
details {
    background: #111827 !important;
    border: 1px solid rgba(99,179,237,0.15) !important;
    border-radius: 10px !important;
}
summary { color: #63b3ed !important; font-weight:600 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:#0a0e1a; }
::-webkit-scrollbar-thumb { background:#2d3748; border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ── Matplotlib dark theme ─────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#111827",
    "axes.facecolor":    "#0d1220",
    "axes.edgecolor":    "#2d3748",
    "axes.labelcolor":   "#a0aec0",
    "xtick.color":       "#718096",
    "ytick.color":       "#718096",
    "text.color":        "#e2e8f0",
    "grid.color":        "#1a2035",
    "grid.linestyle":    "--",
    "grid.alpha":        0.8,
    "lines.linewidth":   2,
    "font.family":       "monospace",
    "legend.facecolor":  "#111827",
    "legend.edgecolor":  "#2d3748",
    "legend.fontsize":   8,
})

ACCENT  = "#63b3ed"
GREEN   = "#68d391"
YELLOW  = "#f6ad55"
RED     = "#fc8181"
PURPLE  = "#b794f4"
ORANGE  = "#f6ad55"

# ── SPC constants (n=5) ──────────────────────────────────────────────────────
SPC = {"A2": 0.577, "D3": 0, "D4": 2.114, "d2": 2.326}

# ── Session-state seed for simulation ────────────────────────────────────────
if "sim_data" not in st.session_state:
    st.session_state.sim_data = None
if "sim_params" not in st.session_state:
    st.session_state.sim_params = {}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Packing Line QC")
    st.markdown("**INE 311 — Quality Engineering**")
    st.markdown("---")

    st.markdown("### How to use")
    st.markdown("""
1. Set parameters in **Inputs + Simulation**
2. Generate data to populate all charts
3. Explore analysis tabs
4. Use **DMAIC Tracker** for improvements
    """)

    st.markdown("---")
    st.markdown("**SPC constants (n = 5)**")
    st.markdown(f"""
<div style='font-family:JetBrains Mono,monospace; font-size:0.75rem; color:#718096; line-height:1.9'>
A₂ = {SPC['A2']}<br>
D₃ = {SPC['D3']}<br>
D₄ = {SPC['D4']}<br>
d₂ = {SPC['d2']}
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    if st.session_state.sim_data is not None:
        p = st.session_state.sim_params
        st.markdown("**Active simulation**")
        st.markdown(f"""
<div style='font-family:JetBrains Mono,monospace; font-size:0.72rem; color:#63b3ed; line-height:1.8'>
μ = {p['mean']} g &nbsp;|&nbsp; σ = {p['std']} g<br>
Target = {p['target']} g<br>
LSL = {p['lsl']} g &nbsp;|&nbsp; USL = {p['usl']} g<br>
{p['n_samples']} × {p['n_obs']} = {p['n_samples']*p['n_obs']} obs
</div>
""", unsafe_allow_html=True)
    else:
        st.caption("No simulation active. Go to Inputs tab.")

# ── Main tabs ─────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🏠  Overview",
    "⚙️  Inputs + Simulation",
    "📊  Capability Analysis",
    "📈  Control Charts",
    "🔧  Quality Tools",
    "🧪  DOE + CLT Sandbox",
    "✅  DMAIC Tracker",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 0 — Overview
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("""
<div class="hero-banner">
  <div class="hero-badge">INE 311 · Quality Engineering</div>
  <div class="hero-title">📦 Packing Line<br>Weight Monitor</div>
  <div class="hero-sub">
    A statistical quality control workspace for engineers, supervisors, and students.
    Configure your process, simulate data, and explore every layer of SPC analysis.
  </div>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    features = [
        ("📊", "Capability Analysis", "Cp, Cpk, % out-of-spec, and fitted normal distribution vs. specification limits."),
        ("📈", "Control Charts", "X̄, R, and p-charts with automatic UCL/LCL computation and out-of-control flagging."),
        ("🔍", "Quality Tools", "Pareto chart of defect categories and sample-mean drift scatter analysis."),
        ("✅", "DMAIC Tracker", "Six Sigma checklist tailored to a dry-goods packing line with progress tracking."),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
        col.markdown(f"""
<div class="feature-card">
  <div class="feature-icon">{icon}</div>
  <div class="feature-title">{title}</div>
  <div class="feature-desc">{desc}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown("#### What this portal supports")
        items = [
            ("📐 Process capability", "Cp, Cpk, percentage out of specification, and a fitted normal distribution chart with target and specification lines."),
            ("📉 Statistical control charts", "X̄ chart for sample means, R chart for sample ranges, and p-chart for defect proportions, with automatic out-of-control flagging."),
            ("🗂️ Defect monitoring", "Pareto analysis of defect categories and scatter analysis of sample-mean drift over time."),
            ("🔬 Quality improvement", "A full Design of Experiments (DOE) module, Central Limit Theorem sandbox, and a Six Sigma DMAIC checklist tailored to a packing line."),
        ]
        for icon_text, desc in items:
            st.markdown(f"""
<div style='display:flex; gap:0.8rem; margin-bottom:0.9rem; align-items:flex-start'>
  <div style='font-size:1.1rem; margin-top:0.1rem'>{icon_text.split()[0]}</div>
  <div>
    <span style='font-weight:700; color:#e2e8f0'>{" ".join(icon_text.split()[1:])}</span>
    <span style='color:#718096; font-size:0.82rem'> — {desc}</span>
  </div>
</div>
""", unsafe_allow_html=True)

    with col_b:
        st.markdown("#### Quick Start")
        st.info("Open the **Inputs + Simulation** tab to configure your process parameters, then explore the analysis tabs to see live results.")
        st.markdown("""
<div style='background:#111827; border:1px solid rgba(99,179,237,0.2); border-radius:10px; padding:1rem 1.2rem; font-size:0.8rem; color:#a0aec0; line-height:1.8'>
<b style='color:#63b3ed'>Step 1</b> — Set target weight, mean, σ, LSL, USL<br>
<b style='color:#63b3ed'>Step 2</b> — Choose subgroup size and sample count<br>
<b style='color:#63b3ed'>Step 3</b> — Hit <b>Generate simulated data</b><br>
<b style='color:#63b3ed'>Step 4</b> — Explore every analysis tab<br>
<b style='color:#63b3ed'>Step 5</b> — Track improvements in DMAIC
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Inputs + Simulation
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-title">Process Inputs & Data Simulation</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Configure the packing line and generate simulated package weights.</div>', unsafe_allow_html=True)

    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            target = st.number_input("Target weight (g)", value=500.0, step=0.5, format="%.2f")
            mean   = st.number_input("Process mean (g)",  value=500.5, step=0.5, format="%.2f")
        with c2:
            std    = st.number_input("Process std deviation (g)", value=2.0, step=0.1, format="%.2f")
            lsl    = st.number_input("LSL — Lower Specification Limit (g)", value=494.0, step=0.5, format="%.2f")
        with c3:
            usl    = st.number_input("USL — Upper Specification Limit (g)", value=506.0, step=0.5, format="%.2f")
            n_obs  = st.number_input("Sample size (per subgroup)", value=5, min_value=2, max_value=25, step=1)

        n_samples = st.slider("Number of samples (subgroups)", min_value=5, max_value=100, value=25, step=1)
        seed      = st.number_input("Random seed", value=42, step=1)

    if st.button("⚡ Generate simulated data", use_container_width=True):
        rng = np.random.default_rng(int(seed))
        data = rng.normal(loc=mean, scale=std, size=(n_samples, n_obs))
        st.session_state.sim_data   = data
        st.session_state.sim_params = dict(target=target, mean=mean, std=std,
                                           lsl=lsl, usl=usl,
                                           n_obs=int(n_obs), n_samples=int(n_samples))

    if st.session_state.sim_data is not None:
        data = st.session_state.sim_data
        p    = st.session_state.sim_params
        flat = data.flatten()

        st.markdown("---")
        st.markdown(f"""
<div class="status-ok">✅ &nbsp;Simulated {p['n_samples']} samples × {p['n_obs']} packages = <b>{p['n_samples']*p['n_obs']} observations</b>.</div>
""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Quick-stats row
        m1, m2, m3, m4 = st.columns(4)
        for col, label, val, unit in [
            (m1, "Observed Mean",    f"{np.mean(flat):.3f}", "grams"),
            (m2, "Observed Std",     f"{np.std(flat, ddof=1):.3f}", "grams"),
            (m3, "Min",              f"{flat.min():.2f}", "grams"),
            (m4, "Max",              f"{flat.max():.2f}", "grams"),
        ]:
            col.markdown(f"""
<div class="metric-card">
  <div class="metric-label">{label}</div>
  <div class="metric-value">{val}</div>
  <div class="metric-unit">{unit}</div>
</div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Data table
        cols_names = [f"x{i+1}" for i in range(p['n_obs'])]
        df = pd.DataFrame(data, columns=cols_names,
                          index=[f"Sample {i+1}" for i in range(p['n_samples'])])
        st.markdown("**Simulated package weights (samples × observations)**")
        st.dataframe(df.style.format("{:.2f}"), use_container_width=True, height=320)

        # Download
        csv_buf = io.StringIO()
        df.to_csv(csv_buf)
        st.download_button("⬇ Download data as CSV", csv_buf.getvalue(),
                           "packing_line_data.csv", "text/csv")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Capability Analysis
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-title">Process Capability Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Cp, Cpk and process distribution against specification limits.</div>', unsafe_allow_html=True)

    if st.session_state.sim_data is None:
        st.warning("⚠️  No simulation data yet. Go to **Inputs + Simulation** first.")
    else:
        data = st.session_state.sim_data
        p    = st.session_state.sim_params
        flat = data.flatten()

        obs_mean = np.mean(flat)
        obs_std  = np.std(flat, ddof=1)
        cp  = (p['usl'] - p['lsl']) / (6 * obs_std)
        cpu = (p['usl'] - obs_mean) / (3 * obs_std)
        cpl = (obs_mean - p['lsl']) / (3 * obs_std)
        cpk = min(cpu, cpl)
        pct_out = (np.sum(flat < p['lsl']) + np.sum(flat > p['usl'])) / len(flat) * 100

        # Metrics
        mc = st.columns(5)
        for col, label, val, unit in [
            (mc[0], "Process Mean",  f"{obs_mean:.3f}", "g"),
            (mc[1], "Process Std",   f"{obs_std:.3f}",  "g"),
            (mc[2], "Cp",            f"{cp:.3f}",       "potential"),
            (mc[3], "Cpk",           f"{cpk:.3f}",      "actual"),
            (mc[4], "Out of Spec",   f"{pct_out:.2f}%", ""),
        ]:
            col.markdown(f"""
<div class="metric-card">
  <div class="metric-label">{label}</div>
  <div class="metric-value">{val}</div>
  <div class="metric-unit">{unit}</div>
</div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Status
        if cpk >= 1.33:
            st.markdown(f'<div class="status-ok">🟢 &nbsp;<b>Highly Capable</b> (Cpk = {cpk:.3f}) — Cpk ≥ 1.33: process is well within specification.</div>', unsafe_allow_html=True)
        elif cpk >= 1.0:
            st.markdown(f'<div class="status-warn">🟡 &nbsp;<b>Capable but needs improvement</b> (Cpk = {cpk:.3f}) — 1.00 ≤ Cpk &lt; 1.33: acceptable but improvement recommended.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-bad">🔴 &nbsp;<b>Not capable</b> (Cpk = {cpk:.3f}) — Cpk &lt; 1.00: investigate centering and variation immediately.</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Distribution chart
        st.markdown("#### Process distribution vs. specifications")
        fig, ax = plt.subplots(figsize=(10, 4))
        x_range = np.linspace(min(flat.min(), p['lsl'] - 2), max(flat.max(), p['usl'] + 2), 400)
        ax.hist(flat, bins=25, density=True, color=ACCENT, alpha=0.25, label="Observed")
        ax.plot(x_range, stats.norm.pdf(x_range, obs_mean, obs_std),
                color=ACCENT, lw=2.5, label=f"Process curve N(μ={obs_mean:.2f}, σ={obs_std:.3f})")
        ax.axvline(obs_mean,   color=GREEN,  lw=2,   linestyle="-",  label=f"Mean = {obs_mean:.2f}")
        ax.axvline(p['target'],color=PURPLE, lw=1.5, linestyle="--", label=f"Target = {p['target']:.2f}")
        ax.axvline(p['lsl'],   color=RED,    lw=2,   linestyle="--", label=f"LSL = {p['lsl']:.2f}")
        ax.axvline(p['usl'],   color=RED,    lw=2,   linestyle="--", label=f"USL = {p['usl']:.2f}")
        ax.fill_betweenx([0, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 1],
                         p['lsl'], p['usl'], color=GREEN, alpha=0.04)
        ax.set_xlabel("Weight (g)"); ax.set_ylabel("Density")
        ax.set_title("Normal Distribution of Package Weights", fontweight="bold", color="#e2e8f0")
        ax.legend(loc="upper right"); ax.grid(True)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        st.markdown("---")
        st.markdown("#### Interpretation guide")
        col_a, col_b = st.columns(2)
        col_a.markdown("""
- **Cp** measures *potential* capability (spread vs. tolerance)
- **Cpk** measures *actual* capability — also penalises off-centring
- **Cp > Cpk** signals the process is off-target
""")
        col_b.markdown(f"""
| Cpk range | Verdict |
|-----------|---------|
| ≥ 1.33    | ✅ Highly capable |
| 1.00–1.33 | 🟡 Capable, improve |
| < 1.00    | 🔴 Not capable |
""")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Control Charts
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-title">Statistical Process Control Charts</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">X̄, R and p-chart with automatic out-of-control flagging.</div>', unsafe_allow_html=True)

    if st.session_state.sim_data is None:
        st.warning("⚠️  Generate data in **Inputs + Simulation** first.")
    else:
        data = st.session_state.sim_data
        p    = st.session_state.sim_params

        sample_means  = data.mean(axis=1)
        sample_ranges = data.max(axis=1) - data.min(axis=1)
        grand_mean    = sample_means.mean()
        mean_range    = sample_ranges.mean()

        # X-bar limits
        ucl_xbar = grand_mean + SPC["A2"] * mean_range
        lcl_xbar = grand_mean - SPC["A2"] * mean_range

        # R-chart limits
        ucl_r = SPC["D4"] * mean_range
        lcl_r = SPC["D3"] * mean_range

        # p-chart (defects = outside spec)
        flat  = data.flatten()
        lsl, usl = p['lsl'], p['usl']
        defects_per = np.array([np.sum((row < lsl) | (row > usl)) for row in data])
        p_vals = defects_per / p['n_obs']
        p_bar  = p_vals.mean()
        total_defects = defects_per.sum()
        sigma_p = np.sqrt(p_bar * (1 - p_bar) / p['n_obs']) if p_bar > 0 else 0
        ucl_p = p_bar + 3 * sigma_p
        lcl_p = max(0, p_bar - 3 * sigma_p)

        # Summary
        mc = st.columns(4)
        for col, label, val in [
            (mc[0], "X̄ (grand mean)",    f"{grand_mean:.3f}"),
            (mc[1], "R̄ (mean range)",    f"{mean_range:.3f}"),
            (mc[2], "p̄ (defect rate)",   f"{p_bar*100:.3f}%"),
            (mc[3], "Total defects",      f"{int(total_defects)} / {p['n_samples']*p['n_obs']}"),
        ]:
            col.markdown(f"""
<div class="metric-card">
  <div class="metric-label">{label}</div>
  <div class="metric-value">{val}</div>
</div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        xs = np.arange(1, p['n_samples'] + 1)
        ooc_xbar = (sample_means > ucl_xbar) | (sample_means < lcl_xbar)
        ooc_r    = (sample_ranges > ucl_r)   | (sample_ranges < lcl_r)
        ooc_p    = (p_vals > ucl_p)          | (p_vals < lcl_p)

        def make_chart(ax, xs, vals, cl, ucl, lcl, title, ylabel, color, ooc_mask):
            ax.plot(xs, vals, "o-", color=color, lw=1.8, ms=5, label="Value")
            ax.axhline(cl,  color=GREEN, lw=1.8, linestyle="-",  label=f"CL = {cl:.3f}")
            ax.axhline(ucl, color=RED,   lw=1.5, linestyle="--", label=f"UCL = {ucl:.3f}")
            ax.axhline(lcl, color=RED,   lw=1.5, linestyle="--", label=f"LCL = {lcl:.3f}")
            ax.fill_between(xs, lcl, ucl, color=GREEN, alpha=0.04)
            if ooc_mask.any():
                ax.scatter(xs[ooc_mask], vals[ooc_mask], color=RED, s=80, zorder=5, label="OOC")
            ax.set_title(title, fontweight="bold", color="#e2e8f0", fontsize=10)
            ax.set_xlabel("Sample"); ax.set_ylabel(ylabel)
            ax.legend(fontsize=7); ax.grid(True)

        fig, axes = plt.subplots(3, 1, figsize=(11, 11))
        make_chart(axes[0], xs, sample_means,  grand_mean,  ucl_xbar, lcl_xbar,
                   "X̄ Chart — Sample Means",   "Mean weight (g)", ACCENT, ooc_xbar)
        make_chart(axes[1], xs, sample_ranges, mean_range,  ucl_r,    lcl_r,
                   "R Chart — Sample Ranges",   "Range (g)",       YELLOW, ooc_r)
        make_chart(axes[2], xs, p_vals,        p_bar,       ucl_p,    lcl_p,
                   "p-Chart — Defect Proportion","Proportion",      PURPLE, ooc_p)
        fig.tight_layout(pad=2.5)
        st.pyplot(fig)
        plt.close(fig)

        if ooc_xbar.any() or ooc_r.any() or ooc_p.any():
            st.markdown(f'<div class="status-bad">⚠️  Out-of-control points detected — X̄: {ooc_xbar.sum()}, R: {ooc_r.sum()}, p: {ooc_p.sum()}. Investigate assignable causes.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-ok">✅ All points within control limits. Process appears stable.</div>', unsafe_allow_html=True)

        with st.expander("📖 Interpretation guide"):
            st.markdown("""
**X̄ chart** — monitors the process mean. Points outside UCL/LCL suggest the mean has shifted.

**R chart** — monitors within-subgroup variability. Spikes indicate instability in variation.

**p-chart** — tracks defect rate (items outside spec). Upward trends signal process degradation.

Control limits are computed from the data itself using SPC constants for n = 5:
- UCL_X̄ = X̄̄ + A₂·R̄ &nbsp;&nbsp; LCL_X̄ = X̄̄ − A₂·R̄
- UCL_R = D₄·R̄ &nbsp;&nbsp; LCL_R = D₃·R̄
""")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Quality Tools
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-title">Quality Tools</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Pareto chart of defect categories and sample-mean drift scatter analysis.</div>', unsafe_allow_html=True)

    if st.session_state.sim_data is None:
        st.warning("⚠️  Generate data in **Inputs + Simulation** first.")
    else:
        data = st.session_state.sim_data
        p    = st.session_state.sim_params

        col_left, col_right = st.columns([1, 1])

        # ── Pareto chart ────────────────────────────────────────────────────
        with col_left:
            st.markdown("#### Pareto Chart — Defect Categories")
            st.caption("Edit defect counts below to reflect observed line data.")

            defect_defaults = {
                "Underweight":    18,
                "Overweight":     12,
                "Seal failure":    9,
                "Label error":     7,
                "Foreign matter":  4,
                "Damaged pack":    3,
                "Other":           2,
            }
            defect_data = {}
            for cat, default in defect_defaults.items():
                defect_data[cat] = st.number_input(cat, value=default, min_value=0, step=1, key=f"def_{cat}")

            if st.button("📊 Update Pareto", key="pareto_btn"):
                pass  # triggers re-render

            cats   = list(defect_data.keys())
            counts = np.array(list(defect_data.values()), dtype=float)
            order  = np.argsort(counts)[::-1]
            cats   = [cats[i] for i in order]
            counts = counts[order]
            cumulative = np.cumsum(counts) / counts.sum() * 100

            fig, ax1 = plt.subplots(figsize=(6, 4))
            bars = ax1.bar(cats, counts, color=ACCENT, alpha=0.8, width=0.6)
            ax1.set_ylabel("Frequency", color="#a0aec0")
            ax1.tick_params(axis='x', rotation=35)
            ax2 = ax1.twinx()
            ax2.plot(cats, cumulative, "o-", color=RED, lw=2, ms=5, label="Cumulative %")
            ax2.axhline(80, color=YELLOW, lw=1.2, linestyle="--", label="80%")
            ax2.set_ylabel("Cumulative %", color="#a0aec0")
            ax2.set_ylim(0, 110)
            ax2.legend(loc="lower right", fontsize=7)
            ax1.set_title("Pareto — Defect Categories", fontweight="bold", color="#e2e8f0")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

            top80 = [c for c, cum in zip(cats, cumulative) if cum <= 80.0 + 1e-9]
            if top80:
                st.markdown(f'<div class="status-warn">📌 &nbsp;Top defects driving 80%+ issues: <b>{", ".join(top80)}</b>. Focus improvement efforts here.</div>', unsafe_allow_html=True)

        # ── Scatter — mean drift ─────────────────────────────────────────────
        with col_right:
            st.markdown("#### Sample Mean Drift Scatter")
            sample_means = data.mean(axis=1)
            xs = np.arange(1, p['n_samples'] + 1)
            z  = np.polyfit(xs, sample_means, 1)
            trend = np.poly1d(z)(xs)

            fig2, ax = plt.subplots(figsize=(6, 4))
            scatter = ax.scatter(xs, sample_means, c=xs, cmap="cool",
                                 s=55, zorder=3, edgecolors="#1a2035", lw=0.5)
            ax.plot(xs, trend, color=RED, lw=1.5, linestyle="--", label=f"Trend (slope={z[0]:.4f})")
            ax.axhline(p['target'], color=PURPLE, lw=1.3, linestyle=":", label=f"Target = {p['target']}")
            ax.set_xlabel("Sample #"); ax.set_ylabel("Sample mean (g)")
            ax.set_title("Sample Mean Drift Over Time", fontweight="bold", color="#e2e8f0")
            ax.legend(fontsize=7); ax.grid(True)
            plt.colorbar(scatter, ax=ax, label="Sample #", pad=0.01)
            fig2.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)

            slope_direction = "upward ↑" if z[0] > 0.005 else ("downward ↓" if z[0] < -0.005 else "flat —")
            st.markdown(f"**Trend slope:** `{z[0]:.5f} g/sample` — direction: **{slope_direction}**")
            if abs(z[0]) > 0.01:
                st.markdown('<div class="status-warn">⚠️  Non-trivial mean drift detected. Check filler calibration and material feed consistency.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-ok">✅  Mean appears stable across samples.</div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### Histogram of Sample Means")
            fig3, ax3 = plt.subplots(figsize=(6, 3))
            ax3.hist(sample_means, bins=12, color=PURPLE, alpha=0.75, edgecolor="#1a2035")
            ax3.axvline(sample_means.mean(), color=GREEN, lw=2, linestyle="--", label=f"Grand mean = {sample_means.mean():.3f}")
            ax3.axvline(p['target'],          color=YELLOW,lw=1.5,linestyle=":",  label=f"Target = {p['target']}")
            ax3.set_xlabel("Sample mean (g)"); ax3.set_ylabel("Count")
            ax3.set_title("Distribution of Sample Means", fontweight="bold", color="#e2e8f0")
            ax3.legend(fontsize=7); ax3.grid(True)
            fig3.tight_layout()
            st.pyplot(fig3)
            plt.close(fig3)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — DOE + CLT Sandbox
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-title">DOE + CLT Sandbox</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Design of Experiments module and Central Limit Theorem interactive demonstration.</div>', unsafe_allow_html=True)

    doe_tab, clt_tab = st.tabs(["🔬 Design of Experiments (DOE)", "📐 Central Limit Theorem"])

    # ── DOE ─────────────────────────────────────────────────────────────────
    with doe_tab:
        st.markdown("#### Full Factorial 2² DOE — Two Factors, Two Levels")
        st.markdown("Explore how **Fill Speed** and **Vibration Level** affect mean package weight.")

        dc1, dc2, dc3 = st.columns(3)
        with dc1:
            speed_lo  = st.number_input("Fill Speed — Low",  value=80.0, step=1.0)
            speed_hi  = st.number_input("Fill Speed — High", value=120.0,step=1.0)
        with dc2:
            vib_lo    = st.number_input("Vibration — Low",   value=1.0,  step=0.5)
            vib_hi    = st.number_input("Vibration — High",  value=3.0,  step=0.5)
        with dc3:
            doe_reps  = st.number_input("Replicates per run", value=5, min_value=2, max_value=20, step=1)
            doe_noise = st.number_input("Noise std (g)",       value=1.5, step=0.1)

        if st.button("▶ Run DOE Simulation", key="doe_btn"):
            rng = np.random.default_rng(123)
            design = [
                ("-", "-", speed_lo, vib_lo),
                ("+", "-", speed_hi, vib_lo),
                ("-", "+", speed_lo, vib_hi),
                ("+", "+", speed_hi, vib_hi),
            ]
            results = []
            for spd_lvl, vib_lvl, spd_val, vib_val in design:
                # simple linear model: higher speed → less weight, higher vibration → more weight
                effect_mean = 500 - 0.05*(spd_val - 100) + 0.8*(vib_val - 2)
                obs = rng.normal(effect_mean, doe_noise, int(doe_reps))
                results.append({
                    "Speed": spd_lvl, "Vibration": vib_lvl,
                    "Speed (rpm)": spd_val, "Vibration": vib_val,
                    "Run mean (g)": round(obs.mean(), 3),
                    "Run std (g)":  round(obs.std(ddof=1), 3),
                    "n": int(doe_reps),
                })

            df_doe = pd.DataFrame(results)
            st.dataframe(df_doe.style.format({"Run mean (g)": "{:.3f}", "Run std (g)": "{:.3f}"},
                                              subset=["Run mean (g)", "Run std (g)"]), use_container_width=True)

            # Interaction plot
            fig, ax = plt.subplots(figsize=(7, 3.5))
            lo_means = [df_doe.iloc[0]["Run mean (g)"], df_doe.iloc[1]["Run mean (g)"]]
            hi_means = [df_doe.iloc[2]["Run mean (g)"], df_doe.iloc[3]["Run mean (g)"]]
            xpos = [speed_lo, speed_hi]
            ax.plot(xpos, lo_means, "o-", color=ACCENT,  lw=2, ms=7, label=f"Vib = {vib_lo}")
            ax.plot(xpos, hi_means, "s--",color=YELLOW,  lw=2, ms=7, label=f"Vib = {vib_hi}")
            ax.axhline(500, color=GREEN, lw=1.3, linestyle=":", label="Target 500 g")
            ax.set_xlabel("Fill Speed (rpm)"); ax.set_ylabel("Mean weight (g)")
            ax.set_title("DOE Interaction Plot", fontweight="bold", color="#e2e8f0")
            ax.legend(); ax.grid(True)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

            # Main effects
            speed_eff = ((df_doe.iloc[1]["Run mean (g)"] + df_doe.iloc[3]["Run mean (g)"]) -
                         (df_doe.iloc[0]["Run mean (g)"] + df_doe.iloc[2]["Run mean (g)"])) / 2
            vib_eff   = ((df_doe.iloc[2]["Run mean (g)"] + df_doe.iloc[3]["Run mean (g)"]) -
                         (df_doe.iloc[0]["Run mean (g)"] + df_doe.iloc[1]["Run mean (g)"])) / 2

            ea, eb = st.columns(2)
            ea.markdown(f"""
<div class="metric-card">
  <div class="metric-label">Fill Speed Effect</div>
  <div class="metric-value">{speed_eff:+.3f}</div>
  <div class="metric-unit">g per level change</div>
</div>""", unsafe_allow_html=True)
            eb.markdown(f"""
<div class="metric-card">
  <div class="metric-label">Vibration Effect</div>
  <div class="metric-value">{vib_eff:+.3f}</div>
  <div class="metric-unit">g per level change</div>
</div>""", unsafe_allow_html=True)

    # ── CLT ─────────────────────────────────────────────────────────────────
    with clt_tab:
        st.markdown("#### Central Limit Theorem Demonstration")
        st.markdown("Shows how sample means converge to normal regardless of the underlying distribution.")

        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            clt_dist = st.selectbox("Population distribution", ["Uniform", "Exponential", "Skewed (gamma)", "Normal"])
        with cc2:
            clt_n    = st.slider("Sample size n", 1, 100, 30)
        with cc3:
            clt_sims = st.slider("Number of samples drawn", 100, 5000, 1000, step=100)

        rng_clt = np.random.default_rng(7)
        if clt_dist == "Uniform":
            pop = rng_clt.uniform(0, 10, 100000)
        elif clt_dist == "Exponential":
            pop = rng_clt.exponential(2, 100000)
        elif clt_dist == "Skewed (gamma)":
            pop = rng_clt.gamma(2, 2, 100000)
        else:
            pop = rng_clt.normal(5, 2, 100000)

        sample_means_clt = [rng_clt.choice(pop, clt_n, replace=True).mean() for _ in range(clt_sims)]
        sample_means_clt = np.array(sample_means_clt)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
        ax1.hist(pop[:5000], bins=50, color=YELLOW, alpha=0.75, density=True, edgecolor="#1a2035")
        ax1.set_title(f"Population — {clt_dist}", fontweight="bold", color="#e2e8f0")
        ax1.set_xlabel("Value"); ax1.set_ylabel("Density"); ax1.grid(True)

        ax2.hist(sample_means_clt, bins=50, color=ACCENT, alpha=0.75, density=True, edgecolor="#1a2035")
        mu_clt = sample_means_clt.mean(); sd_clt = sample_means_clt.std()
        xr = np.linspace(sample_means_clt.min(), sample_means_clt.max(), 300)
        ax2.plot(xr, stats.norm.pdf(xr, mu_clt, sd_clt), color=RED, lw=2.5, label="Normal fit")
        ax2.set_title(f"Distribution of X̄ (n={clt_n}, {clt_sims} draws)", fontweight="bold", color="#e2e8f0")
        ax2.set_xlabel("Sample mean"); ax2.set_ylabel("Density"); ax2.legend(); ax2.grid(True)
        fig.suptitle("Central Limit Theorem", fontsize=12, fontweight="bold", color="#e2e8f0")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        # Normality test
        stat, pval = stats.shapiro(sample_means_clt[:500])
        if pval > 0.05:
            st.markdown(f'<div class="status-ok">✅  Shapiro-Wilk p = {pval:.4f} — sample means are approximately normal (p > 0.05).</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-warn">🟡  Shapiro-Wilk p = {pval:.4f} — mild departure from normality detected with n={clt_n}. Try larger n.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 — DMAIC Tracker
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-title">DMAIC Improvement Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Six Sigma DMAIC checklist tailored to the packing line. Track progress across all phases.</div>', unsafe_allow_html=True)

    phases = {
        "Define": {
            "icon": "🎯",
            "color": "#63b3ed",
            "items": [
                "Define the problem statement (e.g., weight variation exceeds ±6 g)",
                "Identify the project scope (which SKUs / lines are affected)",
                "Document Voice of the Customer (VoC) for weight tolerance",
                "Map the high-level process (SIPOC)",
                "Establish project charter and team roles",
                "Set measurable project goals (e.g., Cpk ≥ 1.33 in 90 days)",
            ]
        },
        "Measure": {
            "icon": "📏",
            "color": "#68d391",
            "items": [
                "Perform Measurement System Analysis (MSA / Gauge R&R) on checkweighers",
                "Collect baseline weight data (≥ 25 subgroups, n = 5)",
                "Calculate baseline Cp and Cpk",
                "Plot baseline X̄ and R charts; note OOC points",
                "Identify defect categories and record Pareto data",
                "Confirm % out-of-spec (DPMO baseline)",
            ]
        },
        "Analyze": {
            "icon": "🔬",
            "color": "#b794f4",
            "items": [
                "Perform fishbone (Ishikawa) analysis on weight variation",
                "Run DOE (at minimum 2² full factorial) on key input factors",
                "Identify top assignable causes driving OOC signals",
                "Confirm mean drift using scatter / regression analysis",
                "Validate root causes with hypothesis tests (t-test, F-test)",
                "Prioritize causes using Pareto (80/20 rule)",
            ]
        },
        "Improve": {
            "icon": "⚡",
            "color": "#f6ad55",
            "items": [
                "Pilot corrective actions on identified root causes",
                "Re-run DOE with optimised factor settings",
                "Verify improved Cp / Cpk on pilot data",
                "Update control limits based on improved process",
                "Update SOPs and operator work instructions",
                "Validate improvement with at least 25 new subgroups",
            ]
        },
        "Control": {
            "icon": "🔒",
            "color": "#fc8181",
            "items": [
                "Implement control plan with response rules for OOC points",
                "Set up SPC charts on the live line (X̄, R, p)",
                "Define control chart monitoring frequency and owner",
                "Train operators on new SOP and OOC response protocol",
                "Schedule periodic Cpk reviews (monthly recommended)",
                "Close project; document lessons learned and savings",
            ]
        },
    }

    total_items    = sum(len(v["items"]) for v in phases.values())
    total_checked  = 0

    for phase_name, phase in phases.items():
        checked = []
        with st.expander(f"{phase['icon']}  **{phase_name} Phase**", expanded=False):
            st.markdown(f"<div style='color:{phase['color']}; font-size:0.72rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.8rem'>{phase_name.upper()} — {len(phase['items'])} action items</div>", unsafe_allow_html=True)
            for i, item in enumerate(phase["items"]):
                val = st.checkbox(item, key=f"dmaic_{phase_name}_{i}")
                if val:
                    checked.append(i)

        total_checked += len(checked)
        pct = len(checked) / len(phase["items"]) * 100
        color = phase["color"]
        st.markdown(f"""
<div style='display:flex; align-items:center; gap:0.8rem; margin:-0.4rem 0 0.8rem 0.5rem'>
  <div style='flex:1; height:4px; background:#1a2035; border-radius:2px'>
    <div style='width:{pct:.0f}%; height:100%; background:{color}; border-radius:2px'></div>
  </div>
  <div style='font-family:JetBrains Mono,monospace; font-size:0.72rem; color:{color}; width:3.5rem; text-align:right'>{len(checked)}/{len(phase["items"])}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    overall_pct = total_checked / total_items * 100
    st.markdown(f"#### Overall DMAIC Progress: {total_checked} / {total_items} items ({overall_pct:.0f}%)")
    bar_color = GREEN if overall_pct >= 80 else (YELLOW if overall_pct >= 40 else ACCENT)
    st.markdown(f"""
<div style='height:12px; background:#1a2035; border-radius:6px; overflow:hidden; margin-bottom:0.5rem'>
  <div style='width:{overall_pct:.1f}%; height:100%; background:linear-gradient(90deg, {bar_color}, {ACCENT}); border-radius:6px; transition:width 0.3s'></div>
</div>
""", unsafe_allow_html=True)

    if overall_pct == 100:
        st.markdown('<div class="status-ok">🎉 All DMAIC phases complete! Document the project and transition to ongoing monitoring.</div>', unsafe_allow_html=True)
    elif overall_pct >= 60:
        st.markdown('<div class="status-warn">🔄 Good progress — continue through Improve and Control phases to sustain gains.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-bad">📋 Project in early stages. Complete Define and Measure phases to establish a solid baseline.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Export DMAIC Status Report")
    if st.button("📄 Generate text report", key="dmaic_export"):
        lines = ["DMAIC TRACKER REPORT", "=" * 40, ""]
        for phase_name, phase in phases.items():
            lines.append(f"[ {phase_name.upper()} ]")
            for i, item in enumerate(phase["items"]):
                chk = st.session_state.get(f"dmaic_{phase_name}_{i}", False)
                lines.append(f"  {'[x]' if chk else '[ ]'}  {item}")
            lines.append("")
        lines.append(f"Overall: {total_checked}/{total_items} ({overall_pct:.0f}%)")
        report_text = "\n".join(lines)
        st.download_button("⬇ Download report (.txt)", report_text, "dmaic_report.txt", "text/plain")
