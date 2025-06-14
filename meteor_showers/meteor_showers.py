import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
import math

df = pd.read_excel("meteor_showers.xlsx", skiprows=2)

df[['Start Date Raw', 'End Date Raw']] = df['Activity_Period'].str.split('-', expand=True)
df['Start Date Raw'] = df['Start Date Raw'].str.strip()
df['End Date Raw'] = df['End Date Raw'].str.strip()

df['Start Month'] = pd.to_datetime(df['Start Date Raw'], format='%b %d').dt.month
df['End Month'] = pd.to_datetime(df['End Date Raw'], format='%b %d').dt.month

base_year = 2025

def assign_years(row):
    start_month = row['Start Month']
    end_month = row['End Month']
    if start_month > end_month and start_month == 12:
        return base_year - 1, base_year
    elif start_month > end_month:
        return base_year, base_year + 1
    else:
        return base_year, base_year

df[['Start Year', 'End Year']] = df.apply(assign_years, axis=1, result_type='expand')

df['Start Date'] = pd.to_datetime(df['Start Date Raw'] + ' ' + df['Start Year'].astype(str), format='%b %d %Y')
df['End Date'] = pd.to_datetime(df['End Date Raw'] + ' ' + df['End Year'].astype(str), format='%b %d %Y')

df['Maximum_Date'] = df['Maximum_Date'].str.strip() 
df['Maximum_Date_dt'] = pd.to_datetime(df['Maximum_Date'] + f' {base_year}', format='%b %d %Y')

df['Duration (days)'] = (df['End Date'] - df['Start Date']).dt.days + 1

df['Start Date Display'] = df['Start Date'].dt.strftime('%b %d')
df['End Date Display'] = df['End Date'].dt.strftime('%b %d')
df['Maximum_Date_Display'] = df['Maximum_Date_dt'].dt.strftime('%b %d')

df.drop(columns=['Start Date Raw', 'End Date Raw', 'Start Month', 'End Month', 'Start Year', 'End Year', 'Maximum_Date_dt'], inplace=True)

#print(df[['Activity_Period', 'Start Date Display', 'End Date Display', 'Maximum_Date_Display', 'Duration (days)']].head())

input_date_str = input("\nEnter a date (e.g., '2025-07-15'): ")
input_date = pd.to_datetime(input_date_str)

filtered_rows = df[(df['Start Date'] <= input_date) & (df['End Date'] >= input_date)]

if not filtered_rows.empty:
    print(f"\nMeteor showers active on {input_date.strftime('%B %d, %Y')}:")
    for _, row in filtered_rows.iterrows():
        print(f" - {row['Shower']} (Class {row['Class']}, peak: {row['Maximum_Date']}, zenith hourly rate: {row['Max_ZHR']})")
else:
    print(f"\nNo meteor showers are active on {input_date.strftime('%B %d, %Y')}.")
    
class_I = df[df['Class'] == 'I'].copy()
class_I['Maximum_Date_dt'] = pd.to_datetime(class_I['Maximum_Date'] + f' {input_date.year}', format='%b %d %Y', errors='coerce')

future_peaks = class_I[class_I['Maximum_Date_dt'] > input_date]

if not future_peaks.empty:
    next_peak = future_peaks.sort_values('Maximum_Date_dt').iloc[0]
    print(f"\nNext Class I shower peak: {next_peak['Shower']} on {next_peak['Maximum_Date_dt'].strftime('%B %d, %Y')}")
else:
    print("\nNo upcoming Class I shower peaks found after the given date.")    

df = pd.read_excel("meteor_showers.xlsx", skiprows=2)
df[['Start Date Raw', 'End Date Raw']] = df['Activity_Period'].str.split('-', expand=True)
df['Start Date Raw'] = df['Start Date Raw'].str.strip()
df['End Date Raw'] = df['End Date Raw'].str.strip()

df['Start Month'] = pd.to_datetime(df['Start Date Raw'], format='%b %d').dt.month
df['End Month'] = pd.to_datetime(df['End Date Raw'], format='%b %d').dt.month

base_year = 2025

def assign_years(row):
    sm, em = row['Start Month'], row['End Month']
    if sm > em and sm == 12:
        return base_year - 1, base_year
    elif sm > em:
        return base_year, base_year + 1
    else:
        return base_year, base_year

df[['Start Year', 'End Year']] = df.apply(assign_years, axis=1, result_type='expand')
df['Start Date'] = pd.to_datetime(df['Start Date Raw'] + ' ' + df['Start Year'].astype(str), format='%b %d %Y')
df['End Date'] = pd.to_datetime(df['End Date Raw'] + ' ' + df['End Year'].astype(str), format='%b %d %Y')
df['Duration (days)'] = (df['End Date'] - df['Start Date']).dt.days + 1

input_day_of_year = input_date.timetuple().tm_yday
input_angle = 2 * np.pi * (input_day_of_year / 365.25)

selected_class = 'II' # choose between I, II, III and IV
df_class = df[df['Class'] == selected_class].copy()
df_class['Start DOY'] = df_class['Start Date'].dt.dayofyear
df_class['End DOY'] = df_class['End Date'].dt.dayofyear

df_class['Start Angle'] = 2 * np.pi * df_class['Start DOY'] / 365.25
df_class['End Angle'] = 2 * np.pi * df_class['End DOY'] / 365.25

df_class.sort_values('Start Angle', inplace=True)

angle_tolerance = 0.01 
used_ranges_by_radius = []

def is_overlap(new_range, existing_ranges, tol=0.01):
    ns, ne = new_range
    new_segments = []
    if ne < ns:
        new_segments = [(ns, 2 * np.pi), (0, ne)]
    else:
        new_segments = [(ns, ne)]

    for seg_start, seg_end in new_segments:
        for es, ee in existing_ranges:
            if ee < es:
                existing_segments = [(es, 2 * np.pi), (0, ee)]
            else:
                existing_segments = [(es, ee)]
            for eseg_start, eseg_end in existing_segments:
                if not (seg_end + tol < eseg_start or seg_start - tol > eseg_end):
                    return True
    return False

def find_non_overlapping_radius(start_angle, end_angle):
    for radius_index, used_ranges in enumerate(used_ranges_by_radius):
        if not is_overlap((start_angle, end_angle), used_ranges):
            used_ranges.append((start_angle, end_angle))
            return radius_index
    used_ranges_by_radius.append([(start_angle, end_angle)])
    return len(used_ranges_by_radius) - 1

radii = []
for idx, row in df_class.iterrows():
    sa, ea = row['Start Angle'], row['End Angle']
    radius_idx = find_non_overlapping_radius(sa, ea)
    radii.append(1 + radius_idx * 0.2)

df_class['Radius'] = radii

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10, 10))
cmap = colormaps['tab20']

ax.set_thetagrids(np.arange(0, 360, 30), labels=[
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
])

df_class['Maximum_Date_clean'] = df_class['Maximum_Date'].astype(str).str.replace('\xa0', ' ', regex=False).str.strip()
df_class['Maximum_Date_dt'] = pd.to_datetime(df_class['Maximum_Date_clean'] + f' {base_year}', format='%b %d %Y')

for i, row in df_class.iterrows():
    color = cmap(i % 20)
    max_angle = 2 * np.pi * (row['Maximum_Date_dt'].timetuple().tm_yday / 365)

    r_peak = row['Radius'] + 0. 

    if row['End Angle'] < row['Start Angle']:
        theta1 = np.linspace(row['Start Angle'], 2 * np.pi, 50)
        r1 = np.ones_like(theta1) * row['Radius']
        theta2 = np.linspace(0, row['End Angle'], 50)
        r2 = np.ones_like(theta2) * row['Radius']
        ax.plot(theta1, r1, lw=5, color=color)
        ax.plot(theta2, r2, lw=5, color=color, label=row['Shower'])
        ax.plot(max_angle, r_peak, marker='x', color=color, markersize=10, zorder=5)
    else:
        theta = np.linspace(row['Start Angle'], row['End Angle'], 100)
        r = np.ones_like(theta) * row['Radius']
        ax.plot(theta, r, lw=5, color=color, label=row['Shower'])
        ax.plot(max_angle, r_peak, marker='x', color=color, markersize=10, zorder=5)

ax.plot([input_angle, input_angle], [0, max(df_class['Radius']) + 0.2], color='red', linestyle='--', label='Input Date')

ax.set_yticklabels([])
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_title(f'Class {selected_class} Meteor Showers of 2025', fontsize=16)
ax.legend(title='Meteor shower', loc='upper right', bbox_to_anchor=(1.2, 1.05), fontsize=8)

plt.tight_layout()
plt.show()