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
from ctypes import *
import math
# from math import degrees
from .functions import *
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
    # if addon_prefs.show_infotext and bpy.context.object is not None:
    if get_addon_preferences().show_infotext:
        infotext_draw_text_array(infotext_key_text())


def infotext_draw_text_array(output_text):
    addon_prefs = get_addon_preferences()
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
    text_size_max = addon_prefs.text_size_max
    text_size_mini = addon_prefs.text_size_mini
    infotext_text_shadow = addon_prefs.infotext_text_shadow
    infotext_shadow_color = addon_prefs.infotext_shadow_color
    infotext_shadow_alpha = addon_prefs.infotext_shadow_alpha
    infotext_offset_shadow_x = addon_prefs.infotext_offset_shadow_x
    infotext_offset_shadow_y = addon_prefs.infotext_offset_shadow_y
    infotext_text_pos_x = addon_prefs.infotext_text_pos_x * infotext_dpi
    infotext_text_pos_y = addon_prefs.infotext_text_pos_y * infotext_dpi
    infotext_text_space = addon_prefs.infotext_text_space

    text_size = min(text_size_max, max(text_size_mini, int(bpy.context.area.width / 100)))

    x = t_panel_width + infotext_text_pos_x
    y = bpy.context.region.height - infotext_text_pos_y

    # kinda lame that we use inline text strings as 'commands' but not worth
    # fixing right now.
    for command in output_text:
        if command == "SPACE" or command[0] == "SPACE":
            y_offset -= (text_size + infotext_text_space) / 2

        elif command == "CR" or command == "Carriage return":
            x_offset = 0
            y_offset -= text_size + infotext_text_space
            # space = int(text_size_max *5)

        elif len(command) == 3:
            Text, Color, Size = command
            # bgl.glColor3f(*Color)
            blf.color(0, *Color)
            blf.size(font_id, Size, 72)

            text_width, text_height = blf.dimensions(font_id, Text)
            if infotext_text_shadow:
                blf.enable(0, blf.SHADOW)
                blf.shadow_offset(0, infotext_offset_shadow_x, infotext_offset_shadow_y)
                blf.shadow(0, 3, infotext_shadow_color[0], infotext_shadow_color[1],
                           infotext_shadow_color[2], infotext_shadow_alpha)
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

    if infotext_text_shadow:
        blf.disable(0, blf.SHADOW)

    bpy.context.area.tag_redraw()


# utility function for floating point comparisons (needs python 3.6+)
def is_close(a, b, precision):
    return f'{a:.{precision}f}' == f'{b:.{precision}f}'


# ---------------------------------------------------------------
# TEST
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


def modal(output_text, color_title, color_setting, color_value,
          text_size_normal, color_warning, color_option, text_size_large):
    window = bpy.context.window
    win = cast(window.as_pointer(), POINTER(wmWindow)).contents

    handle = win.modalhandlers.first
    while handle:
        if handle.contents.type == WM_HANDLER_TYPE_OP:
            output_text.extend(["CR", ("Modal Running", color_title, text_size_normal)])
            # print("Modal running")
            break
        handle = handle.contents.next
    else:
        output_text.extend(["CR", ("No modal Running", color_title, text_size_normal)])
        # print("No running modals")


# ---------------------------------------------------------------
# VIEW
# ---------------------------------------------------------------
def r(x):
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
def view(output_text, color_title, color_setting, color_value,
         text_size_normal, color_warning, color_option, text_size_large):
    rd = bpy.context.region_data

    if rd.view_perspective == "CAMERA":
        output_text.extend(["CR", ("Camera Perspective", color_title, text_size_normal)])
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
        output_text.extend(["CR", (t, color_title, text_size_normal)])


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
    'EDIT_METABALL': 'EDIT LATTICE',
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


def mode(output_text, color_title, color_setting, color_value,
         text_size_normal, color_warning, color_option, text_size_large):
    mode = bpy.context.mode

    if mode in mode_strings:
        output_text.extend([
            "CR",
            (mode_strings[mode], color_title, text_size_large),
        ])
    else:
        output_text.extend([
            "CR",
            (mode_strings['default'], color_title, text_size_large),
        ])

    # Icons, just in case we figure out how to use them again
    # output_text.extend(["CR", ('ICON', 'ICON_OBJECT_DATAMODE.png'), ("   OBJECT MODE", color_title, text_size_deux)])
    # output_text.extend(["CR", ('ICON', 'ICON_EDITMODE_HLT.png'), ("   EDIT MODE", color_title, text_size_deux)])
    # output_text.extend(["CR", ('ICON', 'ICON_SCULPTMODE_HLT.png'), ("   SCULPT MODE", color_title, text_size_deux)])
    # output_text.extend(["CR", ('ICON', 'ICON_VPAINT_HLT.png'), ("    VERTEX PAINT MODE", color_title, text_size_deux)])
    # output_text.extend(["CR", ('ICON', 'ICON_WPAINT_HLT.png'), ("    WEIGHT PAINT MODE", color_title, text_size_deux)])
    # output_text.extend(["CR", ('ICON', 'ICON_TPAINT_HLT.png'), ("    TEXTURE PAINT MODE", color_title, text_size_deux)])
    # output_text.extend(["CR", ('ICON', 'ICON_PARTICLEMODE.png'), ("    PARTICLES EDIT MODE", color_title, text_size_deux)])
   # output_text.extend(["CR", ('ICON', 'ICON_POSE_HLT.png'), ("    POSE MODE", color_title, text_size_deux)])
    # output_text.extend(
    # ["CR", ('ICON', 'ICON_OBJECT_DATAMODE.png'), ("    ", color_setting, text_size_normal)])


# ---------------------------------------------------------------
# NAME
# ---------------------------------------------------------------


def name(output_text, color_title, color_setting, color_value,
         text_size_normal, color_warning, color_option, text_size_large):
    obj = bpy.context.active_object

    output_text.extend([
        "CR",
        ("", color_setting, int(text_size_normal * 5)),
        "CR",
        # (obj.type + ": ", color_title, text_size_normal),
        (obj.type, color_title, text_size_normal),
        "CR",
        "CR",
        (obj.name, color_value, int(text_size_large * 1.5)),
        "CR",
    ])

    # output_text.extend(["CR", (obj.type, color_title, text_size_normal)])
    # output_text.extend(["CR", ("Name: ", color_title, text_size_normal), (obj.name, color_value, text_size_normal)])

    # FIXME: enable icons once icon code is enabled
    # if obj.type == 'MESH':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_MESH.png'), ("    ", color_setting, text_size_normal)])
    #     output_text.extend(["CR", ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])
    # elif obj.type == 'CURVE':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_CURVE.png'), ("    ", color_setting, text_size_normal)])
    #     output_text.extend(["CR", ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])
    # elif obj.type == 'EMPTY':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_EMPTY.png'), ("    ", color_setting, text_size_normal)])
    #     output_text.extend(["CR", ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'CAMERA':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_CAMERA.png'), ("     ", color_setting, text_size_normal)])
    #     output_text.extend(["CR", ("     ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'LATTICE':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_LATTICE.png'), ("     ", color_setting, text_size_normal)])
    #     output_text.extend(["CR", ("     ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'META':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_META.png'), ("    ", color_setting, text_size_normal)])
    #     output_text.extend(["CR", ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'ARMATURE':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_ARMATURE.png'), ("    ", color_setting, text_size_normal)])
    #     output_text.extend(["CR", ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'FONT':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_FONT.png'), ("     ", color_setting, text_size_normal)])
    #     output_text.extend(["CR", ("     ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'LATTICE':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_LATTICE.png'), ("    ", color_setting, text_size_normal)])
    #     output_text.extend(["CR", ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'LAMP':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_LAMP.png'), ("    ", color_setting, text_size_normal)])
    #     output_text.extend(["CR", ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'SURFACE':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_SURFACE.png'), ("    ", color_setting, text_size_normal)])
    #     output_text.extend(["CR", ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'SPEAKER':
    #     # output_text.extend(["CR", ('ICON', 'ICON_OUTLINER_OB_SPEAKER.png'), ("    ", color_setting, text_size_normal)])
    #     output_text.extend(["CR", ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])


# ---------------------------------------------------------------
# LOCATION / ROTATION / SCALE
# ---------------------------------------------------------------


def loc(output_text, color_title, color_setting, color_value,
        text_size_normal, color_warning, color_option, units):
    obj = bpy.context.active_object

    axis_list = (" X ", " Y ", " Z ")
    # LOCATION
    if tuple(obj.location) != (0.0, 0.0, 0.0):
        # output_text.extend(["CR",("LOCATION ", color_title, text_size_normal),
        #                   ("  %s" % round(obj.location[0], 2), color_value, text_size_normal), (units, color_value, text_size_normal),
        #                   ("  %s" % round(obj.location[1], 2), color_value, text_size_normal), (units, color_value, text_size_normal),
        #                   ("  %s" % round(obj.location[2], 2), color_value, text_size_normal), (units, color_value, text_size_normal)])

        # output_text.extend(["CR", ('ICON', 'ICON_MAN_TRANS.png'), ("    ", color_title, text_size_normal)])
        output_text.extend(["CR", ("L: ", color_title, text_size_normal)])

        for idx, axis in enumerate(axis_list):
            output_text.extend([
                (axis, color_setting, text_size_normal),
                (str(round(obj.location[idx], 2)), color_value, text_size_normal),
                (units, color_value, text_size_normal)
            ])

    # ROTATION
    if tuple(obj.rotation_euler) != (0.0, 0.0, 0.0):
        # output_text.extend(["CR", ('ICON', 'ICON_MAN_ROT.png'), ("    ", color_title, text_size_normal)])
        output_text.extend(["CR", ("R: ", color_title, text_size_normal)])

        for idx, axis in enumerate(axis_list):
            output_text.extend([
                (axis, color_setting, text_size_normal),
                (str(round(math.degrees(obj.rotation_euler[idx]), 2)), color_value, text_size_normal),
                ("°", color_value, text_size_normal)
            ])

    # SCALE
    if tuple(obj.scale) != (1, 1, 1):
        # output_text.extend(["CR", ('ICON', 'ICON_MAN_SCALE.png'), ("    ", color_title, text_size_normal)])
        output_text.extend(["CR", ("S: ", color_title, text_size_normal)])

        for idx, axis in enumerate(axis_list):
            output_text.extend([
                (axis, color_setting, text_size_normal),
                (str(round(obj.scale[idx], 2)), color_value, text_size_normal),
            ])

        if not is_close(obj.scale[0], obj.scale[1], 3) or not is_close(obj.scale[1], obj.scale[2], 3):
            output_text.extend([
                (" Non-uniform ", color_warning, text_size_normal),
            ])

    if any([tuple(obj.location) != (0.0, 0.0, 0.0), tuple(obj.rotation_euler) != (0.0, 0.0, 0.0), tuple(obj.scale) != (1, 1, 1)]):
        # SPACE
        output_text.extend(["SPACE"])

# ---------------------------------------------------------------
# NGONS
# ---------------------------------------------------------------


def ngons(output_text, color_title, color_value, text_size_normal):
    obj = bpy.context.active_object
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
    # output_text.extend(["CR", ('ICON', 'vert.png'), ("    ", color_title, text_size_normal),
    #                   (str(vcount), color_value, text_size_normal)])
    output_text.extend([
        "CR",
        ("V: ", color_title, text_size_normal),
        (str(vcount), color_value, text_size_normal),
    ])

    # EDGES
    # output_text.extend([("  ", color_title, text_size_normal), ('ICON', 'edge.png'), ("    ", color_title, text_size_normal),
    #                   (str(ecount), color_value, text_size_normal)])
    output_text.extend([
        ("  E: ", color_title, text_size_normal),
        (" ", color_title, text_size_normal),
        (str(ecount), color_value, text_size_normal),
    ])

    # FACES
    # output_text.extend([("  ", color_title, text_size_normal), ('ICON', 'face.png'), ("    ", color_title, text_size_normal),
    #                   (str(fcount), color_value, text_size_normal)])
    output_text.extend([
        ("  F: ", color_title, text_size_normal),
        (" ", color_title, text_size_normal),
        (str(fcount), color_value, text_size_normal),
    ])

    if not bpy.context.object.mode == 'SCULPT':
        tcount = infotext.face_type_count['TRIS']
        ncount = infotext.face_type_count['NGONS']
        # TRIS
        if tcount:
            # output_text.extend([("  ", color_title, text_size_normal), ('ICON', 'triangle.png'), ("    ", color_title, text_size_normal),
            #                   (str(tcount), color_value, text_size_normal)])

            output_text.extend([
                ("  T: ", color_title, text_size_normal),
                (" ", color_title, text_size_normal),
                (str(tcount), color_value, text_size_normal),
            ])

        # NGONS ICON_OBJECT_DATA
        if ncount:
            # output_text.extend([(" ", color_title, text_size_normal), ('ICON', 'ngons.png'),
            #                   ("     ", color_title, text_size_normal), (str(ncount), color_value, text_size_normal)])

            output_text.extend([
                ("  N: ", color_title, text_size_normal),
                (" ", color_title, text_size_normal),
                (str(ncount), color_value, text_size_normal),
            ])

# ---------------------------------------------------------------
# MESH OPTIONS
# ---------------------------------------------------------------


def mesh_options(output_text, color_title, color_setting, color_value,
                 text_size_normal, color_warning, color_option):
    obj = bpy.context.active_object

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
                # output_text.extend(["CR", ('ICON', 'ICON_SMOOTH.png'),("     ", color_title, text_size_normal)])
                output_text.extend([
                    "CR",
                    ("MATERIAL: ", color_title, text_size_normal),
                ])
                output_text.extend([
                    (str(len(obj.material_slots)), color_setting, text_size_normal),
                    (" ", color_title, text_size_normal),
                    (str(obj.active_material.name), color_value, text_size_normal),
                ])

                if obj.active_material.users >= 2:
                    output_text.extend([
                        (" ", color_setting, text_size_normal),
                        (str(obj.active_material.users), color_setting, text_size_normal),
                        (" users", color_setting, text_size_normal),
                    ])
                if obj.active_material.use_fake_user:
                    output_text.extend([(" ,FAKE USER ", color_setting, text_size_normal)])
            else:
                output_text.extend(["CR", ("SLOT ONLY", color_title, text_size_normal)])

            # SPACE
            output_text.extend(["SPACE"])

    if obj.type == 'MESH':
        # AUTOSMOOTH
        if obj.data.use_auto_smooth:
            output_text.extend(["CR", ("AUTOSMOOTH ", color_title, text_size_normal)])
            # ANGLE
            output_text.extend([
                (" ANGLE ", color_setting, text_size_normal),
                (str(round(math.degrees(obj.data.auto_smooth_angle), 1)), color_value, text_size_normal),
                ("°", color_value, text_size_normal),
            ])

    if obj.type in ['MESH', 'LATTICE']:
        # VERTEX GROUPS
        if obj.vertex_groups:
            output_text.extend(["CR", ("VERTEX GROUPS", color_title, text_size_normal)])
            output_text.extend([
                (" ", color_title, text_size_normal),
                (str(len(obj.vertex_groups)), color_setting, text_size_normal),
            ])
            output_text.extend([
                (" ", color_title, text_size_normal),
                (str(obj.vertex_groups[int(obj.vertex_groups.active_index)].name), color_value, text_size_normal),
            ])

    if obj.type in ['CURVE', 'MESH', 'LATTICE']:
        # SHAPE KEYS
        if obj.data.shape_keys:
            output_text.extend(["CR", ("SHAPE KEYS", color_title, text_size_normal)])
            output_text.extend([
                (" ", color_title, text_size_normal),
                (str(len(obj.data.shape_keys.key_blocks)), color_setting, text_size_normal),
            ])
            output_text.extend([
                (" ", color_title, text_size_normal),
                (str(obj.data.shape_keys.key_blocks[int(
                    bpy.context.object.active_shape_key_index)].name), color_value, text_size_normal),
            ])

            if bpy.context.object.mode == 'OBJECT':
                output_text.extend([
                    (" VALUE ", color_setting, text_size_normal),
                    (str(round(obj.data.shape_keys.key_blocks[int(
                        bpy.context.object.active_shape_key_index)].value, 3)), color_value, text_size_normal),
                ])

    if obj.type == 'MESH':
        # UV's
        if obj.data.uv_layers:
            output_text.extend(["CR", ("UV's", color_title, text_size_normal)])
            output_text.extend([
                (" ", color_title, text_size_normal),
                (str(len(obj.data.uv_layers)), color_setting, text_size_normal),
            ])
            output_text.extend([
                (" ", color_title, text_size_normal),
                (str(
                    obj.data.uv_layers[int(obj.data.uv_layers.active_index)].name), color_value, text_size_normal),
            ])

        # VERTEX COLORS
        if obj.data.vertex_colors:
            output_text.extend(["CR", ("VERTEX COLORS", color_title, text_size_normal)])
            output_text.extend([
                (" ", color_title, text_size_normal),
                (str(len(obj.data.vertex_colors)), color_setting, text_size_normal),
            ])
            output_text.extend([
                (" ", color_title, text_size_normal),
                (str(obj.data.vertex_colors[int(obj.data.vertex_colors.active_index)].name),
                 color_value, text_size_normal),
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


def sculpt(output_text, color_title, color_setting, color_value,
           text_size_normal, color_warning, color_option, text_size_large, units):
    obj = bpy.context.active_object
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
    # output_text.extend(["CR", ('ICON', 'grab.png'), ("    ", color_setting, text_size_normal)])

    output_text.extend(["CR", (str(brush.name.upper()), color_title, text_size_large)])

    # SPACE
    output_text.extend(["SPACE"])

    # RADIUS
    output_text.extend([
        "CR",
        ("RADIUS ", color_setting, text_size_normal),
        (str(round(ups.size, 2)), color_value, text_size_normal),
        (" px", color_value, text_size_normal),
    ])
    # STRENGTH
    output_text.extend([
        "CR",
        ("STRENGTH ", color_setting, text_size_normal),
        (str(round(brush.strength, 3)), color_value, text_size_normal),
    ])

    # STRENGTH
    brush_autosmooth = bpy.data.brushes[brush.name].auto_smooth_factor
    if brush_autosmooth:
        output_text.extend([
            "CR",
            ("AUTOSMOOTH ", color_setting, text_size_normal),
            (str(round(brush_autosmooth, 3)), color_value, text_size_normal),
        ])

    brush_use_frontface = bpy.data.brushes[brush.name].use_frontface
    if bpy.data.brushes[brush.name].use_frontface:
        output_text.extend([
            "CR",
            ("FRONT FACE ", color_setting, text_size_normal),
            (str(brush_use_frontface), color_value, text_size_normal),
        ])

    # brush_stroke_method = bpy.data.brushes[brush.name].stroke_method
    # if brush_stroke_method == 'SPACE':
    #     output_text.extend(["CR", ("STROKE METHOD ", color_setting, text_size_normal)])
    #     output_text.extend(["SPACE"])
    # else:
    #     output_text.extend(["CR", ("STROKE METHOD ", color_setting, text_size_normal),
    #                       (str(brush_stroke_method), color_value, text_size_normal)])

    # SPACE
    output_text.extend(["SPACE"])

    if bpy.context.sculpt_object.use_dynamic_topology_sculpting:
        # SPACE
        output_text.extend(["SPACE"])

        # DYNTOPO
        output_text.extend(["CR", ("DYNTOPO ", color_title, text_size_large)])
        # SPACE
        output_text.extend(["SPACE"])

        if context_tool.detail_type_method == 'CONSTANT':

            output_text.extend([
                "CR",
                ("CONSTANT DETAIL ", color_setting, text_size_normal),
                (str(round(context_tool.constant_detail_resolution, 2)), color_value, text_size_normal),
            ])

        elif context_tool.detail_type_method == 'RELATIVE':
            output_text.extend([
                "CR",
                ("RELATIVE DETAIL ", color_setting, text_size_normal),
                (str(round(context_tool.detail_size, 2)), color_value,
                 text_size_normal),
                (" px", color_value, text_size_normal),
            ])
        else:
            output_text.extend([
                "CR",
                ("BRUSH DETAIL ", color_setting, text_size_normal),
                (str(round(context_tool.detail_percent, 2)), color_value,
                 text_size_normal),
                ("%", color_value, text_size_normal),
            ])

        # SUBDIV METHOD

        # SUBDIVIDE_COLLAPSE
        if context_tool.detail_refine_method == 'SUBDIVIDE_COLLAPSE':
            output_text.extend([
                "CR",
                (str("SUBDIVIDE COLLAPSE"), color_setting, text_size_normal),
            ])

        # COLLAPSE
        elif context_tool.detail_refine_method == 'COLLAPSE':
            output_text.extend(["CR", (str("COLLAPSE"), color_setting, text_size_normal)])

        # SUBDIVIDE
        else:
            output_text.extend(["CR", (str("SUBDIVIDE"), color_setting, text_size_normal)])

        # SMOOTH SHADING
        if context_tool.use_smooth_shading:
            output_text.extend(["CR", (str("SMOOTH SHADING"), color_value, text_size_normal)])

        # SYMMETRIZE DIRECTION
        output_text.extend([
            "CR",
            (str("SYMMETRIZE "), color_setting, text_size_normal),
            (str(context_tool.symmetrize_direction.lower().capitalize()), color_value, text_size_normal),
        ])

        # SPACE
        output_text.extend(["SPACE"])

    # SYMMETRIZE
    if any([context_tool.use_symmetry_x, context_tool.use_symmetry_y, context_tool.use_symmetry_z]):
        output_text.extend(["CR", (str("MIRROR"), color_setting, text_size_normal)])
        if context_tool.use_symmetry_x:
            output_text.extend([(str(" X "), color_value, text_size_normal)])
        if context_tool.use_symmetry_y:
            output_text.extend([(str(" Y "), color_value, text_size_normal)])
        if context_tool.use_symmetry_z:
            output_text.extend([(str(" Z "), color_value, text_size_normal)])

    if context_tool.use_symmetry_feather:
        output_text.extend(["CR", (str("FEATHER "), color_title, text_size_normal)])

    # LOCK
    if any([context_tool.lock_x, context_tool.lock_y, context_tool.lock_z]):
        output_text.extend(["CR", (str("LOCK  "), color_setting, text_size_normal)])
        if context_tool.lock_x:
            output_text.extend([(str(" X "), color_value, text_size_normal)])
        if context_tool.lock_y:
            output_text.extend([(str(" Y "), color_value, text_size_normal)])
        if context_tool.lock_z:
            output_text.extend([(str(" Z "), color_value, text_size_normal)])

    # TILE
    if any([context_tool.tile_x, context_tool.tile_y, context_tool.tile_z]):
        output_text.extend(["CR", (str("TILE    "), color_setting, text_size_normal)])
        if context_tool.tile_x:
            output_text.extend([(str(" X "), color_value, text_size_normal)])
        if context_tool.tile_y:
            output_text.extend([(str(" Y "), color_value, text_size_normal)])
        if context_tool.tile_z:
            output_text.extend([(str(" Z "), color_value, text_size_normal)])

# ----------------------------------------------------------------------------------------------------------------------
# MODIFIERS ------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------
# ARRAY
# ---------------------------------------------------------------


def mod_array(output_text, mod, color_title, color_setting, color_value,
              text_size_normal, color_warning, color_option, units,
              detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR",('ICON', 'ICON_MOD_ARRAY.png'),("    ", color_setting, text_size_normal), (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:

                # FIT MODE
                if mod.fit_type == 'FIXED_COUNT':
                    output_text.extend([(" Count ", color_setting, text_size_normal),
                                        (str(mod.count), color_value, text_size_normal)])

                elif mod.fit_type == 'FIT_CURVE':
                    if mod.curve:
                        # Object
                        output_text.extend([(" Curve ", color_setting, text_size_normal),
                                            (mod.curve.name, color_value, text_size_normal)])
                    else:
                        output_text.extend([(" No Curve Selected", color_warning, text_size_normal)])

                else:
                    output_text.extend([(" Length ", color_setting, text_size_normal),
                                        (str(round(mod.fit_length, 2)), color_value, text_size_normal)])

                # CONSTANT
                if mod.use_constant_offset:
                    # output_text.extend([(" Constant ", color_setting, text_size_normal),
                    #                   ("%s" %round(mod.constant_offset_displace[0], 1),color_value, text_size_normal),
                    #                   ("  %s" %round(mod.constant_offset_displace[1], 1),color_value, text_size_normal),
                    #                   ("  %s" %round(mod.constant_offset_displace[2], 1),color_value, text_size_normal)])

                    output_text.extend([(" Constant ", color_setting, text_size_normal)])

                    # X
                    if mod.constant_offset_displace[0] != 0:
                        output_text.extend([
                            (" X ", color_setting, text_size_normal),
                            (str(round(mod.constant_offset_displace[0], 1)), color_value, text_size_normal),
                            (units, color_value, text_size_normal),
                        ])

                    # Y
                    if mod.constant_offset_displace[1] != 0:
                        output_text.extend([
                            (" Y ", color_setting, text_size_normal),
                            (str(round(mod.constant_offset_displace[1], 1)), color_value, text_size_normal),
                            (units, color_value, text_size_normal),
                        ])

                    # Z
                    if mod.constant_offset_displace[2] != 0:
                        output_text.extend([
                            (" Z ", color_setting, text_size_normal),
                            (str(round(mod.constant_offset_displace[2], 1)), color_value, text_size_normal),
                            (units, color_value, text_size_normal),
                        ])

                # RELATIVE
                elif mod.use_relative_offset:
                    output_text.extend([(" Relative ", color_setting, text_size_normal)])

                    # X
                    if mod.relative_offset_displace[0] != 0:
                        output_text.extend([
                            (" X ", color_setting, text_size_normal),
                            (str(round(mod.relative_offset_displace[0], 1)), color_value, text_size_normal),
                        ])

                    # Y
                    if mod.relative_offset_displace[1] != 0:
                        output_text.extend([
                            (" Y ", color_setting, text_size_normal),
                            (str(round(mod.relative_offset_displace[1], 1)), color_value, text_size_normal),
                        ])

                    # Z
                    if mod.relative_offset_displace[2] != 0:
                        output_text.extend([
                            (" Z ", color_setting, text_size_normal),
                            (str(round(mod.relative_offset_displace[2], 1)), color_value, text_size_normal),
                        ])

                # MERGE
                if mod.use_merge_vertices:
                    output_text.extend([
                        (" Merge ", color_setting, text_size_normal),
                        (str(round(mod.merge_threshold, 3)), color_value, text_size_normal),
                    ])

                    if mod.use_merge_vertices_cap:
                        output_text.extend([(" First Last ", color_setting, text_size_normal)])

                # OPTIONS
                if any([mod.use_object_offset, mod.start_cap, mod.end_cap]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # OBJECT OFFSET
                    if mod.use_object_offset:
                        if mod.offset_object:
                            output_text.extend([
                                (" Object Offset ", color_setting, text_size_normal),
                                (mod.offset_object.name, color_value, text_size_normal),
                            ])
                        else:
                            output_text.extend([
                                (" No Object Selected", color_warning, text_size_normal),
                            ])

                    # STAR CAP
                    if mod.start_cap:
                        output_text.extend([
                            (" Start Cap ", color_setting, text_size_normal),
                            (mod.start_cap.name, color_value, text_size_normal),
                        ])

                    # END CAP
                    if mod.end_cap:
                        output_text.extend([
                            (" End Cap ", color_setting, text_size_normal),
                            (mod.end_cap.name, color_value, text_size_normal),
                        ])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])


# ---------------------------------------------------------------
# BEVEL
# ---------------------------------------------------------------
def mod_bevel(output_text, mod, color_title, color_setting, color_value, text_size_normal, color_warning, color_option, units, detailed_modifiers):
    wm = bpy.context.window_manager
    obj = bpy.context.active_object

    if obj.type in {'MESH', 'CURVE', 'FONT'}:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_BEVEL.png'), ("     ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])

        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # AFFECT
                output_text.extend([
                    (" Affect ", color_setting, text_size_normal),
                    (mod.affect, color_value, text_size_normal),
                ])

                # OFFSET TYPE
                output_text.extend([
                    (" Method ", color_setting, text_size_normal),
                    (str(mod.offset_type.lower().capitalize()), color_value, text_size_normal),
                ])

                # WIDTH
                output_text.extend([
                    (" Width ", color_setting, text_size_normal),
                    (str(round(mod.width, 2)), color_value, text_size_normal),

                ])

                if mod.offset_type == "PERCENT":
                    output_text.extend([
                        ("%", color_value, text_size_normal),
                    ])
                else:
                    output_text.extend([
                        (units, color_value, text_size_normal),
                    ])

                # SEGMENTS
                output_text.extend([
                    (" Segments ", color_setting, text_size_normal),
                    (str(mod.segments), color_value, text_size_normal),
                ])

                # PROFILE
                output_text.extend([
                    (" Profile ", color_setting, text_size_normal),
                    (str(round(mod.profile, 2)), color_value, text_size_normal),
                ])

                # FIXME: Support material index
                # MATERIAL
                # output_text.extend([])

                # OPTIONS
                output_text.extend(["CR", ("----", color_title, text_size_normal)])

                # LIMIT METHOD
                output_text.extend([
                    (" Limit ", color_setting, text_size_normal),
                    (str(mod.limit_method.lower().capitalize()), color_value, text_size_normal),
                ])

                # ANGLE
                if mod.limit_method == 'ANGLE':
                    output_text.extend([
                        (":", color_setting, text_size_normal),
                        (str(round(math.degrees(mod.angle_limit), 2)), color_value, text_size_normal),
                        ("°", color_value, text_size_normal),
                    ])

                # VERTEX GROUP
                elif mod.limit_method == 'VGROUP':
                    if mod.vertex_group:
                        output_text.extend([
                            (":", color_setting, text_size_normal),
                            (str(mod.vertex_group), color_value, text_size_normal),
                        ])
                    else:
                        output_text.extend([
                            (":", color_setting, text_size_normal),
                            ("None", color_warning, text_size_normal),
                        ])

                # LOOP SLIDE
                if mod.loop_slide:
                    output_text.extend([(" Loop Slide ", color_setting, text_size_normal)])

                # CLAMP
                if mod.use_clamp_overlap:
                    output_text.extend([(" Clamp ", color_setting, text_size_normal)])

                # HARDEN NORMALS
                if mod.harden_normals:
                    output_text.extend([(" Harden ", color_setting, text_size_normal)])

                if mod.mark_seam:
                    output_text.extend([(" Mark Seam ", color_setting, text_size_normal)])

                if mod.mark_sharp:
                    output_text.extend([(" Mark Sharp ", color_setting, text_size_normal)])

                # ONLY VERTICES
                # if mod.use_only_vertices:
                #     output_text.extend([(" Only Vertices ", color_setting, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# BOOLEAN
# ---------------------------------------------------------------


def mod_boolean(output_text, mod, color_title, color_setting, color_value,
                text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_BOOLEAN.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # OPERATION
                output_text.extend([(" ", color_title, text_size_normal),
                                    (str(mod.operation), color_value, text_size_normal)])
                if mod.object:
                    # Object
                    output_text.extend([(" Object ", color_setting, text_size_normal),
                                        (mod.object.name, color_value, text_size_normal)])
                else:
                    output_text.extend([(" No object Selected", color_warning, text_size_normal)])

                # SOLVER
                # if (hasattr(bpy.context.preferences.system, 'opensubdiv_compute_type')):
                # if bpy.app.version == (2, 79, 0):
                #     output_text.extend([(" ", color_title, text_size_normal),
                #                           (str(mod.solver.upper()), color_value, text_size_normal)])

                # OVERLAP THRESHOLD
                # if mod.solver == 'BMESH':
                #     if mod.double_threshold > 0 :
                #         output_text.extend([(" Overlap Threshold ", color_setting, text_size_normal),
                #                           (str(round(mod.double_threshold,2)), color_value, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# BUILD
# ---------------------------------------------------------------


def mod_build(output_text, mod, color_title, color_setting, color_value,
              text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_BUILD.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # START
                output_text.extend([
                    (" Start ", color_setting, text_size_normal),
                    (str(round(mod.frame_start, 2)), color_value, text_size_normal),
                ])

                # LENGTH
                output_text.extend([
                    (" Length ", color_setting, text_size_normal),
                    (str(round(mod.frame_duration, 2)), color_value, text_size_normal),
                ])

                # SEED
                if mod.use_random_order:
                    output_text.extend([
                        (" Seed ", color_setting, text_size_normal),
                        (str(mod.seed), color_value, text_size_normal),
                    ])

                if mod.use_reverse:
                    output_text.extend([(" Reversed ", color_setting, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# DECIMATE
# ---------------------------------------------------------------


def mod_decimate(output_text, mod, color_title, color_setting, color_value,
                 text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_DECIM.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # COLLAPSE
                if mod.decimate_type == 'COLLAPSE':
                    output_text.extend([(" Collapse ", color_setting, text_size_normal)])
                    output_text.extend([
                        (" Ratio ", color_setting, text_size_normal),
                        (str(round(mod.ratio, 2)), color_value, text_size_normal),
                    ])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", color_setting, text_size_normal),
                            (str(mod.vertex_group), color_value, text_size_normal),
                        ])

                        # FACTOR
                        output_text.extend([
                            (" Factor ", color_setting, text_size_normal),
                            (str(round(mod.vertex_group_factor, 2)), color_value, text_size_normal),
                        ])
                    # OPTIONS
                    if any([mod.use_collapse_triangulate, mod.use_symmetry]):
                        output_text.extend(["CR", ("----", color_title, text_size_normal)])

                        # TRIANGULATE
                        if mod.use_collapse_triangulate:
                            output_text.extend([(" Triangulate ", color_setting, text_size_normal)])

                        # SYMMETRY
                        if mod.use_symmetry:
                            output_text.extend([(" Symmetry ", color_setting, text_size_normal),
                                                (str(mod.symmetry_axis), color_value, text_size_normal)])

                # UN-SUBDIVDE
                elif mod.decimate_type == 'UNSUBDIV':
                    output_text.extend([(" Un-subdivide ", color_setting, text_size_normal)])
                    output_text.extend([(" Iteration ", color_setting, text_size_normal),
                                        (str(round(mod.iterations, 2)), color_value, text_size_normal)])
                # PLANAR
                else:
                    output_text.extend([(" Planar ", color_setting, text_size_normal)])
                    output_text.extend([(" Angle Limit ", color_setting, text_size_normal), (
                        str(round(math.degrees(mod.angle_limit), 1)), color_value, text_size_normal),
                        ("°", color_value, text_size_normal)])

                    # OPTIONS
                    if any([mod.use_dissolve_boundaries, mod.delimit]):
                        output_text.extend(["CR", ("----", color_title, text_size_normal)])

                        # ALL BOUNDARIES
                        if mod.use_dissolve_boundaries:
                            output_text.extend([(" All Boundaries ", color_setting, text_size_normal)])

                        # DELIMIT
                        if mod.delimit:
                            output_text.extend([(" Delimit ", color_setting, text_size_normal)])
                            if mod.delimit == {'NORMAL'}:
                                output_text.extend([(" NORMAL ", color_value, text_size_normal)])
                            elif mod.delimit == {'MATERIAL'}:
                                output_text.extend([(" MATERIAL ", color_value, text_size_normal)])
                            elif mod.delimit == {'SEAM'}:
                                output_text.extend([(" SEAM ", color_value, text_size_normal)])
                            elif mod.delimit == {'SHARP'}:
                                output_text.extend([(" SHARP ", color_value, text_size_normal)])
                            elif mod.delimit == {'UV'}:
                                output_text.extend([(" UV ", color_value, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# EDGE SPLIT
# ---------------------------------------------------------------


def mod_edge_split(output_text, mod, color_title, color_setting, color_value,
                   text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_EDGESPLIT.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # EDGE ANGLE
                if mod.use_edge_angle:
                    output_text.extend([(" Edges angle ", color_setting, text_size_normal), (
                        str(round(math.degrees(mod.split_angle), 1)), color_value, text_size_normal),
                        ("°", color_value, text_size_normal)])

                # SHARP EDGES
                if mod.use_edge_sharp:
                    output_text.extend([(" Sharp Edges ", color_setting, text_size_normal)])
        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# WEIGHTED NORMALS
# ---------------------------------------------------------------


def mod_weighted_normals(output_text, mod, color_title, color_setting,
                         color_value, text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_EDGESPLIT.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # Mode
                # output_text.extend([(" Mode", color_setting, text_size_normal), (str(mod.mode.lower().capitalize()), color_setting, text_size_normal)])
                output_text.extend([(" Mode ", color_setting, text_size_normal), (str(
                    mod.mode.lower().capitalize()), color_value, text_size_normal)])

                # Weight
                output_text.extend([(" Weight ", color_setting, text_size_normal),
                                    (str(round(mod.weight, 2)), color_value, text_size_normal)])

                # STRENGTH
                output_text.extend([(" Strength ", color_setting, text_size_normal),
                                    (str(round(mod.weight, 2)), color_value, text_size_normal)])

                # THRESHOLD
                output_text.extend([(" Threshold ", color_setting, text_size_normal),
                                    (str(round(mod.thresh, 2)), color_value, text_size_normal)])

                if any([mod.keep_sharp, mod.face_influence, mod.vertex_group]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])
                    # KEEP SHARP
                    if mod.keep_sharp:
                        output_text.extend([(" Keep Sharp ", color_setting, text_size_normal)])

                    # KEEP SHARP
                    if mod.face_influence:
                        output_text.extend([(" Face Influence ", color_setting, text_size_normal)])

                    if mod.vertex_group:
                        output_text.extend([(" Vgroup ", color_setting, text_size_normal),
                                            (str(mod.vertex_group), color_value, text_size_normal)])
                    else:
                        output_text.extend([(" No Vertex Group Selected ", color_warning, text_size_normal)])
        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# LATTICE
# ---------------------------------------------------------------


def mod_lattice(output_text, mod, color_title, color_setting, color_value,
                text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_LATTICE.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                output_text.extend([(" Object ", color_setting, text_size_normal)])
                if mod.object:
                    # OBJECT
                    output_text.extend([(mod.object.name, color_value, text_size_normal)])
                else:
                    output_text.extend([(" None ", color_warning, text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([(" VGroup ", color_setting, text_size_normal),
                                        (str(mod.vertex_group), color_value, text_size_normal)])

                # STRENGTH
                output_text.extend([(" Strength ", color_setting, text_size_normal),
                                    (str(round(mod.strength, 2)), color_value, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# MASK
# ---------------------------------------------------------------


def mod_mask(output_text, mod, color_title, color_setting, color_value,
             text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MASK.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # ARMATURE
                if mod.mode == 'ARMATURE':
                    if mod.armature:
                        output_text.extend([(" Armature ", color_setting, text_size_normal),
                                            (str(mod.armature.name), color_value, text_size_normal)])
                    else:
                        output_text.extend([(" No Armature Selected ", color_warning, text_size_normal)])

                # VERTEX GROUP
                elif mod.mode == 'VERTEX_GROUP':
                    if mod.vertex_group:
                        output_text.extend([(" VGroup ", color_setting, text_size_normal),
                                            (str(mod.vertex_group), color_value, text_size_normal)])
                    else:
                        output_text.extend([(" No Vertex Group Selected ", color_warning, text_size_normal)])
        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# MIRROR
# ---------------------------------------------------------------


def mod_mirror(output_text, mod, color_title, color_setting, color_value,
               text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MIRROR.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                if any([mod.use_axis[0], mod.use_axis[1], mod.use_axis[2]]):
                    output_text.extend([(" Axis ", color_setting, text_size_normal)])
                    # X
                    if mod.use_axis[0]:
                        output_text.extend([(" X ", color_value, text_size_normal)])

                    # Y
                    if mod.use_axis[1]:
                        output_text.extend([(" Y ", color_value, text_size_normal)])

                    # Z
                    if mod.use_axis[2]:
                        output_text.extend([(" Z ", color_value, text_size_normal)])

                # OBJECT
                if mod.mirror_object:
                    output_text.extend([(" Object ", color_setting, text_size_normal),
                                        (mod.mirror_object.name, color_value, text_size_normal)])

                # MERGE
                if mod.use_mirror_merge:
                    output_text.extend([
                        (" Merge ", color_setting, text_size_normal),
                        (str(round(mod.merge_threshold, 3)), color_value, text_size_normal),
                        (units, color_value, text_size_normal),
                    ])

                # OPTIONS
                if any([mod.use_clip, mod.use_mirror_vertex_groups, mod.use_mirror_u, mod.use_mirror_v]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])
                    # CLIPPING
                    if mod.use_clip:
                        output_text.extend([(" Clipping ", color_setting, text_size_normal)])

                    # VERTEX GROUP
                    if mod.use_mirror_vertex_groups:
                        output_text.extend([(" VGroup ", color_setting, text_size_normal)])

                    # TEXTURES
                    if any([mod.use_mirror_u, mod.use_mirror_v]):
                        output_text.extend([(" Textures ", color_setting, text_size_normal)])

                    # TEXTURE U
                    if mod.use_mirror_u:
                        output_text.extend([
                            (" U ", color_setting, text_size_normal),
                            (str(round(mod.mirror_offset_u, 3)), color_value, text_size_normal),
                            (units, color_value, text_size_normal)
                        ])

                    # TEXTURE V
                    if mod.use_mirror_v:
                        output_text.extend([
                            (" V ", color_setting, text_size_normal),
                            (str(round(mod.mirror_offset_v, 3)), color_value, text_size_normal),
                            (units, color_value, text_size_normal)
                        ])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# MULTIRES
# ---------------------------------------------------------------


def mod_multires(output_text, mod, color_title, color_setting, color_value,
                 text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MULTIRES.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])

        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # SUBDIVISION TYPE
                if mod.subdivision_type == 'SIMPLE':
                    output_text.extend([(" Simple ", color_setting, text_size_normal)])
                else:
                    output_text.extend([(" Catmull Clark ", color_setting, text_size_normal)])

                # QUALITY
                output_text.extend([
                    (" Quality ", color_setting, text_size_normal),
                    (str(mod.quality), color_value, text_size_normal)
                ])

                # RENDER SUBDIVISION LEVELS
                output_text.extend([
                    (" Render ", color_setting, text_size_normal),
                    (str(mod.render_levels), color_value, text_size_normal)
                ])

                # VIEWPORT SUBDIVISION LEVELS
                output_text.extend([
                    (" Preview ", color_setting, text_size_normal),
                    (str(mod.levels), color_value, text_size_normal)
                ])

                # FIXME: We need a dynamic wrap here
                if any([mod.uv_smooth == "PRESERVE_CORNERS", mod.show_only_control_edges, mod.use_creases]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                # UV SMOOTHING
                if mod.uv_smooth == "PRESERVE_CORNERS":
                    output_text.extend([
                        (" UV Smoothing (keep corners) ", color_setting, text_size_normal),
                    ])

                # OPTIMAL DISPLAY
                if mod.show_only_control_edges:
                    output_text.extend([(" Optimal Display ", color_setting, text_size_normal)])

                if mod.use_creases:
                    output_text.extend([(" Using Creases ", color_setting, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# REMESH
# ---------------------------------------------------------------


def mod_remesh(output_text, mod, color_title, color_setting, color_value,
               text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_REMESH.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                output_text.extend([(" ", color_title, text_size_normal),
                                    (str(mod.mode), color_value, text_size_normal)])

                if mod.mode != "VOXEL":
                    # OCTREE DEPTH
                    output_text.extend([(" Octree Depth ", color_setting, text_size_normal),
                                        (str(mod.octree_depth), color_value, text_size_normal)])

                    # SCALE
                    output_text.extend([(" Scale ", color_setting, text_size_normal),
                                        (str(round(mod.scale, 2)), color_value, text_size_normal)])

                # SHARPNESS
                if mod.mode == 'SHARP':
                    output_text.extend([(" Sharpness ", color_setting, text_size_normal),
                                        (str(round(mod.sharpness, 2)), color_value, text_size_normal)])

                # OPTIONS
                if any([mod.use_smooth_shade, mod.use_remove_disconnected]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # SMOOTH SHADING
                    if mod.use_smooth_shade:
                        output_text.extend([(" Smooth Shading ", color_setting, text_size_normal)])

                    # REMOVE DISCONNECTED
                    if mod.mode != "VOXEL" and mod.use_remove_disconnected:
                        output_text.extend([(" Remove Disconnected Pieces ", color_setting, text_size_normal),
                                            (str(round(mod.threshold, 2)), color_value, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# SCREW
# ---------------------------------------------------------------


# FIXME: AUpdate for 2.8x
def mod_screw(output_text, mod, color_title, color_setting, color_value,
              text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SCREW.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # AXIS
                output_text.extend([
                    (" Axis ", color_setting, text_size_normal),
                    (str(mod.axis), color_value, text_size_normal)
                ])

                # AXIS OBJECT
                if mod.object:
                    output_text.extend([
                        (" Axis Object ", color_setting, text_size_normal),
                        (str(mod.object.name), color_value, text_size_normal)
                    ])

                # SCREW
                output_text.extend([
                    (" Screw ", color_setting, text_size_normal),
                    (str(round(mod.screw_offset, 2)), color_value, text_size_normal),
                    (units, color_value, text_size_normal)
                ])

                # ITERATIONS
                output_text.extend([
                    (" Iterations ", color_setting, text_size_normal),
                    (str(round(mod.iterations, 2)), color_value, text_size_normal)
                ])

                # Angle
                output_text.extend([
                    (" Angle ", color_setting, text_size_normal),
                    (str(round(math.degrees(mod.angle), 1)), color_value, text_size_normal),
                    ("°", color_value, text_size_normal)
                ])

                # STEPS
                output_text.extend([
                    (" Steps ", color_setting, text_size_normal),
                    (str(round(mod.steps, 2)), color_value, text_size_normal)
                ])

                # OPTIONS LINE 1
                if any([mod.use_normal_flip, mod.use_smooth_shade, mod.use_object_screw_offset,
                        mod.use_normal_calculate]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # USE FLIP
                    if mod.use_normal_flip:
                        output_text.extend([(" Flip ", color_setting, text_size_normal)])

                    # USE SMOOTH SHADE
                    if mod.use_smooth_shade:
                        output_text.extend([(" Smooth Shading ", color_setting, text_size_normal)])

                    # USE OBJECT SCREW OFFSET
                    # if mod.object:
                    if mod.use_object_screw_offset:
                        output_text.extend([(" Object Screw ", color_setting, text_size_normal)])

                    # CALC ORDER
                    if mod.use_normal_calculate:
                        output_text.extend([(" Calc Order ", color_setting, text_size_normal)])

                # OPTIONS LINE 2
                if any([mod.use_merge_vertices, mod.use_stretch_u, mod.use_stretch_v]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])
                    # USE MERGE VERTICES
                    if mod.use_merge_vertices:
                        output_text.extend([
                            (" Merge Vertices ", color_setting, text_size_normal),
                            (str(round(mod.merge_threshold, 2)), color_value, text_size_normal),
                            (units, color_value, text_size_normal)
                        ])

                    # STRETCH U
                    if mod.use_stretch_u:
                        output_text.extend([(" Stretch U ", color_setting, text_size_normal)])

                    # STRETCH V
                    if mod.use_stretch_v:
                        output_text.extend([(" Stretch V ", color_setting, text_size_normal)])
        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# SKIN
# ---------------------------------------------------------------


def mod_skin(output_text, mod, color_title, color_setting, color_value,
             text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SKIN.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # BRANCH SMOOTHING
                if mod.branch_smoothing != 0:
                    output_text.extend([(" Branch Smoothing ", color_setting, text_size_normal),
                                        (str(round(mod.branch_smoothing, 3)), color_value, text_size_normal)])

                if any([mod.use_x_symmetry, mod.use_y_symmetry, mod.use_z_symmetry]):
                    # SYMMETRY
                    output_text.extend([(" Symmetry ", color_setting, text_size_normal)])

                    # X
                    if mod.use_x_symmetry:
                        output_text.extend([(" X ", color_value, text_size_normal)])

                    # Y
                    if mod.use_y_symmetry:
                        output_text.extend([(" Y ", color_value, text_size_normal)])

                    # Z
                    if mod.use_z_symmetry:
                        output_text.extend([(" Z ", color_value, text_size_normal)])

                # OPTIONS
                if any([mod.use_smooth_shade]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # SMOOTH SHADING
                    if mod.use_smooth_shade:
                        output_text.extend([(" Smooth Shading ", color_setting, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# SOLIDIFY
# ---------------------------------------------------------------

# FIXME: Needs to support 'complex' mode


def mod_solidify(output_text, mod, color_title, color_setting, color_value,
                 text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SOLIDIFY.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # THICKNESS
                output_text.extend([
                    (" Thickness ", color_setting, text_size_normal),
                    (str(round(mod.thickness, 3)), color_value, text_size_normal),
                    (units, color_value, text_size_normal)
                ])

                # OFFSET
                output_text.extend([
                    (" Offset ", color_setting, text_size_normal),
                    (str(round(mod.offset, 2)), color_value, text_size_normal)
                ])

                # CLAMP
                if mod.thickness_clamp != 0:
                    output_text.extend([
                        (" Clamp ", color_setting, text_size_normal),
                        (str(round(mod.thickness_clamp, 2)), color_value, text_size_normal)
                    ])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([
                        (" VGroup ", color_setting, text_size_normal),
                        (str(mod.vertex_group), color_value, text_size_normal)
                    ])

                    # THICKNESS VGROUP
                    output_text.extend([
                        (" Clamp ", color_setting, text_size_normal),
                        (str(round(mod.thickness_vertex_group, 2)), color_value, text_size_normal)
                    ])

                # OPTIONS LIGNE 1
                if any([mod.use_flip_normals, mod.use_even_offset, mod.use_quality_normals, mod.use_rim]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # FLIP NORMALS
                    if mod.use_flip_normals:
                        output_text.extend([(" Flip Normals ", color_setting, text_size_normal)])

                    # USE EVEN OFFSET
                    if mod.use_even_offset:
                        output_text.extend([(" Even Thickness ", color_setting, text_size_normal)])

                    # HIGH QUALITY NORMALS
                    if mod.use_quality_normals:
                        output_text.extend([(" High Quality Normals ", color_setting, text_size_normal)])

                    # USE RIM
                    if mod.use_rim:
                        output_text.extend([(" Fill Rim ", color_setting, text_size_normal)])

                        # ONLY RIM
                        if mod.use_rim_only:
                            output_text.extend([(" Only rims ", color_setting, text_size_normal)])

                # OPTIONS LIGNE 2
                if any([mod.edge_crease_inner, mod.edge_crease_outer, mod.edge_crease_rim]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # INNER
                    if mod.edge_crease_inner != 0:
                        output_text.extend([
                            (" Inner ", color_setting, text_size_normal),
                            (str(round(mod.edge_crease_inner, 2)), color_value, text_size_normal)
                        ])

                    # OUTER
                    if mod.edge_crease_outer != 0:
                        output_text.extend([
                            (" Outer ", color_setting, text_size_normal),
                            (str(round(mod.edge_crease_outer, 2)), color_value, text_size_normal)
                        ])

                    # RIM
                    if mod.edge_crease_rim != 0:
                        output_text.extend([
                            (" Rim ", color_setting, text_size_normal),
                            (str(round(mod.edge_crease_rim, 2)), color_value, text_size_normal)
                        ])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# SUBSURF
# ---------------------------------------------------------------


def mod_subsurf(output_text, mod, color_title, color_setting, color_value,
                text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SUBSURF.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        # FIXME: Almost all of this is the same as the multires modifier. Can
        # we consolidate the code a bit?
        if mod.show_viewport:
            if detailed_modifiers:
                # SUBDIVISION TYPE
                if mod.subdivision_type == 'SIMPLE':
                    output_text.extend([(" Simple ", color_setting, text_size_normal)])
                else:
                    output_text.extend([(" Catmull Clark ", color_setting, text_size_normal)])

                # QUALITY
                output_text.extend([
                    (" Quality ", color_setting, text_size_normal),
                    (str(mod.quality), color_value, text_size_normal)
                ])

                # RENDER SUBDIVISION LEVELS
                output_text.extend([
                    (" Render ", color_setting, text_size_normal),
                    (str(mod.render_levels), color_value, text_size_normal)
                ])

                # VIEWPORT SUBDIVISION LEVELS
                output_text.extend([
                    (" Preview ", color_setting, text_size_normal),
                    (str(mod.levels), color_value, text_size_normal)
                ])

                # FIXME: We need a dynamic wrap here
                if any([mod.uv_smooth == "PRESERVE_CORNERS", mod.show_only_control_edges, mod.use_creases]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                # UV SMOOTHING
                if mod.uv_smooth == "PRESERVE_CORNERS":
                    output_text.extend([
                        (" UV Smoothing (keep corners) ", color_setting, text_size_normal),
                    ])

                # OPTIMAL DISPLAY
                if mod.show_only_control_edges:
                    output_text.extend([(" Optimal Display ", color_setting, text_size_normal)])

                if mod.use_creases:
                    output_text.extend([(" Using Creases ", color_setting, text_size_normal)])

                # FIXME: Do we need to add code for this case? Does this case exist in 2.8x?
                # OPEN SUBDIV
                # if (hasattr(bpy.context.preferences.system, 'opensubdiv_compute_type')):
                #     if mod.use_opensubdiv:
                #         output_text.extend([(" Open Subdiv ", color_setting, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# TRIANGULATE
# ---------------------------------------------------------------

# FIXME: Needs to support 'keep normals'  minimum verts, and not have
# underscores in the 'method' field


def mod_triangulate(output_text, mod, color_title, color_setting, color_value,
                    text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_TRIANGULATE.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # VIEW
                output_text.extend([("  ", color_setting, text_size_normal),
                                    (str(mod.quad_method.lower().capitalize()), color_value, text_size_normal)])

                # RENDER
                output_text.extend([("  ", color_setting, text_size_normal),
                                    (str(mod.ngon_method.lower().capitalize()), color_value, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# WIREFRAME
# ---------------------------------------------------------------


def mod_wireframe(output_text, mod, color_title, color_setting, color_value,
                  text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_WIREFRAME.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # THICKNESS
                output_text.extend([(" Thickness ", color_setting, text_size_normal),
                                    (str(round(mod.thickness, 3)), color_value, text_size_normal)])

                # OFFSET
                output_text.extend([(" Offset ", color_setting, text_size_normal),
                                    (str(round(mod.offset, 2)), color_value, text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([(" VGroup ", color_setting, text_size_normal),
                                        (str(mod.vertex_group), color_value, text_size_normal)])

                    # THICKNESS VERTEX GROUP
                    output_text.extend([(" Factor ", color_setting, text_size_normal),
                                        (str(round(mod.thickness_vertex_group, 2)), color_value, text_size_normal)])
                # CREASE WEIGHT
                if mod.use_crease:
                    output_text.extend([(" Crease Weight ", color_setting, text_size_normal),
                                        (str(round(mod.crease_weight, 2)), color_value, text_size_normal)])

                # OPTIONS
                if any([mod.use_even_offset, mod.use_relative_offset, mod.use_replace, mod.use_boundary, mod.material_offset]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # EVEN THICKNESS
                    if mod.use_even_offset:
                        output_text.extend([(" Even Thickness ", color_setting, text_size_normal)])

                    # RELATIVE THICKNESS
                    if mod.use_relative_offset:
                        output_text.extend([(" Relative Thickness ", color_setting, text_size_normal)])

                    # BOUNDARY
                    if mod.use_boundary:
                        output_text.extend([(" Boundary ", color_setting, text_size_normal)])

                    # REPLACE ORIGINAL
                    if mod.use_replace:
                        output_text.extend([(" Replace Original ", color_setting, text_size_normal)])

                    # MATERIAL OFFSET
                    if mod.material_offset:
                        output_text.extend([(" Material Offset ", color_setting, text_size_normal),
                                            (str(mod.material_offset), color_value, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ----------------------------------------------------------------------------------------------------------------------
# MODIFIERS DEFORM -----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------
# ARMATURE
# ---------------------------------------------------------------


def mod_armature(output_text, mod, color_title, color_setting, color_value,
                 text_size_normal, color_warning, color_option, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_ARMATURE.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        # FIXME: We should have a 'problem' color rather than reusing 'color_warning'
        if mod.show_viewport:
            if detailed_modifiers:
                output_text.extend([(" Object ", color_setting, text_size_normal)])
                if mod.object:
                    # START
                    output_text.extend([(str(mod.object.name), color_value, text_size_normal)])
                else:
                    output_text.extend([(" None ", color_warning, text_size_normal)])

                # VERTEX GROUP
                if mod.use_vertex_groups:
                    output_text.extend([(" VGroup ", color_setting, text_size_normal)])
                    if mod.vertex_group:
                        output_text.extend([(str(mod.vertex_group), color_value, text_size_normal)])
                    else:
                        output_text.extend([(" None ", color_warning, text_size_normal)])

                # OPTIONS
                if any([mod.use_deform_preserve_volume, mod.use_bone_envelopes, mod.use_multi_modifier]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # PRESERVE VOLUME
                    if mod.use_deform_preserve_volume:

                        output_text.extend([(" Preserve Volume ", color_setting, text_size_normal)])

                    # BONE ENVELOPES
                    if mod.use_bone_envelopes:
                        output_text.extend([(" Bone Enveloppes ", color_setting, text_size_normal)])

                    # MULTI MODIFIER
                    if mod.use_multi_modifier:
                        output_text.extend([(" Multi Modifier ", color_setting, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# CAST
# ---------------------------------------------------------------


def mod_cast(output_text, mod, color_title, color_setting, color_value,
             text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_CAST.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # CAST TYPE
                output_text.extend([(" Type ", color_setting, text_size_normal), (str(
                    mod.cast_type.lower().capitalize()), color_value, text_size_normal)])

                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    output_text.extend([(" Axis ", color_setting, text_size_normal)])

                    if mod.use_x:
                        output_text.extend([(" X ", color_value, text_size_normal)])

                    if mod.use_y:
                        output_text.extend([(" Y ", color_value, text_size_normal)])

                    if mod.use_z:
                        output_text.extend([(" Z ", color_value, text_size_normal)])

                else:
                    output_text.extend([(" No Axis Selected ", color_warning, text_size_normal)])

                # FACTOR
                output_text.extend([(" Factor ", color_setting, text_size_normal),
                                    (str(round(mod.factor, 2)), color_value, text_size_normal)])

                # RADIUS
                if mod.radius != 0:
                    output_text.extend([
                        (" Radius ", color_setting, text_size_normal),
                        (str(round(mod.radius, 2)), color_value, text_size_normal),
                        (units, color_value, text_size_normal)
                    ])

                # SIZE
                if mod.size != 0:
                    output_text.extend([
                        (" Size ", color_setting, text_size_normal),
                        (str(round(mod.size, 2)), color_value, text_size_normal)
                    ])

                # OPTIONS
                if any([mod.use_radius_as_size, mod.vertex_group, mod.object, mod.use_transform]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", color_setting, text_size_normal),
                            (mod.vertex_group, color_value, text_size_normal)
                        ])

                    # FROM RADIUS
                    if mod.use_radius_as_size:
                        output_text.extend([(" From Radius ", color_setting, text_size_normal)])

                    # OBJECT
                    if mod.object:
                        output_text.extend([
                            (" Control Object ", color_setting, text_size_normal),
                            (mod.object.name, color_value, text_size_normal)
                        ])

                    # USE TRANSFORM
                    if mod.use_transform:
                        output_text.extend([(" Use Transform ", color_setting, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# CORRECTIVE SMOOTH
# ---------------------------------------------------------------


def mod_corrective_smooth(output_text, mod, color_title, color_setting,
                          color_value, text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # FACTOR
                output_text.extend([
                    (" Factor ", color_setting, text_size_normal),
                    (str(round(mod.factor, 2)), color_value, text_size_normal)
                ])

                # ITERATIONS
                output_text.extend([
                    (" Repeat ", color_setting, text_size_normal),
                    (str(mod.iterations), color_value, text_size_normal)
                ])

                # SCALE
                if mod.scale != 1.0:
                    output_text.extend([
                        (" Scale ", color_setting, text_size_normal),
                        (str(round(mod.scale, 2)), color_value, text_size_normal)
                    ])

                # SMOOTH TYPE
                output_text.extend([
                    (" Type ", color_setting, text_size_normal),
                    (str(mod.smooth_type.lower().capitalize()), color_value, text_size_normal)
                ])

                # OPTIONS
                if any([mod.use_only_smooth, mod.vertex_group, mod.use_pin_boundary, mod.rest_source]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([(" VGroup ", color_setting, text_size_normal),
                                            (mod.vertex_group, color_value, text_size_normal)])

                    # ONLY SMOOTH
                    if mod.use_only_smooth:
                        output_text.extend([(" Only Smooth ", color_setting, text_size_normal)])

                    # PIN BOUNDARIES
                    if mod.use_pin_boundary:
                        output_text.extend([(" Pin Boundaries ", color_setting, text_size_normal)])

                    # OBJECT
                    output_text.extend([
                        (" Rest Source ", color_setting, text_size_normal),
                        (mod.rest_source.lower().capitalize(), color_value, text_size_normal)
                    ])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# CURVE
# ---------------------------------------------------------------


def mod_curve(output_text, mod, color_title, color_setting, color_value,
              text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_CURVE.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # OBJECT
                output_text.extend([(" Object ", color_setting, text_size_normal)])
                if mod.object:
                    output_text.extend([(mod.object.name, color_value, text_size_normal)])
                else:
                    output_text.extend([(" None ", color_warning, text_size_normal)])

                # DEFORM AXIS
                output_text.extend([(" Deformation Axis ", color_setting, text_size_normal)])
                if mod.deform_axis == 'POS_X':
                    output_text.extend([(" X ", color_value, text_size_normal)])

                elif mod.deform_axis == 'POS_Y':
                    output_text.extend([(" Y ", color_value, text_size_normal)])

                elif mod.deform_axis == 'POS_Z':
                    output_text.extend([(" Z ", color_value, text_size_normal)])

                elif mod.deform_axis == 'NEG_X':
                    output_text.extend([(" -X ", color_value, text_size_normal)])

                elif mod.deform_axis == 'NEG_Y':
                    output_text.extend([(" -Y ", color_value, text_size_normal)])

                elif mod.deform_axis == 'NEG_Z':
                    output_text.extend([(" -Z ", color_value, text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])
                    output_text.extend([
                        (" VGroup ", color_setting, text_size_normal),
                        (str(mod.vertex_group), color_value, text_size_normal)
                    ])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# DISPLACE
# ---------------------------------------------------------------


def mod_displace(output_text, mod, color_title, color_setting, color_value,
                 text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_DISPLACE.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # MID LEVEL
                output_text.extend([(" Mid Level ", color_setting, text_size_normal),
                                    (str(round(mod.mid_level, 2)), color_value, text_size_normal)])

                # STRENGTH
                output_text.extend([(" Strength ", color_setting, text_size_normal),
                                    (str(round(mod.strength, 2)), color_value, text_size_normal)])

                # DIRECTION
                output_text.extend([(" Direction ", color_setting, text_size_normal), (str(
                    mod.direction.lower().capitalize()), color_value, text_size_normal)])
                if mod.direction in ['RGB_TO_XYZ', 'X', 'Y', 'Z']:
                    # DIRECTION
                    output_text.extend([(" Space ", color_setting, text_size_normal), (str(
                        mod.space.lower().capitalize()), color_value, text_size_normal)])

                # # OPTIONS
                # if any([mod.vertex_group]):
                #     output_text.extend(["CR", ("----", color_title, text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])
                    output_text.extend([
                        (" VGroup ", color_setting, text_size_normal),
                        (str(mod.vertex_group), color_value, text_size_normal)
                    ])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# HOOK
# ---------------------------------------------------------------


def mod_hook(output_text, mod, color_title, color_setting, color_value,
             text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_HOOK.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # OBJECT
                output_text.extend([(" Object ", color_setting, text_size_normal)])
                if mod.object:
                    output_text.extend([(mod.object.name, color_value, text_size_normal)])
                else:
                    output_text.extend([(" None ", color_warning, text_size_normal)])

                # RADIUS
                if mod.falloff_type != 'NONE':
                    if mod.falloff_radius != 0:
                        output_text.extend([
                            (" Radius ", color_setting, text_size_normal),
                            (str(round(mod.falloff_radius, 2)), color_value, text_size_normal),
                            (units, color_value, text_size_normal)
                        ])

                # STRENGTH
                output_text.extend([
                    (" Strength ", color_setting, text_size_normal),
                    (str(round(mod.strength, 2)), color_value, text_size_normal)
                ])

                # OPTIONS
                output_text.extend(["CR", ("----", color_title, text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([(" VGroup ", color_setting, text_size_normal),
                                        (mod.vertex_group, color_value, text_size_normal)])

                # FALLOF TYPE
                output_text.extend([
                    (" Fallof Type ", color_setting, text_size_normal),
                    (str(mod.falloff_type.upper()), color_value, text_size_normal)
                ])

                # UNIFORM FALLOFF
                if mod.use_falloff_uniform:
                    output_text.extend([(" Uniform Falloff ", color_setting, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# LAPLACIAN DEFORMER
# ---------------------------------------------------------------


def mod_laplacian_deformer(output_text, mod, color_title, color_setting,
                           color_value, text_size_normal, color_warning, color_option, units,
                           detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        # FIXME: display this more readably
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # ITERATIONS
                output_text.extend([
                    (" Repeat ", color_setting, text_size_normal),
                    (str(mod.iterations), color_value, text_size_normal)
                ])

                # VERTEX GROUP
                output_text.extend([(" VGroup ", color_setting, text_size_normal)])
                if mod.vertex_group:
                    output_text.extend([(str(mod.vertex_group), color_value, text_size_normal)])
                else:
                    output_text.extend([(" None ", color_warning, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# LAPLACIAN SMOOTH
# ---------------------------------------------------------------


def mod_laplacian_smooth(output_text, mod, color_title, color_setting,
                         color_value, text_size_normal, color_warning, color_option, units,
                         detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # REPEAT
                output_text.extend([
                    (" Repeat ", color_setting, text_size_normal),
                    (str(mod.iterations), color_value, text_size_normal),
                ])

                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    output_text.extend([(" Axis", color_setting, text_size_normal)])

                    if mod.use_x:
                        output_text.extend([(" X", color_value, text_size_normal)])

                    if mod.use_y:
                        output_text.extend([(" Y", color_value, text_size_normal)])

                    if mod.use_z:
                        output_text.extend([(" Z", color_value, text_size_normal)])
                else:
                    output_text.extend([(" None", color_warning, text_size_normal)])

                # FACTOR
                output_text.extend([
                    (" Factor ", color_setting, text_size_normal),
                    (str(round(mod.lambda_factor, 2)), color_value, text_size_normal)
                ])

                # BORDER
                output_text.extend([
                    (" Border ", color_setting, text_size_normal),
                    (str(round(mod.lambda_border, 2)), color_value, text_size_normal)
                ])

                # OPTIONS
                if any([mod.use_volume_preserve, mod.use_normalized, mod.vertex_group]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # PRESERVE VOLUME
                    if mod.use_volume_preserve:
                        output_text.extend([(" Preserve Volume ", color_setting, text_size_normal)])

                    # NORMALIZED
                    if mod.use_normalized:
                        output_text.extend([(" Normalized ", color_setting, text_size_normal)])

                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", color_setting, text_size_normal),
                            (mod.vertex_group, color_value, text_size_normal)
                        ])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# MESH DEFORM
# ---------------------------------------------------------------


def mod_mesh_deform(output_text, mod, color_title, color_setting, color_value,
                    text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # OBJECT
                output_text.extend([(" Object ", color_setting, text_size_normal)])
                if mod.object:
                    output_text.extend([(mod.object.name, color_value, text_size_normal)])
                else:
                    output_text.extend([(" None ", color_warning, text_size_normal)])

                # PRECISION
                output_text.extend([
                    (" Precision ", color_setting, text_size_normal),
                    (str(mod.precision), color_value, text_size_normal),
                ])

                # OPTIONS
                if any([mod.use_dynamic_bind, mod.vertex_group]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([(" VGroup ", color_setting, text_size_normal),
                                            (str(mod.vertex_group), color_value, text_size_normal)])

                    # USE DYNAMIC BIND
                    if mod.use_dynamic_bind:
                        output_text.extend([(" Dynamic ", color_setting, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# SIMPLE DEFORM
# ---------------------------------------------------------------


def mod_simple_deform(output_text, mod, color_title, color_setting,
                      color_value, text_size_normal, color_warning, color_option, units,
                      detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SIMPLEDEFORM.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                output_text.extend([
                    (" ", color_setting, text_size_normal),
                    (str(mod.deform_method.upper()), color_value, text_size_normal)
                ])

                # ORIGIN
                if mod.origin:
                    output_text.extend([(" Axis,Origin ", color_setting, text_size_normal),
                                        (str(mod.origin.name), color_value, text_size_normal)])

                # ANGLE/FACTOR
                if mod.deform_method in ['TWIST', 'BEND']:
                    # Angle
                    output_text.extend([
                        (" Angle ", color_setting, text_size_normal),
                        (str(round(math.degrees(mod.factor), 1)), color_value, text_size_normal),
                        ("°", color_value, text_size_normal)
                    ])

                elif mod.deform_method in ['TAPER', 'STRETCH']:
                    output_text.extend([
                        (" Factor ", color_setting, text_size_normal),
                        (str(round(mod.factor, 2)), color_value, text_size_normal)
                    ])

                # OPTIONS
                output_text.extend(["CR", ("----", color_title, text_size_normal)])

                # AXIS
                # FIXME: Should we always show this?
                output_text.extend([
                    (" Axis ", color_setting, text_size_normal),
                    (mod.deform_axis, color_value, text_size_normal)
                ])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([(" VGroup ", color_setting, text_size_normal),
                                        (str(mod.vertex_group), color_value, text_size_normal)])

                # LOCK
                if mod.deform_method != 'BEND':
                    if any([mod.lock_x, mod.lock_y]):
                        output_text.extend([(" Lock ", color_setting, text_size_normal)])

                        if mod.lock_x:
                            output_text.extend([(" X ", color_value, text_size_normal)])

                        if mod.lock_y:
                            output_text.extend([(" Y ", color_value, text_size_normal)])

                # LIMIT
                output_text.extend([
                    (" Limit ", color_setting, text_size_normal),
                    (str(round(mod.limits[0], 2)), color_value, text_size_normal),
                    (" – ", color_setting, text_size_normal),
                    (str(round(mod.limits[1], 2)), color_value, text_size_normal)
                ])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# SHRINKWRAP
# ---------------------------------------------------------------


def mod_shrinkwrap(output_text, mod, color_title, color_setting, color_value,
                   text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SHRINKWRAP.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])

        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # TARGET
                output_text.extend([(" Target ", color_setting, text_size_normal)])
                if mod.target:
                    output_text.extend([(str(mod.target.name), color_value, text_size_normal)])
                else:
                    output_text.extend([(" None ", color_warning, text_size_normal)])

                # OFFSET
                output_text.extend([
                    (" Offset ", color_setting, text_size_normal),
                    (str(round(mod.offset, 2)), color_value, text_size_normal),
                ])

                # VERTEX GROUP
                if mod.vertex_group:
                    output_text.extend([(" VGroup ", color_setting, text_size_normal),
                                        (str(mod.vertex_group), color_value, text_size_normal)])

                output_text.extend(["CR", ("----", color_title, text_size_normal)])

                # NEAREST SURFACEPOINT
                if mod.wrap_method == 'NEAREST_SURFACEPOINT':
                    # MODE
                    output_text.extend([
                        (" Method ", color_setting, text_size_normal),
                        (str(mod.wrap_method.lower().capitalize()), color_value, text_size_normal),
                        (" Mode ", color_setting, text_size_normal),
                        (str(mod.wrap_mode.lower().capitalize()), color_value, text_size_normal),
                    ])

                # PROJECT
                elif mod.wrap_method == 'PROJECT':
                    # MODE
                    output_text.extend([
                        (" Method ", color_setting, text_size_normal),
                        (str(mod.wrap_method.lower().capitalize()), color_value, text_size_normal),
                        (" Mode ", color_setting, text_size_normal),
                        (str(mod.wrap_mode.lower().capitalize()), color_value, text_size_normal),
                    ])

                    # AXIS
                    if any([mod.use_project_x, mod.use_project_y, mod.use_project_z]):
                        output_text.extend([(" Axis ", color_setting, text_size_normal)])
                        # X
                        if mod.use_project_x:
                            output_text.extend([(" X ", color_value, text_size_normal)])
                        # Y
                        if mod.use_project_y:
                            output_text.extend([(" Y ", color_value, text_size_normal)])
                        # Z
                        if mod.use_project_z:
                            output_text.extend([(" Z ", color_value, text_size_normal)])

                    # LEVELS
                    output_text.extend([
                        (" Subsurf ", color_setting, text_size_normal),
                        (str(mod.subsurf_levels), color_value, text_size_normal)
                    ])

                    # PROJECT LIMIT
                    output_text.extend([
                        (" Limit ", color_setting, text_size_normal),
                        (str(round(mod.project_limit, 2)), color_value, text_size_normal)
                    ])

                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # DIRECTION
                    if mod.use_negative_direction:
                        output_text.extend([(" Negative ", color_setting, text_size_normal)])

                    if mod.use_positive_direction:
                        output_text.extend([(" Positive ", color_setting, text_size_normal)])

                    # MODE
                    output_text.extend([(" Cull Face ", color_setting, text_size_normal),
                                        (str(mod.cull_face.lower().capitalize()), color_value, text_size_normal)])
                    # AUXILIARY TARGET
                    if mod.auxiliary_target:
                        output_text.extend([
                            (" Auxiliary Target ", color_setting, text_size_normal),
                            (mod.auxiliary_target.name, color_value, text_size_normal)
                        ])
                else:
                    # MODE
                    output_text.extend([
                        (" Mode ", color_setting, text_size_normal),
                        (str(mod.wrap_method.lower().capitalize()), color_value, text_size_normal)
                    ])
        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# SMOOTH
# ---------------------------------------------------------------


def mod_smooth(output_text, mod, color_title, color_setting, color_value,
               text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    output_text.extend([(" Axis ", color_setting, text_size_normal)])

                    if mod.use_x:
                        output_text.extend([(" X ", color_value, text_size_normal)])

                    if mod.use_y:
                        output_text.extend([(" Y ", color_value, text_size_normal)])

                    if mod.use_z:
                        output_text.extend([(" Z ", color_value, text_size_normal)])
                else:
                    output_text.extend([(" No Axis Selected ", color_warning, text_size_normal)])

                # FACTOR
                output_text.extend([(" Factor ", color_setting, text_size_normal),
                                    (str(round(mod.factor, 2)), color_value, text_size_normal)])

                # ITERATIONS
                output_text.extend([(" Repeat ", color_setting, text_size_normal),
                                    (str(mod.iterations), color_value, text_size_normal)])

                # OPTIONS
                if mod.vertex_group:
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])
                    output_text.extend([(" VGroup ", color_setting, text_size_normal),
                                        (mod.vertex_group, color_value, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# SURFACE DEFORM
# ---------------------------------------------------------------


def mod_surface_deform(output_text, mod, color_title, color_setting,
                       color_value, text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # TARGET
                output_text.extend([(" Target ", color_setting, text_size_normal)])
                if mod.target:
                    output_text.extend([(str(mod.target.name), color_value, text_size_normal)])
                else:
                    output_text.extend([(" None ", color_warning, text_size_normal)])

                # FALLOFF
                output_text.extend([
                    (" Falloff ", color_setting, text_size_normal),
                    (str(round(mod.falloff, 2)), color_value, text_size_normal),
                ])

                if mod.vertex_group:
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])
                    output_text.extend([
                        (" VGroup ", color_setting, text_size_normal),
                        (mod.vertex_group, color_value, text_size_normal),
                    ])

                output_text.extend([
                    (" Strength ", color_setting, text_size_normal),
                    (str(round(mod.strength, 2)), color_value, text_size_normal),
                ])
        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# WARP
# ---------------------------------------------------------------


def mod_warp(output_text, mod, color_title, color_setting, color_value,
             text_size_normal, color_warning, color_option, units, detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_WARP.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                # FROM
                output_text.extend([(" From ", color_setting, text_size_normal)])
                if mod.object_from:
                    output_text.extend([(str(mod.object_from.name), color_value, text_size_normal)])

                else:
                    output_text.extend([(" None ", color_warning, text_size_normal)])

                # TO
                output_text.extend([(" To ", color_setting, text_size_normal)])
                if mod.object_to:
                    output_text.extend([(str(mod.object_to.name), color_value, text_size_normal)])
                else:
                    output_text.extend([(" None ", color_warning, text_size_normal)])

                # STRENGTH
                output_text.extend([
                    (" Strength ", color_setting, text_size_normal),
                    (str(round(mod.strength, 2)), color_value, text_size_normal),
                ])

                output_text.extend([
                    (" Falloff ", color_setting, text_size_normal),
                    (mod.falloff_type.lower().capitalize(), color_value, text_size_normal),
                ])

                # RADIUS
                if mod.falloff_type != 'NONE':
                    # FIXME: Radius showing in m when units are cm
                    if mod.falloff_radius != 0:
                        output_text.extend([
                            (" Radius ", color_setting, text_size_normal),
                            (str(round(mod.falloff_radius, 2)), color_value, text_size_normal),
                            (units, color_value, text_size_normal),
                        ])

                # OPTIONS
                if any([mod.vertex_group, mod.use_volume_preserve, mod.texture_coords]):
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", color_setting, text_size_normal),
                            (str(mod.vertex_group), color_value, text_size_normal),
                        ])

                    # OFFSET
                    if mod.use_volume_preserve:
                        output_text.extend([(" Preserve Volume ", color_setting, text_size_normal)])

                    # TEXTURE
                    if mod.texture:
                        output_text.extend([
                            (" Texture ", color_setting, text_size_normal),
                            (mod.texture.name, color_value, text_size_normal),
                        ])

                    # TEXTURES COORD
                    output_text.extend([
                        (" Texture Coords ", color_setting, text_size_normal),
                        (mod.texture_coords, color_value, text_size_normal),
                    ])

                    # OBJECT
                    if mod.texture_coords == "OBJECT":
                        if mod.texture_coords_object:
                            output_text.extend([(" Object ", color_setting, text_size_normal)])
                            output_text.extend([
                                (str(mod.texture_coords_object.name), color_value, text_size_normal),
                            ])
                        else:
                            output_text.extend([(" None ", color_warning, text_size_normal)])

                    # UVs
                    if mod.texture_coords == "UV":
                        output_text.extend([(" UVMap ", color_setting, text_size_normal)])

                        if mod.uv_layer:
                            output_text.extend([
                                (str(mod.uv_layer), color_value, text_size_normal)
                            ])
                        else:
                            output_text.extend([(" None ", color_warning, text_size_normal)])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ---------------------------------------------------------------
# WAVE
# ---------------------------------------------------------------


def mod_wave(output_text, mod, color_title, color_setting, color_value,
             text_size_normal, color_warning, color_option, units,
             detailed_modifiers):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # output_text.extend(["CR", ('ICON', 'ICON_MOD_WAVE.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        output_text.extend(["CR", (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if detailed_modifiers:
                if any([mod.use_x, mod.use_y, mod.use_cyclic]):
                    output_text.extend([(" Motion ", color_setting, text_size_normal)])

                    if mod.use_x:
                        output_text.extend([(" X ", color_value, text_size_normal)])

                    if mod.use_y:
                        output_text.extend([(" Y ", color_value, text_size_normal)])

                    if mod.use_cyclic:
                        output_text.extend([(" Cyclic ", color_value, text_size_normal)])

                if mod.use_normal:
                    if any([mod.use_normal_x, mod.use_normal_y, mod.use_normal_z]):
                        output_text.extend([(" Normals ", color_setting, text_size_normal)])

                        if mod.use_normal_x:
                            output_text.extend([(" X ", color_value, text_size_normal)])

                        if mod.use_normal_y:
                            output_text.extend([(" Y ", color_value, text_size_normal)])

                        if mod.use_normal_z:
                            output_text.extend([(" Z ", color_value, text_size_normal)])

                # TIME
                output_text.extend([(" Time ", color_setting, text_size_normal)])

                # OFFSET
                output_text.extend([(" Offset ", color_setting, text_size_normal),
                                    (str(round(mod.time_offset, 2)), color_value, text_size_normal)])
                # LIFE
                output_text.extend([(" Life ", color_setting, text_size_normal),
                                    (str(round(mod.lifetime, 2)), color_value, text_size_normal)])
                # DAMPING
                output_text.extend([(" Damping ", color_setting, text_size_normal),
                                    (str(round(mod.damping_time, 2)), color_value, text_size_normal)])

                if any([mod.start_position_x, mod.start_position_y, mod.falloff_radius]) != 0:
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])
                    # TIME
                    # FIXME: shows m when scale is cm
                    output_text.extend([(" Position ", color_setting, text_size_normal)])

                    # POS X
                    output_text.extend([
                        (" X ", color_setting, text_size_normal),
                        (str(round(mod.start_position_x, 2)), color_value,
                         text_size_normal),
                        (units, color_value, text_size_normal)
                    ])

                    # POS Y
                    output_text.extend([
                        (" Y ", color_setting, text_size_normal),
                        (str(round(mod.start_position_y, 2)), color_value,
                         text_size_normal),
                        (units, color_value, text_size_normal)
                    ])

                    # FALLOFF
                    output_text.extend([
                        (" Falloff ", color_setting, text_size_normal),
                        (str(round(mod.falloff_radius, 2)), color_value,
                         text_size_normal),
                        (units, color_value, text_size_normal)
                    ])

                if any([mod.start_position_object, mod.vertex_group, mod.texture_coords]) != 0:
                    output_text.extend(["CR", ("----", color_title, text_size_normal)])

                    # FROM
                    if mod.start_position_object:
                        output_text.extend([
                            (" From ", color_setting, text_size_normal),
                            (str(mod.start_position_object.name), color_value, text_size_normal)
                        ])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        output_text.extend([
                            (" VGroup ", color_setting, text_size_normal),
                            (str(mod.vertex_group), color_value, text_size_normal)
                        ])

                    # TEXTURES COORD
                    output_text.extend([
                        (" Texture Coords ", color_setting, text_size_normal),
                        (mod.texture_coords, color_value, text_size_normal)
                    ])

                    # OBJECT
                    if mod.texture_coords == "OBJECT":
                        if mod.texture_coords_object:
                            output_text.extend([
                                (" Object ", color_setting, text_size_normal),
                                (str(mod.texture_coords_object.name), color_value, text_size_normal)
                            ])
                        else:
                            output_text.extend([(" No Object Selected ", color_warning, text_size_normal)])

                    # UVs
                    if mod.texture_coords == "UV":
                        output_text.extend([(" UVMap ", color_setting, text_size_normal)])
                        if mod.uv_layer:
                            output_text.extend([(mod.uv_layer, color_value, text_size_normal)])
                        else:
                            output_text.extend([(" None ", color_warning, text_size_normal)])

                output_text.extend(["CR", ("----", color_title, text_size_normal)])

                # SPEED
                output_text.extend([
                    (" Speed ", color_setting, text_size_normal),
                    (str(round(mod.speed, 2)), color_value, text_size_normal)
                ])

                # SPEED
                # FIXME: Shows m when scale is cm
                output_text.extend([
                    (" Height ", color_setting, text_size_normal),
                    (str(round(mod.height, 2)), color_value, text_size_normal), (units, color_value, text_size_normal),
                ])

                # SPEED
                output_text.extend([
                    (" Width ", color_setting, text_size_normal),
                    (str(round(mod.width, 2)), color_value, text_size_normal),
                    (units, color_value, text_size_normal),
                ])

                # SPEED
                output_text.extend([
                    (" Narrowness ", color_setting, text_size_normal),
                    (str(round(mod.narrowness, 2)), color_value, text_size_normal),
                    (units, color_value, text_size_normal),
                ])

        else:
            output_text.extend([(" Hidden ", color_warning, text_size_normal)])

# ----------------------------------------------------------------------------------------------------------------------
# OBJECTS --------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------
# ARMATURE
# ---------------------------------------------------------------


def armature(output_text, color_title, color_setting, color_value,
             text_size_normal, color_warning, color_option, units):
    obj = bpy.context.active_object
    active_bone = bpy.context.active_bone

    # BONE SELECTED
    if active_bone and bpy.context.object.mode in {'POSE', 'EDIT'}:
        output_text.extend(["CR", ("BONE SELECTED ", color_title, text_size_normal),
                            (active_bone.name, color_value, text_size_normal)])

# ---------------------------------------------------------------
# CAMERA
# ---------------------------------------------------------------


def camera(output_text, color_title, color_setting, color_value,
           text_size_normal, color_warning, color_option, units):
    obj = bpy.context.active_object
    units_system = bpy.context.scene.unit_settings.system

    # LENS
    output_text.extend([
        "CR",
        ("LENS ", color_title, text_size_normal),
        (str(round(obj.data.lens, 2)), color_value, text_size_normal),
        ("mm", color_value, int(text_size_normal * 0.80)),
    ])

    # FOCUS
    if obj.data.dof.use_dof and obj.data.dof.focus_object:
        output_text.extend([
            "CR",
            ("FOCUS ", color_title, text_size_normal),
            (str(obj.data.dof.focus_object.name), color_value, text_size_normal),
        ])
    else:
        foc_dist = bpy.utils.units.to_string(units_system, 'LENGTH', obj.data.dof.focus_distance, precision=2)
        output_text.extend([
            "CR",
            ("DISTANCE ", color_title, text_size_normal),
            (foc_dist, color_value, text_size_normal)
        ])

    if bpy.context.object.data.dof.use_dof:
        output_text.extend([
            "CR",
            ("FSTOP ", color_title, text_size_normal),
            (str(round(obj.data.dof.aperture_fstop, 1)), color_value, text_size_normal)
        ])

# ---------------------------------------------------------------
# CURVE / FONT
# ---------------------------------------------------------------


def curve_font(output_text, color_title, color_setting, color_value,
               text_size_normal, color_warning, color_option, units):
    obj = bpy.context.active_object

    # PREVIEW U
    output_text.extend(["CR", ("Preview U ", color_title, text_size_normal),
                        (str(obj.data.resolution_u), color_value, text_size_normal)])

    # RENDER PREVIEW U
    output_text.extend([(" Render U ", color_title, text_size_normal),
                        (str(obj.data.render_resolution_u), color_value, text_size_normal)])

    # FILL MODE
    output_text.extend(["CR", ("FILL ", color_title, text_size_normal), (str(
        obj.data.fill_mode.lower().capitalize()), color_value, text_size_normal)])

    # OFFSET
    if obj.data.offset:
        output_text.extend(
            ["CR", ("Offset ", color_title, text_size_normal), (str(round(obj.data.offset, 2)), color_value, text_size_normal)])

    # DEPTH
    if obj.data.bevel_depth:
        output_text.extend(["CR", ("DEPTH ", color_title, text_size_normal),
                            (str(round(obj.data.bevel_depth, 2)), color_value, text_size_normal)])

    # EXTRUDE
    if obj.data.extrude:
        output_text.extend(["CR", ("EXTRUDE ", color_title, text_size_normal),
                            (str(round(obj.data.extrude, 2)), color_value, text_size_normal)])

    # RESOLUTION
    if obj.data.bevel_resolution:
        output_text.extend(["CR", ("RESOLUTION ", color_title, text_size_normal),
                            (str(obj.data.bevel_resolution), color_value, text_size_normal)])
    # BEVEL
    if obj.data.bevel_object:
        output_text.extend(["CR", ("BEVEL ", color_title, text_size_normal),
                            (obj.data.bevel_object.name, color_value, text_size_normal)])

    # TAPER
    if obj.data.taper_object:
        output_text.extend(["CR", ("TAPER ", color_title, text_size_normal),
                            (obj.data.taper_object.name, color_value, text_size_normal)])

# ---------------------------------------------------------------
# EMPTY
# ---------------------------------------------------------------


def empty(output_text, color_title, color_setting, color_value,
          text_size_normal, color_warning, color_option, units):
    obj = bpy.context.active_object

    # ICON_OUTLINER_OB_EMPTY
    # TYPE
    output_text.extend([("TYPE ", color_title, text_size_normal),
                        (str(obj.empty_display_type.lower().capitalize()), color_value, text_size_normal)])

    # SIZE
    output_text.extend(["CR", ("SIZE ", color_title, text_size_normal),
                        (str(round(obj.empty_display_size, 2)), color_value, text_size_normal)])

# ---------------------------------------------------------------
# LATTICE
# ---------------------------------------------------------------


def text_lattice(output_text, color_title, color_setting, color_value,
                 text_size_normal, color_warning, color_option, units):
    obj = bpy.context.active_object

# U -----------------------------------------------------------------------
    output_text.extend(["CR", ("U  ", color_title, text_size_normal),
                        (str(obj.data.points_u), color_value, text_size_normal)])

    # INTERPOLATION U
    output_text.extend([("  ", color_title, text_size_normal),
                        (str(obj.data.interpolation_type_u.split("_")[-1]), color_setting, text_size_normal)])

# V -----------------------------------------------------------------------
    output_text.extend(["CR", ("V  ", color_title, text_size_normal),
                        (str(obj.data.points_v), color_value, text_size_normal)])

    # INTERPOLATION V
    output_text.extend([("  ", color_title, text_size_normal), (
        str(obj.data.interpolation_type_v.split("_")[-1]), color_setting, text_size_normal)])

# W -----------------------------------------------------------------------
    output_text.extend(["CR", ("W ", color_title, text_size_normal),
                        (str(obj.data.points_w), color_value,
                         text_size_normal)])

    # INTERPOLATION W
    output_text.extend([("  ", color_title, text_size_normal), (
        str(obj.data.interpolation_type_w.split("_")[-1]), color_setting, text_size_normal)])

# ---------------------------------------------------------------
# LIGHTS
# ---------------------------------------------------------------


def cycles_lights(output_text, color_title, color_setting, color_value,
                  text_size_normal, color_warning, color_option, units):
    obj = bpy.context.active_object

    # TYPE
    if obj.data.type == 'AREA':
        output_text.extend(["CR", ("TYPE: ", color_title, text_size_normal),
                            ("AREA ", color_setting, text_size_normal)])

        # SQUARE
        if obj.data.shape == 'SQUARE':
            output_text.extend(["CR", ("SQUARE ", color_title, text_size_normal)])
            output_text.extend(["CR", ("SIZE ", color_title, text_size_normal),
                                (str(round(obj.data.size, 2)), color_value, text_size_normal)])
        # RECTANGLE
        elif obj.data.shape == 'RECTANGLE':
            # RECTANGLE
            output_text.extend(["CR", ("RECTANGLE ", color_title, text_size_normal)])
            # SIZE
            output_text.extend(["CR", ("SIZE X ", color_title, text_size_normal),
                                (str(round(obj.data.size, 2)), color_value, text_size_normal)])
            # SIZE Y
            output_text.extend(["CR", ("SIZE Y ", color_title, text_size_normal),
                                (str(round(obj.data.size_y, 2)), color_value, text_size_normal)])

    # POINT
    elif obj.data.type == 'POINT':
        output_text.extend(["CR", ("TYPE: ", color_title, text_size_normal),
                            ("POINT ", color_setting, text_size_normal)])

        # SIZE
        output_text.extend(["CR", ("SIZE ", color_title, text_size_normal),
                            (str(round(obj.data.shadow_soft_size, 2)), color_value, text_size_normal)])

    # SUN
    elif obj.data.type == 'SUN':
        output_text.extend(["CR", ("TYPE: ", color_title, text_size_normal), ("SUN ", color_setting, text_size_normal)])

        # SIZE
        output_text.extend(["CR", ("SIZE ", color_title, text_size_normal),
                            (str(round(obj.data.shadow_soft_size, 2)), color_value, text_size_normal)])

    elif obj.data.type == 'SPOT':
        output_text.extend(["CR", ("TYPE: ", color_title, text_size_normal),
                            ("SPOT ", color_setting, text_size_normal)])
        # SIZE
        output_text.extend(["CR", ("SIZE ", color_title, text_size_normal),
                            (str(round(obj.data.shadow_soft_size, 2)), color_value, text_size_normal)])
        # SHAPE
        output_text.extend(["CR", ("SHAPE ", color_title, text_size_normal), (
            str(round(math.degrees(obj.data.spot_size), 1)), color_value, text_size_normal),
            ("°", color_value, text_size_normal)])
        # BLEND
        output_text.extend(["CR", ("SIZE ", color_title, text_size_normal),
                            (str(round(obj.data.spot_blend, 2)), color_value, text_size_normal)])

    # HEMI
    elif obj.data.type == 'HEMI':
        output_text.extend(["CR", ("TYPE: ", color_title, text_size_normal),
                            ("HEMI ", color_setting, text_size_normal)])
        # output_text.extend([("HEMI ", color_title, text_size_normal),
        #                   (str(round(bpy.data.node_groups["Shader Nodetree"].nodes["Emission"].inputs[1].default_value, 2)), color_value, text_size_normal)])

    # PORTAL
    if obj.data.cycles.is_portal:
        output_text.extend(["CR", ("PORTAL", color_title, text_size_normal)])

    else:
        # CAST SHADOW
        if obj.data.cycles.cast_shadow:
            output_text.extend(["CR", ("CAST SHADOW ", color_setting, text_size_normal)])
        # MULTIPLE IMPORTANCE
        if obj.data.cycles.use_multiple_importance_sampling:
            output_text.extend(["CR", ("MULTIPLE IMPORTANCE", color_setting, text_size_normal)])

# ---------------------------------------------------------------
# METABALL
# ---------------------------------------------------------------


def metaball(output_text, color_title, color_setting, color_value,
             text_size_normal, color_warning, color_option, units):
    obj = bpy.context.active_object

    # VIEW
    output_text.extend(["CR", ("VIEW ", color_title, text_size_normal),
                        (str(round(obj.data.resolution, 2)), color_value, text_size_normal)])

    # RENDER
    output_text.extend(["CR", ("RENDER ", color_title, text_size_normal),
                        (str(round(obj.data.render_resolution, 2)), color_value, text_size_normal)])

    # THRESHOLD
    output_text.extend(["CR", ("THRESHOLD ", color_title, text_size_normal),
                        (str(round(obj.data.threshold, 2)), color_value, text_size_normal)])

    # UPDATE
    output_text.extend(["CR", ("UPDATE ", color_title, text_size_normal),
                        (obj.data.update_method.split("_")[-1], color_value, text_size_normal)])


# ---------------------------------------------------------------
# WARNING
# ---------------------------------------------------------------
def warning(output_text, color_title, color_setting, color_value,
            text_size_normal, color_warning, color_option, units):
    obj = bpy.context.active_object

    for mod in bpy.context.active_object.modifiers:
        if mod.type in ['BEVEL', 'SOLIDIFY']:
            if obj.scale[0] != obj.scale[2] or obj.scale[1] != obj.scale[0] or obj.scale[1] != obj.scale[2]:
                # output_text.extend([
                #     "CR",
                #     ('ICON', 'ICON_ERROR.png'),
                #     (" Non-Uniform Scale ", color_setting, text_size_normal),
                # ])
                output_text.extend([
                    "CR",
                    (" Non-Uniform Scale ", color_setting, text_size_normal),
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


def infotext_key_text():
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

    prefs = get_addon_preferences()
    obj = bpy.context.active_object
    wm = bpy.context.window_manager

    output_text = []

    # SHOW TEXT
    show_view_perspective = prefs.show_view_perspective
    show_object_mode = prefs.show_object_mode
    show_vert_face_tris = prefs.show_vert_face_tris
    show_object_name = prefs.show_object_name
    show_loc_rot_scale = prefs.show_loc_rot_scale
    show_modifiers = prefs.show_modifiers
    show_object_info = prefs.show_object_info
    detailed_modifiers = prefs.detailed_modifiers
    # show_keymaps = prefs.show_keymaps
    # show_blender_keymaps = prefs.show_blender_keymaps

    # TEXT OPTIONS
    color_warning = prefs.color_warning
    color_title = prefs.color_title
    color_setting = prefs.color_setting
    color_option = prefs.color_option
    color_value = prefs.color_value
    text_size_max = prefs.text_size_max
    text_size_mini = prefs.text_size_mini

    # FIXME: Make sure the math here is sensical
    text_size_normal = min(text_size_max, max(text_size_mini, int(bpy.context.area.width / 100)))
    text_size_large = int(text_size_max * 1.5)
    space = int(text_size_normal * 2)

    # HELP
    # if show_keymaps:
    #     keymaps(output_text, color_title, color_setting, color_value,
    # text_size_normal, color_warning, color_option)

    # EXPERIMENTAL
    # detect a running modal, to display custom things if there
    # is one, IF we can figure out which modal is actually active
    # at any given moment
    # modal(output_text, color_title, color_setting, color_value,
    #   text_size_normal, color_warning, color_option, text_size_large)

    if show_view_perspective:
        # Make sure we don't conflict with the existing information
        # text, by telling it to fuck off if we have the view
        # perspective text enabled. This is SUPER-jenky. Not sure
        # if there's a better way to do this, but my money says 'yes'
        bpy.context.preferences.view.show_object_info = False
        bpy.context.preferences.view.show_view_name = False

        view(output_text, color_title, color_setting, color_value,
             text_size_normal, color_warning, color_option, text_size_large)

        output_text.extend(["SPACE"])

    obj = bpy.context.object
    if obj is None:
        output_text.extend([("SELECTION", color_title, "Active object not found")])
        return output_text

    # MODE
    if show_object_mode:
        mode(output_text, color_title, color_setting, color_value,
             text_size_normal, color_warning, color_option, text_size_large)
        # SPACE
        output_text.extend(["SPACE"])

    # NAME
    if show_object_name:
        name(output_text, color_title, color_setting, color_value,
             text_size_normal, color_warning, color_option, text_size_large)
        # SPACE
        output_text.extend(["SPACE"])

    # LOCATION / ROTATION / SCALE
    if show_loc_rot_scale:
        loc(output_text, color_title, color_setting, color_value,
            text_size_normal, color_warning, color_option, units)

    # VERT/FACES/EDGES/NGONS
    if show_vert_face_tris:
        if obj.type == 'MESH':
            ngons(output_text, color_title, color_value, text_size_normal)
            # SPACE
            output_text.extend(["SPACE"])

    # MESH OPTIONS
    if show_object_info:
        # if bpy.context.object.mode in ['EDIT', 'OBJECT', 'WEIGHT_PAINT']:
        if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
            mesh_options(output_text, color_title, color_setting,
                         color_value, text_size_normal, color_warning, color_option,
                         space)

    # SCULPT
    if bpy.context.object.type == 'MESH' and bpy.context.object.mode == 'SCULPT':
        sculpt(output_text, color_title, color_setting, color_value,
               text_size_normal, color_warning, color_option, text_size_large, units,
               space)
        # SPACE
        output_text.extend(["SPACE"])


# ----------------------------------------------------------------------------------------------------------------------
# OBJECTS --------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    # ARMATURE
    if obj.type == 'ARMATURE':
        armature(output_text, color_title, color_setting, color_value,
                 text_size_normal, color_warning, color_option, units)
        # SPACE
        output_text.extend(["SPACE"])

    # CAMERA
    if obj.type == 'CAMERA':
        camera(output_text, color_title, color_setting, color_value,
               text_size_normal, color_warning, color_option, units)
        # SPACE
        output_text.extend(["SPACE"])

    # CURVES / FONT
    if obj.type in ['CURVE', 'FONT']:
        curve_font(output_text, color_title, color_setting, color_value,
                   text_size_normal, color_warning, color_option, units)
        if obj.modifiers:
            # SPACE
            output_text.extend(["CR", ("", color_title)])

    # EMPTY
    if obj.type == 'EMPTY':
        # SPACE
        output_text.extend(["CR", ("", color_title, text_size_normal)])
        empty(output_text, color_title, color_setting, color_value,
              text_size_normal, color_warning, color_option, units)
        # SPACE
        output_text.extend(["SPACE"])

    # LATTICE
    if obj.type == 'LATTICE':
        text_lattice(output_text, color_title, color_setting, color_value,
                     text_size_normal, color_warning, color_option, units)
        # SPACE
        output_text.extend(["SPACE"])

    # LIGHT
    if obj.type == 'LAMP':
        cycles_lights(output_text, color_title, color_setting, color_value,
                      text_size_normal, color_warning, color_option, units)
        # SPACE
        output_text.extend(["SPACE"])

    # METABALL
    if obj.type == 'META':
        metaball(output_text, color_title, color_setting, color_value,
                 text_size_normal, color_warning, color_option, units)
        # SPACE
        output_text.extend(["SPACE"])

# ----------------------------------------------------------------------
# MODIFIERS
# ----------------------------------------------------------------------
    wm = bpy.context.window_manager

    GREEN = (0.5, 1, 0, 1)
    NOIR = (0, 0, 0, 1)
    BLANC = (1, 1, 1, 1)

    if show_modifiers:
        # for mod in bpy.context.active_object.modifiers:
        for i, mod in enumerate(bpy.context.object.modifiers):
            color_title = BLANC

            # FIXME: explicitly support WELD
            if mod.type not in known_modifiers:
                # Unknown modifier (which we should fix)
                if mod.show_viewport:
                    output_text.extend([
                        "CR",
                        (str(mod.type), color_title, text_size_normal),
                        ("  ", color_title, text_size_normal),
                        (str(mod.name), color_value, text_size_normal),
                    ])
                else:
                    output_text.extend([
                        "CR",
                        (str(mod.type), color_title, text_size_normal),
                        ("  ", color_title, text_size_normal),
                        (str(mod.name), color_value, text_size_normal),
                    ])
                    output_text.extend([
                        (" Hidden ", color_warning, text_size_normal),
                    ])

                output_text.extend([
                    (" (Unknown modifier", color_warning, text_size_normal),
                ])

                return output_text

            # modifiers_list[mod]
            if mod.type == 'ARMATURE':
                mod_armature(output_text, mod, color_title, color_setting,
                             color_value, text_size_normal, color_warning, color_option,
                             space, detailed_modifiers)

            if mod.type == 'ARRAY':
                mod_array(output_text, mod, color_title, color_setting,
                          color_value, text_size_normal, color_warning, color_option,
                          units, detailed_modifiers)

            if mod.type == 'BEVEL':
                mod_bevel(output_text, mod, color_title, color_setting,
                          color_value, text_size_normal, color_warning, color_option,
                          units, detailed_modifiers)

            if mod.type == 'BOOLEAN':
                mod_boolean(output_text, mod, color_title, color_setting,
                            color_value, text_size_normal, color_warning, color_option,
                            units, detailed_modifiers)

            if mod.type == 'BUILD':
                mod_build(output_text, mod, color_title, color_setting,
                          color_value, text_size_normal, color_warning, color_option,
                          units, detailed_modifiers)

            if mod.type == 'CAST':
                mod_cast(output_text, mod, color_title, color_setting,
                         color_value, text_size_normal, color_warning, color_option,
                         units, detailed_modifiers)

            if mod.type == 'CORRECTIVE_SMOOTH':
                mod_corrective_smooth(output_text, mod, color_title,
                                      color_setting, color_value, text_size_normal,
                                      color_warning, color_option, units,
                                      detailed_modifiers)

            if mod.type == 'CURVE':
                mod_curve(output_text, mod, color_title, color_setting,
                          color_value, text_size_normal, color_warning, color_option,
                          units, detailed_modifiers)

            if mod.type == 'DECIMATE':
                mod_decimate(output_text, mod, color_title, color_setting,
                             color_value, text_size_normal, color_warning, color_option,
                             units, detailed_modifiers)

            if mod.type == 'DISPLACE':
                mod_displace(output_text, mod, color_title, color_setting,
                             color_value, text_size_normal, color_warning, color_option,
                             units, detailed_modifiers)

            if mod.type == 'EDGE_SPLIT':
                mod_edge_split(output_text, mod, color_title, color_setting,
                               color_value, text_size_normal, color_warning,
                               color_option, units, detailed_modifiers)

            if mod.type == 'HOOK':
                mod_hook(output_text, mod, color_title, color_setting,
                         color_value, text_size_normal, color_warning, color_option,
                         units, detailed_modifiers)

            if mod.type == 'LAPLACIANDEFORM':
                mod_laplacian_deformer(output_text, mod, color_title,
                                       color_setting, color_value, text_size_normal,
                                       color_warning, color_option, units, detailed_modifiers)

            if mod.type == 'LAPLACIANSMOOTH':
                mod_laplacian_smooth(output_text, mod, color_title,
                                     color_setting, color_value, text_size_normal,
                                     color_warning, color_option, units, detailed_modifiers)

            if mod.type == 'LATTICE':
                mod_lattice(output_text, mod, color_title, color_setting,
                            color_value, text_size_normal, color_warning, color_option,
                            units, detailed_modifiers)

            if mod.type == 'MASK':
                mod_mask(output_text, mod, color_title, color_setting,
                         color_value, text_size_normal, color_warning, color_option,
                         units, detailed_modifiers)

            if mod.type == 'MESH_DEFORM':
                mod_mesh_deform(output_text, mod, color_title, color_setting,
                                color_value, text_size_normal, color_warning,
                                color_option, units, detailed_modifiers)

            if mod.type == 'MIRROR':
                mod_mirror(output_text, mod, color_title, color_setting,
                           color_value, text_size_normal, color_warning, color_option,
                           units, detailed_modifiers)

            if mod.type == 'MULTIRES':
                mod_multires(output_text, mod, color_title, color_setting,
                             color_value, text_size_normal, color_warning, color_option,
                             units, detailed_modifiers)

            if mod.type == 'REMESH':
                mod_remesh(output_text, mod, color_title, color_setting,
                           color_value, text_size_normal, color_warning, color_option,
                           units, detailed_modifiers)

            if mod.type == 'SCREW':
                mod_screw(output_text, mod, color_title, color_setting,
                          color_value, text_size_normal, color_warning, color_option,
                          units, detailed_modifiers)

            if mod.type == 'SHRINKWRAP':
                mod_shrinkwrap(output_text, mod, color_title, color_setting,
                               color_value, text_size_normal, color_warning,
                               color_option, units, detailed_modifiers)

            if mod.type == 'SIMPLE_DEFORM':
                mod_simple_deform(output_text, mod, color_title,
                                  color_setting, color_value, text_size_normal,
                                  color_warning, color_option, units, detailed_modifiers)

            if mod.type == 'SKIN':
                mod_skin(output_text, mod, color_title, color_setting,
                         color_value, text_size_normal, color_warning, color_option,
                         units, detailed_modifiers)

            if mod.type == 'SMOOTH':
                mod_smooth(output_text, mod, color_title, color_setting,
                           color_value, text_size_normal, color_warning, color_option,
                           units, detailed_modifiers)

            if mod.type == 'SOLIDIFY':
                mod_solidify(output_text, mod, color_title, color_setting,
                             color_value, text_size_normal, color_warning, color_option,
                             units, detailed_modifiers)

            if mod.type == 'SUBSURF':
                mod_subsurf(output_text, mod, color_title, color_setting,
                            color_value, text_size_normal, color_warning, color_option,
                            units, detailed_modifiers)

            if mod.type == 'SURFACE_DEFORM':
                mod_surface_deform(output_text, mod, color_title,
                                   color_setting, color_value, text_size_normal,
                                   color_warning, color_option, units, detailed_modifiers)

            if mod.type == 'TRIANGULATE':
                mod_triangulate(output_text, mod, color_title, color_setting,
                                color_value, text_size_normal, color_warning,
                                color_option, units, detailed_modifiers)

            if mod.type == 'WARP':
                mod_warp(output_text, mod, color_title, color_setting,
                         color_value, text_size_normal, color_warning, color_option,
                         units, detailed_modifiers)

            if mod.type == 'WAVE':
                mod_wave(output_text, mod, color_title, color_setting,
                         color_value, text_size_normal, color_warning, color_option,
                         units, detailed_modifiers)

            if mod.type == 'WIREFRAME':
                mod_wireframe(output_text, mod, color_title, color_setting,
                              color_value, text_size_normal, color_warning, color_option,
                              units, detailed_modifiers)

            if mod.type == 'WEIGHTED_NORMAL':
                mod_weighted_normals(output_text, mod, color_title,
                                     color_setting, color_value, text_size_normal,
                                     color_warning, color_option, units, detailed_modifiers)

    # WARNING
    # SPACE
    output_text.extend(["SPACE"])
    warning(output_text, color_title, color_setting, color_value,
            text_size_normal, color_warning, color_option, units)

    # bpy.context.area.tag_redraw()
    return output_text
