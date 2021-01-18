import math
import os
import sys
from typing import Callable, Dict
from typing import *

import bpy
# from bpy.props import (
#     StringProperty,
#     BoolProperty,
#     PointerProperty,
#     FloatVectorProperty,
#     FloatProperty,
#     EnumProperty,
#     IntProperty,
#     BoolVectorProperty
# )
import blf

from .functions import *
from . import prefs


# FIXME: It would be better to auto-find and auto-load these, rather than
# having the list hard-coded. Sadly, I was having trouble making that work
# well, so we're just going to do this.
#
# FIXME: Thewe will not get reloaded when the addon is reloaded
from .modifiers.armature import *
from .modifiers.array import *
from .modifiers.bevel import *
from .modifiers.boolean import *
from .modifiers.build import *
from .modifiers.cast import *
from .modifiers.corrective_smooth import *
from .modifiers.curve import *
from .modifiers.decimate import *
from .modifiers.displace import *
from .modifiers.edge_split import *
from .modifiers.hook import *
from .modifiers.laplacian_deform import *
from .modifiers.laplacian_smooth import *
from .modifiers.lattice import *
from .modifiers.mask import *
from .modifiers.mesh_deform import *
from .modifiers.mirror import *
from .modifiers.multires import *
from .modifiers.remesh import *
from .modifiers.screw import *
from .modifiers.shrinkwrap import *
from .modifiers.simple_deform import *
from .modifiers.skin import *
from .modifiers.smooth import *
from .modifiers.solidify import *
from .modifiers.subsurf import *
from .modifiers.surface_deform import *
from .modifiers.triangulate import *
from .modifiers.warp import *
from .modifiers.wave import *
from .modifiers.weighted_normals import *
from .modifiers.wireframe import *

infotext_text_Handle: bpy.types.Object = []


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


def loc(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object) -> None:
    axis_list = (" X ", " Y ", " Z ")

    # LOCATION
    if tuple(obj.location) != (0.0, 0.0, 0.0):
        # output_text.extend(["CR", ('ICON', 'ICON_MAN_TRANS.png'), ("    ", p.color_title, p.text_size_normal)])
        output_text.extend([
            "CR",
            ("L: ", p.color_title, p.text_size_normal),
        ])

        for idx, axis in enumerate(axis_list):
            output_text.extend([
                (axis, p.color_setting, p.text_size_normal),
                (fmt_length(obj.location[idx], 2), p.color_value, p.text_size_normal),
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

        if not float_is_close(obj.scale[0], obj.scale[1], 3) or not float_is_close(obj.scale[1], obj.scale[2], 3):
            output_text.extend([
                (" Non-uniform ", p.color_warning, p.text_size_normal),
            ])

    if any([tuple(obj.location) != (0.0, 0.0, 0.0), tuple(obj.rotation_euler) != (0.0, 0.0, 0.0), tuple(obj.scale) != (1, 1, 1)]):
        output_text.extend(["SPACE"])


# ---------------------------------------------------------------
# NGONS
# ---------------------------------------------------------------
def ngons(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object) -> None:
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
    # CUSTOM NORMALS
    if obj.type == 'MESH':
        if obj.data.has_custom_normals:
            output_text.extend([
                "CR",
                ("CUSTOM NORMALS", p.color_warning, p.text_size_normal),
            ])

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
def sculpt(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object) -> None:
    toolsettings = bpy.context.tool_settings
    sculpt = toolsettings.sculpt
    context_tool = bpy.context.scene.tool_settings.sculpt

    # BRUSH
    brush = bpy.context.tool_settings.sculpt.brush
    capabilities = brush.sculpt_capabilities
    ups = bpy.context.tool_settings.unified_paint_settings

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

    output_text.extend(["SPACE"])

    # FIXME: Should we be accessing this from the context, or just the active object?
    if bpy.context.sculpt_object.use_dynamic_topology_sculpting:
        output_text.extend(["SPACE"])

        # DYNTOPO
        output_text.extend(["CR", ("DYNTOPO ", p.color_title, p.text_size_large)])
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


# ---------------------------------------------------------------
# OBJECT TYPES
# ---------------------------------------------------------------


# ---------------------------------------------------------------
# ARMATURE
# ---------------------------------------------------------------
def armature(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Armature) -> None:
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
def camera(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Camera) -> None:
    # LENS
    # FIXME: Do we want to make the text size scaled for units, everywhere?
    (l, u) = fmt_camera(obj.data.lens, 2).split()
    output_text.extend([
        "CR",
        ("LENS ", p.color_title, p.text_size_normal),
        # Lens length is alway smm
        # FIXME: Or
        (str(l), p.color_value, p.text_size_normal),
        (u, p.color_value, int(p.text_size_normal * 0.80)),
    ])

    # FOCUS
    if obj.data.dof.use_dof and obj.data.dof.focus_object:
        output_text.extend([
            "CR",
            ("FOCUS ", p.color_title, p.text_size_normal),
            (str(obj.data.dof.focus_object.name), p.color_value, p.text_size_normal),
        ])

    else:
        output_text.extend([
            "CR",
            ("DISTANCE ", p.color_title, p.text_size_normal),
            (fmt_length(obj.data.dof.focus_distance, 2), p.color_value, p.text_size_normal),
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
#
# FIXME: What data type should obj be?
def curve_font(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object) -> None:
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
def empty(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object) -> None:
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
#
# FIXME: What type should obj be?
def text_lattice(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object) -> None:
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
#
# FIXME: What data type should obj be?
def cycles_lights(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object) -> None:
    # obj = bpy.context.active_object

    # TYPE
    # FIXME: Type handling probably needs better here
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
def metaball(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.MetaBall) -> None:
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
# WARNING  -   FIXME: Probably not the way to do this
# ---------------------------------------------------------------
def warning(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object) -> None:
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
# UNKNOWN MODIFIERS
# ----------------------------------------------------------------------
def mod_unknown(output_text, p: prefs.InfotextAddonPrefs, obj: bpy.types.Object,
                mod: bpy.types.Modifier) -> None:

    output_text.extend([
        "CR",
        (str(mod.type), p.color_title, p.text_size_normal),
        ("  ", p.color_title, p.text_size_normal),
        (str(mod.name), p.color_value, p.text_size_normal),
    ])

    if not mod.show_viewport:
        output_text.extend([
            (" Hidden ", p.color_warning, p.text_size_normal),
        ])

    output_text.extend([
        (" (Unknown modifier)", p.color_warning, p.text_size_normal),
    ])


# ----------------------------------------------------------------------
# MODIFIER HANDLING
# ----------------------------------------------------------------------
ModifierFunc = Callable[[Any, prefs.InfotextAddonPrefs, bpy.types.Object, bpy.types.Modifier], None]
modifiers: Dict[str, ModifierFunc] = {
    'ARMATURE': mod_armature,
    'ARRAY': mod_array,
    'BEVEL': mod_bevel,
    'BOOLEAN': mod_boolean,
    'BUILD': mod_build,
    'CAST': mod_cast,
    'CORRECTIVE_SMOOTH': mod_corrective_smooth,
    'CURVE': mod_curve,
    'DECIMATE': mod_decimate,
    'DISPLACE': mod_displace,
    'EDGE_SPLIT': mod_edge_split,
    'HOOK': mod_hook,
    'LAPLACIANDEFORM': mod_laplacian_deform,
    'LAPLACIANSMOOTH': mod_laplacian_smooth,
    'LATTICE': mod_lattice,
    'MASK': mod_mask,
    'MESH_DEFORM': mod_mesh_deform,
    'MIRROR': mod_mirror,
    'MULTIRES': mod_multires,
    'REMESH': mod_remesh,
    'SCREW': mod_screw,
    'SHRINKWRAP': mod_shrinkwrap,
    'SIMPLE_DEFORM': mod_simple_deform,
    'SKIN': mod_skin,
    'SMOOTH': mod_smooth,
    'SOLIDIFY': mod_solidify,
    'SUBSURF': mod_subsurf,
    'SURFACE_DEFORM': mod_surface_deform,
    'TRIANGULATE': mod_triangulate,
    'WARP': mod_warp,
    'WAVE': mod_wave,
    'WIREFRAME': mod_wireframe,
    'WEIGHTED_NORMAL': mod_weighted_normals,
    'default': mod_unknown,
}


# ----------------------------------------------------------------------
# ACTUAL INFOTEXT GENERATION
# ----------------------------------------------------------------------
#
#
# FIXME: Should we pass context, as well?
def infotext_key_text(p):
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
        output_text.extend([
            "CR",
            ("No active object", p.color_warning, p.text_size_normal),
        ])
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
        loc(output_text, p, obj)

    # VERT/FACES/EDGES/NGONS
    if p.show_vert_face_tris:
        if obj.type == 'MESH':
            ngons(output_text, p, obj)
            # SPACE
            output_text.extend(["SPACE"])

    # MESH OPTIONS
    if p.show_object_info:
        if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
            mesh_options(output_text, p, obj)

    # SCULPT
    if bpy.context.object.type == 'MESH' and bpy.context.object.mode == 'SCULPT':
        sculpt(output_text, p, obj)
        # SPACE
        output_text.extend(["SPACE"])

    # ----------------------------------------------------------------------
    # OBJECT TYPE HANDLING
    # ----------------------------------------------------------------------
    # ARMATURE
    if obj.type == 'ARMATURE':
        armature(output_text, p, obj)
        # SPACE
        output_text.extend(["SPACE"])

    # CAMERA
    if obj.type == 'CAMERA':
        camera(output_text, p, obj)
        # SPACE
        output_text.extend(["SPACE"])

    # CURVES / FONT
    if obj.type in ['CURVE', 'FONT']:
        curve_font(output_text, p, obj)
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
        empty(output_text, p, obj)
        # SPACE
        output_text.extend(["SPACE"])

    # LATTICE
    if obj.type == 'LATTICE':
        text_lattice(output_text, p, obj)
        # SPACE
        output_text.extend(["SPACE"])

    # LIGHT
    if obj.type == 'LAMP':
        cycles_lights(output_text, p, obj)
        # SPACE
        output_text.extend(["SPACE"])

    # METABALL
    if obj.type == 'META':
        metaball(output_text, p, obj)
        # SPACE
        output_text.extend(["SPACE"])

    # ----------------------------------------------------------------------
    # MODIFIER HANDLING
    # ----------------------------------------------------------------------
    # wm = bpy.context.window_manager

    # GREEN = (0.5, 1, 0, 1)
    # NOIR = (0, 0, 0, 1)
    # BLANC = (1, 1, 1, 1)

    if p.show_modifiers:
        for i, mod in enumerate(obj.modifiers):
            if mod.type in modifiers:
                func = modifiers[mod.type]
            else:
                func = modifiers['default']
            func(output_text, p, obj, mod)

    output_text.extend(["SPACE"])

    # FIXME: should this actually be here?
    warning(output_text, p, obj)

    return output_text


def register():
    if infotext_text_Handle:
        bpy.types.SpaceView3D.draw_handler_remove(infotext_text_Handle[0], 'WINDOW')
    infotext_text_Handle[:] = [
        bpy.types.SpaceView3D.draw_handler_add(infotext_draw_text_callback, (), 'WINDOW', 'POST_PIXEL')]


def unregister():
    # Remove Text
    if infotext_text_Handle:
        bpy.types.SpaceView3D.draw_handler_remove(
            infotext_text_Handle[0], 'WINDOW')
        infotext_text_Handle[:] = []


# class DATA_PT_customdata(MeshButtonsPanel, Panel):
#     bl_label = "Geometry Data"
#     bl_options = {'DEFAULT_CLOSED'}
#     COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

#     def draw(self, context):
#         layout = self.layout
#         layout.use_property_split = True
#         layout.use_property_decorate = False

#         obj = context.object
#         me = context.mesh
#         col = layout.column()

#         col.operator("mesh.customdata_mask_clear", icon='X')
#         col.operator("mesh.customdata_skin_clear", icon='X')

#         if me.has_custom_normals:
#             col.operator("mesh.customdata_custom_splitnormals_clear", icon='X')
#         else:
#             col.operator("mesh.customdata_custom_splitnormals_add", icon='ADD')

#         col = layout.column(heading="Store")

#         col.enabled = obj is not None and obj.mode != 'EDIT'
#         col.prop(me, "use_customdata_vertex_bevel", text="Vertex Bevel Weight")
#         col.prop(me, "use_customdata_edge_bevel", text="Edge Bevel Weight")
#         col.prop(me, "use_customdata_edge_crease", text="Edge Crease")


# class DATA_PT_custom_props_mesh(MeshButtonsPanel, PropertyPanel, Panel):
#     COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
#     _context_path = "object.data"
#     _property_type = bpy.types.Mesh
