#!/usr/bin/env python3
"""
Simple Aviation Weather Map using NeoPixel library
Displays flight categories on NeoPixel LEDs using aviationweather.gov API
This is the Southeast version with WiFi connectivity monitoring
"""

import requests
import json
import time
import board
import neopixel
import subprocess
import socket
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
            'UNKNOWN': (64, 64, 64), # Dim white for errors
            'WIFI_ERROR': (0, 255, 0)  # Red for WiFi errors
        }

        # WiFi connectivity tracking
        self.wifi_connected = True
        self.consecutive_failures = 0
        self.max_failures_before_flash = 2

    def check_wifi_connectivity(self) -> bool:
        """
        Check WiFi connectivity using multiple methods
        Returns True if connected, False otherwise
        """
        # Method 1: Check if we can reach a reliable DNS server
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except (socket.timeout, OSError):
            pass

        # Method 2: Try to reach the weather API host
        try:
            socket.create_connection(("aviationweather.gov", 443), timeout=5)
            return True
        except (socket.timeout, OSError):
            pass

        # Method 3: Check wireless interface status (Linux specific)
        try:
            result = subprocess.run(['iwconfig'], capture_output=True, text=True, timeout=5)
            if 'ESSID:' in result.stdout and 'off/any' not in result.stdout:
                # Interface shows connected to a network, but network might not have internet
                # This method is less reliable, so we only use it as a last resort
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        return False

    def flash_wifi_error(self, duration_seconds=10):
        """
        Flash all LEDs red to indicate WiFi connectivity issues
        
        Args:
            duration_seconds: How long to flash the LEDs
        """
        print("WiFi connectivity lost - flashing red warning...")
        
        flash_cycles = duration_seconds * 2  # 2 flashes per second
        
        for i in range(flash_cycles):
            if i % 2 == 0:
                # Turn on red
                self.pixels.fill(self.colors['WIFI_ERROR'])
            else:
                # Turn off
                self.pixels.fill((0, 0, 0))
            
            self.pixels.show()
            time.sleep(0.5)
        
        # Clear LEDs after flashing
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

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
        print(f"WiFi Status: {'Connected' if self.wifi_connected else 'Disconnected'}")
        
        if not self.wifi_connected:
            print(f"Consecutive failures: {self.consecutive_failures}")

        # Count categories
        categories = {}
        for data in weather_data.values():
            cat = data['flight_category']
            categories[cat] = categories.get(cat, 0) + 1

        print(f"Flight Categories: {dict(categories)}")
        print(f"Total airports: {len(weather_data)}")

    def run_continuous(self, update_interval_minutes=5, wifi_check_enabled=True):
        """
        Run continuous weather monitoring loop
        
        Args:
            update_interval_minutes: Minutes between weather updates
            wifi_check_enabled: Whether to check WiFi connectivity
        """
        print("Starting NeoPixel Weather Map - Southeast Version")
        print(f"Monitoring {len(self.airport_mapping)} airports")
        print(f"Update interval: {update_interval_minutes} minutes")
        print(f"WiFi monitoring: {'Enabled' if wifi_check_enabled else 'Disabled'}")

        # Run startup sequence
        self.startup_sequence()

        loop_count = 0

        try:
            while True:
                loop_count += 1

                # Check WiFi connectivity if enabled
                if wifi_check_enabled:
                    print("Checking WiFi connectivity...")
                    self.wifi_connected = self.check_wifi_connectivity()
                    
                    if not self.wifi_connected:
                        self.consecutive_failures += 1
                        print(f"WiFi connectivity check failed (attempt {self.consecutive_failures})")
                        
                        if self.consecutive_failures >= self.max_failures_before_flash:
                            self.flash_wifi_error(duration_seconds=10)
                            print("Waiting 30 seconds before retrying...")
                            time.sleep(30)
                            continue
                    else:
                        if self.consecutive_failures > 0:
                            print("WiFi connectivity restored!")
                        self.consecutive_failures = 0

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
    parser.add_argument('--disable-wifi-check', action='store_true',
                        help='Disable WiFi connectivity monitoring')

    args = parser.parse_args()

    try:
        # Create weather map instance
        weather_map = WeatherMap(args.led_count)

        # Run continuous monitoring
        weather_map.run_continuous(
            update_interval_minutes=args.update_interval,
            wifi_check_enabled=not args.disable_wifi_check
        )

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to run with: sudo /path/to/venv/bin/python metar_map_se.py")


if __name__ == "__main__":
    main()