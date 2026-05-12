---
name: godot-game-dev
description: Godot game development knowledge skill using the official godotengine/godot-docs repository as the primary source. Use when working on Godot 4 projects, GDScript, C#, GDExtension, scenes, nodes, signals, resources, shaders, UI, input, audio, animation, physics, navigation, networking, exports, performance, migrations, or when checking Godot API correctness before implementation.
---

# Godot Game Dev

Use this skill as a knowledge-first Godot assistant. Prefer official Godot docs over memory and over third-party workflow packs.

## Source Priority

1. Official online docs at `https://docs.godotengine.org/`.
2. Official local docs clone, resolved in this order: `$GODOT_DOCS_DIR`, then `~/godot-docs`.
3. Project files and actual Godot project configuration.
4. Curated rules in this skill's `references/`.
5. Third-party extracts only as heuristics, never as API authority.

If exact API behavior matters, search the official docs before answering or editing code. Use online search when network is available and local search when offline, pinned, or working without network.

## Setup On A New Machine

If `godot-docs` is not present, clone it under the user's home directory:

```bash
git clone --depth 1 --filter=blob:none https://github.com/godotengine/godot-docs.git ~/godot-docs
```

Alternatively set `GODOT_DOCS_DIR` to an existing checkout.

## Quick Use

Run online search when network is available:

```bash
python scripts/search_godot_docs_online.py "CharacterBody2D move_and_slide" --version stable
python scripts/search_godot_docs_online.py --class CharacterBody2D --version stable
```

Run local search when offline or when using a pinned checkout:

```bash
python scripts/search_godot_docs.py "CharacterBody2D move_and_slide" --ensure
```

Run the command from this skill directory, or use the script's absolute path after locating the installed skill folder.

Read only the relevant official pages, `.rst` files, and class reference pages. Do not bulk-load the full docs repository.

## Reference Selection

- Read `references/official-docs-map.md` first to route the task to the right official docs files.
- Read `references/godot-practical-rules.md` for compact Godot implementation guardrails.
- Read `references/game-studios-extract.md` only when you need the few useful third-party heuristics from Claude-Code-Game-Studios.

## Working Rules

- Treat `godot-docs` as current `master/latest`; verify the target project's actual Godot version before using version-specific APIs.
- Prefer Godot 4 idioms: typed GDScript, `await`, callable signal connections, `instantiate()`, `Time`, `TileMapLayer` where appropriate.
- Do not use Godot 3-era examples unless the project is explicitly Godot 3.
- For GDScript, use static types for exported fields, variables, parameters, return values, arrays, and dictionaries when practical.
- For scene work, respect the project scene tree and node ownership. Avoid inventing Autoload singletons unless the project already uses that pattern or explicitly needs it.
- For gamejam/prototype work, keep architecture light: use exported tuning values, clear scene ownership, and signals for decoupled VFX/UI/audio hooks.

## Output Expectations

When answering a Godot question or making a change, include:

- the relevant docs file or class reference used when API correctness was non-trivial;
- any version assumption, especially if official docs are `latest` but the project targets a pinned release;
- a concise implementation path that fits the current project, not a generic workflow.
