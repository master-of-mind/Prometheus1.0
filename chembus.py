# chembus.py — v5.0
# Centralized chemical routing system with passive chrec-based access

from collections import deque

class ChemBus:
    def __init__(self):
        self.chema = deque()

    def deposit(self, chemical):
        if not self._is_zero(chemical):
            self.chema.append(chemical)

    def _is_zero(self, chem):
        return all(v == 0 for v in chem.values())

    def chrec(self, chemlock):
        """
        Returns True if any chema on the bus matches the provided chemlock.
        Does not remove anything from the bus.
        """
        for chem in self.chema:
            if self._matches_chemlock(chem, chemlock):
                return True
        return False

    def _matches_chemlock(self, chem, lock):
        for k in lock:
            if chem.get(k, 0) + lock[k] != 0:
                return False
        return True

    def decay(self, amount=1):
        """
        Degrades all non-zero chemical values in the bus by the given amount.
        If a chemical reaches zero across all keys, it is removed.
        """
        new_chema = deque()
        for chem in self.chema:
            decayed = {}
            for k, v in chem.items():
                if v > 0:
                    decayed[k] = max(0, v - amount)
                elif v < 0:
                    decayed[k] = min(0, v + amount)
                else:
                    decayed[k] = 0
            if not self._is_zero(decayed):
                new_chema.append(decayed)
        self.chema = new_chema

    def extract_all(self):
        all_chem = list(self.chema)
        self.chema.clear()
        return all_chem

    def peek(self):
        return list(self.chema)
