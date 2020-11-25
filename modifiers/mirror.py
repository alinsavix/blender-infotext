import bpy.types
from .. import prefs

def mod_mirror(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
               mod: bpy.types.MirrorModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MIRROR.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                if any([mod.use_axis[0], mod.use_axis[1], mod.use_axis[2]]):
                    output_text.extend([(" Axis ", p.color_setting, p.text_size_normal)])
                    # X
                    if mod.use_axis[0]:
                        output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                    # Y
                    if mod.use_axis[1]:
                        output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                    # Z
                    if mod.use_axis[2]:
                        output_text.extend([(" Z ", p.color_value, p.text_size_normal)])

                # OBJECT
                if mod.mirror_object:
                    output_text.extend([
                        (" Object ", p.color_setting, p.text_size_normal),
                        (mod.mirror_object.name, p.color_value, p.text_size_normal),
                    ])

                # MERGE
                if mod.use_mirror_merge:
                    output_text.extend([
                        (" Merge ", p.color_setting, p.text_size_normal),
                        (fmt_length(mod.merge_threshold, 3), p.color_value, p.text_size_normal),
                    ])

                # OPTIONS
                if any([mod.use_clip, mod.use_mirror_vertex_groups, mod.use_mirror_u, mod.use_mirror_v]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    # CLIPPING
                    if mod.use_clip:
                        output_text.extend([(" Clipping ", p.color_setting, p.text_size_normal)])

                    # VERTEX GROUP
                    if mod.use_mirror_vertex_groups:
                        output_text.extend([(" VGroup ", p.color_setting, p.text_size_normal)])

                    # TEXTURES
                    if any([mod.use_mirror_u, mod.use_mirror_v]):
                        output_text.extend([(" Textures ", p.color_setting, p.text_size_normal)])

                    # TEXTURE U
                    if mod.use_mirror_u:
                        output_text.extend([
                            (" U ", p.color_setting, p.text_size_normal),
                            (fmt_length(mod.mirror_offset_u, 3), p.color_value, p.text_size_normal),
                        ])

                    # TEXTURE V
                    if mod.use_mirror_v:
                        output_text.extend([
                            (" V ", p.color_setting, p.text_size_normal),
                            (fmt_length(mod.mirror_offset_v, 3), p.color_value, p.text_size_normal),
                        ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
