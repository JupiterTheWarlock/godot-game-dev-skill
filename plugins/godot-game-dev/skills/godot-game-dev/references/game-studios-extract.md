# Claude-Code-Game-Studios Extract

Optional source repo: https://github.com/Donchitos/Claude-Code-Game-Studios

Use this file only for useful heuristics. Do not adopt the repository's workflow, role hierarchy, approval gates, or slash-command lifecycle.

## Useful Extracts

- Keep engine knowledge version-pinned and separate from workflow instructions.
- Maintain a direct stale-pattern map: deprecated API -> replacement -> version note.
- Treat `.gd`, `.gdshader`, `.tscn`, C#, and GDExtension as different knowledge surfaces.
- Require engine-version checks before suggesting APIs introduced after the model's knowledge cutoff.
- Prefer compact subsystem references over monolithic prompts.

## Godot Heuristics Worth Keeping

- Signals: good for decoupled one-to-many notifications, UI/audio/VFX reactions, and child-to-parent communication.
- Direct calls: good for tight ownership, return values, and hot paths.
- GDScript: review type annotations and avoid untyped arrays in update-heavy code.
- C#: useful for CPU-heavy loops, but do not migrate without profiling evidence.
- GDExtension: reserve for extreme performance or native library integration; verify ABI and rebuild on minor engine upgrades.
- Shaders: Godot uses its own shading language; do not output HLSL or raw GLSL unless explicitly translating concepts.

## What To Ignore

- Multi-agent studio hierarchy.
- Director gates and phase transition ceremony.
- Mandatory ADR/story/sprint files for small prototypes.
- Approval-heavy "may I write" loops when Codex is already operating in a coding task.
- Any version claims that conflict with the official Godot docs clone.
