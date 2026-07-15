def arah_korelasi(corr):
    if corr > 0.3:
        return "positif kuat"
    elif corr > 0.1:
        return "positif sedang"
    elif corr > -0.1:
        return "lemah / tidak berarti"
    elif corr > -0.3:
        return "negatif sedang"
    else:
        return "negatif kuat"


LABEL_MAP = {
    "Sleep_Hours": "Jam Tidur",
    "Stress_Level": "Tingkat Stres",
    "Hours_Studied": "Jam Belajar",
    "Screen_Time": "Waktu Layar",
    "Diet_Quality": "Kualitas Diet",
    "Previous_GPA": "GPA",
    "Final_Score": "Nilai Akhir",
    "Work_Life_Balance": "Keseimbangan Hidup",
    "Exam_Anxiety_Score": "Kecemasan Ujian",
    "Attendance": "Kehadiran",
    "Age": "Usia",
}


def fmt(val, decimals=2):
    return f"{val:.{decimals}f}"