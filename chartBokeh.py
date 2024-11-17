import pandas as pd
import re
from bokeh.plotting import figure, show
from bokeh.io import output_file,

with open("soal_chart_bokeh.txt", "r") as file:
    lines = file.readlines()

timestamps = []
speeds = []
current_timestamp = None

timestamp_pattern = r"Timestamp:\s([\d\-:\s]+)"
speed_pattern = r"sec\s+\d+\.\d+\s+\w+\s+([\d.]+)\s+Mbits/sec"

for line in lines:
    timestamp_match = re.search(timestamp_pattern, line)
    if timestamp_match:
        current_timestamp = timestamp_match.group(1).strip()
        timestamps.append(current_timestamp)


    speed_match = re.search(speed_pattern, line)
    if speed_match and current_timestamp:
        speeds.append({"timestamp": current_timestamp, "speed": float(speed_match.group(1))})

data = pd.DataFrame(speeds)

data['timestamp'] = pd.to_datetime(data['timestamp'])


print("\nData setelah parsing:")
print(data.head())


if data.empty:
    print("Data tidak ditemukan, pastikan file input benar!")
else:
    output_file("network_speed_chart.html")
    p = figure(x_axis_type="datetime", title="Network Speed Test", width=800, height=400)
    p.line(data['timestamp'], data['speed'], line_width=2, color="blue", legend_label="Speed (Mbps)")

    p.xaxis.axis_label = "Date Time"
    p.yaxis.axis_label = "Speed (Mbps)"
    p.legend.location = "top_left"
    p.grid.grid_line_alpha = 0.6

    show(p)