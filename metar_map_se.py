#!/usr/bin/env python3
"""
Simple Aviation Weather Map using NeoPixel library
Displays flight categories on NeoPixel LEDs using aviationweather.gov API
This is the Southeast version
"""

import requests
import json
import time
import board
import neopixel
from typing import Dict, List, Optional


class WeatherMap:
    def __init__(self, led_count=50):
        """Initialize the weather map with NeoPixel configuration"""
        self.led_count = led_count
        self.api_url = "https://aviationweather.gov/api/data/metar"

        # Initialize NeoPixel strip
        self.pixels = neopixel.NeoPixel(board.D18, led_count, brightness=0.3, auto_write=False)

        # Airport to LED mapping - Southeast airports from jakecam file
        self.airport_mapping = {
            'KMXF': 0,   # Maxwell AFB, AL
            'KALX': 2,   # Thomas C. Russell Field, AL
            'KAUO': 3,   # Auburn University Regional, AL
            'KCSG': 4,   # Columbus, GA
            'KLGC': 6,   # LaGrange-Callaway, GA
            'KCCO': 7,   # Newnan-Coweta County, GA
            'KCTJ': 8,   # West Georgia Regional, GA
            'KCNI': 10,  # Cherokee County, SC
            'KRYY': 11,  # Cobb County-McCollum Field, GA
            'KATL': 12,  # Hartsfield-Jackson Atlanta Intl, GA
            'KHMP': 13,  # Hampton-Varnville, SC
            'K6A2': 14,  # Griffin-Spalding County, GA
            'KOPN': 15,  # Thomasville-Regional, GA
            'K6A1': 16,  # Moultrie Municipal, GA
            'KWRB': 18,  # Robins AFB, GA
            'KDBN': 19,  # W.H. 'Bud' Barron, GA
            'KSBO': 20,  # Saluda County, SC
            'KHQU': 22,  # Thomson-McDuffie County, GA
            'KMLJ': 24,  # Baldwin County, GA
            'KCVC': 26,  # Covington Municipal, GA
            'KLZU': 27,  # Gwinnett County-Briscoe Field, GA
            'KAHN': 28,  # Athens-Ben Epps, GA
            '18AA': 29,  # Preston Area Community, GA
            'KGMU': 31,  # Gainesville Regional, GA
            'KCEU': 33,  # Clemson-Oconee County, SC
            'KAJR': 35,  # Habersham County, GA
            'KDZJ': 36,  # Blairsville, GA
            'KDNN': 38,  # Dalton Regional, GA
            'KRMG': 40,  # Richard B. Russell Regional, GA
            'K4A6': 42,  # Toccoa-R.G. LeTourneau Field, GA
            'KGAD': 44,  # Gadsden Municipal, AL
            'KASN': 45,  # Talladega Municipal, AL
        }

        # Color mapping for flight categories (G, R, B) - corrected from original
        self.colors = {
            'VFR': (255, 0, 0),     # Green
            'MVFR': (0, 0, 255),    # Blue
            'IFR': (0, 255, 0),     # Red
            'LIFR': (0, 255, 255),  # Magenta
            'UNKNOWN': (64, 64, 64) # Dim white for errors
        }

    def startup_sequence(self):
        """Run LED startup sequence to test all colors"""
        print("Running startup sequence...")

        # Test all LEDs with different colors
        test_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

        for color in test_colors:
            self.pixels.fill(color)
            self.pixels.show()
            time.sleep(0.5)

        # Clear all LEDs
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        print("Startup sequence complete")

    def get_weather_data(self, airport_codes: List[str]) -> Dict:
        """
        Fetch METAR data for all airports in one API call

        Args:
            airport_codes: List of airport codes

        Returns:
            Dictionary with airport codes as keys and weather data as values
        """
        # Convert to comma-separated string for API
        ids = ','.join(airport_codes)

        params = {
            'ids': ids,
            'format': 'json',
            'taf': 'false',
            'hours': 2  # Get data from last 2 hours
        }

        try:
            print(f"Fetching weather data for {len(airport_codes)} airports...")
            response = requests.get(self.api_url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()
            weather_data = {}

            # Process each METAR report
            for metar in data:
                if metar.get('mostRecent') == 1:  # Only most recent data
                    station_id = metar.get('icaoId')
                    if station_id:
                        # Calculate flight category
                        visibility = self._parse_visibility(metar.get('visib'))
                        ceiling = self._parse_ceiling(metar.get('clouds', []))
                        flight_category = self._calculate_flight_category(visibility, ceiling)

                        weather_data[station_id] = {
                            'flight_category': flight_category,
                            'visibility_mi': visibility,
                            'ceiling_ft': ceiling,
                            'temp': metar.get('temp'),
                            'wind_speed': metar.get('wspd'),
                            'report_time': metar.get('reportTime')
                        }

            print(f"Successfully retrieved data for {len(weather_data)} airports")
            return weather_data

        except requests.RequestException as e:
            print(f"API request failed: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"JSON parsing failed: {e}")
            return {}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {}

    def _parse_visibility(self, visib_str: str) -> float:
        """Parse visibility string to numeric value"""
        if not visib_str:
            return 10.0

        visib_str = str(visib_str).strip()

        if visib_str == "10+":
            return 10.0

        try:
            return float(visib_str)
        except ValueError:
            if '/' in visib_str:
                parts = visib_str.split('/')
                if len(parts) == 2:
                    try:
                        return float(parts[0]) / float(parts[1])
                    except ValueError:
                        pass
            return 10.0

    def _parse_ceiling(self, clouds: List[Dict]) -> Optional[int]:
        """Extract ceiling from clouds data"""
        if not clouds:
            return None

        for cloud in clouds:
            cover = cloud.get('cover', '').upper()
            if cover in ['OVC', 'BKN'] and cloud.get('base') is not None:
                return int(cloud.get('base'))

        return None

    def _calculate_flight_category(self, visibility: float, ceiling: Optional[int]) -> str:
        """Calculate flight category based on visibility and ceiling"""
        ceiling_ft = ceiling if ceiling is not None else 9999

        if ceiling_ft < 500 or visibility < 1:
            return 'LIFR'
        elif ceiling_ft < 1000 or visibility < 3:
            return 'IFR'
        elif ceiling_ft <= 3000 or visibility <= 5:
            return 'MVFR'
        else:
            return 'VFR'

    def update_leds(self, weather_data: Dict):
        """Update LEDs based on weather data"""
        print("Updating LEDs...")

        # Clear all LEDs first
        self.pixels.fill((0, 0, 0))

        updated_count = 0
        for airport, led_index in self.airport_mapping.items():
            if airport in weather_data:
                flight_category = weather_data[airport]['flight_category']
                color = self.colors.get(flight_category, self.colors['UNKNOWN'])

                try:
                    self.pixels[led_index] = color
                    updated_count += 1
                    print(f"{airport} (LED {led_index}): {flight_category}")
                except (IndexError, Exception) as e:
                    print(f"Warning: Could not set LED {led_index} for {airport}: {e}")
            else:
                # No data available - set to dim color
                try:
                    self.pixels[led_index] = self.colors['UNKNOWN']
                    print(f"{airport} (LED {led_index}): NO DATA")
                except (IndexError, Exception) as e:
                    print(f"Warning: Could not set LED {led_index} for {airport}: {e}")

        # Update physical LEDs
        self.pixels.show()
        print(f"Updated {updated_count} LEDs with weather data")

    def print_status(self, weather_data: Dict, loop_count: int):
        """Print current status"""
        print(f"\n=== Weather Update #{loop_count} ===")
        print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Count categories
        categories = {}
        for data in weather_data.values():
            cat = data['flight_category']
            categories[cat] = categories.get(cat, 0) + 1

        print(f"Flight Categories: {dict(categories)}")
        print(f"Total airports: {len(weather_data)}")

    def run_continuous(self, update_interval_minutes=5):
        """Run continuous weather monitoring loop"""
        print("Starting NeoPixel Weather Map - Southeast Version")
        print(f"Monitoring {len(self.airport_mapping)} airports")
        print(f"Update interval: {update_interval_minutes} minutes")

        # Run startup sequence
        self.startup_sequence()

        loop_count = 0

        try:
            while True:
                loop_count += 1

                # Get all airport codes
                airports = list(self.airport_mapping.keys())

                # Fetch weather data
                weather_data = self.get_weather_data(airports)

                if weather_data:
                    # Update LEDs
                    self.update_leds(weather_data)

                    # Print status
                    self.print_status(weather_data, loop_count)
                else:
                    print("No weather data received - keeping previous state")

                # Sleep until next update
                sleep_seconds = update_interval_minutes * 60
                print(f"\nSleeping for {update_interval_minutes} minutes...")
                time.sleep(sleep_seconds)

        except KeyboardInterrupt:
            print("\nShutdown requested...")
            self.pixels.fill((0, 0, 0))  # Turn off all LEDs
            self.pixels.show()
            print("All LEDs turned off. Goodbye!")


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='Aviation Weather Map - Southeast')
    parser.add_argument('--led-count', type=int, default=50,
                        help='Number of LEDs')
    parser.add_argument('--update-interval', type=int, default=5,
                        help='Update interval in minutes')

    args = parser.parse_args()

    try:
        # Create weather map instance
        weather_map = WeatherMap(args.led_count)

        # Run continuous monitoring
        weather_map.run_continuous(update_interval_minutes=args.update_interval)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to run with: sudo /path/to/venv/bin/python metar_map_se.py")


if __name__ == "__main__":
    main()