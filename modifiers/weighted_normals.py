import bpy.types
import prefs

def mod_weighted_normals(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                         mod: bpy.types.WeightedNormalModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_EDGESPLIT.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # Mode
                # output_text.extend([(" Mode", p.color_setting, p.text_size_normal), (str(mod.mode.lower().capitalize()), p.color_setting, p.text_size_normal)])
                output_text.extend([
                    (" Mode ", p.color_setting, p.text_size_normal),
                    (str(mod.mode.lower().capitalize()), p.color_value, p.text_size_normal),
                ])

                # Weight
                output_text.extend([
                    (" Weight ", p.color_setting, p.text_size_normal),
                    (str(round(mod.weight, 2)), p.color_value, p.text_size_normal),
                ])

                # STRENGTH
                output_text.extend([
                    (" Strength ", p.color_setting, p.text_size_normal),
                    (str(round(mod.weight, 2)), p.color_value, p.text_size_normal),
                ])

                # THRESHOLD
                output_text.extend([
                    (" Threshold ", p.color_setting, p.text_size_normal),
                    (str(round(mod.thresh, 2)), p.color_value, p.text_size_normal),
                ])

                if any([mod.keep_sharp, mod.face_influence, mod.vertex_group]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    # KEEP SHARP
                    if mod.keep_sharp:
                        output_text.extend([(" Keep Sharp ", p.color_setting, p.text_size_normal)])

                    # KEEP SHARP
                    if mod.face_influence:
                        output_text.extend([(" Face Influence ", p.color_setting, p.text_size_normal)])

                    if mod.vertex_group:
                        output_text.extend([
                            (" Vgroup ", p.color_setting, p.text_size_normal),
                            (str(mod.vertex_group), p.color_value, p.text_size_normal),
                        ])
                    else:
                        output_text.extend([(" No Vertex Group Selected ", p.color_warning, p.text_size_normal)])
        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
