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

# Import des modules
if "bpy" in locals():
    import importlib
    reloadable_modules = [
        "functions",
        "ui",
        "lattice",
        "modals",
        "operators",
        "modifiers_popup",
        "primitives"
    ]
    for module in reloadable_modules:
        if module in locals():
            importlib.reload(locals()[module])

print(__name__ + "::1")
from . import (functions,
               ui,
               #    lattice,
               #    modals,
               #    operators,
               #    modifiers_popup,
               )
print(__name__ + "::2")
import bpy
print(__name__ + "::3")
from mathutils import *
# import rna_keymap_ui
print(__name__ + "::4")
from bpy.props import (StringProperty,
                       BoolProperty,
                       PointerProperty,
                       FloatVectorProperty,
                       FloatProperty,
                       EnumProperty,
                       IntProperty,
                       BoolVectorProperty)
print(__name__ + "::5")
# from .lattice import *
# from .operators import *
# from .modifiers_popup import *
from .companion_text import *
# from .primitives import *
print(__name__ + "::6")
from .functions import get_addon_preferences
# from .addon_updater import AddonUpdater
print(__name__ + "::7")
# from . import developer_utils
print(__name__ + "::8")
from .icon.icons import load_icons
print(__name__ + "::9")

#### updater = AddonUpdater()

# keymaps_items_dict = {"Modifier Popup": ['infotext.modifiers_popup', None, '3D View '
####                                         'Generic', 'VIEW_3D', 'WINDOW',
####                                         'QUOTE', 'PRESS', False, False, False
# ],
####
# "Primitives Popup": ['infotext.primitives_popup', None, '3D View '
####                                           'Generic', 'VIEW_3D', 'WINDOW',
####                                           'QUOTE', 'PRESS', False, True, False
# ],
####
# "Cube Menu":['wm.call_menu', 'TEST_MT_menu_cube_add', '3D View '
# 'Generic', 'VIEW_3D', 'WINDOW', 'RIGHTMOUSE',
# 'PRESS', True, True, False
# ],
####
# "Speedflow Companion Pie Menu": ['wm.call_menu_pie', 'infotext_pie_menu',
####                                                       '3D View Generic', 'VIEW_3D', 'WINDOW',
####                                                       'Q', 'PRESS', False, True, False
# ]
# }

keymaps_items_dict = {}


########################################
# UPDATE UI
########################################


# def update_pie_bl_label(self, context):
#     infotext = context.window_manager.infotext

#     # check for update and edit bl_label
#     if hasattr(bpy.types, "infotext_pie_menu"):
#         try:
#             bpy.utils.unregister_class(ui.infotext_pie_menu)
#         except:
#             pass

#     if infotext.update_available and self.show_update:
#         ui.infotext_pie_menu.bl_label = "An Update is available!"
#     else:
#         ui.infotext_pie_menu.bl_label = "Speedflow Companion"

#     bpy.utils.register_class(ui.infotext_pie_menu)


# def check_for_update(self, context):
#     if self.show_update:
#         updater.async_check_update(True)

#     update_pie_bl_label(self, context)

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
        default=True)

    text_color: BoolProperty(
        name="Text color",
        description="Colorize the Text",
        default=True)

    text_size_pos: BoolProperty(
        name="Text Size & Position",
        description="Change the size ad the position of the text",
        default=True)

    text_shadows: BoolProperty(
        name="Text Shadows",
        description="Text Shadows",
        default=True)

    # solo : BoolProperty(
    #     name="Solo",
    #     description="Solo",
    #     default=True)

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "show_text",
                    text="Show/Hide the text in the viewport")
        layout.prop(self, "text_color", text="Colorize the Text")
        layout.prop(self, "text_size_pos", text="Text Size & Position")
        layout.prop(self, "text_shadows", text="Text Shadows")
        # layout.prop(self, "solo", text="Solo")

    def execute(self, context):
        addon_pref = get_addon_preferences()

        # TEXT OPTIONS
        if self.show_text:
            addon_pref.drawText = True
            addon_pref.show_object_mode = True
            addon_pref.show_vert_face_tris = False
            addon_pref.show_object_name = True
            addon_pref.show_loc_rot_scale = True
            addon_pref.show_modifiers = True
            addon_pref.show_object_info = True
            addon_pref.simple_text_mode = True
            addon_pref.show_keymaps = True
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
            addon_pref.infotext_text_pos_x = 19
            addon_pref.infotext_text_pos_x = 29

        # SHADOWS
        if self.text_shadows:
            addon_pref.infotext_text_shadow = False
            addon_pref.infotext_shadow_color = (0, 0, 0, 0)
            addon_pref.infotext_shadow_alpha = 1
            addon_pref.infotext_offset_shadow_x = 2
            addon_pref.infotext_offset_shadow_y = -2

        # # SOLO
        # if self.solo:
        #     addon_pref.solo_color = (0.2, 0.7, 1, 1)
        #     addon_pref.solo_alpha = 0.3

        bpy.context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


# Preferences
##################################

class infotext_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = __name__

    prefs_tabs: EnumProperty(
        items=(('info', "Info", "NFORMATIONS"),
               ('options', "Options", "ADDON OPTIONS"),
               # ('keymaps', "Keymaps", "CHANGE KEYMAPS"),
               # ('docs', "Doc", "DOCUMENTATION"),
               # ('tutorials', 'Tutorials', 'Tutorials'),
               # ('addons', "Addons", "Addons"),
               # ('links', "Links", "LINKS"),
               ),
        default='info')

    # show_update: BoolProperty(
    #     name="Show update",
    #     description="Display info in the UI panel if an update is available",
    #     default=True,
    #     update=check_for_update
    # )

    # check_for_updates: BoolProperty(
    #     name="",
    #     default=False,
    #     description="Check for updates of the addon")

    scale_y: BoolProperty(
        name="",
        default=False
    )

    # use_normals_buttons: BoolProperty(
    #     name="Use Normal buttons",
    #     default=False,
    #     description="Use Normal buttons to apply, hide and remove")

    # SHOW TEXTS
    drawText: BoolProperty(
        name="Activate Text Modifiers in the viewport",
        default=True,
        description="Activate Text Modifiers in the viewport")

    show_keymaps: BoolProperty(
        name="Show Addons Keymaps",
        default=True,
        description="Show Addons Keymaps")

    show_blender_keymaps: BoolProperty(
        name="Show Blender Keymaps",
        default=True,
        description="Show Blender Keymaps")

    show_object_mode: BoolProperty(
        name="Show Object Mode",
        default=True,
        description="Show Object Mode"
    )

    show_vert_face_tris: BoolProperty(
        name="Show Vertex, Faces, Triangles & Ngons",
        default=False,
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

    simple_text_mode: BoolProperty(
        name="Simple Text Mode",
        default=True,
        description="Show only the name of modifiers"
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
        min=-5, max=5)

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

    use_bevel_node: BoolProperty(
        name="Use Bevel Node",
        default=False,
        description="Use Bevel Node"
    )

    infotext_text_pos_y: IntProperty(
        name="",
        default=29,
        min=0, max=2000,
        description="Position of the text in Y"
    )

    infotext_text_pos_x: IntProperty(
        name="",
        default=19,
        min=0, max=2000,
        description="Position of the text in X"
    )

    # SOLO
    # solo_color : FloatVectorProperty(
    #     name="Solo Color:",
    #     default=(0.2, 0.7, 1, 1),
    #     min=0, max=1, size=4,
    #     # precision=3,
    #     subtype='COLOR_GAMMA'
    # )
    #
    # solo_alpha : FloatProperty(
    #     default=0.3,
    #     min=0, max=1,
    #     precision=3
    # )
    # add_bool_objects_to_collection: BoolProperty(
    #     default=True, description="Add to Bool Objects Collection")
    # auto_smooth_value: FloatProperty(
    #     name="Auto Smooth", default=38.0, min=0.0, max=180.0, description="Add Auto Smooth")

    # def release_note_layout(self, box):
    #     for line in updater.release_note.split("\r"):
    #         box.label(text=line.split("\n")[-1])

    def draw(self, context):
        layout = self.layout
        wm = bpy.context.window_manager
        infotext = bpy.context.window_manager.infotext
        icons = ui.load_icons()

        box = layout.box()
        icon = icons.get("icon_discord")
        row = box.row()
        row.scale_y = 2
        row.operator("wm.url_open", text="SUPPORT ON DISCORD FOR CUSTOMERS",
                     icon_value=icon.icon_id).url = "https://discord.gg/ctQAdbY"

        box = layout.box()
        row = box.row(align=True)
        # row.label(text="Check For Updates")
        # row.prop(self, "show_update", text="      ")

        # if infotext.update_available and self.show_update:
        #     icons = load_icons()

        #     box.label(text="Textmate has been updated", icon='ERROR')
        #     # box.label(text= f"NEW VERSION: {SF.sf_update_new_version}", icon='ERROR')

        #     self.release_note_layout(box)

        #     box.label(text="Please download the last version and intall it")
        #     row = box.row()
        #     icon = icons.get("icon_gumroad")
        #     row.operator("wm.url_open", text="GUMROAD",
        #                  icon_value=icon.icon_id).url = "https://gumroad.com/l/speedflow"
        #     icon = icons.get("icon_market")
        #     row.operator("wm.url_open", text="BLENDER MARKET",
        #                  icon_value=icon.icon_id).url = "https://blendermarket.com/products/speedflow"
        #     icon = icons.get("icon_artstation")
        #     row.operator("wm.url_open", text="ARTSTATION",
        #                  icon_value=icon.icon_id).url = "https://www.artstation.com/pitiwazou/store/0xb/speedflow"
        #     box.separator()
        #     box.label(text="HOW TO UPDATE:", icon='FILE_REFRESH')
        #     box.label(text="- Uninstall previous version with the REMOVE Button")
        #     box.label(text="- Click on INSTALL FROM FILE")
        #     box.label(text="- Select the Zip")
        #     box.label(text="- Click OK")
        #     box.label(text="- Activate it")
        #     box.label(text="- Click on SAVE PREFERENCES")
        #     box.label(text="- Restart Blender")

        row = layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)

        # Info
        if self.prefs_tabs == 'info':
            box = layout.box()
            split = box.split()
            col = split.column()
            col.label(text="Keymap > Shift + Q")
            col.separator()
            col.label(text="Speedflow Companion works with Speedflow")
            col.label(
                text="This Addon allows you to edit your model in Object and Edit mode.")
            col.label(
                text="You can Create Primitives on the mouse to make Booleans.")
            col.label(
                text="You can add Bevel Weight, Sharps, Creases, clean faces, select Ngons etc")
            col.label(
                text="You can call the Carver Addon in the pie menu and add CAD Snap Utilities line tool to cut faces. ")
            col.label(
                text="In Curve selection you can edit the point, Poly, Bezier, change the radius etc")
            col.label(
                text="Each button allow several actions with Shift, Ctrl, Alt...")
            col.separator()
            col.label(
                text="Follow the documentation and videos for more informations.")

        # Options
        if self.prefs_tabs == 'options':
            # if bpy.app.version >= (2, 79, 1):
            box = layout.box()
            split = box.split()
            col = split.column()
            col.label(text="Use Bevel Shader:")
            col = split.column(align=True)
            col.prop(self, 'use_bevel_node', expand=True, text=" ")

            box = layout.box()
            split = box.split()
            col = split.column()
            col.label(text="Use Normal Buttons:")
            col = split.column(align=True)
            col.prop(self, 'use_normals_buttons', expand=True, text=" ")

            box = layout.box()
            split = box.split()
            col = split.column()
            col.label(text="Pie Menus Buttons Scale:")
            col = split.column(align=True)
            col.prop(self, 'scale_y', expand=True, text=" ")

            box = layout.box()
            split = box.split()
            col = split.column()
            col.label(text="Auto smooth :")
            col = split.column(align=True)
            col.prop(self, 'auto_smooth_value', expand=True, text="Angle")

            # box = layout.box()
            split = box.split()
            col = split.column()
            col.label(text="Add Bool Objects to Collection")
            col = split.column()
            col.prop(self, "add_bool_objects_to_collection", text="      ")

            # box = layout.box()
            # split = box.split()
            # col = split.column()
            # col.label(text="Solo Color:")
            # col = split.column(align=True)
            # col.prop(self, "solo_color", text="")
            #
            # split = box.split()
            # col = split.column()
            # col.label(text="Solo Alpha:")
            # col = split.column(align=True)
            # col.prop(self, "solo_alpha", text="")

            # MAT COLOR
            # box = layout.box()
            # split = box.split()
            # col = split.column()
            # col.label(text="Material Color:")
            # row = box.row(align=True)
            # row.label(text="Plastic")
            # row.prop(self, "color_1")
            #
            # row = box.row(align=True)
            # row.label(text="Material 2")
            # row.prop(self, "color_2")

            box = layout.box()
            row = box.row(align=True)
            row.label(text="Text Options:")

            row = box.row(align=True)
            row.label(text="Text in the viewport")
            row.prop(self, "drawText", expand=True, text=" ")

            row = box.row(align=True)
            row.label(text="Show Object Mode")
            row.prop(self, "show_object_mode", expand=True, text=" ")

            # row = box.row(align=True)
            # row.label(text="Show Object Type & Name")
            # row.prop(self, "show_object_name", expand=True, text=" ")

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
            row.label(text="Simple Mode for Modifiers")
            row.prop(self, "simple_text_mode", expand=True, text=" ")

            row = box.row(align=True)
            row.label(text="Show Addons Keymaps")
            row.prop(self, "show_keymaps", expand=True, text=" ")

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

            # RESET PREFS
            row = box.row(align=True)
            row.operator("object.reset_prefs", text="Reset Preferences")

        # -----------Keymap settings
        # if self.prefs_tabs == 'keymaps':
        #     wm = bpy.context.window_manager

        #     draw_keymap_items(wm, layout)

        # ------TUTORIALS
        # if self.prefs_tabs == 'tutorials':
        #     box = layout.box()
        #     box.label(text="Free Tutorials:", icon='COMMUNITY')
        #     box.operator(
        #         "wm.url_open", text="Youtube Channel").url = "https://www.youtube.com/user/pitiwazou"
        #     box.label(text="Paid Tutorials:", icon='HAND')
        #     box.operator("wm.url_open",
        #                  text="Non - Destructive Workflow Tutorial 1").url = "https://gumroad.com/l/Non-Destructive_Workflow_Tutorial_1"
        #     box.operator("wm.url_open",
        #                  text="Non - Destructive Workflow Tutorial 2").url = "https://gumroad.com/l/Non-Destructive_Workflow_Tutorial_2"
        #     box.operator("wm.url_open",
        #                  text="Non - Destructive Workflow Tutorial 3").url = "https://gumroad.com/l/Non-Destructive_Workflow_Tutorial_3"
        #     box.operator("wm.url_open",
        #                  text="Hydrant Modeling Tutorial").url = "https://gumroad.com/l/hydrant_modeling_tutorial"
        #     box.operator("wm.url_open",
        #                  text="Hydrant Unwrapping Tutorial").url = "https://gumroad.com/l/hydrant_unwrapping_tutorial"
        #     box.operator("wm.url_open",
        #                  text="Furry Warfare Plane Modeling Tutorial").url = "https://gumroad.com/l/furry_warfare_plane_modeling_tutorial"

        # # ------Addons
        # if self.prefs_tabs == 'addons':
        #     box = layout.box()
        #     box.operator(
        #         "wm.url_open", text="Addon's Discord").url = "https://discord.gg/ctQAdbY"
        #     box.separator()
        #     box.operator(
        #         "wm.url_open", text="Asset Management").url = "https://gumroad.com/l/asset_management"
        #     box.operator(
        #         "wm.url_open", text="Speedflow").url = "https://gumroad.com/l/speedflow"
        #     box.operator(
        #         "wm.url_open", text="SpeedSculpt").url = "https://gumroad.com/l/SpeedSculpt"
        #     box.operator(
        #         "wm.url_open", text="SpeedRetopo").url = "https://gumroad.com/l/speedretopo"
        #     box.operator(
        #         "wm.url_open", text="Easyref").url = "https://gumroad.com/l/easyref"
        #     box.operator(
        #         "wm.url_open", text="RMB Pie Menu").url = "https://gumroad.com/l/wazou_rmb_pie_menu_v2"
        #     box.operator(
        #         "wm.url_open", text="Wazou's Pie Menu").url = "https://gumroad.com/l/wazou_pie_menus"
        #     box.operator(
        #         "wm.url_open", text="Smart Cursor").url = "https://gumroad.com/l/smart_cursor"
        #     box.operator("wm.url_open",
        #                  text="My 2.79 Theme").url = "https://www.dropbox.com/s/x6vcip7n11j5w4e/wazou_2_79_001.xml?dl=0"

        # # ------URls
        # if self.prefs_tabs == 'links':
        #     box = layout.box()
        #     box.label(text="Support me:", icon='HAND')
        #     box.operator(
        #         "wm.url_open", text="Patreon").url = "https://www.patreon.com/pitiwazou"
        #     box.operator(
        #         "wm.url_open", text="Tipeee").url = "https://www.tipeee.com/blenderlounge"
        #     box.separator()

        #     box.label(text="Archipack", icon='BLENDER')
        #     box.operator(
        #         "wm.url_open", text="Archi Pack").url = "https://blender-archipack.org"

        #     box.separator()
        #     box.label(text="Web:", icon='WORLD')
        #     box.operator(
        #         "wm.url_open", text="Pitiwazou.com").url = "http://www.pitiwazou.com/"
        #     box.separator()
        #     box.label(text="Youtube:", icon='SEQUENCE')
        #     box.operator(
        #         "wm.url_open", text="Youtube - Pitiwazou").url = "https://www.youtube.com/user/pitiwazou"
        #     box.operator("wm.url_open",
        #                  text="Youtube - Blenderlounge").url = "https://www.youtube.com/channel/UCaA3_WSE5A0H6YrS1SDfAQw/videos"
        #     box.separator()
        #     box.label(text="Social:", icon='USER')
        #     box.operator(
        #         "wm.url_open", text="Artstation").url = "https://www.artstation.com/artist/pitiwazou"
        #     box.operator(
        #         "wm.url_open", text="Twitter").url = "https://twitter.com/#!/pitiwazou"
        #     box.operator("wm.url_open",
        #                  text="Facebook").url = "https://www.facebook.com/Pitiwazou-C%C3%A9dric-Lepiller-120591657966584/"
        #     box.operator(
        #         "wm.url_open", text="Google+").url = "https://plus.google.com/u/0/116916824325428422972"
        #     box.operator(
        #         "wm.url_open", text="Blenderlounge's Discord").url = "https://discord.gg/MBDphac"


# -----------------------------------------------------------------------------
#    Keymap
# -----------------------------------------------------------------------------
addon_keymaps = []


# def draw_keymap_items(wm, layout):
#     kc = wm.keyconfigs.user

#     for name, items in keymaps_items_dict.items():
#         kmi_name, kmi_value, km_name = items[:3]
#         box = layout.box()
#         split = box.split()
#         col = split.column()
#         col.label(text=name)
#         col.separator()
#         km = kc.keymaps[km_name]
#         get_hotkey_entry_item(kc, km, kmi_name, kmi_value, col)


# def get_hotkey_entry_item(kc, km, kmi_name, kmi_value, col):

#     # for menus and pie_menu
#     if kmi_value:
#         for km_item in km.keymap_items:
#             if km_item.idname == kmi_name and km_item.properties.name == kmi_value:
#                 col.context_pointer_set('keymap', km)
#                 rna_keymap_ui.draw_kmi([], kc, km, km_item, col, 0)
#                 return

#         col.label(text="No hotkey entry found for {}".format(kmi_value))
#         col.operator(
#             INFOTEXT_OT_add_hotkey.bl_idname, icon='ZOOMIN')

#     # for operators
#     else:
#         if km.keymap_items.get(kmi_name):
#             col.context_pointer_set('keymap', km)
#             rna_keymap_ui.draw_kmi(
#                 [], kc, km, km.keymap_items[kmi_name], col, 0)
#         else:
#             col.label(text="No hotkey entry found for {}".format(kmi_name))
#             col.operator(
#                 INFOTEXT_OT_add_hotkey.bl_idname, icon='ZOOMIN')


# class INFOTEXT_OT_add_hotkey(bpy.types.Operator):
#     ''' Add hotkey entry '''
#     bl_idname = "template.add_hotkey"
#     bl_label = "Add Hotkeys"
#     bl_options = {'REGISTER', 'INTERNAL'}

#     def execute(self, context):
#         add_hotkey()

#         self.report({'INFO'},
#                     "Hotkey added in User Preferences -> Input -> Screen -> Screen (Global)")
#         return {'FINISHED'}


# def add_hotkey():
#     wm = bpy.context.window_manager
#     kc = wm.keyconfigs.addon

#     if not kc:
#         return

#     for items in keymaps_items_dict.values():
#         kmi_name, kmi_value, km_name, space_type, region_type = items[:5]
#         eventType, eventValue, ctrl, shift, alt = items[5:]
#         km = kc.keymaps.new(name=km_name, space_type=space_type,
#                             region_type=region_type)

#         kmi = km.keymap_items.new(kmi_name, eventType,
#                                   eventValue, ctrl=ctrl, shift=shift,
#                                   alt=alt

#                                   )
#         if kmi_value:
#             kmi.properties.name = kmi_value

#         kmi.active = True

#     addon_keymaps.append((km, kmi))


# def remove_hotkey():
#     ''' clears all addon level keymap hotkeys stored in addon_keymaps '''

#     kmi_values = [item[1] for item in keymaps_items_dict.values() if item]
#     kmi_names = [item[0] for item in keymaps_items_dict.values() if item not in [
#         'wm.call_menu', 'wm.call_menu_pie']]

#     for km, kmi in addon_keymaps:
#         # remove addon keymap for menu and pie menu
#         if hasattr(kmi.properties, 'name'):
#             if kmi_values:
#                 if kmi.properties.name in kmi_values:
#                     km.keymap_items.remove(kmi)

#         # remove addon_keymap for operators
#         else:
#             if kmi_names:
#                 if kmi.name in kmi_names:
#                     km.keymap_items.remove(kmi)

#     addon_keymaps.clear()

# Property Group


class INFOTEXT_OT_property_group(bpy.types.PropertyGroup):

    # Poky count
    face_type_count = {}
    previous_mesh = []
    previous_mode: StringProperty()

# Check Update
# sc_update_check: BoolProperty(
#     default=False, description="Check For Updates")

# sc_update_new_version: StringProperty(description="Updates Version")

# Modifiers popup
# add_apply_remove: EnumProperty(
#     items=(('add', "Add", "ADD MODIFIERS ON SELECTION"),
#            ('apply', "Apply", "APPLY MODIFIERS ON SELECTION"),
#            ('remove', "Remove", "REMOVE MODIFIERS ON SELECTION")),
#     default='add')

# toggle_all_modifiers_prop: BoolProperty(
#     default=True, update=toggle_all_modifiers)
# hide_all_modifiers_prop: BoolProperty(
#     default=True, update=hide_all_modifiers)

# Primitives
# infotext_global_orientation: BoolProperty(
#     default=False,
#     description="Hide Lattice on selected objects")

# align_to_view: BoolProperty(
#     name="Align To View",
#     default=False,
#     description="Align To View")

# align_cursor_rot: BoolProperty(
#     name="Align To Cursor Rotation",
#     default=False,
#     description="Align To Cursor Rotation")

# update_available: BoolProperty(default=False)

# Already disabled when I got here   --A
# Solo
# material_color : FloatVectorProperty(
##             name="Material Color",
##             default=(0.214041, 0.214041, 0.214041, 1),
# min=0, max=1,
# precision=3,
# size=3,
# subtype='COLOR_GAMMA',
##             update = Set_Material_Color
# )
##
##
# material_alpha : FloatProperty(
##     name="Material Alpha",
##     default= 1.0,
# min=0.1, max=1,
# precision=3,
# update=Set_Material_Alpha
# )
##
# shader_type : EnumProperty(
# items=(('metal', "Metal", "ADD METAL SHADER"),
##                ('plastic', "Plastic", "ADD PLASTIC SHADER"),
# ('glass', "Glass", "ADD GLASS SHADER")),
# default='plastic'
# )
##
# random_or_color : EnumProperty(
# items=(('color', "Color", "ADD SELECTED COLOR"),
# ('random', "Random", "ADD RANDOM COLOR")),
# default='random'
# )

# def cursor_rot_boolean(context):
#     SFC_prim = context.window_manager.SFC_prim
#
#     SFC_prim.align_cursor_rot = not SFC_prim.align_cursor_rot
#     SFC_prim.add_boolean = not SFC_prim.add_boolean


# class infotext_Primitives_PropertyGroup(bpy.types.PropertyGroup):
#     align_cursor_rot: BoolProperty(
#         name="",
#         default=False,
#         description="Align To Cursor Rotation")

#     align_view: BoolProperty(
#         name="",
#         default=False,
#         description="Align To View")

#     bounds_display: BoolProperty(
#         name="",
#         default=False,
#         description="Use bound display for Boolean Operation")

#     edit_mode: BoolProperty(
#         name="",
#         default=False,
#         description="Launch in edit mode")

#     screw_mode: BoolProperty(
#         name="",
#         default=False,
#         description="Screw Mode")

#     add_boolean: BoolProperty(
#         name="",
#         default=False,
#         description="Add Boolean")

#     add_mirror: BoolProperty(
#         name="",
#         default=False,
#         description="Add Mirror")

#     add_rebool: BoolProperty(
#         name="",
#         default=False,
#         description="Add Rebool")

#     mirror_axis_x: BoolProperty(
#         name="",
#         default=False,
#         description="Mirror Axis X")

#     mirror_axis_y: BoolProperty(
#         name="",
#         default=False,
#         description="Mirror Axis Y")

#     mirror_axis_z: BoolProperty(
#         name="",
#         default=False,
#         description="Mirror Axis Z")

#     boolean_enum: EnumProperty(
#         items=(('DIFFERENCE', "DIFFERENCE", ""),
#                ('INTERSECT', "INTERSECT", ""),
#                ('UNION', "UNION", "")),
#         default='DIFFERENCE'
#     )

#     mirror_axis_xyz: EnumProperty(
#         items=(('X', "X", ""),
#                ('Y', "Y", ""),
#                ('Z', "Z", "")),
#         options={'ENUM_FLAG'},
#         # default = {'X'}
#     )

#     # cursor_and_boolean: BoolProperty(
#     #     name="",
#     #     default=False,
#     #     description="Align To Cursor Rotation and Use Boolean",
#     #     update = cursor_rot_boolean)


##################################
# Register
##################################


# CLASSES = [SFC_OT_Reset_Prefs,
#            infotext_addon_prefs,
#            SPEEDFLOW_COMPANION_OT_add_hotkey,
#            SFC_OT_property_group,
#            SFC_Primitives_PropertyGroup
#            ]

CLASSES = [INFOTEXT_OT_Reset_Prefs,
           infotext_addon_prefs,
           #    INFOTEXT_OT_add_hotkey,
           INFOTEXT_OT_property_group,
           #    infotext_Primitives_PropertyGroup
           ]

# Register


def register():
    functions.register()
    ui.register()
    # lattice.register()
    # modals.register()
    # operators.register()
    # modifiers_popup.register()
    # primitives.register()

    for cls in CLASSES:
        try:
            bpy.utils.register_class(cls)
        except:
            print(f"{cls.__name__} already registred")

    bpy.types.WindowManager.infotext = PointerProperty(
        type=INFOTEXT_OT_property_group)
    # bpy.types.WindowManager.infotext_prim = PointerProperty(
    #     type=infotext_Primitives_PropertyGroup)

    # hotkey setup
    # add_hotkey()

    # Check the addon version on Github
    context = bpy.context
    prefs = context.preferences.addons[__name__].preferences
    #### check_for_update(prefs, context)

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
    # lattice.unregister()
    # modals.unregister()
    # operators.unregister()
    # modifiers_popup.unregister()
    # primitives.unregister()

    for cls in CLASSES:
        bpy.utils.unregister_class(cls)

    # hotkey cleanup
    # remove_hotkey()

    # Remove Text
    if infotext_text_Handle:
        bpy.types.SpaceView3D.draw_handler_remove(
            infotext_text_Handle[0], 'WINDOW')
        infotext_text_Handle[:] = []
