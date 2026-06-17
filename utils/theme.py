"""
Single source of truth untuk CSS, color constants, dan Plotly base layout.
Digunakan di semua halaman untuk konsistensi visual.
"""

import streamlit as st

# COLOR CONSTANTS
COLORS = {
    "green"  : "#4caf50",
    "green2" : "#66bb6a",
    "teal"   : "#26a69a",
    "blue"   : "#2196f3",
    "orange" : "#ff9800",
    "red"    : "#f44336",
    "purple" : "#9c27b0",
    "yellow" : "#ffc107",
    "bg"     : "#0e1117",
    "card"   : "#1a1f2e",
    "border" : "#2d3748",
    "text"   : "#e2e8f0",
    "muted"  : "#718096",
}

# Alias singkat untuk backward-compat dengan file yang pakai C = {...}
C = COLORS

# PLOTLY BASE LAYOUT
PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=COLORS["muted"], size=11, family="Inter"),
    margin=dict(t=42, b=36, l=36, r=16),
    xaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", showline=False),
    yaxis=dict(gridcolor="#2d3748", zerolinecolor="#2d3748", showline=False),
)

# Alias singkat
PBASE = PLOTLY_BASE


# CSS INJECTION

def inject_css():
    """Inject global CSS dark-theme ke halaman Streamlit."""
    C = COLORS
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

/* ── KPI Cards ────────────────────────────────────────────── */
.kpi-wrap {{
    background: {C['card']};
    border: 1px solid {C['border']};
    border-radius: 14px;
    padding: 1.2rem 1.4rem 1rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: transform .18s ease, border-color .18s ease;
}}
.kpi-wrap:hover {{
    transform: translateY(-3px);
    border-color: #4a5568;
}}
.kpi-wrap::after {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}}
.kpi-green::after  {{ background: linear-gradient(90deg,{C['green']},{C['teal']}); }}
.kpi-blue::after   {{ background: linear-gradient(90deg,{C['blue']},#7c3aed); }}
.kpi-orange::after {{ background: linear-gradient(90deg,{C['orange']},{C['yellow']}); }}
.kpi-red::after    {{ background: linear-gradient(90deg,{C['red']},{C['orange']}); }}
.kpi-purple::after {{ background: linear-gradient(90deg,{C['purple']},#ec4899); }}
.kpi-teal::after   {{ background: linear-gradient(90deg,{C['teal']},{C['blue']}); }}

.kpi-icon  {{ font-size:1.7rem; margin-bottom:.35rem; display:block; }}
.kpi-lbl   {{ font-size:.7rem; color:{C['muted']}; text-transform:uppercase;
              letter-spacing:.1em; font-weight:600; margin-bottom:.25rem; }}
.kpi-val   {{ font-size:1.9rem; font-weight:800; color:{C['text']};
              font-family:'JetBrains Mono',monospace; line-height:1; }}
.kpi-sub   {{ font-size:.73rem; margin-top:.3rem; font-weight:500; }}
.kpi-sub.up   {{ color:{C['green']}; }}
.kpi-sub.dn   {{ color:{C['red']}; }}
.kpi-sub.neu  {{ color:{C['muted']}; }}

/* ── KPI Result (large centered output di prediksi.py) ────── */
.kpi-result {{
    border-radius: 14px;
    padding: 2rem 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    border: 1px solid {C['border']};
}}
.kpi-result::after {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    border-radius: 14px 14px 0 0;
}}
.kpi-result.res-green  {{ background: rgba(76,175,80,.08); }}
.kpi-result.res-green::after {{ background: linear-gradient(90deg,{C['green']},{C['teal']}); }}
.kpi-result.res-orange {{ background: rgba(255,152,0,.08); }}
.kpi-result.res-orange::after {{ background: linear-gradient(90deg,{C['orange']},{C['yellow']}); }}
.kpi-result.res-red    {{ background: rgba(244,67,54,.08); }}
.kpi-result.res-red::after {{ background: linear-gradient(90deg,{C['red']},{C['orange']}); }}

.kpi-result .res-label  {{ font-size:2rem; font-weight:800; font-family:'JetBrains Mono',monospace; line-height:1; }}
.kpi-result .res-sub    {{ font-size:.85rem; margin-top:.5rem; color:{C['muted']}; }}
.kpi-result .res-badge  {{ display:inline-block; padding:.3rem .8rem; border-radius:20px;
                           font-size:.75rem; font-weight:700; margin-top:.6rem;
                           font-family:'JetBrains Mono',monospace; }}
.res-green  .res-badge  {{ background:rgba(76,175,80,.2); color:{C['green']}; border:1px solid {C['green']}55; }}
.res-orange .res-badge  {{ background:rgba(255,152,0,.2); color:{C['orange']}; border:1px solid {C['orange']}55; }}
.res-red    .res-badge  {{ background:rgba(244,67,54,.2); color:{C['red']}; border:1px solid {C['red']}55; }}

/* ── Input Cards (form sections di prediksi.py) ───────────── */
.input-card {{
    background: {C['card']};
    border: 1px solid {C['border']};
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}}
.input-card-title {{
    font-size:.8rem; font-weight:700; text-transform:uppercase;
    letter-spacing:.08em; color:{C['muted']};
    margin-bottom:.9rem; display:flex; align-items:center; gap:.4rem;
}}

/* ── Section headers ─────────────────────────────────────── */
.sec-hdr {{
    display:flex; align-items:center; gap:.6rem;
    padding:.5rem 0 .6rem 0;
    border-bottom: 1px solid {C['border']};
    margin: 1.8rem 0 1rem 0;
}}
.sec-hdr h3 {{ margin:0; font-size:1rem; font-weight:700; color:{C['text']}; }}
.sec-dot {{
    width:9px; height:9px; border-radius:50%; flex-shrink:0;
    background: linear-gradient(135deg,{C['green']},{C['teal']});
}}

/* ── Info boxes ──────────────────────────────────────────── */
.ibox {{
    border-radius:10px; padding:.9rem 1.1rem;
    font-size:.8rem; line-height:1.65; color:{C['muted']};
}}
.ibox.green  {{ background:rgba(76,175,80,.07); border:1px solid rgba(76,175,80,.25); }}
.ibox.orange {{ background:rgba(255,152,0,.07); border:1px solid rgba(255,152,0,.25); }}
.ibox.blue   {{ background:rgba(33,150,243,.07); border:1px solid rgba(33,150,243,.25); }}
.ibox.red    {{ background:rgba(244,67,54,.07); border:1px solid rgba(244,67,54,.25); }}

/* ── Feature bar ─────────────────────────────────────────── */
.fbar-wrap {{ margin-bottom:.45rem; }}
.fbar-row  {{ display:flex; justify-content:space-between; margin-bottom:.2rem; }}
.fbar-name {{ font-size:.78rem; font-weight:600; color:{C['text']};
              font-family:'JetBrains Mono',monospace; }}
.fbar-pct  {{ font-size:.75rem; color:{C['green']}; font-family:'JetBrains Mono',monospace; }}
.fbar-bg   {{ background:#2d3748; border-radius:4px; height:5px; }}
.fbar-fill {{ border-radius:4px; height:5px;
              background:linear-gradient(90deg,{C['green']},{C['teal']}); }}

/* ── Pill tags ───────────────────────────────────────────── */
.pill {{
    display:inline-block; padding:.22rem .7rem;
    border-radius:20px; font-size:.72rem; font-weight:600;
    margin:.15rem .1rem; font-family:'JetBrains Mono',monospace;
}}
.pill-green  {{ background:rgba(76,175,80,.15); color:{C['green']};
                border:1px solid rgba(76,175,80,.35); }}
.pill-blue   {{ background:rgba(33,150,243,.15); color:{C['blue']};
                border:1px solid rgba(33,150,243,.35); }}
.pill-orange {{ background:rgba(255,152,0,.15);  color:{C['orange']};
                border:1px solid rgba(255,152,0,.35); }}
.pill-red    {{ background:rgba(244,67,54,.15);  color:{C['red']};
                border:1px solid rgba(244,67,54,.35); }}

/* ── AI Report Card ──────────────────────────────────────── */
.ai-report-card {{
    background: {C['card']};
    border: 1px solid {C['border']};
    border-left: 4px solid {C['green']};
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin: 1rem 0;
    font-size: .85rem;
    line-height: 1.7;
    color: {C['text']};
}}

/* ── Page header ─────────────────────────────────────────── */
.page-header {{
    border-left: 4px solid {C['green']};
    padding-left: 16px;
    margin-bottom: 4px;
}}
.page-header h1 {{
    margin: 0; font-size: 28px; font-weight: 800; color: {C['text']};
}}
.page-header p {{
    margin: 4px 0 0 0; opacity: .55; font-size: 13px;
}}

/* ── Scrollbar ───────────────────────────────────────────── */
::-webkit-scrollbar {{ width:5px; height:5px; }}
::-webkit-scrollbar-track {{ background:{C['bg']}; }}
::-webkit-scrollbar-thumb {{ background:#4a5568; border-radius:3px; }}
</style>
""", unsafe_allow_html=True)


# REUSABLE COMPONENTS

def page_header(title: str, subtitle: str = "", icon: str = ""):
    """Render halaman header dengan border-left green."""
    full_title = f"{icon} {title}" if icon else title
    st.markdown(f"""
<div class="page-header">
    <h1>{full_title}</h1>
    <p>{subtitle}</p>
</div>
""", unsafe_allow_html=True)


def section_header(title: str):
    """Render section header dengan dot accent."""
    st.markdown(f"""
<div class="sec-hdr">
    <div class="sec-dot"></div>
    <h3>{title}</h3>
</div>
""", unsafe_allow_html=True)


def kpi_card(col, color_cls: str, icon: str, label: str, value: str, sub: str, sub_cls: str = "neu"):
    """Render KPI card di dalam kolom Streamlit."""
    with col:
        st.markdown(f"""
<div class="kpi-wrap {color_cls}">
    <span class="kpi-icon">{icon}</span>
    <div class="kpi-lbl">{label}</div>
    <div class="kpi-val">{value}</div>
    <div class="kpi-sub {sub_cls}">{sub}</div>
</div>""", unsafe_allow_html=True)


def prediction_result_card(prob: float, label: str, sub: str, badge: str, color_cls: str):
    """Render kartu hasil prediksi besar (KPI result) di prediksi.py."""
    pct = prob * 100
    st.markdown(f"""
<div class="kpi-result {color_cls}">
    <div class="res-label">{label}</div>
    <div class="res-sub">{pct:.1f}% probabilitas spoilage</div>
    <div class="res-badge">{badge}</div>
    <div class="res-sub" style="margin-top:.5rem;">{sub}</div>
</div>
""", unsafe_allow_html=True)


def info_box(text: str, color: str = "green"):
    """Render info box berwarna. color: green | orange | blue | red"""
    st.markdown(f'<div class="ibox {color}">{text}</div>', unsafe_allow_html=True)
