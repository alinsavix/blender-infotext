import bpy.types
import prefs

def mod_simple_deform(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                      mod: bpy.types.SimpleDeformModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SIMPLEDEFORM.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                output_text.extend([
                    (" ", p.color_setting, p.text_size_normal),
                    (str(mod.deform_method.upper()), p.color_value, p.text_size_normal),
                ])

                # ORIGIN
                if mod.origin:
                    output_text.extend([(" Axis,Origin ", p.color_setting, p.text_size_normal),
                                        (str(mod.origin.name), p.color_value, p.text_size_normal),
                                        ])

                # ANGLE/FACTOR
                if mod.deform_method in ['TWIST', 'BEND']:
                    # Angle
                    output_text.extend([
                        (" Angle ", p.color_setting, p.text_size_normal),
                        (str(round(math.degrees(mod.factor), 1)), p.color_value, p.text_size_normal),
                        ("°", p.color_value, p.text_size_normal),
                    ])

                elif mod.deform_method in ['TAPER', 'STRETCH']:
                    output_text.extend([
                        (" Factor ", p.color_setting, p.text_size_normal),
                        (str(round(mod.factor, 2)), p.color_value, p.text_size_normal),
                    ])

                # OPTIONS
                output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                # AXIS
                # FIXME: Should we always show this?
                output_text.extend([
                    (" Axis ", p.color_setting, p.text_size_normal),
                    (mod.deform_axis, p.color_value, p.text_size_normal),
                ])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (str(mod.vertex_group), p.color_value, p.text_size_normal),
                    ])

                # LOCK
                if mod.deform_method != 'BEND':
                    if any([mod.lock_x, mod.lock_y]):
                        output_text.extend([(" Lock ", p.color_setting, p.text_size_normal)])

                        if mod.lock_x:
                            output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                        if mod.lock_y:
                            output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                # LIMIT
                output_text.extend([
                    (" Limit ", p.color_setting, p.text_size_normal),
                    (str(round(mod.limits[0], 2)), p.color_value, p.text_size_normal),
                    (" – ", p.color_setting, p.text_size_normal),
                    (str(round(mod.limits[1], 2)), p.color_value, p.text_size_normal),
                ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
