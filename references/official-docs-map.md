# Official Godot Docs Map

Primary source: official `godotengine/godot-docs`.

Default local checkout location: `~/godot-docs`.

Override location with `GODOT_DOCS_DIR`.

The official docs checkout may be `master/latest`, `stable`, or a version branch. Verify the target project's pinned engine version before using version-sensitive APIs.

## Online Search Commands

Use online search for current official docs:

```powershell
python scripts/search_godot_docs_online.py "signal connect callable" --version stable
python scripts/search_godot_docs_online.py "AnimationPlayer animation_finished" --class AnimationPlayer --version stable
python scripts/search_godot_docs_online.py --class CharacterBody2D --version stable
```

Versions map to official docs URLs such as `stable`, `latest`, `4.4`, `4.5`, `4.6`, or `3.6`.

## Local Search Commands

Use local search for offline or pinned docs:

```powershell
python scripts/search_godot_docs.py "signal connect callable" --ensure
python scripts/search_godot_docs.py "AnimationPlayer animation_finished" --class AnimationPlayer --ensure
```

Use `rg` for exact local searches:

```powershell
rg -n "move_and_slide|CharacterBody2D" ~/godot-docs
rg -n "TileMapLayer|TileMap" ~/godot-docs/tutorials ~/godot-docs/classes
```

## Topic Routing

Start with these files before falling back to broad search.

| Task | Official docs files |
|---|---|
| Godot concepts | `getting_started/introduction/key_concepts_overview.rst`, `getting_started/step_by_step/nodes_and_scenes.rst` |
| Signals | `getting_started/step_by_step/signals.rst`, `tutorials/scripting/instancing_with_signals.rst`, relevant `classes/class_*.rst` |
| GDScript language | `classes/class_@gdscript.rst`, `tutorials/scripting/gdscript/static_typing.rst`, `tutorials/scripting/gdscript/warning_system.rst` |
| Input | `getting_started/step_by_step/scripting_player_input.rst`, `tutorials/inputs/index.rst`, `classes/class_input.rst`, `classes/class_inputevent*.rst` |
| Nodes and scene instances | `tutorials/scripting/nodes_and_scene_instances.rst`, `tutorials/scripting/scene_tree.rst`, `tutorials/scripting/scene_unique_nodes.rst` |
| Resources | `tutorials/scripting/resources.rst`, `classes/class_resource.rst`, `classes/class_resourceloader.rst`, `classes/class_resourcesaver.rst` |
| Autoload/singletons | `tutorials/scripting/singletons_autoload.rst` |
| 2D gameplay | `getting_started/first_2d_game/*.rst`, `tutorials/2d/index.rst`, `classes/class_node2d.rst`, `classes/class_characterbody2d.rst` |
| 3D gameplay | `getting_started/first_3d_game/*.rst`, `tutorials/3d/index.rst`, `classes/class_node3d.rst`, `classes/class_characterbody3d.rst` |
| Physics | `tutorials/physics/index.rst`, `classes/class_physicsserver2d.rst`, `classes/class_physicsserver3d.rst`, `classes/class_area2d.rst`, `classes/class_raycast2d.rst` |
| Animation | `tutorials/animation/index.rst`, `classes/class_animationplayer.rst`, `classes/class_animationtree.rst`, `classes/class_animationmixer.rst` |
| Audio | `tutorials/audio/index.rst`, `classes/class_audiostreamplayer.rst`, `classes/class_audiostreamplayer2d.rst`, `classes/class_audiostreamplayer3d.rst`, `classes/class_audioserver.rst` |
| UI | `tutorials/ui/index.rst`, `tutorials/ui/size_and_anchors.rst`, `classes/class_control.rst`, `classes/class_container.rst`, `classes/class_richtextlabel.rst` |
| Shaders | `tutorials/shaders/index.rst`, `tutorials/shaders/shader_reference/index.rst`, `classes/class_shader.rst`, `classes/class_shadermaterial.rst` |
| Rendering/postprocess | `tutorials/rendering/index.rst`, `tutorials/3d/environment_and_post_processing.rst`, `classes/class_worldenvironment.rst`, `classes/class_environment.rst` |
| Navigation | `tutorials/navigation/index.rst`, `classes/class_navigationagent2d.rst`, `classes/class_navigationagent3d.rst`, `classes/class_navigationserver2d.rst`, `classes/class_navigationserver3d.rst` |
| Networking | `tutorials/networking/index.rst`, `classes/class_multiplayerapi.rst`, `classes/class_scenemultiplayer.rst`, `classes/class_enetmultiplayerpeer.rst` |
| Performance | `tutorials/performance/index.rst`, `tutorials/best_practices/index.rst`, `classes/class_workerthreadpool.rst`, `classes/class_thread.rst` |
| Export/platform | `tutorials/export/index.rst`, `tutorials/platform/index.rst` |
| Migration | `tutorials/migrating/index.rst`, `tutorials/migrating/upgrading_to_godot_4.4.rst`, `tutorials/migrating/upgrading_to_godot_4.5.rst`, `tutorials/migrating/upgrading_to_godot_4.6.rst` |
| Class API | `classes/class_<lowercaseclassname>.rst`, `classes/index.rst` |

## Class Reference Rule

For any named class, read the class file directly. Examples:

- `CharacterBody2D` -> `classes/class_characterbody2d.rst`
- `AnimationPlayer` -> `classes/class_animationplayer.rst`
- `TileMapLayer` -> `classes/class_tilemaplayer.rst`
- `ResourceLoader` -> `classes/class_resourceloader.rst`

If a class file and a tutorial disagree, treat the class file as API reference and the tutorial as usage guidance.
