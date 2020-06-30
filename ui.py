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
# from .modifiers_popup import *
# from .primitives import *
# from .lattice import *
# from .modals import *
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

# Show Text Options Popup


class INFOTEXT_show_text_options_popup(bpy.types.Operator):
    bl_idname = "object.infotext_text_options_popup"
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

            row = col.row(align=True)
            row.label(text="Object Type & Name")
            row.prop(addon_pref, "show_object_name", text="")

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
            row.prop(addon_pref, "infotext_text_space")

            row = col.row(align=True)
            row.label(text="Text X position")
            row.prop(addon_pref, "infotext_text_pos_x")

            row = col.row(align=True)
            row.label(text="Text Y position")
            row.prop(addon_pref, "infotext_text_pos_y")

            row = col.row(align=True)
            row.label(text="Activate Shadows")
            row.prop(addon_pref, "infotext_text_shadow", text="      ")

            if addon_pref.infotext_text_shadow:

                row = col.row(align=True)
                row.label(text="Color")
                row.prop(addon_pref, "infotext_shadow_color")

                row = col.row(align=True)
                row.label(text="Transparency")
                row.prop(addon_pref, "infotext_shadow_alpha")

                row = col.row(align=True)
                row.label(text="Offset X")
                row.prop(addon_pref, "infotext_offset_shadow_x")

                row = col.row(align=True)
                row.label(text="Offset Y")
                row.prop(addon_pref, "infotext_offset_shadow_y")

        row = col.row(align=True)
        row.operator_context = 'EXEC_AREA'
        row.operator("wm.save_userpref", text="Save", icon='FILE_TICK')
        row.operator("object.reset_prefs", text="Reset", icon='RECOVER_LAST')

    def invoke(self, context, event):
        dpi_value = bpy.context.preferences.view.ui_scale
        coef = dpi_value * (-175) + 425
        return context.window_manager.invoke_props_dialog(self, width=dpi_value * coef, height=100)

    bl_label = "COMPANION"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"

    def draw(self, context):
        INFOTEXT_prim = context.window_manager.INFOTEXT_prim
        layout = self.layout
        icons = load_icons()

        box = layout.box()
        row = box.row(align=True)
        row.prop(INFOTEXT_prim, "align_cursor_rot", text="Cursor Rot")
        row.prop(INFOTEXT_prim, "add_mirror", text="Mirror")
        if INFOTEXT_prim.add_mirror:
            row = box.row(align=True)
            row.prop(INFOTEXT_prim, "mirror_axis_xyz", expand=True)

        if INFOTEXT_prim.add_boolean == False:
            INFOTEXT_prim.add_rebool = False

        row = box.row(align=True)
        row.prop(INFOTEXT_prim, "add_boolean", text="Boolean")
        if INFOTEXT_prim.add_boolean:
            row.prop(INFOTEXT_prim, "add_rebool", text="Rebool")

        if INFOTEXT_prim.add_boolean or INFOTEXT_prim.add_rebool:
            row = box.row(align=True)
            if INFOTEXT_prim.add_rebool:
                INFOTEXT_prim.boolean_enum = 'DIFFERENCE'
            row.prop(INFOTEXT_prim, "boolean_enum", expand=True)

        # -------DEFAULT PRIMITIVES

        layout.label(text="Default Primitives", icon='MESH_CUBE')
        row = layout.row(align=True)
        row.scale_x = 1.3
        op = row.operator("infotext.primitives_new", text="", icon='DOT')
        op.primitives_enum = "default_prim"
        op.default_enum = 'vertex'

        op = row.operator("infotext.primitives_new", text="", icon='MESH_PLANE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'plane'

        op = row.operator("infotext.primitives_new", text="", icon='MESH_CUBE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'cube'

        op = row.operator("infotext.primitives_new", text="", icon='MESH_CIRCLE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'circle'

        op = row.operator("infotext.primitives_new", text="", icon='MESH_UVSPHERE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'uv_sphere'

        op = row.operator("infotext.primitives_new", text="", icon='MESH_ICOSPHERE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'ico_sphere'

        op = row.operator("infotext.primitives_new", text="", icon='MESH_CYLINDER')
        op.primitives_enum = "default_prim"
        op.default_enum = 'cylinder'

        op = row.operator("infotext.primitives_new", text="", icon='MESH_CONE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'cone'

        op = row.operator("infotext.primitives_new", text="", icon='MESH_TORUS')
        op.primitives_enum = "default_prim"
        op.default_enum = 'torus'

        row = layout.row(align=True)
        row.scale_x = 2

        op = row.operator("infotext.primitives_new", text="", icon='MESH_GRID')
        op.primitives_enum = "default_prim"
        op.default_enum = 'grid'

        op = row.operator("infotext.primitives_new", text="", icon='CURVE_BEZCURVE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'bezier_curve'

        op = row.operator("infotext.primitives_new", text="", icon='CURVE_BEZCIRCLE')
        op.primitives_enum = "default_prim"
        op.default_enum = 'bezier_circle'

        row.operator("infotext.cursor_line", text="", icon='LINE_DATA')

        op = row.operator("infotext.primitives_new", text="", icon='MESH_MONKEY')
        op.primitives_enum = "default_prim"
        op.default_enum = 'monkey'

        # -------SCREW PRIMITIVES
        layout.label(text="Screw Primitives", icon='MOD_SCREW')
        row = layout.row(align=True)
        row.scale_x = 2
        op = row.operator("infotext.primitives_new", text="", icon='DOT')
        op.primitives_enum = "screw_prim"
        op.screw_enum = 'screw_7'

        op = row.operator("infotext.primitives_new", text="", icon='MESH_CIRCLE')
        op.primitives_enum = "screw_prim"
        op.screw_enum = 'screw_6'

        op = row.operator("infotext.primitives_new", text="", icon='MESH_CYLINDER')
        op.primitives_enum = "screw_prim"
        op.screw_enum = 'screw_1'

        screw = icons.get("prim_screw_2")
        op = row.operator("infotext.primitives_new", text="", icon_value=screw.icon_id)
        op.primitives_enum = "screw_prim"
        op.screw_enum = 'screw_2'

        screw = icons.get("prim_screw_3")
        op = row.operator("infotext.primitives_new", text="", icon_value=screw.icon_id)
        op.primitives_enum = "screw_prim"
        op.screw_enum = 'screw_3'

        screw = icons.get("prim_screw_4")
        op = row.operator("infotext.primitives_new", text="", icon_value=screw.icon_id)
        op.primitives_enum = "screw_prim"
        op.screw_enum = 'screw_4'

        screw = icons.get("prim_screw_5")
        op = row.operator("infotext.primitives_new", text="", icon_value=screw.icon_id)
        op.primitives_enum = "screw_prim"
        op.screw_enum = 'screw_5'

        # -------EDITABLE PRIMITIVES
        layout.label(text="Editable Primitives", icon='MODIFIER')
        row = layout.row(align=True)
        row.scale_x = 1.3
        op = row.operator("infotext.primitives_new", icon='MESH_CUBE', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'cube'

        op = row.operator("infotext.primitives_new", icon='MESH_UVSPHERE', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'sphere'

        op = row.operator("infotext.primitives_new", icon='MESH_CYLINDER', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'cylinder'

        op = row.operator("infotext.primitives_new", icon='MESH_CONE', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'cone'

        op = row.operator("infotext.primitives_new", icon='MESH_TORUS', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'torus'

        op = row.operator("infotext.primitives_new", icon='MESH_GRID', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'grid'

        op = row.operator("infotext.primitives_new", icon='MESH_CAPSULE', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'capsule'

        op = row.operator("infotext.primitives_new", icon='MATSPHERE', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'quad_sphere'

        op = row.operator("infotext.primitives_new", icon='MESH_CIRCLE', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'circle'

        # -------CUSTOM PRIMITIVES
        layout.label(text="Custom Primitives", icon='META_CAPSULE')
        row = layout.row(align=True)

        row.scale_x = 1.3
        op = row.operator("infotext.primitives_new", icon='META_CUBE', text="")
        op.primitives_enum = "custom_prim"
        op.custom_enum = 'rounded_cube'

        op = row.operator("infotext.primitives_new", icon='META_PLANE', text="")
        op.primitives_enum = "custom_prim"
        op.custom_enum = 'rounded_plane'

        op = row.operator("infotext.primitives_new", icon='META_CUBE', text="")
        op.primitives_enum = "custom_prim"
        op.custom_enum = 'rounded_plane_round'

        op = row.operator("infotext.primitives_new", icon='META_CUBE', text="")
        op.primitives_enum = "custom_prim"
        op.custom_enum = 'rounded_plane_2'

        custom = icons.get("prim_cross")
        op = row.operator("infotext.primitives_new", icon_value=custom.icon_id, text="")
        op.custom_enum = 'cross'

        custom = icons.get("prim_cross_rounded")
        op = row.operator("infotext.primitives_new", icon_value=custom.icon_id, text="")
        op.custom_enum = 'rounded_cross'

        op = row.operator("infotext.primitives_new", icon='MESH_CAPSULE', text="")
        op.primitives_enum = "custom_prim"
        op.custom_enum = 'long_cylinder'

        op = row.operator("infotext.primitives_new", icon='IPO_CONSTANT', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'line'

        op = row.operator("infotext.primitives_new", icon='ANTIALIASED', text="")
        op.primitives_enum = "editable_prim"
        op.editable_enum = 'tube'

        # -------TOOLS
        layout.label(text="Tools", icon='TOOL_SETTINGS')

        split = layout.split()
        col = split.column(align=True)
        col.scale_y = 1.5
        col.operator("infotext.cursor_tools", text="Copy Cursor Rotation",
                     icon='PIVOT_CURSOR').cursor_tools = 'copy_cursor_rot'
        col.operator("infotext.cursor_tools", text="Selection To Cursor",
                     icon='PIVOT_BOUNDBOX').cursor_tools = 'selection_to_cursor'
        col.operator("infotext.cursor_tools", text="Cursor To Selection + Rotation",
                     icon='PIVOT_CURSOR').cursor_tools = 'cursor_to_selection_rot'
        col.operator("infotext.cursor_tools", text="Align View To Cursor Rotation",
                     icon='VIEW_PERSPECTIVE').cursor_tools = 'align_view_to_cursor_rot'
        col.operator("infotext.cursor_tools", text="Align Cursor To Object Rotation",
                     icon='EMPTY_AXIS').cursor_tools = 'align_cursor_to_object_rot'


UI_CLASSES = [
    # INFOTEXT_simplify_popup,
    # INFOTEXT_vertex_group,
    # INFOTEXT_primitives_popup,
    # INFOTEXT_color_Popup,
    # INFOTEXT_lattice_popup,
    INFOTEXT_show_text_options_popup,
    # INFOTEXT_MT_tools_menu,
    # INFOTEXT_PT_panel
]

EXTRA_CLASSES = [
    # INFOTEXT_pie_menu
]


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
