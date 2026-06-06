# Sky Plot

## Info

This Jupyter notebook visualises how the night sky appears on a selected date and location (latitude, longitude and height). It includes:

- The ecliptic line (path of the Sun across the sky throughout the year)
- The circumpolar stars boundary (stars that never set from selected location)
- Rising and setting times for the planets
- Durations of twilight phases and astronomical night
- A slider to simulate visibility in urban areas by adjusting limiting magnitude (in 0.5 steps)

You can either use the default values for date and location or modify the variables manually. To input your own values, comment out or replace the default variable assignment lines.

The displayed stars are pulled from the SIMBAD database, including stars with a visual magnitude (Vmag) up to 6.5, which are typically visible to the naked eye under perfect conditions.

## 📥 How to Get Star Data

To download the required `.tsv` (tab-separated values) file of visible stars from SIMBAD:

1. Visit: [SIMBAD FSAM](https://simbad.cds.unistra.fr/simbad/sim-fsam)

2. In the ADQL query input box, enter:
   ```sql
   Vmag < 6.5
3. On the right side, change the result limit to 10,000 objects (maximum allowed).

4. Click on the *Output options* tab and make sure the following fields are selected:
    
    Output format - ASCII (tab-separator) and ✅ **file output**

    ✅ **Identifier** (Main identifier)

    ✅ **Object type** (Short abbreviation + Display all types)

    ✅ **Coordinates 1** (ICRS, J2000 epoch, decimal format)

    ✅ **Fluxes/Magnitudes** (V magnitude)

5. Click SAVE and return to the previous page.
6. Click SUBMIT to run the query (after the query is completed, the file will be automatically downloaded). The whole process may take a few minutes.


## Planned features

Future updates will include:
- 👁️ Toggle options for ecliptic line, boundary for circumpolar stars, constellation lines
- 🔄 Sky rotation - animate star positions as they move through the night
- 🌁 Atmospheric extinction – simulate the air mass and magnitude change depending on the altitude
- 🌓 Dark mode – black/blue background with star colors based on surface temperature
- 🪐 Solar system view – plot current positions of planets around the Sun in the ecliptic plane
- 🌌 Deep sky objects - Messier objects as well as other objects of interest will be shown
- 🌍 Exoplanet host stars – highlight naked-eye stars known to host confirmed exoplanets 
- 🌠 Stellar streams & moving groups – highlight naked-eye stars that belong to common-origin stellar populations
