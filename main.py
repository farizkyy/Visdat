"""
Dashboard Gaya Hidup Mahasiswa — Entry Point
Menyatukan semua modul: config, data_loader, charts, insights
"""

import streamlit as st
import pandas as pd

from config import apply_config
from data_loader import load_and_clean_data
from charts import (
    scatter_study_gpa,
    box_extracurricular_gpa,
    heatmap_correlation,
    hist_gpa_distribution,
    bubble_sleep_stress_gpa,
    bar_gpa_by_gender_study,
    violin_anxiety_job,
    radar_profile,
    pie_sleep_category,
    bar_diet_quality_gpa,
)
from insights import (
    generate_deep_insights,
    generate_comparative_analysis,
    generate_strategic_recommendations,
)


# 1. KONFIGURASI & CSS
apply_config()

# 2. LOAD DATA
df = load_and_clean_data()

# 3. SIDEBAR — Filter
st.sidebar.header("⚙️ Opsi Filter")

gpa_min, gpa_max = float(df["Previous_GPA"].min()), float(df["Previous_GPA"].max())
gpa_range = st.sidebar.slider(
    "Rentang GPA",
    min_value=gpa_min,
    max_value=gpa_max,
    value=(gpa_min, gpa_max),
    step=0.1,
)

stress_min, stress_max = float(df["Stress_Level"].min()), float(df["Stress_Level"].max())
stress_range = st.sidebar.slider(
    "Rentang Tingkat Stres",
    min_value=stress_min,
    max_value=stress_max,
    value=(stress_min, stress_max),
    step=0.01,
)

sleep_min, sleep_max = float(df["Sleep_Hours"].min()), float(df["Sleep_Hours"].max())
sleep_range = st.sidebar.slider(
    "Rentang Jam Tidur",
    min_value=sleep_min,
    max_value=sleep_max,
    value=(sleep_min, sleep_max),
    step=0.5,
)

filtered_df = df[
    (df["Previous_GPA"] >= gpa_range[0]) & (df["Previous_GPA"] <= gpa_range[1]) &
    (df["Stress_Level"] >= stress_range[0]) & (df["Stress_Level"] <= stress_range[1]) &
    (df["Sleep_Hours"] >= sleep_range[0]) & (df["Sleep_Hours"] <= sleep_range[1])
].copy()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**📊 Data Tersaring:** {len(filtered_df):,} / {len(df):,} baris")

# Download CSV
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    label="⬇️ Download Data (CSV)",
    data=csv,
    file_name="data_filtered.csv",
    mime="text/csv",
)

# 4. HEADER
st.title("📊 Dashboard Gaya Hidup Mahasiswa")
st.caption(
    "Eksplorasi interaktif hubungan antara tidur, stres, kebiasaan belajar, dan performa akademik."
)
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# 5. METRIK UTAMA
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Rata-rata GPA", f"{filtered_df['Previous_GPA'].mean():.2f}")
m2.metric("Rata-rata Tidur (jam)", f"{filtered_df['Sleep_Hours'].mean():.1f}")
m3.metric("Rata-rata Belajar (norm)", f"{filtered_df['Hours_Studied'].mean():.2f}")
m4.metric("Rata-rata Stres", f"{filtered_df['Stress_Level'].mean():.2f}")
m5.metric("Rata-rata Kecemasan", f"{filtered_df['Exam_Anxiety_Score'].mean():.2f}")

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

# 6. TABS — VISUALISASI
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔑 Hubungan Utama",
    "📈 Distribusi & Pola",
    "👤 Demografi & Perilaku",
    "🌡️ Kesehatan & Stres",
    "🔥 Korelasi Lengkap",
])

# Hubungan Utama
with tab1:
    st.markdown("### 🔑 Hubungan Variabel Kunci")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Jam Belajar vs GPA")
        st.plotly_chart(scatter_study_gpa(filtered_df), width="stretch")

    with col2:
        st.subheader("GPA Berdasarkan Ekstrakurikuler")
        st.plotly_chart(box_extracurricular_gpa(filtered_df), width="stretch")

    # INSIGHT & STORYTELLING
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("### 📋 Insight dan Analisis Strategis")

    deep_insights = generate_deep_insights(filtered_df)
    comparative = generate_comparative_analysis(filtered_df)
    recommendations = generate_strategic_recommendations(filtered_df)

    with st.expander("📖 Interpretasi Mendalam", expanded=True):
        for text, alert_type in deep_insights:
            if alert_type == "success":
                st.success(text)
            elif alert_type == "warning":
                st.warning(text)
            else:
                st.info(text)

    with st.expander("⚖️ Analisis Komparatif", expanded=True):
        for text, alert_type in comparative:
            if alert_type == "success":
                st.success(text)
            elif alert_type == "warning":
                st.warning(text)
            else:
                st.info(text)

    with st.expander("💡 Saran Strategis", expanded=True):
        for text, alert_type in recommendations:
            if alert_type == "success":
                st.success(text)
            elif alert_type == "warning":
                st.warning(text)
            else:
                st.info(text)

# Distribusi & Pola
with tab2:
    st.markdown("### 📈 Distribusi dan Pola Data")
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Distribusi GPA")
        st.plotly_chart(hist_gpa_distribution(filtered_df), width="stretch")

    with c2:
        st.subheader("Kategori Jam Tidur")
        st.plotly_chart(pie_sleep_category(filtered_df), width="stretch")

    st.markdown("<br>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Diet Quality vs GPA")
        st.plotly_chart(bar_diet_quality_gpa(filtered_df), width="stretch")

    with c4:
        st.subheader("Profil GPA Tinggi vs Rendah")
        st.plotly_chart(radar_profile(filtered_df), width="stretch")

# Demografi & Perilaku
with tab3:
    st.markdown("### 👤 Demografi dan Perilaku Belajar")
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("GPA berdasarkan Gender & Metode Belajar")
        st.plotly_chart(bar_gpa_by_gender_study(filtered_df), width="stretch")

    with c2:
        st.subheader("Bubble: Tidur, Stres, & GPA")
        st.plotly_chart(bubble_sleep_stress_gpa(filtered_df), width="stretch")

# Kesehatan & Stres
with tab4:
    st.markdown("### 🌡️ Kesehatan Mental dan Stres")
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Kecemasan Ujian vs Kerja Paruh Waktu")
        st.plotly_chart(violin_anxiety_job(filtered_df), width="stretch")

    with c2:
        st.subheader("Insight: Tidur vs Stres")
        corr = filtered_df["Sleep_Hours"].corr(filtered_df["Stress_Level"])
        st.metric("Korelasi Tidur-Stres", f"{corr:.3f}")
        st.markdown(
            f"Semakin tinggi korelasi negatif, artinya mahasiswa yang tidur lebih lama "
            f"cenderung mengalami stres lebih rendah. Saat ini korelasi: **{corr:.3f}**."
        )

# Korelasi Lengkap
with tab5:
    st.markdown("### 🔥 Heatmap Korelasi Lengkap")
    lifestyle_cols = [
        "Sleep_Hours", "Stress_Level", "Hours_Studied", "Screen_Time",
        "Diet_Quality", "Previous_GPA", "Final_Score",
        "Work_Life_Balance", "Exam_Anxiety_Score",
    ]
    st.plotly_chart(
        heatmap_correlation(filtered_df, lifestyle_cols),
        width="stretch",
    )

# 7. FOOTER
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.caption(
    "Dibuat dengan Streamlit & Plotly | Prinsip: High Data-Ink Ratio & Modern UI"
)