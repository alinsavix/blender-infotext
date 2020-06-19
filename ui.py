# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import bpy
from bpy.types import Menu, Panel
from .icon.icons import load_icons
from .functions import *
from .modifiers_popup import *
from .primitives import *
from .lattice import *
from .modals import*
from bpy.props import (StringProperty,
                       BoolProperty,
                       FloatVectorProperty,
                       FloatProperty,
                       EnumProperty,
                       IntProperty)


# class ActivateCarver(bpy.types.Operator):
#     bl_idname = "object.activate_carver"
#     bl_label = "Activate Carver"
#     bl_description = "ACTIVATE CARVER"
#     bl_options = {"REGISTER"}
#
#
#     def execute(self, context):
#         bpy.ops.wm.addon_enable(module="mesh_carver")
#         bpy.ops.wm.save_userpref()
#         return {"FINISHED"}


from bpy.props import *

# Simplify Popup


class SFC_PT_simplify_popup(bpy.types.Operator):
    # bl_idname = "SFC_PT_simplify_popup"
    bl_idname = "sfc.simplify_popup"
    bl_label = "Simplify Popup"

    def execute(self, context):
        return {'FINISHED'}

    def check(self, context):
        return True

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render
        cscene = scene.cycles

        layout.active = rd.use_simplify

        col = layout.column(align=True)
        col.label(text="Subdivision")
        row = col.row(align=True)
        row.prop(rd, "simplify_subdivision", text="Viewport")
        row.prop(rd, "simplify_subdivision_render", text="Render")

        col = layout.column(align=True)
        col.label(text="Child Particles")
        row = col.row(align=True)
        row.prop(rd, "simplify_child_particles", text="Viewport")
        row.prop(rd, "simplify_child_particles_render", text="Render")

        col = layout.column(align=True)
        split = col.split()
        sub = split.column()
        sub.label(text="Texture Limit Viewport")
        sub.prop(cscene, "texture_limit", text="")
        sub = split.column()
        sub.label(text="Texture Limit Render")
        sub.prop(cscene, "texture_limit_render", text="")

        split = layout.split()
        col = split.column()
        col.prop(cscene, "use_camera_cull")
        row = col.row()
        row.active = cscene.use_camera_cull
        row.prop(cscene, "camera_cull_margin")

        col = split.column()
        col.prop(cscene, "use_distance_cull")
        row = col.row()
        row.active = cscene.use_distance_cull
        row.prop(cscene, "distance_cull_margin", text="Distance")

        split = layout.split()
        col = split.column()
        col.prop(cscene, "ao_bounces")

        col = split.column()
        col.prop(cscene, "ao_bounces_render")

    def invoke(self, context, event):
        dpi_value = bpy.context.preferences.view.ui_scale
        return context.window_manager.invoke_props_dialog(self, width=dpi_value * 300, height=800)


# Vertex Groups
class SFC_PT_vertex_group(bpy.types.Operator):
    # bl_idname = "SFC_PT_vertex_group"
    bl_idname = "sfc.vertex_group"
    bl_label = "Vertex Groups Popup"

    def execute(self, context):
        return {'FINISHED'}

    def check(self, context):
        return True

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw(self, context):
        layout = self.layout

        ob = context.object
        group = ob.vertex_groups.active

        rows = 2
        if group:
            rows = 4

        row = layout.row()
        row.template_list("MESH_UL_vgroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=rows)

        col = row.column(align=True)
        col.operator("object.vertex_group_add", icon='ADD', text="")
        props = col.operator("object.vertex_group_remove", icon='REMOVE', text="")
        props.all_unlocked = props.all = False
        col.menu("MESH_MT_vertex_group_specials", icon='DOWNARROW_HLT', text="")
        if group:
            col.separator()
            col.operator("object.vertex_group_move", icon='TRIA_UP', text="").direction = 'UP'
            col.operator("object.vertex_group_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

        if ob.vertex_groups and (ob.mode == 'EDIT' or (
                ob.mode == 'WEIGHT_PAINT' and ob.type == 'MESH' and ob.data.use_paint_mask_vertex)):
            row = layout.row()

            sub = row.row(align=True)
            sub.operator("object.vertex_group_assign", text="Assign")
            sub.operator("object.vertex_group_remove_from", text="Remove")

            sub = row.row(align=True)
            sub.operator("object.vertex_group_select", text="Select")
            sub.operator("object.vertex_group_deselect", text="Deselect")

            layout.prop(context.tool_settings, "vertex_group_weight", text="Weight")

    def invoke(self, context, event):
        dpi_value = bpy.context.preferences.view.ui_scale
        coef = dpi_value * (-175) + 525
        return context.window_manager.invoke_props_dialog(self, width=dpi_value * coef, height=100)


# Show Random color Popup
class SFC_PT_color_Popup(bpy.types.Operator):
    # bl_idname = "SFC_PT_color_Popup"
    bl_idname = "object.random_color_popup"
    bl_label = "Material Popup"
    # bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}

    def check(self, context):
        return True

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def find_node_input(node, name):
        for input in node.inputs:
            if input.name == name:
                return input
        return None

    def draw(self, context):

        obj = bpy.context.active_object
        WM = bpy.context.window_manager

        layout = self.layout

        split = layout.split()
        col = split.column(align=True)

        if bpy.app.version >= (2, 78, 5):
            row = col.row(align=True)
            row.prop(WM, 'shader_type', expand=True)

        row = col.row(align=True)
        row.prop(WM, 'random_or_color', expand=True)
        if WM.random_or_color == 'color':
            row = col.row(align=True)
            row.template_color_picker(WM, "material_color", value_slider=True)

        # row = col.row(align=True)
        # row.scale_y = 1.5
        # if WM.random_or_color == 'color':
        #     row.operator("object.sfc_random_color", text="Add Color", icon='COLOR_RED')
        # else:
        #     row.operator("object.sfc_random_color", text="Add Random Color", icon='COLOR')

        row = col.row(align=True)
        row.prop(WM, "material_alpha", text="Transparency")

        row = col.row(align=True)
        if self.scale_y:
            row.scale_y = 1.5
        # if len(obj.material_slots):

        row.operator("object.sfc_random_color", text="Add Material", icon='COLOR')

        row = col.row(align=True)
        if len(obj.material_slots):
            is_sortable = len(obj.material_slots) > 1
            rows = 1
            if (is_sortable):
                rows = 4

            row = layout.row()

            row.template_list("MATERIAL_UL_matslots", "", obj, "material_slots",
                              obj, "active_material_index", rows=rows)

            col = row.column(align=True)
            # col.operator("object.material_slot_add", icon='ADD', text="")
            col.operator("object.material_slot_remove", icon='REMOVE', text="")

            # col.menu("MATERIAL_MT_specials", icon='DOWNARROW_HLT', text="")
            if is_sortable:
                col.separator()
                col.operator("object.material_slot_move", icon='TRIA_UP', text="").direction = 'UP'
                col.operator("object.material_slot_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

            if obj.mode == 'EDIT':
                row = layout.row()
                row.operator("object.material_slot_assign", text="Assign")
                row.operator("object.material_slot_select", text="Select")
                row.operator("object.material_slot_deselect", text="Deselect")

            row = layout.row()
            row.template_ID(obj, "active_material")
            activeMaterial = bpy.context.active_object.active_material
            currentNodeTree = activeMaterial.node_tree
            split = layout.split()
            col = split.column(align=True)

            # bpy.data.node_groups["Shader Nodetree"].nodes["Principled BSDF"].distribution = 'MULTI_GGX'

            # if currentNodeTree.nodes == "Principled BSDF":
            if activeMaterial and currentNodeTree.nodes["Principled BSDF"]:
                row = col.row(align=True)
                row.separator()
                row.prop(currentNodeTree.nodes["Principled BSDF"], "distribution", text="")
                row = col.row(align=True)
                row.label(text="Principled shader")
                # row = col.row(align=True)
                # row.prop(WM, "material_color", text="Color")
                row = col.row(align=True)
                index_4 = 4
                row.prop(currentNodeTree.nodes["Principled BSDF"].inputs[index_4], "default_value", text="Metallic:")
                row = col.row(align=True)
                index_5 = 5
                row.prop(currentNodeTree.nodes["Principled BSDF"].inputs[index_5], "default_value", text="Specular:")
                row = col.row(align=True)
                index_6 = 6
                row.prop(currentNodeTree.nodes["Principled BSDF"].inputs[index_6],
                         "default_value", text="Specular Tint:")
                row = col.row(align=True)
                index_7 = 7
                row.prop(currentNodeTree.nodes["Principled BSDF"].inputs[index_7], "default_value", text="Roughness:")
                row = col.row(align=True)
                row.separator()
                row = col.row(align=True)
                index_8 = 8
                row.prop(currentNodeTree.nodes["Principled BSDF"].inputs[index_8], "default_value", text="Anisotropic:")
                row = col.row(align=True)
                index_9 = 9
                row.prop(currentNodeTree.nodes["Principled BSDF"].inputs[index_9],
                         "default_value", text="Anisotropic Rot:")
                row = col.row(align=True)
                row.separator()
                row = col.row(align=True)
                index_10 = 10
                row.prop(currentNodeTree.nodes["Principled BSDF"].inputs[index_10], "default_value", text="Sheen:")
                row = col.row(align=True)
                index_11 = 11
                row.prop(currentNodeTree.nodes["Principled BSDF"].inputs[index_11], "default_value", text="Sheen Tint:")
                row = col.row(align=True)
                row.separator()
                row = col.row(align=True)
                index_12 = 12
                row.prop(currentNodeTree.nodes["Principled BSDF"].inputs[index_12], "default_value", text="Clearcoat:")
                row = col.row(align=True)
                index_13 = 13
                row.prop(currentNodeTree.nodes["Principled BSDF"].inputs[index_13],
                         "default_value", text="Clearcoat Roughness:")
                row = col.row(align=True)
                row.separator()
                row = col.row(align=True)
                index_14 = 14
                row.prop(currentNodeTree.nodes["Principled BSDF"].inputs[index_14], "default_value", text="IOR:")
                row = col.row(align=True)
                index_15 = 15
                row.prop(currentNodeTree.nodes["Principled BSDF"].inputs[index_15],
                         "default_value", text="Transmission:")

                if currentNodeTree.nodes["Principled BSDF"].distribution == 'GGX':
                    row = col.row(align=True)
                    index_16 = 16
                    row.prop(currentNodeTree.nodes["Principled BSDF"].inputs[index_16], "default_value",
                             text="Transmission Roughness:")

    def invoke(self, context, event):
        dpi_value = bpy.context.preferences.view.ui_scale
        coef = dpi_value * (-175) + 525
        return context.window_manager.invoke_props_dialog(self, width=dpi_value * coef, height=100)


# LATTICE POPUP
class SFC_PT_lattice_popup(bpy.types.Operator):
    # bl_idname = "SFC_PT_lattice_popup"
    bl_idname = "object.sfc_lattice_popup"
    bl_label = "Lattice Popup"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def check(self, context):

        return True

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        WM = bpy.context.window_manager
        self.scale_y = get_addon_preferences().scale_y

        layout = self.layout
        split = layout.split()
        col = split.column(align=True)
        row = col.row(align=True)
        if self.scale_y:
            row.scale_y = 1.5
        row.operator("object.sfc_apply_lattice_objects", text="Apply Lattice", icon='FILE_TICK')
        row.operator("object.sfc_remove_lattice_objects", text="", icon='X')
        row = col.row(align=True)
        row.prop(context.object.data, "points_u")
        row = col.row(align=True)
        row.prop(context.object.data, "points_v")
        row = col.row(align=True)
        row.prop(context.object.data, "points_w")
        row = col.row(align=True)
        row.prop(WM, "lattice_interp", text="")

    def invoke(self, context, event):
        dpi_value = bpy.context.preferences.view.ui_scale
        coef = dpi_value * (-175) + 525
        return context.window_manager.invoke_props_dialog(self, width=dpi_value * coef, height=100)


# Show Text Options Popup
class SFC_PT_show_text_options_popup(bpy.types.Operator):
    bl_idname = "object.sfc_text_options_popup"
    bl_label = "Text Options"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    show_text_options_tab: EnumProperty(
        items=(('show', "Show Hide Text", ""),
               ('edit', "Edit Text", "")),
        default='show'
    )

    def check(self, context):

        return True

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        addon_pref = get_addon_preferences()
        layout = self.layout
        row = layout.row(align=True)
        row.prop(self, "show_text_options_tab", expand=True)

        if self.show_text_options_tab == 'show':

            box = layout.box()
            split = box.split()
            col = split.column(align=True)
            row = col.row(align=True)
            row.label(text="Text in the viewport")
            row.prop(addon_pref, "drawText", text="")

            row = col.row(align=True)
            row.label(text="Object Mode")
            row.prop(addon_pref, "show_object_mode", text="")

            # row = col.row(align=True)
            # row.label(text="Object Type & Name")
            # row.prop(addon_pref, "show_object_name", text="")

            row = col.row(align=True)
            row.label(text="Transforms")
            row.prop(addon_pref, "show_loc_rot_scale", text="")

            row = col.row(align=True)
            row.label(text="Vert/Faces/Tris/Ngons")
            row.prop(addon_pref, "show_vert_face_tris", text="")

            row = col.row(align=True)
            row.label(text="Show Object information")
            row.prop(addon_pref, "show_object_info", text="")

            row = col.row(align=True)
            row.label(text="Modifiers")
            row.prop(addon_pref, "show_modifiers", text="")

            row = col.row(align=True)
            row.label(text="Simple Mode for Modifiers")
            row.prop(addon_pref, "simple_text_mode", text="")

            row = col.row(align=True)
            row.label(text="Show Addons Keymaps")
            row.prop(addon_pref, "show_keymaps", text="")

            row = col.row(align=True)
            row.label(text="Show Blender Keymaps")
            row.prop(addon_pref, "show_blender_keymaps", text="")

        if self.show_text_options_tab == 'edit':

            box = layout.box()
            split = box.split()
            col = split.column(align=True)
            row = col.row(align=True)
            row.label(text="Title Color")
            row.prop(addon_pref, "title")

            row = col.row(align=True)
            row.label(text="Settings Color")
            row.prop(addon_pref, "setting")

            row = col.row(align=True)
            row.label(text="Value Color")
            row.prop(addon_pref, "value")

            row = col.row(align=True)
            row.label(text="Modifier Hidden")
            row.prop(addon_pref, "hidden")

            row = col.row(align=True)
            row.label(text="Text Size Max")
            row.prop(addon_pref, "text_size_max")

            row = col.row(align=True)
            row.label(text="Text Size Min")
            row.prop(addon_pref, "text_size_mini")

            row = col.row(align=True)
            row.label(text="Text Space")
            row.prop(addon_pref, "sfc_text_space")

            row = col.row(align=True)
            row.label(text="Text X position")
            row.prop(addon_pref, "sfc_text_pos_x")

            row = col.row(align=True)
            row.label(text="Text Y position")
            row.prop(addon_pref, "sfc_text_pos_y")

            row = col.row(align=True)
            row.label(text="Activate Shadows")
            row.prop(addon_pref, "sfc_text_shadow", text="      ")

            if addon_pref.sfc_text_shadow:

                row = col.row(align=True)
                row.label(text="Color")
                row.prop(addon_pref, "sfc_shadow_color")

                row = col.row(align=True)
                row.label(text="Transparency")
                row.prop(addon_pref, "sfc_shadow_alpha")

                row = col.row(align=True)
                row.label(text="Offset X")
                row.prop(addon_pref, "sfc_offset_shadow_x")

                row = col.row(align=True)
                row.label(text="Offset Y")
                row.prop(addon_pref, "sfc_offset_shadow_y")

        row = col.row(align=True)
        row.operator_context = 'EXEC_AREA'
        row.operator("wm.save_userpref", text="Save", icon='FILE_TICK')
        row.operator("object.reset_prefs", text="Reset", icon='RECOVER_LAST')

    def invoke(self, context, event):
        dpi_value = bpy.context.preferences.view.ui_scale
        coef = dpi_value * (-175) + 425
        return context.window_manager.invoke_props_dialog(self, width=dpi_value * coef, height=100)

# Primitives Operations


class SFC_OT_primitives_popup(bpy.types.Operator):
    bl_idname = "sfc.primitives_popup"
    bl_label = "Speedflow Companion Primitives"

    def execute(self, context):
        return {'FINISHED'}

    def check(self, context):
        return True

    # @classmethod
    # def poll(cls, context):
    #     return context.active_object is not None

    def draw(self, context):
        SFC_prim = context.window_manager.SFC_prim
        icons = load_icons()
        layout = self.layout
        box = layout.box()
        row = box.row(align=True)
        row.prop(SFC_prim, "align_cursor_rot", text="Cursor Rot")
        row.prop(SFC_prim, "add_mirror", text="Mirror")
        if SFC_prim.add_mirror:
            row = box.row(align=True)
            row.prop(SFC_prim, "mirror_axis_xyz", expand=True)

        if SFC_prim.add_boolean == False:
            SFC_prim.add_rebool = False

        row = box.row(align=True)
        row.prop(SFC_prim, "add_boolean", text="Boolean")
        if SFC_prim.add_boolean:
            row.prop(SFC_prim, "add_rebool", text="Rebool")

        if SFC_prim.add_boolean or SFC_prim.add_rebool:
            row = box.row(align=True)
            if SFC_prim.add_rebool:
                SFC_prim.boolean_enum = 'DIFFERENCE'
            row.prop(SFC_prim, "boolean_enum", expand=True)

        # # -------DEFAULT PRIMITIVES
        #
        # layout.label(text="Default Primitives", icon='MESH_CUBE')
        # row = layout.row(align=True)
        # row.scale_x = 1.3
        # op = row.operator("sfc.primitives_new", text="", icon='DOT')
        # op.primitives_enum = "default_prim"
        # op.default_enum = 'vertex'
        #
        # op = row.operator("sfc.primitives_new", text="", icon='MESH_PLANE')
        # op.primitives_enum = "default_prim"
        # op.default_enum = 'plane'
        #
        # op = row.operator("sfc.primitives_new", text="", icon='MESH_CUBE')
        # op.primitives_enum = "default_prim"
        # op.default_enum = 'cube'
        #
        # op = row.operator("sfc.primitives_new", text="", icon='MESH_CIRCLE')
        # op.primitives_enum = "default_prim"
        # op.default_enum = 'circle'
        #
        # op = row.operator("sfc.primitives_new", text="", icon='MESH_UVSPHERE')
        # op.primitives_enum = "default_prim"
        # op.default_enum = 'uv_sphere'
        #
        # op = row.operator("sfc.primitives_new", text="", icon='MESH_ICOSPHERE')
        # op.primitives_enum = "default_prim"
        # op.default_enum = 'ico_sphere'
        #
        # op = row.operator("sfc.primitives_new", text="", icon='MESH_CYLINDER')
        # op.primitives_enum = "default_prim"
        # op.default_enum = 'cylinder'
        #
        # op = row.operator("sfc.primitives_new", text="", icon='MESH_CONE')
        # op.primitives_enum = "default_prim"
        # op.default_enum = 'cone'
        #
        # op = row.operator("sfc.primitives_new", text="", icon='MESH_TORUS')
        # op.primitives_enum = "default_prim"
        # op.default_enum = 'torus'
        #
        # row = layout.row(align=True)
        # row.scale_x = 1.5
        # op = row.operator("sfc.primitives_new", text="", icon='MESH_GRID')
        # op.primitives_enum = "default_prim"
        # op.default_enum = 'grid'
        #
        # op = row.operator("sfc.primitives_new", text="", icon='CURVE_BEZCURVE')
        # op.primitives_enum = "default_prim"
        # op.default_enum = 'bezier_curve'
        #
        # op = row.operator("sfc.primitives_new", text="", icon='CURVE_BEZCIRCLE')
        # op.primitives_enum = "default_prim"
        # op.default_enum = 'bezier_circle'
        #
        # row.operator("sfc.cursor_line", text="", icon='LINE_DATA')
        #
        # op = row.operator("sfc.primitives_new", text="", icon='MESH_MONKEY')
        # op.primitives_enum = "default_prim"
        # op.default_enum = 'monkey'
        #
        # # -------SCREW PRIMITIVES
        # layout.label(text="Screw Primitives", icon='MOD_SCREW')
        # row = layout.row(align=True)
        # row.scale_x = 1.3
        # op = row.operator("sfc.primitives_new", text="", icon='DOT')
        # op.primitives_enum = "screw_prim"
        # op.screw_enum = 'screw_7'
        #
        # op = row.operator("sfc.primitives_new", text="", icon='MESH_CIRCLE')
        # op.primitives_enum = "screw_prim"
        # op.screw_enum = 'screw_6'
        #
        # op = row.operator("sfc.primitives_new", text="", icon='MESH_CYLINDER')
        # op.primitives_enum = "screw_prim"
        # op.screw_enum = 'screw_1'
        #
        # screw = icons.get("prim_screw_2")
        # op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
        # op.primitives_enum = "screw_prim"
        # op.screw_enum = 'screw_2'
        #
        # screw = icons.get("prim_screw_3")
        # op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
        # op.primitives_enum = "screw_prim"
        # op.screw_enum = 'screw_3'
        #
        # screw = icons.get("prim_screw_4")
        # op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
        # op.primitives_enum = "screw_prim"
        # op.screw_enum = 'screw_4'
        #
        # screw = icons.get("prim_screw_5")
        # op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
        # op.primitives_enum = "screw_prim"
        # op.screw_enum = 'screw_5'
        #
        # # -------EDITABLE PRIMITIVES
        # layout.label(text="Editable Primitives", icon='MODIFIER')
        # row = layout.row(align=True)
        # row.scale_x = 1.3
        # op = row.operator("sfc.primitives_new", icon='MESH_CUBE', text="")
        # op.primitives_enum = "editable_prim"
        # op.editable_enum = 'cube'
        #
        # op = row.operator("sfc.primitives_new", icon='MESH_UVSPHERE', text="")
        # op.primitives_enum = "editable_prim"
        # op.editable_enum = 'sphere'
        #
        # op = row.operator("sfc.primitives_new", icon='MESH_CYLINDER', text="")
        # op.primitives_enum = "editable_prim"
        # op.editable_enum = 'cylinder'
        #
        # op = row.operator("sfc.primitives_new", icon='MESH_CONE', text="")
        # op.primitives_enum = "editable_prim"
        # op.editable_enum = 'cone'
        #
        # op = row.operator("sfc.primitives_new", icon='MESH_TORUS', text="")
        # op.primitives_enum = "editable_prim"
        # op.editable_enum = 'torus'
        #
        # op = row.operator("sfc.primitives_new", icon='MESH_GRID', text="")
        # op.primitives_enum = "editable_prim"
        # op.editable_enum = 'grid'
        #
        # op = row.operator("sfc.primitives_new", icon='MESH_CAPSULE', text="")
        # op.primitives_enum = "editable_prim"
        # op.editable_enum = 'capsule'
        #
        # op = row.operator("sfc.primitives_new", icon='MATSPHERE', text="")
        # op.primitives_enum = "editable_prim"
        # op.editable_enum = 'quad_sphere'
        #
        # op = row.operator("sfc.primitives_new", icon='MESH_CIRCLE', text="")
        # op.primitives_enum = "editable_prim"
        # op.editable_enum = 'circle'
        #
        # # -------CUSTOM PRIMITIVES
        # layout.label(text="Custom Primitives", icon='META_CAPSULE')
        # row = layout.row(align=True)
        #
        # row.scale_x = 1.3
        # op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
        # op.primitives_enum = "custom_prim"
        # op.custom_enum = 'rounded_cube'
        #
        # op = row.operator("sfc.primitives_new", icon='META_PLANE', text="")
        # op.primitives_enum = "custom_prim"
        # op.custom_enum = 'rounded_plane'
        #
        # op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
        # op.primitives_enum = "custom_prim"
        # op.custom_enum = 'rounded_plane_round'
        #
        # op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
        # op.primitives_enum = "custom_prim"
        # op.custom_enum = 'rounded_plane_2'
        #
        # custom = icons.get("prim_cross")
        # op = row.operator("sfc.primitives_new", icon_value=custom.icon_id, text="")
        # op.custom_enum = 'cross'
        #
        # custom = icons.get("prim_cross_rounded")
        # op = row.operator("sfc.primitives_new", icon_value=custom.icon_id, text="")
        # op.custom_enum = 'rounded_cross'
        #
        # op = row.operator("sfc.primitives_new", icon='MESH_CAPSULE', text="")
        # op.primitives_enum = "custom_prim"
        # op.custom_enum = 'long_cylinder'
        #
        # op = row.operator("sfc.primitives_new", icon='IPO_CONSTANT', text="")
        # op.primitives_enum = "editable_prim"
        # op.editable_enum = 'line'
        #
        # op = row.operator("sfc.primitives_new", icon='ANTIALIASED', text="")
        # op.primitives_enum = "editable_prim"
        # op.editable_enum = 'tube'

    def invoke(self, context, event):
        # dpi_value = bpy.context.preferences.view.ui_scale
        # coef = dpi_value * (-175) #+ 125
        # return context.window_manager.invoke_props_dialog(self, width=dpi_value * coef, height=100)

        return context.window_manager.invoke_props_dialog(self, width=200, height=100)


# Primitives
def SFC_Primitives(self, context):
    obj = context.active_object
    SFC = bpy.context.window_manager.SFC
    # align_to_view = SFC.align_to_view

    icons = load_icons()
    layout = self.layout
    pie = layout.menu_pie()
    split = pie.split()
    col = split.column(align=True)

    row = col.row(align=True)
    row.separator()
    row = col.row(align=True)
    if self.scale_y:
        row.scale_y = 1.2

    SFC_prim = context.window_manager.SFC_prim

    row = col.row(align=True)
    row.prop(SFC_prim, "align_cursor_rot", text="Align To C")

    # -------DEFAULT PRIMITIVES

    col.label(text="Default Primitives", icon='MESH_CUBE')
    row = col.row(align=True)
    op = row.operator("sfc.primitives_new", text="", icon='DOT')
    op.primitives_enum = "default_prim"
    op.default_enum = 'vertex'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_PLANE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'plane'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_CUBE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'cube'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_CIRCLE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'circle'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_UVSPHERE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'uv_sphere'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_ICOSPHERE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'ico_sphere'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_CYLINDER')
    op.primitives_enum = "default_prim"
    op.default_enum = 'cylinder'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_CONE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'cone'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_TORUS')
    op.primitives_enum = "default_prim"
    op.default_enum = 'torus'

    row = col.row(align=True)
    op = row.operator("sfc.primitives_new", text="", icon='MESH_GRID')
    op.primitives_enum = "default_prim"
    op.default_enum = 'grid'

    op = row.operator("sfc.primitives_new", text="", icon='CURVE_BEZCURVE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'bezier_curve'

    op = row.operator("sfc.primitives_new", text="", icon='CURVE_BEZCIRCLE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'bezier_circle'

    row.operator("sfc.cursor_line", text="", icon='LINE_DATA')

    op = row.operator("sfc.primitives_new", text="", icon='MESH_MONKEY')
    op.primitives_enum = "default_prim"
    op.default_enum = 'monkey'

    # -------SCREW PRIMITIVES
    col.label(text="Screw Primitives", icon='MOD_SCREW')
    row = col.row(align=True)
    op = row.operator("sfc.primitives_new", text="", icon='DOT')
    op.primitives_enum = "screw_prim"
    op.screw_enum = 'screw_7'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_CIRCLE')
    op.primitives_enum = "screw_prim"
    op.screw_enum = 'screw_6'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_CYLINDER')
    op.primitives_enum = "screw_prim"
    op.screw_enum = 'screw_1'

    screw = icons.get("prim_screw_2")
    op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
    op.primitives_enum = "screw_prim"
    op.screw_enum = 'screw_2'

    screw = icons.get("prim_screw_3")
    op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
    op.primitives_enum = "screw_prim"
    op.screw_enum = 'screw_3'

    screw = icons.get("prim_screw_4")
    op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
    op.primitives_enum = "screw_prim"
    op.screw_enum = 'screw_4'

    screw = icons.get("prim_screw_5")
    op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
    op.primitives_enum = "screw_prim"
    op.screw_enum = 'screw_5'

    # -------EDITABLE PRIMITIVES
    col.label(text="Editable Primitives", icon='MODIFIER')
    row = col.row(align=True)
    op = row.operator("sfc.primitives_new", icon='MESH_CUBE', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'cube'

    op = row.operator("sfc.primitives_new", icon='MESH_UVSPHERE', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'sphere'

    op = row.operator("sfc.primitives_new", icon='MESH_CYLINDER', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'cylinder'

    op = row.operator("sfc.primitives_new", icon='MESH_CONE', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'cone'

    op = row.operator("sfc.primitives_new", icon='MESH_TORUS', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'torus'

    op = row.operator("sfc.primitives_new", icon='MESH_GRID', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'grid'

    op = row.operator("sfc.primitives_new", icon='MESH_CAPSULE', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'capsule'

    op = row.operator("sfc.primitives_new", icon='MATSPHERE', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'quad_sphere'

    op = row.operator("sfc.primitives_new", icon='MESH_CIRCLE', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'circle'

    # -------CUSTOM PRIMITIVES
    col.label(text="Custom Primitives", icon='META_CAPSULE')
    row = col.row(align=True)
    op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
    op.primitives_enum = "custom_prim"
    op.custom_enum = 'rounded_cube'

    op = row.operator("sfc.primitives_new", icon='META_PLANE', text="")
    op.primitives_enum = "custom_prim"
    op.custom_enum = 'rounded_plane'

    op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
    op.primitives_enum = "custom_prim"
    op.custom_enum = 'rounded_plane_round'

    op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
    op.primitives_enum = "custom_prim"
    op.custom_enum = 'rounded_plane_2'

    custom = icons.get("prim_cross")
    op = row.operator("sfc.primitives_new", icon_value=custom.icon_id, text="")
    op.custom_enum = 'cross'

    custom = icons.get("prim_cross_rounded")
    op = row.operator("sfc.primitives_new", icon_value=custom.icon_id, text="")
    op.custom_enum = 'rounded_cross'

    op = row.operator("sfc.primitives_new", icon='MESH_CAPSULE', text="")
    op.primitives_enum = "custom_prim"
    op.custom_enum = 'long_cylinder'

    op = row.operator("sfc.primitives_new", icon='IPO_CONSTANT', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'line'

    op = row.operator("sfc.primitives_new", icon='ANTIALIASED', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'tube'

    # -------TOOLS
    col.label(text="Tools", icon='TOOL_SETTINGS')
    col.operator("sfc.cursor_tools", text="Copy Cursor Rotation",
                 icon='PIVOT_CURSOR').cursor_tools = 'copy_cursor_rot'
    col.operator("sfc.cursor_tools", text="Selection To Cursor",
                 icon='PIVOT_BOUNDBOX').cursor_tools = 'selection_to_cursor'
    col.operator("sfc.cursor_tools", text="Cursor To Selection + Rotation",
                 icon='PIVOT_CURSOR').cursor_tools = 'cursor_to_selection_rot'
    col.operator("sfc.cursor_tools", text="Align View To Cursor Rotation",
                 icon='VIEW_PERSPECTIVE').cursor_tools = 'align_view_to_cursor_rot'
    col.operator("sfc.cursor_tools", text="Align Cursor To Object Rotation",
                 icon='EMPTY_AXIS').cursor_tools = 'align_cursor_to_object_rot'


# --------------------------------------------------------------------------------
#  4 - LEFT
# --------------------------------------------------------------------------------
def SFC_OBJMode_Modifiers(self, context):
    obj = context.active_object
    icons = load_icons()
    layout = self.layout
    pie = layout.menu_pie()
    col = pie.column(align=True)
    row = col.row(align=True)
    if self.scale_y:
        row.scale_y = 1.5
    row.scale_x = 1.3
    modifiers = icons.get("icon_modifiers")
    row.operator("object.apply_remove_hide_modifiers", text="Modifiers", icon_value=modifiers.icon_id)

    if self.use_normals_buttons:
        if obj.modifiers:
            row.operator("object.sfc_hide_modifiers", text='', icon='RESTRICT_VIEW_OFF')
            row.operator("object.sfc_apply_modifiers", text='', icon='FILE_TICK')
            row.operator("object.sfc_remove_modifiers", text='', icon='X')
# --------------------------------------------------------------------------------
# 6 - RIGHT
# --------------------------------------------------------------------------------


def SFC_OBJMode_Right(self, context):
    icons = load_icons()
    layout = self.layout
    pie = layout.menu_pie()

    col = pie.column(align=True)
    row = col.row(align=True)
    if self.scale_y:
        row.scale_y = 1.5
    row.scale_x = 1.1
    subsurf = icons.get("icon_subsurf")
    row.operator("object.sfc_subdiv_booleans_prepare", text="Subdiv Booleans", icon_value=subsurf.icon_id)
    if self.use_normals_buttons:
        row.operator("object.sfc_clean_subdiv_booleans", text="", icon='X')

    row = col.row(align=True)
    if self.scale_y:
        row.scale_y = 1.5
    row.scale_x = 1.1
    boolean = icons.get("icon_add_boolean")
    row.operator("object.sfc_show_bool_objects", text="Show/Hide Bool Object", icon_value=boolean.icon_id)
# --------------------------------------------------------------------------------
# 2 - BOTTOM
# --------------------------------------------------------------------------------


def SFC_OBJMode_Bottom(self, context):

    layout = self.layout
    pie = layout.menu_pie()

    # 2 - BOTTOM
    col = pie.column(align=True)
    SFC_prim = context.window_manager.SFC_prim
    icons = load_icons()

    row = col.row(align=True)
    row.prop(SFC_prim, "align_cursor_rot", text="Cursor Rot")
    row.prop(SFC_prim, "add_mirror", text="Mirror")
    if SFC_prim.add_mirror:
        row = col.row(align=True)
        row.prop(SFC_prim, "mirror_axis_xyz", expand=True)

    if SFC_prim.add_boolean == False:
        SFC_prim.add_rebool = False

    row = col.row(align=True)
    row.prop(SFC_prim, "add_boolean", text="Boolean")
    if SFC_prim.add_boolean:
        row.prop(SFC_prim, "add_rebool", text="Rebool")

    if SFC_prim.add_boolean or SFC_prim.add_rebool:
        row = col.row(align=True)
        if SFC_prim.add_rebool:
            SFC_prim.boolean_enum = 'DIFFERENCE'
        row.prop(SFC_prim, "boolean_enum", expand=True)

    row = col.row(align=True)
    row.operator("sfc.primitives_popup", text="Popup Settings", icon='MODIFIER')

    # -------DEFAULT PRIMITIVES

    col.label(text="Default Primitives", icon='MESH_CUBE')
    row = col.row(align=True)
    op = row.operator("sfc.primitives_new", text="", icon='DOT')
    op.primitives_enum = "default_prim"
    op.default_enum = 'vertex'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_PLANE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'plane'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_CUBE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'cube'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_CIRCLE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'circle'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_UVSPHERE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'uv_sphere'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_ICOSPHERE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'ico_sphere'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_CYLINDER')
    op.primitives_enum = "default_prim"
    op.default_enum = 'cylinder'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_CONE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'cone'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_TORUS')
    op.primitives_enum = "default_prim"
    op.default_enum = 'torus'

    row = col.row(align=True)

    op = row.operator("sfc.primitives_new", text="", icon='MESH_GRID')
    op.primitives_enum = "default_prim"
    op.default_enum = 'grid'

    op = row.operator("sfc.primitives_new", text="", icon='CURVE_BEZCURVE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'bezier_curve'

    op = row.operator("sfc.primitives_new", text="", icon='CURVE_BEZCIRCLE')
    op.primitives_enum = "default_prim"
    op.default_enum = 'bezier_circle'

    row.operator("sfc.cursor_line", text="", icon='LINE_DATA')

    op = row.operator("sfc.primitives_new", text="", icon='MESH_MONKEY')
    op.primitives_enum = "default_prim"
    op.default_enum = 'monkey'

    # -------SCREW PRIMITIVES
    col.label(text="Screw Primitives", icon='MOD_SCREW')
    row = col.row(align=True)
    op = row.operator("sfc.primitives_new", text="", icon='DOT')
    op.primitives_enum = "screw_prim"
    op.screw_enum = 'screw_7'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_CIRCLE')
    op.primitives_enum = "screw_prim"
    op.screw_enum = 'screw_6'

    op = row.operator("sfc.primitives_new", text="", icon='MESH_CYLINDER')
    op.primitives_enum = "screw_prim"
    op.screw_enum = 'screw_1'

    screw = icons.get("prim_screw_2")
    op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
    op.primitives_enum = "screw_prim"
    op.screw_enum = 'screw_2'

    screw = icons.get("prim_screw_3")
    op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
    op.primitives_enum = "screw_prim"
    op.screw_enum = 'screw_3'

    screw = icons.get("prim_screw_4")
    op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
    op.primitives_enum = "screw_prim"
    op.screw_enum = 'screw_4'

    screw = icons.get("prim_screw_5")
    op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
    op.primitives_enum = "screw_prim"
    op.screw_enum = 'screw_5'

    # -------EDITABLE PRIMITIVES
    col.label(text="Editable Primitives", icon='MODIFIER')
    row = col.row(align=True)
    op = row.operator("sfc.primitives_new", icon='MESH_CUBE', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'cube'

    op = row.operator("sfc.primitives_new", icon='MESH_UVSPHERE', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'sphere'

    op = row.operator("sfc.primitives_new", icon='MESH_CYLINDER', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'cylinder'

    op = row.operator("sfc.primitives_new", icon='MESH_CONE', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'cone'

    op = row.operator("sfc.primitives_new", icon='MESH_TORUS', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'torus'

    op = row.operator("sfc.primitives_new", icon='MESH_GRID', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'grid'

    op = row.operator("sfc.primitives_new", icon='MESH_CAPSULE', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'capsule'

    op = row.operator("sfc.primitives_new", icon='MATSPHERE', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'quad_sphere'

    op = row.operator("sfc.primitives_new", icon='MESH_CIRCLE', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'circle'

    # -------CUSTOM PRIMITIVES
    col.label(text="Custom Primitives", icon='META_CAPSULE')
    row = col.row(align=True)

    op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
    op.primitives_enum = "custom_prim"
    op.custom_enum = 'rounded_cube'

    op = row.operator("sfc.primitives_new", icon='META_PLANE', text="")
    op.primitives_enum = "custom_prim"
    op.custom_enum = 'rounded_plane'

    op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
    op.primitives_enum = "custom_prim"
    op.custom_enum = 'rounded_plane_round'

    op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
    op.primitives_enum = "custom_prim"
    op.custom_enum = 'rounded_plane_2'

    custom = icons.get("prim_cross")
    op = row.operator("sfc.primitives_new", icon_value=custom.icon_id, text="")
    op.custom_enum = 'cross'

    custom = icons.get("prim_cross_rounded")
    op = row.operator("sfc.primitives_new", icon_value=custom.icon_id, text="")
    op.custom_enum = 'rounded_cross'

    op = row.operator("sfc.primitives_new", icon='MESH_CAPSULE', text="")
    op.primitives_enum = "custom_prim"
    op.custom_enum = 'long_cylinder'

    op = row.operator("sfc.primitives_new", icon='IPO_CONSTANT', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'line'

    op = row.operator("sfc.primitives_new", icon='ANTIALIASED', text="")
    op.primitives_enum = "editable_prim"
    op.editable_enum = 'tube'

    # -------TOOLS
    col.label(text="Tools", icon='TOOL_SETTINGS')
    col.operator("sfc.cursor_tools", text="Copy Cursor Rotation",
                 icon='PIVOT_CURSOR').cursor_tools = 'copy_cursor_rot'
    col.operator("sfc.cursor_tools", text="Selection To Cursor",
                 icon='PIVOT_BOUNDBOX').cursor_tools = 'selection_to_cursor'
    col.operator("sfc.cursor_tools", text="Cursor To Selection + Rotation",
                 icon='PIVOT_CURSOR').cursor_tools = 'cursor_to_selection_rot'
    col.operator("sfc.cursor_tools", text="Align View To Cursor Rotation",
                 icon='VIEW_PERSPECTIVE').cursor_tools = 'align_view_to_cursor_rot'
    col.operator("sfc.cursor_tools", text="Align Cursor To Object Rotation",
                 icon='EMPTY_AXIS').cursor_tools = 'align_cursor_to_object_rot'

# --------------------------------------------------------------------------------
# 8 - TOP
# --------------------------------------------------------------------------------


def SFC_OBJMode_Top(self, context):
    icons = load_icons()
    layout = self.layout
    pie = layout.menu_pie()

    # pie.separator()
    box = pie.split().column()
    row = box.split(align=True)
    if hasattr(bpy.types, "MESH_OT_snap_utilities_line"):
        if self.scale_y:
            row.scale_y = 1.5
        row.scale_x = 1.7
        line = icons.get("icon_line")
        row.operator("mesh.snap_utilities_line", text="Line", icon_value=line.icon_id)
    else:
        if self.scale_y:
            row.scale_y = 1.5
        row.scale_x = 1.1
        row.operator("object.sfc_activate_line", text="Snap Utilities Line", icon='ERROR')

# --------------------------------------------------------------------------------
# 7 - TOP - LEFT
# --------------------------------------------------------------------------------


def SFC_OBJMode_Top_Left(self, context):
    addon_pref = get_addon_preferences()

    if bpy.context.object is not None:
        mesh = context.active_object.data

    icons = load_icons()
    layout = self.layout
    pie = layout.menu_pie()

    col = pie.column(align=True)
    row = col.row(align=True)
    if self.scale_y:
        row.scale_y = 1.5
    row.scale_x = 1.1

    if bpy.context.object.type == 'MESH':
        if context.object.data.use_auto_smooth == True:
            autosmooth = icons.get("icon_autosmooth")
            row.operator("object.sfc_toggle_smooth", text="AutoSmooth", icon_value=autosmooth.icon_id)
            row = col.row(align=True)
            row.prop(mesh, "auto_smooth_angle", text="Angle")
        else:
            autosmooth_off = icons.get("icon_autosmooth_off")
            row.operator("object.sfc_toggle_smooth", text="AutoSmooth", icon_value=autosmooth_off.icon_id)

    if self.use_normals_buttons:
        row = col.row(align=True)
        if self.scale_y:
            row.scale_y = 1.5
        row.scale_x = 1.1
        wire = icons.get("icon_wire")
        row.operator("object.sfc_wire_mode", text="Wire", icon_value=wire.icon_id)
        solid = icons.get("icon_solid")
        row.operator("object.sfc_solid_mode", text="Solid", icon_value=solid.icon_id)
        bounds = icons.get("icon_bounds")
        row.operator("object.sfc_bounds_mode", text="Bound", icon_value=bounds.icon_id)
    else:
        row = col.row(align=True)
        if self.scale_y:
            row.scale_y = 1.5
        row.scale_x = 1.1
        wire = icons.get("icon_wire")
        row.operator("object.sfc_display_mode", text="Display Mode", icon_value=wire.icon_id)

    draw_text = icons.get("draw_text")
    # row.prop(addon_pref, "drawText", text="", icon_value=draw_text.icon_id)
    row.operator("object.show_text_options", text="", icon_value=draw_text.icon_id)

    # if bpy.context.scene.render.engine == 'CYCLES':
    #     row = col.row(align=True)
    #     if self.scale_y:
    #         row.scale_y = 1.5
    #     row.scale_x = 1.1
    #     sharp = icons.get("icon_sharp")
    #     row.operator("object.sfc_make_solo", text="Solo", icon_value=sharp.icon_id)
    #     row = col.row(align=True)
    #
    #     if bpy.data.materials.get('Transparent_shader'):
    #         row.prop(bpy.data.materials['Transparent_shader'], "diffuse_color", text="")
    #         row.prop(bpy.data.materials['Transparent_shader'], "alpha", text="Alpha")


# --------------------------------------------------------------------------------
# 9 - TOP - RIGHT
# --------------------------------------------------------------------------------
def SFC_OBJMode_Top_Right_Shader(self, context):
    WM = bpy.context.window_manager
    SFC = context.window_manager.SFC
    obj = context.active_object
    layout = self.layout
    pie = layout.menu_pie()
    col = pie.column(align=True)
    row = col.row(align=True)
    row.separator()
    row = col.row(align=True)
    row.separator()
    row = col.row(align=True)
    row.scale_x = 1.3
    if len([obj for obj in context.selected_objects if context.object is not None if
            obj.type in ['MESH', 'CURVE', 'LATTICE']]) >= 1:
        if context.object is not None and obj.type == 'MESH':
            lattice = False
            for mod in obj.modifiers:
                if mod.type == "LATTICE":
                    lattice = True
            if not lattice:
                if self.scale_y:
                    row.scale_y = 1.5

                # row.operator("object.sfc_add_lattice", text="Add Lattice", icon='OUTLINER_OB_LATTICE')
                row.operator("sfc.add_lattice", text="Add Lattice", icon='OUTLINER_OB_LATTICE')
                # row.operator("object.sfc_add_lattice_to_selection", text="Add Lattice", icon='OUTLINER_OB_LATTICE')

            else:
                if self.scale_y:
                    row.scale_y = 1.5
                row.operator("object.sfc_edit_objects", text="Edit Lattice", icon='MOD_LATTICE')

        elif len([obj for obj in context.selected_objects]) >= 2:
            if self.scale_y:
                row.scale_y = 1.5
            row.operator("object.sfc_connect_lattice", text="Connect Lattice", icon='MOD_LATTICE')

        elif len([obj for obj in context.selected_objects if obj.type == 'LATTICE']) == 1:
            if self.scale_y:
                row.scale_y = 1.5
            row.operator("object.sfc_edit_lattice", text="Edit Lattice", icon='LATTICE_DATA')
    # WM = bpy.context.window_manager
    # layout = self.layout
    # pie = layout.menu_pie()
    # act_obj = context.active_object
    # icons = load_icons()
    #
    # split = pie.split()
    # col = split.column(align=True)
    #
    # row = col.row(align=True)
    # red = icons.get("red")
    # row.operator("object.sfc_material_dif_colors", text="", icon_value=red.icon_id).material_dif_colors = "red"
    # orange = icons.get("orange")
    # row.operator("object.sfc_material_dif_colors", text="", icon_value=orange.icon_id).material_dif_colors = "orange"
    # yellow = icons.get("yellow")
    # row.operator("object.sfc_material_dif_colors", text="", icon_value=yellow.icon_id).material_dif_colors = "yellow"
    # green = icons.get("green")
    # row.operator("object.sfc_material_dif_colors", text="", icon_value=green.icon_id).material_dif_colors = "green"
    # cian = icons.get("cian")
    # row.operator("object.sfc_material_dif_colors", text="", icon_value=cian.icon_id).material_dif_colors = "cian"
    # blue = icons.get("blue")
    # row.operator("object.sfc_material_dif_colors", text="", icon_value=blue.icon_id).material_dif_colors = "blue"
    # purple = icons.get("purple")
    # row.operator("object.sfc_material_dif_colors", text="", icon_value=purple.icon_id).material_dif_colors = "purple"
    # pink = icons.get("pink")
    # row.operator("object.sfc_material_dif_colors", text="", icon_value=pink.icon_id).material_dif_colors = "pink"
    #
    # row = col.row(align=True)
    # nb_1 = icons.get("nb_1")
    # row.operator("object.sfc_material_dif_colors", text="",
    #              icon_value=nb_1.icon_id).material_dif_colors = "nb_1"
    # nb_2 = icons.get("nb_2")
    # row.operator("object.sfc_material_dif_colors", text="",
    #              icon_value=nb_2.icon_id).material_dif_colors = "nb_2"
    # nb_3 = icons.get("nb_3")
    # row.operator("object.sfc_material_dif_colors", text="",
    #              icon_value=nb_3.icon_id).material_dif_colors = "nb_3"
    # nb_4 = icons.get("nb_4")
    # row.operator("object.sfc_material_dif_colors", text="",
    #              icon_value=nb_4.icon_id).material_dif_colors = "nb_4"
    # nb_5 = icons.get("nb_5")
    # row.operator("object.sfc_material_dif_colors", text="",
    #              icon_value=nb_5.icon_id).material_dif_colors = "nb_5"
    # nb_6 = icons.get("nb_6")
    # row.operator("object.sfc_material_dif_colors", text="",
    #              icon_value=nb_6.icon_id).material_dif_colors = "nb_6"
    # nb_7 = icons.get("nb_7")
    # row.operator("object.sfc_material_dif_colors", text="",
    #              icon_value=nb_7.icon_id).material_dif_colors = "nb_7"
    # nb_8 = icons.get("nb_8")
    # row.operator("object.sfc_material_dif_colors", text="",
    #              icon_value=nb_8.icon_id).material_dif_colors = "nb_8"
    # if act_obj.active_material:
    #     row = col.row(align=True)
    #     row.prop(WM, "material_color", text="")
    #
    #     # if act_obj.show_transparent:
    #     # row = col.row(align=True)
    #     row.prop(WM, "material_alpha", text="Alpha")
    #     # row.prop(bpy.data.materials[act_obj.active_material.name], "alpha", text="Alpha")
    #
    # row = col.row(align=True)
    # if self.scale_y:
    #     row.scale_y = 1.5
    # # row.scale_x = 0.8
    # row.operator("object.sfc_random_color", text="Add Material", icon='COLOR')
    # if self.scale_y:
    #     row.scale_y = 1.5
    # # row.scale_x = 1.2
    # row.operator("object.random_color_popup", text="", icon='MODIFIER')
    #
    # if len(bpy.data.materials):
    #     # row = col.row(align=True)
    #       if self.scale_y:
    #     #     row.scale_y = 1.5
    #     # row.scale_x = 0.8
    #     row.operator("object.sfc_material_list_menu", text="", icon='MATERIAL_DATA')
    #     # row.scale_x = 1.2
    #     row.operator("object.sfc_clean_unused_data", text="", icon='GHOST_DISABLED')


# --------------------------------------------------------------------------------
# 1 - BOTTOM - LEFT
# --------------------------------------------------------------------------------
def SFC_OBJMode_Bottom_Left_Carver(self, context):
    layout = self.layout
    pie = layout.menu_pie()
    pie.separator()

    # icons = load_icons()
    # layout = self.layout
    # pie = layout.menu_pie()
    # box = pie.split().column()
    # row = box.split(align=True)
    # if hasattr(bpy.types, "OBJECT_OT_carver"):
    #     if self.scale_y:
    #         row.scale_y = 1.5
    #     row.scale_x = 1.5
    #     carver = icons.get("icon_carver")
    #     row.operator("object.carver", text="Carver", icon_value=carver.icon_id)
    # else:
    #     row = box.split(align=True)
    #     if self.scale_y:
    #         row.scale_y = 1.5
    #     row.scale_x = 1.7
    #     row.operator("object.activate_carver", text="Activate Carver", icon='ERROR')

    # icons = load_icons()
    # layout = self.layout
    # pie = layout.menu_pie()
    # box = pie.split().column()
    # row = box.split(align=True)
    # if hasattr(bpy.types, "CLASS_OT_autocompleteone"):
    #     if self.scale_y:
    #         row.scale_y = 1.5
    #     row.scale_x = 1.5
    #     fluent = icons.get("icon_fluent")
    #     # row.operator("wm.call_menu_pie", text="fluent", icon_value=fluent.icon_id).name = "menu.fluent"
    #     row.operator("wm.call_menu_pie", text="fluent", icon_value=fluent.icon_id).name = "FLUENT_MT_pie_menu"


# --------------------------------------------------------------------------------
# 3 - BOTTOM - RIGHT
# --------------------------------------------------------------------------------
def SFC_OBJMode_Bottom_Right(self, context):
    icons = load_icons()
    layout = self.layout
    pie = layout.menu_pie()
    col = pie.column(align=True)
    # row = col.row(align=True)
    # if self.scale_y:
    #     row.scale_y = 1.5
    # row.scale_x = 1.5
    # project = icons.get("icon_project")
    # row.operator("object.sfc_project_modal", text='Project', icon_value=project.icon_id)

    row = col.row(align=True)
    if self.scale_y:
        row.scale_y = 1.5
    # row.scale_x = 1.5
    # faces = icons.get("icon_faces")
    # row.operator("object.sfc_clean_mesh", text="Clean Meshes", icon_value=faces.icon_id)
    modifiers = icons.get("icon_modifiers")
    row.menu("SFC_MT_tools_menu", text='Companion Tools', icon_value=modifiers.icon_id)


class SFC_MT_tools_menu(bpy.types.Menu):
    bl_label = "Sc Tools Menu"

    def draw(self, context):
        layout = self.layout
        icons = load_icons()

        split = layout.split()
        col = split.column(align=True)
        project = icons.get("icon_project")
        col.operator("object.sfc_project_modal", text='Project', icon_value=project.icon_id)
        faces = icons.get("icon_faces")
        col.operator("object.sfc_clean_mesh", text="Clean Meshes", icon_value=faces.icon_id)
        intersection = icons.get("icon_intersection")
        col.operator("object.sc_fast_intersect", text='Fast Intersect', icon_value=intersection.icon_id)
        replace = icons.get("icon_replace")
        col.operator("object.sc_replace_mesh_data", text='Replace Mesh Data', icon_value=replace.icon_id)
        parent = icons.get("icon_parent")
        col.operator("object.sc_parent_asset", text='Parent Assets', icon_value=parent.icon_id)
        rename = icons.get("icon_rename")
        col.operator("object.sc_fast_rename", text='Fast Rename', icon_value=rename.icon_id)


# Menu
class SFC_MT_pie_menu(Menu):
    bl_label = "Speedflow Companion"

    def draw(self, context):
        self.drawText = get_addon_preferences().drawText
        self.use_normals_buttons = get_addon_preferences().use_normals_buttons
        self.scale_y = get_addon_preferences().scale_y
        addon_pref = get_addon_preferences()
        obj = context.active_object
        WM = bpy.context.window_manager
        layout = self.layout
        pie = layout.menu_pie()
        SFC = context.window_manager.SFC

        if bpy.context.object is not None:
            mesh = context.active_object.data

        icons = load_icons()

# =================================================================#
#  No Object Mode
# =================================================================#
        if bpy.context.area.type == 'VIEW_3D' and not bpy.context.object:

            #4 - LEFT
            if not context.selected_objects:
                col = pie.column(align=True)
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 1.3
                row.prop(context.scene.render, "use_simplify", text="Simplify")
                # row.operator("SFC_PT_simplify_popup", text="", icon='MODIFIER')
                row.operator("sfc.simplify_popup", text="", icon='MODIFIER')

            #6 - RIGHT
            pie.separator()

            #2 - BOTTOM
            SFC_Primitives(self, context)

            #8 - TOP
            pie.separator()

            #7 - TOP - LEFT
            pie.separator()

            #9 - TOP - RIGHT
            pie.separator()

            #1 - BOTTOM - LEFT
            SFC_OBJMode_Bottom_Left_Carver(self, context)

            #3 - BOTTOM - RIGHT
            pie.separator()

#=================================================================#
#  Object Mode
#=================================================================#
        # if bpy.context.area.type == 'VIEW_3D' and context.object is not None and bpy.context.object.mode == 'OBJECT' and bpy.context.object.type in ['MESH', 'LATTICE', 'EMPTY','FONT','ARMATURE'] :
        if bpy.context.area.type == 'VIEW_3D' and context.object is not None and bpy.context.object.mode == 'OBJECT':
            #4 - LEFT
            if not context.selected_objects:
                col = pie.column(align=True)
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 1.3
                row.prop(context.scene.render, "use_simplify", text="Simplify")
                # row.operator("SFC_PT_simplify_popup", text="", icon='MODIFIER')
                row.operator("sfc.simplify_popup", text="", icon='MODIFIER')
            else:
                SFC_OBJMode_Modifiers(self, context)

            #6 - RIGHT
            SFC_OBJMode_Right(self, context)

            #2 - BOTTOM
            SFC_OBJMode_Bottom(self, context)

            #8 - TOP
            SFC_OBJMode_Top(self, context)

            #7 - TOP - LEFT
            SFC_OBJMode_Top_Left(self, context)

            #9 - TOP - RIGHT
            SFC_OBJMode_Top_Right_Shader(self, context)

            #1 - BOTTOM - LEFT
            SFC_OBJMode_Bottom_Left_Carver(self, context)

            #3 - BOTTOM - RIGHT
            SFC_OBJMode_Bottom_Right(self, context)

# =================================================================#
#  SCULPT Mode
# =================================================================#
        if bpy.context.area.type == 'VIEW_3D' and context.object is not None and bpy.context.object.mode == 'SCULPT' and bpy.context.object.type == 'MESH':
            # 4 - LEFT
            SFC_OBJMode_Modifiers(self, context)

            # 6 - RIGHT
            pie.separator()

            # 2 - BOTTOM
            SFC_OBJMode_Bottom(self, context)

            # 8 - TOP
            pie.separator()
            # SFC_OBJMode_Top(self, context)

            # 7 - TOP - LEFT
            SFC_OBJMode_Top_Left(self, context)

            # 9 - TOP - RIGHT
            SFC_OBJMode_Top_Right_Shader(self, context)

            # 1 - BOTTOM - LEFT
            SFC_OBJMode_Bottom_Left_Carver(self, context)
            # pie.separator()

            # 3 - BOTTOM - RIGHT
            pie.separator()

# ------------------------------------------------------------------------------------
# CURVE
# ------------------------------------------------------------------------------------

        elif context.object is not None and bpy.context.area.type == 'VIEW_3D' and bpy.context.object.mode == 'OBJECT' and bpy.context.object.type == 'CURVE':
            # 4 - LEFT
            SFC_OBJMode_Modifiers(self, context)

            # 6 - RIGHT
            pie.separator()

            # 2 - BOTTOM
            SFC_OBJMode_Bottom(self, context)
            # SFC_Primitives(self, context)

            # 8 - TOP
            pie.separator()

            # 7 - TOP - LEFT
            SFC_OBJMode_Top_Left(self, context)

            # 9 - TOP - RIGHT
            SFC_OBJMode_Top_Right_Shader(self, context)

            # 1 - BOTTOM - LEFT
            SFC_OBJMode_Bottom_Left_Carver(self, context)

            # 3 - BOTTOM - RIGHT
            pie.separator()

# ------------------------------------------------------------------------------------
# Empty Image
# ------------------------------------------------------------------------------------
        elif bpy.context.object is not None and bpy.context.area.type == 'VIEW_3D' and bpy.context.object.mode == 'OBJECT' and bpy.context.object.type == 'EMPTY_IMAGE':
            # 4 - LEFT
            pie.separator()

            # 6 - RIGHT
            pie.separator()

            # 2 - BOTTOM
            SFC_OBJMode_Bottom(self, context)

            # 8 - TOP
            pie.separator()

            # 7 - TOP - LEFT
            pie.separator()

            # 9 - TOP - RIGHT
            SFC_OBJMode_Top_Right_Shader(self, context)

            # 1 - BOTTOM - LEFT

            SFC_OBJMode_Bottom_Left_Carver(self, context)

            # 3 - BOTTOM - RIGHT
            pie.separator()


#=================================================================#
# Edit Mode
#=================================================================#

        elif context.object is not None and bpy.context.area.type == 'VIEW_3D' and bpy.context.object.mode == 'EDIT':

            #            if bpy.context.object.type in ['MESH', 'LATTICE'] :
            if bpy.context.object.type == 'MESH':
                #4 - LEFT
                col = pie.column(align=True)
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 1.4
                modifiers = icons.get("icon_modifiers")
                row.operator("object.apply_remove_hide_modifiers", text="Modifiers", icon_value=modifiers.icon_id)

                if self.use_normals_buttons:
                    if obj.modifiers:
                        row.operator("object.sfc_hide_modifiers", text='', icon='RESTRICT_VIEW_OFF')
                        row.operator("object.sfc_apply_modifiers", text='', icon='FILE_TICK')
                        row.operator("object.sfc_remove_modifiers", text='', icon='X')

                #6 - RIGHT
                col = pie.column(align=True)
                row = col.row(align=True)
                bevel = icons.get("icon_bevel_1")
                row.operator("object.sfc_bevel_weight", text="Bevel Weight", icon_value=bevel.icon_id)
                if self.use_normals_buttons:
                    row.operator("transform.edge_bevelweight", text="", icon='X').value = -1

                #2 - BOTTOM
                col = pie.column(align=True)
                row = col.row(align=True)
                row.separator()
                row = col.row(align=True)
                row.separator()
                row = col.row(align=True)
                row.separator()

                SFC_prim = context.window_manager.SFC_prim

                row = col.row(align=True)
                row.prop(SFC_prim, "align_cursor_rot", text="Cursor Rot")
                row.prop(SFC_prim, "add_mirror", text="Mirror")
                if SFC_prim.add_mirror:
                    row = col.row(align=True)
                    row.prop(SFC_prim, "mirror_axis_xyz", expand=True)

                if SFC_prim.add_boolean == False:
                    SFC_prim.add_rebool = False

                row = col.row(align=True)
                row.prop(SFC_prim, "add_boolean", text="Boolean")
                if SFC_prim.add_boolean:
                    row.prop(SFC_prim, "add_rebool", text="Rebool")

                if SFC_prim.add_boolean or SFC_prim.add_rebool:
                    row = col.row(align=True)
                    if SFC_prim.add_rebool:
                        SFC_prim.boolean_enum = 'DIFFERENCE'
                    row.prop(SFC_prim, "boolean_enum", expand=True)
                row = col.row(align=True)
                row.operator("sfc.primitives_popup", text="Popup Settings", icon='MODIFIER')

                # -------DEFAULT PRIMITIVES

                col.label(text="Default Primitives", icon='MESH_CUBE')
                row = col.row(align=True)
                # row.scale_x = 1.2
                op = row.operator("sfc.primitives_new", text="", icon='DOT')
                op.primitives_enum = "default_prim"
                op.default_enum = 'vertex'

                op = row.operator("sfc.primitives_new", text="", icon='MESH_PLANE')
                op.primitives_enum = "default_prim"
                op.default_enum = 'plane'

                op = row.operator("sfc.primitives_new", text="", icon='MESH_CUBE')
                op.primitives_enum = "default_prim"
                op.default_enum = 'cube'

                op = row.operator("sfc.primitives_new", text="", icon='MESH_CIRCLE')
                op.primitives_enum = "default_prim"
                op.default_enum = 'circle'

                op = row.operator("sfc.primitives_new", text="", icon='MESH_UVSPHERE')
                op.primitives_enum = "default_prim"
                op.default_enum = 'uv_sphere'

                op = row.operator("sfc.primitives_new", text="", icon='MESH_ICOSPHERE')
                op.primitives_enum = "default_prim"
                op.default_enum = 'ico_sphere'

                op = row.operator("sfc.primitives_new", text="", icon='MESH_CYLINDER')
                op.primitives_enum = "default_prim"
                op.default_enum = 'cylinder'

                op = row.operator("sfc.primitives_new", text="", icon='MESH_CONE')
                op.primitives_enum = "default_prim"
                op.default_enum = 'cone'

                op = row.operator("sfc.primitives_new", text="", icon='MESH_TORUS')
                op.primitives_enum = "default_prim"
                op.default_enum = 'torus'

                row = col.row(align=True)
                # row.scale_x = 1

                op = row.operator("sfc.primitives_new", text="", icon='MESH_GRID')
                op.primitives_enum = "default_prim"
                op.default_enum = 'grid'

                op = row.operator("sfc.primitives_new", text="", icon='CURVE_BEZCURVE')
                op.primitives_enum = "default_prim"
                op.default_enum = 'bezier_curve'

                op = row.operator("sfc.primitives_new", text="", icon='CURVE_BEZCIRCLE')
                op.primitives_enum = "default_prim"
                op.default_enum = 'bezier_circle'

                row.operator("sfc.cursor_line", text="", icon='LINE_DATA')

                op = row.operator("sfc.primitives_new", text="", icon='MESH_MONKEY')
                op.primitives_enum = "default_prim"
                op.default_enum = 'monkey'

                # -------SCREW PRIMITIVES
                col.label(text="Screw Primitives", icon='MOD_SCREW')
                row = col.row(align=True)
                # row.scale_x = 1.3
                op = row.operator("sfc.primitives_new", text="", icon='DOT')
                op.primitives_enum = "screw_prim"
                op.screw_enum = 'screw_7'

                op = row.operator("sfc.primitives_new", text="", icon='MESH_CIRCLE')
                op.primitives_enum = "screw_prim"
                op.screw_enum = 'screw_6'

                op = row.operator("sfc.primitives_new", text="", icon='MESH_CYLINDER')
                op.primitives_enum = "screw_prim"
                op.screw_enum = 'screw_1'

                screw = icons.get("prim_screw_2")
                op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
                op.primitives_enum = "screw_prim"
                op.screw_enum = 'screw_2'

                screw = icons.get("prim_screw_3")
                op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
                op.primitives_enum = "screw_prim"
                op.screw_enum = 'screw_3'

                screw = icons.get("prim_screw_4")
                op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
                op.primitives_enum = "screw_prim"
                op.screw_enum = 'screw_4'

                screw = icons.get("prim_screw_5")
                op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
                op.primitives_enum = "screw_prim"
                op.screw_enum = 'screw_5'

                # -------EDITABLE PRIMITIVES
                col.label(text="Editable Primitives", icon='MODIFIER')
                row = col.row(align=True)
                # row.scale_x = 1.3
                op = row.operator("sfc.primitives_new", icon='MESH_CUBE', text="")
                op.primitives_enum = "editable_prim"
                op.editable_enum = 'cube'

                op = row.operator("sfc.primitives_new", icon='MESH_UVSPHERE', text="")
                op.primitives_enum = "editable_prim"
                op.editable_enum = 'sphere'

                op = row.operator("sfc.primitives_new", icon='MESH_CYLINDER', text="")
                op.primitives_enum = "editable_prim"
                op.editable_enum = 'cylinder'

                op = row.operator("sfc.primitives_new", icon='MESH_CONE', text="")
                op.primitives_enum = "editable_prim"
                op.editable_enum = 'cone'

                op = row.operator("sfc.primitives_new", icon='MESH_TORUS', text="")
                op.primitives_enum = "editable_prim"
                op.editable_enum = 'torus'

                op = row.operator("sfc.primitives_new", icon='MESH_GRID', text="")
                op.primitives_enum = "editable_prim"
                op.editable_enum = 'grid'

                op = row.operator("sfc.primitives_new", icon='MESH_CAPSULE', text="")
                op.primitives_enum = "editable_prim"
                op.editable_enum = 'capsule'

                op = row.operator("sfc.primitives_new", icon='MATSPHERE', text="")
                op.primitives_enum = "editable_prim"
                op.editable_enum = 'quad_sphere'

                op = row.operator("sfc.primitives_new", icon='MESH_CIRCLE', text="")
                op.primitives_enum = "editable_prim"
                op.editable_enum = 'circle'

                # -------CUSTOM PRIMITIVES
                col.label(text="Custom Primitives", icon='META_CAPSULE')
                row = col.row(align=True)

                # row.scale_x = 1.3
                op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
                op.primitives_enum = "custom_prim"
                op.custom_enum = 'rounded_cube'

                op = row.operator("sfc.primitives_new", icon='META_PLANE', text="")
                op.primitives_enum = "custom_prim"
                op.custom_enum = 'rounded_plane'

                op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
                op.primitives_enum = "custom_prim"
                op.custom_enum = 'rounded_plane_round'

                op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
                op.primitives_enum = "custom_prim"
                op.custom_enum = 'rounded_plane_2'

                custom = icons.get("prim_cross")
                op = row.operator("sfc.primitives_new", icon_value=custom.icon_id, text="")
                op.custom_enum = 'cross'

                custom = icons.get("prim_cross_rounded")
                op = row.operator("sfc.primitives_new", icon_value=custom.icon_id, text="")
                op.custom_enum = 'rounded_cross'

                op = row.operator("sfc.primitives_new", icon='MESH_CAPSULE', text="")
                op.primitives_enum = "custom_prim"
                op.custom_enum = 'long_cylinder'

                op = row.operator("sfc.primitives_new", icon='IPO_CONSTANT', text="")
                op.primitives_enum = "editable_prim"
                op.editable_enum = 'line'

                op = row.operator("sfc.primitives_new", icon='ANTIALIASED', text="")
                op.primitives_enum = "editable_prim"
                op.editable_enum = 'tube'

                # -------TOOLS
                col.label(text="Tools", icon='TOOL_SETTINGS')
                col.operator("sfc.cursor_tools", text="Copy Cursor Rotation",
                             icon='PIVOT_CURSOR').cursor_tools = 'copy_cursor_rot'
                col.operator("sfc.cursor_tools", text="Selection To Cursor",
                             icon='PIVOT_BOUNDBOX').cursor_tools = 'selection_to_cursor'
                col.operator("sfc.cursor_tools", text="Cursor To Selection + Rotation",
                             icon='PIVOT_CURSOR').cursor_tools = 'cursor_to_selection_rot'
                col.operator("sfc.cursor_tools", text="Align View To Cursor Rotation",
                             icon='VIEW_PERSPECTIVE').cursor_tools = 'align_view_to_cursor_rot'
                col.operator("sfc.cursor_tools", text="Align Cursor To Object Rotation",
                             icon='EMPTY_AXIS').cursor_tools = 'align_cursor_to_object_rot'

                #8 - TOP
                # pie.separator()
                col = pie.column(align=True)
                row = col.row(align=True)
                if hasattr(bpy.types, "MESH_OT_snap_utilities_line"):
                    if self.scale_y:
                        row.scale_y = 1.5
                    row.scale_x = 1.7
                    line = icons.get("icon_line")
                    row.operator("mesh.snap_utilities_line", text="Line", icon_value=line.icon_id)
                else:
                    if self.scale_y:
                        row.scale_y = 1.5
                    row.scale_x = 1.5
                    row.operator("object.sfc_activate_line", text="Line", icon='ERROR')
                    row.operator(
                        "wm.url_open", text="", icon='URL').url = "https://blenderartists.org/forum/showthread.php?363859-Addon-CAD-Snap-Utilities"

                #7 - TOP - LEFT
                col = pie.column(align=True)
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 1.1
                if bpy.context.object.type == 'MESH':
                    if context.object.data.use_auto_smooth == True:
                        autosmooth = icons.get("icon_autosmooth")
                        row.operator("object.sfc_toggle_smooth", text="AutoSmooth", icon_value=autosmooth.icon_id)
                        row = col.row(align=True)
                        row.prop(mesh, "auto_smooth_angle", text="Angle")
                    else:
                        autosmooth_off = icons.get("icon_autosmooth_off")
                        row.operator("object.sfc_toggle_smooth", text="AutoSmooth", icon_value=autosmooth_off.icon_id)

                if self.use_normals_buttons:
                    row = col.row(align=True)
                    if self.scale_y:
                        row.scale_y = 1.5
                    row.scale_x = 1.1
                    wire = icons.get("icon_wire")
                    row.operator("object.sfc_wire_mode", text="Wire", icon_value=wire.icon_id)
                    solid = icons.get("icon_solid")
                    row.operator("object.sfc_solid_mode", text="Solid", icon_value=solid.icon_id)
                    bounds = icons.get("icon_bounds")
                    row.operator("object.sfc_bounds_mode", text="Bound", icon_value=bounds.icon_id)
                else:
                    row = col.row(align=True)
                    if self.scale_y:
                        row.scale_y = 1.5
                    row.scale_x = 1.1
                    wire = icons.get("icon_wire")
                    row.operator("object.sfc_display_mode", text="Display Mode", icon_value=wire.icon_id)

                # draw_text = icons.get("draw_text")
                # row.prop(addon_pref, "drawText", text="", icon_value=draw_text.icon_id)

                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 1.1
                subsurf = icons.get("icon_subsurf")
                row.operator("object.sfc_subdiv_booleans_prepare", text="Subdiv Booleans", icon_value=subsurf.icon_id)
                if self.use_normals_buttons:
                    row.operator("object.clean_subdiv_booleans", text="", icon='X')
                # row=col.row(align=True)
                # if self.scale_y:
                #     row.scale_y = 1.5
                # row.scale_x = 1.3
                # mirror = icons.get("icon_mirror")
                # row.operator("object.sfc_auto_mirror", text = "Automirror", icon_value=mirror.icon_id)
                # if self.use_normals_buttons:
                #     if obj.modifiers:
                #         if "Mirror" in obj.modifiers:
                #             row.operator("object.sfc_hide_mirror_modifier", text="", icon="RESTRICT_VIEW_OFF")
                #             row.operator("object.sfc_apply_mirror_modifiers", text="", icon="FILE_TICK")
                #             row.operator("object.remove_bevel", text="", icon='X')

                #9 - TOP - RIGHT
                layout = self.layout
                pie = layout.menu_pie()
                col = pie.column(align=True)
                # pie.separator()
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.2
                row.scale_x = 0.9
                if self.use_normals_buttons:
                    row.operator("object.sfc_show_hide_sharps", text="Show Sharps")
                    row.operator("object.sfc_hide_sharps", text="Hide Sharps")
                else:
                    row.operator("object.sfc_show_hide_sharps", text="Show/Hide Sharps")

                # SFC_OBJMode_Bottom(self, context)
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.2
                row.scale_x = 0.9

                mesh = context.space_data.overlay

                row.prop(mesh, "show_edge_bevel_weight", text="B")
                row.prop(mesh, "show_edge_sharp", text="S")
                row.prop(mesh, "show_edge_crease", text="C")
                row.prop(mesh, "show_edge_seams", text="S")

                row = col.row(align=True)
                row.separator()
                row = col.row(align=True)
                # row.separator()
                # row = col.row(align=True)
                if len([obj for obj in context.selected_objects if context.object is not None if
                        obj.type == 'MESH']) >= 1:
                    if context.object is not None and obj.type == 'MESH':
                        lattice = False
                        for mod in obj.modifiers:
                            if mod.type == "LATTICE":
                                lattice = True
                        if not lattice:
                            if self.scale_y:
                                row.scale_y = 1.2
                            row.scale_x = 1.2
                            row.operator("sfc.add_lattice", text="Add Lattice", icon='OUTLINER_OB_LATTICE')
                            # row.operator("object.sfc_add_lattice_to_selection", text="Add Lattice",
                            #              icon='OUTLINER_OB_LATTICE')
                        else:
                            if self.scale_y:
                                row.scale_y = 1.2
                            row.scale_x = 1.2
                            row.operator("object.sfc_edit_objects", text="Edit Lattice", icon='LATTICE_DATA')

                    elif len([obj for obj in context.selected_objects]) >= 2:
                        if self.scale_y:
                            row.scale_y = 1.2
                        row.scale_x = 1.2
                        row.operator("object.sfc_connect_lattice", text="Connect Lattice", icon='MOD_LATTICE')

                    elif len([obj for obj in context.selected_objects if obj.type == 'LATTICE']) == 1:
                        if self.scale_y:
                            row.scale_y = 1.2
                        row.scale_x = 1.2
                        row.operator("object.sfc_edit_lattice", text="Edit Lattice", icon='LATTICE_DATA')

                # split = pie.split()
                # col = split.column(align=True)
                # row = col.row(align=True)
                # red = icons.get("red")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=red.icon_id).material_dif_colors = "red"
                # orange = icons.get("orange")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=orange.icon_id).material_dif_colors = "orange"
                # yellow = icons.get("yellow")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=yellow.icon_id).material_dif_colors = "yellow"
                # green = icons.get("green")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=green.icon_id).material_dif_colors = "green"
                # cian = icons.get("cian")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=cian.icon_id).material_dif_colors = "cian"
                # blue = icons.get("blue")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=blue.icon_id).material_dif_colors = "blue"
                # purple = icons.get("purple")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=purple.icon_id).material_dif_colors = "purple"
                # pink = icons.get("pink")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=pink.icon_id).material_dif_colors = "pink"
                #
                # row = col.row(align=True)
                # nb_1 = icons.get("nb_1")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=nb_1.icon_id).material_dif_colors = "nb_1"
                # nb_2 = icons.get("nb_2")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=nb_2.icon_id).material_dif_colors = "nb_2"
                # nb_3 = icons.get("nb_3")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=nb_3.icon_id).material_dif_colors = "nb_3"
                # nb_4 = icons.get("nb_4")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=nb_4.icon_id).material_dif_colors = "nb_4"
                # nb_5 = icons.get("nb_5")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=nb_5.icon_id).material_dif_colors = "nb_5"
                # nb_6 = icons.get("nb_6")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=nb_6.icon_id).material_dif_colors = "nb_6"
                # nb_7 = icons.get("nb_7")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=nb_7.icon_id).material_dif_colors = "nb_7"
                # nb_8 = icons.get("nb_8")
                # row.operator("object.sfc_material_dif_colors", text="",
                #              icon_value=nb_8.icon_id).material_dif_colors = "nb_8"
                #
                # if obj.active_material:
                #     row = col.row(align=True)
                #     row.prop(WM, "material_color", text="")
                #
                #     # if act_obj.show_transparent:
                #     # row = col.row(align=True)
                #     row.prop(WM, "material_alpha", text="Alpha")
                #     # row.prop(bpy.data.materials[act_obj.active_material.name], "alpha", text="Alpha")
                #
                # row = col.row(align=True)
                # if self.scale_y:
                #     row.scale_y = 1.5
                # # row.scale_x = 0.8
                # row.operator("object.sfc_random_color", text="Add Material", icon='COLOR')
                # if self.scale_y:
                #     row.scale_y = 1.5
                # # row.scale_x = 1.2
                # row.operator("object.random_color_popup", text="", icon='MODIFIER')
                #
                # if len(bpy.data.materials):
                #     # row = col.row(align=True)
                #       if self.scale_y:
                #     #     row.scale_y = 1.5
                #     # row.scale_x = 0.8
                #     row.operator("object.sfc_material_list_menu", text="", icon='MATERIAL_DATA')
                #     # row.scale_x = 1.2
                #     row.operator("object.sfc_clean_unused_data", text="", icon='GHOST_DISABLED')
                #
                # # col = pie.column(align=True)
                # # row=col.row(align=True)
                # # if self.scale_y:
                # #     row.scale_y = 1.5
                # # row.scale_x = 1.5
                # # crease = icons.get("icon_crease")
                # # row.operator("object.sfc_creases", text = "Creases", icon_value=crease.icon_id)
                # # if self.use_normals_buttons:
                # #     row.operator("transform.edge_crease", text='',icon='X').value=-1
                # # row = col.row(align=True)
                # # if self.scale_y:
                # #     row.scale_y = 1.5
                # # row.scale_x = 1.5
                # # sharps = icons.get("icon_sharp")
                # # row.operator("object.sfc_sharps", text="Sharps", icon_value=sharps.icon_id)
                # # if self.use_normals_buttons:
                # #     row.operator("object.sfc_unsharps", text="", icon='X')

                #1 - BOTTOM - LEFT
                col = pie.column(align=True)
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.2
                row.scale_x = 1.2
                ngons = icons.get("icon_ngons")
                row.operator("object.sfc_facetype_select", text="Select Ngons", icon_value=ngons.icon_id)
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.2
                row.scale_x = 1.2
                faces = icons.get("icon_faces")
                row.operator("object.sfc_clean_faces", text="Clean Faces", icon_value=faces.icon_id)
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.2
                row.scale_x = 1.2
                laprelax = icons.get("icon_laprelax")
                row.operator("mesh.sfc_laprelax", text="Lap Relax", icon_value=laprelax.icon_id)
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.2
                row.scale_x = 1.2
                faces = icons.get("icon_faces")
                row.operator("object.sc_parent_asset", text='Parent Assets', icon_value=faces.icon_id)

                #3 - BOTTOM - RIGHT
                col = pie.column(align=True)
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.2
                row.scale_x = 1.2
                crease = icons.get("icon_crease")
                row.operator("object.sfc_creases", text="Creases", icon_value=crease.icon_id)
                if self.use_normals_buttons:
                    row.operator("transform.edge_crease", text='', icon='X').value = -1
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.2
                row.scale_x = 1.2
                sharps = icons.get("icon_sharp")
                row.operator("object.sfc_sharps", text="Sharps", icon_value=sharps.icon_id)
                if self.use_normals_buttons:
                    row.operator("object.sfc_unsharps", text="", icon='X')

                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.2
                row.scale_x = 1.2
                sharps = icons.get("icon_sharp")
                row.operator("object.sfc_seams", text="Seam", icon_value=sharps.icon_id)
                if self.use_normals_buttons:
                    row.operator("object.sfc_unseam", text="", icon='X')

                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.2
                row.scale_x = 1.2
                sharp = icons.get("icon_sharp")
                row.operator("object.sfc_sharp_all", text="All Sharps", icon_value=sharp.icon_id)
                if self.use_normals_buttons:
                    row.operator("object.sfc_unsharp_all", text="", icon='X')

                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.2
                row.scale_x = 1.2
                vgroup = icons.get("icon_vgroup")
                row.operator("object.sfc_vgroups", text="Vertex Groups", icon_value=vgroup.icon_id)
                # row.operator("SFC_PT_vertex_group", text="", icon='MODIFIER')
                row.operator("sfc.vertex_group", text="", icon='MODIFIER')

            #=================================================================#
            #  Lattice
            #=================================================================#
            elif context.object is not None and bpy.context.object.type == 'LATTICE':

                #4 - LEFT
                pie.separator()
                #6 - RIGHT
                pie.separator()
                #2 - BOTTOM
                col = pie.column(align=True)
                row = col.row(align=True)
                if len([obj for obj in context.selected_objects if context.object is not None if obj.type in ['MESH', 'LATTICE']]) >= 1:
                    if context.object is not None and obj.type == 'MESH':
                        lattice = False
                        for mod in obj.modifiers:
                            if mod.type == "LATTICE":
                                lattice = True
                        if not lattice:
                            if self.scale_y:
                                row.scale_y = 1.5
                            row.operator("sfc.add_lattice", text="Add Lattice", icon='OUTLINER_OB_LATTICE')
                            # row.operator("object.sfc_add_lattice_to_selection", text="Add Lattice",
                            #              icon='OUTLINER_OB_LATTICE')

                        else:
                            if self.scale_y:
                                row.scale_y = 1.5
                            row.operator("object.sfc_edit_objects", text="Edit Lattice", icon='LATTICE_DATA')

                    elif len([obj for obj in context.selected_objects]) >= 2:
                        if self.scale_y:
                            row.scale_y = 1.5
                        row.operator("object.sfc_connect_lattice", text="Connect Lattice", icon='MOD_LATTICE')

                    # elif len([obj for obj in context.selected_objects if obj.type == 'LATTICE' ]) == 1:
                    elif obj.type == 'LATTICE':
                        if self.scale_y:
                            row.scale_y = 1.5
                        row.operator("object.sfc_edit_lattice", text="Edit Lattice", icon='LATTICE_DATA')

                #8 - TOP
                pie.separator()
                #7 - TOP - LEFT
                pie.separator()
                #9 - TOP - RIGHT
                pie.separator()
                #1 - BOTTOM - LEFT
                pie.separator()
                #3 - BOTTOM - RIGHT
                pie.separator()

            #=================================================================#
            #  Curves
            #=================================================================#
            elif context.object is not None and bpy.context.object.type == 'CURVE':

                #4 - LEFT
                box = pie.split().column()
                row = box.split(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 2.2
                poly = icons.get("icon_poly")
                row.operator("curve.spline_type_set", text="Poly", icon_value=poly.icon_id).type = 'POLY'

                #6 - RIGHT
                box = pie.split().column()
                row = box.split(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 2
                bezier = icons.get("icon_bezier")
                row.operator("curve.spline_type_set", text="Bezier", icon_value=bezier.icon_id).type = 'BEZIER'

                #2 - BOTTOM
                curve = context.active_object.data
                col = pie.column(align=True)
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 1.2
                recalc_normals = icons.get("icon_recalc_normals")
                row.operator("curve.normals_make_consistent", text="Recalc Normals", icon_value=recalc_normals.icon_id)
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 1.2
                show_normals = icons.get("icon_show_normals")
                row.prop(curve, "show_normal_face", text="show Normals", icon_value=show_normals.icon_id)

                #8 - TOP
                box = pie.split().column()
                row = box.split(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 2
                radius = icons.get("icon_radius")
                row.operator("curve.radius_set", text="Radius", icon_value=radius.icon_id)
                # row.operator("object.curve_radius", text="Radius", icon_value=radius.icon_id)

                #7 - TOP - LEFT
                col = pie.column(align=True)
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 1.8
                vector = icons.get("icon_vector")
                row.operator("curve.handle_type_set", text="Vector", icon_value=vector.icon_id).type = 'VECTOR'
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 1.8
                free = icons.get("icon_free")
                row.operator("curve.handle_type_set", text="Free", icon_value=free.icon_id).type = 'FREE_ALIGN'

                #9 - TOP - RIGHT
                col = pie.column(align=True)
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 2
                auto = icons.get("icon_auto")
                row.operator("curve.handle_type_set", text="Auto", icon_value=auto.icon_id).type = 'AUTOMATIC'
                row = col.row(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 2
                align = icons.get("icon_align")
                row.operator("curve.handle_type_set", text="Align", icon_value=align.icon_id).type = 'ALIGNED'

                #1 - BOTTOM - LEFT
                box = pie.split().column()
                row = box.split(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 2
                close = icons.get("icon_close")
                row.operator("curve.cyclic_toggle", text="Close", icon_value=close.icon_id)

                #3 - BOTTOM - RIGHT
                box = pie.split().column()
                row = box.split(align=True)
                if self.scale_y:
                    row.scale_y = 1.5
                row.scale_x = 1.2
                switch_direction = icons.get("icon_switch_direction")
                row.operator("curve.switch_direction", icon_value=switch_direction.icon_id)


class SFC_PT_panel(Panel):
    bl_label = "COMPANION"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"

    def draw(self, context):
        SFC_prim = context.window_manager.SFC_prim
        layout = self.layout
        icons = load_icons()

        box = layout.box()
        row = box.row(align=True)
        row.prop(SFC_prim, "align_cursor_rot", text="Cursor Rot")
        row.prop(SFC_prim, "add_mirror", text="Mirror")
        if SFC_prim.add_mirror:
            row = box.row(align=True)
            row.prop(SFC_prim, "mirror_axis_xyz", expand=True)

        if SFC_prim.add_boolean == False:
            SFC_prim.add_rebool = False

        row = box.row(align=True)
        row.prop(SFC_prim, "add_boolean", text="Boolean")
        if SFC_prim.add_boolean:
            row.prop(SFC_prim, "add_rebool", text="Rebool")

        if SFC_prim.add_boolean or SFC_prim.add_rebool:
            row = box.row(align=True)
            if SFC_prim.add_rebool:
                SFC_prim.boolean_enum = 'DIFFERENCE'
            row.prop(SFC_prim, "boolean_enum", expand=True)

        # -------DEFAULT PRIMITIVES

        layout.label(text="Default Primitives", icon='MESH_CUBE')
        row = layout.row(align=True)
        row.scale_x = 1.3
        op = row.operator("sfc.primitives_new", text="", icon='DOT')
        op.primitives_enum = "default_prim"
        op.default_enum = 'vertex'

        op = row.operator("sfc.primitives_new", text="", icon='MESH_PLANE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'plane'

        op = row.operator("sfc.primitives_new", text="", icon='MESH_CUBE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'cube'

        op = row.operator("sfc.primitives_new", text="", icon='MESH_CIRCLE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'circle'

        op = row.operator("sfc.primitives_new", text="", icon='MESH_UVSPHERE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'uv_sphere'

        op = row.operator("sfc.primitives_new", text="", icon='MESH_ICOSPHERE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'ico_sphere'

        op = row.operator("sfc.primitives_new", text="", icon='MESH_CYLINDER')
        op.primitives_enum = "default_prim"
        op.default_enum = 'cylinder'

        op = row.operator("sfc.primitives_new", text="", icon='MESH_CONE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'cone'

        op = row.operator("sfc.primitives_new", text="", icon='MESH_TORUS')
        op.primitives_enum = "default_prim"
        op.default_enum = 'torus'

        row = layout.row(align=True)
        row.scale_x = 2

        op = row.operator("sfc.primitives_new", text="", icon='MESH_GRID')
        op.primitives_enum = "default_prim"
        op.default_enum = 'grid'

        op = row.operator("sfc.primitives_new", text="", icon='CURVE_BEZCURVE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'bezier_curve'

        op = row.operator("sfc.primitives_new", text="", icon='CURVE_BEZCIRCLE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'bezier_circle'

        row.operator("sfc.cursor_line", text="", icon='LINE_DATA')

        op = row.operator("sfc.primitives_new", text="", icon='MESH_MONKEY')
        op.primitives_enum = "default_prim"
        op.default_enum = 'monkey'

        # -------SCREW PRIMITIVES
        layout.label(text="Screw Primitives", icon='MOD_SCREW')
        row = layout.row(align=True)
        row.scale_x = 2
        op = row.operator("sfc.primitives_new", text="", icon='DOT')
        op.primitives_enum = "screw_prim"
        op.screw_enum = 'screw_7'

        op = row.operator("sfc.primitives_new", text="", icon='MESH_CIRCLE')
        op.primitives_enum = "screw_prim"
        op.screw_enum = 'screw_6'

        op = row.operator("sfc.primitives_new", text="", icon='MESH_CYLINDER')
        op.primitives_enum = "screw_prim"
        op.screw_enum = 'screw_1'

        screw = icons.get("prim_screw_2")
        op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
        op.primitives_enum = "screw_prim"
        op.screw_enum = 'screw_2'

        screw = icons.get("prim_screw_3")
        op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
        op.primitives_enum = "screw_prim"
        op.screw_enum = 'screw_3'

        screw = icons.get("prim_screw_4")
        op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
        op.primitives_enum = "screw_prim"
        op.screw_enum = 'screw_4'

        screw = icons.get("prim_screw_5")
        op = row.operator("sfc.primitives_new", text="", icon_value=screw.icon_id)
        op.primitives_enum = "screw_prim"
        op.screw_enum = 'screw_5'

        # -------EDITABLE PRIMITIVES
        layout.label(text="Editable Primitives", icon='MODIFIER')
        row = layout.row(align=True)
        row.scale_x = 1.3
        op = row.operator("sfc.primitives_new", icon='MESH_CUBE', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'cube'

        op = row.operator("sfc.primitives_new", icon='MESH_UVSPHERE', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'sphere'

        op = row.operator("sfc.primitives_new", icon='MESH_CYLINDER', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'cylinder'

        op = row.operator("sfc.primitives_new", icon='MESH_CONE', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'cone'

        op = row.operator("sfc.primitives_new", icon='MESH_TORUS', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'torus'

        op = row.operator("sfc.primitives_new", icon='MESH_GRID', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'grid'

        op = row.operator("sfc.primitives_new", icon='MESH_CAPSULE', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'capsule'

        op = row.operator("sfc.primitives_new", icon='MATSPHERE', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'quad_sphere'

        op = row.operator("sfc.primitives_new", icon='MESH_CIRCLE', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'circle'

        # -------CUSTOM PRIMITIVES
        layout.label(text="Custom Primitives", icon='META_CAPSULE')
        row = layout.row(align=True)

        row.scale_x = 1.3
        op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
        op.primitives_enum = "custom_prim"
        op.custom_enum = 'rounded_cube'

        op = row.operator("sfc.primitives_new", icon='META_PLANE', text="")
        op.primitives_enum = "custom_prim"
        op.custom_enum = 'rounded_plane'

        op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
        op.primitives_enum = "custom_prim"
        op.custom_enum = 'rounded_plane_round'

        op = row.operator("sfc.primitives_new", icon='META_CUBE', text="")
        op.primitives_enum = "custom_prim"
        op.custom_enum = 'rounded_plane_2'

        custom = icons.get("prim_cross")
        op = row.operator("sfc.primitives_new", icon_value=custom.icon_id, text="")
        op.custom_enum = 'cross'

        custom = icons.get("prim_cross_rounded")
        op = row.operator("sfc.primitives_new", icon_value=custom.icon_id, text="")
        op.custom_enum = 'rounded_cross'

        op = row.operator("sfc.primitives_new", icon='MESH_CAPSULE', text="")
        op.primitives_enum = "custom_prim"
        op.custom_enum = 'long_cylinder'

        op = row.operator("sfc.primitives_new", icon='IPO_CONSTANT', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'line'

        op = row.operator("sfc.primitives_new", icon='ANTIALIASED', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'tube'

        # -------TOOLS
        layout.label(text="Tools", icon='TOOL_SETTINGS')

        split = layout.split()
        col = split.column(align=True)
        col.scale_y = 1.5
        col.operator("sfc.cursor_tools", text="Copy Cursor Rotation",
                     icon='PIVOT_CURSOR').cursor_tools = 'copy_cursor_rot'
        col.operator("sfc.cursor_tools", text="Selection To Cursor",
                     icon='PIVOT_BOUNDBOX').cursor_tools = 'selection_to_cursor'
        col.operator("sfc.cursor_tools", text="Cursor To Selection + Rotation",
                     icon='PIVOT_CURSOR').cursor_tools = 'cursor_to_selection_rot'
        col.operator("sfc.cursor_tools", text="Align View To Cursor Rotation",
                     icon='VIEW_PERSPECTIVE').cursor_tools = 'align_view_to_cursor_rot'
        col.operator("sfc.cursor_tools", text="Align Cursor To Object Rotation",
                     icon='EMPTY_AXIS').cursor_tools = 'align_cursor_to_object_rot'


UI_CLASSES = [SFC_PT_simplify_popup,
              SFC_PT_vertex_group,
              SFC_OT_primitives_popup,
              SFC_PT_color_Popup,
              SFC_PT_lattice_popup,
              SFC_PT_show_text_options_popup,
              SFC_MT_tools_menu,
              SFC_PT_panel]

EXTRA_CLASSES = [SFC_MT_pie_menu]


def register():
    for cls in UI_CLASSES:
        try:
            bpy.utils.register_class(cls)
        except:
            print(f"{cls.__name__} already registred")


def unregister():
    for cls in UI_CLASSES + EXTRA_CLASSES:
        if hasattr(bpy.types, cls.__name__):
            bpy.utils.unregister_class(cls)
