"""
Biometric Data Integration
Supports: Apple Watch (HRV, HR), Oura Ring (Sleep), Manual mood logging
"""
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class BiometricIntegration:
    """
    Unified biometric data interface
    Polls from various sources and aggregates
    """

    def __init__(self, data_dir: str = "psyche_edge/data/biometrics"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.cache_file = self.data_dir / "latest_biometrics.json"

        # Latest readings
        self.latest_biometrics = {
            'hrv': None,
            'heart_rate': None,
            'sleep_score': None,
            'mood': None,
            'stress_level': None,
            'timestamp': None
        }

    def get_latest_biometrics(self) -> Dict[str, Any]:
        """Get most recent biometric readings"""
        # Load from cache
        if self.cache_file.exists():
            with open(self.cache_file) as f:
                cached = json.load(f)

                # Check if cache is fresh (< 5 minutes old)
                if cached.get('timestamp'):
                    age = time.time() - cached['timestamp']
                    if age < 300:  # 5 minutes
                        return cached

        # Otherwise poll from sources
        self._poll_sources()

        return self.latest_biometrics

    def _poll_sources(self):
        """Poll all biometric sources"""
        # Apple Watch / HealthKit
        apple_data = self._poll_apple_watch()
        if apple_data:
            self.latest_biometrics.update(apple_data)

        # Oura Ring
        oura_data = self._poll_oura()
        if oura_data:
            self.latest_biometrics.update(oura_data)

        # Manual mood log
        mood_data = self._get_latest_mood()
        if mood_data:
            self.latest_biometrics.update(mood_data)

        self.latest_biometrics['timestamp'] = time.time()

        # Save to cache
        with open(self.cache_file, 'w') as f:
            json.dump(self.latest_biometrics, f)

    def _poll_apple_watch(self) -> Optional[Dict]:
        """
        Poll Apple Watch data
        Options:
        1. Read from HealthKit export XML
        2. Use Apple Health API (requires iOS app)
        3. Manual CSV import
        """
        # Check for recent HealthKit export
        export_file = self.data_dir / "apple_health_export.json"

        if export_file.exists():
            with open(export_file) as f:
                data = json.load(f)

                # Extract latest HRV and HR
                return {
                    'hrv': data.get('hrv'),
                    'heart_rate': data.get('heart_rate'),
                    'source': 'apple_watch'
                }

        # Check for manual CSV
        csv_file = self.data_dir / "hrv_data.csv"
        if csv_file.exists():
            import pandas as pd
            try:
                df = pd.read_csv(csv_file)
                latest = df.iloc[-1]

                return {
                    'hrv': float(latest.get('hrv', 0)),
                    'heart_rate': float(latest.get('hr', 0)),
                    'source': 'apple_watch_csv'
                }
            except Exception as e:
                print(f"Error reading Apple Watch CSV: {e}")

        return None

    def _poll_oura(self) -> Optional[Dict]:
        """
        Poll Oura Ring API for sleep data
        Requires OURA_API_TOKEN in .env
        """
        import os
        import requests

        api_token = os.getenv('OURA_API_TOKEN')

        if not api_token:
            # Check for manual import
            oura_file = self.data_dir / "oura_sleep.json"
            if oura_file.exists():
                with open(oura_file) as f:
                    data = json.load(f)
                    return {
                        'sleep_score': data.get('score'),
                        'source': 'oura_manual'
                    }
            return None

        # API call
        try:
            # Get sleep data from yesterday
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

            response = requests.get(
                f'https://api.ouraring.com/v2/usercollection/sleep',
                headers={'Authorization': f'Bearer {api_token}'},
                params={'start_date': yesterday, 'end_date': yesterday}
            )

            if response.status_code == 200:
                data = response.json()

                if data.get('data'):
                    latest_sleep = data['data'][-1]

                    return {
                        'sleep_score': latest_sleep['score'],
                        'source': 'oura_api'
                    }

        except Exception as e:
            print(f"Error polling Oura API: {e}")

        return None

    def _get_latest_mood(self) -> Optional[Dict]:
        """Get latest manual mood log"""
        mood_log = self.data_dir / "mood_log.jsonl"

        if mood_log.exists():
            # Read last line
            with open(mood_log) as f:
                lines = f.readlines()
                if lines:
                    latest = json.loads(lines[-1])

                    # Check if recent (< 12 hours)
                    age = time.time() - latest.get('timestamp', 0)
                    if age < 43200:  # 12 hours
                        return {
                            'mood': latest['mood'],
                            'stress_level': latest.get('stress_level'),
                            'source': 'manual_mood'
                        }

        return None

    def log_mood(self, mood: str, stress_level: int = 5, notes: str = ""):
        """Manually log mood"""
        mood_log = self.data_dir / "mood_log.jsonl"

        entry = {
            'timestamp': time.time(),
            'mood': mood,
            'stress_level': stress_level,
            'notes': notes
        }

        with open(mood_log, 'a') as f:
            f.write(json.dumps(entry) + '\n')

        self.latest_biometrics['mood'] = mood
        self.latest_biometrics['stress_level'] = stress_level

    def import_apple_health_export(self, export_path: str):
        """
        Import Apple Health XML export
        User can export from iPhone Health app
        """
        # Placeholder for XML parsing
        # Would parse export.xml and extract HRV, HR data
        print(f"Import Apple Health from: {export_path}")

    def import_oura_data(self, json_path: str):
        """Import Oura sleep data from JSON"""
        import shutil

        dest = self.data_dir / "oura_sleep.json"
        shutil.copy(json_path, dest)

        print(f"Imported Oura data to {dest}")


class BiometricSimulator:
    """
    Simulate biometric data for testing/demo
    Generates realistic patterns with circadian rhythms
    """

    def __init__(self):
        self.base_hrv = 60
        self.base_hr = 70
        self.base_sleep = 80

    def generate_realistic_biometrics(self) -> Dict[str, Any]:
        """Generate biometric data with realistic patterns"""
        import random
        import math

        # Time of day affects metrics
        hour = datetime.now().hour

        # HRV - higher in morning, lower at night/when stressed
        hrv_circadian = 10 * math.cos((hour - 6) * math.pi / 12)
        hrv = self.base_hrv + hrv_circadian + random.gauss(0, 5)
        hrv = max(20, min(100, hrv))

        # Heart rate - inverse of HRV
        hr = self.base_hr - (hrv - 60) / 3 + random.gauss(0, 3)
        hr = max(50, min(120, hr))

        # Sleep score - simulated from "last night"
        sleep = random.gauss(self.base_sleep, 10)
        sleep = max(50, min(100, sleep))

        # Mood - weighted random
        moods = ['calm', 'neutral', 'excited', 'anxious', 'tired']
        mood_weights = [0.3, 0.3, 0.2, 0.15, 0.05]

        # Stress level correlates with HRV
        stress = int(10 - (hrv - 50) / 10)
        stress = max(1, min(10, stress))

        return {
            'hrv': round(hrv, 1),
            'heart_rate': round(hr, 1),
            'sleep_score': round(sleep, 1),
            'mood': random.choices(moods, weights=mood_weights)[0],
            'stress_level': stress,
            'timestamp': time.time(),
            'source': 'simulator'
        }
