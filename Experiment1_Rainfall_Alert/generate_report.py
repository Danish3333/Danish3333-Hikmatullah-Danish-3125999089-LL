"""
Generate static outputs for Experiment 1: Rainfall Alert System.
Fetches real-time weather data and saves:
- weather_report.txt — all 5 cities weather summary
- alert_report.txt — alert status for all cities
- weather_data.csv — structured CSV export
"""

import os
import csv
from datetime import datetime
from weather_monitor import fetch_weather, check_alert, get_rainfall_category, CITIES

os.makedirs('outputs', exist_ok=True)

# ---- 1. Fetch all city data ----
print("Fetching weather data for 5 cities...")
all_data = {}
for city in CITIES:
    result = fetch_weather(city)
    if 'error' in result:
        print(f"  {city}: ERROR - {result['error']}")
        all_data[city] = None
    else:
        print(f"  {city}: {result['rainfall']:.1f} mm/h, {result['temperature']:.1f}C, {result['description']}")
        all_data[city] = result

# ---- 2. Generate Weather Report ----
report_lines = []
report_lines.append("=" * 60)
report_lines.append("RAINFALL MONITORING SYSTEM - WEATHER REPORT")
report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report_lines.append("=" * 60)
report_lines.append("")

for city in CITIES:
    data = all_data.get(city)
    if data is None:
        report_lines.append(f"[{city}] DATA UNAVAILABLE")
        continue
    level, status, _ = check_alert(data['rainfall'])
    category = get_rainfall_category(data['rainfall'])
    report_lines.append(f"{'='*60}")
    report_lines.append(f"  CITY: {data['city']}")
    report_lines.append(f"  Timestamp: {data['timestamp']}")
    report_lines.append(f"  Rainfall: {data['rainfall']:.2f} mm/h")
    report_lines.append(f"  Temperature: {data['temperature']:.1f}°C")
    report_lines.append(f"  Humidity: {data['humidity']}%")
    report_lines.append(f"  Condition: {data['description']}")
    report_lines.append(f"  Alert Level: {level} ({status})")
    report_lines.append(f"  CMA Category: {category}")
    report_lines.append("")

with open('outputs/weather_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))
print("\nSaved: outputs/weather_report.txt")

# ---- 3. Generate Alert Summary ----
alert_lines = []
alert_lines.append("=" * 60)
alert_lines.append("ALERT STATUS SUMMARY")
alert_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
alert_lines.append("=" * 60)
alert_lines.append(f"\n{'City':<15} {'Rainfall (mm/h)':>16} {'Alert':>10} {'Status':>10} {'Category':>25}")
alert_lines.append("-" * 80)

for city in CITIES:
    data = all_data.get(city)
    if data is None:
        alert_lines.append(f"{city:<15} {'N/A':>16} {'N/A':>10} {'ERROR':>10}")
        continue
    level, status, _ = check_alert(data['rainfall'])
    category = get_rainfall_category(data['rainfall'])
    alert_lines.append(f"{data['city']:<15} {data['rainfall']:>16.2f} {level:>10} {status:>10} {category:<25}")

alert_lines.append("-" * 80)
red_cities = [c for c in CITIES if all_data.get(c) and check_alert(all_data[c]['rainfall'])[0] == 'Red']
if red_cities:
    alert_lines.append(f"\n  ACTIVE RED ALERTS: {len(red_cities)} city(s) - {', '.join(red_cities)}")
else:
    alert_lines.append("\n  No active Red alerts.")

with open('outputs/alert_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(alert_lines))
print("Saved: outputs/alert_report.txt")

# ---- 4. Generate CSV ----
csv_path = 'outputs/weather_data.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['City', 'Timestamp', 'Rainfall_mmh', 'Temperature_C', 'Humidity_pct', 'Description', 'Alert_Level', 'CMA_Category'])
    for city in CITIES:
        data = all_data.get(city)
        if data is None:
            writer.writerow([city, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'ERROR', '', '', '', '', ''])
            continue
        level, _, _ = check_alert(data['rainfall'])
        category = get_rainfall_category(data['rainfall'])
        writer.writerow([data['city'], data['timestamp'], f"{data['rainfall']:.2f}",
                        f"{data['temperature']:.1f}", data['humidity'],
                        data['description'], level, category])
print("Saved: outputs/weather_data.csv")

print("\n" + "=" * 60)
print("All Experiment 1 outputs generated successfully!")
print(f"Files in outputs/: {os.listdir('outputs')}")