import math

import bpy.types

from ..functions import *
from .. import prefs

def mod_hook(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
             mod: bpy.types. HookModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_HOOK.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # OBJECT
                output_text.extend([(" Object ", p.color_setting, p.text_size_normal)])
                if mod.object:
                    output_text.extend([(mod.object.name, p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # RADIUS
                if mod.falloff_type != 'NONE':
                    if mod.falloff_radius != 0:
                        output_text.extend([
                            (" Radius ", p.color_setting, p.text_size_normal),
                            (fmt_length(mod.falloff_radius, 2), p.color_value, p.text_size_normal),
                        ])

                # STRENGTH
                output_text.extend([
                    (" Strength ", p.color_setting, p.text_size_normal),
                    (str(round(mod.strength, 2)), p.color_value, p.text_size_normal),
                ])

                # OPTIONS
                output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (mod.vertex_group, p.color_value, p.text_size_normal),
                    ])

                # FALLOF TYPE
                output_text.extend([
                    (" Fallof Type ", p.color_setting, p.text_size_normal),
                    (str(mod.falloff_type.upper()), p.color_value, p.text_size_normal),
                ])

                # UNIFORM FALLOFF
                if mod.use_falloff_uniform:
                    output_text.extend([(" Uniform Falloff ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
