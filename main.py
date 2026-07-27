import streamlit as st

from config import apply_config
from data_loader import load_and_clean_data
from charts import (
    scatter_study_gpa,
    heatmap_correlation,
    hist_gpa_distribution,
    bubble_sleep_stress_gpa,
    bar_gpa_by_gender_study,

    violin_anxiety_job,
    radar_profile,
    pie_sleep_category,
)
from insights import (
    generate_deep_insights,
    generate_comparative_analysis,
    generate_strategic_recommendations,
)

apply_config()

df = load_and_clean_data()

st.sidebar.header("Opsi Filter")

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
    (df["Previous_GPA"] >= gpa_range[0])
    & (df["Previous_GPA"] <= gpa_range[1])
    & (df["Stress_Level"] >= stress_range[0])
    & (df["Stress_Level"] <= stress_range[1])
    & (df["Sleep_Hours"] >= sleep_range[0])
    & (df["Sleep_Hours"] <= sleep_range[1])
].copy()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Data tersaring:** {len(filtered_df):,} / {len(df):,} baris")

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    label="Download Data (CSV)",
    data=csv,
    file_name="data_filtered.csv",
    mime="text/csv",
)

st.title("Dashboard Gaya Hidup Mahasiswa")
st.caption("Eksplorasi interaktif hubungan antara tidur, stres, kebiasaan belajar, dan performa akademik.")
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Rata-rata Nilai Akhir (GPA)", f"{filtered_df['Final_Score'].mean():.2f}")
m2.metric("Rata-rata Jam Tidur", f"{filtered_df['Sleep_Hours'].mean():.1f}")
m3.metric("Rata-rata Jam Belajar", f"{filtered_df['Hours_Studied'].mean():.2f}")
m4.metric("Rata-rata Tingkat Stres", f"{filtered_df['Stress_Level'].mean():.2f}")
m5.metric("Rata-rata Kecemasan", f"{filtered_df['Exam_Anxiety_Score'].mean():.2f}")

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

st_tabs = st.tabs(["Performa Akademik", "Pola Hidup & Kesejahteraan", "Profil Mahasiswa"])

tab1, tab2, tab3 = st_tabs

with tab1:
    st.subheader("Scatter Plot: Jam Belajar vs Nilai Akhir")
    st.plotly_chart(scatter_study_gpa(filtered_df), width="stretch")

    st.subheader("Distribusi Nilai Akhir")
    st.plotly_chart(hist_gpa_distribution(filtered_df), width="stretch")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.subheader("Insight dan Analisis Strategis")

    deep_insights = generate_deep_insights(filtered_df)
    comparative = generate_comparative_analysis(filtered_df)
    recommendations = generate_strategic_recommendations(filtered_df)

    with st.expander("Interpretasi Mendalam", expanded=True):
        for text, alert_type in deep_insights:
            if alert_type == "success":
                st.success(text)
            elif alert_type == "warning":
                st.warning(text)
            else:
                st.info(text)

    with st.expander("Analisis Komparatif", expanded=True):
        for text, alert_type in comparative:
            if alert_type == "success":
                st.success(text)
            elif alert_type == "warning":
                st.warning(text)
            else:
                st.info(text)

    with st.expander("Saran Strategis", expanded=True):
        for text, alert_type in recommendations:
            if alert_type == "success":
                st.success(text)
            elif alert_type == "warning":
                st.warning(text)
            else:
                st.info(text)

with tab2:
    st.subheader("Kategori Jam Tidur")
    st.plotly_chart(pie_sleep_category(filtered_df), width="stretch")

    st.subheader("Bubble: Tidur, Stres, & Work-Life Balance")
    st.plotly_chart(bubble_sleep_stress_gpa(filtered_df), width="stretch")

    st.subheader("Kecemasan Ujian vs Kerja Paruh Waktu")
    st.plotly_chart(violin_anxiety_job(filtered_df), width="stretch")

with tab3:
    st.subheader("Profil Mahasiswa: GPA Tinggi vs Rendah")
    st.plotly_chart(radar_profile(filtered_df), width="stretch")

    st.subheader("Heatmap Korelasi Lengkap")
    lifestyle_cols = [
        "Sleep_Hours",
        "Stress_Level",
        "Hours_Studied",
        "Screen_Time",
        "Diet_Quality",
        "Previous_GPA",
        "Final_Score",
        "Work_Life_Balance",
        "Exam_Anxiety_Score",
    ]
    st.plotly_chart(heatmap_correlation(filtered_df, lifestyle_cols), width="stretch")


st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.caption("Dibuat dengan Streamlit & Plotly | Fokus: interpretasi yang jujur, cepat, dan rapi")