# Installation Guide

> **The supported install is [INSTALL.md](../INSTALL.md).** Paste one block into Claude Code
> and it registers the plugin for you. This page covers the manual install, where the skills
> are copied into `~/.claude/skills/` instead. Pick one. Running both leaves you with two
> copies of every skill.

## Prerequisites

- **Python 3.10+** with pip
- **Git** for cloning the repository
- **Claude Code CLI** installed and configured

Optional:
- **Playwright Chromium** - install.sh attempts this automatically; failure is non-fatal; needed only for SPA rendering and screenshots

## Quick Install

### Plugin Install (Claude Code 1.0.33+)

The recommended path. Inside Claude Code:

```
/plugin marketplace add Solnest-AI/solnest-seo-aeo
/plugin install solnest-seo@solnest-ai
/solnest-seo:seo setup
```

You have to type these yourself — they are interactive slash commands, so Claude cannot run
them for you. If the `/plugin` browser is not available in your client, use the declarative
block in [INSTALL.md](../INSTALL.md) instead.

Plugin installation does not run package managers. `/solnest-seo:seo setup` is an explicit,
one-time provisioning step that writes the virtual environment and browser only
to Claude's persistent plugin data. Use `/solnest-seo:seo doctor` for a read-only check.

### Manual Install (Unix, macOS, Linux)

```bash
git clone --depth 1 https://github.com/Solnest-AI/solnest-seo-aeo.git
bash solnest-seo-aeo/install.sh
```

Review-then-run alternative:

```bash
curl -fsSL https://raw.githubusercontent.com/Solnest-AI/solnest-seo-aeo/main/install.sh > install.sh
cat install.sh        # review
bash install.sh       # run when satisfied
rm install.sh
```

### Manual Install (Windows, PowerShell)

```powershell
git clone --depth 1 https://github.com/Solnest-AI/solnest-seo-aeo.git
powershell -ExecutionPolicy Bypass -File solnest-seo-aeo\install.ps1
```

The Windows path uses `git clone` rather than `irm | iex` because Claude Code's own security guardrails flag piped remote-script execution. Inspect `install.ps1` before running.

## Manual Installation

1. **Clone the repository**

```bash
git clone https://github.com/Solnest-AI/solnest-seo-aeo.git
cd solnest-seo-aeo
```

2. **Run the installer**

```bash
./install.sh
```

3. **Verify the managed runtime**

The installer delegates dependency and Chromium provisioning to the same runtime
used by every skill. It creates `~/.claude/skills/seo/.venv/` and never falls
back to global or user package installation.

```bash
~/.claude/skills/seo/bin/claude-seo doctor
```

If core setup failed, rerun the inspected installer. If only Chromium failed,
the installer reports a degraded result and raw-fetch analysis remains available.

## Installation Paths

The installer copies files to:

| Component | Path |
|-----------|------|
| Main skill | `~/.claude/skills/seo/` |
| Sub-skills | `~/.claude/skills/seo-*/` |
| Subagents | `~/.claude/agents/seo-*.md` |
| Runtime launcher | `~/.claude/skills/seo/bin/claude-seo` |
| Isolated Python | `~/.claude/skills/seo/.venv/` |

## Verify Installation

1. Start Claude Code:

```bash
claude
```

2. Check that the skill is loaded:

```
/seo
```

You should see a help message or prompt for a URL.

## Uninstallation

If installed as a plugin:

```
/plugin uninstall solnest-seo@solnest-ai
/plugin marketplace remove Solnest-AI/solnest-seo-aeo
```

If installed manually, run the uninstaller from a fresh clone:

```bash
git clone --depth 1 https://github.com/Solnest-AI/solnest-seo-aeo.git
bash solnest-seo-aeo/uninstall.sh
```

`uninstall.sh` removes all installed sub-skills, sub-agents, and the plugin's MCP entries from `~/.claude/settings.json`. Do not maintain a hand-coded `rm` list. The shipped uninstaller is the canonical source.

## Upgrading

To upgrade to the latest version:

Caution: Prefer downloading, inspecting, then running remote scripts; the pipe-to-shell form below is the less-safe convenience option.

```bash
# Uninstall current version
curl -fsSL https://raw.githubusercontent.com/Solnest-AI/solnest-seo-aeo/main/uninstall.sh | bash

# Install new version
curl -fsSL https://raw.githubusercontent.com/Solnest-AI/solnest-seo-aeo/main/install.sh | bash
```

## Troubleshooting

### "Skill not found" error

Ensure the skill is installed in the correct location:

```bash
ls ~/.claude/skills/seo/SKILL.md
```

If the file doesn't exist, re-run the installer.

### Python dependency errors

Run the managed setup again:

```bash
~/.claude/skills/seo/bin/claude-seo setup
```

### Playwright screenshot errors

Run the managed setup again and inspect the result:

```bash
~/.claude/skills/seo/bin/claude-seo setup
~/.claude/skills/seo/bin/claude-seo doctor
```

### Permission errors on Unix

Make sure scripts are executable:

```bash
chmod +x ~/.claude/skills/seo/scripts/*.py
```
