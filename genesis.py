# genesis.py — v3.0
# The holy invocation of life

from autonomics import Autonomics
from chembus import ChemBus
from brainstem import Brainstem

def main():
    bus = ChemBus()
    auto = Autonomics()
    stem = Brainstem()

    # Wire chembus into autonomics
    auto.set_bus(bus)

    # Register brainstem as a chemical source
    bus.register_source(stem.emit)

    # Begin ticking loop
    auto.start()

if __name__ == "__main__":
    main()
