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
    "blender": (2, 80, 0),
    "location": "View3D",
    "wiki_url": "",
    "category": "Tools"
}

from . import (
    functions,
    ui,
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
from .icon.icons import load_icons


# RESET PREFERENCES
class INFOTEXT_OT_Reset_Prefs(bpy.types.Operator):
    bl_idname = 'object.reset_prefs'
    bl_label = "Reset Addon Preferences"
    bl_options = {'REGISTER', "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    show_text: BoolProperty(
        name="Show text",
        description="Show/Hide the text in the viewport",
        default=True
    )

    text_color: BoolProperty(
        name="Text color",
        description="Colorize the Text",
        default=True
    )

    text_size_pos: BoolProperty(
        name="Text Size & Position",
        description="Change the size ad the position of the text",
        default=True
    )

    text_shadows: BoolProperty(
        name="Text Shadows",
        description="Text Shadows",
        default=True
    )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "show_text",
                    text="Show/Hide the text in the viewport")
        layout.prop(self, "text_color", text="Colorize the Text")
        layout.prop(self, "text_size_pos", text="Text Size & Position")
        layout.prop(self, "text_shadows", text="Text Shadows")

    # FIXME: Why is all this set here, if it's also set inside
    # INFOTEXT_MT_addon_prefs, and the stuff here seems to do nothing?
    def execute(self, context):
        addon_pref = get_addon_preferences()

        # TEXT OPTIONS
        if self.show_text:
            addon_pref.show_infotext = True
            addon_pref.show_view_perspective = True
            addon_pref.show_object_mode = True
            addon_pref.show_vert_face_tris = True
            addon_pref.show_object_name = True
            addon_pref.show_loc_rot_scale = True
            addon_pref.show_modifiers = True
            addon_pref.show_object_info = True
            addon_pref.detailed_modifiers = False
            addon_pref.show_blender_keymaps = True

        # TEXT COLOR
        if self.text_color:
            addon_pref.title = (1, 1, 1, 1)
            addon_pref.setting = (0.5, 1, 0, 1)
            addon_pref.value = (0, 0.7, 1, 1)
            addon_pref.hidden = (1, 0, 0, 1)

        # TEXT SIZE & POSITION
        if self.text_size_pos:
            addon_pref.text_size_max = 22
            addon_pref.text_size_mini = 10
            addon_pref.infotext_text_space = 2
            addon_pref.infotext_text_pos_x = 31
            addon_pref.infotext_text_pos_y = 52

        # SHADOWS
        if self.text_shadows:
            addon_pref.infotext_text_shadow = False
            addon_pref.infotext_shadow_color = (0, 0, 0, 0)
            addon_pref.infotext_shadow_alpha = 1
            addon_pref.infotext_offset_shadow_x = 2
            addon_pref.infotext_offset_shadow_y = -2

        bpy.context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


# Preferences
##################################
class INFOTEXT_MT_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = __name__

    prefs_tabs: EnumProperty(
        items=(
            ('info', "Info", "NFORMATIONS"),
            ('options', "Options", "ADDON OPTIONS"),
            ('links', "Links", "LINKS"),
        ),
        default='info',
    )

    # SHOW TEXTS
    show_infotext: BoolProperty(
        name="Enable Infotext in Viewport",
        default=True,
        description="Enable Infotext in Viewport"
    )

    show_blender_keymaps: BoolProperty(
        name="Show Blender Keymaps",
        default=True,
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

    # TEXTS OPTIONS
    # title : FloatVectorProperty(
    #         name="",
    #         default=(1, 1, 1, 1),
    #         min=0, max=1, size=4,
    #         subtype='COLOR_GAMMA'
    #         )
    #
    # setting : FloatVectorProperty(
    #         name="",
    #         default=(0.5, 1, 0, 1),
    #         min=0, max=1, size=4,
    #         subtype='COLOR_GAMMA'
    #         )
    #
    # value : FloatVectorProperty(
    #         name="",
    #         default=(0, 0.7, 1, 1),
    #         min=0, max=1, size=4,
    #         subtype='COLOR_GAMMA'
    #         )

    text_color: FloatVectorProperty(
        name="",
        default=(1, 1, 1, 1),
        min=0, max=1, size=4,
        subtype='COLOR_GAMMA'
    )

    text_color_1: FloatVectorProperty(
        name="",
        default=(0.5, 1, 0, 1),
        min=0, max=1, size=4,
        subtype='COLOR_GAMMA'
    )

    text_color_2: FloatVectorProperty(
        name="",
        default=(0, 0.7, 1, 1),
        min=0, max=1, size=4,
        subtype='COLOR_GAMMA'
    )

    option: FloatVectorProperty(
        name="",
        default=(1, 0.886, 0.2, 1),
        min=0, max=1, size=4,
        subtype='COLOR_GAMMA'
    )

    hidden: FloatVectorProperty(
        name="",
        default=(1, 0, 0, 1),
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
        default=(0.0, 0.0, 0, 1),
        min=0, max=1, size=4,
        subtype='COLOR_GAMMA'
    )

    infotext_shadow_alpha: FloatProperty(
        name="",
        default=1,
        min=0, max=1
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
        name="Space Between lines",
        default=2,
        min=0.5, max=100,
        description="Space Between lines"
    )

    infotext_text_pos_y: IntProperty(
        name="",
        default=52,
        min=0, max=2000,
        description="Position of the text in Y"
    )

    infotext_text_pos_x: IntProperty(
        name="",
        default=31,
        min=0, max=2000,
        description="Position of the text in X"
    )

    def draw(self, context):
        layout = self.layout
        wm = bpy.context.window_manager
        infotext = bpy.context.window_manager.infotext
        icons = ui.load_icons()

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
                row.label(text="Title Color")
                row.prop(self, "text_color")

                row = box.row(align=True)
                row.label(text="Settings Color")
                row.prop(self, "text_color_1")

                row = box.row(align=True)
                row.label(text="Value Color")
                row.prop(self, "text_color_2")

                row = box.row(align=True)
                row.label(text="Modifier Hidden")
                row.prop(self, "hidden")

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
            row = box.row(align=True)
            row.operator("object.reset_prefs", text="Reset Preferences")

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
    previous_mesh = []   # FIXME: What is this used for?
    previous_mode: StringProperty()


##################################
# Register
##################################

CLASSES = [
    INFOTEXT_OT_Reset_Prefs,
    INFOTEXT_MT_addon_prefs,
    INFOTEXT_OT_property_group,
]


def register():
    functions.register()
    ui.register()

    for cls in CLASSES:
        try:
            bpy.utils.register_class(cls)
        except:
            print(f"{cls.__name__} already registred")

    bpy.types.WindowManager.infotext = PointerProperty(type=INFOTEXT_OT_property_group)

    context = bpy.context
    prefs = context.preferences.addons[__name__].preferences

    # Add Text
    if infotext_text_Handle:
        bpy.types.SpaceView3D.draw_handler_remove(
            infotext_text_Handle[0], 'WINDOW')
    infotext_text_Handle[:] = [
        bpy.types.SpaceView3D.draw_handler_add(infotext_draw_text_callback, (), 'WINDOW', 'POST_PIXEL')]


# Unregister
def unregister():
    functions.unregister()
    ui.unregister()

    for cls in CLASSES:
        bpy.utils.unregister_class(cls)

    # Remove Text
    if infotext_text_Handle:
        bpy.types.SpaceView3D.draw_handler_remove(
            infotext_text_Handle[0], 'WINDOW')
        infotext_text_Handle[:] = []
