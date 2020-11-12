import bpy.types
import prefs

def mod_corrective_smooth(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                          mod: bpy.types.CorrectiveSmoothModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend([
            "CR",
            (str(mod.name.upper()), p.color_title, p.text_size_normal),
        ])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # FACTOR
                output_text.extend([
                    (" Factor ", p.color_setting, p.text_size_normal),
                    (str(round(mod.factor, 2)), p.color_value, p.text_size_normal),
                ])

                # ITERATIONS
                output_text.extend([
                    (" Repeat ", p.color_setting, p.text_size_normal),
                    (str(mod.iterations), p.color_value, p.text_size_normal),
                ])

                # SCALE
                if mod.scale != 1.0:
                    output_text.extend([
                        (" Scale ", p.color_setting, p.text_size_normal),
                        (str(round(mod.scale, 2)), p.color_value, p.text_size_normal),
                    ])

                # SMOOTH TYPE
                output_text.extend([
                    (" Type ", p.color_setting, p.text_size_normal),
                    (str(mod.smooth_type.lower().capitalize()), p.color_value, p.text_size_normal),
                ])

                # OPTIONS
                if any([mod.use_only_smooth, mod.vertex_group, mod.use_pin_boundary, mod.rest_source]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", p.color_setting, p.text_size_normal),
                            (mod.vertex_group, p.color_value, p.text_size_normal),
                        ])

                    # ONLY SMOOTH
                    if mod.use_only_smooth:
                        output_text.extend([(" Only Smooth ", p.color_setting, p.text_size_normal)])

                    # PIN BOUNDARIES
                    if mod.use_pin_boundary:
                        output_text.extend([(" Pin Boundaries ", p.color_setting, p.text_size_normal)])

                    # OBJECT
                    output_text.extend([
                        (" Rest Source ", p.color_setting, p.text_size_normal),
                        (mod.rest_source.lower().capitalize(), p.color_value, p.text_size_normal),
                    ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
