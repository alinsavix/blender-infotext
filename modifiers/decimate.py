import math

import bpy.types

from ..functions import *
from .. import prefs

def mod_decimate(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                 mod: bpy.types.DecimateModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_DECIM.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # COLLAPSE
                if mod.decimate_type == 'COLLAPSE':
                    output_text.extend([(" Collapse ", p.color_setting, p.text_size_normal)])
                    output_text.extend([
                        (" Ratio ", p.color_setting, p.text_size_normal),
                        (str(round(mod.ratio, 2)), p.color_value, p.text_size_normal),
                    ])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", p.color_setting, p.text_size_normal),
                            (str(mod.vertex_group), p.color_value, p.text_size_normal),
                        ])

                        # FACTOR
                        output_text.extend([
                            (" Factor ", p.color_setting, p.text_size_normal),
                            (str(round(mod.vertex_group_factor, 2)), p.color_value, p.text_size_normal),
                        ])
                    # OPTIONS
                    if any([mod.use_collapse_triangulate, mod.use_symmetry]):
                        output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                        # TRIANGULATE
                        if mod.use_collapse_triangulate:
                            output_text.extend([(" Triangulate ", p.color_setting, p.text_size_normal)])

                        # SYMMETRY
                        if mod.use_symmetry:
                            output_text.extend([
                                (" Symmetry ", p.color_setting, p.text_size_normal),
                                (str(mod.symmetry_axis), p.color_value, p.text_size_normal),
                            ])

                # UN-SUBDIVDE
                elif mod.decimate_type == 'UNSUBDIV':
                    output_text.extend([(" Un-subdivide ", p.color_setting, p.text_size_normal)])
                    output_text.extend([
                        (" Iteration ", p.color_setting, p.text_size_normal),
                        (str(round(mod.iterations, 2)), p.color_value, p.text_size_normal),
                    ])
                # PLANAR
                else:
                    output_text.extend([(" Planar ", p.color_setting, p.text_size_normal)])
                    output_text.extend([
                        (" Angle Limit ", p.color_setting, p.text_size_normal), (
                            str(round(math.degrees(mod.angle_limit), 1)), p.color_value, p.text_size_normal),
                        ("°", p.color_value, p.text_size_normal),
                    ])

                    # OPTIONS
                    if any([mod.use_dissolve_boundaries, mod.delimit]):
                        output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                        # ALL BOUNDARIES
                        if mod.use_dissolve_boundaries:
                            output_text.extend([(" All Boundaries ", p.color_setting, p.text_size_normal)])

                        # DELIMIT
                        if mod.delimit:
                            output_text.extend([(" Delimit ", p.color_setting, p.text_size_normal)])
                            if mod.delimit == {'NORMAL'}:
                                output_text.extend([(" NORMAL ", p.color_value, p.text_size_normal)])
                            elif mod.delimit == {'MATERIAL'}:
                                output_text.extend([(" MATERIAL ", p.color_value, p.text_size_normal)])
                            elif mod.delimit == {'SEAM'}:
                                output_text.extend([(" SEAM ", p.color_value, p.text_size_normal)])
                            elif mod.delimit == {'SHARP'}:
                                output_text.extend([(" SHARP ", p.color_value, p.text_size_normal)])
                            elif mod.delimit == {'UV'}:
                                output_text.extend([(" UV ", p.color_value, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
