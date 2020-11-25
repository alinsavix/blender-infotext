import math

import bpy.types

from ..functions import *
from .. import prefs

def mod_solidify(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                 mod: bpy.types.SolidifyModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SOLIDIFY.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # THICKNESS
                output_text.extend([
                    (" Thickness ", p.color_setting, p.text_size_normal),
                    (fmt_length(mod.thickness, 3), p.color_value, p.text_size_normal),
                ])

                # OFFSET
                output_text.extend([
                    (" Offset ", p.color_setting, p.text_size_normal),
                    (str(round(mod.offset, 2)), p.color_value, p.text_size_normal),
                ])

                # CLAMP
                if mod.thickness_clamp != 0:
                    output_text.extend([
                        (" Clamp ", p.color_setting, p.text_size_normal),
                        (str(round(mod.thickness_clamp, 2)), p.color_value, p.text_size_normal),
                    ])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (str(mod.vertex_group), p.color_value, p.text_size_normal),
                    ])

                    # THICKNESS VGROUP
                    output_text.extend([
                        (" Clamp ", p.color_setting, p.text_size_normal),
                        (str(round(mod.thickness_vertex_group, 2)), p.color_value, p.text_size_normal),
                    ])

                # OPTIONS LIGNE 1
                if any([mod.use_flip_normals, mod.use_even_offset, mod.use_quality_normals, mod.use_rim]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # FLIP NORMALS
                    if mod.use_flip_normals:
                        output_text.extend([(" Flip Normals ", p.color_setting, p.text_size_normal)])

                    # USE EVEN OFFSET
                    if mod.use_even_offset:
                        output_text.extend([(" Even Thickness ", p.color_setting, p.text_size_normal)])

                    # HIGH QUALITY NORMALS
                    if mod.use_quality_normals:
                        output_text.extend([(" High Quality Normals ", p.color_setting, p.text_size_normal)])

                    # USE RIM
                    if mod.use_rim:
                        output_text.extend([(" Fill Rim ", p.color_setting, p.text_size_normal)])

                        # ONLY RIM
                        if mod.use_rim_only:
                            output_text.extend([(" Only rims ", p.color_setting, p.text_size_normal)])

                # OPTIONS LIGNE 2
                if any([mod.edge_crease_inner, mod.edge_crease_outer, mod.edge_crease_rim]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # INNER
                    if mod.edge_crease_inner != 0:
                        output_text.extend([
                            (" Inner ", p.color_setting, p.text_size_normal),
                            (str(round(mod.edge_crease_inner, 2)), p.color_value, p.text_size_normal),
                        ])

                    # OUTER
                    if mod.edge_crease_outer != 0:
                        output_text.extend([
                            (" Outer ", p.color_setting, p.text_size_normal),
                            (str(round(mod.edge_crease_outer, 2)), p.color_value, p.text_size_normal),
                        ])

                    # RIM
                    if mod.edge_crease_rim != 0:
                        output_text.extend([
                            (" Rim ", p.color_setting, p.text_size_normal),
                            (str(round(mod.edge_crease_rim, 2)), p.color_value, p.text_size_normal),
                        ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
