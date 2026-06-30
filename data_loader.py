"""
Fungsi untuk memuat, membersihkan, dan mentransformasi dataset.
"""

import pandas as pd
import numpy as np
import streamlit as st


@st.cache_data(show_spinner=False)
def load_and_clean_data():
    """Muat CSV, bersihkan missing values, filter outlier, dan buat kolom kategori."""
    df = pd.read_csv("dataset.csv")

    critical_cols = [
        "Sleep_Hours", "Hours_Studied", "Stress_Level",
        "Previous_GPA", "Extracurricular_Yes", "Final_Score",
        "Screen_Time", "Diet_Quality", "Work_Life_Balance",
        "Exam_Anxiety_Score",
    ]
    df = df.dropna(subset=critical_cols)

    def iqr_filter(series):
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        return series.clip(lower, upper)

    df["Sleep_Hours"] = iqr_filter(df["Sleep_Hours"])
    df["Hours_Studied"] = iqr_filter(df["Hours_Studied"])

    # Rekonstruksi kolom kategori dari one-hot encoding
    df["Extracurricular"] = df["Extracurricular_Yes"].map({True: "Ya", False: "Tidak"})

    df["Gender"] = df.apply(
        lambda row: "Perempuan" if row.get("Gender_Female", False)
        else "Laki-laki" if row.get("Gender_Male", False)
        else "Non-Biner" if row.get("Gender_Non-Binary", False)
        else "Tidak Diketahui",
        axis=1
    )

    df["Part_Time_Job"] = df.apply(
        lambda row: "Ya" if row.get("Part_Time_Job_Yes", False) else "Tidak",
        axis=1
    )

    def get_study_method(row):
        if row.get("Study_Method_Online", False):
            return "Online"
        elif row.get("Study_Method_Offline", False):
            return "Offline"
        elif row.get("Study_Method_Hybrid", False):
            return "Hybrid"
        return "Lainnya"
    df["Study_Method"] = df.apply(get_study_method, axis=1)

    # Buat kategori tambahan
    df["GPA_Category"] = pd.cut(
        df["Previous_GPA"],
        bins=[0, 2.5, 3.0, 3.5, 4.0],
        labels=["Rendah", "Sedang", "Baik", "Sangat Baik"]
    )

    df["Sleep_Category"] = pd.cut(
        df["Sleep_Hours"],
        bins=[0, 5, 7, 9, 24],
        labels=["Kurang Tidur", "Cukup", "Baik", "Banyak Tidur"]
    )

    return df