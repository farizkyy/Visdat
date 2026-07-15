import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from config import COLORS, CHART_COLORSCALE, HEATMAP_COLORSCALE
from utils import LABEL_MAP, fmt


def _apply_standard_layout(fig, height=None):

    chart_text = "#E2E8F0"  # light slate
    chart_tick = "#F8FAFC"  # hampir putih

    layout_updates = dict(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color=chart_text),
        margin=dict(l=20, r=20, t=40, b=20),
        title_font=dict(color=chart_text),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            title_font=dict(size=14, color=chart_tick),
            tickfont=dict(size=12, color=chart_text),
            color=chart_tick,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            title_font=dict(size=14, color=chart_tick),
            tickfont=dict(size=12, color=chart_text),
            color=chart_tick,
        ),
    )

    if height:
        layout_updates["height"] = height

    title = getattr(fig.layout, "title", None)
    if title is not None:
        try:
            t = title.text
            if t is None or str(t).strip().lower() in {"none", "undefined"}:
                fig.update_layout(title="")
        except Exception:
            pass

    annotations = getattr(fig.layout, "annotations", None)
    if annotations:
        for a in annotations:
            try:
                txt = a.get("text") if isinstance(a, dict) else getattr(a, "text", None)
                if txt is None or str(txt).strip().lower() in {"none", "undefined"}:
                    if isinstance(a, dict):
                        a["text"] = ""
                    else:
                        a.text = ""
            except Exception:
                continue

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
            textfont={"size": 11, "family": "Inter, sans-serif"},

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
        category_orders={"GPA_Category": ["Rendah", "Sedang", "Baik", "Sangat Baik"]},
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

    gpa_median = df["Final_Score"].median()
    high = df[df["Final_Score"] >= gpa_median]
    low = df[df["Final_Score"] < gpa_median]
    
    dimensions = [
        "Sleep_Hours",
        "Stress_Level",
        "Hours_Studied",
        "Screen_Time",
        "Exam_Anxiety_Score",
    ]
    labels = ["Jam Tidur", "Stres", "Jam Belajar", "Waktu Layar", "Kecemasan"]
    units = ["jam", "skor", "jam", "jam", "skor"]

    mins = {d: float(df[d].min()) for d in dimensions}
    maxs = {d: float(df[d].max()) for d in dimensions}
    ranges = {d: (maxs[d] - mins[d]) for d in dimensions}

    def norm_value(x: float, d: str) -> float:
        r = ranges[d]
        if r == 0:
            return 0.0
        return (x - mins[d]) / r

    def group_stats(subset, d: str) -> tuple[float, float]:
        raw_mean = float(subset[d].mean())
        norm_mean = float(norm_value(raw_mean, d))
        return raw_mean, norm_mean

    fig = go.Figure()

    for name, subset, color in [
        ("GPA Tinggi", high, COLORS["accent"]),
        ("GPA Rendah", low, COLORS["accent2"]),
    ]:
        raw_means = [group_stats(subset, d)[0] for d in dimensions]
        norm_means = [group_stats(subset, d)[1] for d in dimensions]

        r_vals = norm_means + [norm_means[0]]
        theta_vals = labels + [labels[0]]

        raw_cycle = raw_means + [raw_means[0]]
        units_cycle = units + [units[0]]

        rgb = (
            f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.2)"
        )

        custom = list(zip(raw_cycle, units_cycle))

        fig.add_trace(
            go.Scatterpolar(
                r=r_vals,
                theta=theta_vals,
                fill="toself",
                name=name,
                line=dict(color=color, width=2.5),
                fillcolor=rgb,
                customdata=custom,
                hovertemplate=(
                    f"<b>{name}</b><br>"
                    "%{theta}<br>"
                    "Normalisasi (0..1): %{r:.2f}<br>"
                    "Nilai asli: %{customdata[0]:.2f} %{customdata[1]}<extra></extra>"
                ),
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
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(l=40, r=40, t=40, b=40),
        height=500,
        annotations=[
            dict(
                text=(
                    "<b>Catatan:</b> Radar memakai <i>normalisasi 0..1</i> untuk semua metrik agar bias satuan (jam vs skor) hilang. "
                    "Bentuk polygon adalah pola relatif. Nilai asli per metrik tersedia di hover (rata-rata kelompok)."
                ),
                x=0.5,
                y=-0.12,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=11, color=COLORS["text_muted"]),
            )
        ],
    )

    fig = _apply_standard_layout(fig)
    return fig


def pie_sleep_category(df):
    # NOTE: nama fungsi dipertahankan agar kompatibel dengan `main.py`.
    order = ["Kurang Tidur", "Cukup", "Baik", "Banyak Tidur"]

    counts = (
        df["Sleep_Category"]
        .value_counts()
        .reindex(order)
        .fillna(0)
        .reset_index()
    )
    counts.columns = ["Sleep_Category", "Jumlah"]

    fig = px.bar(
        counts,
        x="Jumlah",
        y="Sleep_Category",
        orientation="h",
        color="Sleep_Category",
        color_discrete_sequence=[COLORS["accent2"], COLORS["accent"], COLORS["accent3"], COLORS["accent4"]],
        labels={"Jumlah": "Jumlah Mahasiswa", "Sleep_Category": "Kategori Jam Tidur"},
        height=420,
    )

    fig.update_traces(
        texttemplate="%{x}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Jumlah: %{x}<extra></extra>",
        marker=dict(line=dict(width=1, color="white")),
        textfont={},
    )


    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(showgrid=False, zeroline=False, title_font=dict(size=14), tickfont=dict(size=12)),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    fig = _apply_standard_layout(fig)
    return fig


def bar_diet_quality_gpa(df):
    # NOTE: nama fungsi dipertahankan agar kompatibel dengan `main.py`.
    categories = sorted(df["Diet_Quality"].dropna().unique())
    neon_colors = [COLORS["accent2"], COLORS["accent"], COLORS["accent4"], COLORS["accent3"]]

    fig = go.Figure()

    for i, cat in enumerate(categories):
        subset = df[df["Diet_Quality"] == cat]
        color = neon_colors[i % len(neon_colors)]
        fig.add_trace(
            go.Box(
                x=[str(cat)] * len(subset),
                y=subset["Final_Score"],
                name=f"{cat}",
                marker_color=color,
                boxpoints=False,
                line=dict(color=color, width=2),
                fillcolor=f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.15)",
                hovertemplate=(
                    f"<b>Kualitas Diet:</b> {cat}<br>"
                    "<b>Nilai Akhir:</b> %{y:.2f}<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        height=420,
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
        showlegend=False,
        boxmode="group",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    fig = _apply_standard_layout(fig)
    return fig