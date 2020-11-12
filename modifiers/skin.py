import bpy.types
import prefs

def mod_skin(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
             mod: bpy.types.SkinModifier) -> None:
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SKIN.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # BRANCH SMOOTHING
                if mod.branch_smoothing != 0:
                    output_text.extend([
                        (" Branch Smoothing ", p.color_setting, p.text_size_normal),
                        (str(round(mod.branch_smoothing, 3)), p.color_value, p.text_size_normal),
                    ])

                if any([mod.use_x_symmetry, mod.use_y_symmetry, mod.use_z_symmetry]):
                    # SYMMETRY
                    output_text.extend([(" Symmetry ", p.color_setting, p.text_size_normal)])

                    # X
                    if mod.use_x_symmetry:
                        output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                    # Y
                    if mod.use_y_symmetry:
                        output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                    # Z
                    if mod.use_z_symmetry:
                        output_text.extend([(" Z ", p.color_value, p.text_size_normal)])

                # OPTIONS
                if any([mod.use_smooth_shade]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # SMOOTH SHADING
                    if mod.use_smooth_shade:
                        output_text.extend([(" Smooth Shading ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
