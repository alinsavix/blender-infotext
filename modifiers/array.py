import math

import bpy.types

from ..functions import *
from .. import prefs

def mod_array(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
              mod: bpy.types.ArrayModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR",('ICON', 'ICON_MOD_ARRAY.png'),("    ", p.color_setting, p.text_size_normal), (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # FIT MODE
                if mod.fit_type == 'FIXED_COUNT':
                    output_text.extend([
                        (" Count ", p.color_setting, p.text_size_normal),
                        (str(mod.count), p.color_value, p.text_size_normal),
                    ])

                elif mod.fit_type == 'FIT_CURVE':
                    if mod.curve:
                        # Object
                        output_text.extend([
                            (" Curve ", p.color_setting, p.text_size_normal),
                            (mod.curve.name, p.color_value, p.text_size_normal),
                        ])
                    else:
                        output_text.extend([(" No Curve Selected", p.color_warning, p.text_size_normal)])

                else:
                    output_text.extend([
                        (" Length ", p.color_setting, p.text_size_normal),
                        (str(round(mod.fit_length, 2)), p.color_value, p.text_size_normal),
                    ])

                # CONSTANT
                if mod.use_constant_offset:
                    # output_text.extend([(" Constant ", p.color_setting, p.text_size_normal),
                    #                   ("%s" %round(mod.constant_offset_displace[0], 1),color_value, p.text_size_normal),
                    #                   ("  %s" %round(mod.constant_offset_displace[1], 1),color_value, p.text_size_normal),
                    #                   ("  %s" %round(mod.constant_offset_displace[2], 1),color_value, p.text_size_normal)])

                    output_text.extend([(" Constant ", p.color_setting, p.text_size_normal)])

                    # X
                    if mod.constant_offset_displace[0] != 0:
                        output_text.extend([
                            (" X ", p.color_setting, p.text_size_normal),
                            (fmt_length(mod.constant_offset_displace[0], 1), p.color_value, p.text_size_normal),
                        ])

                    # Y
                    if mod.constant_offset_displace[1] != 0:
                        output_text.extend([
                            (" Y ", p.color_setting, p.text_size_normal),
                            (fmt_length(mod.constant_offset_displace[1], 1), p.color_value, p.text_size_normal),
                        ])

                    # Z
                    if mod.constant_offset_displace[2] != 0:
                        output_text.extend([
                            (" Z ", p.color_setting, p.text_size_normal),
                            (fmt_length(mod.constant_offset_displace[2], 1), p.color_value, p.text_size_normal),
                        ])

                # RELATIVE
                elif mod.use_relative_offset:
                    output_text.extend([(" Relative ", p.color_setting, p.text_size_normal)])

                    # X
                    if mod.relative_offset_displace[0] != 0:
                        output_text.extend([
                            (" X ", p.color_setting, p.text_size_normal),
                            (str(round(mod.relative_offset_displace[0], 1)), p.color_value, p.text_size_normal),
                        ])

                    # Y
                    if mod.relative_offset_displace[1] != 0:
                        output_text.extend([
                            (" Y ", p.color_setting, p.text_size_normal),
                            (str(round(mod.relative_offset_displace[1], 1)), p.color_value, p.text_size_normal),
                        ])

                    # Z
                    if mod.relative_offset_displace[2] != 0:
                        output_text.extend([
                            (" Z ", p.color_setting, p.text_size_normal),
                            (str(round(mod.relative_offset_displace[2], 1)), p.color_value, p.text_size_normal),
                        ])

                # MERGE
                if mod.use_merge_vertices:
                    output_text.extend([
                        (" Merge ", p.color_setting, p.text_size_normal),
                        (str(round(mod.merge_threshold, 3)), p.color_value, p.text_size_normal),
                    ])

                    if mod.use_merge_vertices_cap:
                        output_text.extend([(" First Last ", p.color_setting, p.text_size_normal)])

                # OPTIONS
                if any([mod.use_object_offset, mod.start_cap, mod.end_cap]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # OBJECT OFFSET
                    if mod.use_object_offset:
                        if mod.offset_object:
                            output_text.extend([
                                (" Object Offset ", p.color_setting, p.text_size_normal),
                                (mod.offset_object.name, p.color_value, p.text_size_normal),
                            ])
                        else:
                            output_text.extend([
                                (" No Object Selected", p.color_warning, p.text_size_normal),
                            ])

                    # STAR CAP
                    if mod.start_cap:
                        output_text.extend([
                            (" Start Cap ", p.color_setting, p.text_size_normal),
                            (mod.start_cap.name, p.color_value, p.text_size_normal),
                        ])

                    # END CAP
                    if mod.end_cap:
                        output_text.extend([
                            (" End Cap ", p.color_setting, p.text_size_normal),
                            (mod.end_cap.name, p.color_value, p.text_size_normal),
                        ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
