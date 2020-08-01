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

from bpy.props import (
    StringProperty,
    BoolProperty,
    FloatVectorProperty,
    FloatProperty,
    EnumProperty,
    IntProperty
)

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

    # FIXME: Do we need this?
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
            row.prop(addon_pref, "show_infotext", text="")

            row = col.row(align=True)
            row.label(text="View Perspective")
            row.prop(addon_pref, "show_view_perspective", text="")

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
            row.label(text="Detailed Modifiers")
            row.prop(addon_pref, "detailed_modifiers", text="")

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


UI_CLASSES = [
    INFOTEXT_show_text_options_popup,
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
