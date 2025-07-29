Rule 1: Signals, Not Symbols

The system operates through electrical (elema) and chemical (chema) matrices.
No human-readable metadata, print statements, or string-based identifiers should appear in core logic.
Let structure and signal define behavior, not descriptive text.


---

Rule 2: Modular Isolation via the Triune

Modules must not communicate directly.
All interaction occurs through:

autonomics.py (electrical routing),

chembus.py (chemical routing), and

genesis.py (orchestration/bootstrap).


Other modules are black boxes. No peeking inside. No backdoors. No cheating.


---

Rule 3: No Debugging Clutter in Live Code

The architecture must remain clean and deterministic.
Avoid developer shortcuts like:

Temporary flags,

print() calls,

Hardcoded text labels.


For diagnostics, build a dedicated sensory or cortex module. The system is allowed to introspect—not explain itself.
