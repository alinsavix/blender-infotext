import bpy.types
import prefs

def mod_lattice(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                mod: bpy.types.LatticeModifier) -> None:
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_LATTICE.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                output_text.extend([(" Object ", p.color_setting, p.text_size_normal)])
                if mod.object:
                    # OBJECT
                    output_text.extend([(mod.object.name, p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (str(mod.vertex_group), p.color_value, p.text_size_normal),
                    ])

                # STRENGTH
                output_text.extend([
                    (" Strength ", p.color_setting, p.text_size_normal),
                    (str(round(mod.strength, 2)), p.color_value, p.text_size_normal),
                ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
