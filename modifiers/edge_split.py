import bpy.types
import prefs

def mod_edge_split(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                   mod: bpy.types.EdgeSplitModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_EDGESPLIT.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # EDGE ANGLE
                if mod.use_edge_angle:
                    output_text.extend([
                        (" Edges angle ", p.color_setting, p.text_size_normal),
                        (str(round(math.degrees(mod.split_angle), 1)), p.color_value, p.text_size_normal),
                        ("°", p.color_value, p.text_size_normal),
                    ])

                # SHARP EDGES
                if mod.use_edge_sharp:
                    output_text.extend([(" Sharp Edges ", p.color_setting, p.text_size_normal)])
        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
