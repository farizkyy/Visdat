import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from config import COLORS, CHART_COLORSCALE, HEATMAP_COLORSCALE
from utils import LABEL_MAP, fmt

def _apply_standard_layout(fig, height=None):
    """Terapkan standar visual premium ke figure."""
    layout_updates = dict(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color=COLORS["text_main"]),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            title_font=dict(size=14),
            tickfont=dict(size=12),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            title_font=dict(size=14),
            tickfont=dict(size=12),
        ),
    )
    if height:
        layout_updates["height"] = height
    fig.update_layout(**layout_updates)
    return fig

def scatter_study_gpa(df):
    fig = px.scatter(
        df,
        x="Hours_Studied",
        y="Final_Score",
        color="Stress_Level",
        color_continuous_scale=CHART_COLORSCALE,
        opacity=0.8,
        labels={
            "Hours_Studied": "Jam Belajar (normalisasi)",
            "Final_Score": "Nilai Akhir",
            "Stress_Level": "Tingkat Stres",
        },
        height=500,
    )
    fig.update_traces(
        marker=dict(size=10, line=dict(width=1, color="white")),
        hovertemplate=(
            "<b>Jam Belajar:</b> %{x:.2f}<br>"
            "<b>Nilai Akhir:</b> %{y:.2f}<br>"
            "<b>Tingkat Stres:</b> %{marker.color:.2f}<extra></extra>"
        ),
    )

    z = np.polyfit(df["Hours_Studied"].dropna(), df["Final_Score"].dropna(), 1)
    p = np.poly1d(z)
    x_line = np.linspace(df["Hours_Studied"].min(), df["Hours_Studied"].max(), 100)
    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=p(x_line),
            mode="lines",
            name="Tren",
            line=dict(color=COLORS["accent2"], width=2.5, dash="dash"),
            hovertemplate="<b>Tren:</b> y = " + f"{z[0]:.2f}x + {z[1]:.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        hovermode="closest",
        coloraxis_colorbar=dict(
            title=dict(text="Stres", side="right"),
            tickformat=".2f",
            len=0.8,
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig = _apply_standard_layout(fig)
    return fig

def box_extracurricular_gpa(df):
    fig = go.Figure()

    categories = df["Extracurricular"].unique()
    neon_colors = ["#00FFFF", "#00FF00"]

    for i, cat in enumerate(categories):
        subset = df[df["Extracurricular"] == cat]
        color = neon_colors[i % len(neon_colors)]
        rgb_fill = f"rgba(0, 255, 255, 0.12)" if "Tidak" in cat else f"rgba(0, 255, 0, 0.12)"

        fig.add_trace(
            go.Box(
                y=subset["Final_Score"],
                name=cat,
                marker_color=color,
                boxpoints=False,
                line=dict(color=color, width=3),
                fillcolor=rgb_fill,
                hovertemplate=(
                    f"<b>{cat}</b><br>"
                    "Kuartil 1: %{q1:.2f}<br>"
                    "Median: %{median:.2f}<br>"
                    "Kuartil 3: %{q3:.2f}<extra></extra>"
                ),
            )
        )

        fig.add_trace(
            go.Scatter(
                y=subset["Final_Score"],
                x=[cat] * len(subset),
                mode="markers",
                marker=dict(
                    color=color,
                    size=7,
                    opacity=0.5,
                    line=dict(color=color, width=1),
                ),
                name=f"{cat} (data)",
                hovertemplate=f"<b>{cat}</b><br>Final_Score: %{{y:.2f}}<extra></extra>",
                showlegend=False,
            )
        )

    fig.update_layout(
        xaxis_title="Ekstrakurikuler",
        yaxis_title="Final_Score",
        hovermode="closest",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            categoryorder="array",
            categoryarray=["Tidak", "Ya"],
            title_standoff=15,
            title_font=dict(size=14),
            tickfont=dict(size=12),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            title_standoff=10,
            title_font=dict(size=14),
            tickfont=dict(size=12),
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500,
    )
    fig = _apply_standard_layout(fig, height=500)
    return fig

def heatmap_correlation(df, cols):
    corr_matrix = df[cols].corr()
    corr_matrix_id = corr_matrix.rename(columns=LABEL_MAP, index=LABEL_MAP)

    fig = go.Figure(
        data=go.Heatmap(
            z=corr_matrix_id.values,
            x=corr_matrix_id.columns,
            y=corr_matrix_id.columns,
            colorscale=HEATMAP_COLORSCALE,
            zmin=-1,
            zmax=1,
            text=np.round(corr_matrix_id.values, 2),
            texttemplate="%{text}",
            textfont={"size": 11, "family": "Inter, sans-serif", "color": "white"},
            hovertemplate="<b>%{x}</b> ↔ <b>%{y}</b><br>Korelasi: %{z:.2f}<extra></extra>",
            colorbar=dict(
                title="Korelasi",
                thickness=15,
                len=0.8,
                tickformat=".1f",
            ),
        )
    )
    fig.update_layout(
        height=600,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=11)),
        yaxis=dict(showgrid=False, zeroline=False, autorange="reversed", tickfont=dict(size=11)),
    )
    fig = _apply_standard_layout(fig)
    return fig

def hist_gpa_distribution(df):
    fig = px.histogram(
        df,
        x="Final_Score",
        color="GPA_Category",
        color_discrete_sequence=[COLORS["accent2"], COLORS["accent4"], COLORS["accent"], COLORS["accent3"]],
        labels={"Final_Score": "Final_Score", "count": "Jumlah Mahasiswa"},
        opacity=0.85,
        nbins=30,
        marginal="box",
        height=500,
    )
    fig.update_traces(
        marker=dict(line=dict(width=1, color="white")),
        hovertemplate="<b>Final Score:</b> %{x:.2f}<br><b>Jumlah:</b> %{y}<extra></extra>",
    )
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(showgrid=False, zeroline=False, title_font=dict(size=14), tickfont=dict(size=12)),
        legend=dict(title="Kategori GPA", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        bargap=0.05,
    )
    fig = _apply_standard_layout(fig)
    return fig

def bubble_sleep_stress_gpa(df):
    fig = px.scatter(
        df,
        x="Sleep_Hours",
        y="Stress_Level",
        size="Work_Life_Balance",
        color="Final_Score",
        color_continuous_scale=CHART_COLORSCALE,
        hover_data=["Screen_Time"],
        labels={
            "Sleep_Hours": "Jam Tidur",
            "Stress_Level": "Tingkat Stres",
            "Work_Life_Balance": "Work-Life Balance",
            "Final_Score": "Nilai Akhir",
            "Screen_Time": "Waktu Layar",
        },
        height=500,
    )
    fig.update_traces(
        marker=dict(opacity=0.75, line=dict(width=1, color="white")),
        hovertemplate=(
            "<b>Jam Tidur:</b> %{x:.1f}<br>"
            "<b>Tingkat Stres:</b> %{y:.2f}<br>"
            "<b>Final_Score:</b> %{marker.color:.2f}<br>"
            "<b>Work-Life Balance:</b> %{marker.size:.2f}<br>"
            "<b>Waktu Layar:</b> %{customdata[0]:.2f}<extra></extra>"
        ),
    )
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(showgrid=False, zeroline=False, title_font=dict(size=14), tickfont=dict(size=12)),
        coloraxis_colorbar=dict(title=dict(text="Nilai Akhir", side="right"), tickformat=".2f"),
    )
    fig = _apply_standard_layout(fig)
    return fig

def bar_gpa_by_gender_study(df):
    avg = df.groupby(["Gender", "Study_Method"], observed=True)["Final_Score"].mean().reset_index()

    fig = px.bar(
        avg,
        x="Study_Method",
        y="Final_Score",
        color="Gender",
        barmode="group",
        color_discrete_sequence=[COLORS["accent"], COLORS["accent2"], COLORS["accent4"], COLORS["accent3"]],
        labels={"Study_Method": "Metode Belajar", "Final_Score": "Rata-rata GPA"},
        height=450,
    )
    fig.update_traces(
        marker=dict(line=dict(width=1, color="white")),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "<b>Gender:</b> %{fullData.name}<br>"
            "<b>Rata-rata GPA:</b> %{y:.2f}<extra></extra>"
        ),
    )
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(showgrid=False, zeroline=False, range=[0, 4.2], title_font=dict(size=14), tickfont=dict(size=12)),
        legend=dict(title="Gender", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig = _apply_standard_layout(fig)
    return fig

def violin_anxiety_job(df):
    fig = go.Figure()

    categories = df["Part_Time_Job"].unique()
    colors = [COLORS["accent3"], COLORS["accent2"]]

    for i, cat in enumerate(categories):
        subset = df[df["Part_Time_Job"] == cat]
        color = colors[i % len(colors)]
        rgb = f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.2)"

        fig.add_trace(
            go.Violin(
                y=subset["Exam_Anxiety_Score"],
                name=cat,
                box_visible=True,
                meanline_visible=True,
                line_color=color,
                fillcolor=rgb,
                opacity=0.6,
                points="all",
                jitter=0.05,
                pointpos=-0.3,
                marker=dict(size=5, opacity=0.5, color=color),
                hovertemplate=f"<b>{cat}</b><br>Kecemasan: %{{y:.2f}}<extra></extra>",
            )
        )

    fig.update_layout(
        xaxis_title="Kerja Paruh Waktu",
        yaxis_title="Skor Kecemasan Ujian",
        xaxis=dict(showgrid=False, zeroline=False, title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(showgrid=False, zeroline=False, title_font=dict(size=14), tickfont=dict(size=12)),
        showlegend=False,
        height=450,
    )
    fig = _apply_standard_layout(fig)
    return fig

def radar_profile(df):
    # Tentukan threshold
    gpa_median = df["Final_Score"].median()
    high = df[df["Final_Score"] >= gpa_median]
    low = df[df["Final_Score"] < gpa_median]

    dimensions = ["Sleep_Hours", "Stress_Level", "Hours_Studied", "Screen_Time", "Exam_Anxiety_Score"]
    labels = ["Jam Tidur", "Stres", "Jam Belajar", "Waktu Layar", "Kecemasan"]

    def normalize(series):
        return (series - series.min()) / (series.max() - series.min())

    fig = go.Figure()

    for name, subset, color in [
        ("GPA Tinggi", high, COLORS["accent"]),
        ("GPA Rendah", low, COLORS["accent2"]),
    ]:
        values = [normalize(subset[d]).mean() for d in dimensions]
        values += [values[0]]
        rgb = f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.2)"

        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=labels + [labels[0]],
                fill="toself",
                name=name,
                line=dict(color=color, width=2.5),
                fillcolor=rgb,
                hovertemplate=f"<b>{name}</b><br>%{{theta}}: %{{r:.2f}}<extra></extra>",
            )
        )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                showline=False,
                gridcolor="rgba(226, 232, 240, 0.3)",
                tickfont=dict(size=10),
            ),
            angularaxis=dict(
                gridcolor="rgba(226, 232, 240, 0.3)",
                tickfont=dict(size=12),
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=40, b=40),
        height=500,
    )
    fig = _apply_standard_layout(fig)
    return fig

def pie_sleep_category(df):
    counts = df["Sleep_Category"].value_counts().reset_index()
    counts.columns = ["Kategori", "Jumlah"]

    fig = px.pie(
        counts,
        names="Kategori",
        values="Jumlah",
        color="Kategori",
        color_discrete_sequence=[COLORS["accent2"], COLORS["accent"], COLORS["accent3"], COLORS["accent4"]],
        hole=0.5,
        height=400,
    )
    fig.update_traces(
        textinfo="percent+label",
        textfont=dict(size=11, family="Inter, sans-serif"),
        hovertemplate="<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}<extra></extra>",
        marker=dict(line=dict(color="white", width=2)),
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
    )
    fig = _apply_standard_layout(fig)
    return fig

def bar_diet_quality_gpa(df):
    avg = df.groupby("Diet_Quality", observed=True)["Final_Score"].agg(["mean", "std", "count"]).reset_index()
    avg.columns = ["Kualitas Diet", "Rata-rata GPA", "Std Dev", "Jumlah"]

    fig = px.bar(
        avg,
        x="Kualitas Diet",
        y="Rata-rata GPA",
        error_y="Std Dev",
        text="Jumlah",
        color="Rata-rata GPA",
        color_continuous_scale=CHART_COLORSCALE,
        labels={"Kualitas Diet": "Kualitas Diet (0-2)", "Rata-rata GPA": "Rata-rata GPA"},
        height=420,
    )
    fig.update_traces(
        texttemplate="n=%{text}",
        textposition="outside",
        marker=dict(line=dict(width=1, color="white")),
        hovertemplate=(
            "<b>Kualitas Diet %{x}</b><br>"
            "Rata-rata GPA: %{y:.2f}<br>"
            "Jumlah: %{text}<extra></extra>"
        ),
    )
    fig.update_layout(
        coloraxis_showscale=False,
        xaxis=dict(showgrid=False, zeroline=False, dtick=1, title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(showgrid=False, zeroline=False, range=[0, 4.2], title_font=dict(size=14), tickfont=dict(size=12)),
    )
    _apply_standard_layout(fig)
    return fig