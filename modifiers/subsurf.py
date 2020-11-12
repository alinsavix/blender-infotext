import bpy.types
import prefs

def mod_subsurf(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                mod: bpy.types.SubsurfModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SUBSURF.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        # FIXME: Almost all of this is the same as the multires modifier. Can
        # we consolidate the code a bit?
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

                # FIXME: Do we need to add code for this case? Does this case exist in 2.8x?
                # OPEN SUBDIV
                # if (hasattr(bpy.context.preferences.system, 'opensubdiv_compute_type')):
                #     if mod.use_opensubdiv:
                #         output_text.extend([(" Open Subdiv ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
