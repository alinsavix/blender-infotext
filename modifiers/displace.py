import bpy.types
import prefs

def mod_displace(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                 mod: bpy.types.DisplaceModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_DISPLACE.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # MID LEVEL
                output_text.extend([
                    (" Mid Level ", p.color_setting, p.text_size_normal),
                    (str(round(mod.mid_level, 2)), p.color_value, p.text_size_normal),
                ])

                # STRENGTH
                output_text.extend([
                    (" Strength ", p.color_setting, p.text_size_normal),
                    (str(round(mod.strength, 2)), p.color_value, p.text_size_normal),
                ])

                # DIRECTION
                output_text.extend([
                    (" Direction ", p.color_setting, p.text_size_normal),
                    (str(mod.direction.lower().capitalize()), p.color_value, p.text_size_normal),
                ])
                if mod.direction in ['RGB_TO_XYZ', 'X', 'Y', 'Z']:
                    # DIRECTION
                    output_text.extend([
                        (" Space ", p.color_setting, p.text_size_normal),
                        (str(mod.space.lower().capitalize()), p.color_value, p.text_size_normal),
                    ])

                # # OPTIONS
                # if any([mod.vertex_group]):
                #     output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (str(mod.vertex_group), p.color_value, p.text_size_normal),
                    ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
