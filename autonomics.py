# autonomics.py — v5.0
# Rhythmic wave engine and electrical signaling core (sacred)

import time
import threading
from collections import defaultdict

BASE_WAVE_FREQUENCIES = {
    'δ': 1,    # Delta
    'θ': 4,    # Theta
    'α': 8,    # Alpha
    'β': 13,   # Beta
    'γ': 30    # Gamma
}

class Autonomics:
    def __init__(self):
        self.electrical_subscribers = []
        self.wave_amplitude = defaultdict(int)
        self.mods = []
        self.active = True
        self.lock = threading.RLock()

    def start(self):
        for wave, freq in BASE_WAVE_FREQUENCIES.items():
            t = threading.Thread(target=self._oscillate, args=(wave, freq), daemon=True)
            t.start()

    def register_mod(self, mod):
        self.mods.append(mod)

    def register_elrec(self, match_fn, callback):
        self.electrical_subscribers.append((match_fn, callback))

    def _oscillate(self, wave, freq):
        interval = 1.0 / freq
        while self.active:
            time.sleep(interval)
            self._tick(wave)

    def _tick(self, wave):
        with self.lock:
            self._update_wave_amplitudes()
            matrix = self._generate_matrix(wave)
            self._dispatch(matrix)

    def _update_wave_amplitudes(self):
        summed = defaultdict(int)
        for mod in self.mods:
            if hasattr(mod, "get_chemical_pressure"):
                pressure = mod.get_chemical_pressure()
                for k, v in pressure.items():
                    summed[k] += v
        self.wave_amplitude = summed

    def _generate_matrix(self, spike_wave):
        matrix = {}
        for wave in BASE_WAVE_FREQUENCIES:
            amp = self.wave_amplitude.get(wave, 0)
            matrix[wave] = amp + (1 if wave == spike_wave else 0)
        return matrix

    def _dispatch(self, matrix):
        for match_fn, callback in self.electrical_subscribers:
            if match_fn(matrix):
                callback(matrix)
