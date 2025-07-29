# genesis.py — v5.0
# Bootstrapper for core brain modules

from autonomics import Autonomics
from chembus import ChemBus
from brainstem import Brainstem

def main():
    bus = ChemBus()
    auto = Autonomics()
    stem = Brainstem()

    # Wire autonomics to chembus and brainstem
    auto.set_chembus(bus)
    auto.register_chemical_source(stem.emit)

    # Start the autonomics loop
    auto.start()

if __name__ == "__main__":
    main()
