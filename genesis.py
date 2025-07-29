# genesis.py — v5.0
# Bootstraps the triune brain: autonomics, chembus, and brainstem

import signal
import sys
from autonomics import Autonomics
from chembus import ChemBus
from brainstem import Brainstem

if __name__ == "__main__":
    bus = ChemBus()
    loop = Autonomics()
    core = Brainstem()

    # Link the organs
    bus.register_source(core.emit)
    loop.register_chembus(bus)
    loop.register_autonomics(core)

    def shutdown_handler(sig, frame):
        print("\n[Prometheus] Received termination signal. Shutting down gracefully...")
        loop.stop()
        sys.exit(0)

    # Attach Ctrl+C / SIGINT handler
    signal.signal(signal.SIGINT, shutdown_handler)

    print("[Prometheus] Ignition sequence initialized. Loop starting...")
    
    try:
        loop.start()
    except KeyboardInterrupt:
        shutdown_handler(None, None)
    finally:
        print("[Prometheus] All pulses silenced.")
