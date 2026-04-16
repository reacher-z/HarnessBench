# HarnessBench / hermes — installs Nous Research's hermes-agent on top of
# the clawbench-base image (Chrome + Xvfb + FFmpeg + extension-server
# already present). The agent attaches to the running Chrome on CDP 9222.
FROM ghcr.io/reacher-z/clawbench-base:latest

COPY setup.sh /opt/harness/setup.sh
COPY run.sh   /opt/harness/run.sh
RUN chmod +x /opt/harness/setup.sh /opt/harness/run.sh && /opt/harness/setup.sh

ENTRYPOINT ["/opt/harness/run.sh"]
