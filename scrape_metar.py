#!/usr/bin/env python3
"""
METAR Flight Category Scraper
Fetches METAR data from aviationweather.gov and determines flight categories
"""

import requests
import json
from typing import Dict, List, Optional
import sys
from datetime import datetime


class METARScraper:
    def __init__(self):
        self.base_url = "https://aviationweather.gov/api/data/metar"

    def get_metar_data(self, airport_codes: List[str], hours: int = 1) -> Dict:
        """
        Fetch METAR data for given airport codes

        Args:
            airport_codes: List of 4-letter airport codes (e.g., ['KJFK', 'KLAX'])
            hours: How many hours back to fetch data (default: 1)

        Returns:
            Dictionary with airport codes as keys and METAR data as values
        """
        # Convert airport codes to comma-separated string
        ids = ','.join(airport_codes)

        params = {
            'ids': ids,
            'format': 'json',
            'taf': 'false',
            'hours': hours
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            # Parse JSON response
            data = response.json()

            # Process METAR data
            metar_data = {}
            for metar in data:
                if metar.get('mostRecent') == 1:  # Only get most recent data
                    station_id = metar.get('icaoId')
                    if station_id:
                        # Extract visibility in statute miles
                        visibility = self._parse_visibility(metar.get('visib'))

                        # Extract ceiling from clouds data
                        ceiling = self._parse_ceiling(metar.get('clouds', []))

                        # Calculate flight category
                        flight_category = self._calculate_flight_category(visibility, ceiling)

                        metar_data[station_id] = {
                            'raw_text': metar.get('rawOb', 'N/A'),
                            'flight_category': flight_category,
                            'visibility_mi': visibility,
                            'ceiling_ft': ceiling,
                            'temp': metar.get('temp'),
                            'dewp': metar.get('dewp'),
                            'wind_dir': metar.get('wdir'),
                            'wind_speed': metar.get('wspd'),
                            'altimeter': metar.get('altim'),
                            'report_time': metar.get('reportTime'),
                            'station_name': metar.get('name', 'Unknown')
                        }

            return metar_data

        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return {}

    def _parse_visibility(self, visib_str: str) -> float:
        """Parse visibility string to numeric value in statute miles"""
        if not visib_str:
            return 99.0  # Default high visibility

        visib_str = str(visib_str).strip()

        # Handle "10+" case
        if visib_str == "10+":
            return 10.0

        # Handle numeric values
        try:
            return float(visib_str)
        except ValueError:
            # Handle fractions like "1/2", "3/4", etc.
            if '/' in visib_str:
                parts = visib_str.split('/')
                if len(parts) == 2:
                    try:
                        return float(parts[0]) / float(parts[1])
                    except ValueError:
                        pass
            return 10.0  # Default if can't parse

    def _parse_ceiling(self, clouds: List[Dict]) -> Optional[int]:
        """Extract ceiling height from clouds data"""
        if not clouds:
            return None

        # Look for overcast (OVC) or broken (BKN) layers
        for cloud in clouds:
            cover = cloud.get('cover', '').upper()
            if cover in ['OVC', 'BKN'] and cloud.get('base') is not None:
                return int(cloud.get('base'))

        return None  # No ceiling found

    def _calculate_flight_category(self, visibility: float, ceiling: Optional[int]) -> str:
        """
        Calculate flight category based on visibility and ceiling

        Flight Categories:
        - VFR: Ceiling > 3000 ft AND Visibility > 5 mi
        - MVFR: Ceiling 1000-3000 ft OR Visibility 3-5 mi
        - IFR: Ceiling 500-999 ft OR Visibility 1-3 mi
        - LIFR: Ceiling < 500 ft OR Visibility < 1 mi
        """
        # Use high ceiling if no ceiling reported (clear skies)
        ceiling_ft = ceiling if ceiling is not None else 9999

        if ceiling_ft < 500 or visibility < 1:
            return 'LIFR'
        elif ceiling_ft < 1000 or visibility < 3:
            return 'IFR'
        elif ceiling_ft <= 3000 or visibility <= 5:
            return 'MVFR'
        else:
            return 'VFR'

    def print_flight_categories(self, metar_data: Dict):
        """Print formatted flight category information"""
        if not metar_data:
            print("No METAR data available")
            return

        print(f"{'Airport':<8} {'Name':<25} {'Category':<8} {'Vis':<8} {'Ceiling':<10} {'Time':<16}")
        print("-" * 85)

        for airport, data in metar_data.items():
            visibility = f"{data['visibility_mi']:.1f} mi" if data['visibility_mi'] else "N/A"
            ceiling = f"{data['ceiling_ft']} ft" if data['ceiling_ft'] else "Clear"

            # Format report time
            report_time = data.get('report_time', '')
            if report_time:
                try:
                    dt = datetime.fromisoformat(report_time.replace('Z', '+00:00'))
                    time_str = dt.strftime('%m/%d %H:%M UTC')
                except:
                    time_str = report_time[:16]  # Fallback
            else:
                time_str = 'N/A'

            # Truncate station name if too long
            station_name = data.get('station_name', 'Unknown')[:24]

            print(
                f"{airport:<8} {station_name:<25} {data['flight_category']:<8} {visibility:<8} {ceiling:<10} {time_str:<16}")

        print(f"\nFlight Categories:")
        print("VFR  = Visual Flight Rules (Ceiling > 3000 ft AND Visibility > 5 mi)")
        print("MVFR = Marginal VFR (Ceiling 1000-3000 ft OR Visibility 3-5 mi)")
        print("IFR  = Instrument Flight Rules (Ceiling 500-999 ft OR Visibility 1-3 mi)")
        print("LIFR = Low IFR (Ceiling < 500 ft OR Visibility < 1 mi)")

    def print_detailed_weather(self, metar_data: Dict):
        """Print detailed weather information"""
        print(f"\nDetailed Weather Information:")
        print("=" * 50)

        for airport, data in metar_data.items():
            print(f"\n{airport} - {data.get('station_name', 'Unknown')}")
            print(f"Flight Category: {data['flight_category']}")
            print(f"Temperature: {data.get('temp', 'N/A')}°C")
            print(f"Dewpoint: {data.get('dewp', 'N/A')}°C")

            if data.get('wind_dir') and data.get('wind_speed'):
                print(f"Wind: {data['wind_dir']}° at {data['wind_speed']} kts")

            if data.get('altimeter'):
                print(f"Altimeter: {data['altimeter']:.2f} inHg")

            print(f"Raw METAR: {data['raw_text']}")


def main():
    """Main function to run the METAR scraper"""
    # Example airport codes - modify as needed
    airports = [
        # Massachusetts
        'KBOS',  # BOS – Logan International Airport (Boston)
        'KHYA',  # HYA – Barnstable (Cape Cod Gateway)
        'KACK',  # ACK – Nantucket Memorial Airport
        'KMVY',  # MVY – Martha’s Vineyard Airport
        'KORH',  # ORH – Worcester Regional Airport
        'KBED',  # BED – Hanscom Field
        'KEWB',  # EWB – New Bedford Regional Airport
        'KPVC',  # PVC – Provincetown Municipal Airport
        'KBVY',  # BVY – Beverly Regional Airport
        'KLWM',  # LWM – Lawrence Municipal Airport
        'KOWD',  # OWD – Norwood Memorial Airport

        # Connecticut
        'KBDL',  # BDL – Bradley International Airport
        'KHVN',  # HVN – Tweed-New Haven Airport
        'KDXR',  # DXR – Danbury Municipal Airport
        'KHFD',  # HFD – Hartford-Brainard Airport
        'KBDR',  # BDR – Sikorsky Memorial (Bridgeport)
        'KLZD',  # LZD – Danielson Airport
        'KGON',  # GON – Groton–New London Airport
        'KMMK',  # MMK – Meriden Markham Municipal Airport
        'KOXC',  # OXC – Waterbury-Oxford Airport
        'KIJD',  # IJD – Windham Airport
        'KSNC',  # SNC – Chester Airport

        # New Hampshire
        'KMHT',  # MHT – Manchester-Boston Regional Airport
        'KPSM',  # PSM – Portsmouth International at Pease
        'KLEB',  # LEB – Lebanon Municipal Airport
        'KASH',  # ASH – Boire Field (Nashua reliever)
        'KBML',  # BML – Berlin Regional Airport
        'KCNH',  # CNH – Claremont Municipal Airport
        'KCON',  # CON – Concord Municipal Airport
        'KAFN',  # AFN – Jaffrey/Silver Ranch Airport
        'KEEN',  # EEN – Dillant-Hopkins Airport (Keene)
        'KLCI',  # LCI – Laconia Municipal Airport
        'KDAW',  # DAW – Skyhaven Airport (Rochester)
        'KHIE',  # HIE – Mount Washington Regional Airport

        # Vermont
        'KBTV',  # BTV – Burlington International Airport
        'KRUT',  # RUT – Rutland–Southern Vermont Regional Airport
        'KMPV',  # MPV – Edward F. Knapp State Airport (Barre/Montpelier)
        'KDDH',  # DDH – William H. Morse State Airport (Bennington)
        'KFSO',  # FSO – Franklin County State Airport (Highgate)
        'KCDA',  # CDA – Caledonia County Airport (Lyndonville)
        # (Note: Middlebury State Airport [FAA 6B0], Warren-Sugarbush [0B7], etc., have FAA codes only)
        'KMVL',  # MVL – Morrisville–Stowe State Airport
        'KEFK',  # EFK – Northeast Kingdom International Airport (Newport)
        'KVSF',  # VSF – Hartness State (Springfield) Airport
    ]

    # airports = [
    #     'KCLT',  # Charlotte Douglas International Airport
    #     'KEQY',  # Charlotte-Monroe Executive Airport
    #     'KJQF',  # Concord-Padgett Regional Airport
    #     'KRUQ',  # Mid-Carolina Regional Airport (Salisbury)
    #     'KAKH',  # Gastonia Municipal Airport
    #     'KIPJ',  # Lincolnton-Lincoln County Regional Airport
    #     'KMRN',  # Foothills Regional Airport (Morganton)
    #     'KVUJ',  # Stanly County Airport (Albemarle)
    #     'KAFP',  # Anson County Airport (Wadesboro)
    #     'KSRW',  # Rowan County Airport
    #     'KEHO',  # Shelby-Cleveland County Regional Airport
    #     'KRCZ',  # Rockingham-Hamlet Airport
    #     'KASN',  # Anson County Airport (duplicate name used elsewhere)
    #     'KHBI',  # Asheboro Regional Airport
    #     'KLKR',  # Lancaster County Airport (McWhirter Field)
    #     'KUDG',  # Darlington County Jetport
    #     'KCQW',  # Cheraw Municipal Airport
    #     'KIXA',  # Halifax-Northampton Regional Airport
    #     'KIPF',  # Pecan Plantation Airport (note: far small field)
    #     'KEXX',  # Davidson County Airport (Lexington, NC)
    # ]

    airports = [
        'KPOU',  # Poughkeepsie, NY
        'KDXR',  # Danbury, CT
        'KHVN',  # New Haven, CT
        'KGON',  # Groton-New London, CT
        'KBID',  # Block Island, RI
        'KMVY',  # Martha's Vineyard, MA
        'KHYA',  # Hyannis, MA
        'KACK',  # Nantucket, MA
        'KPVC',  # Provincetown, MA
        'KPYM',  # Plymouth, MA
        'KEWB',  # New Bedford, MA
        'KPVD',  # Providence, RI
        'KIJD',  # Windham, CT
        'KBDL',  # Bradley Intl, CT
        'KBAF',  # Westfield-Barnes, MA
        'KCEF',  # Chicopee Falls, MA
        'KAQW',  # Whitman, NY
        'KPSF',  # Pittsfield, MA
        'KALB',  # Albany, NY
        'KGFL',  # Glens Falls, NY
        'KVSF',  # Springfield, VT
        'KEEN',  # Keene, NH
        'KORE',  # Orange, MA
        'KORH',  # Worcester, MA
        'KFIT',  # Fitchburg, MA
        'KASH',  # Nashua, NH
        'KCON',  # Concord, NH
        'KLCI',  # Laconia, NH
        'KSFM',  # Sanford, ME
        'KPSM',  # Portsmouth, NH
        'KBED',  # Bedford, MA
        'KBOS',  # Boston Logan, MA
        'KOWD',  # Norwood, MA
    ]    # You can also get airports from command line arguments
    if len(sys.argv) > 1:
        airports = [arg.upper() for arg in sys.argv[1:]]

    scraper = METARScraper()

    print(f"Fetching METAR data for airports: {', '.join(airports)}")
    print("=" * 85)

    metar_data = scraper.get_metar_data(airports)

    if metar_data:
        scraper.print_flight_categories(metar_data)

        # Ask if user wants detailed information
        try:
            show_details = input(f"\nShow detailed weather information? (y/n): ").lower().strip()
            if show_details in ['y', 'yes']:
                scraper.print_detailed_weather(metar_data)
        except KeyboardInterrupt:
            print(f"\nExiting...")
    else:
        print("No data retrieved. Please check airport codes and try again.")


if __name__ == "__main__":
    main()