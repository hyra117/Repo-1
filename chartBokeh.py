import pandas as pd
import re
from bokeh.plotting import figure, show
from bokeh.io import output_file, output_notebook

# Baca file sebagai teks mentah
with open("soal_chart_bokeh.txt", "r") as file:
    lines = file.readlines()

# Ekstraksi data dengan RegEx
timestamps = []
speeds = []
current_timestamp = None

# Pola untuk menangkap timestamp dan kecepatan
timestamp_pattern = r"Timestamp:\s([\d\-:\s]+)"
speed_pattern = r"sec\s+\d+\.\d+\s+\w+\s+([\d.]+)\s+Mbits/sec"

for line in lines:
    # Cari timestamp
    timestamp_match = re.search(timestamp_pattern, line)
    if timestamp_match:
        current_timestamp = timestamp_match.group(1).strip()
        timestamps.append(current_timestamp)  # Tambahkan timestamp ke daftar

    # Cari speed
    speed_match = re.search(speed_pattern, line)
    if speed_match and current_timestamp:
        speeds.append({"timestamp": current_timestamp, "speed": float(speed_match.group(1))})

# Buat DataFrame dari hasil parsing
data = pd.DataFrame(speeds)

# Konversi kolom timestamp ke format datetime
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Tampilkan beberapa baris data untuk verifikasi
print("\nData setelah parsing:")
print(data.head())

# Pastikan data tidak kosong
if data.empty:
    print("Data tidak ditemukan, pastikan file input benar!")
else:
    # Buat grafik dengan Bokeh
    output_file("network_speed_chart.html")  # Atau gunakan output_notebook() untuk Jupyter
    p = figure(x_axis_type="datetime", title="Network Speed Test", width=800, height=400)
    p.line(data['timestamp'], data['speed'], line_width=2, color="blue", legend_label="Speed (Mbps)")

    p.xaxis.axis_label = "Date Time"
    p.yaxis.axis_label = "Speed (Mbps)"
    p.legend.location = "top_left"
    p.grid.grid_line_alpha = 0.6

    # Menampilkan grafik
    show(p)

    # Alternatif untuk Jupyter Notebooks (gunakan hanya jika di Jupyter):
    # output_notebook()
    # show(p)
