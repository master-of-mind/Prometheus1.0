# genesis.py — v5.0
# Bootstraps the triune brain: autonomics, chembus, and brainstem

from autonomics import Autonomics
from chembus import ChemBus
from brainstem import Brainstem

if __name__ == "__main__":
    bus = ChemBus()
    loop = Autonomics()
    core = Brainstem()

    bus.register_source(core.emit)
    loop.register_chembus(bus)
    loop.register_autonomics(core)

    loop.start()
