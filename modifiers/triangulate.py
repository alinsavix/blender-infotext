import math

import bpy.types

from ..functions import *
from .. import prefs

# FIXME: Needs to support 'keep normals'  minimum verts, and not have
# underscores in the 'method' field


def mod_triangulate(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, mod: bpy.types.TriangulateModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_TRIANGULATE.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # VIEW
                output_text.extend([
                    ("  ", p.color_setting, p.text_size_normal),
                    (str(mod.quad_method.lower().capitalize()), p.color_value, p.text_size_normal),
                ])

                # RENDER
                output_text.extend([
                    ("  ", p.color_setting, p.text_size_normal),
                    (str(mod.ngon_method.lower().capitalize()), p.color_value, p.text_size_normal),
                ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
