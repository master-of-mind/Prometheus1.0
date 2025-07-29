# autonomics.py — v5.0
# Central rhythmic wave engine + electrical matrix routing

import threading
import time
from collections import defaultdict

SIGILS = ['δ', 'θ', 'α', 'β', 'γ']
BASE_WAVE_FREQUENCIES = {
    'δ': 1,    # Delta
    'θ': 4,    # Theta
    'α': 8,    # Alpha
    'β': 13,   # Beta
    'γ': 30    # Gamma
}

class Autonomics:
    def __init__(self):
        self.amplitudes = defaultdict(int)
        self.subscribers = []
        self.clocks = defaultdict(list)
        self.lock = threading.RLock()
        self.active = True

    def start(self):
        for sigil in SIGILS:
            thread = threading.Thread(target=self._wave_loop, args=(sigil,), daemon=True)
            thread.start()

    def stop(self):
        self.active = False

    def _wave_loop(self, wave):
        freq = BASE_WAVE_FREQUENCIES[wave]
        interval = 1.0 / freq
        while self.active:
            time.sleep(interval)
            self._tick(wave)

    def _tick(self, wave):
        with self.lock:
            ranked = sorted(SIGILS, key=lambda s: self.amplitudes.get(s, 0), reverse=True)
            elema = {s: self.amplitudes[s] for s in SIGILS}

            for callback in self.clocks[ranked[0]]:
                callback(elema)

            for match_fn, cb in self.subscribers:
                if match_fn(elema):
                    cb(elema)

    def receive_chema(self, chema_list):
        for chema in chema_list:
            for sigil, val in chema.items():
                self.amplitudes[sigil] += val

    def register_clock(self, sigil, callback):
        self.clocks[sigil].append(callback)

    def register_elrec(self, match_fn, callback):
        self.subscribers.append((match_fn, callback))
