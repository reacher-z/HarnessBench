# HarnessBench / browser-use — installs the browser-use package on top of
# clawbench-base. Attaches to the running Chrome via Playwright CDP.
FROM ghcr.io/reacher-z/clawbench-base:latest

COPY setup.sh /opt/harness/setup.sh
COPY run.sh   /opt/harness/run.sh
RUN chmod +x /opt/harness/setup.sh /opt/harness/run.sh && /opt/harness/setup.sh

ENTRYPOINT ["/opt/harness/run.sh"]
