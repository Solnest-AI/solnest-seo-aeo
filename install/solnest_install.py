#!/usr/bin/env python3
"""
Solnest SEO/AEO installer.

Registers the Solnest marketplace and enables the plugin by MERGING two keys
into ~/.claude/settings.json. Never overwrites unrelated settings, and is safe
to run more than once.

Usage:
    python3 solnest_install.py            # install
    python3 solnest_install.py --check    # report state, change nothing
    python3 solnest_install.py --uninstall
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

MARKETPLACE = "solnest-ai"
PLUGIN = "solnest-seo"
REPO = "Solnest-AI/solnest-seo-aeo"
PLUGIN_KEY = f"{PLUGIN}@{MARKETPLACE}"
SETTINGS = Path.home() / ".claude" / "settings.json"
MIN_PY = (3, 10)


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return {}
    return json.loads(text)


def _atomic_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".solnest-tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def check_python() -> tuple[bool, str]:
    for exe in ("python3", "python"):
        found = shutil.which(exe)
        if not found:
            continue
        try:
            out = subprocess.run(
                [found, "-c", "import sys;print('%d.%d' % sys.version_info[:2])"],
                capture_output=True, text=True, timeout=20)
            major, minor = (int(x) for x in out.stdout.strip().split("."))
            if (major, minor) >= MIN_PY:
                return True, f"{found} is Python {major}.{minor}"
        except Exception:
            continue
    return False, ("No Python 3.10+ found. macOS ships 3.9 at /usr/bin/python3. "
                   "Install a current Python (brew install python) and run this again.")


def install() -> int:
    ok, msg = check_python()
    print(f"Python check: {msg}")
    if not ok:
        return 2

    try:
        settings = _load(SETTINGS)
    except json.JSONDecodeError as exc:
        print(f"\n{SETTINGS} is not valid JSON ({exc}).")
        print("Fix or move that file, then run this again. Nothing was changed.")
        return 3

    desired_market = {"source": {"source": "github", "repo": REPO}}
    already = (settings.get("extraKnownMarketplaces", {}).get(MARKETPLACE) == desired_market
               and settings.get("enabledPlugins", {}).get(PLUGIN_KEY) is True)

    if already:
        print("\nAlready installed. Nothing to change, no backup written.")
    else:
        # Back up only when we are actually about to modify the file, so repeat
        # runs do not litter the directory with identical backups.
        if SETTINGS.is_file():
            backup = SETTINGS.with_name(
                f"settings.json.bak-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}")
            shutil.copy2(SETTINGS, backup)
            print(f"Backed up existing settings to {backup.name}")
            print(f"Preserving {len(settings)} existing top-level key(s): "
                  f"{', '.join(sorted(settings)) or 'none'}")

        markets = settings.setdefault("extraKnownMarketplaces", {})
        plugins = settings.setdefault("enabledPlugins", {})
        markets[MARKETPLACE] = desired_market
        plugins[PLUGIN_KEY] = True
        _atomic_write(SETTINGS, settings)
        print(f"\nRegistered marketplace '{MARKETPLACE}' -> {REPO}")
        print(f"Enabled plugin '{PLUGIN_KEY}'")
        print(f"Other plugins left untouched: "
              f"{len([k for k in plugins if k != PLUGIN_KEY])}")

    print("\nNext:")
    print("  1. Restart Claude Code. It clones the marketplace and installs the plugin.")
    print("  2. Run:  /seo setup           (builds an isolated Python env, ~4 minutes)")
    print("  3. Try:  /solnest-seo:seo-aeo https://yoursite.com")
    return 0


def uninstall() -> int:
    try:
        settings = _load(SETTINGS)
    except json.JSONDecodeError:
        print(f"{SETTINGS} is not valid JSON. Nothing changed.")
        return 3
    changed = False
    if settings.get("extraKnownMarketplaces", {}).pop(MARKETPLACE, None) is not None:
        changed = True
    if settings.get("enabledPlugins", {}).pop(PLUGIN_KEY, None) is not None:
        changed = True
    if changed:
        _atomic_write(SETTINGS, settings)
        print("Removed the Solnest marketplace and plugin entries. Restart Claude Code.")
    else:
        print("Not installed. Nothing to remove.")
    return 0


def check() -> int:
    ok, msg = check_python()
    print(f"Python 3.10+:      {'yes' if ok else 'NO'}  ({msg})")
    print(f"settings.json:     {SETTINGS} {'exists' if SETTINGS.is_file() else 'MISSING (will be created)'}")
    try:
        s = _load(SETTINGS)
    except json.JSONDecodeError as exc:
        print(f"settings.json:     INVALID JSON ({exc})")
        return 3
    m = s.get("extraKnownMarketplaces", {}).get(MARKETPLACE)
    p = s.get("enabledPlugins", {}).get(PLUGIN_KEY)
    print(f"marketplace:       {'registered' if m else 'not registered'}")
    print(f"plugin enabled:    {'yes' if p else 'no'}")
    return 0 if (ok and m and p) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Install Solnest SEO/AEO for Claude Code")
    ap.add_argument("--check", action="store_true", help="report state, change nothing")
    ap.add_argument("--uninstall", action="store_true", help="remove the settings entries")
    args = ap.parse_args()
    if args.check:
        return check()
    if args.uninstall:
        return uninstall()
    return install()


if __name__ == "__main__":
    sys.exit(main())
