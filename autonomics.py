# autonomics.py — v5.0
# Unified autonomic loop: wave engine, chembus, ars, and coma

import threading
import time
import sys
from collections import defaultdict, deque

BASE_WAVE_FREQUENCIES = {
    'δ': 1,    # Delta
    'θ': 4,    # Theta
    'α': 8,    # Alpha
    'β': 13,   # Beta
    'γ': 30    # Gamma
}

class Autonomics:
    def __init__(self):
        self.chembus = []
        self.subscribers = []
        self.mods = []
        self.wave_amplitude = defaultdict(int)
        self.wave_threads = {}
        self.lock = threading.RLock()

        self.chemical_sources = []  # funcs that return chema dicts
        self.active = True

        self._coma_triggered = False
        self._coma_thresholds = {
            'δ': 20,
            'θ': 20,
            'α': 0,
            'β': -20,
            'γ': -20
        }

    # ======== BOOTSTRAP ========
    def start(self):
        self.active = True
        for wave in BASE_WAVE_FREQUENCIES:
            thread = threading.Thread(target=self._wave_loop, args=(wave,), daemon=True)
            thread.start()
            self.wave_threads[wave] = thread

    def stop(self):
        self.active = False

    # ======== TICKING ========
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

    # ======== MOD REGISTRATION ========
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

    # ======== CHEMBUS ========
    def extract_matching_chema(self, chrec_fn):
        matching = [c for c in self.chembus if chrec_fn(c)]
        self.chembus = [c for c in self.chembus if not chrec_fn(c)]
        return matching

    def get_all_chema(self):
        return list(self.chembus)

    def _is_zero(self, matrix):
        return all(v == 0 for v in matrix.values())

    # ======== AMPLITUDE COLLECTION ========
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

    # ======== COMA CHECK ========
    def _check_coma_condition(self):
        if self._coma_triggered:
            return

        match = all(
            self.wave_amplitude.get(k, 0) <= v if v < 0 else self.wave_amplitude.get(k, 0) >= v
            for k, v in self._coma_thresholds.items()
        )

        if match:
            self._coma_triggered = True
            self._shutdown_sequence()

    def _shutdown_sequence(self):
        try:
            sys.exit(0)
        except SystemExit:
            pass
