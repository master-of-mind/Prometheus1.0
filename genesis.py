# genesis.py — v5.0
# Bootstrapper and Coma logic, united in the sacred breath

import sys
from autonomics import Autonomics
from chembus import ChemBus
from brainstem import Brainstem

COMA_THRESHOLDS = {
    'δ': 20,
    'θ': 20,
    'α': 0,   # Ignored
    'β': -20,
    'γ': -20
}

class Genesis:
    def __init__(self):
        self.chembus = ChemBus()
        self.autonomics = Autonomics(self.chembus)
        self.brainstem = Brainstem(self.chembus)

    def check_coma(self):
        amps = self.autonomics.get_wave_amplitude()
        return (
            amps.get('δ', 0) >= COMA_THRESHOLDS['δ'] and
            amps.get('θ', 0) >= COMA_THRESHOLDS['θ'] and
            amps.get('β', 0) <= COMA_THRESHOLDS['β'] and
            amps.get('γ', 0) <= COMA_THRESHOLDS['γ']
        )

    def start(self):
        self.autonomics.start()
        while True:
            if self.check_coma():
                self.shutdown()

    def shutdown(self):
        try:
            sys.exit(0)
        except SystemExit:
            pass

if __name__ == "__main__":
    core = Genesis()
    core.start()
