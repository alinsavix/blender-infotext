import bpy.types
import prefs

def mod_boolean(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                mod: bpy.types.BooleanModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_BOOLEAN.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # OPERATION
                output_text.extend([
                    (" ", p.color_title, p.text_size_normal),
                    (str(mod.operation), p.color_value, p.text_size_normal),
                ])
                if mod.object:
                    # Object
                    output_text.extend([
                        (" Object ", p.color_setting, p.text_size_normal),
                        (mod.object.name, p.color_value, p.text_size_normal),
                    ])
                else:
                    output_text.extend([(" No object Selected", p.color_warning, p.text_size_normal)])

                # SOLVER
                # if (hasattr(bpy.context.preferences.system, 'opensubdiv_compute_type')):
                # if bpy.app.version == (2, 79, 0):
                #     output_text.extend([(" ", p.color_title, p.text_size_normal),
                #                           (str(mod.solver.upper()), p.color_value, p.text_size_normal)])

                # OVERLAP THRESHOLD
                # if mod.solver == 'BMESH':
                #     if mod.double_threshold > 0 :
                #         output_text.extend([(" Overlap Threshold ", p.color_setting, p.text_size_normal),
                #                           (str(round(mod.double_threshold,2)), p.color_value, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
