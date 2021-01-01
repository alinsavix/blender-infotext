import math

import bpy.types

from ..functions import *
from .. import prefs

def mod_armature(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, mod: bpy.types.ArmatureModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_ARMATURE.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend([
            "CR",
            (str(mod.name.upper()), p.color_title, p.text_size_normal),
        ])

        # FIXME: We should have a 'problem' color rather than reusing 'color_warning'
        if mod.show_viewport:
            if p.detailed_modifiers:
                output_text.extend([
                    "CR",
                    (" Object ", p.color_setting, p.text_size_normal),
                    "CR",
                ])

                if mod.object:
                    # START
                    output_text.extend([
                        "CR",
                        (str(mod.object.name), p.color_value, p.text_size_normal),
                        "CR",
                    ])
                else:
                    output_text.extend([
                        (" None ", p.color_warning, p.text_size_normal),
                    ])

                # VERTEX GROUP
                if mod.use_vertex_groups:
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                    ])
                    if mod.vertex_group:
                        output_text.extend([
                            (str(mod.vertex_group), p.color_value, p.text_size_normal),
                        ])
                    else:
                        output_text.extend([
                            (" None ", p.color_warning, p.text_size_normal),
                        ])

                # OPTIONS
                if any([mod.use_deform_preserve_volume, mod.use_bone_envelopes, mod.use_multi_modifier]):
                    output_text.extend([
                        "CR",
                        ("----", p.color_title, p.text_size_normal),
                    ])

                    # PRESERVE VOLUME
                    if mod.use_deform_preserve_volume:
                        output_text.extend([
                            (" Preserve Volume ", p.color_setting, p.text_size_normal),
                        ])

                    # BONE ENVELOPES
                    if mod.use_bone_envelopes:
                        output_text.extend([
                            (" Bone Enveloppes ", p.color_setting, p.text_size_normal),
                        ])

                    # MULTI MODIFIER
                    if mod.use_multi_modifier:
                        output_text.extend([
                            (" Multi Modifier ", p.color_setting, p.text_size_normal),
                        ])

        else:
            output_text.extend([
                (" Hidden ", p.color_warning, p.text_size_normal),
            ])

infotext_modifiers = {
    'ARMATURE': mod_armature,
}
