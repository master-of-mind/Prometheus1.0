# brainstem.py — v2.1
# Introspective sensor module for internal system diagnostics and chema output

import psutil
import random

SIGILS = ['δ', 'θ', 'α', 'β', 'γ']

class Brainstem:
    def __init__(self):
        self.tolerance = {sigil: 5 for sigil in SIGILS}
        self.ideal = {sigil: 0 for sigil in SIGILS}

    def emit(self):
        state = self._get_system_state()
        packets = []

        for sigil in SIGILS:
            val = state[sigil]
            ideal = self.ideal[sigil]
            tol = self.tolerance[sigil]

            if abs(val - ideal) <= tol:
                self.tolerance[sigil] = max(1, self.tolerance[sigil] - 1)
            else:
                self.tolerance[sigil] += 1
                self.ideal[sigil] += (val - ideal) * 0.05

            if val == 1:
                packets.append({s: 1 if s == sigil else 0 for s in SIGILS})
            elif val == -1:
                packets.append({s: -1 if s == sigil else 0 for s in SIGILS})

        return packets

    def _get_system_state(self):
        try:
            temp = psutil.sensors_temperatures().get("coretemp", [{}])[0].get("current", 50)
        except:
            temp = 50  # default fallback

        ram = psutil.virtual_memory().available / psutil.virtual_memory().total
        load = psutil.cpu_percent() / 100.0
        integrity = 1.0 if not psutil.disk_usage('/').percent > 90 else 0.0
        plugged = psutil.sensors_battery().power_plugged if psutil.sensors_battery() else True

        return {
            'δ': self._scale(temp, 30, 85),           # temperature
            'θ': self._scale(load, 0, 1),             # cpu load
            'α': self._scale(ram, 0.1, 1),            # ram availability
            'β': 1 if plugged else -1,                # power
            'γ': 1 if integrity else -1               # system integrity
        }

    def _scale(self, val, low, high):
        if val < low:
            return -1
        elif val > high:
            return 1
        return 0
