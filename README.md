# Dashboard Gaya Hidup & Performa Akademik Mahasiswa (Visdat)

Aplikasi web interaktif berbasis **Streamlit** dan **Plotly** yang dikembangkan untuk menganalisis hubungan antara pola hidup harian mahasiswa (*durasi tidur, tingkat stres, jam belajar, waktu layar, kecemasan ujian, serta status kerja paruh waktu*) terhadap performa akademik (*GPA / Nilai Akhir*).

---

##  Deskripsi Proyek

Dashboard ini menyajikan eksplorasi data visualisasi interaktif yang dilengkapi dengan analisis statistik dan interpretasi strategis otomatis. Berdasarkan data survei gaya hidup mahasiswa, dashboard ini membantu mengidentifikasi pola kebiasaan mahasiswa berprestasi tinggi (*High Performing Students*) dibanding mahasiswa yang membutuhkan intervensi akademik.

### Fitur Utama
* **KPI Metrics Real-time**: Menampilkan ringkasan rata-rata Nilai Akhir (GPA), Jam Tidur, Jam Belajar, Tingkat Stres, dan Kecemasan Ujian.
* **Filter Sidebar Interaktif**: Menyaring dataset secara dinamis berdasarkan rentang GPA, Tingkat Stres, dan Jam Tidur.
* **Fitur Ekspor Data**: Mengunduh dataset hasil penyaringan ke dalam format CSV.
* **Visualisasi Data Interaktif (Plotly)**: 8 jenis diagram dinamis dengan tooltip lengkap dan zoom interaktif.
* **Insight & Rekomendasi Otomatis**: Generator analisis berbasis aturan (*rule-based insight*) untuk memberikan interpretasi mendalam, analisis komparatif, dan saran strategis.

---

## Visualisasi & Chart yang Tersedia

Visualisasi dikelompokkan ke dalam **3 Tab Utama**:

### 1. Tab Performa Akademik
* **Scatter Plot (Jam Belajar vs Nilai Akhir)**: Memetakan jam belajar terhadap nilai akhir dengan gradasi warna tingkat stres (`scatter_study_gpa`).
* **Histogram & Marginal Box Plot**: Distribusi frekuensi nilai akhir berdasarkan kategori GPA (*Rendah, Sedang, Baik, Sangat Baik*) dilengkapi *box plot* di bagian atas (`hist_gpa_distribution`).

### 2. Tab Pola Hidup & Kesejahteraan
* **Horizontal Bar Chart (Kategori Jam Tidur)**: Distribusi jumlah mahasiswa berdasarkan kecukupan jam tidur harian (`pie_sleep_category`).
* **Bubble Chart (Tidur, Stres, & Work-Life Balance)**: Visualisasi 4D (Jam Tidur, Tingkat Stres, Work-Life Balance sebagai ukuran gelembung, dan Nilai Akhir sebagai warna) (`bubble_sleep_stress_gpa`).
* **Violin Plot (Kecemasan Ujian vs Kerja Paruh Waktu)**: Perbandingan bentuk distribusi kecemasan ujian mahasiswa yang bekerja paruh waktu vs tidak bekerja (`violin_anxiety_job`).

### 3. Tab Profil Mahasiswa
* **Radar / Spider Chart (Profil Mahasiswa 5D)**: Perbandingan pola 5 dimensi (*Tidur, Stres, Belajar, Screen Time, Kecemasan*) antara kelompok mahasiswa GPA Tinggi vs GPA Rendah (`radar_profile`).
* **Heatmap Korelasi Lengkap**: Matriks korelasi Pearson 9x9 antar seluruh variabel numerik (`heatmap_correlation`).

---

##  Struktur Proyek

```text
C:\xampp\htdocs\visdat\
├── .streamlit/                     # Konfigurasi tema Streamlit
├── .venv/                          # Virtual Environment Python
├── dataset.csv                     # File dataset survei mahasiswa yang sudah cleaning
|-- student_performance_finalscore  # File dataset survei mahasiswa yang mentah
├── config.py                       # Konfigurasi halaman, skema warna, dan CSS kustom
├── data_loader.py                  # Script pemuat, pembersih, dan pra-pemrosesan data
├── charts.py                       # Modul pembuat chart interaktif (Plotly)
├── insights.py                     # Generator narasi insight dan rekomendasi strategis
├── utils.py                        # Fungsi pembantu (mapping label, format penulisan)
├── main.py                         # File aplikasi utama (Streamlit entrypoint)
├── requirements.txt                # Daftar pustaka/dependensi Python
└── README.md                       # Dokumentasi proyek
```

---

## Prasyarat Sistem

Sebelum menjalankan aplikasi, pastikan sistem Anda memenuhi kebutuhan berikut:
* **Python**: Versi 3.9 atau yang lebih baru.
* **Browser**: Google Chrome, Mozilla Firefox, Microsoft Edge, atau browser modern lainnya.

---

## Panduan Instalasi

1. **Buka Terminal / Command Prompt**:
   Masuk ke direktori proyek XAMPP Anda:
   ```bash
   cd C:\xampp\htdocs\visdat
   ```

2. **Buat Virtual Environment (Opsional tetapi Disarankan)**:
   ```bash
   python -m venv .venv
   ```

3. **Aktifkan Virtual Environment**:
   * **Windows (PowerShell)**:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   * **Windows (CMD)**:
     ```cmd
     .\.venv\Scripts\activate.bat
     ```

4. **Install Dependensi Proyek**:
   Jalankan perintah berikut untuk menginstall seluruh paket yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```
   *Atau install secara manual:*
   ```bash
   pip install streamlit pandas numpy plotly
   ```

---

## Cara Jalankan Aplikasi

1. Pastikan Virtual Environment telah aktif di direktori `C:\xampp\htdocs\visdat`.
2. Jalankan perintah Streamlit berikut:
   ```bash
   streamlit run main.py
   ```
3. Aplikasi akan secara otomatis terbuka di browser default Anda pada alamat:
   ```text
   Local URL:  http://localhost:8501
   Network URL: http://<ip-lokal-anda>:8501
   ```

---

## Petunjuk Penggunaan Dashboard

1. **Filter Data**: Gunakan panel **Opsi Filter** di sebelah kiri (sidebar) untuk menyesuaikan rentang GPA, Tingkat Stres, dan Jam Tidur.
2. **Eksplorasi Chart**: Gunakan kursor mouse untuk melihat detail nilai (*hover tooltip*), *zoom*, *pan*, atau *download chart sebagai PNG* via toolbar Plotly di pojok kanan atas setiap grafik.
3. **Ekspor CSV**: Klik tombol **Download Data (CSV)** di sidebar untuk menyimpan data yang sudah tersaring.
4. **Analisis Naratif**: Buka bagian **Insight dan Analisis Strategis** di Tab 1 untuk membaca interpretasi mendalam dan rekomendasi otomatis.

---

## Lisensi & Kredit

* **Framework UI**: [Streamlit](https://streamlit.io/)
* **Engine Visualisasi**: [Plotly Express & Graph Objects](https://plotly.com/python/)
* **Pengolah Data**: [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)
* **Pengembang**: Arya / Tim Visdat (Praktikum Visualisasi Data)
