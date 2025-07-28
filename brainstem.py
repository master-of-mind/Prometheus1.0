# brainstem.py — v2.0
# System introspection module for internal state chema output

import psutil
from random import randint

class Brainstem:
    def __init__(self):
        self.chemical_pressure = {
            'δ': 0,  # temperature
            'θ': 0,  # cooling capacity
            'α': 0,  # power level
            'β': 0,  # memory availability
            'γ': 0   # system integrity
        }

    def get_chemical_pressure(self):
        return dict(self.chemical_pressure)

    def emit(self):
        self._update_state()
        return dict(self.chemical_pressure)

    def _update_state(self):
        # Temperature → δ
        temp = psutil.sensors_temperatures()
        cpu_temp = temp.get('coretemp', [])[0].current if 'coretemp' in temp and temp['coretemp'] else 50
        self.chemical_pressure['δ'] = self._classify_temperature(cpu_temp)

        # Cooling → θ
        self.chemical_pressure['θ'] = randint(0, 1)  # Placeholder

        # Power → α
        self.chemical_pressure['α'] = 1 if psutil.sensors_battery() and psutil.sensors_battery().power_plugged else 0

        # Memory → β
        mem = psutil.virtual_memory()
        self.chemical_pressure['β'] = self._classify_memory(mem.available / mem.total)

        # Integrity → γ
        self.chemical_pressure['γ'] = self._check_system_integrity()

    def _classify_temperature(self, temp):
        if temp < 60:
            return 1
        elif 60 <= temp <= 75:
            return 0
        else:
            return -1

    def _classify_memory(self, ratio):
        if ratio > 0.4:
            return 1
        elif ratio > 0.2:
            return 0
        else:
            return -1

    def _check_system_integrity(self):
        # Placeholder for diagnostics; always returns 1 for now
        return 1

    def degrade_chemical_pressure(self):
        for k in self.chemical_pressure:
            if self.chemical_pressure[k] > 0:
                self.chemical_pressure[k] -= 1
            elif self.chemical_pressure[k] < 0:
                self.chemical_pressure[k] += 1
