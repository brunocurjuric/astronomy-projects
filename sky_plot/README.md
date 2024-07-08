## Sky Plot

#### Info
This notebook shows how sky looks like on a given date and location (latitude and longitude) together with the ecliptic line - pathway of the sun. Location and date can be given by deafult, or can be obtained by input. If you want to input either location or date, just comment the row where variable is declared or write yours. Slider can be used to simulate urban areas (with the increment of 0.5).

Stars are taken from SIMBAD database where stars up to 6.5th visual magnitude are given. There are no deep sky objects shown.

<br>

#### How to get star data
In order to obtain .tsv files (tab-separated values), go to https://simbad.cds.unistra.fr/simbad/sim-fsam and enter a search expression in ADQL language:

```sql
Vmag < 6.5
```

Return option (right side) should be changed to display (maximum 10000 objects).

Before submitting the query, be sure that in Output options tab you ticked Identifier (main identifier), Object type (short abbreviation + display all types), Coordinates 1 (ICRS, J200 epoch, decimal) and Fluxes/Magnitudes (V). Output format should be ASCII (tab-separator) and file output should be chosen. It may take up to several minutes.

<br>

#### Future
Future updates will include ecliptic line toggle on/off, constellation lines (also with toggle on/off), as well as rotating sky feature. It will also feature when the night begins on a given date. Moreover, information about rising and setting times of planets will be given. For a given latitude, circumpolar stars and constellations will be displayed.