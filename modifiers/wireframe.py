import bpy.types
import prefs

def mod_wireframe(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                  mod: bpy.types.WireframeModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_WIREFRAME.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # THICKNESS
                output_text.extend([
                    (" Thickness ", p.color_setting, p.text_size_normal),
                    (str(round(mod.thickness, 3)), p.color_value, p.text_size_normal),
                ])

                # OFFSET
                output_text.extend([
                    (" Offset ", p.color_setting, p.text_size_normal),
                    (str(round(mod.offset, 2)), p.color_value, p.text_size_normal),
                ])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (str(mod.vertex_group), p.color_value, p.text_size_normal),
                    ])

                    # THICKNESS VERTEX GROUP
                    output_text.extend([
                        (" Factor ", p.color_setting, p.text_size_normal),
                        (str(round(mod.thickness_vertex_group, 2)), p.color_value, p.text_size_normal),
                    ])
                # CREASE WEIGHT
                if mod.use_crease:
                    output_text.extend([
                        (" Crease Weight ", p.color_setting, p.text_size_normal),
                        (str(round(mod.crease_weight, 2)), p.color_value, p.text_size_normal),
                    ])

                # OPTIONS
                if any([mod.use_even_offset, mod.use_relative_offset, mod.use_replace, mod.use_boundary, mod.material_offset]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # EVEN THICKNESS
                    if mod.use_even_offset:
                        output_text.extend([(" Even Thickness ", p.color_setting, p.text_size_normal)])

                    # RELATIVE THICKNESS
                    if mod.use_relative_offset:
                        output_text.extend([(" Relative Thickness ", p.color_setting, p.text_size_normal)])

                    # BOUNDARY
                    if mod.use_boundary:
                        output_text.extend([(" Boundary ", p.color_setting, p.text_size_normal)])

                    # REPLACE ORIGINAL
                    if mod.use_replace:
                        output_text.extend([(" Replace Original ", p.color_setting, p.text_size_normal)])

                    # MATERIAL OFFSET
                    if mod.material_offset:
                        output_text.extend([
                            (" Material Offset ", p.color_setting, p.text_size_normal),
                            (str(mod.material_offset), p.color_value, p.text_size_normal),
                        ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])
