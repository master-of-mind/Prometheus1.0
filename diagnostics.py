# diagnostics.py — v1.1
# Timestamped session-based signal logger for Prometheus system

import json
import threading
from datetime import datetime

class Diagnostics:
    def __init__(self, chembus):
        self.chembus = chembus
        self.active = False
        self.lock = threading.Lock()
        self.log = []
        self.filename = None

    def start(self):
        with self.lock:
            self.active = True
            timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
            self.filename = f"prometheus_log_{timestamp}.json"
            self.log = []
            print(f"[Diagnostics] Recording started. Logging to {self.filename}")

    def stop(self):
        with self.lock:
            self.active = False
            self._dump_to_file()
            print("[Diagnostics] Recording stopped and data saved.")

    def toggle(self):
        if self.active:
            self.stop()
        else:
            self.start()

    def record(self, pulse):
        if not self.active:
            return

        data = {
            "timestamp": datetime.utcnow().isoformat(),
            "pulse": pulse,
            "pressure": self.chembus.get_wave_amplitude(),
            "chema": list(self.chembus.chema)
        }

        with self.lock:
            self.log.append(data)

    def _dump_to_file(self):
        if not self.filename:
            return  # Should never happen, but just in case

        try:
            with open(self.filename, "w") as f:
                json.dump(self.log, f, indent=2)
        except Exception as e:
            print(f"[Diagnostics] Error writing file: {e}")
