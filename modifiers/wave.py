import math

import bpy.types

from ..functions import *
from .. import prefs

def mod_wave(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
             mod: bpy.types.WaveModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_WAVE.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                if any([mod.use_x, mod.use_y, mod.use_cyclic]):
                    output_text.extend([(" Motion ", p.color_setting, p.text_size_normal)])

                    if mod.use_x:
                        output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                    if mod.use_y:
                        output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                    if mod.use_cyclic:
                        output_text.extend([(" Cyclic ", p.color_value, p.text_size_normal)])

                if mod.use_normal:
                    if any([mod.use_normal_x, mod.use_normal_y, mod.use_normal_z]):
                        output_text.extend([(" Normals ", p.color_setting, p.text_size_normal)])

                        if mod.use_normal_x:
                            output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                        if mod.use_normal_y:
                            output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                        if mod.use_normal_z:
                            output_text.extend([(" Z ", p.color_value, p.text_size_normal)])

                # TIME
                output_text.extend([(" Time ", p.color_setting, p.text_size_normal)])

                # OFFSET
                output_text.extend([
                    (" Offset ", p.color_setting, p.text_size_normal),
                    (str(round(mod.time_offset, 2)), p.color_value, p.text_size_normal),
                ])
                # LIFE
                output_text.extend([
                    (" Life ", p.color_setting, p.text_size_normal),
                    (str(round(mod.lifetime, 2)), p.color_value, p.text_size_normal),
                ])
                # DAMPING
                output_text.extend([
                    (" Damping ", p.color_setting, p.text_size_normal),
                    (str(round(mod.damping_time, 2)), p.color_value, p.text_size_normal),
                ])

                if any([mod.start_position_x, mod.start_position_y, mod.falloff_radius]) != 0:
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    # TIME
                    # FIXME: shows m when scale is cm
                    output_text.extend([(" Position ", p.color_setting, p.text_size_normal)])

                    # POS X
                    output_text.extend([
                        (" X ", p.color_setting, p.text_size_normal),
                        (fmt_length(mod.start_position_x, 2), p.color_value, p.text_size_normal),
                    ])

                    # POS Y
                    output_text.extend([
                        (" Y ", p.color_setting, p.text_size_normal),
                        (fmt_length(mod.start_position_y, 2), p.color_value, p.text_size_normal),
                    ])

                    # FALLOFF
                    output_text.extend([
                        (" Falloff ", p.color_setting, p.text_size_normal),
                        (fmt_length(mod.falloff_radius, 2), p.color_value, p.text_size_normal),
                    ])

                if any([mod.start_position_object, mod.vertex_group, mod.texture_coords]) != 0:
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # FROM
                    if mod.start_position_object:
                        output_text.extend([
                            (" From ", p.color_setting, p.text_size_normal),
                            (str(mod.start_position_object.name), p.color_value, p.text_size_normal),
                        ])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", p.color_setting, p.text_size_normal),
                            (str(mod.vertex_group), p.color_value, p.text_size_normal),
                        ])

                    # TEXTURES COORD
                    output_text.extend([
                        (" Texture Coords ", p.color_setting, p.text_size_normal),
                        (mod.texture_coords, p.color_value, p.text_size_normal),
                    ])

                    # OBJECT
                    if mod.texture_coords == "OBJECT":
                        if mod.texture_coords_object:
                            output_text.extend([
                                (" Object ", p.color_setting, p.text_size_normal),
                                (str(mod.texture_coords_object.name), p.color_value, p.text_size_normal),
                            ])
                        else:
                            output_text.extend([(" No Object Selected ", p.color_warning, p.text_size_normal)])

                    # UVs
                    if mod.texture_coords == "UV":
                        output_text.extend([(" UVMap ", p.color_setting, p.text_size_normal)])
                        if mod.uv_layer:
                            output_text.extend([(mod.uv_layer, p.color_value, p.text_size_normal)])
                        else:
                            output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                # SPEED
                output_text.extend([
                    (" Speed ", p.color_setting, p.text_size_normal),
                    (str(round(mod.speed, 2)), p.color_value, p.text_size_normal),
                ])

                # SPEED
                # FIXME: Shows m when scale is cm
                output_text.extend([
                    (" Height ", p.color_setting, p.text_size_normal),
                    (fmt_length(mod.height, 2), p.color_value, p.text_size_normal),
                ])

                # SPEED
                output_text.extend([
                    (" Width ", p.color_setting, p.text_size_normal),
                    (fmt_length(mod.width, 2), p.color_value, p.text_size_normal),
                ])

                # SPEED
                output_text.extend([
                    (" Narrowness ", p.color_setting, p.text_size_normal),
                    (fmt_length(mod.narrowness, 2), p.color_value, p.text_size_normal),
                ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
