import math

import bpy.types

from ..functions import *
from .. import prefs

def mod_smooth(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
               mod: bpy.types.SmoothModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    output_text.extend([(" Axis ", p.color_setting, p.text_size_normal)])

                    if mod.use_x:
                        output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                    if mod.use_y:
                        output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                    if mod.use_z:
                        output_text.extend([(" Z ", p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" No Axis Selected ", p.color_warning, p.text_size_normal)])

                # FACTOR
                output_text.extend([
                    (" Factor ", p.color_setting, p.text_size_normal),
                    (str(round(mod.factor, 2)), p.color_value, p.text_size_normal),
                ])

                # ITERATIONS
                output_text.extend([
                    (" Repeat ", p.color_setting, p.text_size_normal),
                    (str(mod.iterations), p.color_value, p.text_size_normal),
                ])

                # OPTIONS
                if mod.vertex_group:
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (mod.vertex_group, p.color_value, p.text_size_normal),
                    ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
