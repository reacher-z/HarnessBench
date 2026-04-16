# HarnessBench / openclaw — re-uses ClawBench's reference harness image.
#
# Once clawbench ships `ghcr.io/reacher-z/clawbench-base:<version>`, this
# file becomes a one-line FROM. For now we reference the bundled data
# tree via the clawbench-eval wheel; during build the setup script copies
# the three needed files into the context.
FROM ghcr.io/reacher-z/clawbench-base:latest

COPY setup.sh /opt/harness/setup.sh
COPY run.sh   /opt/harness/run.sh
RUN chmod +x /opt/harness/setup.sh /opt/harness/run.sh && /opt/harness/setup.sh

ENTRYPOINT ["/opt/harness/run.sh"]
