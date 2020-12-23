# Roadmap

- Build mobile nodes and sinks  **Update 26.08:** *only sinks missing now*
- ✅ Define an algorithm to create paths for mobile nodes:
    - Option 1: A*-like algorithm  **Update 26.08:** *done this* ✅
    - *~~Option 2: find next waypoint every time the target one is reached~~*
- Build the overall simulator (clock, avg and confidence intervals measurements, ...)
    - Optimize the number of distance checks, in order to avoid O(n^2) distance measurements every clock tick
- Extend the simulator in order to emulate disaster scenarios