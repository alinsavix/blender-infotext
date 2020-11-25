import math

import bpy.types

from ..functions import *
from .. import prefs

def mod_remesh(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
               mod: bpy.types.RemeshModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_REMESH.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                output_text.extend([
                    (" ", p.color_title, p.text_size_normal),
                    (str(mod.mode), p.color_value, p.text_size_normal),
                ])

                if mod.mode != "VOXEL":
                    # OCTREE DEPTH
                    output_text.extend([
                        (" Octree Depth ", p.color_setting, p.text_size_normal),
                        (str(mod.octree_depth), p.color_value, p.text_size_normal),
                    ])

                    # SCALE
                    output_text.extend([
                        (" Scale ", p.color_setting, p.text_size_normal),
                        (str(round(mod.scale, 2)), p.color_value, p.text_size_normal),
                    ])

                # SHARPNESS
                if mod.mode == 'SHARP':
                    output_text.extend([
                        (" Sharpness ", p.color_setting, p.text_size_normal),
                        (str(round(mod.sharpness, 2)), p.color_value, p.text_size_normal),
                    ])

                # OPTIONS
                if any([mod.use_smooth_shade, mod.use_remove_disconnected]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # SMOOTH SHADING
                    if mod.use_smooth_shade:
                        output_text.extend([(" Smooth Shading ", p.color_setting, p.text_size_normal)])

                    # REMOVE DISCONNECTED
                    if mod.mode != "VOXEL" and mod.use_remove_disconnected:
                        output_text.extend([
                            (" Remove Disconnected Pieces ", p.color_setting, p.text_size_normal),
                            (str(round(mod.threshold, 2)), p.color_value, p.text_size_normal),
                        ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
