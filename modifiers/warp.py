import bpy.types
import prefs

def mod_warp(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
             mod: bpy.types.WarpModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_WARP.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # FROM
                output_text.extend([(" From ", p.color_setting, p.text_size_normal)])
                if mod.object_from:
                    output_text.extend([(str(mod.object_from.name), p.color_value, p.text_size_normal)])

                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # TO
                output_text.extend([(" To ", p.color_setting, p.text_size_normal)])
                if mod.object_to:
                    output_text.extend([(str(mod.object_to.name), p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # STRENGTH
                output_text.extend([
                    (" Strength ", p.color_setting, p.text_size_normal),
                    (str(round(mod.strength, 2)), p.color_value, p.text_size_normal),
                ])

                output_text.extend([
                    (" Falloff ", p.color_setting, p.text_size_normal),
                    (mod.falloff_type.lower().capitalize(), p.color_value, p.text_size_normal),
                ])

                # RADIUS
                if mod.falloff_type != 'NONE':
                    # FIXME: Radius showing in m when units are cm
                    # (might be fixed now)
                    if mod.falloff_radius != 0:
                        output_text.extend([
                            (" Radius ", p.color_setting, p.text_size_normal),
                            (fmt_length(mod.falloff_radius, 2), p.color_value, p.text_size_normal),
                        ])

                # OPTIONS
                if any([mod.vertex_group, mod.use_volume_preserve, mod.texture_coords]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", p.color_setting, p.text_size_normal),
                            (str(mod.vertex_group), p.color_value, p.text_size_normal),
                        ])

                    # OFFSET
                    if mod.use_volume_preserve:
                        output_text.extend([(" Preserve Volume ", p.color_setting, p.text_size_normal)])

                    # TEXTURE
                    if mod.texture:
                        output_text.extend([
                            (" Texture ", p.color_setting, p.text_size_normal),
                            (mod.texture.name, p.color_value, p.text_size_normal),
                        ])

                    # TEXTURES COORD
                    output_text.extend([
                        (" Texture Coords ", p.color_setting, p.text_size_normal),
                        (mod.texture_coords, p.color_value, p.text_size_normal),
                    ])

                    # OBJECT
                    if mod.texture_coords == "OBJECT":
                        if mod.texture_coords_object:
                            output_text.extend([(" Object ", p.color_setting, p.text_size_normal)])
                            output_text.extend([
                                (str(mod.texture_coords_object.name), p.color_value, p.text_size_normal),
                            ])
                        else:
                            output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                    # UVs
                    if mod.texture_coords == "UV":
                        output_text.extend([(" UVMap ", p.color_setting, p.text_size_normal)])

                        if mod.uv_layer:
                            output_text.extend([
                                (str(mod.uv_layer), p.color_value, p.text_size_normal)
                            ])
                        else:
                            output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
