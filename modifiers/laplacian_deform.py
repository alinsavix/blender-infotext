import bpy.types
import prefs

def mod_laplacian_deform(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                         mod: bpy.types.LaplacianDeformModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        # FIXME: display this more readably
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # ITERATIONS
                output_text.extend([
                    (" Repeat ", p.color_setting, p.text_size_normal),
                    (str(mod.iterations), p.color_value, p.text_size_normal),
                ])

                # VERTEX GROUP
                output_text.extend([(" VGroup ", p.color_setting, p.text_size_normal)])
                if mod.vertex_group:
                    output_text.extend([(str(mod.vertex_group), p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
