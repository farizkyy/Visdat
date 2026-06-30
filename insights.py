import pandas as pd

from utils import arah_korelasi, fmt

def generate_deep_insights(df):
    insights = []

    corr_sleep_gpa = df["Sleep_Hours"].corr(df["Final_Score"])
    if corr_sleep_gpa > 0.15:
        insights.append((
            f"Korelasi antara jam tidur dan GPA menunjukkan hubungan **{arah_korelasi(corr_sleep_gpa)}** "
            f"(r = {fmt(corr_sleep_gpa)}). Data ini mengindikasikan bahwa manajemen waktu istirahat "
            f"yang berkualitas memiliki peran lebih krusial dalam mendukung performa akademik "
            f"dibandingkan dengan sekadar penambahan jam belajar semata. Mahasiswa yang memperhatikan "
            f"durasi dan kualitas tidur cenderung mencatat capaian GPA yang lebih tinggi.",
            "success"
        ))
    elif corr_sleep_gpa > -0.15:
        insights.append((
            f"Korelasi antara jam tidur dan GPA tergolong **{arah_korelasi(corr_sleep_gpa)}** "
            f"(r = {fmt(corr_sleep_gpa)}). Meskipun tidak menunjukkan hubungan yang signifikan, "
            f"tidur yang cukup tetap menjadi faktor pendukung kesehatan kognitif yang tidak boleh diabaikan.",
            "info"
        ))
    else:
        insights.append((
            f"Korelasi antara jam tidur dan GPA bersifat **{arah_korelasi(corr_sleep_gpa)}** "
            f"(r = {fmt(corr_sleep_gpa)}). Temuan ini menarik: semakin sedikit jam tidur, "
            f"cenderung semakin tinggi GPA. Hal ini mungkin mengindikasikan adanya pola belajar intensif "
            f"yang mengorbankan istirahat, namun perlu diwaspadai risiko burnout jangka panjang.",
            "warning"
        ))

    corr_stress_gpa = df["Stress_Level"].corr(df["Final_Score"])
    if corr_stress_gpa < -0.15:
        insights.append((
            f"Terdapat hubungan **{arah_korelasi(corr_stress_gpa)}** antara tingkat stres dan GPA "
            f"(r = {fmt(corr_stress_gpa)}). Stres akademik yang berlebihan tampaknya berbanding terbalik "
            f"dengan performa belajar. Tekanan yang tidak terkelola dapat menurunkan konsentrasi, "
            f"motivasi, dan daya ingat, yang pada akhirnya memengaruhi hasil studi.",
            "warning"
        ))
    elif corr_stress_gpa > 0.15:
        insights.append((
            f"Terdapat hubungan **{arah_korelasi(corr_stress_gpa)}** antara tingkat stres dan GPA "
            f"(r = {fmt(corr_stress_gpa)}). Temuan ini mengindikasikan bahwa stres dalam tingkat tertentu "
            f"mungkin berfungsi sebagai motivator positif (eustress) yang mendorong mahasiswa untuk lebih giat.",
            "info"
        ))
    else:
        insights.append((
            f"Korelasi antara stres dan GPA tergolong **{arah_korelasi(corr_stress_gpa)}** "
            f"(r = {fmt(corr_stress_gpa)}). Tingkat stres tidak menunjukkan pengaruh langsung yang signifikan "
            f"terhadap capaian akademik dalam kelompok data ini, meskipun tetap perlu dipantau secara berkala.",
            "info"
        ))

    corr_study_gpa = df["Hours_Studied"].corr(df["Final_Score"])
    if corr_study_gpa > 0.15:
        insights.append((
            f"Jam belajar memiliki korelasi **{arah_korelasi(corr_study_gpa)}** dengan GPA "
            f"(r = {fmt(corr_study_gpa)}). Waktu yang diinvestasikan untuk belajar terbukti berkontribusi "
            f"positif terhadap capaian akademik. Namun, penting untuk diingat bahwa efisiensi dan strategi "
            f"belajar tetap menjadi faktor penentu, tidak hanya durasi semata.",
            "success"
        ))
    elif corr_study_gpa < -0.15:
        insights.append((
            f"Jam belajar memiliki korelasi **{arah_korelasi(corr_study_gpa)}** dengan GPA "
            f"(r = {fmt(corr_study_gpa)}). Temuan ini mengindikasikan adanya inefisiensi dalam pola belajar: "
            f"semakin banyak jam belajar, justru semakin rendah GPA. Hal ini menunjukkan perlunya evaluasi "
            f"metode belajar dan manajemen waktu yang lebih efektif.",
            "warning"
        ))
    else:
        insights.append((
            f"Korelasi antara jam belajar dan GPA tergolong **{arah_korelasi(corr_study_gpa)}** "
            f"(r = {fmt(corr_study_gpa)}). Durasi belajar saat ini tidak menunjukkan hubungan yang kuat "
            f"dengan capaian GPA, yang mengindikasikan bahwa faktor lain seperti kualitas tidur, stres, "
            f"atau metode belajar mungkin memiliki pengaruh lebih dominan.",
            "info"
        ))

    corr_sleep_stress = df["Sleep_Hours"].corr(df["Stress_Level"])
    if corr_sleep_stress < -0.15:
        insights.append((
            f"Terdapat hubungan **{arah_korelasi(corr_sleep_stress)}** antara jam tidur dan tingkat stres "
            f"(r = {fmt(corr_sleep_stress)}). Mahasiswa yang tidur lebih lama cenderung mengalami stres "
            f"yang lebih rendah. Kualitas istirahat yang baik berperan sebagai buffer psikologis "
            f"yang membantu mengelola tekanan akademik dengan lebih baik.",
            "success"
        ))
    elif corr_sleep_stress > 0.15:
        insights.append((
            f"Terdapat hubungan **{arah_korelasi(corr_sleep_stress)}** antara jam tidur dan tingkat stres "
            f"(r = {fmt(corr_sleep_stress)}). Temuan ini menunjukkan bahwa mahasiswa dengan jam tidur lebih "
            f"banyak justru cenderung lebih stres, yang mungkin mengindikasikan adanya pola prokrastinasi "
            f"atau gangguan tidur yang perlu ditangani.",
            "warning"
        ))
    else:
        insights.append((
            f"Korelasi antara jam tidur dan stres tergolong **{arah_korelasi(corr_sleep_stress)}** "
            f"(r = {fmt(corr_sleep_stress)}). Tidak terdapat hubungan linear yang signifikan, "
            f"yang menunjukkan bahwa faktor lain di luar durasi tidur mungkin lebih memengaruhi tingkat stres.",
            "info"
        ))

    corr_anxiety_gpa = df["Exam_Anxiety_Score"].corr(df["Final_Score"])
    if corr_anxiety_gpa < -0.15:
        insights.append((
            f"Kecemasan ujian menunjukkan korelasi **{arah_korelasi(corr_anxiety_gpa)}** dengan GPA "
            f"(r = {fmt(corr_anxiety_gpa)}). Kecemasan yang tinggi saat evaluasi akademik dapat mengganggu "
            f"performa optimal mahasiswa. Intervensi berbasis manajemen kecemasan, seperti teknik relaksasi "
            f"dan persiapan sistematis, dapat membantu meningkatkan hasil belajar.",
            "warning"
        ))
    elif corr_anxiety_gpa > 0.15:
        insights.append((
            f"Kecemasan ujian menunjukkan korelasi **{arah_korelasi(corr_anxiety_gpa)}** dengan GPA "
            f"(r = {fmt(corr_anxiety_gpa)}). Secara menarik, kecemasan yang moderat tampaknya berkorelasi "
            f"positif dengan performa, yang mengindikasikan adanya tingkat optimal kecemasan yang mendorong "
            f"kewaspadaan dan persiapan lebih matang.",
            "info"
        ))
    else:
        insights.append((
            f"Korelasi antara kecemasan ujian dan GPA tergolong **{arah_korelasi(corr_anxiety_gpa)}** "
            f"(r = {fmt(corr_anxiety_gpa)}). Kecemasan tidak menunjukkan pengaruh signifikan terhadap "
            f"capaian akademik dalam kelompok data ini, meskipun tetap perlu diperhatikan dari sisi kesehatan mental.",
            "info"
        ))

    return insights

def generate_comparative_analysis(df):
    """
    Analisis Komparatif: membandingkan kelompok mahasiswa.
    Mengembalikan list of tuples: (text, alert_type)
    """
    insights = []

    if "Extracurricular" in df.columns:
        gpa_with = df[df["Extracurricular"] == "Ya"]["Final_Score"].mean()
        gpa_without = df[df["Extracurricular"] == "Tidak"]["Final_Score"].mean()
        count_with = len(df[df["Extracurricular"] == "Ya"])
        count_without = len(df[df["Extracurricular"] == "Tidak"])

        if count_with > 0 and count_without > 0:
            diff = gpa_with - gpa_without
            if diff > 0.1:
                insights.append((
                    f"Mahasiswa yang aktif dalam ekstrakurikuler mencatat rata-rata GPA **{fmt(gpa_with)}**, "
                    f"sedangkan yang tidak aktif mencatat **{fmt(gpa_without)}**. Selisih sebesar {fmt(diff)} "
                    f"poin mengindikasikan bahwa partisipasi dalam organisasi tidak mengganggu akademik, "
                    f"melainkan justru membangun keseimbangan hidup, manajemen waktu, dan soft skills "
                    f"yang berdampak positif pada performa belajar.",
                    "success"
                ))
            elif diff < -0.1:
                insights.append((
                    f"Mahasiswa yang tidak aktif dalam ekstrakurikuler mencatat rata-rata GPA **{fmt(gpa_without)}**, "
                    f"sedangkan yang aktif mencatat **{fmt(gpa_with)}**. Selisih negatif sebesar {fmt(abs(diff))} "
                    f"poin menunjukkan bahwa dalam kelompok data ini, aktivitas ekstrakurikuler mungkin "
                    f"membebani waktu belajar. Namun, perlu dievaluasi apakah hal ini disebabkan oleh "
                    f"overload aktivitas atau kurangnya manajemen waktu.",
                    "warning"
                ))
            else:
                insights.append((
                    f"Tidak terdapat perbedaan GPA yang signifikan antara mahasiswa yang aktif ekstrakurikuler "
                    f"({fmt(gpa_with)}) dan yang tidak aktif ({fmt(gpa_without)}). Hal ini menunjukkan bahwa "
                    f"partisipasi dalam organisasi tidak secara otomatis memengaruhi performa akademik, "
                    f"baik positif maupun negatif. Faktor individual seperti manajemen waktu dan prioritas "
                    f"kemungkinan menjadi penentu utama.",
                    "info"
                ))

    if "Extracurricular" in df.columns:
        stress_with = df[df["Extracurricular"] == "Ya"]["Stress_Level"].mean()
        stress_without = df[df["Extracurricular"] == "Tidak"]["Stress_Level"].mean()
        if not (pd.isna(stress_with) or pd.isna(stress_without)):
            if stress_with > stress_without + 0.1:
                insights.append((
                    f"Mahasiswa yang aktif dalam ekstrakurikuler menunjukkan tingkat stres rata-rata "
                    f"**{fmt(stress_with)}**, lebih tinggi dibandingkan yang tidak aktif (**{fmt(stress_without)}**). "
                    f"Hal ini mengindikasikan bahwa meskipun aktivitas organisasi memiliki manfaat, "
                    f"terdapat risiko beban ganda (dual burden) yang perlu diperhatikan.",
                    "warning"
                ))
            elif stress_with < stress_without - 0.1:
                insights.append((
                    f"Mahasiswa yang aktif dalam ekstrakurikuler justru menunjukkan tingkat stres "
                    f"rata-rata **{fmt(stress_with)}**, lebih rendah dibandingkan yang tidak aktif "
                    f"(**{fmt(stress_without)}**). Aktivitas organisasi tampaknya berfungsi sebagai "
                    f"saluran pelepasan stres dan pembentukan jaringan sosial yang mendukung kesejahteraan.",
                    "success"
                ))
            else:
                insights.append((
                    f"Tingkat stres antara mahasiswa yang aktif ekstrakurikuler ({fmt(stress_with)}) "
                    f"dan yang tidak aktif ({fmt(stress_without)}) relatif seimbang. Partisipasi dalam "
                    f"organisasi tidak secara signifikan memengaruhi tingkat stres dalam kelompok data ini.",
                    "info"
                ))

    high_gpa = df[df["Final_Score"] >= df["Final_Score"].quantile(0.75)]
    low_gpa = df[df["Final_Score"] <= df["Final_Score"].quantile(0.25)]
    if len(high_gpa) > 0 and len(low_gpa) > 0:
        sleep_high = high_gpa["Sleep_Hours"].mean()
        sleep_low = low_gpa["Sleep_Hours"].mean()
        if sleep_high > sleep_low + 0.3:
            insights.append((
                f"Mahasiswa dengan GPA tinggi (kuartil atas) rata-rata tidur **{fmt(sleep_high)} jam**, "
                f"sedangkan mahasiswa dengan GPA rendah (kuartil bawah) rata-rata tidur **{fmt(sleep_low)} jam**. "
                f"Perbedaan ini memperkuat argumen bahwa kualitas istirahat merupakan fondasi penting "
                f"bagi performa kognitif dan konsentrasi belajar.",
                "success"
            ))
        elif sleep_high < sleep_low - 0.3:
            insights.append((
                f"Mahasiswa dengan GPA tinggi (kuartil atas) rata-rata tidur **{fmt(sleep_high)} jam**, "
                f"lebih sedikit dibandingkan mahasiswa dengan GPA rendah (**{fmt(sleep_low)} jam**). "
                f"Temuan ini mengindikasikan adanya pola belajar intensif yang mengorbankan waktu tidur, "
                f"yang meskipun berhasil secara akademik jangka pendek, berpotensi menimbulkan risiko kesehatan.",
                "warning"
            ))
        else:
            insights.append((
                f"Durasi tidur antara mahasiswa dengan GPA tinggi ({fmt(sleep_high)} jam) dan GPA rendah "
                f"({fmt(sleep_low)} jam) relatif serupa. Hal ini menunjukkan bahwa durasi tidur bukanlah "
                f"faktor pembeda utama dalam capaian akademik, dan faktor lain seperti kualitas tidur "
                f"atau metode belajar mungkin lebih relevan.",
                "info"
            ))

    return insights


def generate_strategic_recommendations(df):

    recommendations = []

    avg_stress = df["Stress_Level"].mean()
    avg_sleep = df["Sleep_Hours"].mean()
    avg_gpa = df["Final_Score"].mean()
    corr_sleep_gpa = df["Sleep_Hours"].corr(df["Final_Score"])
    corr_stress_gpa = df["Stress_Level"].corr(df["Final_Score"])
    corr_study_gpa = df["Hours_Studied"].corr(df["Final_Score"])

    if avg_stress > 0.6:
        recommendations.append((
            f"Tingkat stres rata-rata dalam kelompok data ini tergolong tinggi ({fmt(avg_stress)}). "
            f"Direkomendasikan untuk segera mengimplementasikan program kesehatan mental kampus, "
            f"seperti layanan konseling psikologis, workshop manajemen stres, dan kegiatan mindfulness. "
            f"Pihak akademik juga perlu meninjau kembali beban tugas dan jadwal ujian untuk mencegah burnout.",
            "warning"
        ))
    elif avg_stress > 0.4:
        recommendations.append((
            f"Tingkat stres rata-rata dalam kelompok data ini berada pada level moderat ({fmt(avg_stress)}). "
            f"Disarankan untuk menyediakan sesi edukasi tentang teknik coping yang efektif, seperti "
            f"manajemen waktu, relaksasi progresif, dan pengembangan growth mindset. Pencegahan dini "
            f"dapat membantu mencegah eskalasi stres ke level yang berbahaya.",
            "info"
        ))
    else:
        recommendations.append((
            f"Tingkat stres rata-rata dalam kelompok data ini tergolong rendah ({fmt(avg_stress)}), "
            f"yang merupakan kondisi positif. Tetap pertahankan ekosistem kampus yang mendukung "
            f"kesejahteraan mental, dan gunakan momentum ini untuk memperkuat program-program "
            f"pencegahan dan promosi kesehatan mental secara proaktif.",
            "success"
        ))

    if avg_sleep < 5.5:
        recommendations.append((
            f"Rata-rata jam tidur mahasiswa dalam data ini hanya {fmt(avg_sleep)} jam, yang berada "
            f"di bawah rekomendasi kesehatan (7-9 jam). Direkomendasikan kampanye edukasi sleep hygiene, "
            f"penyediaan fasilitas istirahat di kampus, dan kolaborasi dengan layanan kesehatan untuk "
            f"menangani gangguan tidur. Kurang tidur berisiko menurunkan daya ingat, konsentrasi, "
            f"dan daya tahan tubuh.",
            "warning"
        ))
    elif avg_sleep < 6.5:
        recommendations.append((
            f"Rata-rata jam tidur mahasiswa dalam data ini adalah {fmt(avg_sleep)} jam, masih di bawah "
            f"rekomendasi optimal. Disarankan untuk mengadakan seminar tentang pentingnya tidur bagi "
            f"performa akademik, serta memberikan tips praktis manajemen waktu agar mahasiswa dapat "
            f"mengalokasikan waktu istirahat yang cukup tanpa mengorbankan aktivitas belajar.",
            "info"
        ))
    else:
        recommendations.append((
            f"Rata-rata jam tidur mahasiswa dalam data ini adalah {fmt(avg_sleep)} jam, yang sudah "
            f"memenuhi rekomendasi kesehatan. Pertahankan kebiasaan baik ini dan dorong mahasiswa "
            f"untuk tetap konsisten dalam menjadikan tidur sebagai prioritas kesehatan primer.",
            "success"
        ))

    if corr_sleep_gpa > 0.15 and corr_study_gpa < 0.1:
        recommendations.append((
            f"Data menunjukkan bahwa korelasi tidur-GPA ({fmt(corr_sleep_gpa)}) lebih kuat dibandingkan "
            f"korelasi jam belajar-GPA ({fmt(corr_study_gpa)}). Rekomendasi strategis: fokus intervensi "
            f"perlu bergeser dari menambah jam belajar ke meningkatkan kualitas istirahat. Pusat bantuan "
            f"akademik dapat mengintegrasikan edukasi sleep hygiene dalam program mentoring belajar.",
            "info"
        ))
    elif corr_study_gpa > 0.2 and corr_sleep_gpa < 0.1:
        recommendations.append((
            f"Jam belajar menunjukkan hubungan yang cukup bermakna dengan GPA (r = {fmt(corr_study_gpa)}), "
            f"sementara korelasi tidur-GPA relatif lemah. Pusat bantuan akademik disarankan untuk fokus "
            f"memperkuat strategi belajar yang efektif, seperti teknik active recall, spaced repetition, "
            f"dan pembuatan jadwal belajar terstruktur, bukan sekadar menambah durasi belajar.",
            "success"
        ))
    elif corr_stress_gpa < -0.2:
        recommendations.append((
            f"Korelasi negatif yang kuat antara stres dan GPA (r = {fmt(corr_stress_gpa)}) mengindikasikan "
            f"bahwa stres merupakan faktor penghambat utama performa akademik. Intervensi prioritas adalah "
            f"penyediaan layanan kesehatan mental yang mudah diakses, penyesuaian beban tugas, dan "
            f"pengembangan program resiliensi akademik yang berbasis bukti.",
            "warning"
        ))
    else:
        recommendations.append((
            f"Berdasarkan pola korelasi yang teramati, tidak terdapat satu faktor dominan yang secara "
            f"signifikan memengaruhi GPA. Oleh karena itu, intervensi yang paling relevan adalah pendekatan "
            f"holistik yang menyentuh aspek tidur, stres, efisiensi belajar, dan kesejahteraan psikologis "
            f"secara bersamaan untuk keberhasilan akademik jangka panjang.",
            "info"
        ))

    if avg_gpa < 2.5:
        recommendations.append((
            f"Rata-rata GPA kelompok data ini tergolong rendah ({fmt(avg_gpa)}). Diperlukan evaluasi "
            f"mendalam terhadap faktor-faktor penyebab, termasuk kualitas pengajaran, dukungan akademik, "
            f"dan kondisi sosial-ekonomi mahasiswa. Program remedial, tutoring peer-to-peer, dan "
            f"peningkatan akses sumber daya belajar perlu dipercepat.",
            "warning"
        ))
    elif avg_gpa > 3.5:
        recommendations.append((
            f"Rata-rata GPA kelompok data ini tergolong tinggi ({fmt(avg_gpa)}). Gunakan data ini "
            f"sebagai benchmark untuk mengidentifikasi praktik-praktik terbaik yang dapat direplikasi. "
            f"Dokumentasikan pola gaya hidup dan strategi belajar mahasiswa berprestasi sebagai "
            f"model bagi mahasiswa lain.",
            "success"
        ))

    return recommendations