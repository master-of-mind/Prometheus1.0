# genesis.py — v5.1
# Bootstraps the triune brain: autonomics, chembus, and brainstem

import signal
import sys
from autonomics import Autonomics
from chembus import ChemBus
from brainstem import Brainstem
from diagnostics import Diagnostics

if __name__ == "__main__":
    bus = ChemBus()
    loop = Autonomics()
    core = Brainstem()
    diagnostics = Diagnostics(bus)

    # Link the organs
    bus.register_source(core.emit)
    loop.register_chembus(bus)
    loop.register_autonomics(core)
    loop.register_tick_callback(diagnostics.record)

    def shutdown_handler(sig, frame):
        print("\n[Prometheus] Received termination signal. Shutting down gracefully...")
        diagnostics.stop()
        loop.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)

    print("[Prometheus] Ignition sequence initialized. Loop starting...")

    diagnostics.start()

    try:
        loop.start()
    except KeyboardInterrupt:
        shutdown_handler(None, None)
    finally:
        print("[Prometheus] All pulses silenced.")
