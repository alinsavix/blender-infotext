import bpy.types
import prefs

def mod_shrinkwrap(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                   mod: bpy.types.ShrinkwrapModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SHRINKWRAP.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # TARGET
                output_text.extend([(" Target ", p.color_setting, p.text_size_normal)])
                if mod.target:
                    output_text.extend([(str(mod.target.name), p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # OFFSET
                output_text.extend([
                    (" Offset ", p.color_setting, p.text_size_normal),
                    (str(round(mod.offset, 2)), p.color_value, p.text_size_normal),
                ])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (str(mod.vertex_group), p.color_value, p.text_size_normal),
                    ])

                output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                # NEAREST SURFACEPOINT
                if mod.wrap_method == 'NEAREST_SURFACEPOINT':
                    # MODE
                    output_text.extend([
                        (" Method ", p.color_setting, p.text_size_normal),
                        (str(mod.wrap_method.lower().capitalize()), p.color_value, p.text_size_normal),
                        (" Mode ", p.color_setting, p.text_size_normal),
                        (str(mod.wrap_mode.lower().capitalize()), p.color_value, p.text_size_normal),
                    ])

                # PROJECT
                elif mod.wrap_method == 'PROJECT':
                    # MODE
                    output_text.extend([
                        (" Method ", p.color_setting, p.text_size_normal),
                        (str(mod.wrap_method.lower().capitalize()), p.color_value, p.text_size_normal),
                        (" Mode ", p.color_setting, p.text_size_normal),
                        (str(mod.wrap_mode.lower().capitalize()), p.color_value, p.text_size_normal),
                    ])

                    # AXIS
                    if any([mod.use_project_x, mod.use_project_y, mod.use_project_z]):
                        output_text.extend([(" Axis ", p.color_setting, p.text_size_normal)])
                        # X
                        if mod.use_project_x:
                            output_text.extend([(" X ", p.color_value, p.text_size_normal)])
                        # Y
                        if mod.use_project_y:
                            output_text.extend([(" Y ", p.color_value, p.text_size_normal)])
                        # Z
                        if mod.use_project_z:
                            output_text.extend([(" Z ", p.color_value, p.text_size_normal)])

                    # LEVELS
                    output_text.extend([
                        (" Subsurf ", p.color_setting, p.text_size_normal),
                        (str(mod.subsurf_levels), p.color_value, p.text_size_normal),
                    ])

                    # PROJECT LIMIT
                    output_text.extend([
                        (" Limit ", p.color_setting, p.text_size_normal),
                        (str(round(mod.project_limit, 2)), p.color_value, p.text_size_normal)
                    ])

                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # DIRECTION
                    if mod.use_negative_direction:
                        output_text.extend([(" Negative ", p.color_setting, p.text_size_normal)])

                    if mod.use_positive_direction:
                        output_text.extend([(" Positive ", p.color_setting, p.text_size_normal)])

                    # MODE
                    output_text.extend([
                        (" Cull Face ", p.color_setting, p.text_size_normal),
                        (str(mod.cull_face.lower().capitalize()), p.color_value, p.text_size_normal),
                    ])
                    # AUXILIARY TARGET
                    if mod.auxiliary_target:
                        output_text.extend([
                            (" Auxiliary Target ", p.color_setting, p.text_size_normal),
                            (mod.auxiliary_target.name, p.color_value, p.text_size_normal),
                        ])
                else:
                    # MODE
                    output_text.extend([
                        (" Mode ", p.color_setting, p.text_size_normal),
                        (str(mod.wrap_method.lower().capitalize()), p.color_value, p.text_size_normal),
                    ])
        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
