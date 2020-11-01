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
import blf
# from ctypes import *
import math
# from math import degrees
from typing import *
from .functions import get_face_type_count, get_addon_preferences
from . import prefs

# from . import InfotextAddonPrefs
# import bmesh
# from .icon.icons import load_icons

# from os.path import dirname, join
# from . import png

infotext_text_Handle = []
TEXTURES = {}


# ----------------------------------------------------------------------
# DRAW ICONS
# ----------------------------------------------------------------------
# def load_texture(name, scale=1):
#     full_path = join(dirname(__file__), 'icon', 'modifiers', name)
#     img = png.Reader(full_path)
#     img.read()
#     img = img.asFloat()
#     content = list(img[2])
#     buf = bgl.Buffer(bgl.GL_FLOAT, [len(content), len(content[0])], content)
#
#     TEXTURES[name] = {'dimensions': [img[3]['size'][0], img[3]['size'][1]],
#                       'full_path': full_path, 'data': buf,
#                       'is_gl_initialised': False, 'scale': scale,
#                       'texture_id': 0}
#
#     return TEXTURES[name]
#
# def draw_icon(icon_name, location, size):
#     if not icon_name in TEXTURES:
#         load_texture(icon_name)
#
#     tex = TEXTURES[icon_name]
#
#     if not tex['is_gl_initialised']:
#
#         tex['texture_id'] = bgl.Buffer(bgl.GL_INT, [1])
#
#         bgl.glGenTextures(1, tex['texture_id'])
#
#         bgl.glBindTexture(bgl.GL_TEXTURE_2D, tex['texture_id'].to_list()[0])
#
#         bgl.glTexImage2D(bgl.GL_TEXTURE_2D, 0, bgl.GL_RGBA, tex['dimensions'][0],
#                          tex['dimensions'][1], 0, bgl.GL_RGBA, bgl.GL_FLOAT, tex['data'])
#         bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER, bgl.GL_NEAREST)
#         bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER, bgl.GL_NEAREST)
#         tex['is_gl_initialised'] = True
#     else:
#         bgl.glBindTexture(bgl.GL_TEXTURE_2D, tex['texture_id'].to_list()[0])
#
#     bgl.glColor4f(1, 1, 1, 1)
#     bgl.glEnable(bgl.GL_BLEND)
#     bgl.glEnable(bgl.GL_TEXTURE_2D)
#     bgl.glBegin(bgl.GL_QUADS)
#
#     coeff = tex['dimensions'][0] / size
#     iconWidth = tex['dimensions'][0] / coeff
#     iconHeight = tex['dimensions'][1] / coeff
#     x, y = location
#
#     # bottom left
#     bgl.glTexCoord2d(0, 1)
#     bgl.glVertex2d(x, y)
#
#     # top left
#     bgl.glTexCoord2d(0, 0)
#     bgl.glVertex2d(x, y + iconHeight)
#
#     # top right
#     bgl.glTexCoord2d(1, 0)
#     bgl.glVertex2d(x + iconWidth, y + iconHeight)
#
#     # bottom right
#     bgl.glTexCoord2d(1, 1)
#     bgl.glVertex2d(x + iconWidth, y)
#
#     bgl.glEnd()
#     bgl.glDisable(bgl.GL_TEXTURE_2D)
#     bgl.glDisable(bgl.GL_BLEND)


# ----------------------------------------------------------------------
# DRAW TEXT
# -----------------------------------------------------------------------
def infotext_draw_text_callback():
    addon_prefs = get_addon_preferences()
    # if addon_prefs.show_infotext and bpy.context.object is not None:
    if addon_prefs.show_infotext:
        infotext_draw_text_array(infotext_key_text(addon_prefs), addon_prefs)


def infotext_draw_text_array(output_text, p: prefs.InfotextAddonPrefs) -> None:
    font_id = 0
    x_offset = 0
    y_offset = 0

    # first_line_width = 0
    overlap = bpy.context.preferences.system.use_region_overlap
    t_panel_width = 0
    if overlap:
        for region in bpy.context.area.regions:
            if region.type == 'TOOLS':
                t_panel_width = region.width

    infotext_dpi = bpy.context.preferences.view.ui_scale

    text_size = min(p.text_size_max, max(p.text_size_mini, int(bpy.context.area.width / 100)))

    x = t_panel_width + (p.infotext_text_pos_x * infotext_dpi)
    y = bpy.context.region.height - (p.infotext_text_pos_y * infotext_dpi)

    # kinda lame that we use inline text strings as 'commands' but not worth
    # fixing right now.
    for command in output_text:
        if command == "SPACE" or command[0] == "SPACE":
            y_offset -= (text_size + p.infotext_text_space) / 2

        elif command == "CR" or command == "Carriage return":
            x_offset = 0
            y_offset -= text_size + p.infotext_text_space
            # space = int(text_size_max *5)

        elif len(command) == 3:
            Text, Color, Size = command
            # bgl.glColor3f(*Color)
            blf.color(0, *Color)
            blf.size(font_id, Size, 72)

            text_width, text_height = blf.dimensions(font_id, Text)
            if p.infotext_text_shadow:
                blf.enable(0, blf.SHADOW)
                blf.shadow_offset(0, p.infotext_offset_shadow_x, p.infotext_offset_shadow_y)
                blf.shadow(0, 3, p.infotext_shadow_color[0], p.infotext_shadow_color[1],
                           p.infotext_shadow_color[2], p.infotext_shadow_alpha)
            blf.position(font_id, (x + x_offset), (y + y_offset), 0)
            blf.draw(font_id, Text)
            x_offset += text_width

        # elif len(command) == 2 and command[0] == 'ICON':
        #     icon_size = int(text_size_max * 1.1)
        #     draw_icon(command[1], ((x + x_offset ), (y + y_offset)), icon_size)
        #

        else:
            print("Unknown command '%s' passed to infotext_draw_text_array" % (command))
            continue

    if p.infotext_text_shadow:
        blf.disable(0, blf.SHADOW)

    bpy.context.area.tag_redraw()


# utility function for floating point comparisons (needs python 3.6+)
def is_close(a, b, precision):
    return f'{a:.{precision}f}' == f'{b:.{precision}f}'


'''
# ---------------------------------------------------------------
# EXPERIMENTAL - ctypes to try to find out if a modal is running
# ---------------------------------------------------------------
# Handler type enum. Operator is 3
WM_HANDLER_TYPE_GIZMO = 1
WM_HANDLER_TYPE_UI = 2
WM_HANDLER_TYPE_OP = 3
WM_HANDLER_TYPE_DROPBOX = 4
WM_HANDLER_TYPE_KEYMAP = 5

# Generate listbase of appropriate type. None: generic


def listbase(type_=None):
    ptr = POINTER(type_)
    fields = ("first", ptr), ("last", ptr)
    return type("ListBase", (Structure,), {'_fields_': fields})


# Mini struct for Op handlers. *not* bContext!
class OpContext(Structure):
    pass


class wmEventHandler(Structure):  # Generic
    pass


class wmEventHandler_Op(Structure):  # Operator
    pass


class wmWindow(Structure):
    pass


wmEventHandler._fields_ = (
    ("next", POINTER(wmEventHandler)),
    ("prev", POINTER(wmEventHandler)),
    ("type", c_int),  # Enum
    ("flag", c_char),
    ("poll", c_void_p),
)

wmWindow._fields_ = (  # from DNA_windowmanager_types.h
    ("next", POINTER(wmWindow)),
    ("prev", POINTER(wmWindow)),
    ("ghostwin", c_void_p),
    ("gpuctx", c_void_p),
    ("parent", POINTER(wmWindow)),
    ("scene", c_void_p),
    ("new_scene", c_void_p),
    ("view_layer_name", c_char * 64),
    ("workspace_hook", c_void_p),
    ("global_areas", listbase(type_=None) * 3),
    ("screen", c_void_p),
    ("posx", c_short),
    ("posy", c_short),
    ("sizex", c_short),
    ("sizey", c_short),
    ("windowstate", c_short),
    ("monitor", c_short),
    ("active", c_short),
    ("cursor", c_short),
    ("lastcursor", c_short),
    ("modalcursor", c_short),
    ("grabcursor", c_short),
    ("addmousemove", c_short),
    ("winid", c_int),
    ("lock_pie_event", c_short),
    ("last_pie_event", c_short),
    ("eventstate", c_void_p),
    ("tweak", c_void_p),
    ("ime_data", c_void_p),
    ("queue", listbase(type_=None)),
    ("handlers", listbase(type_=None)),
    ("modalhandlers", listbase(type_=wmEventHandler)),
    ("gesture", listbase(type_=None)),
    ("stereo3d_format", c_void_p),
    ("drawcalls", listbase(type_=None)),
    ("cursor_keymap_status", c_void_p)
)

OpContext._fields_ = (
    ("win", POINTER(wmWindow)),
    ("area", c_void_p),  # <-- ScrArea ptr
    ("region", c_void_p),  # <-- ARegion ptr
    ("region_type", c_short)
)

wmEventHandler_Op._fields_ = (
    ("head", wmEventHandler),
    ("op", c_void_p),  # <-- wmOperator
    ("is_file_select", c_bool),
    ("context", OpContext)
)


def modal(output_text, p: prefs.InfotextAddonPrefs):
    window = bpy.context.window
    win = cast(window.as_pointer(), POINTER(wmWindow)).contents

    handle = win.modalhandlers.first
    while handle:
        if handle.contents.type == WM_HANDLER_TYPE_OP:
            output_text.extend([
                "CR",
                ("Modal Running", p.color_title, p.text_size_normal),
            ])
            break
        handle = handle.contents.next
    else:
        output_text.extend([
            "CR",
            ("No modal Running", p.color_title, p.text_size_normal)
        ])
        # print("No running modals")
'''

# ---------------------------------------------------------------
# VIEW
# ---------------------------------------------------------------


def r(x: Union[float, int]) -> float:
    return round(x, 3)


view_orientation_dict = {
    (0.0, 0.0, 0.0): 'Top',
    (r(-math.pi), 0.0, r(-math.pi)): 'Top',
    (r(-math.pi), 0.0, r(math.pi)): 'Top',
    (r(math.pi), 0.0, r(-math.pi)): 'Top',
    (r(math.pi), 0.0, r(math.pi)): 'Top',
    (0.0, 0.0, r(math.pi)): 'Top',  # 180 degree
    (0.0, 0.0, r(-math.pi / 2)): 'Top',  # 90 degree
    (0.0, 0.0, r(math.pi / 2)): 'Top',  # -90 degree

    #  (0.0, 0.0, 0.0): 'Bottom',  # 180 degree    ???
    (r(math.pi), 0.0, 0.0): 'Bottom',
    (r(math.pi), 0.0, r(math.pi / 2)): 'Bottom',  # 90 degree
    (r(-math.pi), 0.0, 0.0): 'Bottom',
    (r(-math.pi), 0.0, r(-math.pi / 2)): 'Bottom',  # -90 degree
    (0.0, r(-math.pi), 0.0): 'Bottom',

    (r(math.pi / 2), 0.0, 0.0): 'Front',
    (r(math.pi / 2), 0.0, r(math.pi)): 'Back',
    (r(math.pi / 2), 0.0, r(-math.pi / 2)): 'Left',
    (r(math.pi / 2), 0.0, r(math.pi / 2)): 'Right',
}

view_perspective_dict = {
    # "CAMERA": "Camera",
    "ORTHO": "Orthographic",
    "PERSP": "Perspective"
}


# Example outputs:
# Camera Perspective; User Orthographic; User Perspective; Bottom Perspective;
# Bottom Orthographic
#
# FIXME: The top/bottom/side orthographic views normally show the grid scale, too,
# probably
def view(output_text, p: prefs.InfotextAddonPrefs):
    rd = bpy.context.region_data

    if rd.view_perspective == "CAMERA":
        output_text.extend([
            "CR",
            ("Camera Perspective", p.color_title, p.text_size_normal),
        ])
    else:
        view_rot = rd.view_rotation.to_euler()
        # from pprint import pprint
        # print(pprint(tuple(map(r, view_rot))))
        # print(pprint(view_rot))

        # For figuring out what our perspective is, we don't care about what
        # the y rotation is. Just ignore it so we don't have to care
        x, y, z = tuple(map(r, view_rot))
        # print(x, y, z)
        # orientation = view_orientation_dict.get(tuple(map(r, view_rot)), 'User')
        orientation = view_orientation_dict.get(tuple([x, y, z]), 'User')
        perspective = view_perspective_dict.get(rd.view_perspective)

        # t = "%s %s (%0.3f %0.3f %0.3f %s)" % (orientation, perspective, x, y, z, view_rot.order)
        t = "%s %s" % (orientation, perspective)
        output_text.extend([
            "CR",
            (t, p.color_title, p.text_size_normal),
        ])


# ---------------------------------------------------------------
# MODE
# ---------------------------------------------------------------
mode_strings = {
    'OBJECT': 'OBJECT MODE',
    'EDIT_MESH': 'EDIT MODE',
    'EDIT_CURVE': 'EDIT MODE',
    'EDIT_SURFACE': 'EDIT MODE',
    'EDIT_TEXT': 'EDIT MODE',
    'EDIT_ARMATURE': 'EDIT MODE',
    'EDIT_METABALL': 'EDIT MODE',
    'EDIT_LATTICE': 'EDIT MODE',
    'POSE': 'POSE MODE',
    'SCULPT': 'SCULPT MODE',
    'PAINT_WEIGHT': 'WEIGHT PAINT MODE',
    'PAINT_VERTEX': 'VERTEX PAINT MODE',
    'PAINT_TEXTURE': 'TEXTURE PAINT MODE',
    'PARTICLE': 'PARTICLE EDIT MODE',
    'EDIT_GPENCIL': 'EDIT MODE',  # FIXME: should this mention gpencil?
    'PAINT GPENCIL': 'GR.PENCIL PAINT MODE',
    'SCULPT_GPENCIL': 'GR.PENCIL SCULPT MODE',
    'WEIGHT_GPENCIL': 'GR.PENCIL WEIGHT MODE',  # should this have 'paint' in the string?
    'VERTEX_GPENCIL': 'GR.PENCIL VERTEX MODE',  # should this have 'paint' in the string?
    'default': 'UNKNOWN MODE',
}


def mode(output_text, p: prefs.InfotextAddonPrefs):
    mode = bpy.context.mode

    if mode in mode_strings:
        output_text.extend([
            "CR",
            (mode_strings[mode], p.color_title, p.text_size_large),
        ])
    else:
        output_text.extend([
            "CR",
            (mode_strings['default'], p.color_title, p.text_size_large),
        ])

    # Icons, just in case we figure out how to use them again
    # output_text.extend(["CR", ('ICON', 'ICON_OBJECT_DATAMODE.png'), ("   OBJECT MODE", p.color_title, p.text_size_deux)])
    # output_text.extend(["CR", ('ICON', 'ICON_EDITMODE_HLT.png'), ("   EDIT MODE", p.color_title, p.text_size_deux)])
    # output_text.extend(["CR", ('ICON', 'ICON_SCULPTMODE_HLT.png'), ("   SCULPT MODE", p.color_title, p.text_size_deux)])
    # output_text.extend(["CR", ('ICON', 'ICON_VPAINT_HLT.png'), ("    VERTEX PAINT MODE", p.color_title, p.text_size_deux)])
    # output_text.extend(["CR", ('ICON', 'ICON_WPAINT_HLT.png'), ("    WEIGHT PAINT MODE", p.color_title, p.text_size_deux)])
    # output_text.extend(["CR", ('ICON', 'ICON_TPAINT_HLT.png'), ("    TEXTURE PAINT MODE", p.color_title, p.text_size_deux)])
    # output_text.extend(["CR", ('ICON', 'ICON_PARTICLEMODE.png'), ("    PARTICLES EDIT MODE", p.color_title, p.text_size_deux)])
   # output_text.extend(["CR", ('ICON', 'ICON_POSE_HLT.png'), ("    POSE MODE", p.color_title, p.text_size_deux)])
    # output_text.extend(
    # ["CR", ('ICON', 'ICON_OBJECT_DATAMODE.png'), ("    ", p.color_setting, p.text_size_normal)])


# ---------------------------------------------------------------
# NAME
# ---------------------------------------------------------------


def name(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object) -> None:
    # obj = bpy.context.active_object

    output_text.extend([
        "CR",
        ("", p.color_setting, int(p.text_size_normal * 5)),
        "CR",
        # (obj.type + ": ", p.color_title, p.text_size_normal),
        (obj.type, p.color_title, p.text_size_normal),
        "CR",
        "CR",
        (obj.name, p.color_value, int(p.text_size_large * 1.5)),
        "CR",
    ])

    # output_text.extend(["CR", (obj.type, p.color_title, p.text_size_normal)])
    # output_text.extend(["CR", ("Name: ", p.color_title, p.text_size_normal), (obj.name, p.color_value, p.text_size_normal)])

    # FIXME: enable icons once icon code is enabled
    # if obj.type == 'MESH':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_MESH.png'), ("    ", p.color_setting, p.text_size_normal)])
    #     output_text.extend(["CR", ("    ", p.color_setting, p.text_size_normal), (obj.name, p.color_value, p.text_size_normal)])
    # elif obj.type == 'CURVE':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_CURVE.png'), ("    ", p.color_setting, p.text_size_normal)])
    #     output_text.extend(["CR", ("    ", p.color_setting, p.text_size_normal), (obj.name, p.color_value, p.text_size_normal)])
    # elif obj.type == 'EMPTY':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_EMPTY.png'), ("    ", p.color_setting, p.text_size_normal)])
    #     output_text.extend(["CR", ("    ", p.color_setting, p.text_size_normal), (obj.name, p.color_value, p.text_size_normal)])

    # elif obj.type == 'CAMERA':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_CAMERA.png'), ("     ", p.color_setting, p.text_size_normal)])
    #     output_text.extend(["CR", ("     ", p.color_setting, p.text_size_normal), (obj.name, p.color_value, p.text_size_normal)])

    # elif obj.type == 'LATTICE':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_LATTICE.png'), ("     ", p.color_setting, p.text_size_normal)])
    #     output_text.extend(["CR", ("     ", p.color_setting, p.text_size_normal), (obj.name, p.color_value, p.text_size_normal)])

    # elif obj.type == 'META':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_META.png'), ("    ", p.color_setting, p.text_size_normal)])
    #     output_text.extend(["CR", ("    ", p.color_setting, p.text_size_normal), (obj.name, p.color_value, p.text_size_normal)])

    # elif obj.type == 'ARMATURE':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_ARMATURE.png'), ("    ", p.color_setting, p.text_size_normal)])
    #     output_text.extend(["CR", ("    ", p.color_setting, p.text_size_normal), (obj.name, p.color_value, p.text_size_normal)])

    # elif obj.type == 'FONT':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_FONT.png'), ("     ", p.color_setting, p.text_size_normal)])
    #     output_text.extend(["CR", ("     ", p.color_setting, p.text_size_normal), (obj.name, p.color_value, p.text_size_normal)])

    # elif obj.type == 'LATTICE':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_LATTICE.png'), ("    ", p.color_setting, p.text_size_normal)])
    #     output_text.extend(["CR", ("    ", p.color_setting, p.text_size_normal), (obj.name, p.color_value, p.text_size_normal)])

    # elif obj.type == 'LAMP':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_LAMP.png'), ("    ", p.color_setting, p.text_size_normal)])
    #     output_text.extend(["CR", ("    ", p.color_setting, p.text_size_normal), (obj.name, p.color_value, p.text_size_normal)])

    # elif obj.type == 'SURFACE':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_SURFACE.png'), ("    ", p.color_setting, p.text_size_normal)])
    #     output_text.extend(["CR", ("    ", p.color_setting, p.text_size_normal), (obj.name, p.color_value, p.text_size_normal)])

    # elif obj.type == 'SPEAKER':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_SPEAKER.png'), ("    ", p.color_setting, p.text_size_normal)])
    #     output_text.extend(["CR", ("    ", p.color_setting, p.text_size_normal), (obj.name, p.color_value, p.text_size_normal)])


# ---------------------------------------------------------------
# LOCATION / ROTATION / SCALE
# ---------------------------------------------------------------


def loc(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, units) -> None:
    # obj = bpy.context.active_object

    axis_list = (" X ", " Y ", " Z ")
    # LOCATION
    if tuple(obj.location) != (0.0, 0.0, 0.0):
        # output_text.extend(["CR",("LOCATION ", p.color_title, p.text_size_normal),
        #                   ("  %s" % round(obj.location[0], 2), p.color_value, p.text_size_normal), (units, p.color_value, p.text_size_normal),
        #                   ("  %s" % round(obj.location[1], 2), p.color_value, p.text_size_normal), (units, p.color_value, p.text_size_normal),
        #                   ("  %s" % round(obj.location[2], 2), p.color_value, p.text_size_normal), (units, p.color_value, p.text_size_normal)])

        # output_text.extend(["CR", ('ICON', 'ICON_MAN_TRANS.png'), ("    ", p.color_title, p.text_size_normal)])
        output_text.extend([
            "CR",
            ("L: ", p.color_title, p.text_size_normal),
        ])

        for idx, axis in enumerate(axis_list):
            output_text.extend([
                (axis, p.color_setting, p.text_size_normal),
                (str(round(obj.location[idx], 2)), p.color_value, p.text_size_normal),
                (units, p.color_value, p.text_size_normal)
            ])

    # ROTATION
    if tuple(obj.rotation_euler) != (0.0, 0.0, 0.0):
        # output_text.extend(["CR", ('ICON', 'ICON_MAN_ROT.png'), ("    ", p.color_title, p.text_size_normal)])
        output_text.extend(["CR", ("R: ", p.color_title, p.text_size_normal)])

        for idx, axis in enumerate(axis_list):
            output_text.extend([
                (axis, p.color_setting, p.text_size_normal),
                (str(round(math.degrees(obj.rotation_euler[idx]), 2)), p.color_value, p.text_size_normal),
                ("°", p.color_value, p.text_size_normal)
            ])

    # SCALE
    if tuple(obj.scale) != (1, 1, 1):
        # output_text.extend(["CR", ('ICON', 'ICON_MAN_SCALE.png'), ("    ", p.color_title, p.text_size_normal)])
        output_text.extend([
            "CR",
            ("S: ", p.color_title, p.text_size_normal),
        ])

        for idx, axis in enumerate(axis_list):
            output_text.extend([
                (axis, p.color_setting, p.text_size_normal),
                (str(round(obj.scale[idx], 2)), p.color_value, p.text_size_normal),
            ])

        if not is_close(obj.scale[0], obj.scale[1], 3) or not is_close(obj.scale[1], obj.scale[2], 3):
            output_text.extend([
                (" Non-uniform ", p.color_warning, p.text_size_normal),
            ])

    if any([tuple(obj.location) != (0.0, 0.0, 0.0), tuple(obj.rotation_euler) != (0.0, 0.0, 0.0), tuple(obj.scale) != (1, 1, 1)]):
        # SPACE
        output_text.extend(["SPACE"])

# ---------------------------------------------------------------
# NGONS
# ---------------------------------------------------------------


def ngons(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object) -> None:
    # obj = bpy.context.active_object
    # WM = bpy.context.window_manager.infotext_properties
    infotext = bpy.context.window_manager.infotext

    if not infotext.face_type_count:
        get_face_type_count(infotext, obj)

    # tcount = infotext_properties.face_type_count['TRIS']
    # ncount = infotext_properties.face_type_count['NGONS']
    vcount = len(obj.data.vertices)
    fcount = len(obj.data.polygons)
    ecount = len(obj.data.edges)

    # VERTEX
    # output_text.extend(["CR", ('ICON', 'vert.png'), ("    ", p.color_title, p.text_size_normal),
    #                   (str(vcount), p.color_value, p.text_size_normal)])
    output_text.extend([
        "CR",
        ("V: ", p.color_title, p.text_size_normal),
        (str(vcount), p.color_value, p.text_size_normal),
    ])

    # EDGES
    # output_text.extend([("  ", p.color_title, p.text_size_normal), ('ICON', 'edge.png'), ("    ", p.color_title, p.text_size_normal),
    #                   (str(ecount), p.color_value, p.text_size_normal)])
    output_text.extend([
        ("  E: ", p.color_title, p.text_size_normal),
        (" ", p.color_title, p.text_size_normal),
        (str(ecount), p.color_value, p.text_size_normal),
    ])

    # FACES
    # output_text.extend([("  ", p.color_title, p.text_size_normal), ('ICON', 'face.png'), ("    ", p.color_title, p.text_size_normal),
    #                   (str(fcount), p.color_value, p.text_size_normal)])
    output_text.extend([
        ("  F: ", p.color_title, p.text_size_normal),
        (" ", p.color_title, p.text_size_normal),
        (str(fcount), p.color_value, p.text_size_normal),
    ])

    # FIXME: Make sure this is ok in all cases
    # if not bpy.context.object.mode == 'SCULPT':
    if not obj.mode == 'SCULPT':
        tcount = infotext.face_type_count['TRIS']
        ncount = infotext.face_type_count['NGONS']
        # TRIS
        if tcount:
            # output_text.extend([("  ", p.color_title, p.text_size_normal), ('ICON', 'triangle.png'), ("    ", p.color_title, p.text_size_normal),
            #                   (str(tcount), p.color_value, p.text_size_normal)])

            output_text.extend([
                ("  T: ", p.color_title, p.text_size_normal),
                (" ", p.color_title, p.text_size_normal),
                (str(tcount), p.color_value, p.text_size_normal),
            ])

        # NGONS ICON_OBJECT_DATA
        if ncount:
            # output_text.extend([(" ", p.color_title, p.text_size_normal), ('ICON', 'ngons.png'),
            #                   ("     ", p.color_title, p.text_size_normal), (str(ncount), p.color_value, p.text_size_normal)])

            output_text.extend([
                ("  N: ", p.color_title, p.text_size_normal),
                (" ", p.color_title, p.text_size_normal),
                (str(ncount), p.color_value, p.text_size_normal),
            ])

# ---------------------------------------------------------------
# MESH OPTIONS
# ---------------------------------------------------------------


def mesh_options(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object) -> None:
    # obj = bpy.context.active_object

    # from ppretty import ppretty
    # import pprint
    # pp = pprint.PrettyPrinter(indent=4, depth=5)
    # print("object:")
    # print(ppretty(bpy.context.object, depth=2, seq_length=100))
    # , depth=10, seq_length=50, show_protected=True,
    #               show_private=True, show_static=True, show_properties=True))
    # print("active_object:")
    # print(ppretty(bpy.context.active_object))

    # MATERIALS
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        if obj.material_slots:
            if obj.active_material:
                # output_text.extend(["CR", ('ICON', 'ICON_SMOOTH.png'),("     ", p.color_title, p.text_size_normal)])
                output_text.extend([
                    "CR",
                    ("MATERIAL: ", p.color_title, p.text_size_normal),
                ])
                output_text.extend([
                    (str(len(obj.material_slots)), p.color_setting, p.text_size_normal),
                    (" ", p.color_title, p.text_size_normal),
                    (str(obj.active_material.name), p.color_value, p.text_size_normal),
                ])

                if obj.active_material.users >= 2:
                    output_text.extend([
                        (" ", p.color_setting, p.text_size_normal),
                        (str(obj.active_material.users), p.color_setting, p.text_size_normal),
                        (" users", p.color_setting, p.text_size_normal),
                    ])
                if obj.active_material.use_fake_user:
                    output_text.extend([(" ,FAKE USER ", p.color_setting, p.text_size_normal)])
            else:
                output_text.extend(["CR", ("SLOT ONLY", p.color_title, p.text_size_normal)])

            # SPACE
            output_text.extend(["SPACE"])

    if obj.type == 'MESH':
        # AUTOSMOOTH
        if obj.data.use_auto_smooth:
            output_text.extend([
                "CR",
                ("AUTOSMOOTH ", p.color_title, p.text_size_normal),
            ])
            # ANGLE
            output_text.extend([
                (" ANGLE ", p.color_setting, p.text_size_normal),
                (str(round(math.degrees(obj.data.auto_smooth_angle), 1)), p.color_value, p.text_size_normal),
                ("°", p.color_value, p.text_size_normal),
            ])

    if obj.type in ['MESH', 'LATTICE']:
        # VERTEX GROUPS
        if obj.vertex_groups:
            output_text.extend([
                "CR",
                ("VERTEX GROUPS", p.color_title, p.text_size_normal),
            ])
            output_text.extend([
                (" ", p.color_title, p.text_size_normal),
                (str(len(obj.vertex_groups)), p.color_setting, p.text_size_normal),
            ])
            output_text.extend([
                (" ", p.color_title, p.text_size_normal),
                (str(obj.vertex_groups[int(obj.vertex_groups.active_index)].name), p.color_value, p.text_size_normal),
            ])

    if obj.type in ['CURVE', 'MESH', 'LATTICE']:
        # SHAPE KEYS
        if obj.data.shape_keys:
            output_text.extend(["CR", ("SHAPE KEYS", p.color_title, p.text_size_normal)])
            output_text.extend([
                (" ", p.color_title, p.text_size_normal),
                (str(len(obj.data.shape_keys.key_blocks)), p.color_setting, p.text_size_normal),
            ])
            output_text.extend([
                (" ", p.color_title, p.text_size_normal),
                (str(obj.data.shape_keys.key_blocks[int(
                    bpy.context.object.active_shape_key_index)].name), p.color_value, p.text_size_normal),
            ])

            if bpy.context.object.mode == 'OBJECT':
                output_text.extend([
                    (" VALUE ", p.color_setting, p.text_size_normal),
                    (str(round(obj.data.shape_keys.key_blocks[int(
                        bpy.context.object.active_shape_key_index)].value, 3)), p.color_value, p.text_size_normal),
                ])

    if obj.type == 'MESH':
        # UV's
        if obj.data.uv_layers:
            output_text.extend(["CR", ("UV's", p.color_title, p.text_size_normal)])
            output_text.extend([
                (" ", p.color_title, p.text_size_normal),
                (str(len(obj.data.uv_layers)), p.color_setting, p.text_size_normal),
            ])
            output_text.extend([
                (" ", p.color_title, p.text_size_normal),
                (str(
                    obj.data.uv_layers[int(obj.data.uv_layers.active_index)].name), p.color_value, p.text_size_normal),
            ])

        # VERTEX COLORS
        if obj.data.vertex_colors:
            output_text.extend(["CR", ("VERTEX COLORS", p.color_title, p.text_size_normal)])
            output_text.extend([
                (" ", p.color_title, p.text_size_normal),
                (str(len(obj.data.vertex_colors)), p.color_setting, p.text_size_normal),
            ])
            output_text.extend([
                (" ", p.color_title, p.text_size_normal),
                (str(obj.data.vertex_colors[int(obj.data.vertex_colors.active_index)].name),
                 p.color_value, p.text_size_normal),
            ])

    if obj.type == 'LATTICE':
        if any([obj.vertex_groups, obj.data.shape_keys]):
            # SPACE
            output_text.extend(["SPACE"])

    if obj.type in ['CURVE', 'FONT']:
        if any([obj.vertex_groups, obj.data.shape_keys]):
            # SPACE
            output_text.extend(["SPACE"])

    if obj.type == 'MESH':
        if any([obj.data.use_auto_smooth, obj.vertex_groups, obj.data.shape_keys, obj.data.uv_layers, obj.data.vertex_colors]):
            # SPACE
            output_text.extend(["SPACE"])

# ---------------------------------------------------------------
# SCULPT
# ---------------------------------------------------------------


def sculpt(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, units) -> None:
    # obj = bpy.context.active_object
    toolsettings = bpy.context.tool_settings
    sculpt = toolsettings.sculpt
    context_tool = bpy.context.scene.tool_settings.sculpt

    # BRUSH
    brush = bpy.context.tool_settings.sculpt.brush
    capabilities = brush.sculpt_capabilities
    ups = bpy.context.tool_settings.unified_paint_settings

    # bpy.ops.paint.brush_select(sculpt_tool='GRAB')

    # SPACE
    output_text.extend(["SPACE"])

    # if bpy.types.Brush == 'GRAB':
    # output_text.extend(["CR", ('ICON', 'grab.png'), ("    ", p.color_setting, p.text_size_normal)])

    output_text.extend(["CR", (str(brush.name.upper()), p.color_title, p.text_size_large)])

    # SPACE
    output_text.extend(["SPACE"])

    # RADIUS
    output_text.extend([
        "CR",
        ("RADIUS ", p.color_setting, p.text_size_normal),
        (str(round(ups.size, 2)), p.color_value, p.text_size_normal),
        (" px", p.color_value, p.text_size_normal),
    ])
    # STRENGTH
    output_text.extend([
        "CR",
        ("STRENGTH ", p.color_setting, p.text_size_normal),
        (str(round(brush.strength, 3)), p.color_value, p.text_size_normal),
    ])

    # STRENGTH
    brush_autosmooth = bpy.data.brushes[brush.name].auto_smooth_factor
    if brush_autosmooth:
        output_text.extend([
            "CR",
            ("AUTOSMOOTH ", p.color_setting, p.text_size_normal),
            (str(round(brush_autosmooth, 3)), p.color_value, p.text_size_normal),
        ])

    brush_use_frontface = bpy.data.brushes[brush.name].use_frontface
    if bpy.data.brushes[brush.name].use_frontface:
        output_text.extend([
            "CR",
            ("FRONT FACE ", p.color_setting, p.text_size_normal),
            (str(brush_use_frontface), p.color_value, p.text_size_normal),
        ])

    # brush_stroke_method = bpy.data.brushes[brush.name].stroke_method
    # if brush_stroke_method == 'SPACE':
    #     output_text.extend(["CR", ("STROKE METHOD ", p.color_setting, p.text_size_normal)])
    #     output_text.extend(["SPACE"])
    # else:
    #     output_text.extend(["CR", ("STROKE METHOD ", p.color_setting, p.text_size_normal),
    #                       (str(brush_stroke_method), p.color_value, p.text_size_normal)])

    # SPACE
    output_text.extend(["SPACE"])

    # FIXME: Should we be accessing this from the context, or just the active object?
    if bpy.context.sculpt_object.use_dynamic_topology_sculpting:
        # SPACE
        output_text.extend(["SPACE"])

        # DYNTOPO
        output_text.extend(["CR", ("DYNTOPO ", p.color_title, p.text_size_large)])
        # SPACE
        output_text.extend(["SPACE"])

        if context_tool.detail_type_method == 'CONSTANT':
            output_text.extend([
                "CR",
                ("CONSTANT DETAIL ", p.color_setting, p.text_size_normal),
                (str(round(context_tool.constant_detail_resolution, 2)), p.color_value, p.text_size_normal),
            ])

        elif context_tool.detail_type_method == 'RELATIVE':
            output_text.extend([
                "CR",
                ("RELATIVE DETAIL ", p.color_setting, p.text_size_normal),
                (str(round(context_tool.detail_size, 2)), p.color_value, p.text_size_normal),
                (" px", p.color_value, p.text_size_normal),
            ])

        else:
            output_text.extend([
                "CR",
                ("BRUSH DETAIL ", p.color_setting, p.text_size_normal),
                (str(round(context_tool.detail_percent, 2)), p.color_value, p.text_size_normal),
                ("%", p.color_value, p.text_size_normal),
            ])

        # SUBDIV METHOD

        # SUBDIVIDE_COLLAPSE
        if context_tool.detail_refine_method == 'SUBDIVIDE_COLLAPSE':
            output_text.extend([
                "CR",
                (str("SUBDIVIDE COLLAPSE"), p.color_setting, p.text_size_normal),
            ])

        # COLLAPSE
        elif context_tool.detail_refine_method == 'COLLAPSE':
            output_text.extend(["CR", (str("COLLAPSE"), p.color_setting, p.text_size_normal)])

        # SUBDIVIDE
        else:
            output_text.extend(["CR", (str("SUBDIVIDE"), p.color_setting, p.text_size_normal)])

        # SMOOTH SHADING
        if context_tool.use_smooth_shading:
            output_text.extend(["CR", (str("SMOOTH SHADING"), p.color_value, p.text_size_normal)])

        # SYMMETRIZE DIRECTION
        output_text.extend([
            "CR",
            (str("SYMMETRIZE "), p.color_setting, p.text_size_normal),
            (str(context_tool.symmetrize_direction.lower().capitalize()), p.color_value, p.text_size_normal),
        ])

        # SPACE
        output_text.extend(["SPACE"])

    # SYMMETRIZE
    if any([context_tool.use_symmetry_x, context_tool.use_symmetry_y, context_tool.use_symmetry_z]):
        output_text.extend(["CR", (str("MIRROR"), p.color_setting, p.text_size_normal)])
        if context_tool.use_symmetry_x:
            output_text.extend([(str(" X "), p.color_value, p.text_size_normal)])
        if context_tool.use_symmetry_y:
            output_text.extend([(str(" Y "), p.color_value, p.text_size_normal)])
        if context_tool.use_symmetry_z:
            output_text.extend([(str(" Z "), p.color_value, p.text_size_normal)])

    if context_tool.use_symmetry_feather:
        output_text.extend(["CR", (str("FEATHER "), p.color_title, p.text_size_normal)])

    # LOCK
    if any([context_tool.lock_x, context_tool.lock_y, context_tool.lock_z]):
        output_text.extend(["CR", (str("LOCK  "), p.color_setting, p.text_size_normal)])
        if context_tool.lock_x:
            output_text.extend([(str(" X "), p.color_value, p.text_size_normal)])
        if context_tool.lock_y:
            output_text.extend([(str(" Y "), p.color_value, p.text_size_normal)])
        if context_tool.lock_z:
            output_text.extend([(str(" Z "), p.color_value, p.text_size_normal)])

    # TILE
    if any([context_tool.tile_x, context_tool.tile_y, context_tool.tile_z]):
        output_text.extend(["CR", (str("TILE    "), p.color_setting, p.text_size_normal)])
        if context_tool.tile_x:
            output_text.extend([(str(" X "), p.color_value, p.text_size_normal)])
        if context_tool.tile_y:
            output_text.extend([(str(" Y "), p.color_value, p.text_size_normal)])
        if context_tool.tile_z:
            output_text.extend([(str(" Z "), p.color_value, p.text_size_normal)])

# ----------------------------------------------------------------------
# MODIFIERS
# ----------------------------------------------------------------------

# ---------------------------------------------------------------
# ARRAY
# ---------------------------------------------------------------


def mod_array(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
              mod: bpy.types.ArrayModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR",('ICON', 'ICON_MOD_ARRAY.png'),("    ", p.color_setting, p.text_size_normal), (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # FIT MODE
                if mod.fit_type == 'FIXED_COUNT':
                    output_text.extend([
                        (" Count ", p.color_setting, p.text_size_normal),
                        (str(mod.count), p.color_value, p.text_size_normal),
                    ])

                elif mod.fit_type == 'FIT_CURVE':
                    if mod.curve:
                        # Object
                        output_text.extend([
                            (" Curve ", p.color_setting, p.text_size_normal),
                            (mod.curve.name, p.color_value, p.text_size_normal),
                        ])
                    else:
                        output_text.extend([(" No Curve Selected", p.color_warning, p.text_size_normal)])

                else:
                    output_text.extend([
                        (" Length ", p.color_setting, p.text_size_normal),
                        (str(round(mod.fit_length, 2)), p.color_value, p.text_size_normal),
                    ])

                # CONSTANT
                if mod.use_constant_offset:
                    # output_text.extend([(" Constant ", p.color_setting, p.text_size_normal),
                    #                   ("%s" %round(mod.constant_offset_displace[0], 1),color_value, p.text_size_normal),
                    #                   ("  %s" %round(mod.constant_offset_displace[1], 1),color_value, p.text_size_normal),
                    #                   ("  %s" %round(mod.constant_offset_displace[2], 1),color_value, p.text_size_normal)])

                    output_text.extend([(" Constant ", p.color_setting, p.text_size_normal)])

                    # X
                    if mod.constant_offset_displace[0] != 0:
                        output_text.extend([
                            (" X ", p.color_setting, p.text_size_normal),
                            (str(round(mod.constant_offset_displace[0], 1)), p.color_value, p.text_size_normal),
                            (units, p.color_value, p.text_size_normal),
                        ])

                    # Y
                    if mod.constant_offset_displace[1] != 0:
                        output_text.extend([
                            (" Y ", p.color_setting, p.text_size_normal),
                            (str(round(mod.constant_offset_displace[1], 1)), p.color_value, p.text_size_normal),
                            (units, p.color_value, p.text_size_normal),
                        ])

                    # Z
                    if mod.constant_offset_displace[2] != 0:
                        output_text.extend([
                            (" Z ", p.color_setting, p.text_size_normal),
                            (str(round(mod.constant_offset_displace[2], 1)), p.color_value, p.text_size_normal),
                            (units, p.color_value, p.text_size_normal),
                        ])

                # RELATIVE
                elif mod.use_relative_offset:
                    output_text.extend([(" Relative ", p.color_setting, p.text_size_normal)])

                    # X
                    if mod.relative_offset_displace[0] != 0:
                        output_text.extend([
                            (" X ", p.color_setting, p.text_size_normal),
                            (str(round(mod.relative_offset_displace[0], 1)), p.color_value, p.text_size_normal),
                        ])

                    # Y
                    if mod.relative_offset_displace[1] != 0:
                        output_text.extend([
                            (" Y ", p.color_setting, p.text_size_normal),
                            (str(round(mod.relative_offset_displace[1], 1)), p.color_value, p.text_size_normal),
                        ])

                    # Z
                    if mod.relative_offset_displace[2] != 0:
                        output_text.extend([
                            (" Z ", p.color_setting, p.text_size_normal),
                            (str(round(mod.relative_offset_displace[2], 1)), p.color_value, p.text_size_normal),
                        ])

                # MERGE
                if mod.use_merge_vertices:
                    output_text.extend([
                        (" Merge ", p.color_setting, p.text_size_normal),
                        (str(round(mod.merge_threshold, 3)), p.color_value, p.text_size_normal),
                    ])

                    if mod.use_merge_vertices_cap:
                        output_text.extend([(" First Last ", p.color_setting, p.text_size_normal)])

                # OPTIONS
                if any([mod.use_object_offset, mod.start_cap, mod.end_cap]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # OBJECT OFFSET
                    if mod.use_object_offset:
                        if mod.offset_object:
                            output_text.extend([
                                (" Object Offset ", p.color_setting, p.text_size_normal),
                                (mod.offset_object.name, p.color_value, p.text_size_normal),
                            ])
                        else:
                            output_text.extend([
                                (" No Object Selected", p.color_warning, p.text_size_normal),
                            ])

                    # STAR CAP
                    if mod.start_cap:
                        output_text.extend([
                            (" Start Cap ", p.color_setting, p.text_size_normal),
                            (mod.start_cap.name, p.color_value, p.text_size_normal),
                        ])

                    # END CAP
                    if mod.end_cap:
                        output_text.extend([
                            (" End Cap ", p.color_setting, p.text_size_normal),
                            (mod.end_cap.name, p.color_value, p.text_size_normal),
                        ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])


# ---------------------------------------------------------------
# BEVEL
# ---------------------------------------------------------------
def mod_bevel(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
              mod: bpy.types.BevelModifier, units) -> None:
    # FIXME: Should we take WM as an argument, too?
    wm = bpy.context.window_manager
    # obj = bpy.context.active_object

    if obj.type in {'MESH', 'CURVE', 'FONT'}:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_BEVEL.png'),
        #   ("     ", p.color_setting, p.text_size_normal),
        #   (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # AFFECT
                output_text.extend([
                    (" Affect ", p.color_setting, p.text_size_normal),
                    (mod.affect, p.color_value, p.text_size_normal),
                ])

                # OFFSET TYPE
                output_text.extend([
                    (" Method ", p.color_setting, p.text_size_normal),
                    (str(mod.offset_type.lower().capitalize()), p.color_value, p.text_size_normal),
                ])

                # WIDTH
                output_text.extend([
                    (" Width ", p.color_setting, p.text_size_normal),
                    (str(round(mod.width, 2)), p.color_value, p.text_size_normal),

                ])

                if mod.offset_type == "PERCENT":
                    output_text.extend([
                        ("%", p.color_value, p.text_size_normal),
                    ])
                else:
                    output_text.extend([
                        (units, p.color_value, p.text_size_normal),
                    ])

                # SEGMENTS
                output_text.extend([
                    (" Segments ", p.color_setting, p.text_size_normal),
                    (str(mod.segments), p.color_value, p.text_size_normal),
                ])

                # PROFILE
                output_text.extend([
                    (" Profile ", p.color_setting, p.text_size_normal),
                    (str(round(mod.profile, 2)), p.color_value, p.text_size_normal),
                ])

                # FIXME: Support material index
                # MATERIAL
                # output_text.extend([])

                # OPTIONS
                output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                # LIMIT METHOD
                output_text.extend([
                    (" Limit ", p.color_setting, p.text_size_normal),
                    (str(mod.limit_method.lower().capitalize()), p.color_value, p.text_size_normal),
                ])

                # ANGLE
                if mod.limit_method == 'ANGLE':
                    output_text.extend([
                        (":", p.color_setting, p.text_size_normal),
                        (str(round(math.degrees(mod.angle_limit), 2)), p.color_value, p.text_size_normal),
                        ("°", p.color_value, p.text_size_normal),
                    ])

                # VERTEX GROUP
                elif mod.limit_method == 'VGROUP':
                    if mod.vertex_group:
                        output_text.extend([
                            (":", p.color_setting, p.text_size_normal),
                            (str(mod.vertex_group), p.color_value, p.text_size_normal),
                        ])
                    else:
                        output_text.extend([
                            (":", p.color_setting, p.text_size_normal),
                            ("None", p.color_warning, p.text_size_normal),
                        ])

                # LOOP SLIDE
                if mod.loop_slide:
                    output_text.extend([(" Loop Slide ", p.color_setting, p.text_size_normal)])

                # CLAMP
                if mod.use_clamp_overlap:
                    output_text.extend([(" Clamp ", p.color_setting, p.text_size_normal)])

                # HARDEN NORMALS
                if mod.harden_normals:
                    output_text.extend([(" Harden ", p.color_setting, p.text_size_normal)])

                if mod.mark_seam:
                    output_text.extend([(" Mark Seam ", p.color_setting, p.text_size_normal)])

                if mod.mark_sharp:
                    output_text.extend([(" Mark Sharp ", p.color_setting, p.text_size_normal)])

                # ONLY VERTICES
                # if mod.use_only_vertices:
                #     output_text.extend([(" Only Vertices ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# BOOLEAN
# ---------------------------------------------------------------


def mod_boolean(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                mod: bpy.types.BooleanModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_BOOLEAN.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # OPERATION
                output_text.extend([
                    (" ", p.color_title, p.text_size_normal),
                    (str(mod.operation), p.color_value, p.text_size_normal),
                ])
                if mod.object:
                    # Object
                    output_text.extend([
                        (" Object ", p.color_setting, p.text_size_normal),
                        (mod.object.name, p.color_value, p.text_size_normal),
                    ])
                else:
                    output_text.extend([(" No object Selected", p.color_warning, p.text_size_normal)])

                # SOLVER
                # if (hasattr(bpy.context.preferences.system, 'opensubdiv_compute_type')):
                # if bpy.app.version == (2, 79, 0):
                #     output_text.extend([(" ", p.color_title, p.text_size_normal),
                #                           (str(mod.solver.upper()), p.color_value, p.text_size_normal)])

                # OVERLAP THRESHOLD
                # if mod.solver == 'BMESH':
                #     if mod.double_threshold > 0 :
                #         output_text.extend([(" Overlap Threshold ", p.color_setting, p.text_size_normal),
                #                           (str(round(mod.double_threshold,2)), p.color_value, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# BUILD
# ---------------------------------------------------------------


def mod_build(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
              mod: bpy.types.BuildModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_BUILD.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # START
                output_text.extend([
                    (" Start ", p.color_setting, p.text_size_normal),
                    (str(round(mod.frame_start, 2)), p.color_value, p.text_size_normal),
                ])

                # LENGTH
                output_text.extend([
                    (" Length ", p.color_setting, p.text_size_normal),
                    (str(round(mod.frame_duration, 2)), p.color_value, p.text_size_normal),
                ])

                # SEED
                if mod.use_random_order:
                    output_text.extend([
                        (" Seed ", p.color_setting, p.text_size_normal),
                        (str(mod.seed), p.color_value, p.text_size_normal),
                    ])

                if mod.use_reverse:
                    output_text.extend([(" Reversed ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# DECIMATE
# ---------------------------------------------------------------


def mod_decimate(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                 mod: bpy.types.DecimateModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_DECIM.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # COLLAPSE
                if mod.decimate_type == 'COLLAPSE':
                    output_text.extend([(" Collapse ", p.color_setting, p.text_size_normal)])
                    output_text.extend([
                        (" Ratio ", p.color_setting, p.text_size_normal),
                        (str(round(mod.ratio, 2)), p.color_value, p.text_size_normal),
                    ])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", p.color_setting, p.text_size_normal),
                            (str(mod.vertex_group), p.color_value, p.text_size_normal),
                        ])

                        # FACTOR
                        output_text.extend([
                            (" Factor ", p.color_setting, p.text_size_normal),
                            (str(round(mod.vertex_group_factor, 2)), p.color_value, p.text_size_normal),
                        ])
                    # OPTIONS
                    if any([mod.use_collapse_triangulate, mod.use_symmetry]):
                        output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                        # TRIANGULATE
                        if mod.use_collapse_triangulate:
                            output_text.extend([(" Triangulate ", p.color_setting, p.text_size_normal)])

                        # SYMMETRY
                        if mod.use_symmetry:
                            output_text.extend([
                                (" Symmetry ", p.color_setting, p.text_size_normal),
                                (str(mod.symmetry_axis), p.color_value, p.text_size_normal),
                            ])

                # UN-SUBDIVDE
                elif mod.decimate_type == 'UNSUBDIV':
                    output_text.extend([(" Un-subdivide ", p.color_setting, p.text_size_normal)])
                    output_text.extend([
                        (" Iteration ", p.color_setting, p.text_size_normal),
                        (str(round(mod.iterations, 2)), p.color_value, p.text_size_normal),
                    ])
                # PLANAR
                else:
                    output_text.extend([(" Planar ", p.color_setting, p.text_size_normal)])
                    output_text.extend([
                        (" Angle Limit ", p.color_setting, p.text_size_normal), (
                            str(round(math.degrees(mod.angle_limit), 1)), p.color_value, p.text_size_normal),
                        ("°", p.color_value, p.text_size_normal),
                    ])

                    # OPTIONS
                    if any([mod.use_dissolve_boundaries, mod.delimit]):
                        output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                        # ALL BOUNDARIES
                        if mod.use_dissolve_boundaries:
                            output_text.extend([(" All Boundaries ", p.color_setting, p.text_size_normal)])

                        # DELIMIT
                        if mod.delimit:
                            output_text.extend([(" Delimit ", p.color_setting, p.text_size_normal)])
                            if mod.delimit == {'NORMAL'}:
                                output_text.extend([(" NORMAL ", p.color_value, p.text_size_normal)])
                            elif mod.delimit == {'MATERIAL'}:
                                output_text.extend([(" MATERIAL ", p.color_value, p.text_size_normal)])
                            elif mod.delimit == {'SEAM'}:
                                output_text.extend([(" SEAM ", p.color_value, p.text_size_normal)])
                            elif mod.delimit == {'SHARP'}:
                                output_text.extend([(" SHARP ", p.color_value, p.text_size_normal)])
                            elif mod.delimit == {'UV'}:
                                output_text.extend([(" UV ", p.color_value, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# EDGE SPLIT
# ---------------------------------------------------------------


def mod_edge_split(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                   mod: bpy.types.EdgeSplitModifier, units) -> None:
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

# ---------------------------------------------------------------
# WEIGHTED NORMALS
# ---------------------------------------------------------------


def mod_weighted_normals(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                         mod: bpy.types.WeightedNormalModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_EDGESPLIT.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # Mode
                # output_text.extend([(" Mode", p.color_setting, p.text_size_normal), (str(mod.mode.lower().capitalize()), p.color_setting, p.text_size_normal)])
                output_text.extend([
                    (" Mode ", p.color_setting, p.text_size_normal),
                    (str(mod.mode.lower().capitalize()), p.color_value, p.text_size_normal),
                ])

                # Weight
                output_text.extend([
                    (" Weight ", p.color_setting, p.text_size_normal),
                    (str(round(mod.weight, 2)), p.color_value, p.text_size_normal),
                ])

                # STRENGTH
                output_text.extend([
                    (" Strength ", p.color_setting, p.text_size_normal),
                    (str(round(mod.weight, 2)), p.color_value, p.text_size_normal),
                ])

                # THRESHOLD
                output_text.extend([
                    (" Threshold ", p.color_setting, p.text_size_normal),
                    (str(round(mod.thresh, 2)), p.color_value, p.text_size_normal),
                ])

                if any([mod.keep_sharp, mod.face_influence, mod.vertex_group]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    # KEEP SHARP
                    if mod.keep_sharp:
                        output_text.extend([(" Keep Sharp ", p.color_setting, p.text_size_normal)])

                    # KEEP SHARP
                    if mod.face_influence:
                        output_text.extend([(" Face Influence ", p.color_setting, p.text_size_normal)])

                    if mod.vertex_group:
                        output_text.extend([
                            (" Vgroup ", p.color_setting, p.text_size_normal),
                            (str(mod.vertex_group), p.color_value, p.text_size_normal),
                        ])
                    else:
                        output_text.extend([(" No Vertex Group Selected ", p.color_warning, p.text_size_normal)])
        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# LATTICE
# ---------------------------------------------------------------


def mod_lattice(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                mod: bpy.types.LatticeModifier, units) -> None:
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_LATTICE.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                output_text.extend([(" Object ", p.color_setting, p.text_size_normal)])
                if mod.object:
                    # OBJECT
                    output_text.extend([(mod.object.name, p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (str(mod.vertex_group), p.color_value, p.text_size_normal),
                    ])

                # STRENGTH
                output_text.extend([
                    (" Strength ", p.color_setting, p.text_size_normal),
                    (str(round(mod.strength, 2)), p.color_value, p.text_size_normal),
                ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# MASK
# ---------------------------------------------------------------


def mod_mask(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
             mod: bpy.types.MaskModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MASK.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # ARMATURE
                if mod.mode == 'ARMATURE':
                    if mod.armature:
                        output_text.extend([
                            (" Armature ", p.color_setting, p.text_size_normal),
                            (str(mod.armature.name), p.color_value, p.text_size_normal),
                        ])
                    else:
                        output_text.extend([(" No Armature Selected ", p.color_warning, p.text_size_normal)])

                # VERTEX GROUP
                elif mod.mode == 'VERTEX_GROUP':
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", p.color_setting, p.text_size_normal),
                            (str(mod.vertex_group), p.color_value, p.text_size_normal),
                        ])
                    else:
                        output_text.extend([(" No Vertex Group Selected ", p.color_warning, p.text_size_normal)])
        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# MIRROR
# ---------------------------------------------------------------


def mod_mirror(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
               mod: bpy.types.MirrorModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MIRROR.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                if any([mod.use_axis[0], mod.use_axis[1], mod.use_axis[2]]):
                    output_text.extend([(" Axis ", p.color_setting, p.text_size_normal)])
                    # X
                    if mod.use_axis[0]:
                        output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                    # Y
                    if mod.use_axis[1]:
                        output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                    # Z
                    if mod.use_axis[2]:
                        output_text.extend([(" Z ", p.color_value, p.text_size_normal)])

                # OBJECT
                if mod.mirror_object:
                    output_text.extend([
                        (" Object ", p.color_setting, p.text_size_normal),
                        (mod.mirror_object.name, p.color_value, p.text_size_normal),
                    ])

                # MERGE
                if mod.use_mirror_merge:
                    output_text.extend([
                        (" Merge ", p.color_setting, p.text_size_normal),
                        (str(round(mod.merge_threshold, 3)), p.color_value, p.text_size_normal),
                        (units, p.color_value, p.text_size_normal),
                    ])

                # OPTIONS
                if any([mod.use_clip, mod.use_mirror_vertex_groups, mod.use_mirror_u, mod.use_mirror_v]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    # CLIPPING
                    if mod.use_clip:
                        output_text.extend([(" Clipping ", p.color_setting, p.text_size_normal)])

                    # VERTEX GROUP
                    if mod.use_mirror_vertex_groups:
                        output_text.extend([(" VGroup ", p.color_setting, p.text_size_normal)])

                    # TEXTURES
                    if any([mod.use_mirror_u, mod.use_mirror_v]):
                        output_text.extend([(" Textures ", p.color_setting, p.text_size_normal)])

                    # TEXTURE U
                    if mod.use_mirror_u:
                        output_text.extend([
                            (" U ", p.color_setting, p.text_size_normal),
                            (str(round(mod.mirror_offset_u, 3)), p.color_value, p.text_size_normal),
                            (units, p.color_value, p.text_size_normal),
                        ])

                    # TEXTURE V
                    if mod.use_mirror_v:
                        output_text.extend([
                            (" V ", p.color_setting, p.text_size_normal),
                            (str(round(mod.mirror_offset_v, 3)), p.color_value, p.text_size_normal),
                            (units, p.color_value, p.text_size_normal),
                        ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# MULTIRES
# ---------------------------------------------------------------


def mod_multires(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, mod: bpy.types.MultiresModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MULTIRES.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # SUBDIVISION TYPE
                if mod.subdivision_type == 'SIMPLE':
                    output_text.extend([(" Simple ", p.color_setting, p.text_size_normal)])
                else:
                    output_text.extend([(" Catmull Clark ", p.color_setting, p.text_size_normal)])

                # QUALITY
                output_text.extend([
                    (" Quality ", p.color_setting, p.text_size_normal),
                    (str(mod.quality), p.color_value, p.text_size_normal),
                ])

                # RENDER SUBDIVISION LEVELS
                output_text.extend([
                    (" Render ", p.color_setting, p.text_size_normal),
                    (str(mod.render_levels), p.color_value, p.text_size_normal),
                ])

                # VIEWPORT SUBDIVISION LEVELS
                output_text.extend([
                    (" Preview ", p.color_setting, p.text_size_normal),
                    (str(mod.levels), p.color_value, p.text_size_normal),
                ])

                # FIXME: We need a dynamic wrap here
                if any([mod.uv_smooth == "PRESERVE_CORNERS", mod.show_only_control_edges, mod.use_creases]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                # UV SMOOTHING
                if mod.uv_smooth == "PRESERVE_CORNERS":
                    output_text.extend([
                        (" UV Smoothing (keep corners) ", p.color_setting, p.text_size_normal),
                    ])

                # OPTIMAL DISPLAY
                if mod.show_only_control_edges:
                    output_text.extend([(" Optimal Display ", p.color_setting, p.text_size_normal)])

                if mod.use_creases:
                    output_text.extend([(" Using Creases ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# REMESH
# ---------------------------------------------------------------


def mod_remesh(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
               mod: bpy.types.RemeshModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_REMESH.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                output_text.extend([
                    (" ", p.color_title, p.text_size_normal),
                    (str(mod.mode), p.color_value, p.text_size_normal),
                ])

                if mod.mode != "VOXEL":
                    # OCTREE DEPTH
                    output_text.extend([
                        (" Octree Depth ", p.color_setting, p.text_size_normal),
                        (str(mod.octree_depth), p.color_value, p.text_size_normal),
                    ])

                    # SCALE
                    output_text.extend([
                        (" Scale ", p.color_setting, p.text_size_normal),
                        (str(round(mod.scale, 2)), p.color_value, p.text_size_normal),
                    ])

                # SHARPNESS
                if mod.mode == 'SHARP':
                    output_text.extend([
                        (" Sharpness ", p.color_setting, p.text_size_normal),
                        (str(round(mod.sharpness, 2)), p.color_value, p.text_size_normal),
                    ])

                # OPTIONS
                if any([mod.use_smooth_shade, mod.use_remove_disconnected]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # SMOOTH SHADING
                    if mod.use_smooth_shade:
                        output_text.extend([(" Smooth Shading ", p.color_setting, p.text_size_normal)])

                    # REMOVE DISCONNECTED
                    if mod.mode != "VOXEL" and mod.use_remove_disconnected:
                        output_text.extend([
                            (" Remove Disconnected Pieces ", p.color_setting, p.text_size_normal),
                            (str(round(mod.threshold, 2)), p.color_value, p.text_size_normal),
                        ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# SCREW
# ---------------------------------------------------------------


# FIXME: Update for 2.8x/2.9x
def mod_screw(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, mod: bpy.types.ScrewModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SCREW.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # AXIS
                output_text.extend([
                    (" Axis ", p.color_setting, p.text_size_normal),
                    (str(mod.axis), p.color_value, p.text_size_normal),
                ])

                # AXIS OBJECT
                if mod.object:
                    output_text.extend([
                        (" Axis Object ", p.color_setting, p.text_size_normal),
                        (str(mod.object.name), p.color_value, p.text_size_normal),
                    ])

                # SCREW
                output_text.extend([
                    (" Screw ", p.color_setting, p.text_size_normal),
                    (str(round(mod.screw_offset, 2)), p.color_value, p.text_size_normal),
                    (units, p.color_value, p.text_size_normal),
                ])

                # ITERATIONS
                output_text.extend([
                    (" Iterations ", p.color_setting, p.text_size_normal),
                    (str(round(mod.iterations, 2)), p.color_value, p.text_size_normal),
                ])

                # Angle
                output_text.extend([
                    (" Angle ", p.color_setting, p.text_size_normal),
                    (str(round(math.degrees(mod.angle), 1)), p.color_value, p.text_size_normal),
                    ("°", p.color_value, p.text_size_normal),
                ])

                # STEPS
                output_text.extend([
                    (" Steps ", p.color_setting, p.text_size_normal),
                    (str(round(mod.steps, 2)), p.color_value, p.text_size_normal),
                ])

                # OPTIONS LINE 1
                if any([mod.use_normal_flip, mod.use_smooth_shade, mod.use_object_screw_offset,
                        mod.use_normal_calculate]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # USE FLIP
                    if mod.use_normal_flip:
                        output_text.extend([(" Flip ", p.color_setting, p.text_size_normal)])

                    # USE SMOOTH SHADE
                    if mod.use_smooth_shade:
                        output_text.extend([(" Smooth Shading ", p.color_setting, p.text_size_normal)])

                    # USE OBJECT SCREW OFFSET
                    # if mod.object:
                    if mod.use_object_screw_offset:
                        output_text.extend([(" Object Screw ", p.color_setting, p.text_size_normal)])

                    # CALC ORDER
                    if mod.use_normal_calculate:
                        output_text.extend([(" Calc Order ", p.color_setting, p.text_size_normal)])

                # OPTIONS LINE 2
                if any([mod.use_merge_vertices, mod.use_stretch_u, mod.use_stretch_v]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    # USE MERGE VERTICES
                    if mod.use_merge_vertices:
                        output_text.extend([
                            (" Merge Vertices ", p.color_setting, p.text_size_normal),
                            (str(round(mod.merge_threshold, 2)), p.color_value, p.text_size_normal),
                            (units, p.color_value, p.text_size_normal),
                        ])

                    # STRETCH U
                    if mod.use_stretch_u:
                        output_text.extend([(" Stretch U ", p.color_setting, p.text_size_normal)])

                    # STRETCH V
                    if mod.use_stretch_v:
                        output_text.extend([(" Stretch V ", p.color_setting, p.text_size_normal)])
        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# SKIN
# ---------------------------------------------------------------


def mod_skin(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
             mod: bpy.types.SkinModifier, units) -> None:
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SKIN.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # BRANCH SMOOTHING
                if mod.branch_smoothing != 0:
                    output_text.extend([
                        (" Branch Smoothing ", p.color_setting, p.text_size_normal),
                        (str(round(mod.branch_smoothing, 3)), p.color_value, p.text_size_normal),
                    ])

                if any([mod.use_x_symmetry, mod.use_y_symmetry, mod.use_z_symmetry]):
                    # SYMMETRY
                    output_text.extend([(" Symmetry ", p.color_setting, p.text_size_normal)])

                    # X
                    if mod.use_x_symmetry:
                        output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                    # Y
                    if mod.use_y_symmetry:
                        output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                    # Z
                    if mod.use_z_symmetry:
                        output_text.extend([(" Z ", p.color_value, p.text_size_normal)])

                # OPTIONS
                if any([mod.use_smooth_shade]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # SMOOTH SHADING
                    if mod.use_smooth_shade:
                        output_text.extend([(" Smooth Shading ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# SOLIDIFY
# ---------------------------------------------------------------

# FIXME: Needs to support 'complex' mode


def mod_solidify(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                 mod: bpy.types.SolidifyModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SOLIDIFY.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # THICKNESS
                output_text.extend([
                    (" Thickness ", p.color_setting, p.text_size_normal),
                    (str(round(mod.thickness, 3)), p.color_value, p.text_size_normal),
                    (units, p.color_value, p.text_size_normal),
                ])

                # OFFSET
                output_text.extend([
                    (" Offset ", p.color_setting, p.text_size_normal),
                    (str(round(mod.offset, 2)), p.color_value, p.text_size_normal),
                ])

                # CLAMP
                if mod.thickness_clamp != 0:
                    output_text.extend([
                        (" Clamp ", p.color_setting, p.text_size_normal),
                        (str(round(mod.thickness_clamp, 2)), p.color_value, p.text_size_normal),
                    ])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (str(mod.vertex_group), p.color_value, p.text_size_normal),
                    ])

                    # THICKNESS VGROUP
                    output_text.extend([
                        (" Clamp ", p.color_setting, p.text_size_normal),
                        (str(round(mod.thickness_vertex_group, 2)), p.color_value, p.text_size_normal),
                    ])

                # OPTIONS LIGNE 1
                if any([mod.use_flip_normals, mod.use_even_offset, mod.use_quality_normals, mod.use_rim]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # FLIP NORMALS
                    if mod.use_flip_normals:
                        output_text.extend([(" Flip Normals ", p.color_setting, p.text_size_normal)])

                    # USE EVEN OFFSET
                    if mod.use_even_offset:
                        output_text.extend([(" Even Thickness ", p.color_setting, p.text_size_normal)])

                    # HIGH QUALITY NORMALS
                    if mod.use_quality_normals:
                        output_text.extend([(" High Quality Normals ", p.color_setting, p.text_size_normal)])

                    # USE RIM
                    if mod.use_rim:
                        output_text.extend([(" Fill Rim ", p.color_setting, p.text_size_normal)])

                        # ONLY RIM
                        if mod.use_rim_only:
                            output_text.extend([(" Only rims ", p.color_setting, p.text_size_normal)])

                # OPTIONS LIGNE 2
                if any([mod.edge_crease_inner, mod.edge_crease_outer, mod.edge_crease_rim]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # INNER
                    if mod.edge_crease_inner != 0:
                        output_text.extend([
                            (" Inner ", p.color_setting, p.text_size_normal),
                            (str(round(mod.edge_crease_inner, 2)), p.color_value, p.text_size_normal),
                        ])

                    # OUTER
                    if mod.edge_crease_outer != 0:
                        output_text.extend([
                            (" Outer ", p.color_setting, p.text_size_normal),
                            (str(round(mod.edge_crease_outer, 2)), p.color_value, p.text_size_normal),
                        ])

                    # RIM
                    if mod.edge_crease_rim != 0:
                        output_text.extend([
                            (" Rim ", p.color_setting, p.text_size_normal),
                            (str(round(mod.edge_crease_rim, 2)), p.color_value, p.text_size_normal),
                        ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# SUBSURF
# ---------------------------------------------------------------


def mod_subsurf(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                mod: bpy.types.SubsurfModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SUBSURF.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        # FIXME: Almost all of this is the same as the multires modifier. Can
        # we consolidate the code a bit?
        if mod.show_viewport:
            if p.detailed_modifiers:
                # SUBDIVISION TYPE
                if mod.subdivision_type == 'SIMPLE':
                    output_text.extend([(" Simple ", p.color_setting, p.text_size_normal)])
                else:
                    output_text.extend([(" Catmull Clark ", p.color_setting, p.text_size_normal)])

                # QUALITY
                output_text.extend([
                    (" Quality ", p.color_setting, p.text_size_normal),
                    (str(mod.quality), p.color_value, p.text_size_normal),
                ])

                # RENDER SUBDIVISION LEVELS
                output_text.extend([
                    (" Render ", p.color_setting, p.text_size_normal),
                    (str(mod.render_levels), p.color_value, p.text_size_normal),
                ])

                # VIEWPORT SUBDIVISION LEVELS
                output_text.extend([
                    (" Preview ", p.color_setting, p.text_size_normal),
                    (str(mod.levels), p.color_value, p.text_size_normal),
                ])

                # FIXME: We need a dynamic wrap here
                if any([mod.uv_smooth == "PRESERVE_CORNERS", mod.show_only_control_edges, mod.use_creases]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                # UV SMOOTHING
                if mod.uv_smooth == "PRESERVE_CORNERS":
                    output_text.extend([
                        (" UV Smoothing (keep corners) ", p.color_setting, p.text_size_normal),
                    ])

                # OPTIMAL DISPLAY
                if mod.show_only_control_edges:
                    output_text.extend([(" Optimal Display ", p.color_setting, p.text_size_normal)])

                if mod.use_creases:
                    output_text.extend([(" Using Creases ", p.color_setting, p.text_size_normal)])

                # FIXME: Do we need to add code for this case? Does this case exist in 2.8x?
                # OPEN SUBDIV
                # if (hasattr(bpy.context.preferences.system, 'opensubdiv_compute_type')):
                #     if mod.use_opensubdiv:
                #         output_text.extend([(" Open Subdiv ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# TRIANGULATE
# ---------------------------------------------------------------

# FIXME: Needs to support 'keep normals'  minimum verts, and not have
# underscores in the 'method' field


def mod_triangulate(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, mod: bpy.types.TriangulateModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_TRIANGULATE.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # VIEW
                output_text.extend([
                    ("  ", p.color_setting, p.text_size_normal),
                    (str(mod.quad_method.lower().capitalize()), p.color_value, p.text_size_normal),
                ])

                # RENDER
                output_text.extend([
                    ("  ", p.color_setting, p.text_size_normal),
                    (str(mod.ngon_method.lower().capitalize()), p.color_value, p.text_size_normal),
                ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# WIREFRAME
# ---------------------------------------------------------------


def mod_wireframe(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                  mod: bpy.types.WireframeModifier, units) -> None:
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

# ----------------------------------------------------------------------
# MODIFIERS DEFORM -----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------

# ---------------------------------------------------------------
# ARMATURE
# ---------------------------------------------------------------


def mod_armature(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, mod: bpy.types.ArmatureModifier) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_ARMATURE.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        # FIXME: We should have a 'problem' color rather than reusing 'color_warning'
        if mod.show_viewport:
            if p.detailed_modifiers:
                output_text.extend([(" Object ", p.color_setting, p.text_size_normal)])
                if mod.object:
                    # START
                    output_text.extend([(str(mod.object.name), p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # VERTEX GROUP
                if mod.use_vertex_groups:
                    output_text.extend([(" VGroup ", p.color_setting, p.text_size_normal)])
                    if mod.vertex_group:
                        output_text.extend([(str(mod.vertex_group), p.color_value, p.text_size_normal)])
                    else:
                        output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # OPTIONS
                if any([mod.use_deform_preserve_volume, mod.use_bone_envelopes, mod.use_multi_modifier]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # PRESERVE VOLUME
                    if mod.use_deform_preserve_volume:

                        output_text.extend([(" Preserve Volume ", p.color_setting, p.text_size_normal)])

                    # BONE ENVELOPES
                    if mod.use_bone_envelopes:
                        output_text.extend([(" Bone Enveloppes ", p.color_setting, p.text_size_normal)])

                    # MULTI MODIFIER
                    if mod.use_multi_modifier:
                        output_text.extend([(" Multi Modifier ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# CAST
# ---------------------------------------------------------------


def mod_cast(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
             mod: bpy.types.CastModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_CAST.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # CAST TYPE
                output_text.extend([
                    (" Type ", p.color_setting, p.text_size_normal),
                    (str(mod.cast_type.lower().capitalize()), p.color_value, p.text_size_normal),
                ])

                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    output_text.extend([(" Axis ", p.color_setting, p.text_size_normal)])

                    if mod.use_x:
                        output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                    if mod.use_y:
                        output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                    if mod.use_z:
                        output_text.extend([(" Z ", p.color_value, p.text_size_normal)])

                else:
                    output_text.extend([(" No Axis Selected ", p.color_warning, p.text_size_normal)])

                # FACTOR
                output_text.extend([
                    (" Factor ", p.color_setting, p.text_size_normal),
                    (str(round(mod.factor, 2)), p.color_value, p.text_size_normal),
                ])

                # RADIUS
                if mod.radius != 0:
                    output_text.extend([
                        (" Radius ", p.color_setting, p.text_size_normal),
                        (str(round(mod.radius, 2)), p.color_value, p.text_size_normal),
                        (units, p.color_value, p.text_size_normal),
                    ])

                # SIZE
                if mod.size != 0:
                    output_text.extend([
                        (" Size ", p.color_setting, p.text_size_normal),
                        (str(round(mod.size, 2)), p.color_value, p.text_size_normal),
                    ])

                # OPTIONS
                if any([mod.use_radius_as_size, mod.vertex_group, mod.object, mod.use_transform]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", p.color_setting, p.text_size_normal),
                            (mod.vertex_group, p.color_value, p.text_size_normal),
                        ])

                    # FROM RADIUS
                    if mod.use_radius_as_size:
                        output_text.extend([(" From Radius ", p.color_setting, p.text_size_normal)])

                    # OBJECT
                    if mod.object:
                        output_text.extend([
                            (" Control Object ", p.color_setting, p.text_size_normal),
                            (mod.object.name, p.color_value, p.text_size_normal)
                        ])

                    # USE TRANSFORM
                    if mod.use_transform:
                        output_text.extend([(" Use Transform ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# CORRECTIVE SMOOTH
# ---------------------------------------------------------------


def mod_corrective_smooth(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                          mod: bpy.types.CorrectiveSmoothModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend([
            "CR",
            (str(mod.name.upper()), p.color_title, p.text_size_normal),
        ])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # FACTOR
                output_text.extend([
                    (" Factor ", p.color_setting, p.text_size_normal),
                    (str(round(mod.factor, 2)), p.color_value, p.text_size_normal),
                ])

                # ITERATIONS
                output_text.extend([
                    (" Repeat ", p.color_setting, p.text_size_normal),
                    (str(mod.iterations), p.color_value, p.text_size_normal),
                ])

                # SCALE
                if mod.scale != 1.0:
                    output_text.extend([
                        (" Scale ", p.color_setting, p.text_size_normal),
                        (str(round(mod.scale, 2)), p.color_value, p.text_size_normal),
                    ])

                # SMOOTH TYPE
                output_text.extend([
                    (" Type ", p.color_setting, p.text_size_normal),
                    (str(mod.smooth_type.lower().capitalize()), p.color_value, p.text_size_normal),
                ])

                # OPTIONS
                if any([mod.use_only_smooth, mod.vertex_group, mod.use_pin_boundary, mod.rest_source]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", p.color_setting, p.text_size_normal),
                            (mod.vertex_group, p.color_value, p.text_size_normal),
                        ])

                    # ONLY SMOOTH
                    if mod.use_only_smooth:
                        output_text.extend([(" Only Smooth ", p.color_setting, p.text_size_normal)])

                    # PIN BOUNDARIES
                    if mod.use_pin_boundary:
                        output_text.extend([(" Pin Boundaries ", p.color_setting, p.text_size_normal)])

                    # OBJECT
                    output_text.extend([
                        (" Rest Source ", p.color_setting, p.text_size_normal),
                        (mod.rest_source.lower().capitalize(), p.color_value, p.text_size_normal),
                    ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# CURVE
# ---------------------------------------------------------------


def mod_curve(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
              mod: bpy.types.CurveModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_CURVE.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend([
            "CR",
            (str(mod.name.upper()), p.color_title, p.text_size_normal),
        ])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # OBJECT
                output_text.extend([(" Object ", p.color_setting, p.text_size_normal)])
                if mod.object:
                    output_text.extend([(mod.object.name, p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # DEFORM AXIS
                output_text.extend([(" Deformation Axis ", p.color_setting, p.text_size_normal)])
                if mod.deform_axis == 'POS_X':
                    output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                elif mod.deform_axis == 'POS_Y':
                    output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                elif mod.deform_axis == 'POS_Z':
                    output_text.extend([(" Z ", p.color_value, p.text_size_normal)])

                elif mod.deform_axis == 'NEG_X':
                    output_text.extend([(" -X ", p.color_value, p.text_size_normal)])

                elif mod.deform_axis == 'NEG_Y':
                    output_text.extend([(" -Y ", p.color_value, p.text_size_normal)])

                elif mod.deform_axis == 'NEG_Z':
                    output_text.extend([(" -Z ", p.color_value, p.text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (str(mod.vertex_group), p.color_value, p.text_size_normal),
                    ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# DISPLACE
# ---------------------------------------------------------------


def mod_displace(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                 mod: bpy.types.DisplaceModifier, units) -> None:
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

# ---------------------------------------------------------------
# HOOK
# ---------------------------------------------------------------


def mod_hook(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
             mod: bpy.types. HookModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_HOOK.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # OBJECT
                output_text.extend([(" Object ", p.color_setting, p.text_size_normal)])
                if mod.object:
                    output_text.extend([(mod.object.name, p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # RADIUS
                if mod.falloff_type != 'NONE':
                    if mod.falloff_radius != 0:
                        output_text.extend([
                            (" Radius ", p.color_setting, p.text_size_normal),
                            (str(round(mod.falloff_radius, 2)), p.color_value, p.text_size_normal),
                            (units, p.color_value, p.text_size_normal),
                        ])

                # STRENGTH
                output_text.extend([
                    (" Strength ", p.color_setting, p.text_size_normal),
                    (str(round(mod.strength, 2)), p.color_value, p.text_size_normal),
                ])

                # OPTIONS
                output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (mod.vertex_group, p.color_value, p.text_size_normal),
                    ])

                # FALLOF TYPE
                output_text.extend([
                    (" Fallof Type ", p.color_setting, p.text_size_normal),
                    (str(mod.falloff_type.upper()), p.color_value, p.text_size_normal),
                ])

                # UNIFORM FALLOFF
                if mod.use_falloff_uniform:
                    output_text.extend([(" Uniform Falloff ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# LAPLACIAN DEFORMER
# ---------------------------------------------------------------


def mod_laplacian_deformer(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                           mod: bpy.types.LaplacianDeformModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        # FIXME: display this more readably
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # ITERATIONS
                output_text.extend([
                    (" Repeat ", p.color_setting, p.text_size_normal),
                    (str(mod.iterations), p.color_value, p.text_size_normal),
                ])

                # VERTEX GROUP
                output_text.extend([(" VGroup ", p.color_setting, p.text_size_normal)])
                if mod.vertex_group:
                    output_text.extend([(str(mod.vertex_group), p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# LAPLACIAN SMOOTH
# ---------------------------------------------------------------


def mod_laplacian_smooth(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                         mod: bpy.types.LaplacianSmoothModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # REPEAT
                output_text.extend([
                    (" Repeat ", p.color_setting, p.text_size_normal),
                    (str(mod.iterations), p.color_value, p.text_size_normal),
                ])

                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    output_text.extend([(" Axis", p.color_setting, p.text_size_normal)])

                    if mod.use_x:
                        output_text.extend([(" X", p.color_value, p.text_size_normal)])

                    if mod.use_y:
                        output_text.extend([(" Y", p.color_value, p.text_size_normal)])

                    if mod.use_z:
                        output_text.extend([(" Z", p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None", p.color_warning, p.text_size_normal)])

                # FACTOR
                output_text.extend([
                    (" Factor ", p.color_setting, p.text_size_normal),
                    (str(round(mod.lambda_factor, 2)), p.color_value, p.text_size_normal),
                ])

                # BORDER
                output_text.extend([
                    (" Border ", p.color_setting, p.text_size_normal),
                    (str(round(mod.lambda_border, 2)), p.color_value, p.text_size_normal),
                ])

                # OPTIONS
                if any([mod.use_volume_preserve, mod.use_normalized, mod.vertex_group]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # PRESERVE VOLUME
                    if mod.use_volume_preserve:
                        output_text.extend([(" Preserve Volume ", p.color_setting, p.text_size_normal)])

                    # NORMALIZED
                    if mod.use_normalized:
                        output_text.extend([(" Normalized ", p.color_setting, p.text_size_normal)])

                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", p.color_setting, p.text_size_normal),
                            (mod.vertex_group, p.color_value, p.text_size_normal)
                        ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# MESH DEFORM
# ---------------------------------------------------------------


def mod_mesh_deform(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                    mod: bpy.types.MeshDeformModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # OBJECT
                output_text.extend([(" Object ", p.color_setting, p.text_size_normal)])
                if mod.object:
                    output_text.extend([(mod.object.name, p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # PRECISION
                output_text.extend([
                    (" Precision ", p.color_setting, p.text_size_normal),
                    (str(mod.precision), p.color_value, p.text_size_normal),
                ])

                # OPTIONS
                if any([mod.use_dynamic_bind, mod.vertex_group]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([(" VGroup ", p.color_setting, p.text_size_normal),
                                            (str(mod.vertex_group), p.color_value, p.text_size_normal)])

                    # USE DYNAMIC BIND
                    if mod.use_dynamic_bind:
                        output_text.extend([(" Dynamic ", p.color_setting, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# SIMPLE DEFORM
# ---------------------------------------------------------------


def mod_simple_deform(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                      mod: bpy.types.SimpleDeformModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SIMPLEDEFORM.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                output_text.extend([
                    (" ", p.color_setting, p.text_size_normal),
                    (str(mod.deform_method.upper()), p.color_value, p.text_size_normal),
                ])

                # ORIGIN
                if mod.origin:
                    output_text.extend([(" Axis,Origin ", p.color_setting, p.text_size_normal),
                                        (str(mod.origin.name), p.color_value, p.text_size_normal),
                                        ])

                # ANGLE/FACTOR
                if mod.deform_method in ['TWIST', 'BEND']:
                    # Angle
                    output_text.extend([
                        (" Angle ", p.color_setting, p.text_size_normal),
                        (str(round(math.degrees(mod.factor), 1)), p.color_value, p.text_size_normal),
                        ("°", p.color_value, p.text_size_normal),
                    ])

                elif mod.deform_method in ['TAPER', 'STRETCH']:
                    output_text.extend([
                        (" Factor ", p.color_setting, p.text_size_normal),
                        (str(round(mod.factor, 2)), p.color_value, p.text_size_normal),
                    ])

                # OPTIONS
                output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                # AXIS
                # FIXME: Should we always show this?
                output_text.extend([
                    (" Axis ", p.color_setting, p.text_size_normal),
                    (mod.deform_axis, p.color_value, p.text_size_normal),
                ])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (str(mod.vertex_group), p.color_value, p.text_size_normal),
                    ])

                # LOCK
                if mod.deform_method != 'BEND':
                    if any([mod.lock_x, mod.lock_y]):
                        output_text.extend([(" Lock ", p.color_setting, p.text_size_normal)])

                        if mod.lock_x:
                            output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                        if mod.lock_y:
                            output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                # LIMIT
                output_text.extend([
                    (" Limit ", p.color_setting, p.text_size_normal),
                    (str(round(mod.limits[0], 2)), p.color_value, p.text_size_normal),
                    (" – ", p.color_setting, p.text_size_normal),
                    (str(round(mod.limits[1], 2)), p.color_value, p.text_size_normal),
                ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# SHRINKWRAP
# ---------------------------------------------------------------


def mod_shrinkwrap(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                   mod: bpy.types.ShrinkwrapModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SHRINKWRAP.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # TARGET
                output_text.extend([(" Target ", p.color_setting, p.text_size_normal)])
                if mod.target:
                    output_text.extend([(str(mod.target.name), p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

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

                output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                # NEAREST SURFACEPOINT
                if mod.wrap_method == 'NEAREST_SURFACEPOINT':
                    # MODE
                    output_text.extend([
                        (" Method ", p.color_setting, p.text_size_normal),
                        (str(mod.wrap_method.lower().capitalize()), p.color_value, p.text_size_normal),
                        (" Mode ", p.color_setting, p.text_size_normal),
                        (str(mod.wrap_mode.lower().capitalize()), p.color_value, p.text_size_normal),
                    ])

                # PROJECT
                elif mod.wrap_method == 'PROJECT':
                    # MODE
                    output_text.extend([
                        (" Method ", p.color_setting, p.text_size_normal),
                        (str(mod.wrap_method.lower().capitalize()), p.color_value, p.text_size_normal),
                        (" Mode ", p.color_setting, p.text_size_normal),
                        (str(mod.wrap_mode.lower().capitalize()), p.color_value, p.text_size_normal),
                    ])

                    # AXIS
                    if any([mod.use_project_x, mod.use_project_y, mod.use_project_z]):
                        output_text.extend([(" Axis ", p.color_setting, p.text_size_normal)])
                        # X
                        if mod.use_project_x:
                            output_text.extend([(" X ", p.color_value, p.text_size_normal)])
                        # Y
                        if mod.use_project_y:
                            output_text.extend([(" Y ", p.color_value, p.text_size_normal)])
                        # Z
                        if mod.use_project_z:
                            output_text.extend([(" Z ", p.color_value, p.text_size_normal)])

                    # LEVELS
                    output_text.extend([
                        (" Subsurf ", p.color_setting, p.text_size_normal),
                        (str(mod.subsurf_levels), p.color_value, p.text_size_normal),
                    ])

                    # PROJECT LIMIT
                    output_text.extend([
                        (" Limit ", p.color_setting, p.text_size_normal),
                        (str(round(mod.project_limit, 2)), p.color_value, p.text_size_normal)
                    ])

                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # DIRECTION
                    if mod.use_negative_direction:
                        output_text.extend([(" Negative ", p.color_setting, p.text_size_normal)])

                    if mod.use_positive_direction:
                        output_text.extend([(" Positive ", p.color_setting, p.text_size_normal)])

                    # MODE
                    output_text.extend([
                        (" Cull Face ", p.color_setting, p.text_size_normal),
                        (str(mod.cull_face.lower().capitalize()), p.color_value, p.text_size_normal),
                    ])
                    # AUXILIARY TARGET
                    if mod.auxiliary_target:
                        output_text.extend([
                            (" Auxiliary Target ", p.color_setting, p.text_size_normal),
                            (mod.auxiliary_target.name, p.color_value, p.text_size_normal),
                        ])
                else:
                    # MODE
                    output_text.extend([
                        (" Mode ", p.color_setting, p.text_size_normal),
                        (str(mod.wrap_method.lower().capitalize()), p.color_value, p.text_size_normal),
                    ])
        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# SMOOTH
# ---------------------------------------------------------------


def mod_smooth(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
               mod: bpy.types.SmoothModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    output_text.extend([(" Axis ", p.color_setting, p.text_size_normal)])

                    if mod.use_x:
                        output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                    if mod.use_y:
                        output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                    if mod.use_z:
                        output_text.extend([(" Z ", p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" No Axis Selected ", p.color_warning, p.text_size_normal)])

                # FACTOR
                output_text.extend([
                    (" Factor ", p.color_setting, p.text_size_normal),
                    (str(round(mod.factor, 2)), p.color_value, p.text_size_normal),
                ])

                # ITERATIONS
                output_text.extend([
                    (" Repeat ", p.color_setting, p.text_size_normal),
                    (str(mod.iterations), p.color_value, p.text_size_normal),
                ])

                # OPTIONS
                if mod.vertex_group:
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (mod.vertex_group, p.color_value, p.text_size_normal),
                    ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# SURFACE DEFORM
# ---------------------------------------------------------------


def mod_surface_deform(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                       mod: bpy.types.SurfaceDeformModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # TARGET
                output_text.extend([(" Target ", p.color_setting, p.text_size_normal)])
                if mod.target:
                    output_text.extend([(str(mod.target.name), p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # FALLOFF
                output_text.extend([
                    (" Falloff ", p.color_setting, p.text_size_normal),
                    (str(round(mod.falloff, 2)), p.color_value, p.text_size_normal),
                ])

                if mod.vertex_group:
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    output_text.extend([
                        (" VGroup ", p.color_setting, p.text_size_normal),
                        (mod.vertex_group, p.color_value, p.text_size_normal),
                    ])

                output_text.extend([
                    (" Strength ", p.color_setting, p.text_size_normal),
                    (str(round(mod.strength, 2)), p.color_value, p.text_size_normal),
                ])
        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# WARP
# ---------------------------------------------------------------


def mod_warp(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
             mod: bpy.types.WarpModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_WARP.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                # FROM
                output_text.extend([(" From ", p.color_setting, p.text_size_normal)])
                if mod.object_from:
                    output_text.extend([(str(mod.object_from.name), p.color_value, p.text_size_normal)])

                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # TO
                output_text.extend([(" To ", p.color_setting, p.text_size_normal)])
                if mod.object_to:
                    output_text.extend([(str(mod.object_to.name), p.color_value, p.text_size_normal)])
                else:
                    output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                # STRENGTH
                output_text.extend([
                    (" Strength ", p.color_setting, p.text_size_normal),
                    (str(round(mod.strength, 2)), p.color_value, p.text_size_normal),
                ])

                output_text.extend([
                    (" Falloff ", p.color_setting, p.text_size_normal),
                    (mod.falloff_type.lower().capitalize(), p.color_value, p.text_size_normal),
                ])

                # RADIUS
                if mod.falloff_type != 'NONE':
                    # FIXME: Radius showing in m when units are cm
                    if mod.falloff_radius != 0:
                        output_text.extend([
                            (" Radius ", p.color_setting, p.text_size_normal),
                            (str(round(mod.falloff_radius, 2)), p.color_value, p.text_size_normal),
                            (units, p.color_value, p.text_size_normal),
                        ])

                # OPTIONS
                if any([mod.vertex_group, mod.use_volume_preserve, mod.texture_coords]):
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", p.color_setting, p.text_size_normal),
                            (str(mod.vertex_group), p.color_value, p.text_size_normal),
                        ])

                    # OFFSET
                    if mod.use_volume_preserve:
                        output_text.extend([(" Preserve Volume ", p.color_setting, p.text_size_normal)])

                    # TEXTURE
                    if mod.texture:
                        output_text.extend([
                            (" Texture ", p.color_setting, p.text_size_normal),
                            (mod.texture.name, p.color_value, p.text_size_normal),
                        ])

                    # TEXTURES COORD
                    output_text.extend([
                        (" Texture Coords ", p.color_setting, p.text_size_normal),
                        (mod.texture_coords, p.color_value, p.text_size_normal),
                    ])

                    # OBJECT
                    if mod.texture_coords == "OBJECT":
                        if mod.texture_coords_object:
                            output_text.extend([(" Object ", p.color_setting, p.text_size_normal)])
                            output_text.extend([
                                (str(mod.texture_coords_object.name), p.color_value, p.text_size_normal),
                            ])
                        else:
                            output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                    # UVs
                    if mod.texture_coords == "UV":
                        output_text.extend([(" UVMap ", p.color_setting, p.text_size_normal)])

                        if mod.uv_layer:
                            output_text.extend([
                                (str(mod.uv_layer), p.color_value, p.text_size_normal)
                            ])
                        else:
                            output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ---------------------------------------------------------------
# WAVE
# ---------------------------------------------------------------


def mod_wave(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
             mod: bpy.types.WaveModifier, units) -> None:
    # obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_WAVE.png'), ("    ", p.color_setting, p.text_size_normal),
        #                   (str(mod.name.upper()), p.color_title, p.text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), p.color_title, p.text_size_normal)])

        if mod.show_viewport:
            if p.detailed_modifiers:
                if any([mod.use_x, mod.use_y, mod.use_cyclic]):
                    output_text.extend([(" Motion ", p.color_setting, p.text_size_normal)])

                    if mod.use_x:
                        output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                    if mod.use_y:
                        output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                    if mod.use_cyclic:
                        output_text.extend([(" Cyclic ", p.color_value, p.text_size_normal)])

                if mod.use_normal:
                    if any([mod.use_normal_x, mod.use_normal_y, mod.use_normal_z]):
                        output_text.extend([(" Normals ", p.color_setting, p.text_size_normal)])

                        if mod.use_normal_x:
                            output_text.extend([(" X ", p.color_value, p.text_size_normal)])

                        if mod.use_normal_y:
                            output_text.extend([(" Y ", p.color_value, p.text_size_normal)])

                        if mod.use_normal_z:
                            output_text.extend([(" Z ", p.color_value, p.text_size_normal)])

                # TIME
                output_text.extend([(" Time ", p.color_setting, p.text_size_normal)])

                # OFFSET
                output_text.extend([
                    (" Offset ", p.color_setting, p.text_size_normal),
                    (str(round(mod.time_offset, 2)), p.color_value, p.text_size_normal),
                ])
                # LIFE
                output_text.extend([
                    (" Life ", p.color_setting, p.text_size_normal),
                    (str(round(mod.lifetime, 2)), p.color_value, p.text_size_normal),
                ])
                # DAMPING
                output_text.extend([
                    (" Damping ", p.color_setting, p.text_size_normal),
                    (str(round(mod.damping_time, 2)), p.color_value, p.text_size_normal),
                ])

                if any([mod.start_position_x, mod.start_position_y, mod.falloff_radius]) != 0:
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])
                    # TIME
                    # FIXME: shows m when scale is cm
                    output_text.extend([(" Position ", p.color_setting, p.text_size_normal)])

                    # POS X
                    output_text.extend([
                        (" X ", p.color_setting, p.text_size_normal),
                        (str(round(mod.start_position_x, 2)), p.color_value, p.text_size_normal),
                        (units, p.color_value, p.text_size_normal),
                    ])

                    # POS Y
                    output_text.extend([
                        (" Y ", p.color_setting, p.text_size_normal),
                        (str(round(mod.start_position_y, 2)), p.color_value, p.text_size_normal),
                        (units, p.color_value, p.text_size_normal),
                    ])

                    # FALLOFF
                    output_text.extend([
                        (" Falloff ", p.color_setting, p.text_size_normal),
                        (str(round(mod.falloff_radius, 2)), p.color_value, p.text_size_normal),
                        (units, p.color_value, p.text_size_normal)
                    ])

                if any([mod.start_position_object, mod.vertex_group, mod.texture_coords]) != 0:
                    output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                    # FROM
                    if mod.start_position_object:
                        output_text.extend([
                            (" From ", p.color_setting, p.text_size_normal),
                            (str(mod.start_position_object.name), p.color_value, p.text_size_normal),
                        ])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", p.color_setting, p.text_size_normal),
                            (str(mod.vertex_group), p.color_value, p.text_size_normal),
                        ])

                    # TEXTURES COORD
                    output_text.extend([
                        (" Texture Coords ", p.color_setting, p.text_size_normal),
                        (mod.texture_coords, p.color_value, p.text_size_normal),
                    ])

                    # OBJECT
                    if mod.texture_coords == "OBJECT":
                        if mod.texture_coords_object:
                            output_text.extend([
                                (" Object ", p.color_setting, p.text_size_normal),
                                (str(mod.texture_coords_object.name), p.color_value, p.text_size_normal),
                            ])
                        else:
                            output_text.extend([(" No Object Selected ", p.color_warning, p.text_size_normal)])

                    # UVs
                    if mod.texture_coords == "UV":
                        output_text.extend([(" UVMap ", p.color_setting, p.text_size_normal)])
                        if mod.uv_layer:
                            output_text.extend([(mod.uv_layer, p.color_value, p.text_size_normal)])
                        else:
                            output_text.extend([(" None ", p.color_warning, p.text_size_normal)])

                output_text.extend(["CR", ("----", p.color_title, p.text_size_normal)])

                # SPEED
                output_text.extend([
                    (" Speed ", p.color_setting, p.text_size_normal),
                    (str(round(mod.speed, 2)), p.color_value, p.text_size_normal),
                ])

                # SPEED
                # FIXME: Shows m when scale is cm
                output_text.extend([
                    (" Height ", p.color_setting, p.text_size_normal),
                    (str(round(mod.height, 2)), p.color_value, p.text_size_normal), (units, p.color_value, p.text_size_normal),
                ])

                # SPEED
                output_text.extend([
                    (" Width ", p.color_setting, p.text_size_normal),
                    (str(round(mod.width, 2)), p.color_value, p.text_size_normal),
                    (units, p.color_value, p.text_size_normal),
                ])

                # SPEED
                output_text.extend([
                    (" Narrowness ", p.color_setting, p.text_size_normal),
                    (str(round(mod.narrowness, 2)), p.color_value, p.text_size_normal),
                    (units, p.color_value, p.text_size_normal),
                ])

        else:
            output_text.extend([(" Hidden ", p.color_warning, p.text_size_normal)])

# ----------------------------------------------------------------------------------------------------------------------
# OBJECTS --------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------
# ARMATURE
# ---------------------------------------------------------------


def armature(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Armature, units) -> None:
    # obj = bpy.context.active_object

    # FIXME: Can we get this from the object rather than the context?
    active_bone = bpy.context.active_bone

    # BONE SELECTED
    if active_bone and obj.mode in {'POSE', 'EDIT'}:
        output_text.extend([
            "CR",
            ("BONE SELECTED ", p.color_title, p.text_size_normal),
            (active_bone.name, p.color_value, p.text_size_normal),
        ])

# ---------------------------------------------------------------
# CAMERA
# ---------------------------------------------------------------


def camera(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Camera, units) -> None:
    # obj = bpy.context.active_object

    # FIXME: Should this use the 'units' parameter?
    units_system = bpy.context.scene.unit_settings.system

    # LENS
    output_text.extend([
        "CR",
        ("LENS ", p.color_title, p.text_size_normal),
        (str(round(obj.data.lens, 2)), p.color_value, p.text_size_normal),
        ("mm", p.color_value, int(p.text_size_normal * 0.80)),
    ])

    # FOCUS
    if obj.data.dof.use_dof and obj.data.dof.focus_object:
        output_text.extend([
            "CR",
            ("FOCUS ", p.color_title, p.text_size_normal),
            (str(obj.data.dof.focus_object.name), p.color_value, p.text_size_normal),
        ])

    else:
        foc_dist = bpy.utils.units.to_string(units_system, 'LENGTH', obj.data.dof.focus_distance, precision=2)
        output_text.extend([
            "CR",
            ("DISTANCE ", p.color_title, p.text_size_normal),
            (foc_dist, p.color_value, p.text_size_normal),
        ])

    if bpy.context.object.data.dof.use_dof:
        output_text.extend([
            "CR",
            ("FSTOP ", p.color_title, p.text_size_normal),
            (str(round(obj.data.dof.aperture_fstop, 1)), p.color_value, p.text_size_normal),
        ])

# ---------------------------------------------------------------
# CURVE / FONT
# ---------------------------------------------------------------

# FIXME: What data type should obj be?


def curve_font(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, units) -> None:
    # obj = bpy.context.active_object

    # PREVIEW U
    output_text.extend([
        "CR",
        ("Preview U ", p.color_title, p.text_size_normal),
        (str(obj.data.resolution_u), p.color_value, p.text_size_normal),
    ])

    # RENDER PREVIEW U
    output_text.extend([
        (" Render U ", p.color_title, p.text_size_normal),
        (str(obj.data.render_resolution_u), p.color_value, p.text_size_normal),
    ])

    # FILL MODE
    output_text.extend([
        "CR",
        ("FILL ", p.color_title, p.text_size_normal), (str(
            obj.data.fill_mode.lower().capitalize()), p.color_value, p.text_size_normal),
    ])

    # OFFSET
    if obj.data.offset:
        output_text.extend(
            ["CR",
             ("Offset ", p.color_title, p.text_size_normal),
             (str(round(obj.data.offset, 2)), p.color_value, p.text_size_normal),
             ])

    # DEPTH
    if obj.data.bevel_depth:
        output_text.extend([
            "CR",
            ("DEPTH ", p.color_title, p.text_size_normal),
            (str(round(obj.data.bevel_depth, 2)), p.color_value, p.text_size_normal),
        ])

    # EXTRUDE
    if obj.data.extrude:
        output_text.extend([
            "CR",
            ("EXTRUDE ", p.color_title, p.text_size_normal),
            (str(round(obj.data.extrude, 2)), p.color_value, p.text_size_normal),
        ])

    # RESOLUTION
    if obj.data.bevel_resolution:
        output_text.extend([
            "CR",
            ("RESOLUTION ", p.color_title, p.text_size_normal),
            (str(obj.data.bevel_resolution), p.color_value, p.text_size_normal),
        ])
    # BEVEL
    if obj.data.bevel_object:
        output_text.extend([
            "CR",
            ("BEVEL ", p.color_title, p.text_size_normal),
            (obj.data.bevel_object.name, p.color_value, p.text_size_normal),
        ])

    # TAPER
    if obj.data.taper_object:
        output_text.extend([
            "CR",
            ("TAPER ", p.color_title, p.text_size_normal),
            (obj.data.taper_object.name, p.color_value, p.text_size_normal),
        ])

# ---------------------------------------------------------------
# EMPTY
# ---------------------------------------------------------------


def empty(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, units) -> None:
    # obj = bpy.context.active_object

    # ICON_OUTLINER_OB_EMPTY
    # TYPE
    output_text.extend([
        ("TYPE ", p.color_title, p.text_size_normal),
        (str(obj.empty_display_type.lower().capitalize()), p.color_value, p.text_size_normal),
    ])

    # SIZE
    output_text.extend([
        "CR",
        ("SIZE ", p.color_title, p.text_size_normal),
        (str(round(obj.empty_display_size, 2)), p.color_value, p.text_size_normal),
    ])

# ---------------------------------------------------------------
# LATTICE
# ---------------------------------------------------------------

# FIXME: What type should obj be?


def text_lattice(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, units) -> None:
    # obj = bpy.context.active_object

    # U -----------------------------------------------------------------------
    output_text.extend([
        "CR",
        ("U  ", p.color_title, p.text_size_normal),
        (str(obj.data.points_u), p.color_value, p.text_size_normal),
    ])

    # INTERPOLATION U
    output_text.extend([
        ("  ", p.color_title, p.text_size_normal),
        (str(obj.data.interpolation_type_u.split("_")[-1]), p.color_setting, p.text_size_normal),
    ])

# V -----------------------------------------------------------------------
    output_text.extend([
        "CR",
        ("V  ", p.color_title, p.text_size_normal),
        (str(obj.data.points_v), p.color_value, p.text_size_normal),
    ])

    # INTERPOLATION V
    output_text.extend([
        ("  ", p.color_title, p.text_size_normal),
        (str(obj.data.interpolation_type_v.split("_")[-1]), p.color_setting, p.text_size_normal),
    ])

# W -----------------------------------------------------------------------
    output_text.extend([
        "CR",
        ("W ", p.color_title, p.text_size_normal),
        (str(obj.data.points_w), p.color_value, p.text_size_normal),
    ])

    # INTERPOLATION W
    output_text.extend([
        ("  ", p.color_title, p.text_size_normal),
        (str(obj.data.interpolation_type_w.split("_")[-1]), p.color_setting, p.text_size_normal),
    ])

# ---------------------------------------------------------------
# LIGHTS
# ---------------------------------------------------------------

# FIXME: What data type should obj be?


def cycles_lights(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, units) -> None:
    # obj = bpy.context.active_object

    # TYPE
    if obj.data.type == 'AREA':
        output_text.extend([
            "CR",
            ("TYPE: ", p.color_title, p.text_size_normal),
            ("AREA ", p.color_setting, p.text_size_normal),
        ])

        # SQUARE
        if obj.data.shape == 'SQUARE':
            output_text.extend(["CR", ("SQUARE ", p.color_title, p.text_size_normal)])
            output_text.extend([
                "CR",
                ("SIZE ", p.color_title, p.text_size_normal),
                (str(round(obj.data.size, 2)), p.color_value, p.text_size_normal),
            ])
        # RECTANGLE
        elif obj.data.shape == 'RECTANGLE':
            # RECTANGLE
            output_text.extend(["CR", ("RECTANGLE ", p.color_title, p.text_size_normal)])
            # SIZE
            output_text.extend([
                "CR",
                ("SIZE X ", p.color_title, p.text_size_normal),
                (str(round(obj.data.size, 2)), p.color_value, p.text_size_normal),
            ])
            # SIZE Y
            output_text.extend([
                "CR",
                ("SIZE Y ", p.color_title, p.text_size_normal),
                (str(round(obj.data.size_y, 2)), p.color_value, p.text_size_normal),
            ])

    # POINT
    elif obj.data.type == 'POINT':
        output_text.extend(["CR",
                            ("TYPE: ", p.color_title, p.text_size_normal),
                            ("POINT ", p.color_setting, p.text_size_normal),
                            ])

        # SIZE
        output_text.extend([
            "CR",
            ("SIZE ", p.color_title, p.text_size_normal),
            (str(round(obj.data.shadow_soft_size, 2)), p.color_value, p.text_size_normal),
        ])

    # SUN
    elif obj.data.type == 'SUN':
        output_text.extend([
            "CR",
            ("TYPE: ", p.color_title, p.text_size_normal),
            ("SUN ", p.color_setting, p.text_size_normal),
        ])

        # SIZE
        output_text.extend([
            "CR",
            ("SIZE ", p.color_title, p.text_size_normal),
            (str(round(obj.data.shadow_soft_size, 2)), p.color_value, p.text_size_normal),
        ])

    elif obj.data.type == 'SPOT':
        output_text.extend([
            "CR",
            ("TYPE: ", p.color_title, p.text_size_normal),
            ("SPOT ", p.color_setting, p.text_size_normal),
        ])
        # SIZE
        output_text.extend([
            "CR",
            ("SIZE ", p.color_title, p.text_size_normal),
            (str(round(obj.data.shadow_soft_size, 2)), p.color_value, p.text_size_normal),
        ])

        # SHAPE
        output_text.extend([
            "CR",
            ("SHAPE ", p.color_title, p.text_size_normal),
            (str(round(math.degrees(obj.data.spot_size), 1)), p.color_value, p.text_size_normal),
            ("°", p.color_value, p.text_size_normal),
        ])

        # BLEND
        output_text.extend([
            "CR",
            ("SIZE ", p.color_title, p.text_size_normal),
            (str(round(obj.data.spot_blend, 2)), p.color_value, p.text_size_normal),
        ])

    # HEMI
    elif obj.data.type == 'HEMI':
        output_text.extend([
            "CR",
            ("TYPE: ", p.color_title, p.text_size_normal),
            ("HEMI ", p.color_setting, p.text_size_normal),
        ])
        # output_text.extend([("HEMI ", p.color_title, p.text_size_normal),
        #                   (str(round(bpy.data.node_groups["Shader Nodetree"].nodes["Emission"].inputs[1].default_value, 2)), p.color_value, p.text_size_normal)])

    # PORTAL
    if obj.data.cycles.is_portal:
        output_text.extend(["CR", ("PORTAL", p.color_title, p.text_size_normal)])

    else:
        # CAST SHADOW
        if obj.data.cycles.cast_shadow:
            output_text.extend(["CR", ("CAST SHADOW ", p.color_setting, p.text_size_normal)])
        # MULTIPLE IMPORTANCE
        if obj.data.cycles.use_multiple_importance_sampling:
            output_text.extend(["CR", ("MULTIPLE IMPORTANCE", p.color_setting, p.text_size_normal)])

# ---------------------------------------------------------------
# METABALL
# ---------------------------------------------------------------


def metaball(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.MetaBall, units) -> None:
    # obj = bpy.context.active_object

    # VIEW
    output_text.extend([
        "CR",
        ("VIEW ", p.color_title, p.text_size_normal),
        (str(round(obj.data.resolution, 2)), p.color_value, p.text_size_normal),
    ])

    # RENDER
    output_text.extend([
        "CR",
        ("RENDER ", p.color_title, p.text_size_normal),
        (str(round(obj.data.render_resolution, 2)), p.color_value, p.text_size_normal),
    ])

    # THRESHOLD
    output_text.extend([
        "CR",
        ("THRESHOLD ", p.color_title, p.text_size_normal),
        (str(round(obj.data.threshold, 2)), p.color_value, p.text_size_normal),
    ])

    # UPDATE
    output_text.extend([
        "CR",
        ("UPDATE ", p.color_title, p.text_size_normal),
        (obj.data.update_method.split("_")[-1], p.color_value, p.text_size_normal),
    ])


# ---------------------------------------------------------------
# WARNING
# ---------------------------------------------------------------
def warning(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object, units) -> None:
    # obj = bpy.context.active_object

    for mod in obj.modifiers:
        if mod.type in ['BEVEL', 'SOLIDIFY']:
            if obj.scale[0] != obj.scale[2] or obj.scale[1] != obj.scale[0] or obj.scale[1] != obj.scale[2]:
                # output_text.extend([
                #     "CR",
                #     ('ICON', 'ICON_ERROR.png'),
                #     (" Non-Uniform Scale ", p.color_setting, p.text_size_normal),
                # ])
                output_text.extend([
                    "CR",
                    (" Non-Uniform Scale ", p.color_warning, p.text_size_normal),
                ])


# ----------------------------------------------------------------------
# TEXTS
# ----------------------------------------------------------------------
# FIXME: explicitly support WELD
known_modifiers = {
    'BEVEL', 'ARRAY', 'SUBSURF', 'LATTICE', 'BOOLEAN', 'MIRROR', 'SOLIDIFY',
    'DECIMATE', 'EDGE_SPLIT', 'DISPLACE', 'MULTIRES', 'BUILD', 'ARMATURE',
    'MASK', 'REMESH', 'TRIANGULATE', 'SHRINKWRAP', 'WIREFRAME', 'SKIN', 'SCREW',
    'CURVE', 'MESH_DEFORM', 'LAPLACIANDEFORM', 'CAST', 'CORRECTIVE_SMOOTH',
    'HOOK', 'LAPLACIANSMOOTH', 'SIMPLE_DEFORM', 'SMOOTH', 'SURFACE_DEFORM',
    'WARP', 'WAVE', 'WEIGHTED_NORMAL',
}

# FIXME: Should we pass context, as well?


def infotext_key_text(p):
    units = ""

    # FIXME: Do we need to generate units/units_values for non-metric?
    if bpy.context.scene.unit_settings.system == 'METRIC':
        units_values = {1000: "km",
                        1: "m",
                        0.1: "dm",
                        0.01: "cm",
                        0.001: "mm",
                        0.0001: "µm",
                        0.3048: "'",
                        0.0254: '"',
                        }

        unit_scale = round(bpy.context.scene.unit_settings.scale_length, 6)
        units = units_values[unit_scale]

    # prefs = get_addon_preferences()
    # obj = bpy.context.active_object
    # wm = bpy.context.window_manager

    output_text = []

    # HELP
    # if show_keymaps:
    #     keymaps(output_text, p.color_title, p.color_setting, p.color_value,
    # text_size_normal, p.color_warning, p.color_option)

    # EXPERIMENTAL
    # detect a running modal, to display custom things if there
    # is one, IF we can figure out which modal is actually active
    # at any given moment
    # modal(output_text, p.color_title, p.color_setting, p.color_value,
    #   text_size_normal, p.color_warning, p.color_option, p.text_size_large)

    if p.show_view_perspective:
        # Make sure we don't conflict with the existing information
        # text, by telling it to fuck off if we have the view
        # perspective text enabled. This is SUPER-jenky. Not sure
        # if there's a better way to do this, but my money says 'yes'
        bpy.context.preferences.view.show_object_info = False
        bpy.context.preferences.view.show_view_name = False

        view(output_text, p)

        output_text.extend(["SPACE"])

    obj = bpy.context.active_object
    if obj is None:
        output_text.extend([("Active object not found", p.color_warning, p.text_size_normal)])
        return output_text

    # MODE
    if p.show_object_mode:
        mode(output_text, p)
        # SPACE
        output_text.extend(["SPACE"])

    # NAME
    if p.show_object_name:
        name(output_text, p, obj)
        # SPACE
        output_text.extend(["SPACE"])

    # LOCATION / ROTATION / SCALE
    if p.show_loc_rot_scale:
        loc(output_text, p, obj, units)

    # VERT/FACES/EDGES/NGONS
    if p.show_vert_face_tris:
        if obj.type == 'MESH':
            ngons(output_text, p, obj)
            # SPACE
            output_text.extend(["SPACE"])

    # MESH OPTIONS
    if p.show_object_info:
        # if bpy.context.object.mode in ['EDIT', 'OBJECT', 'WEIGHT_PAINT']:
        if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
            mesh_options(output_text, p, obj)

    # SCULPT
    if bpy.context.object.type == 'MESH' and bpy.context.object.mode == 'SCULPT':
        sculpt(output_text, p, obj, units)
        # SPACE
        output_text.extend(["SPACE"])


# ----------------------------------------------------------------------------------------------------------------------
# OBJECTS --------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    # ARMATURE
    if obj.type == 'ARMATURE':
        armature(output_text, p, obj, units)
        # SPACE
        output_text.extend(["SPACE"])

    # CAMERA
    if obj.type == 'CAMERA':
        camera(output_text, p, obj, units)
        # SPACE
        output_text.extend(["SPACE"])

    # CURVES / FONT
    if obj.type in ['CURVE', 'FONT']:
        curve_font(output_text, p, obj, units)
        if obj.modifiers:
            # SPACE
            output_text.extend(["CR", ("", p.color_title)])

    # EMPTY
    if obj.type == 'EMPTY':
        # SPACE
        output_text.extend([
            "CR",
            ("", p.color_title, p.text_size_normal),
        ])
        empty(output_text, p, obj, units)
        # SPACE
        output_text.extend(["SPACE"])

    # LATTICE
    if obj.type == 'LATTICE':
        text_lattice(output_text, p, obj, units)
        # SPACE
        output_text.extend(["SPACE"])

    # LIGHT
    if obj.type == 'LAMP':
        cycles_lights(output_text, p, obj, units)
        # SPACE
        output_text.extend(["SPACE"])

    # METABALL
    if obj.type == 'META':
        metaball(output_text, p, obj, units)
        # SPACE
        output_text.extend(["SPACE"])

# ----------------------------------------------------------------------
# MODIFIERS
# ----------------------------------------------------------------------
    wm = bpy.context.window_manager

    GREEN = (0.5, 1, 0, 1)
    NOIR = (0, 0, 0, 1)
    BLANC = (1, 1, 1, 1)

    if p.show_modifiers:
        # for mod in bpy.context.active_object.modifiers:
        for i, mod in enumerate(obj.modifiers):
            # FIXME: explicitly support WELD
            if mod.type not in known_modifiers:
                # Unknown modifier (which we should fix)
                if mod.show_viewport:
                    output_text.extend([
                        "CR",
                        (str(mod.type), p.color_title, p.text_size_normal),
                        ("  ", p.color_title, p.text_size_normal),
                        (str(mod.name), p.color_value, p.text_size_normal),
                    ])
                else:
                    output_text.extend([
                        "CR",
                        (str(mod.type), p.color_title, p.text_size_normal),
                        ("  ", p.color_title, p.text_size_normal),
                        (str(mod.name), p.color_value, p.text_size_normal),
                    ])
                    output_text.extend([
                        (" Hidden ", p.color_warning, p.text_size_normal),
                    ])

                output_text.extend([
                    (" (Unknown modifier)", p.color_warning, p.text_size_normal),
                ])

                continue

            # modifiers_list[mod]
            if mod.type == 'ARMATURE':
                mod_armature(output_text, p, obj, mod)

            if mod.type == 'ARRAY':
                mod_array(output_text, p, obj, mod, units)

            if mod.type == 'BEVEL':
                mod_bevel(output_text, p, obj, mod, units)

            if mod.type == 'BOOLEAN':
                mod_boolean(output_text, p, obj, mod, units)

            if mod.type == 'BUILD':
                mod_build(output_text, p, obj, mod, units)

            if mod.type == 'CAST':
                mod_cast(output_text, p, obj, mod, units)

            if mod.type == 'CORRECTIVE_SMOOTH':
                mod_corrective_smooth(output_text, p, obj, mod, units)

            if mod.type == 'CURVE':
                mod_curve(output_text, p, obj, mod, units)

            if mod.type == 'DECIMATE':
                mod_decimate(output_text, p, obj, mod, units)

            if mod.type == 'DISPLACE':
                mod_displace(output_text, p, obj, mod, units)

            if mod.type == 'EDGE_SPLIT':
                mod_edge_split(output_text, p, obj, mod, units)

            if mod.type == 'HOOK':
                mod_hook(output_text, p, obj, mod, units)

            if mod.type == 'LAPLACIANDEFORM':
                mod_laplacian_deformer(output_text, p, obj, mod, units)

            if mod.type == 'LAPLACIANSMOOTH':
                mod_laplacian_smooth(output_text, p, obj, mod, units)

            if mod.type == 'LATTICE':
                mod_lattice(output_text, p, obj, mod, units)

            if mod.type == 'MASK':
                mod_mask(output_text, p, obj, mod, units)

            if mod.type == 'MESH_DEFORM':
                mod_mesh_deform(output_text, p, obj, mod, units)

            if mod.type == 'MIRROR':
                mod_mirror(output_text, p, obj, mod, units)

            if mod.type == 'MULTIRES':
                mod_multires(output_text, p, obj, units)

            if mod.type == 'REMESH':
                mod_remesh(output_text, p, obj, mod, units)

            if mod.type == 'SCREW':
                mod_screw(output_text, p, obj, mod, units)

            if mod.type == 'SHRINKWRAP':
                mod_shrinkwrap(output_text, p, obj, mod, units)

            if mod.type == 'SIMPLE_DEFORM':
                mod_simple_deform(output_text, p, obj, mod, units)

            if mod.type == 'SKIN':
                mod_skin(output_text, p, obj, mod, units)

            if mod.type == 'SMOOTH':
                mod_smooth(output_text, p, obj, mod, units)

            if mod.type == 'SOLIDIFY':
                mod_solidify(output_text, p, obj, mod, units)

            if mod.type == 'SUBSURF':
                mod_subsurf(output_text, p, obj, mod, units)

            if mod.type == 'SURFACE_DEFORM':
                mod_surface_deform(output_text, p, obj, mod, units)

            if mod.type == 'TRIANGULATE':
                mod_triangulate(output_text, p, obj, mod, units)

            if mod.type == 'WARP':
                mod_warp(output_text, p, obj, mod, units)

            if mod.type == 'WAVE':
                mod_wave(output_text, p, obj, mod, units)

            if mod.type == 'WIREFRAME':
                mod_wireframe(output_text, p, obj, mod, units)

            if mod.type == 'WEIGHTED_NORMAL':
                mod_weighted_normals(output_text, p, obj, mod, units)

    # WARNING
    # SPACE
    output_text.extend(["SPACE"])
    warning(output_text, p, obj, units)

    # bpy.context.area.tag_redraw()
    return output_text


def register():
    # Add Text
    if infotext_text_Handle:
        bpy.types.SpaceView3D.draw_handler_remove(
            infotext_text_Handle[0], 'WINDOW')
    infotext_text_Handle[:] = [
        bpy.types.SpaceView3D.draw_handler_add(infotext_draw_text_callback, (), 'WINDOW', 'POST_PIXEL')]


def unregister():
    # Remove Text
    if infotext_text_Handle:
        bpy.types.SpaceView3D.draw_handler_remove(
            infotext_text_Handle[0], 'WINDOW')
        infotext_text_Handle[:] = []
