# brainstem.py — v2.2
# Internal system sensor for introspective chema: δ, θ, α, β, γ represent
# [temp, cool, power, mem, integrity]

import random
import time
from collections import defaultdict

class Brainstem:
    def __init__(self):
        self.last_emit_time = 0
        self.delay = 1.0  # seconds between pulses

        # Sliding thresholds
        self.ideal_values = {
            'δ': 1,   # Temperature ideal
            'θ': 1,   # Cooling ideal
            'α': 1,   # Power ideal
            'β': 1,   # Memory ideal
            'γ': 1    # Integrity ideal
        }

        self.tolerances = {
            'δ': 0.1,
            'θ': 0.1,
            'α': 0.1,
            'β': 0.1,
            'γ': 0.1
        }

    def read(self):
        """
        Stubbed hardware read returning simulated system values.
        Replace these with actual sensor integrations.
        """
        return {
            'δ': random.uniform(0.5, 1.5),   # temperature
            'θ': random.uniform(0.5, 1.5),   # cooling
            'α': 1.0,                        # power (1 = plugged in)
            'β': random.uniform(0.5, 1.5),   # memory availability
            'γ': random.uniform(0.5, 1.5)    # system integrity
        }

    def update_sliding_thresholds(self, current):
        for k in self.ideal_values:
            diff = current[k] - self.ideal_values[k]

            # Adjust ideal toward current
            self.ideal_values[k] += 0.01 * diff

            # Adjust tolerance based on whether we're inside or outside range
            if abs(diff) <= self.tolerances[k]:
                self.tolerances[k] = max(0.05, self.tolerances[k] - 0.005)
            else:
                self.tolerances[k] = min(0.5, self.tolerances[k] + 0.01)

    def emit(self):
        now = time.time()
        if now - self.last_emit_time < self.delay:
            return []

        self.last_emit_time = now
        current = self.read()
        self.update_sliding_thresholds(current)

        chema = defaultdict(int)

        for k in current:
            ideal = self.ideal_values[k]
            tolerance = self.tolerances[k]
            deviation = current[k] - ideal

            if deviation > tolerance:
                chema[k] = -1
            elif deviation < -tolerance:
                chema[k] = -1
            else:
                chema[k] = 1

        return [dict(chema) for _ in range(sum(abs(v) for v in chema.values()))]
