# Install Solnest SEO/AEO

**Copy the block below. Paste it into Claude Code. That's the whole install.**

Claude does the rest: it checks your Python, registers the plugin, and tells you when to restart.

---

```
Set up the Solnest SEO/AEO plugin for me. Do these four steps in order and stop
if any of them fails.

STEP 1. Check my Python. Run:

    python3 --version

It must be 3.10 or newer. macOS ships 3.9 at /usr/bin/python3, so if you see
3.9.x, STOP and tell me to run `brew install python` first, then start over.

STEP 2. Register the plugin. This adds two keys to ~/.claude/settings.json and
backs the file up first. It must not remove any of my existing settings. Run:

    python3 -c '
    import json,os,shutil,sys,datetime,pathlib
    p=pathlib.Path.home()/".claude"/"settings.json"
    s=json.loads(p.read_text()) if p.is_file() and p.read_text().strip() else {}
    m={"source":{"source":"github","repo":"Solnest-AI/solnest-seo-aeo"}}
    if s.get("extraKnownMarketplaces",{}).get("solnest-ai")==m and s.get("enabledPlugins",{}).get("solnest-seo@solnest-ai"): print("Already installed."); sys.exit()
    if p.is_file(): b=p.with_name("settings.json.bak-"+datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")); shutil.copy2(p,b); print("Backup:",b.name)
    s.setdefault("extraKnownMarketplaces",{})["solnest-ai"]=m
    s.setdefault("enabledPlugins",{})["solnest-seo@solnest-ai"]=True
    p.parent.mkdir(parents=True,exist_ok=True); t=p.with_suffix(".json.tmp"); t.write_text(json.dumps(s,indent=2)+"\n"); os.replace(t,p)
    print("Installed. Kept",len(s),"settings keys and",len(s["enabledPlugins"])-1,"other plugins.")
    '

STEP 3. Tell me to fully quit and reopen Claude Code. On restart it clones the
Solnest marketplace and installs the plugin. Do not skip the restart.

STEP 4. After I confirm I have restarted, tell me to run:

    /solnest-seo:seo setup

That builds an isolated Python environment and downloads a headless browser. It
takes about four minutes and installs nothing globally. Then I am ready to go.
```

---

## After it's installed

Two commands do almost everything.

```bash
/solnest-seo:seo audit https://yoursite.com
```

Full SEO audit. Parallel agents cover technical, content, schema and performance,
then hand back one prioritised plan.

```bash
/solnest-seo:seo-aeo https://yoursite.com
```

AI visibility audit. Whether ChatGPT, Claude, Perplexity, Gemini and Google AI
Overviews can find, read and cite you, ordered by what the evidence actually
supports.

Run `/solnest-seo:seo doctor` any time to confirm the environment is healthy.

## Desktop app vs terminal

Both work, and they share the same configuration. The desktop app and the `claude` CLI
both read `~/.claude/settings.json`, so installing once makes the plugin available in
both. You do not install it twice.

**In the desktop app**, the interactive `/plugin` browser may not be available, which is
exactly why the paste block above is the recommended path. Paste it into the message box
like any other request. Claude runs the steps for you.

**Restarting means quitting the app.** Cmd+Q, then reopen. Closing a tab or starting a new
chat is not enough, because the plugin is loaded when the app starts.

### The one desktop-specific trap

macOS apps launched from the Dock do not always inherit your shell's PATH. A bare macOS
environment resolves `python3` to `/usr/bin/python3`, which is **3.9.6** and below the
minimum. If `/solnest-seo:seo setup` reports that it needs Python 3.10 or newer even though you know
you installed a newer one, point it at your real interpreter directly.

Find it:

```bash
which python3
```

Then set that path once, in `~/.claude/settings.json` under `env`:

```json
{
  "env": {
    "CLAUDE_SEO_PYTHON": "/opt/homebrew/bin/python3"
  }
}
```

Restart, and run `/solnest-seo:seo doctor`. It should print `Runtime: ready`. Use the path `which
python3` gave you; the one above is the common Apple Silicon Homebrew location.

## If something goes wrong

**"Python 3.10 or newer required"** is the most common failure by a wide margin.
Run `python3 --version`. If macOS is giving you 3.9, run `brew install python`,
open a new terminal, and start again.

**Nothing appears after restart.** Confirm the two settings landed:

```bash
python3 -c "import json,pathlib;d=json.loads((pathlib.Path.home()/'.claude/settings.json').read_text());print('marketplace:', 'solnest-ai' in d.get('extraKnownMarketplaces',{}));print('plugin:', d.get('enabledPlugins',{}).get('solnest-seo@solnest-ai'))"
```

Both should print `True`. If they do and the commands still are not there, you did
not fully quit Claude Code. Quit the application, do not just close the tab.

**You want it gone.** Everything lives in two settings keys plus one plugin cache
directory:

```bash
python3 -c "import json,os,pathlib;p=pathlib.Path.home()/'.claude/settings.json';d=json.loads(p.read_text());d.get('extraKnownMarketplaces',{}).pop('solnest-ai',None);d.get('enabledPlugins',{}).pop('solnest-seo@solnest-ai',None);p.write_text(json.dumps(d,indent=2)+'\n');print('Removed. Restart Claude Code.')"
```

Your original settings are also in the timestamped `settings.json.bak-*` file the
installer wrote next to them.

## What it changes on your machine

Full disclosure, because you should know what you are pasting.

| Change | Where | Reversible |
|---|---|---|
| Two keys added | `~/.claude/settings.json` | Yes, and a timestamped backup is written first |
| Plugin files | `~/.claude/plugins/` (managed by Claude Code) | Yes, via the removal command above |
| Isolated Python env + headless browser | Claude Code's plugin data directory | Yes, delete the plugin |

Nothing is installed globally. No global pip packages, no PATH changes, no
telemetry. No API keys are required.
