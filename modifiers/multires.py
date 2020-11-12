import bpy.types
import prefs

def mod_multires(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, mod: bpy.types.MultiresModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MULTIRES.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # SUBDIVISION TYPE
                if mod.subdivision_type == 'SIMPLE':
                    output_text.extend([(" Simple ", p.color_setting, p.text_size_normal)])
                else:
                    output_text.extend([(" Catmull Clark ", p.color_setting, p.text_size_normal)])

                # QUALITY
                output_text.extend([
                    (" Quality ", p.color_setting, p.text_size_normal),
                    (str(mod.quality), p.color_value, p.text_size_normal),
                ])

                # RENDER SUBDIVISION LEVELS
                output_text.extend([
                    (" Render ", p.color_setting, p.text_size_normal),
                    (str(mod.render_levels), p.color_value, p.text_size_normal),
                ])

                # VIEWPORT SUBDIVISION LEVELS
                output_text.extend([
                    (" Preview ", p.color_setting, p.text_size_normal),
                    (str(mod.levels), p.color_value, p.text_size_normal),
                ])

                # FIXME: We need a dynamic wrap here
                if any([mod.uv_smooth == "PRESERVE_CORNERS", mod.show_only_control_edges, mod.use_creases]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                # UV SMOOTHING
                if mod.uv_smooth == "PRESERVE_CORNERS":
                    output_text.extend([
                        (" UV Smoothing (keep corners) ", p.color_setting, p.text_size_normal),
                    ])

                # OPTIMAL DISPLAY
                if mod.show_only_control_edges:
                    output_text.extend([(" Optimal Display ", p.color_setting, p.text_size_normal)])

                if mod.use_creases:
                    output_text.extend([(" Using Creases ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
