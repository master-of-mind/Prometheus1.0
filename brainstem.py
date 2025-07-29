# brainstem.py — v5.0
# Internal system monitor with chemical output

import psutil
from collections import defaultdict
import random

SIGILS = ['δ', 'θ', 'α', 'β', 'γ']

class Brainstem:
    def __init__(self):
        self.ideal = {
            'δ': 45,   # temperature
            'θ': 1,    # cooling
            'α': 1,    # power
            'β': 500,  # memory
            'γ': 1     # system integrity
        }
        self.tolerance = {
            'δ': 5,
            'θ': 1,
            'α': 0,
            'β': 100,
            'γ': 0
        }
        self._tick = 0

    def _get_temperature(self):
        try:
            temps = psutil.sensors_temperatures()
            for sensor_list in temps.values():
                for entry in sensor_list:
                    if entry.current:
                        return entry.current
        except Exception:
            pass
        return 50 + random.randint(-2, 2)  # fallback stub

    def _get_cooling(self):
        try:
            fans = psutil.sensors_fans()
            return sum([fan.current for group in fans.values() for fan in group]) or 0
        except Exception:
            return 1 + random.randint(0, 2)

    def _get_power(self):
        try:
            battery = psutil.sensors_battery()
            return 1 if battery and battery.power_plugged else -1
        except Exception:
            return 1

    def _get_memory(self):
        return psutil.virtual_memory().available // (1024 * 1024)

    def _get_integrity(self):
        return 1  # Replace with actual check if needed

    def _slide_ideal(self, current, target, weight=0.05):
        return current + (target - current) * weight

    def emit(self):
        self._tick += 1
        chema_packets = []

        system = {
            'δ': self._get_temperature(),
            'θ': self._get_cooling(),
            'α': self._get_power(),
            'β': self._get_memory(),
            'γ': self._get_integrity()
        }

        for sigil in SIGILS:
            curr = system[sigil]
            base = self.ideal[sigil]
            tol = self.tolerance[sigil]

            # Update ideal range over time
            self.ideal[sigil] = self._slide_ideal(base, curr)

            delta = curr - self.ideal[sigil]

            if delta > tol:
                packet = {s: 0 for s in SIGILS}
                packet[sigil] = 1
                chema_packets.append(packet)
            elif delta < -tol:
                packet = {s: 0 for s in SIGILS}
                packet[sigil] = -1
                chema_packets.append(packet)

        return chema_packets
