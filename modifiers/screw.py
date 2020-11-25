import math

import bpy.types

from ..functions import *
from .. import prefs

# FIXME: Update for 2.8x/2.9x
def mod_screw(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, mod: bpy.types.ScrewModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend([" CR", ('ICON', 'ICON_MOD_SCREW.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # AXIS
                output_text.extend([
                    (" Axis ", p.color_setting, p.text_size_normal),
                    (str(mod.axis), p.color_value, p.text_size_normal),
                ])

                # AXIS OBJECT
                if mod.object:
                    output_text.extend([
                        (" Axis Object ", p.color_setting, p.text_size_normal),
                        (str(mod.object.name), p.color_value, p.text_size_normal),
                    ])

                # SCREW
                output_text.extend([
                    (" Screw ", p.color_setting, p.text_size_normal),
                    (fmt_length(mod.screw_offset, 2), p.color_value, p.text_size_normal),
                ])

                # ITERATIONS
                output_text.extend([
                    (" Iterations ", p.color_setting, p.text_size_normal),
                    (str(round(mod.iterations, 2)), p.color_value, p.text_size_normal),
                ])

                # Angle
                output_text.extend([
                    (" Angle ", p.color_setting, p.text_size_normal),
                    (str(round(math.degrees(mod.angle), 1)), p.color_value, p.text_size_normal),
                    ("°", p.color_value, p.text_size_normal),
                ])

                # STEPS
                output_text.extend([
                    (" Steps ", p.color_setting, p.text_size_normal),
                    (str(round(mod.steps, 2)), p.color_value, p.text_size_normal),
                ])

                # OPTIONS LINE 1
                if any([mod.use_normal_flip, mod.use_smooth_shade, mod.use_object_screw_offset,
                        mod.use_normal_calculate]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # USE FLIP
                    if mod.use_normal_flip:
                        output_text.extend([(" Flip ", p.color_setting, p.text_size_normal)])

                    # USE SMOOTH SHADE
                    if mod.use_smooth_shade:
                        output_text.extend([(" Smooth Shading ", p.color_setting, p.text_size_normal)])

                    # USE OBJECT SCREW OFFSET
                    # if mod.object:
                    if mod.use_object_screw_offset:
                        output_text.extend([(" Object Screw ", p.color_setting, p.text_size_normal)])

                    # CALC ORDER
                    if mod.use_normal_calculate:
                        output_text.extend([(" Calc Order ", p.color_setting, p.text_size_normal)])

                # OPTIONS LINE 2
                if any([mod.use_merge_vertices, mod.use_stretch_u, mod.use_stretch_v]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    # USE MERGE VERTICES
                    if mod.use_merge_vertices:
                        output_text.extend([
                            (" Merge Vertices ", p.color_setting, p.text_size_normal),
                            (fmt_length(mod.merge_threshold, 2), p.color_value, p.text_size_normal),
                        ])

                    # STRETCH U
                    if mod.use_stretch_u:
                        output_text.extend([(" Stretch U ", p.color_setting, p.text_size_normal)])

                    # STRETCH V
                    if mod.use_stretch_v:
                        output_text.extend([(" Stretch V ", p.color_setting, p.text_size_normal)])
        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
