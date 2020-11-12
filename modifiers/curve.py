import bpy.types
import prefs

def mod_curve(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
              mod: bpy.types.CurveModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_CURVE.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend([
            "CR",
            (str(mod.name.upper()), p.color_title, p.text_size_normal),
        ])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # OBJECT
                output_text.extend([(" Object ", p.color_setting, p.text_size_normal)])
                if mod.object:
                    output_text.extend([(mod.object.name, p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # DEFORM AXIS
                output_text.extend([(" Deformation Axis ", p.color_setting, p.text_size_normal)])
                if mod.deform_axis == 'POS_X':
                    output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                elif mod.deform_axis == 'POS_Y':
                    output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                elif mod.deform_axis == 'POS_Z':
                    output_text.extend([(" Z ", p.color_value, p.text_size_normal)])

                elif mod.deform_axis == 'NEG_X':
                    output_text.extend([(" -X ", p.color_value, p.text_size_normal)])

                elif mod.deform_axis == 'NEG_Y':
                    output_text.extend([(" -Y ", p.color_value, p.text_size_normal)])

                elif mod.deform_axis == 'NEG_Z':
                    output_text.extend([(" -Z ", p.color_value, p.text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (str(mod.vertex_group), p.color_value, p.text_size_normal),
                    ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
