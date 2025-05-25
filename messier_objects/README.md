## Messier marathon

### Description

`messier_marathon.py` calculates how many Messier objects are visible from a given location on a specific date. Currently, only *astronomical nights* are considered—periods when the Sun is more than 18° below the horizon. It also includes Moon illumination data to help assess the quality of observing conditions.


This script uses Astropy and astroplan packages, which can be installed via:
```console
pip install astropy astroplan
```


### Roadmap

Planned features for upcoming releases:

- 🌐 **Equatorial Coordinate Map**  
A sky chart showing all Messier objects with RA/Dec grid overlays.

- 🌃 **Night Sky Visualisation**  
  Dynamic sky plots indicating which Messier objects are visible throughout the night.

- 📅 **Annual Visibility Chart**  
  A graph displaying the number of visible Messier objects per night across the year, including corresponding Moon illumination.

- 🔍 **Optimal Date Finder**  
  Automatically selects the best night for a Messier marathon based on object visibility and Moon phase for a given time interval.

- 🗂️ **Observation Strategy Guide**  
  Step-by-step observing order to maximise found objects within the night (early evening → dawn progression).

- 🧠 **Interactive Quiz Mode**  
  A learning module with:
    - Guess the object based on its Messier number (and vice versa)
    - Guess the object’s type from its Messier number
    - Identify the object based on its position in the sky
    - Identify the object from an image (only for nebulae and galaxies)
    - Match each object to its corresponding constellation

- ⚙️ **Command-line Interface Enhancements**  
  Easily set observation parameters using CLI flags (e.g. `--lat`, `--lon`, `--date`, `--quiz-mode`).

- 🌗 **Custom Night Start Definition**  
  Option to choose when visibility begins—civil, nautical, astronomical twilight, or full night—based on observer preference.

### How to Run

You can run the script directly from the command line:

```bash
python3 messier_marathon.py
```