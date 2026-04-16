# HarnessBench / claw-code — installs Rust toolchain on top of
# clawbench-base and builds the claw-code CLI binary.
FROM ghcr.io/reacher-z/clawbench-base:latest

COPY setup.sh /opt/harness/setup.sh
COPY run.sh   /opt/harness/run.sh
RUN chmod +x /opt/harness/setup.sh /opt/harness/run.sh && /opt/harness/setup.sh

ENTRYPOINT ["/opt/harness/run.sh"]
