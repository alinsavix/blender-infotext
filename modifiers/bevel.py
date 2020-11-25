import math

import bpy.types

from ..functions import *
from .. import prefs

def mod_bevel(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
              mod: bpy.types.BevelModifier) -> None:
    # FIXME: Should we take WM as an argument, too?
    wm = bpy.context.window_manager
    # obj = bpy.context.active_object

    if obj.type in {'MESH', 'CURVE', 'FONT'}:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_BEVEL.png'),
        #   ("     ", p.color_setting, p.text_size_normal),
        #   (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # AFFECT
                output_text.extend([
                    (" Affect ", p.color_setting, p.text_size_normal),
                    (mod.affect, p.color_value, p.text_size_normal),
                ])

                # OFFSET TYPE
                output_text.extend([
                    (" Method ", p.color_setting, p.text_size_normal),
                    (str(mod.offset_type.lower().capitalize()), p.color_value, p.text_size_normal),
                ])

                # WIDTH
                if mod.offset_type == "PERCENT":
                    s = fmt_pct(mod.width)
                else:
                    s = fmt_length(mod.width)

                output_text.extend([
                    (" Width ", p.color_setting, p.text_size_normal),
                    (s, p.color_value, p.text_size_normal),
                ])

                # SEGMENTS
                output_text.extend([
                    (" Segments ", p.color_setting, p.text_size_normal),
                    (str(mod.segments), p.color_value, p.text_size_normal),
                ])

                # PROFILE
                output_text.extend([
                    (" Profile ", p.color_setting, p.text_size_normal),
                    (str(round(mod.profile, 2)), p.color_value, p.text_size_normal),
                ])

                # FIXME: Support material index
                # MATERIAL
                # output_text.extend([])

                # OPTIONS
                output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                # LIMIT METHOD
                output_text.extend([
                    (" Limit ", p.color_setting, p.text_size_normal),
                    (str(mod.limit_method.lower().capitalize()), p.color_value, p.text_size_normal),
                ])

                # ANGLE
                if mod.limit_method == 'ANGLE':
                    output_text.extend([
                        (":", p.color_setting, p.text_size_normal),
                        (str(round(math.degrees(mod.angle_limit), 2)), p.color_value, p.text_size_normal),
                        ("°", p.color_value, p.text_size_normal),
                    ])

                # VERTEX GROUP
                elif mod.limit_method == 'VGROUP':
                    if mod.vertex_group:
                        output_text.extend([
                            (":", p.color_setting, p.text_size_normal),
                            (str(mod.vertex_group), p.color_value, p.text_size_normal),
                        ])
                    else:
                        output_text.extend([
                            (":", p.color_setting, p.text_size_normal),
                            ("None", p.color_warning, p.text_size_normal),
                        ])

                # LOOP SLIDE
                if mod.loop_slide:
                    output_text.extend([(" Loop Slide ", p.color_setting, p.text_size_normal)])

                # CLAMP
                if mod.use_clamp_overlap:
                    output_text.extend([(" Clamp ", p.color_setting, p.text_size_normal)])

                # HARDEN NORMALS
                if mod.harden_normals:
                    output_text.extend([(" Harden ", p.color_setting, p.text_size_normal)])

                if mod.mark_seam:
                    output_text.extend([(" Mark Seam ", p.color_setting, p.text_size_normal)])

                if mod.mark_sharp:
                    output_text.extend([(" Mark Sharp ", p.color_setting, p.text_size_normal)])

                # ONLY VERTICES
                # if mod.use_only_vertices:
                #     output_text.extend([(" Only Vertices ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
