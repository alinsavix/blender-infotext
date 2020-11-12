import bpy.types
import prefs

def mod_unknown(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                mod: bpy.types.Modifier) -> None:

    output_text.extend([
        "CR",
        (str(mod.type), p.color_title, p.text_size_normal),
        ("  ", p.color_title, p.text_size_normal),
        (str(mod.name), p.color_value, p.text_size_normal),
    ])

    if not mod.show_viewport:
        output_text.extend([
            (" Hidden ", p.color_warning, p.text_size_normal),
        ])

    output_text.extend([
        (" (Unknown modifier)", p.color_warning, p.text_size_normal),
    ])
