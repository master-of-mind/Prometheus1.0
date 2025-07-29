# chembus.py — v5.0
# Shared chemical routing and chrec logic

from collections import deque

SIGILS = ['δ', 'θ', 'α', 'β', 'γ']

class ChemBus:
    def __init__(self):
        self.chema = deque()
        self.chrec_registry = []

    def add(self, chemical):
        if not self._is_zero(chemical):
            self.chema.append(chemical)

    def _is_zero(self, chem):
        return all(v == 0 for v in chem.values())

    def register_chrec(self, chrec_fn, callback):
        self.chrec_registry.append((chrec_fn, callback))

    def evaluate(self):
        remaining = deque()
        for chem in self.chema:
            matched = False
            for chrec_fn, callback in self.chrec_registry:
                if chrec_fn(chem):
                    callback(chem)
                    matched = True
                    break
            if not matched:
                remaining.append(chem)
        self.chema = remaining

    def get_all(self):
        return list(self.chema)
