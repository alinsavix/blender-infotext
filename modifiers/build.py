import math

import bpy.types

from ..functions import *
from .. import prefs

def mod_build(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
              mod: bpy.types.BuildModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_BUILD.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # START
                output_text.extend([
                    (" Start ", p.color_setting, p.text_size_normal),
                    (str(round(mod.frame_start, 2)), p.color_value, p.text_size_normal),
                ])

                # LENGTH
                output_text.extend([
                    (" Length ", p.color_setting, p.text_size_normal),
                    (str(round(mod.frame_duration, 2)), p.color_value, p.text_size_normal),
                ])

                # SEED
                if mod.use_random_order:
                    output_text.extend([
                        (" Seed ", p.color_setting, p.text_size_normal),
                        (str(mod.seed), p.color_value, p.text_size_normal),
                    ])

                if mod.use_reverse:
                    output_text.extend([(" Reversed ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
