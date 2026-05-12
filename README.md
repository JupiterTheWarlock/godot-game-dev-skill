# Godot Game Dev Skill

A portable knowledge skill for Godot game development agents.

This skill uses the official Godot documentation as the primary source for API and engine behavior. It supports both online search against `docs.godotengine.org` and offline search against a local `godotengine/godot-docs` checkout.

## What It Covers

- Godot 4 projects and migration checks
- GDScript, C#, GDExtension, scenes, nodes, signals, and resources
- Shaders, UI, input, audio, animation, physics, navigation, networking, exports, and performance
- Lightweight gamejam/prototype guardrails
- A small curated extract from Claude-Code-Game-Studios, used only as heuristics

## Install

Copy this folder into any agent skill directory, for example:

```bash
~/.codex/skills/godot-game-dev
~/.claude/skills/godot-game-dev
```

Restart the agent app after installing so it can discover the skill.

## Online Docs Search

Use this when network access is available:

```bash
python scripts/search_godot_docs_online.py "CharacterBody2D move_and_slide" --version stable
python scripts/search_godot_docs_online.py --class CharacterBody2D --version stable
```

Supported versions follow Godot docs URL names, such as `stable`, `latest`, `4.6`, `4.5`, or `3.6`.

## Offline Docs Search

Clone the official docs under your home directory:

```bash
git clone --depth 1 --filter=blob:none https://github.com/godotengine/godot-docs.git ~/godot-docs
```

Then search locally:

```bash
python scripts/search_godot_docs.py "signal connect callable"
python scripts/search_godot_docs.py --class AnimationPlayer "animation_finished"
```

You can also point to another checkout:

```bash
GODOT_DOCS_DIR=/path/to/godot-docs python scripts/search_godot_docs.py "TileMapLayer"
```

Or let the script clone the docs if missing:

```bash
python scripts/search_godot_docs.py "ResourceLoader threaded load" --ensure
```

## Design Notes

The skill intentionally does not vendor the full Godot docs repository. Full docs are large and change often, so the skill keeps a compact routing map and retrieval scripts instead.

Use official docs as API authority. Use bundled practical rules as implementation guardrails. Use third-party extracts only as non-authoritative heuristics.

## License

MIT.
