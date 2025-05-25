import pandas as pd
from astropy.coordinates import Angle, SkyCoord, AltAz, get_sun, EarthLocation
from astropy.time import Time
import astropy.units as u
import numpy as np
import sys
import astroplan

table = pd.read_excel('messier_objects.xlsx', index_col=None)

table['RA_deg'] = table['RA'].apply(lambda x: Angle(x, unit=u.hourangle).degree)
table['Dec_clean'] = table['Dec'].apply(
    lambda x: x.replace('°', 'd').replace('′', "'").replace('″', '"') if pd.notnull(x) else x
)
table['Dec_deg'] = table['Dec_clean'].apply(
    lambda x: Angle(x, unit=u.deg).degree if pd.notnull(x) and x.strip() else None
)

latitude = 45.829
longitude = 15.979

if -90 <= latitude <= 90:
    pass
else:
    print("Invalid value for latitude. Latitude must be between -90 and 90 degrees.")
    sys.exit()
if -180 < longitude <= 180:
    pass
else:
    print("Invalid value for longitude. longitude must be between -180 and 180 degrees.")
    sys.exit()

observation_time = Time("2025-5-25 00:00:00", scale='utc')
hgt = 349
offset_hours = 0
utcoffset = offset_hours*u.hour 
loc = EarthLocation(lat=latitude*u.deg, lon=longitude*u.deg, height=hgt*u.m)
midnight = observation_time - utcoffset
delta_midnight = np.linspace(-12, 12, 1000)*u.hour
times = midnight + delta_midnight

sun_altaz = get_sun(times).transform_to(AltAz(obstime=times, location=loc))
sun_down = sun_altaz.alt < -18 * u.deg

if sun_down.sum()  == 0:
    print("No astronomical night for this date - no Messier objects visible!")
    sys.exit()

visible_objects = []
not_visible_objects = []

for i, row in table.iterrows():
    obj_coord = SkyCoord(ra=row['RA_deg'] * u.deg, dec=row['Dec_deg'] * u.deg)
    obj_altaz = obj_coord.transform_to(AltAz(obstime=times, location=loc))
    obj_up = obj_altaz.alt > 0 * u.deg
    visible = sun_down & obj_up

    if np.any(visible):
        visible_objects.append(row['Name'])
    else:
        not_visible_objects.append(row['Name'])

print(f"✅ Visible: {', '.join(visible_objects)}")
print(f"❌ Not visible: {', '.join(not_visible_objects)}")

print(f"\n🌌 Total Messier objects visible during the night of {observation_time.strftime('%Y/%m/%d')}: {len(visible_objects)} / {len(table)}")

moon_illumination = astroplan.moon_illumination(observation_time)*100
print(f"The Moon is {moon_illumination:.2f}% illuminated.")