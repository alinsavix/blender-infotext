import math

import bpy.types

from ..functions import *
from .. import prefs

def mod_mask(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
             mod: bpy.types.MaskModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MASK.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # ARMATURE
                if mod.mode == 'ARMATURE':
                    if mod.armature:
                        output_text.extend([
                            (" Armature ", p.color_setting, p.text_size_normal),
                            (str(mod.armature.name), p.color_value, p.text_size_normal),
                        ])
                    else:
                        output_text.extend([(" No Armature Selected ", p.color_warning, p.text_size_normal)])

                # VERTEX GROUP
                elif mod.mode == 'VERTEX_GROUP':
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", p.color_setting, p.text_size_normal),
                            (str(mod.vertex_group), p.color_value, p.text_size_normal),
                        ])
                    else:
                        output_text.extend([(" No Vertex Group Selected ", p.color_warning, p.text_size_normal)])
        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
