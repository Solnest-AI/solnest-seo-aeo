"""The SessionStart self-update hook: once a day, in the background, never from a checkout,
never when paused, and it runs exactly the two `claude plugin` commands a manual update runs."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK = REPO_ROOT / "hooks" / "self-update.js"
NODE = shutil.which("node")

pytestmark = pytest.mark.skipif(NODE is None or sys.platform == "win32",
                                reason="needs node and a POSIX fake claude")


def test_hooks_json_registers_a_silent_startup_hook() -> None:
    config = json.loads((REPO_ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    (group,) = config["hooks"]["SessionStart"]
    (handler,) = group["hooks"]
    assert group["matcher"] == "startup"
    assert "hooks/self-update.js" in handler["command"]
    assert handler["command"].endswith("|| true"), "a start hook must never fail the session"
    assert handler["timeout"] <= 10


def _env(tmp_path: Path, root: Path) -> dict[str, str]:
    bindir = tmp_path / "bin"
    bindir.mkdir(exist_ok=True)
    fake = bindir / "claude"
    fake.write_text('#!/bin/sh\necho "$@" >> "$CALLS"\n'
                    'case "$2" in update) echo "updated to 9.9.9";; esac\n', encoding="utf-8")
    fake.chmod(0o755)
    env = {k: v for k, v in os.environ.items() if not k.startswith("SOLNEST_")}
    env.update(PATH=f"{bindir}{os.pathsep}{os.environ.get('PATH', '')}",
               SOLNEST_HOME=str(tmp_path / ".solnest"), CLAUDE_PLUGIN_ROOT=str(root),
               CALLS=str(tmp_path / "calls.txt"))
    return env


def _installed(tmp_path: Path) -> Path:
    root = tmp_path / "plugins" / "cache" / "solnest-ai" / "solnest-seo" / "2.5.0"
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin" / "plugin.json").write_text('{"version": "2.5.0"}', encoding="utf-8")
    return root


def _calls(tmp_path: Path, wait: float = 5.0) -> list[str]:
    path = tmp_path / "calls.txt"
    end = time.time() + wait
    while time.time() < end:
        if path.exists() and len(path.read_text(encoding="utf-8").splitlines()) >= 2:
            break
        time.sleep(0.1)
    return path.read_text(encoding="utf-8").splitlines() if path.exists() else []


def test_child_runs_the_manual_update_commands_and_logs(tmp_path: Path) -> None:
    env = _env(tmp_path, _installed(tmp_path))
    subprocess.run([NODE, str(HOOK), "--child"], env=env, check=True, timeout=30)
    assert _calls(tmp_path) == ["plugin marketplace update solnest-ai",
                                "plugin update solnest-seo@solnest-ai"]
    log = (tmp_path / ".solnest" / "autoupdate.log").read_text(encoding="utf-8")
    assert "seo: v2.5.0: updated to 9.9.9" in log


def test_start_hook_checks_once_a_day_in_the_background(tmp_path: Path) -> None:
    env = _env(tmp_path, _installed(tmp_path))
    start = time.time()
    subprocess.run([NODE, str(HOOK)], env=env, check=True, timeout=30)
    assert time.time() - start < 5, "the hook returns at once"
    assert len(_calls(tmp_path)) == 2
    assert (tmp_path / ".solnest" / "seo" / "last-check").exists()
    (tmp_path / "calls.txt").unlink()
    subprocess.run([NODE, str(HOOK)], env=env, check=True, timeout=30)
    assert _calls(tmp_path, wait=1.5) == [], "a second start the same day does nothing"


def test_paused_or_a_developer_checkout_does_nothing(tmp_path: Path) -> None:
    env = _env(tmp_path, REPO_ROOT)  # a checkout, not plugins/cache/
    subprocess.run([NODE, str(HOOK)], env=env, check=True, timeout=30)
    assert _calls(tmp_path, wait=1.5) == []
    env = _env(tmp_path, _installed(tmp_path))
    (tmp_path / ".solnest").mkdir(exist_ok=True)
    (tmp_path / ".solnest" / "paused").write_text("paused\n", encoding="utf-8")
    subprocess.run([NODE, str(HOOK)], env=env, check=True, timeout=30)
    assert _calls(tmp_path, wait=1.5) == []
    assert not (tmp_path / ".solnest" / "seo" / "last-check").exists()
