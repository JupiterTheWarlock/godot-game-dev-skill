# Godot Practical Rules

Use these as compact guardrails after checking official docs.

## Version Discipline

- Confirm the target project version from `project.godot`, export presets, README, or user context.
- The bundled official docs clone is `master/latest`, currently configured for Godot `4.7`; do not silently assume a Godot 4.6 or 4.7 project.
- Check migration docs for 4.x version-sensitive changes before using newly added APIs.

## GDScript

- Prefer static typing for exported variables, locals, parameters, return values, arrays, and dictionaries.
- Prefer `@onready var node: Type = %Node` or explicit cached paths over repeated `$Node` lookups in hot paths.
- Prefer `await some_signal` over Godot 3 `yield()`.
- Prefer `PackedScene.instantiate()` over `instance()`.
- Prefer callable signal connections such as `button.pressed.connect(_on_pressed)` over old string-based connection forms.
- Use `StringName` literals such as `&"move_left"` in repeated input checks or signal/action names.
- Keep per-frame allocation low: avoid constructing arrays, dictionaries, lambdas, and strings inside `_process()` or `_physics_process()` unless measured as harmless.

## Scenes, Nodes, and Resources

- Let scenes own their local behavior. Avoid broad global managers for systems that can be scene-local.
- Use signals for decoupled event notifications, especially UI/VFX/SFX reactions and child-to-parent communication.
- Use direct method calls when the relationship is explicit, the caller needs a return value, or the path is performance-critical.
- Use resources for data definitions and tunable content when many scene instances share the same schema.
- Duplicate mutable resources intentionally when per-instance state is needed.

## Prototype and Gamejam Bias

- Prefer a working vertical slice over a large framework.
- Use exported tuning variables for speed, damage, timing windows, spawn rates, colors, and audio levels.
- Keep node names and signal names boring and discoverable.
- Add abstraction only when two or more systems already need the same behavior.
- If a system will be replaced after validation, isolate it under `prototypes/` or a clearly named scene/script.

## Review Checklist

Before finalizing Godot code:

- Does it match the project Godot version?
- Are node paths and scene dependencies explicit?
- Are hot paths typed and allocation-conscious?
- Are signals documented by names and payload shape where cross-system?
- Are UI strings/localization concerns handled if user-facing?
- Did you run the smallest relevant Godot command or project test available?
