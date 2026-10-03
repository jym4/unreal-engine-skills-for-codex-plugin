"""Export actors from the currently open Unreal Editor world to a CSV file.

Run from Unreal Editor with File > Execute Python Script.
The CSV is written to <Project>/Saved/CurrentLevelActors.csv.
"""

import csv
import os
import unreal


def get_editor_actors():
    """Use the current actor subsystem, with a fallback for older Unreal versions."""
    subsystem_class = getattr(unreal, "EditorActorSubsystem", None)
    get_editor_subsystem = getattr(unreal, "get_editor_subsystem", None)

    if subsystem_class is not None and get_editor_subsystem is not None:
        subsystem = get_editor_subsystem(subsystem_class)
        if subsystem is not None:
            return subsystem.get_all_level_actors()

    # Deprecated in newer Unreal versions, but available in older editor builds.
    legacy_library = getattr(unreal, "EditorLevelLibrary", None)
    if legacy_library is not None:
        return legacy_library.get_all_level_actors()

    raise RuntimeError(
        "Could not find an Unreal Editor actor-listing API. "
        "Check that the Python Editor Script Plugin is enabled."
    )


actors = get_editor_actors()
saved_dir = unreal.Paths.project_saved_dir()
output_path = os.path.join(saved_dir, "CurrentLevelActors.csv")

with open(output_path, "w", newline="", encoding="utf-8-sig") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Actor Label", "Object Name", "Class", "X", "Y", "Z"])

    for actor in actors:
        location = actor.get_actor_location()
        writer.writerow([
            actor.get_actor_label(),
            actor.get_name(),
            actor.get_class().get_name(),
            "{:.3f}".format(location.x),
            "{:.3f}".format(location.y),
            "{:.3f}".format(location.z),
        ])

unreal.log(
    "Exported {} actors to {}".format(len(actors), output_path)
)
