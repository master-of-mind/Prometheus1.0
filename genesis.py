# genesis.py — v5.0
# System bootstrapper: initializes the sacred triune and launches the core loop

from autonomics import Autonomics
from chembus import ChemBus
from brainstem import Brainstem

def main():
    # === Create core systems ===
    bus = ChemBus()
    core = Brainstem()
    loop = Autonomics()

    # === Wire sacred triune ===
    loop.register_chembus(bus)
    core.register_chembus(bus)
    core.register_autonomics(loop)

    # === Start the loop ===
    loop.start()

if __name__ == "__main__":
    main()
