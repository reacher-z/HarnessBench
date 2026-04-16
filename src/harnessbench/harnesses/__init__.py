"""Built-in HarnessBench harness plugins.

Each subpackage exports a single module-level attribute ``spec`` whose type
matches ``clawbench.HarnessSpec`` (to be surfaced by the ClawBench toolkit
refactor). The subpackage also carries ``Dockerfile``, ``setup.sh``, and
``run.sh`` for the 3-file adapter pattern.
"""
