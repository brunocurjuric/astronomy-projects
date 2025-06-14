# Meteor showers

## Overview

This project provides detailed information about meteor showers occurring in 2025. By entering a date, you can quickly find which meteor showers are active on that day, along with their peak dates and zenithal hourly rate (ZHR) — a measure of meteor activity intensity. It also produces polar plot of given class of meteor showers over a year with indicated peaks.

Meteor showers are categorised into four classes based on their visibility and activity level:
- Class I (Major) – The most prominent showers, easily observable, best viewed after midnight.

- Class II (Minor) – Moderate activity, typically 2 to 10 meteors per hour at peak.

- Class III (Variable) – Rarely strong activity; usually low rates (~1 meteor per night). Best observed during evening hours.

- Class IV (Weak) – Generally low meteor counts, rarely exceeding 2 meteors per hour.

The data is sourced from the International Meteor Organization (IMO) and Masahiro Koseki’s meteor shower calendar, ensuring accuracy and reliability.


## How to run
Simply run the script with Python in terminal:
```bash
python3 meteor_showers.py
```
You will be prompted to enter a date, after which the active meteor showers for that date will be displayed.

After that polar plot of meteor shower for specific class will be laid out. You can choose which class you want to plot by modifying line 96:
```python
selected_class = 'II' # choose between I, II, III and IV
```

## Future enchancements
Planned upgrades include:
- Sky map with radiant points plotted in equatorial coordinates
- Night sky simulation for given date, incorporating stars and meteor shower radiants
- Moon phase and illumination integration to better predict viewing conditions
