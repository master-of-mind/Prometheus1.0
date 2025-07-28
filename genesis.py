# genesis.py — v4.1
# Bootstrapper for the unified brain system

from autonomics import Autonomics
from brainstem import Brainstem

def main():
    core = Autonomics()

    # Instantiate and register brainstem only
    brainstem = Brainstem()
    core.register_mod(brainstem)
    core.register_chemical_source(brainstem.emit)

    # Boot system
    core.start()

if __name__ == "__main__":
    main()
