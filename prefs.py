import os
import sys
from typing import TYPE_CHECKING, Tuple, Union, Optional

import bpy
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

class InfotextAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    if TYPE_CHECKING:
        layout: bpy.types.UILayout

    if TYPE_CHECKING:
        prefs_tabs: bpy.types.EnumProperty
    else:
        prefs_tabs: bpy.props.EnumProperty(
            items=(
                # ('info', "Info", "INFORMATION"),
                ('options', "Options", "ADDON OPTIONS"),
                ('links', "Links", "LINKS"),
            ),
            default='options',
        )

    # Do we show the info text at all?
    if TYPE_CHECKING:
        show_infotext: bpy.types.BoolProperty
    else:
        show_infotext: bpy.props.BoolProperty(
            name="Enable Infotext",
            default=True,
            description="Enable Infotext in Viewport",
        )

    # it'd be really cool if we could show the key choices when there was a
    # modal running, for blender in general, but it doesn't seem to be possible
    # show_blender_keymaps: bpy.props.BoolProperty(
    #     name="Show Blender Keymaps",
    #     default=False,
    #     description="Show Blender Keymaps",
    # )

    if TYPE_CHECKING:
        show_view_perspective: bpy.types.BoolProperty
    else:
        show_view_perspective: bpy.props.BoolProperty(
            name="Show View Perspective",
            default=True,
            description="Show View Perspective (perspective, orthographic, etc)",
        )

    if TYPE_CHECKING:
        show_object_mode: bpy.types.BoolProperty
    else:
        show_object_mode: bpy.props.BoolProperty(
            name="Show Object Mode",
            default=True,
            description="Show Object Mode (object, edit, pose, etc)",
        )

    if TYPE_CHECKING:
        show_object_name: bpy.types.BoolProperty
    else:
        show_object_name: bpy.props.BoolProperty(
            name="Show Object Type & Name",
            default=True,
            description="Show Object & Name",
        )

    if TYPE_CHECKING:
        show_vert_face_tris: bpy.types.BoolProperty
    else:
        show_vert_face_tris: bpy.props.BoolProperty(
            name="Show Vertex, Face, Triangle & Ngon counts",
            default=True,
            description="Show Vertex, Face, Triangle & Ngon counts",
        )

    if TYPE_CHECKING:
        show_object_info: bpy.types.BoolProperty
    else:
        show_object_info: bpy.props.BoolProperty(
            name="Show Modifiers",
            default=True,
            description="Show Modifiers",
        )

    if TYPE_CHECKING:
        show_parent: bpy.types.BoolProperty
    else:
        show_parent: bpy.props.BoolProperty(
            name="Show Parent",
            default=True,
            description="Show Parent",
        )

    if TYPE_CHECKING:
        show_loc_rot_scale: bpy.types.BoolProperty
    else:
        show_loc_rot_scale: bpy.props.BoolProperty(
            name="Show Location, Rotation & Scale",
            default=True,
            description="Show Location, Rotation & Scale",
        )

    if TYPE_CHECKING:
        flag_bad_transforms: bpy.types.BoolProperty
    else:
        flag_bad_transforms: bpy.props.BoolProperty(
            name="Flag Unapplied & Non-uniform Scaling",
            default=True,
            description="Flag Unapplied & Non-uniform Scaling (when modifiers are present)",
        )

    if TYPE_CHECKING:
        show_modifiers: bpy.types.BoolProperty
    else:
        show_modifiers: bpy.props.BoolProperty(
            name="Show Modifiers",
            default=True,
            description="Show Modifiers",
        )

    if TYPE_CHECKING:
        detailed_modifiers: bpy.types.BoolProperty
    else:
        detailed_modifiers: bpy.props.BoolProperty(
            name="Detailed Modifiers",
            default=True,
            description="Show Detailed Modifier Properties",
        )


    # Prefs for the actual text
    if TYPE_CHECKING:
        color_title: Tuple[bpy.types.FloatProperty, ...]
    else:
        color_title: bpy.props.FloatVectorProperty(
            name="",
            default=[1.0, 1.0, 1.0, 1.0],
            min=0.0, max=1.0, size=4,
            subtype='COLOR_GAMMA',
        )

    if TYPE_CHECKING:
        color_setting: Tuple[bpy.types.FloatProperty, ...]
    else:
        color_setting: bpy.props.FloatVectorProperty(
            name="",
            default=[0.5, 1.0, 0.0, 1.0],
            min=0.0, max=1.0, size=4,
            subtype='COLOR_GAMMA',
        )

    if TYPE_CHECKING:
        color_value: Tuple[bpy.types.FloatProperty, ...]
    else:
        color_value: bpy.props.FloatVectorProperty(
            name="",
            default=[0.0, 0.7, 1.0, 1.0],
            min=0.0, max=1.0, size=4,
            subtype='COLOR_GAMMA',
        )

    if TYPE_CHECKING:
        color_option: Tuple[bpy.types.FloatProperty, ...]
    else:
        color_option: bpy.props.FloatVectorProperty(
            name="",
            default=[1.0, 0.886, 0.2, 1.0],
            min=0.0, max=1.0, size=4,
            subtype='COLOR_GAMMA',
        )

    if TYPE_CHECKING:
        color_warning: Tuple[bpy.types.FloatProperty, ...]
    else:
        color_warning: bpy.props.FloatVectorProperty(
            name="",
            default=[1.0, 0.0, 0.0, 1.0],
            min=0, max=1, size=4,
            subtype='COLOR_GAMMA',
        )

    if TYPE_CHECKING:
        infotext_text_shadow: bpy.types.BoolProperty
    else:
        infotext_text_shadow: bpy.props.BoolProperty(
            name="Text Shadows",
            default=False,
            description="Text Shadows",
        )

    if TYPE_CHECKING:
        infotext_shadow_color: Tuple[bpy.types.FloatProperty, ...]
    else:
        infotext_shadow_color: bpy.props.FloatVectorProperty(
            name="",
            default=[0.0, 0.0, 0.0, 1.0],
            min=0.0, max=1.0, size=4,
            subtype='COLOR_GAMMA',
        )

    if TYPE_CHECKING:
        infotext_shadow_alpha: bpy.types.FloatProperty
    else:
        infotext_shadow_alpha: bpy.props.FloatProperty(
            name="",
            default=1.0,
            min=0.0, max=1.0,
        )

    if TYPE_CHECKING:
        infotext_offset_shadow_x: bpy.types.IntProperty
    else:
        infotext_offset_shadow_x: bpy.props.IntProperty(
            name="",
            default=2,
            min=-5, max=5,
        )

    if TYPE_CHECKING:
        infotext_offset_shadow_y: bpy.types.IntProperty
    else:
        infotext_offset_shadow_y: bpy.props.IntProperty(
            name="",
            default=-2,
            min=-5, max=5,
        )

    if TYPE_CHECKING:
        text_size_max: bpy.types.IntProperty
    else:
        text_size_max: bpy.props.IntProperty(
            name="",
            default=22,
            min=10, max=30,
            description="Maximal size of the text",
        )

    if TYPE_CHECKING:
        text_size_mini: bpy.types.IntProperty
    else:
        text_size_mini: bpy.props.IntProperty(
            name="",
            default=10,
            min=10, max=30,
            description="Minimal size when the window is smaller",
        )

    if TYPE_CHECKING:
        infotext_text_space: bpy.types.FloatProperty
    else:
        infotext_text_space: bpy.props.FloatProperty(
            name="",
            default=2.0,
            min=0.5, max=100.0,
            description="Space Between lines",
        )

    if TYPE_CHECKING:
        infotext_text_pos_y: bpy.types.IntProperty
    else:
        infotext_text_pos_y: bpy.props.IntProperty(
            name="",
            default=105,
            min=0, max=4000,
            description="Position of the text in Y",
        )

    if TYPE_CHECKING:
        infotext_text_pos_x: bpy.types.IntProperty
    else:
        infotext_text_pos_x: bpy.props.IntProperty(
            name="",
            default=20,
            min=0, max=4000,
            description="Position of the text in X",
        )

    # Hidden/calculated values
    # FIXME: Make sure the math here is sensical
    if TYPE_CHECKING:
        text_size_normal: bpy.types.IntProperty
    else:
        text_size_normal: bpy.props.IntProperty(
            name="",
            default=-1,
            description="Normal size for normal text",
            get=lambda s: min(s.text_size_max, max(
                s.text_size_mini, int(bpy.context.area.width / 100))),
        )

    if TYPE_CHECKING:
        text_size_large: bpy.types.IntProperty
    else:
        text_size_large: bpy.props.IntProperty(
            name="",
            default=-1,
            description="Large size for large text",
            get=lambda s: int(s.text_size_max * 1.5),
        )

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        # wm = bpy.context.window_manager
        # infotext = bpy.context.window_manager.infotext
        # icons = ui.load_icons()

        row = layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)

        # Info
        # if self.prefs_tabs == 'info':
        #     box = layout.box()
        #     split = box.split()
        #     col = split.column()
        #     col.label(text="This is a test addon text string")
        #     col.separator()
        #     col.label(text="more test text")
        #     col.label(text="and more test text")

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
                row.label(text="Show Object Parent")
                row.prop(self, "show_parent", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Show Object Transforms")
                row.prop(self, "show_loc_rot_scale", expand=True, text=" ")

                if self.show_loc_rot_scale:
                    row = box.row(align=True)
                    row.label(text="    Flag Problematic Transforms")
                    row.prop(self, "flag_bad_transforms", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Show Vert/Faces/Tris/Ngons")
                row.prop(self, "show_vert_face_tris", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Show Object Information")
                row.prop(self, "show_object_info", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Show Modifiers")
                row.prop(self, "show_modifiers", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Detailed Modifiers")
                row.prop(self, "detailed_modifiers", expand=True, text=" ")

                # row = box.row(align=True)
                # row.label(text="Show Blender Keymaps")
                # row.prop(self, "show_blender_keymaps", expand=True, text=" ")

                row = box.row(align=True)
                row.label(text="Title Text Color")
                row.prop(self, "color_title")

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
            box.label(text="Issues, bugs, etc:", icon='LINK_BLEND')
            z = box.operator("wm.url_open", text="Github")
            from tdvutil import alintrospect
            alintrospect(z)
            box.operator("wm.url_open",
                         text="Github").url = "https://www.github.com/alinsavix/blender-infotext"

            # box.separator()
            # box.label(text="Web:", icon='WORLD')
            # box.operator("wm.url_open", text="example.com").url = "http://www.example.com/"

            # box.separator()
            # box.label(text="Social:", icon='USER')
            # box.operator("wm.url_open", text="Twitter").url = "https://twitter.com/example"


CLASSES = [
    InfotextAddonPrefs
]

def register():
    for cls in CLASSES:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            print(f"{cls.__name__} already registred")

def unregister():
    for cls in CLASSES:
        try:
            bpy.utils.unregister_class(cls)
        except ValueError:
            print(f"{cls.__name__} already unregistred")
