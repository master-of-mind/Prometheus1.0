# autonomics.py — v5.0
# Handles wave tick rhythm and electrical routing only

import threading
import time
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
        self.subscribers = []
        self.wave_amplitude = defaultdict(int)
        self.wave_threads = {}
        self.lock = threading.RLock()
        self.active = True

    def set_amplitude(self, amp_dict):
        with self.lock:
            self.wave_amplitude = amp_dict

    def register_elrec(self, match_fn, callback):
        self.subscribers.append((match_fn, callback))

    def _get_dominant_wave(self):
        if not self.wave_amplitude:
            return 'α'
        return max(self.wave_amplitude, key=self.wave_amplitude.get)

    def _wave_loop(self, wave):
        interval = 1.0 / BASE_WAVE_FREQUENCIES[wave]
        while self.active:
            time.sleep(interval)
            self._tick(wave)

    def _tick(self, wave):
        with self.lock:
            dominant = self._get_dominant_wave()
            if wave == dominant:
                matrix = {w: self.wave_amplitude.get(w, 0) for w in BASE_WAVE_FREQUENCIES}
                matrix[wave] += 1
                self._push_packet(matrix)

    def _push_packet(self, matrix):
        for match_fn, callback in self.subscribers:
            if match_fn(matrix):
                callback(matrix)

    def start(self):
        self.active = True
        for wave in BASE_WAVE_FREQUENCIES:
            thread = threading.Thread(target=self._wave_loop, args=(wave,), daemon=True)
            thread.start()
            self.wave_threads[wave] = thread

    def stop(self):
        self.active = False
