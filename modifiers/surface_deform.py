import bpy.types
import prefs

def mod_surface_deform(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                       mod: bpy.types.SurfaceDeformModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", p.color_setting, p.text_size_normal),
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

                # FALLOFF
                output_text.extend([
                    (" Falloff ", p.color_setting, p.text_size_normal),
                    (str(round(mod.falloff, 2)), p.color_value, p.text_size_normal),
                ])

                if mod.vertex_group:
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (mod.vertex_group, p.color_value, p.text_size_normal),
                    ])

                output_text.extend([
                    (" Strength ", p.color_setting, p.text_size_normal),
                    (str(round(mod.strength, 2)), p.color_value, p.text_size_normal),
                ])
        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
