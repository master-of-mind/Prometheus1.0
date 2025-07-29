# chembus.py — v5.0
# Global chemical bus and chrec matcher

from collections import Counter
from constants import SIGILS

class ChemBus:
    def __init__(self):
        self.chema = []

    def add(self, chema_batch):
        for chem in chema_batch:
            if not self._is_zero(chem):
                self.chema.append(chem)

    def get_wave_amplitude(self):
        total = Counter()
        for chem in self.chema:
            for k, v in chem.items():
                total[k] += v
        return dict(total)

    def chrec(self, match_fn):
        matched = []
        remaining = []

        for chem in self.chema:
            if match_fn(chem):
                matched.append(chem)
            else:
                remaining.append(chem)

        self.chema = remaining
        return matched

    def _is_zero(self, chem):
        return all(v == 0 for v in chem.values())
