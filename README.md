# Godot Game Dev Skill

A portable Godot game development knowledge plugin for Claude Code and other skill-capable agents.

This skill uses the official Godot documentation as the primary source for API and engine behavior. It supports both online search against `docs.godotengine.org` and offline search against a local `godotengine/godot-docs` checkout.

## What It Covers

- Godot 4 projects and migration checks
- GDScript, C#, GDExtension, scenes, nodes, signals, and resources
- Shaders, UI, input, audio, animation, physics, navigation, networking, exports, and performance
- Lightweight gamejam/prototype guardrails
- A small curated extract from Claude-Code-Game-Studios, used only as heuristics

## Claude Code Marketplace Install

Add this repository as a Claude Code plugin marketplace:

```bash
claude plugin marketplace add JupiterTheWarlock/godot-game-dev-skill
```

Install the plugin:

```bash
claude plugin install godot-game-dev@jthewl-godot-skills
```

Inside Claude Code, the skill is namespaced as:

```text
/godot-game-dev:godot-game-dev
```

For local development before publishing changes:

```bash
claude --plugin-dir ./plugins/godot-game-dev
claude plugin validate .
```

## Manual Skill Install

If your agent does not support Claude Code plugins, copy the skill folder directly:

```bash
plugins/godot-game-dev/skills/godot-game-dev -> ~/.codex/skills/godot-game-dev
plugins/godot-game-dev/skills/godot-game-dev -> ~/.claude/skills/godot-game-dev
```

Restart the agent app after installing so it can discover the skill.

## Online Docs Search

Use this when network access is available:

```bash
python plugins/godot-game-dev/skills/godot-game-dev/scripts/search_godot_docs_online.py "CharacterBody2D move_and_slide" --version stable
python plugins/godot-game-dev/skills/godot-game-dev/scripts/search_godot_docs_online.py --class CharacterBody2D --version stable
```

Supported versions follow Godot docs URL names, such as `stable`, `latest`, `4.6`, `4.5`, or `3.6`.

## Offline Docs Search

Clone the official docs under your home directory:

```bash
git clone --depth 1 --filter=blob:none https://github.com/godotengine/godot-docs.git ~/godot-docs
```

Then search locally:

```bash
python plugins/godot-game-dev/skills/godot-game-dev/scripts/search_godot_docs.py "signal connect callable"
python plugins/godot-game-dev/skills/godot-game-dev/scripts/search_godot_docs.py --class AnimationPlayer "animation_finished"
```

You can also point to another checkout:

```bash
GODOT_DOCS_DIR=/path/to/godot-docs python plugins/godot-game-dev/skills/godot-game-dev/scripts/search_godot_docs.py "TileMapLayer"
```

Or let the script clone the docs if missing:

```bash
python plugins/godot-game-dev/skills/godot-game-dev/scripts/search_godot_docs.py "ResourceLoader threaded load" --ensure
```

## Design Notes

The skill intentionally does not vendor the full Godot docs repository. Full docs are large and change often, so the skill keeps a compact routing map and retrieval scripts instead.

Use official docs as API authority. Use bundled practical rules as implementation guardrails. Use third-party extracts only as non-authoritative heuristics.

## License

MIT.
