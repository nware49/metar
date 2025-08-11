# METAR Flight Category Scraper

## Overview

This Python script fetches current **METAR** weather data for a list of airports and determines the corresponding **flight categories**—VFR, MVFR, IFR, or LIFR—based on visibility and cloud ceiling information.

It is designed to integrate with an **existing, older control system** that drives a **physical LED-indicated METAR map**. In that setup, each airport location on the map has an LED that changes color to reflect the current flight category.
This script replaces the outdated METAR-fetching logic, supplying fresh and more reliable data to the legacy LED control code.

---

## USAGE

Follow this guide to set up your RPi.

```bash
sudo systemctl daemon-reload
sudo systemctl enable startup.service
sudo systemctl start startup.service
```

If you need to stop the service while doing maintenance, use
```bash 
sudo systemctl stop startup.service
```


## How It Works

1. **Airport Selection**

   * A list of ICAO airport codes is defined in the script (`airports = [...]`).
   * The script can also accept airport codes from the command line:

     ```bash
     python3 metar_scraper.py KCLT KJQF KEQY
     ```

2. **Data Retrieval**

   * Fetches JSON-formatted METAR data from the [Aviation Weather Center API](https://aviationweather.gov/).
   * Only the most recent METAR for each station is processed.

3. **Flight Category Calculation**

   * Categories are determined using FAA criteria:

     * **VFR** – Ceiling > 3000 ft and Visibility > 5 mi
     * **MVFR** – Ceiling 1000–3000 ft or Visibility 3–5 mi
     * **IFR** – Ceiling 500–999 ft or Visibility 1–3 mi
     * **LIFR** – Ceiling < 500 ft or Visibility < 1 mi

4. **Output**

   * Prints a formatted table of airports, names, categories, and basic conditions.
   * Optionally, shows detailed weather data for each station.

5. **Integration with the LED Map**

   * The legacy LED map system expects flight category values per airport.
   * This script can replace the old METAR logic by feeding its `flight_category` results into the LED map control module.
   * No hardware changes are required—only the data source is updated for better accuracy and reliability.

---

## Example Output

```
Fetching METAR data for airports: KCLT, KEQY, KJQF
=====================================================================================
Airport  Name                      Category Vis      Ceiling    Time
-------------------------------------------------------------------------------------
KCLT     Charlotte Douglas Intl    VFR      10.0 mi  5000 ft    08/07 12:52 UTC
KEQY     Charlotte-Monroe Exec     MVFR     4.0 mi   2500 ft    08/07 12:45 UTC
KJQF     Concord-Padgett Regional  IFR      1.5 mi   800 ft     08/07 12:50 UTC
```

---

## Requirements

* Python 3.7+
* Dependencies:

  ```bash
  pip install requests
  ```

---

## Usage

```bash
# Default airports (as defined in the script)
python3 metar_scraper.py

# Custom list from command line
python3 metar_scraper.py KCLT KEQY KJQF

# View detailed weather after summary
python3 metar_scraper.py
# (At the prompt, enter "y")
```

---

## Notes on Integration

* The original LED METAR map code likely uses a hardcoded data fetcher for METARs or decodes raw strings.
* You can adapt this script to:

  * Run periodically (e.g., via cron job).
  * Output just the ICAO code and category in a format the old code expects.
  * Feed results directly into the LED control loop.
* Since the legacy code is “read-only” for the LED hardware, this script’s role is purely to replace the weather-fetching portion.

---

## Future Improvements

* Add FAA-only station support (non-ICAO codes).
* Implement caching to reduce API calls.
* Support color-mapping output directly for LED driver compatibility.
* Add logging for debugging hardware integration.

---