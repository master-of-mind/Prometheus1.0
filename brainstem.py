# brainstem.py — v4.1
# Unified brain loop, routing, chembus, coma logic, and now: the bootstrapper.

import threading
import time
import sys
from collections import defaultdict, deque
from subconscious import Subconscious
from curiosity import CuriosityDrive
from cstem import CStem

BASE_WAVE_FREQUENCIES = {
    'δ': 1,
    'θ': 4,
    'α': 8,
    'β': 13,
    'γ': 30
}

class Brainstem:
    def __init__(self):
        self.chembus = []
        self.subscribers = []
        self.mods = []
        self.wave_amplitude = defaultdict(int)
        self.wave_threads = {}
        self.lock = threading.RLock()

        self.chemical_sources = []
        self.active = True

        self._coma_triggered = False

        # === Instantiate Mods ===
        self.subconscious = Subconscious()
        self.curiosity = CuriosityDrive()
        self.cstem = CStem()

        self._wire()

    def _wire(self):
        self.register_mod(self.subconscious)
        self.register_mod(self.curiosity)
        self.register_mod(self.cstem)

        self.register_subscriber(lambda m: self.subconscious.elrec(m), self.subconscious._on_tick)
        self.register_subscriber(lambda m: self.curiosity.elrec(m), self.curiosity._on_tick)

        self.register_chemical_source(self.cstem.emit)

    def start(self):
        self.active = True
        for wave in BASE_WAVE_FREQUENCIES:
            thread = threading.Thread(target=self._wave_loop, args=(wave,), daemon=True)
            thread.start()
            self.wave_threads[wave] = thread

    def stop(self):
        self.active = False

    def _wave_loop(self, wave):
        interval = 1.0 / BASE_WAVE_FREQUENCIES[wave]
        while self.active:
            time.sleep(interval)
            self._tick(wave)

    def _tick(self, wave):
        with self.lock:
            self._collect_chemical_pressures()
            self._check_coma_condition()

            dominant = self._get_dominant_wave()
            if wave == dominant:
                matrix = {w: self.wave_amplitude.get(w, 0) for w in BASE_WAVE_FREQUENCIES}
                matrix[wave] += 1
                self.push_packet(matrix)

                for mod in self.mods:
                    if hasattr(mod, "degrade_chemical_pressure"):
                        mod.degrade_chemical_pressure()

                for func in self.chemical_sources:
                    chem = func()
                    if not self._is_zero(chem):
                        self.chembus.append(chem)

    def _collect_chemical_pressures(self):
        summed = defaultdict(int)
        for mod in self.mods:
            if hasattr(mod, "get_chemical_pressure"):
                pressure = mod.get_chemical_pressure()
                for k, v in pressure.items():
                    summed[k] += v
        self.wave_amplitude = summed

    def _get_dominant_wave(self):
        if not self.wave_amplitude:
            return 'α'
        return max(self.wave_amplitude, key=self.wave_amplitude.get)

    def register_subscriber(self, match_fn, callback):
        self.subscribers.append((match_fn, callback))

    def push_packet(self, matrix):
        for match_fn, callback in self.subscribers:
            if match_fn(matrix):
                callback(matrix)

    def register_mod(self, mod):
        self.mods.append(mod)

    def register_chemical_source(self, func):
        self.chemical_sources.append(func)

    # ======== COMA ========
    def _check_coma_condition(self):
        if self._coma_triggered:
            return

        δ = self.wave_amplitude.get('δ', 0)
        θ = self.wave_amplitude.get('θ', 0)
        β = self.wave_amplitude.get('β', 0)
        γ = self.wave_amplitude.get('γ', 0)

        if δ >= 20 and θ >= 20 and β <= -20 and γ <= -20:
            self._coma_triggered = True
            self._shutdown_sequence()

    def _shutdown_sequence(self):
        try:
            sys.exit(0)
        except SystemExit:
            pass

    # ======== CHEMBUS TOOLS ========
    def extract_matching_chema(self, chrec_fn):
        matching = [c for c in self.chembus if chrec_fn(c)]
        self.chembus = [c for c in self.chembus if not chrec_fn(c)]
        return matching

    def get_all_chema(self):
        return list(self.chembus)

    def _is_zero(self, matrix):
        return all(v == 0 for v in matrix.values())

# ======== Invocation ========
if __name__ == "__main__":
    core = Brainstem()
    core.start()
