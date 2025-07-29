# Prometheus 1.0

Prometheus 1.0 implements a minimal triune-brain architecture. The system is
composed of three cooperating modules that exchange electrical and chemical
signals to emulate a nervous system.

## Modules

- **Autonomics (`autonomics.py`)** – Drives the global electrical rhythm. It
  polls the chemical bus to determine wave amplitudes and emits pulses to
  registered clocks and callbacks.
- **ChemBus (`chembus.py`)** – A global chemical message bus. It collects
  chemical packets, exposes the current wave amplitudes and allows consumers to
  retrieve matching chemical records.
- **Brainstem (`brainstem.py`)** – Monitors host resources using `psutil` and
  outputs chemical packets that influence the autonomic rhythms.
- **Constants (`constants.py`)** – Shared sigils and base wave frequencies.
- **Genesis (`genesis.py`)** – Orchestrates the system by wiring Autonomics,
  ChemBus and Brainstem together and starting the loop.
- **Rules (`RULES.md`)** – Describes the coding principles for the project,
  emphasizing signal-based communication, modular isolation and clean code.

## Setup

1. Ensure Python 3 is installed.
2. Install required dependencies:

   ```bash
   pip install psutil
3. Start the system:

   ```bash
   python genesis.py


This README summarizes the system’s purpose, outlines each module in the triune-brain architecture, references `RULES.md` for coding principles, and provides setup instructions to run `genesis.py`.
   
