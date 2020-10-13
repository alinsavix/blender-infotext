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

bl_info = {
    "name": "Blender InfoText",
    "description": "Better text handling for informational text",
    "author": "TDV Alinsa",
    "version": (0, 0, 1),
    "blender": (2, 90, 0),
    "location": "View3D",
    "warning": "WIP",
    "wiki_url": "",
    "category": "Tools"
}

from . import (
    functions,
)

import bpy
from mathutils import *
from bpy.props import (
    StringProperty,
    BoolProperty,
    PointerProperty,
    FloatVectorProperty,
    FloatProperty,
    EnumProperty,
    IntProperty,
    BoolVectorProperty
)

from .companion_text import *
from .functions import get_addon_preferences
# from .icon.icons import load_icons

#
# Preferences
#


class InfotextAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__

    prefs_tabs: EnumProperty(
        items=(
            ('info', "Info", "INFORMATION"),
            ('options', "Options", "ADDON OPTIONS"),
            ('links', "Links", "LINKS"),
        ),
        default='info',
    )

    # SHOW TEXTS
    show_infotext: BoolProperty(
        name="Enable Infotext",
        default=True,
        description="Enable Infotext in Viewport"
    )

    show_blender_keymaps: BoolProperty(
        name="Show Blender Keymaps",
        default=False,
        description="Show Blender Keymaps"
    )

    show_view_perspective: BoolProperty(
        name="Show View Perspective",
        default=True,
        description="Show View Perspective"
    )

    show_object_mode: BoolProperty(
        name="Show Object Mode",
        default=True,
        description="Show Object Mode"
    )

    show_vert_face_tris: BoolProperty(
        name="Show Vertex, Faces, Triangles & Ngons",
        default=True,
        description="Show Vertex, Faces, Triangles & Ngons"
    )

    show_object_info: BoolProperty(
        name="Show Modifiers",
        default=True,
        description="Show Modifiers"
    )

    show_object_name: BoolProperty(
        name="Show Object Type & Name",
        default=True,
        description="Show Object & Name"
    )

    show_loc_rot_scale: BoolProperty(
        name="Show Location, Rotation & Scale",
        default=True,
        description="Show Location, Rotation & Scale"
    )

    show_modifiers: BoolProperty(
        name="Show Modifiers",
        default=True,
        description="Show Modifiers"
    )

    detailed_modifiers: BoolProperty(
        name="Detailed Modifiers",
        default=True,
        description="Show Detailed Modifier Properties"
    )

    # TEXT OPTIONS
    color_title: FloatVectorProperty(
        name="",
        default=(1.0, 1.0, 1.0, 1.0),
        min=0.0, max=1.0, size=4,
        subtype='COLOR_GAMMA'
    )

    color_setting: FloatVectorProperty(
        name="",
        default=(0.5, 1.0, 0.0, 1.0),
        min=0.0, max=1.0, size=4,
        subtype='COLOR_GAMMA'
    )

    color_value: FloatVectorProperty(
        name="",
        default=(0.0, 0.7, 1.0, 1.0),
        min=0.0, max=1.0, size=4,
        subtype='COLOR_GAMMA'
    )

    color_option: FloatVectorProperty(
        name="",
        default=(1.0, 0.886, 0.2, 1.0),
        min=0.0, max=1.0, size=4,
        subtype='COLOR_GAMMA'
    )

    color_warning: FloatVectorProperty(
        name="",
        default=(1.0, 0.0, 0.0, 1.0),
        min=0, max=1, size=4,
        subtype='COLOR_GAMMA'
    )

    infotext_text_shadow: BoolProperty(
        name="Text Shadows",
        default=False,
        description="Text Shadows"
    )

    infotext_shadow_color: FloatVectorProperty(
        name="",
        default=(0.0, 0.0, 0.0, 1.0),
        min=0.0, max=1.0, size=4,
        subtype='COLOR_GAMMA'
    )

    infotext_shadow_alpha: FloatProperty(
        name="",
        default=1.0,
        min=0.0, max=1.0
    )

    infotext_offset_shadow_x: IntProperty(
        name="",
        default=2,
        min=-5, max=5
    )

    infotext_offset_shadow_y: IntProperty(
        name="",
        default=-2,
        min=-5, max=5
    )

    text_size_max: IntProperty(
        name="",
        default=22,
        min=10, max=30,
        description="Maximal size of the text"
    )

    text_size_mini: IntProperty(
        name="",
        default=10,
        min=10, max=30,
        description="Minimal size when the window is smaller"
    )

    infotext_text_space: FloatProperty(
        name="",
        default=2.0,
        min=0.5, max=100.0,
        description="Space Between lines"
    )

    infotext_text_pos_y: IntProperty(
        name="",
        default=105,
        min=0, max=2000,
        description="Position of the text in Y"
    )

    infotext_text_pos_x: IntProperty(
        name="",
        default=20,
        min=0, max=2000,
        description="Position of the text in X"
    )

    def draw(self, context):
        layout = self.layout
        wm = bpy.context.window_manager
        infotext = bpy.context.window_manager.infotext
        # icons = ui.load_icons()

        row = layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)

        # Info
        if self.prefs_tabs == 'info':
            box = layout.box()
            split = box.split()
            col = split.column()
            col.label(text="This is a test addon text string")
            col.separator()
            col.label(text="more test text")
            col.label(text="and more test text")

        # Options
        if self.prefs_tabs == 'options':
            box = layout.box()

            row = box.row(align=True)
            row.label(text="Enable Infotext in Viewport")
            row.prop(self, "show_infotext", expand=True, text=" ")

            if self.show_infotext:
                row = box.row(align=True)
                row.label(text="Show View Perspective")
                row.prop(self, "show_view_perspective", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Show Object Mode")
                row.prop(self, "show_object_mode", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Show Object Type & Name")
                row.prop(self, "show_object_name", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Show Transforms")
                row.prop(self, "show_loc_rot_scale", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Show Vert/Faces/Tris/Ngons")
                row.prop(self, "show_vert_face_tris", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Show Object informations")
                row.prop(self, "show_object_info", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Show Modifiers")
                row.prop(self, "show_modifiers", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Detailed Modifiers")
                row.prop(self, "detailed_modifiers", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Show Blender Keymaps")
                row.prop(self, "show_blender_keymaps", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Title Text Color")
                row.prop(self, "olor_title")

                row = box.row(align=True)
                row.label(text="Setting Name Text Color")
                row.prop(self, "color_setting")

                row = box.row(align=True)
                row.label(text="Setting Value Text Color")
                row.prop(self, "color_value")

                row = box.row(align=True)
                row.label(text="Warning Text Color")
                row.prop(self, "color_warning")

                row = box.row(align=True)
                row.label(text="Text Size Max")
                row.prop(self, "text_size_max")

                row = box.row(align=True)
                row.label(text="Text Size Min")
                row.prop(self, "text_size_mini")

                row = box.row(align=True)
                row.label(text="Text Space")
                row.prop(self, "infotext_text_space")

                row = box.row(align=True)
                row.label(text="Text X position")
                row.prop(self, "infotext_text_pos_x")

                row = box.row(align=True)
                row.label(text="Text Y position")
                row.prop(self, "infotext_text_pos_y")

                row = box.row(align=True)
                row.label(text="Activate Shadows")
                row.prop(self, "infotext_text_shadow", text="      ")

                if self.infotext_text_shadow:
                    row = box.row(align=True)
                    row.label(text="Shadows Color")
                    row.prop(self, "infotext_shadow_color")

                    row = box.row(align=True)
                    row.label(text="Shadows Transparency")
                    row.prop(self, "infotext_shadow_alpha")

                    row = box.row(align=True)
                    row.label(text="Offset Shadows X")
                    row.prop(self, "infotext_offset_shadow_x")

                    row = box.row(align=True)
                    row.label(text="Offset Shadows Y")
                    row.prop(self, "infotext_offset_shadow_y")
                    # End of original IF block above

            # RESET PREFS
            # row = box.row(align=True)
            # row.operator("object.reset_prefs", text="Reset Preferences")

        # # ------URls
        if self.prefs_tabs == 'links':
            box = layout.box()
            box.label(text="Support me:", icon='HAND')
            box.operator("wm.url_open",
                         text="Patreon").url = "https://www.patreon.com/someone"

            box.separator()
            box.label(text="Web:", icon='WORLD')
            box.operator("wm.url_open", text="example.com").url = "http://www.example.com/"

            box.separator()
            box.label(text="Social:", icon='USER')
            box.operator("wm.url_open", text="Twitter").url = "https://twitter.com/example"


# Property Group
class INFOTEXT_OT_property_group(bpy.types.PropertyGroup):
    face_type_count = {}
    # previous_mesh = []   # FIXME: What is this used for?
    # previous_mode: StringProperty()


##################################
# Register
##################################

CLASSES = [
    # INFOTEXT_OT_Reset_Prefs,
    InfotextAddonPrefs,
    INFOTEXT_OT_property_group,
]


def register():
    functions.register()

    for cls in CLASSES:
        try:
            bpy.utils.register_class(cls)
        except:
            print(f"{cls.__name__} already registred")

    bpy.types.WindowManager.infotext = PointerProperty(type=INFOTEXT_OT_property_group)

    # Check the addon version on Github
    # context = bpy.context
    # prefs = context.preferences.addons[__name__].preferences
    # check_for_update(prefs, context)

    # Add Text
    if infotext_text_Handle:
        bpy.types.SpaceView3D.draw_handler_remove(
            infotext_text_Handle[0], 'WINDOW')
    infotext_text_Handle[:] = [
        bpy.types.SpaceView3D.draw_handler_add(infotext_draw_text_callback, (), 'WINDOW', 'POST_PIXEL')]


# Unregister
def unregister():
    functions.unregister()

    for cls in CLASSES:
        bpy.utils.unregister_class(cls)

    # Remove Text
    if infotext_text_Handle:
        bpy.types.SpaceView3D.draw_handler_remove(
            infotext_text_Handle[0], 'WINDOW')
        infotext_text_Handle[:] = []
