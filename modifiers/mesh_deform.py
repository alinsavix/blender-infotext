import math

import bpy.types

from ..functions import *
from .. import prefs

def mod_mesh_deform(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                    mod: bpy.types.MeshDeformModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", p.color_setting, p.text_size_normal),
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

                # PRECISION
                output_text.extend([
                    (" Precision ", p.color_setting, p.text_size_normal),
                    (str(mod.precision), p.color_value, p.text_size_normal),
                ])

                # OPTIONS
                if any([mod.use_dynamic_bind, mod.vertex_group]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([(" VGroup ", p.color_setting, p.text_size_normal),
                                            (str(mod.vertex_group), p.color_value, p.text_size_normal)])

                    # USE DYNAMIC BIND
                    if mod.use_dynamic_bind:
                        output_text.extend([(" Dynamic ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
