"""Exercise the setup script with real npm/Node and a tiny offline SDK package."""

from __future__ import annotations

import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest


@pytest.mark.parametrize("module_kind", ["commonjs", "module", "broken-module"])
@pytest.mark.parametrize("requested_version", [None, "4.3.0"])
def test_setup_smokes_sdk_installed_beside_driver(tmp_path, module_kind, requested_version):
    if not shutil.which("node") or not shutil.which("npm"):
        pytest.skip("Node and npm are required for the offline Stagehand setup regression")

    # Mirror Stagehand's ESM-only export as well as its older CommonJS packaging.
    esm = module_kind != "commonjs"
    filename = "index.mjs" if esm else "index.cjs"
    exports = {"import": f"./{filename}"} if esm else f"./{filename}"
    manifest = {
        "name": "@browserbasehq/stagehand",
        "version": "4.3.0",
        "type": "module" if esm else "commonjs",
        "exports": exports,
    }
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive, mode="w:gz") as bundle:
        for name, content in {
            "package.json": json.dumps(manifest),
            filename: (
                "throw new Error('offline-import-failed');" if module_kind == "broken-module"
                else "console.log('offline-stagehand-imported');"
            ),
        }.items():
            payload = content.encode()
            info = tarfile.TarInfo(f"package/{name}")
            info.size = len(payload)
            bundle.addfile(info, io.BytesIO(payload))

    class Registry(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.endswith(".tgz"):
                payload = archive.getvalue()
            else:
                version = dict(manifest, dist={"tarball": f"{registry_url}/stagehand.tgz"})
                payload = json.dumps({
                    "name": manifest["name"],
                    "dist-tags": {"latest": "4.3.0"},
                    "versions": {"4.3.0": version},
                }).encode()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *_args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Registry)
    registry_url = f"http://127.0.0.1:{server.server_port}"
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        harness = tmp_path / "harness with spaces"
        harness.mkdir()
        script = harness / "setup.sh"
        shutil.copyfile(
            Path(__file__).parents[1] / "src/harnessbench/harnesses/stagehand/setup.sh", script
        )
        stubs = tmp_path / "bin"
        stubs.mkdir()
        # Only the OS installer commands are replaced: npm and Node run for real.
        for name, body in {
            "curl": 'printf "%s\\n" "$*" > "$INSTALL_REQUEST"\nprintf "# offline installer\\n"\n',
            "apt-get": "exit 0\n",
        }.items():
            command = stubs / name
            command.write_text("#!/bin/sh\n" + body)
            command.chmod(0o755)
        env = dict(os.environ)
        env.pop("NODE_PATH", None)
        env.update({
            "PATH": f"{stubs}{os.pathsep}{env['PATH']}",
            "INSTALL_REQUEST": str(tmp_path / "installer-request"),
            "npm_config_registry": registry_url,
            "npm_config_cache": str(tmp_path / "npm-cache"),
            "npm_config_prefix": str(tmp_path / "global-prefix"),
            "npm_config_audit": "false",
            "npm_config_fund": "false",
            "STAGEHAND_VERSION": "4.3.0",
        })
        env.pop("STAGEHAND_VERSION", None)
        if requested_version is not None:
            env["STAGEHAND_VERSION"] = requested_version
        result = subprocess.run(
            ["bash", str(script)], cwd=tmp_path, env=env,
            capture_output=True, text=True, timeout=60,
        )
        if module_kind == "broken-module":
            assert result.returncode != 0
            assert "offline-import-failed" in result.stderr
        else:
            assert result.returncode == 0, result.stdout + result.stderr
            assert "offline-stagehand-imported" in result.stdout
        assert "setup_22.x" in (tmp_path / "installer-request").read_text()
        assert (harness / "node_modules/@browserbasehq/stagehand/package.json").is_file()
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)
