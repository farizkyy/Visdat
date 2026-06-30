"""
Konfigurasi global, tema, styling CSS, dan palet warna untuk dashboard.
"""

import streamlit as st

# ── Konfigurasi Halaman ──
PAGE_CONFIG = {
    "page_title": "Dashboard Gaya Hidup Mahasiswa",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# ── Palet Warna Modern ──
COLORS = {
    "primary": "#0F172A",      # slate-900
    "secondary": "#334155",    # slate-700
    "accent": "#06B6D4",       # cyan-500
    "accent2": "#F43F5E",      # rose-500
    "accent3": "#10B981",      # emerald-500
    "accent4": "#8B5CF6",      # violet-500
    "bg_light": "#F8FAFC",     # slate-50
    "bg_card": "#FFFFFF",
    "text_main": "#0F172A",
    "text_muted": "#64748B",
    "border": "#E2E8F0",
}

CHART_COLORSCALE = "Viridis"
HEATMAP_COLORSCALE = "RdBu"

# ── CSS Custom Final (Fix Sidebar Contrast) ──
CSS_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* --- Sidebar Styling --- */
[data-testid="stSidebar"] {
    background-color: #F1F5F9 !important;
    border-right: 1px solid #E2E8F0;
}

/* Maksa teks sidebar jadi item pekat agar kontras (Fix image_98af50.png) */
[data-testid="stSidebar"] .stMarkdown p, 
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] .stSlider p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] .stCaption {
    color: #1E293B !important; 
    font-weight: 600 !important;
}

/* Warna angka rentang di ujung slider */
[data-testid="stSidebar"] [data-testid="stTickBarMin"],
[data-testid="stSidebar"] [data-testid="stTickBarMax"],
[data-testid="stSidebar"] [data-baseweb="slider"] div {
    color: #1E293B !important;
}

/* Judul/Heading di Sidebar */
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3 {
    color: #0F172A !important;
    margin-bottom: 1rem;
}

/* --- Main Content Styling --- */
h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    color: #0F172A;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}

.stSlider [data-baseweb="slider"] {
    margin-top: 25px;
}

div[data-testid="metric-container"] {
    background-color: #FFFFFF;
    border-left: 4px solid #06B6D4;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
    transition: all 0.2s ease;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
}

div.stPlotlyChart > div {
    border-radius: 12px;
    overflow: hidden;
}

.insight-card {
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #E2E8F0;
    margin-bottom: 1rem;
}

.section-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #E2E8F0, transparent);
    margin: 2rem 0;
}
</style>
"""

def apply_config():
    """Terapkan konfigurasi halaman dan CSS."""
    # set_page_config WAJIB dipanggil paling pertama di main.py 
    # (Biasanya dipanggil lewat fungsi ini)
    st.set_page_config(**PAGE_CONFIG)
    st.markdown(CSS_STYLE, unsafe_allow_html=True)