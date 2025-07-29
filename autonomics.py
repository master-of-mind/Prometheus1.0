# autonomics.py — v5.0
# Global electrical rhythm engine that drives elema based on wave amplitude

import threading
import time
from constants import SIGILS

BASE_WAVE_FREQUENCIES = {
    'δ': 1,
    'θ': 4,
    'α': 8,
    'β': 13,
    'γ': 30
}

class Autonomics:
    def __init__(self):
        self.wave_amplitude = {s: 0 for s in SIGILS}
        self.tick_callbacks = []
        self.clocks = []
        self.chembus = None
        self.active = False
        self.threads = {}

    def register_tick_callback(self, callback):
        self.tick_callbacks.append(callback)

    def register_chembus(self, bus):
        self.chembus = bus

    def register_clock(self, clock_fn):
        self.clocks.append(clock_fn)

    def start(self):
        self.active = True
        for sigil in SIGILS:
            t = threading.Thread(target=self._wave_loop, args=(sigil,), daemon=True)
            t.start()
            self.threads[sigil] = t

    def stop(self):
        self.active = False

    def _wave_loop(self, sigil):
        interval = 1.0 / BASE_WAVE_FREQUENCIES[sigil]
        while self.active:
            time.sleep(interval)
            self._tick(sigil)

    def _tick(self, sigil):
        if not self.chembus:
            return

        # 1. Refresh wave amplitudes from chembus
        self.wave_amplitude = self.chembus.get_wave_amplitude()

        # 2. Sort and find top-ranked wave
        ranked = sorted(SIGILS, key=lambda k: self.wave_amplitude.get(k, 0), reverse=True)
        top_wave = ranked[0]

        # 3. If this is the top wave, emit a pulse
        if sigil == top_wave:
            pulse = {k: self.wave_amplitude.get(k, 0) for k in SIGILS}
            for clock_fn in self.clocks:
                clock_fn(pulse)
            for cb in self.tick_callbacks:
                cb(pulse)
