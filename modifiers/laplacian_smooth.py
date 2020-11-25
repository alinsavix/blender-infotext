import math

import bpy.types

from ..functions import *
from .. import prefs

def mod_laplacian_smooth(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                         mod: bpy.types.LaplacianSmoothModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # REPEAT
                output_text.extend([
                    (" Repeat ", p.color_setting, p.text_size_normal),
                    (str(mod.iterations), p.color_value, p.text_size_normal),
                ])

                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    output_text.extend([(" Axis", p.color_setting, p.text_size_normal)])

                    if mod.use_x:
                        output_text.extend([(" X", p.color_value, p.text_size_normal)])

                    if mod.use_y:
                        output_text.extend([(" Y", p.color_value, p.text_size_normal)])

                    if mod.use_z:
                        output_text.extend([(" Z", p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None", p.color_warning, p.text_size_normal)])

                # FACTOR
                output_text.extend([
                    (" Factor ", p.color_setting, p.text_size_normal),
                    (str(round(mod.lambda_factor, 2)), p.color_value, p.text_size_normal),
                ])

                # BORDER
                output_text.extend([
                    (" Border ", p.color_setting, p.text_size_normal),
                    (str(round(mod.lambda_border, 2)), p.color_value, p.text_size_normal),
                ])

                # OPTIONS
                if any([mod.use_volume_preserve, mod.use_normalized, mod.vertex_group]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # PRESERVE VOLUME
                    if mod.use_volume_preserve:
                        output_text.extend([(" Preserve Volume ", p.color_setting, p.text_size_normal)])

                    # NORMALIZED
                    if mod.use_normalized:
                        output_text.extend([(" Normalized ", p.color_setting, p.text_size_normal)])

                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", p.color_setting, p.text_size_normal),
                            (mod.vertex_group, p.color_value, p.text_size_normal)
                        ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
