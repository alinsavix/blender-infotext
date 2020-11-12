import bpy.types
import prefs

def mod_cast(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
             mod: bpy.types.CastModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_CAST.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # CAST TYPE
                output_text.extend([
                    (" Type ", p.color_setting, p.text_size_normal),
                    (str(mod.cast_type.lower().capitalize()), p.color_value, p.text_size_normal),
                ])

                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    output_text.extend([(" Axis ", p.color_setting, p.text_size_normal)])

                    if mod.use_x:
                        output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                    if mod.use_y:
                        output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                    if mod.use_z:
                        output_text.extend([(" Z ", p.color_value, p.text_size_normal)])

                else:
                    output_text.extend([(" No Axis Selected ", p.color_warning, p.text_size_normal)])

                # FACTOR
                output_text.extend([
                    (" Factor ", p.color_setting, p.text_size_normal),
                    (str(round(mod.factor, 2)), p.color_value, p.text_size_normal),
                ])

                # RADIUS
                if mod.radius != 0:
                    output_text.extend([
                        (" Radius ", p.color_setting, p.text_size_normal),
                        (fmt_length(mod.radius, 2), p.color_value, p.text_size_normal),
                    ])

                # SIZE
                if mod.size != 0:
                    output_text.extend([
                        (" Size ", p.color_setting, p.text_size_normal),
                        (str(round(mod.size, 2)), p.color_value, p.text_size_normal),
                    ])

                # OPTIONS
                if any([mod.use_radius_as_size, mod.vertex_group, mod.object, mod.use_transform]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", p.color_setting, p.text_size_normal),
                            (mod.vertex_group, p.color_value, p.text_size_normal),
                        ])

                    # FROM RADIUS
                    if mod.use_radius_as_size:
                        output_text.extend([(" From Radius ", p.color_setting, p.text_size_normal)])

                    # OBJECT
                    if mod.object:
                        output_text.extend([
                            (" Control Object ", p.color_setting, p.text_size_normal),
                            (mod.object.name, p.color_value, p.text_size_normal)
                        ])

                    # USE TRANSFORM
                    if mod.use_transform:
                        output_text.extend([(" Use Transform ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
