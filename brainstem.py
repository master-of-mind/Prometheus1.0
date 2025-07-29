# brainstem.py — v1.0
# Internal sensor module. Emits chema during δ wave pulses.

import random

class Brainstem:
    """
    Reports introspective system values (temp, cooling, power, RAM, system integrity)
    Emits chemical signals to chembus on delta wave pulses.
    """
    def __init__(self, chembus):
        self.chembus = chembus
        self.sigils = ['δ', 'θ', 'α', 'β', 'γ']  # Sigils mapped to internal metrics

    def register_with_autonomics(self, auto):
        auto.register_subscriber(self._delta_only, self.on_tick)

    def _delta_only(self, matrix):
        return matrix.get('δ', 0) > 0  # Respond only to delta pulses

    def on_tick(self, matrix):
        # Simulated system status checks
        temperature = self._check_temp()
        cooling = self._check_cooling()
        power = self._check_power()
        ram = self._check_ram()
        integrity = self._check_integrity()

        # Map values to chema [-1, 0, 1] across sigils
        chema = {
            'δ': temperature,
            'θ': cooling,
            'α': power,
            'β': ram,
            'γ': integrity
        }

        self.chembus.receive(chema)

    # ==== Simulated Sensor Methods ====
    def _check_temp(self):
        # Placeholder logic; replace with real probe later
        val = random.randint(25, 80)
        return -1 if val > 70 else 1 if val < 40 else 0

    def _check_cooling(self):
        # Placeholder fan speed range
        val = random.randint(0, 100)
        return 1 if val > 60 else -1 if val < 20 else 0

    def _check_power(self):
        # Assume always plugged in for now
        return 1

    def _check_ram(self):
        # Placeholder: 80% used triggers warning
        val = random.randint(30, 95)
        return -1 if val > 85 else 1 if val < 50 else 0

    def _check_integrity(self):
        # Simulated random fault
        return -1 if random.random() < 0.1 else 1
