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
import math
from math import degrees
from .functions import *
import bmesh
# from .icon.icons import load_icons

from os.path import dirname, join
from . import png

infotext_text_Handle = []
TEXTURES = {}

# ----------------------------------------------------------------------------------------------------------------------
# DRAW ICONS------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------------------------------------------------
# DRAW TEXT ------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def infotext_draw_text_callback():
    drawText = get_addon_preferences().drawText

    if drawText and bpy.context.object is not None:
        infotext_draw_text_array(infotext_key_text())


def infotext_draw_text_array(infotext_key_text):
    addon_pref = get_addon_preferences()
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
    text_size_max = addon_pref.text_size_max
    text_size_mini = addon_pref.text_size_mini
    infotext_text_shadow = addon_pref.infotext_text_shadow
    infotext_shadow_color = addon_pref.infotext_shadow_color
    infotext_shadow_alpha = addon_pref.infotext_shadow_alpha
    infotext_offset_shadow_x = addon_pref.infotext_offset_shadow_x
    infotext_offset_shadow_y = addon_pref.infotext_offset_shadow_y
    infotext_text_pos_x = addon_pref.infotext_text_pos_x * infotext_dpi
    infotext_text_pos_y = addon_pref.infotext_text_pos_y * infotext_dpi
    infotext_text_space = addon_pref.infotext_text_space

    text_size = min(text_size_max, max(text_size_mini, int(bpy.context.area.width / 100)))

    x = t_panel_width + infotext_text_pos_x
    y = bpy.context.region.height - infotext_text_pos_y

    for command in infotext_key_text:
        if len(command) == 3:
            Text, Color, Size = command
            if Text == "SPACE":
                y_offset -= (text_size + infotext_text_space) / 2
            else:
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
            x_offset = 0
            y_offset -= text_size + infotext_text_space

            # space = int(text_size_max *5)

    if infotext_text_shadow:
        blf.disable(0, blf.SHADOW)

    bpy.context.area.tag_redraw()


# ---------------------------------------------------------------
# BLENDER KEYMAPS
# ---------------------------------------------------------------
def blender_keymaps(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, space):
    test_text.extend([CR, ("BLENDER KEYMAPS:", color_value, text_size_normal)])
    test_text.extend([CR, ("", color_title, text_size_normal)])
    test_text.extend([CR, ("G: ", color_title, text_size_normal), ("Move", color_setting, text_size_normal)])
    test_text.extend([CR, ("R: ", color_title, text_size_normal), ("Rotate", color_setting, text_size_normal)])
    test_text.extend([CR, ("S: ", color_title, text_size_normal), ("Scale", color_setting, text_size_normal)])
    test_text.extend([CR, (" ", color_title, text_size_normal)])
    test_text.extend([CR, ("SHFT+D: ", color_title, text_size_normal), ("Duplicate", color_setting, text_size_normal)])
    test_text.extend([CR, ("ALT+D: ", color_title, text_size_normal),
                      ("Duplicate Instance", color_setting, text_size_normal)])
    test_text.extend([CR, ("", color_title, text_size_normal)])
    test_text.extend([CR, ("H: ", color_title, text_size_normal), ("Hide Selection", color_setting, text_size_normal)])
    test_text.extend([CR, ("ALT+H: ", color_title, text_size_normal),
                      ("Unhide Everything", color_setting, text_size_normal)])
    test_text.extend([CR, ("M: ", color_title, text_size_normal), ("Collections", color_setting, text_size_normal)])
    test_text.extend([CR, ("CTRL+A: ", color_title, text_size_normal),
                      ("Apply Transforms", color_setting, text_size_normal)])
    test_text.extend([CR, ("", color_value, text_size_normal)])

    # if bpy.context.object.mode == "OBJECT":

    if bpy.context.object.mode == "EDIT":
        if tuple(bpy.context.tool_settings.mesh_select_mode) == (True, False, False):
            test_text.extend([CR, ("VERTEX MODE: ", color_value, text_size_normal)])
            test_text.extend([CR, ("", color_value, text_size_normal)])
            test_text.extend([CR, ("CTRL+V: ", color_title, text_size_normal),
                              ("Vertex Menu", color_setting, text_size_normal)])
            test_text.extend([CR, ("ALT+M: ", color_title, text_size_normal),
                              ("Merge MEnu", color_setting, text_size_normal)])
            test_text.extend([CR, ("E: ", color_title, text_size_normal),
                              ("Extrude Vertex", color_setting, text_size_normal)])
            test_text.extend([CR, ("F: ", color_title, text_size_normal),
                              ("New Face", color_setting, text_size_normal)])
            test_text.extend([CR, ("K: ", color_title, text_size_normal), ("Knife", color_setting, text_size_normal)])
            test_text.extend([CR, ("P: ", color_title, text_size_normal),
                              ("Separate", color_setting, text_size_normal)])
            test_text.extend([CR, ("X: ", color_title, text_size_normal), ("Delete", color_setting, text_size_normal)])
            test_text.extend([CR, ("Y: ", color_title, text_size_normal), ("Split", color_setting, text_size_normal)])
            test_text.extend([CR, ("CTRL+SHIT+B: ", color_title, text_size_normal),
                              ("Bevel Vertices", color_setting, text_size_normal)])
            test_text.extend([CR, ("ALT+D: ", color_title, text_size_normal),
                              ("Extand Vertex", color_setting, text_size_normal)])
            test_text.extend([CR, ("ALT+S: ", color_title, text_size_normal),
                              ("Shrink Fatten", color_setting, text_size_normal)])

        elif tuple(bpy.context.tool_settings.mesh_select_mode) == (False, True, False):
            test_text.extend([CR, ("EDGE MODE: ", color_value, text_size_normal)])
            test_text.extend([CR, ("", color_value, text_size_normal)])
            test_text.extend([CR, ("CTRL+E: ", color_title, text_size_normal),
                              ("Edge Menu", color_setting, text_size_normal)])
            test_text.extend([CR, ("ALT+M: ", color_title, text_size_normal),
                              ("Merge MEnu", color_setting, text_size_normal)])
            test_text.extend([CR, ("E: ", color_title, text_size_normal),
                              ("Extrude Edge", color_setting, text_size_normal)])
            test_text.extend([CR, ("F: ", color_title, text_size_normal),
                              ("New Face", color_setting, text_size_normal)])
            test_text.extend([CR, ("K: ", color_title, text_size_normal), ("Knife", color_setting, text_size_normal)])
            test_text.extend([CR, ("P: ", color_title, text_size_normal),
                              ("Separate", color_setting, text_size_normal)])
            test_text.extend([CR, ("X: ", color_title, text_size_normal), ("Delete", color_setting, text_size_normal)])
            test_text.extend([CR, ("Y: ", color_title, text_size_normal), ("Split", color_setting, text_size_normal)])
            test_text.extend([CR, ("CTRL+B: ", color_title, text_size_normal),
                              ("Bevel Edge", color_setting, text_size_normal)])
            test_text.extend([CR, ("ALT+F: ", color_title, text_size_normal),
                              ("Fill", color_setting, text_size_normal)])
            test_text.extend([CR, ("ALT+S: ", color_title, text_size_normal),
                              ("Shrink Fatten", color_setting, text_size_normal)])

        elif tuple(bpy.context.tool_settings.mesh_select_mode) == (False, False, True):
            test_text.extend([CR, ("FACE MODE: ", color_value, text_size_normal)])
            test_text.extend([CR, ("", color_value, text_size_normal)])
            test_text.extend([CR, ("CTRL+F: ", color_title, text_size_normal),
                              ("Face Menu", color_setting, text_size_normal)])
            test_text.extend([CR, ("ALT+M: ", color_title, text_size_normal),
                              ("Merge MEnu", color_setting, text_size_normal)])
            test_text.extend([CR, ("ALT+N: ", color_title, text_size_normal),
                              ("Normal Menu", color_setting, text_size_normal)])
            test_text.extend([CR, ("E: ", color_title, text_size_normal),
                              ("Extrude Face", color_setting, text_size_normal)])
            test_text.extend([CR, ("F: ", color_title, text_size_normal),
                              ("New Face", color_setting, text_size_normal)])
            test_text.extend([CR, ("I: ", color_title, text_size_normal), ("Inset", color_setting, text_size_normal)])
            test_text.extend([CR, ("K: ", color_title, text_size_normal), ("Knife", color_setting, text_size_normal)])
            test_text.extend([CR, ("P: ", color_title, text_size_normal),
                              ("Separate", color_setting, text_size_normal)])
            test_text.extend([CR, ("X: ", color_title, text_size_normal), ("Delete", color_setting, text_size_normal)])
            test_text.extend([CR, ("Y: ", color_title, text_size_normal), ("Split", color_setting, text_size_normal)])
            test_text.extend([CR, ("CTRL+T: ", color_title, text_size_normal),
                              ("Triangulate", color_setting, text_size_normal)])
            test_text.extend([CR, ("ALT+J: ", color_title, text_size_normal),
                              ("Tri To Quad", color_setting, text_size_normal)])
            test_text.extend([CR, ("ALT+S: ", color_title, text_size_normal),
                              ("Shrink Fatten", color_setting, text_size_normal)])


# ---------------------------------------------------------------
# MODE
# ---------------------------------------------------------------


def mode(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, text_size_large, space):
    obj = bpy.context.active_object

    mode = obj.mode

    if bpy.context.object.mode == "OBJECT":
        # test_text.extend([CR, ('ICON', 'ICON_OBJECT_DATAMODE.png'), ("   OBJECT MODE", color_title, text_size_deux)])
        test_text.extend([CR, ("OBJECT MODE", color_title, text_size_large)])

    elif bpy.context.object.mode == "EDIT":
        # test_text.extend([CR, ('ICON', 'ICON_EDITMODE_HLT.png'), ("   EDIT MODE", color_title, text_size_deux)])
        test_text.extend([CR, ("EDIT MODE", color_title, text_size_large)])

    elif bpy.context.object.mode == "SCULPT":
        # test_text.extend([CR, ('ICON', 'ICON_SCULPTMODE_HLT.png'), ("   SCULPT MODE", color_title, text_size_deux)])
        test_text.extend([CR, ("SCULPT MODE", color_title, text_size_large)])

    elif bpy.context.object.mode == "VERTEX_PAINT":
        # test_text.extend([CR, ('ICON', 'ICON_VPAINT_HLT.png'), ("    VERTEX PAINT MODE", color_title, text_size_deux)])
        test_text.extend([CR, ("VERTEX PAINT MODE", color_title, text_size_large)])

    elif bpy.context.object.mode == "WEIGHT_PAINT":
        # test_text.extend([CR, ('ICON', 'ICON_WPAINT_HLT.png'), ("    WEIGHT PAINT MODE", color_title, text_size_deux)])
        test_text.extend([CR, ("WEIGHT PAINT MODE", color_title, text_size_large)])

    elif bpy.context.object.mode == "TEXTURE_PAINT":
        # test_text.extend([CR, ('ICON', 'ICON_TPAINT_HLT.png'), ("    TEXTURE PAINT MODE", color_title, text_size_deux)])
        test_text.extend([CR, ("TEXTURE PAINT MODE", color_title, text_size_large)])

    # elif bpy.context.object.mode == "PARTICLE":
    #     test_text.extend([CR, ('ICON', 'ICON_PARTICLEMODE.png'), ("    PARTICLES EDIT MODE", color_title, text_size_deux)])

    elif bpy.context.object.mode == "POSE":
        # test_text.extend([CR, ('ICON', 'ICON_POSE_HLT.png'), ("    POSE MODE", color_title, text_size_deux)])
        test_text.extend([CR, ("POSE MODE", color_title, text_size_large)])

    # test_text.extend(
    #     [CR, ('ICON', 'ICON_OBJECT_DATAMODE.png'), ("    ", color_setting, text_size_normal)])

    # if "_" in mode:
    #     text_mode = mode.replace("_", " ")
    #     test_text.extend([CR,('ICON', 'ICON_OBJECT_DATAMODE.png'), ("    ", color_setting, text_size_normal), (text_mode, color_title, text_size_deux)])
    # else:
    #     test_text.extend([CR, ("{} MODE".format(mode), color_title, text_size_deux)])

# ---------------------------------------------------------------
# NAME
# ---------------------------------------------------------------


def name(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, text_size_large, space):
    obj = bpy.context.active_object

    test_text.extend([CR, ("", color_setting, int(text_size_normal * 5)),
                      CR,  # CR, CR,
                      # (obj.type + ": ", color_title, text_size_normal),
                      (obj.type, color_title, text_size_normal), CR, CR,
                      (obj.name, color_value, int(text_size_large * 1.5)), CR,
                      ])
    # test_text.extend([CR, (obj.type, color_title, text_size_normal)])
    # test_text.extend([CR, ("Name: ", color_title, text_size_normal), (obj.name, color_value, text_size_normal)])

    # FIXME: enable icons once icon code is enabled
    # if obj.type == 'MESH':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_MESH.png'), ("    ", color_setting, text_size_normal)])
    #     test_text.extend([CR, ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])
    # elif obj.type == 'CURVE':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_CURVE.png'), ("    ", color_setting, text_size_normal)])
    #     test_text.extend([CR, ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])
    # elif obj.type == 'EMPTY':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_EMPTY.png'), ("    ", color_setting, text_size_normal)])
    #     test_text.extend([CR, ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'CAMERA':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_CAMERA.png'), ("     ", color_setting, text_size_normal)])
    #     test_text.extend([CR, ("     ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'LATTICE':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_LATTICE.png'), ("     ", color_setting, text_size_normal)])
    #     test_text.extend([CR, ("     ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'META':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_META.png'), ("    ", color_setting, text_size_normal)])
    #     test_text.extend([CR, ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'ARMATURE':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_ARMATURE.png'), ("    ", color_setting, text_size_normal)])
    #     test_text.extend([CR, ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'FONT':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_FONT.png'), ("     ", color_setting, text_size_normal)])
    #     test_text.extend([CR, ("     ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'LATTICE':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_LATTICE.png'), ("    ", color_setting, text_size_normal)])
    #     test_text.extend([CR, ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'LAMP':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_LAMP.png'), ("    ", color_setting, text_size_normal)])
    #     test_text.extend([CR, ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'SURFACE':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_SURFACE.png'), ("    ", color_setting, text_size_normal)])
    #     test_text.extend([CR, ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])

    # elif obj.type == 'SPEAKER':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_SPEAKER.png'), ("    ", color_setting, text_size_normal)])
    #     test_text.extend([CR, ("    ", color_setting, text_size_normal), (obj.name, color_value, text_size_normal)])


# ---------------------------------------------------------------
# LOCATION / ROTATION / SCALE
# ---------------------------------------------------------------


def loc(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space):
    obj = bpy.context.active_object

    axis_list = (" X ", " Y ", " Z ")
    # LOCATION
    if tuple(obj.location) != (0.0, 0.0, 0.0):
        # test_text.extend([CR,("LOCATION ", color_title, text_size_normal),
        #                   ("  %s" % round(obj.location[0], 2), color_value, text_size_normal), (units, color_value, text_size_normal),
        #                   ("  %s" % round(obj.location[1], 2), color_value, text_size_normal), (units, color_value, text_size_normal),
        #                   ("  %s" % round(obj.location[2], 2), color_value, text_size_normal), (units, color_value, text_size_normal)])

        # test_text.extend([CR, ('ICON', 'ICON_MAN_TRANS.png'), ("    ", color_title, text_size_normal)])
        test_text.extend([CR, ("L: ", color_title, text_size_normal)])

        for idx, axis in enumerate(axis_list):
            test_text.extend([(axis, color_setting, text_size_normal),
                              (str(round(obj.location[idx], 2)), color_value, text_size_normal),
                              (units, color_value, text_size_normal)])

    # ROTATION
    if tuple(obj.rotation_euler) != (0.0, 0.0, 0.0):
        # test_text.extend([CR, ('ICON', 'ICON_MAN_ROT.png'), ("    ", color_title, text_size_normal)])
        test_text.extend([CR, ("R: ", color_title, text_size_normal)])

        for idx, axis in enumerate(axis_list):
            test_text.extend([(axis, color_setting, text_size_normal),
                              (str(round(math.degrees(obj.rotation_euler[idx]), 2)), color_value, text_size_normal), ("°", color_value, text_size_normal)])

    # SCALE
    if tuple(obj.scale) != (1, 1, 1):
        # test_text.extend([CR, ('ICON', 'ICON_MAN_SCALE.png'), ("    ", color_title, text_size_normal)])
        test_text.extend([CR, ("S: ", color_title, text_size_normal)])

        for idx, axis in enumerate(axis_list):
            test_text.extend([(axis, color_setting, text_size_normal),
                              (str(round(obj.scale[idx], 2)), color_value, text_size_normal)])

    if any([tuple(obj.location) != (0.0, 0.0, 0.0), tuple(obj.rotation_euler) != (0.0, 0.0, 0.0), tuple(obj.scale) != (1, 1, 1)]):
        # SPACE
        test_text.extend([("SPACE", color_title, space)])

# ---------------------------------------------------------------
# NGONS
# ---------------------------------------------------------------


def ngons(test_text, CR, color_title, color_value, text_size_normal, space):
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
    # test_text.extend([CR, ('ICON', 'vert.png'), ("    ", color_title, text_size_normal),
    #                   (str(vcount), color_value, text_size_normal)])
    test_text.extend([CR, ("V: ", color_title, text_size_normal),
                      (str(vcount), color_value, text_size_normal)])

    # EDGES
    # test_text.extend([("  ", color_title, text_size_normal), ('ICON', 'edge.png'), ("    ", color_title, text_size_normal),
    #                   (str(ecount), color_value, text_size_normal)])
    test_text.extend([("  E: ", color_title, text_size_normal), (" ", color_title, text_size_normal),
                      (str(ecount), color_value, text_size_normal)])

    # FACES
    # test_text.extend([("  ", color_title, text_size_normal), ('ICON', 'face.png'), ("    ", color_title, text_size_normal),
    #                   (str(fcount), color_value, text_size_normal)])
    test_text.extend([("  F: ", color_title, text_size_normal), (" ", color_title, text_size_normal),
                      (str(fcount), color_value, text_size_normal)])

    if not bpy.context.object.mode == 'SCULPT':
        tcount = infotext.face_type_count['TRIS']
        ncount = infotext.face_type_count['NGONS']
        # TRIS
        if tcount:
            # test_text.extend([("  ", color_title, text_size_normal), ('ICON', 'triangle.png'), ("    ", color_title, text_size_normal),
            #                   (str(tcount), color_value, text_size_normal)])

            test_text.extend([("  T: ", color_title, text_size_normal), (" ", color_title, text_size_normal),
                              (str(tcount), color_value, text_size_normal)])

        # NGONS ICON_OBJECT_DATA
        if ncount:
            # test_text.extend([(" ", color_title, text_size_normal), ('ICON', 'ngons.png'),
            #                   ("     ", color_title, text_size_normal), (str(ncount), color_value, text_size_normal)])

            test_text.extend([("  N: ", color_title, text_size_normal),
                              (" ", color_title, text_size_normal), (str(ncount), color_value, text_size_normal)])

# ---------------------------------------------------------------
# MESH OPTIONS
# ---------------------------------------------------------------


def mesh_options(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, space):
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
                # test_text.extend([CR, ('ICON', 'ICON_SMOOTH.png'),("     ", color_title, text_size_normal)])
                test_text.extend([CR, ("MATERIAL: ", color_title, text_size_normal)])
                test_text.extend([(str(len(obj.material_slots)), color_setting, text_size_normal), (" ", color_title,
                                                                                                    text_size_normal), (str(obj.active_material.name), color_value, text_size_normal)])

                if obj.active_material.users >= 2:
                    test_text.extend([(" ", color_setting, text_size_normal), (str(obj.active_material.users),
                                                                               color_setting, text_size_normal), (" users", color_setting, text_size_normal)])
                if obj.active_material.use_fake_user:
                    test_text.extend([(" ,FAKE USER ", color_setting, text_size_normal)])
            else:
                test_text.extend([CR, ("SLOT ONLY", color_title, text_size_normal)])

            # SPACE
            test_text.extend([("SPACE", color_title, space)])

    if obj.type == 'MESH':
        # AUTOSMOOTH
        if obj.data.use_auto_smooth:
            test_text.extend([CR, ("AUTOSMOOTH ", color_title, text_size_normal)])
            # ANGLE
            test_text.extend([(" ANGLE ", color_setting, text_size_normal), (
                str(round(math.degrees(obj.data.auto_smooth_angle), 1)), color_value, text_size_normal),
                ("°", color_value, text_size_normal)])

    if obj.type in ['MESH', 'LATTICE']:
        # VERTEX GROUPS
        if obj.vertex_groups:
            test_text.extend([CR, ("VERTEX GROUPS", color_title, text_size_normal)])
            test_text.extend([(" ", color_title, text_size_normal),
                              (str(len(obj.vertex_groups)), color_setting, text_size_normal)])
            test_text.extend([(" ", color_title, text_size_normal),
                              (str(obj.vertex_groups[int(obj.vertex_groups.active_index)].name), color_value, text_size_normal)])

    if obj.type in ['CURVE', 'MESH', 'LATTICE']:
        # SHAPE KEYS
        if obj.data.shape_keys:
            test_text.extend([CR, ("SHAPE KEYS", color_title, text_size_normal)])
            test_text.extend([(" ", color_title, text_size_normal),
                              (str(len(obj.data.shape_keys.key_blocks)), color_setting, text_size_normal)])
            test_text.extend([(" ", color_title, text_size_normal),
                              (str(obj.data.shape_keys.key_blocks[int(bpy.context.object.active_shape_key_index)].name), color_value, text_size_normal)])

            if bpy.context.object.mode == 'OBJECT':
                test_text.extend([(" VALUE ", color_setting, text_size_normal),
                                  (str(round(obj.data.shape_keys.key_blocks[int(bpy.context.object.active_shape_key_index)].value, 3)),
                                   color_value, text_size_normal)])

    if obj.type == 'MESH':
        # UV's
        if obj.data.uv_layers:
            test_text.extend([CR, ("UV's", color_title, text_size_normal)])
            test_text.extend([(" ", color_title, text_size_normal), (str(
                len(obj.data.uv_layers)), color_setting, text_size_normal)])
            test_text.extend([(" ", color_title, text_size_normal), (str(
                obj.data.uv_layers[int(obj.data.uv_layers.active_index)].name), color_value, text_size_normal)])

        # VERTEX COLORS
        if obj.data.vertex_colors:
            test_text.extend([CR, ("VERTEX COLORS", color_title, text_size_normal)])
            test_text.extend([(" ", color_title, text_size_normal),
                              (str(len(obj.data.vertex_colors)), color_setting, text_size_normal)])
            test_text.extend([(" ", color_title, text_size_normal),
                              (str(obj.data.vertex_colors[int(obj.data.vertex_colors.active_index)].name), color_value, text_size_normal)])

    if obj.type == 'LATTICE':
        if any([obj.vertex_groups, obj.data.shape_keys]):
            # SPACE
            test_text.extend([("SPACE", color_title, space)])

    if obj.type in ['CURVE', 'FONT']:
        if any([obj.vertex_groups, obj.data.shape_keys]):
            # SPACE
            test_text.extend([("SPACE", color_title, space)])

    if obj.type == 'MESH':
        if any([obj.data.use_auto_smooth, obj.vertex_groups, obj.data.shape_keys, obj.data.uv_layers, obj.data.vertex_colors]):
            # SPACE
            test_text.extend([("SPACE", color_title, space)])

# ---------------------------------------------------------------
# SCULPT
# ---------------------------------------------------------------


def sculpt(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, text_size_large, units, space):
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
    test_text.extend([("SPACE", color_title, space)])

    # if bpy.types.Brush == 'GRAB':
    # test_text.extend([CR, ('ICON', 'grab.png'), ("    ", color_setting, text_size_normal)])

    test_text.extend([CR, (str(brush.name.upper()), color_title, text_size_large)])

    # SPACE
    test_text.extend([("SPACE", color_title, space)])

    # RADIUS
    test_text.extend([CR, ("RADIUS ", color_setting, text_size_normal),
                      (str(round(ups.size, 2)), color_value, text_size_normal), (" px", color_value, text_size_normal)])
    # STRENGTH
    test_text.extend([CR, ("STRENGTH ", color_setting, text_size_normal),
                      (str(round(brush.strength, 3)), color_value, text_size_normal)])

    # STRENGTH
    brush_autosmooth = bpy.data.brushes[brush.name].auto_smooth_factor
    if brush_autosmooth:
        test_text.extend([CR, ("AUTOSMOOTH ", color_setting, text_size_normal),
                          (str(round(brush_autosmooth, 3)), color_value, text_size_normal)])

    brush_use_frontface = bpy.data.brushes[brush.name].use_frontface
    if bpy.data.brushes[brush.name].use_frontface:
        test_text.extend([CR, ("FRONT FACE ", color_setting, text_size_normal),
                          (str(brush_use_frontface), color_value, text_size_normal)])

    # brush_stroke_method = bpy.data.brushes[brush.name].stroke_method
    # if brush_stroke_method == 'SPACE':
    #     test_text.extend([CR, ("STROKE METHOD ", color_setting, text_size_normal)])
    #     test_text.extend([("SPACE", color_value, text_size_normal)])
    # else:
    #     test_text.extend([CR, ("STROKE METHOD ", color_setting, text_size_normal),
    #                       (str(brush_stroke_method), color_value, text_size_normal)])

    # SPACE
    test_text.extend([("SPACE", color_title, space)])

    if bpy.context.sculpt_object.use_dynamic_topology_sculpting:
        # SPACE
        test_text.extend([("SPACE", color_title, space)])

        # DYNTOPO
        test_text.extend([CR, ("DYNTOPO ", color_title, text_size_large)])
        # SPACE
        test_text.extend([("SPACE", color_title, space)])

        if context_tool.detail_type_method == 'CONSTANT':

            test_text.extend([CR, ("CONSTANT DETAIL ", color_setting, text_size_normal),
                              (str(round(context_tool.constant_detail_resolution, 2)), color_value, text_size_normal)])

        elif context_tool.detail_type_method == 'RELATIVE':
            test_text.extend([CR, ("RELATIVE DETAIL ", color_setting, text_size_normal),
                              (str(round(context_tool.detail_size, 2)), color_value,
                               text_size_normal), (" px", color_value, text_size_normal)])
        else:
            test_text.extend([CR, ("BRUSH DETAIL ", color_setting, text_size_normal),
                              (str(round(context_tool.detail_percent, 2)), color_value,
                               text_size_normal), ("%", color_value, text_size_normal)])

        # SUBDIV METHOD

        # SUBDIVIDE_COLLAPSE
        if context_tool.detail_refine_method == 'SUBDIVIDE_COLLAPSE':
            test_text.extend([CR, (str("SUBDIVIDE COLLAPSE"), color_setting, text_size_normal)])

        # COLLAPSE
        elif context_tool.detail_refine_method == 'COLLAPSE':
            test_text.extend([CR, (str("COLLAPSE"), color_setting, text_size_normal)])

        # SUBDIVIDE
        else:
            test_text.extend([CR, (str("SUBDIVIDE"), color_setting, text_size_normal)])

        # SMOOTH SHADING
        if context_tool.use_smooth_shading:
            test_text.extend([CR, (str("SMOOTH SHADING"), color_value, text_size_normal)])

        # SYMMETRIZE DIRECTION
        test_text.extend([CR, (str("SYMMETRIZE "), color_setting, text_size_normal),
                          (str(context_tool.symmetrize_direction.lower().capitalize()), color_value, text_size_normal)])

        # SPACE
        test_text.extend([("SPACE", color_title, space)])

    # SYMMETRIZE
    if any([context_tool.use_symmetry_x, context_tool.use_symmetry_y, context_tool.use_symmetry_z]):
        test_text.extend([CR, (str("MIRROR"), color_setting, text_size_normal)])
        if context_tool.use_symmetry_x:
            test_text.extend([(str(" X "), color_value, text_size_normal)])
        if context_tool.use_symmetry_y:
            test_text.extend([(str(" Y "), color_value, text_size_normal)])
        if context_tool.use_symmetry_z:
            test_text.extend([(str(" Z "), color_value, text_size_normal)])

    if context_tool.use_symmetry_feather:
        test_text.extend([CR, (str("FEATHER "), color_title, text_size_normal)])

    # LOCK
    if any([context_tool.lock_x, context_tool.lock_y, context_tool.lock_z]):
        test_text.extend([CR, (str("LOCK  "), color_setting, text_size_normal)])
        if context_tool.lock_x:
            test_text.extend([(str(" X "), color_value, text_size_normal)])
        if context_tool.lock_y:
            test_text.extend([(str(" Y "), color_value, text_size_normal)])
        if context_tool.lock_z:
            test_text.extend([(str(" Z "), color_value, text_size_normal)])

    # TILE
    if any([context_tool.tile_x, context_tool.tile_y, context_tool.tile_z]):
        test_text.extend([CR, (str("TILE    "), color_setting, text_size_normal)])
        if context_tool.tile_x:
            test_text.extend([(str(" X "), color_value, text_size_normal)])
        if context_tool.tile_y:
            test_text.extend([(str(" Y "), color_value, text_size_normal)])
        if context_tool.tile_z:
            test_text.extend([(str(" Z "), color_value, text_size_normal)])

# ----------------------------------------------------------------------------------------------------------------------
# MODIFIERS ------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------
# ARRAY
# ---------------------------------------------------------------


def mod_array(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR,('ICON', 'ICON_MOD_ARRAY.png'),("    ", color_setting, text_size_normal), (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:

                # FIT MODE
                if mod.fit_type == 'FIXED_COUNT':
                    test_text.extend([(" Count ", color_setting, text_size_normal),
                                      (str(mod.count), color_value, text_size_normal)])

                elif mod.fit_type == 'FIT_CURVE':
                    if mod.curve:
                        # Object
                        test_text.extend([(" Curve ", color_setting, text_size_normal),
                                          (mod.curve.name, color_value, text_size_normal)])
                    else:
                        test_text.extend([(" No Curve Selected", hidden, text_size_normal)])

                else:
                    test_text.extend([(" Length ", color_setting, text_size_normal),
                                      (str(round(mod.fit_length, 2)), color_value, text_size_normal)])

                # CONSTANT
                if mod.use_constant_offset:
                    # test_text.extend([(" Constant ", color_setting, text_size_normal),
                    #                   ("%s" %round(mod.constant_offset_displace[0], 1),color_value, text_size_normal),
                    #                   ("  %s" %round(mod.constant_offset_displace[1], 1),color_value, text_size_normal),
                    #                   ("  %s" %round(mod.constant_offset_displace[2], 1),color_value, text_size_normal)])

                    test_text.extend([(" Constant ", color_setting, text_size_normal)])

                    # X
                    if mod.constant_offset_displace[0] != 0:
                        test_text.extend(
                            [(" X ", color_setting, text_size_normal), (str(round(mod.constant_offset_displace[0], 1)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                    # Y
                    if mod.constant_offset_displace[1] != 0:
                        test_text.extend(
                            [(" Y ", color_setting, text_size_normal), (str(round(mod.constant_offset_displace[1], 1)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                    # Z
                    if mod.constant_offset_displace[2] != 0:
                        test_text.extend(
                            [(" Z ", color_setting, text_size_normal), (str(round(mod.constant_offset_displace[2], 1)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                # RELATIVE
                elif mod.use_relative_offset:
                    test_text.extend([(" Relative ", color_setting, text_size_normal)])

                    # X
                    if mod.relative_offset_displace[0] != 0:
                        test_text.extend([(" X ", color_setting, text_size_normal), (str(
                            round(mod.relative_offset_displace[0], 1)), color_value, text_size_normal)])

                    # Y
                    if mod.relative_offset_displace[1] != 0:
                        test_text.extend([(" Y ", color_setting, text_size_normal), (str(
                            round(mod.relative_offset_displace[1], 1)), color_value, text_size_normal)])

                    # Z
                    if mod.relative_offset_displace[2] != 0:
                        test_text.extend([(" Z ", color_setting, text_size_normal), (str(
                            round(mod.relative_offset_displace[2], 1)), color_value, text_size_normal)])

                # MERGE
                if mod.use_merge_vertices:
                    test_text.extend([(" Merge ", color_setting, text_size_normal),
                                      (str(round(mod.merge_threshold, 3)), color_value, text_size_normal)])

                    if mod.use_merge_vertices_cap:
                        test_text.extend([(" First Last ", color_setting, text_size_normal)])

                # OPTIONS
                if any([mod.use_object_offset, mod.start_cap, mod.end_cap]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # OBJECT OFFSET
                    if mod.use_object_offset:
                        if mod.offset_object:
                            test_text.extend([(" Object Offset ", color_setting, text_size_normal),
                                              (mod.offset_object.name, color_value, text_size_normal)])
                        else:
                            test_text.extend([(" No Object Selected", hidden, text_size_normal)])

                    # STAR CAP
                    if mod.start_cap:
                        test_text.extend([(" Start Cap ", color_setting, text_size_normal),
                                          (mod.start_cap.name, color_value, text_size_normal)])

                    # END CAP
                    if mod.end_cap:
                        test_text.extend([(" End Cap ", color_setting, text_size_normal),
                                          (mod.end_cap.name, color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])


# ---------------------------------------------------------------
# BEVEL
# ---------------------------------------------------------------
def mod_bevel(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    wm = bpy.context.window_manager
    obj = bpy.context.active_object

    if obj.type in {'MESH', 'CURVE', 'FONT'}:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_BEVEL.png'), ("     ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])

        # if self.active_mod:
        #     test_text.extend([CR, (str(mod.name.upper()), hidden, text_size_normal)])
        # else:
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # WIDTH
                test_text.extend([(" Width ", color_setting, text_size_normal), (str(round(mod.width, 2)),
                                                                                 color_value, text_size_normal), (units, color_value, text_size_normal)])

                # SEGMENTS
                test_text.extend([(" Segments ", color_setting, text_size_normal),
                                  (str(mod.segments), color_value, text_size_normal)])

                # PROFILE
                test_text.extend([(" Profile ", color_setting, text_size_normal),
                                  (str(round(mod.profile, 2)), color_value, text_size_normal)])

                # LIMIT METHOD
                test_text.extend([(" ", color_setting, text_size_normal),
                                  (str(mod.limit_method.lower().capitalize()), color_setting, text_size_normal)])

                # ANGLE
                if mod.limit_method == 'ANGLE':
                    test_text.extend([("  ", color_setting, text_size_normal),
                                      (str(round(math.degrees(mod.angle_limit), 2)), color_value, text_size_normal),
                                      ("°", color_value, text_size_normal)])
                # VERTEX GROUP
                elif mod.limit_method == 'VGROUP':

                    if mod.vertex_group:
                        test_text.extend([("  ", color_setting, text_size_normal),
                                          (str(mod.vertex_group), color_value, text_size_normal)])
                    else:
                        test_text.extend([(" No Vertex Group Selected ", hidden, text_size_normal)])

                # SPEEDFLOW
                if obj.get('SpeedFlow') and 'Bevel' in obj['SpeedFlow']:
                    if obj['SpeedFlow']['Bevel']:
                        test_text.extend([(" SUBDIV ", color_value, text_size_normal)])
                    else:
                        test_text.extend([(" NO-SUBDIV ", color_value, text_size_normal)])

                # OPTIONS
                if any([mod.use_clamp_overlap, mod.loop_slide, mod.use_only_vertices, mod.offset_type]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # LOOP SLIDE
                    if mod.loop_slide:
                        test_text.extend([(" Loop Slide ", color_setting, text_size_normal)])

                    # CLAMP
                    if mod.use_clamp_overlap:
                        test_text.extend([(" Clamp ", color_setting, text_size_normal)])

                    # ONLY VERTICES
                    if mod.use_only_vertices:
                        test_text.extend([(" Only Vertices ", color_setting, text_size_normal)])

                    # OFFSET TYPE
                    test_text.extend([(" Width Method ", color_setting, text_size_normal),
                                      (str(mod.offset_type.lower().capitalize()), color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# BOOLEAN
# ---------------------------------------------------------------


def mod_boolean(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_BOOLEAN.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # OPERATION
                test_text.extend([(" ", color_title, text_size_normal),
                                  (str(mod.operation), color_value, text_size_normal)])
                if mod.object:
                    # Object
                    test_text.extend([(" Object ", color_setting, text_size_normal),
                                      (mod.object.name, color_value, text_size_normal)])
                else:
                    test_text.extend([(" No object Selected", hidden, text_size_normal)])

                # SOLVER
                # if (hasattr(bpy.context.preferences.system, 'opensubdiv_compute_type')):
                # if bpy.app.version == (2, 79, 0):
                #     test_text.extend([(" ", color_title, text_size_normal),
                #                           (str(mod.solver.upper()), color_value, text_size_normal)])

                # OVERLAP THRESHOLD
                # if mod.solver == 'BMESH':
                #     if mod.double_threshold > 0 :
                #         test_text.extend([(" Overlap Threshold ", color_setting, text_size_normal),
                #                           (str(round(mod.double_threshold,2)), color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# BUILD
# ---------------------------------------------------------------


def mod_build(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_BUILD.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # START
                test_text.extend([(" Start ", color_setting, text_size_normal),
                                  (str(round(mod.frame_start, 2)), color_value, text_size_normal)])

                # LENGTH
                test_text.extend([(" Length ", color_setting, text_size_normal),
                                  (str(round(mod.frame_duration, 2)), color_value, text_size_normal)])

                # SEED
                if mod.use_random_order:
                    test_text.extend([(" Seed ", color_setting, text_size_normal),
                                      (str(mod.seed), color_value, text_size_normal)])

                if mod.use_reverse:
                    test_text.extend([(" Reversed ", color_setting, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# DECIMATE
# ---------------------------------------------------------------


def mod_decimate(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_DECIM.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # COLLAPSE
                if mod.decimate_type == 'COLLAPSE':
                    test_text.extend([(" Collapse ", color_setting, text_size_normal)])
                    test_text.extend([(" Ratio ", color_setting, text_size_normal),
                                      (str(round(mod.ratio, 2)), color_value, text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                          (str(mod.vertex_group), color_value, text_size_normal)])

                        # FACTOR
                        test_text.extend([(" Factor ", color_setting, text_size_normal),
                                          (str(round(mod.vertex_group_factor, 2)), color_value, text_size_normal)])
                    # OPTIONS
                    if any([mod.use_collapse_triangulate, mod.use_symmetry]):
                        test_text.extend([CR, ("----", color_title, text_size_normal)])

                        # TRIANGULATE
                        if mod.use_collapse_triangulate:
                            test_text.extend([(" Triangulate ", color_setting, text_size_normal)])

                        # SYMMETRY
                        if mod.use_symmetry:
                            test_text.extend([(" Symmetry ", color_setting, text_size_normal),
                                              (str(mod.symmetry_axis), color_value, text_size_normal)])

                # UN-SUBDIVDE
                elif mod.decimate_type == 'UNSUBDIV':
                    test_text.extend([(" Un-subdivide ", color_setting, text_size_normal)])
                    test_text.extend([(" Iteration ", color_setting, text_size_normal),
                                      (str(round(mod.iterations, 2)), color_value, text_size_normal)])
                # PLANAR
                else:
                    test_text.extend([(" Planar ", color_setting, text_size_normal)])
                    test_text.extend([(" Angle Limit ", color_setting, text_size_normal), (
                        str(round(math.degrees(mod.angle_limit), 1)), color_value, text_size_normal),
                        ("°", color_value, text_size_normal)])

                    # OPTIONS
                    if any([mod.use_dissolve_boundaries, mod.delimit]):
                        test_text.extend([CR, ("----", color_title, text_size_normal)])

                        # ALL BOUNDARIES
                        if mod.use_dissolve_boundaries:
                            test_text.extend([(" All Boundaries ", color_setting, text_size_normal)])

                        # DELIMIT
                        if mod.delimit:
                            test_text.extend([(" Delimit ", color_setting, text_size_normal)])
                            if mod.delimit == {'NORMAL'}:
                                test_text.extend([(" NORMAL ", color_value, text_size_normal)])
                            elif mod.delimit == {'MATERIAL'}:
                                test_text.extend([(" MATERIAL ", color_value, text_size_normal)])
                            elif mod.delimit == {'SEAM'}:
                                test_text.extend([(" SEAM ", color_value, text_size_normal)])
                            elif mod.delimit == {'SHARP'}:
                                test_text.extend([(" SHARP ", color_value, text_size_normal)])
                            elif mod.delimit == {'UV'}:
                                test_text.extend([(" UV ", color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# EDGE SPLIT
# ---------------------------------------------------------------


def mod_edge_split(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_EDGESPLIT.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # EDGE ANGLE
                if mod.use_edge_angle:
                    test_text.extend([(" Edges angle ", color_setting, text_size_normal), (
                        str(round(math.degrees(mod.split_angle), 1)), color_value, text_size_normal),
                        ("°", color_value, text_size_normal)])

                # SHARP EDGES
                if mod.use_edge_sharp:
                    test_text.extend([(" Sharp Edges ", color_setting, text_size_normal)])
        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# WEIGHTED NORMALS
# ---------------------------------------------------------------


def mod_weighted_normals(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_EDGESPLIT.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # Mode
                # test_text.extend([(" Mode", color_setting, text_size_normal), (str(mod.mode.lower().capitalize()), color_setting, text_size_normal)])
                test_text.extend([(" Mode ", color_setting, text_size_normal), (str(
                    mod.mode.lower().capitalize()), color_value, text_size_normal)])

                # Weight
                test_text.extend([(" Weight ", color_setting, text_size_normal),
                                  (str(round(mod.weight, 2)), color_value, text_size_normal)])

                # STRENGTH
                test_text.extend([(" Strength ", color_setting, text_size_normal),
                                  (str(round(mod.weight, 2)), color_value, text_size_normal)])

                # THRESHOLD
                test_text.extend([(" Threshold ", color_setting, text_size_normal),
                                  (str(round(mod.thresh, 2)), color_value, text_size_normal)])

                if any([mod.keep_sharp, mod.face_influence, mod.vertex_group]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])
                    # KEEP SHARP
                    if mod.keep_sharp:
                        test_text.extend([(" Keep Sharp ", color_setting, text_size_normal)])

                    # KEEP SHARP
                    if mod.face_influence:
                        test_text.extend([(" Face Influence ", color_setting, text_size_normal)])

                    if mod.vertex_group:
                        test_text.extend([(" Vgroup ", color_setting, text_size_normal),
                                          (str(mod.vertex_group), color_value, text_size_normal)])
                    else:
                        test_text.extend([(" No Vertex Group Selected ", hidden, text_size_normal)])
        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# LATTICE
# ---------------------------------------------------------------


def mod_lattice(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_LATTICE.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                if mod.object:
                    # OBJECT
                    test_text.extend([(" Object ", color_setting, text_size_normal),
                                      (mod.object.name, color_value, text_size_normal)])
                else:
                    test_text.extend([(" No Object Selected ", hidden, text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                      (str(mod.vertex_group), color_value, text_size_normal)])

                # STRENGTH
                test_text.extend([(" Strength ", color_setting, text_size_normal),
                                  (str(round(mod.strength, 2)), color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# MASK
# ---------------------------------------------------------------


def mod_mask(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_MASK.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # ARMATURE
                if mod.mode == 'ARMATURE':
                    if mod.armature:
                        test_text.extend([(" Armature ", color_setting, text_size_normal),
                                          (str(mod.armature.name), color_value, text_size_normal)])
                    else:
                        test_text.extend([(" No Armature Selected ", hidden, text_size_normal)])

                # VERTEX GROUP
                elif mod.mode == 'VERTEX_GROUP':
                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                          (str(mod.vertex_group), color_value, text_size_normal)])
                    else:
                        test_text.extend([(" No Vertex Group Selected ", hidden, text_size_normal)])
        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# MIRROR
# ---------------------------------------------------------------


def mod_mirror(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_MIRROR.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                if any([mod.use_axis[0], mod.use_axis[1], mod.use_axis[2]]):
                    test_text.extend([(" Axis ", color_setting, text_size_normal)])
                    # X
                    if mod.use_axis[0]:
                        test_text.extend([(" X ", color_value, text_size_normal)])

                    # Y
                    if mod.use_axis[1]:
                        test_text.extend([(" Y ", color_value, text_size_normal)])

                    # Z
                    if mod.use_axis[2]:
                        test_text.extend([(" Z ", color_value, text_size_normal)])

                # OBJECT
                if mod.mirror_object:
                    test_text.extend([(" Object ", color_setting, text_size_normal),
                                      (mod.mirror_object.name, color_value, text_size_normal)])

                # MERGE
                if mod.use_mirror_merge:
                    test_text.extend([(" Merge ", color_setting, text_size_normal),
                                      (str(round(mod.merge_threshold, 3)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                # OPTIONS
                if any([mod.use_clip, mod.use_mirror_vertex_groups, mod.use_mirror_u, mod.use_mirror_v]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])
                    # CLIPPING
                    if mod.use_clip:
                        test_text.extend([(" Clipping ", color_setting, text_size_normal)])

                    # VERTEX GROUP
                    if mod.use_mirror_vertex_groups:
                        test_text.extend([(" VGroup ", color_setting, text_size_normal)])

                    # TEXTURES
                    if any([mod.use_mirror_u, mod.use_mirror_v]):
                        test_text.extend([(" Textures ", color_setting, text_size_normal)])

                    # TEXTURE U
                    if mod.use_mirror_u:
                        test_text.extend([(" U ", color_setting, text_size_normal),
                                          (str(round(mod.mirror_offset_u, 3)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                    # TEXTURE V
                    if mod.use_mirror_v:
                        test_text.extend([(" V ", color_setting, text_size_normal),
                                          (str(round(mod.mirror_offset_v, 3)), color_value, text_size_normal), (units, color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# MULTIRES
# ---------------------------------------------------------------


def mod_multires(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_MULTIRES.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])

        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # SUBDIVISION TYPE
                if mod.subdivision_type == 'SIMPLE':
                    test_text.extend([(" Simple ", color_setting, text_size_normal)])
                else:
                    test_text.extend([(" Catmull Clark ", color_setting, text_size_normal)])

                if mod.levels >= 1:
                    # LEVELS
                    test_text.extend([(" Levels ", color_setting, text_size_normal),
                                      (str(mod.levels), color_value, text_size_normal)])

                    # RENDER
                    test_text.extend([(" Render ", color_setting, text_size_normal),
                                      (str(mod.render_levels), color_value, text_size_normal)])

                    # SCULPT
                    test_text.extend([(" Sculpt ", color_setting, text_size_normal),
                                      (str(mod.sculpt_levels), color_value, text_size_normal)])

                # OPTIONS
                if any([mod.use_subsurf_uv, mod.show_only_control_edges]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # UV's
                    if mod.use_subsurf_uv:
                        test_text.extend([(" UV's ", color_setting, text_size_normal)])

                    # OPTIMAL DISPLAY
                    if mod.show_only_control_edges:
                        test_text.extend([(" Optimal Display ", color_setting, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# REMESH
# ---------------------------------------------------------------


def mod_remesh(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_REMESH.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                test_text.extend([(" ", color_title, text_size_normal), (str(mod.mode), color_value, text_size_normal)])

                # OCTREE DEPTH
                test_text.extend([(" Octree Depth ", color_setting, text_size_normal),
                                  (str(mod.octree_depth), color_value, text_size_normal)])

                # SCALE
                test_text.extend([(" Scale ", color_setting, text_size_normal),
                                  (str(round(mod.scale, 2)), color_value, text_size_normal)])

                # SHARPNESS
                if mod.mode == 'SHARP':
                    test_text.extend([(" Sharpness ", color_setting, text_size_normal),
                                      (str(round(mod.sharpness, 2)), color_value, text_size_normal)])

                # OPTIONS
                if any([mod.use_smooth_shade, mod.use_remove_disconnected]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # SMOOTH SHADING
                    if mod.use_smooth_shade:
                        test_text.extend([(" Smooth Shading ", color_setting, text_size_normal)])

                    # REMOVE DISCONNECTED
                    if mod.use_remove_disconnected:
                        test_text.extend([(" Remove Disconnected Pieces ", color_setting, text_size_normal),
                                          (str(round(mod.threshold, 2)), color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# SCREW
# ---------------------------------------------------------------


def mod_screw(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SCREW.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # AXIS
                test_text.extend([(" Axis ", color_setting, text_size_normal),
                                  (str(mod.axis), color_value, text_size_normal)])

                # AXIS OBJECT
                if mod.object:
                    test_text.extend([(" Axis Object ", color_setting, text_size_normal),
                                      (str(mod.object.name), color_value, text_size_normal)])

                # SCREW
                test_text.extend([(" Screw ", color_setting, text_size_normal),
                                  (str(round(mod.screw_offset, 2)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                # ITERATIONS
                test_text.extend([(" Iterations ", color_setting, text_size_normal),
                                  (str(round(mod.iterations, 2)), color_value, text_size_normal)])

                # Angle
                test_text.extend([(" Angle ", color_setting, text_size_normal),
                                  (str(round(math.degrees(mod.angle), 1)), color_value, text_size_normal),
                                  ("°", color_value, text_size_normal)])

                # STEPS
                test_text.extend([(" Steps ", color_setting, text_size_normal),
                                  (str(round(mod.steps, 2)), color_value, text_size_normal)])

                # OPTIONS LINE 1
                if any([mod.use_normal_flip, mod.use_smooth_shade, mod.use_object_screw_offset,
                        mod.use_normal_calculate]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # USE FLIP
                    if mod.use_normal_flip:
                        test_text.extend([(" Flip ", color_setting, text_size_normal)])

                    # USE SMOOTH SHADE
                    if mod.use_smooth_shade:
                        test_text.extend([(" Smooth Shading ", color_setting, text_size_normal)])

                    # USE OBJECT SCREW OFFSET
                    # if mod.object:
                    if mod.use_object_screw_offset:
                        test_text.extend([(" Object Screw ", color_setting, text_size_normal)])

                    # CALC ORDER
                    if mod.use_normal_calculate:
                        test_text.extend([(" Calc Order ", color_setting, text_size_normal)])

                # OPTIONS LINE 2
                if any([mod.use_merge_vertices, mod.use_stretch_u, mod.use_stretch_v]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])
                    # USE MERGE VERTICES
                    if mod.use_merge_vertices:
                        test_text.extend([(" Merge Vertices ", color_setting, text_size_normal),
                                          (str(round(mod.merge_threshold, 2)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                    # STRETCH U
                    if mod.use_stretch_u:
                        test_text.extend([(" Stretch U ", color_setting, text_size_normal)])

                    # STRETCH V
                    if mod.use_stretch_v:
                        test_text.extend([(" Stretch V ", color_setting, text_size_normal)])
        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# SKIN
# ---------------------------------------------------------------


def mod_skin(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SKIN.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # BRANCH SMOOTHING
                if mod.branch_smoothing != 0:
                    test_text.extend([(" Branch Smoothing ", color_setting, text_size_normal),
                                      (str(round(mod.branch_smoothing, 3)), color_value, text_size_normal)])

                if any([mod.use_x_symmetry, mod.use_y_symmetry, mod.use_z_symmetry]):
                    # SYMMETRY
                    test_text.extend([(" Symmetry ", color_setting, text_size_normal)])

                    # X
                    if mod.use_x_symmetry:
                        test_text.extend([(" X ", color_value, text_size_normal)])

                    # Y
                    if mod.use_y_symmetry:
                        test_text.extend([(" Y ", color_value, text_size_normal)])

                    # Z
                    if mod.use_z_symmetry:
                        test_text.extend([(" Z ", color_value, text_size_normal)])

                # OPTIONS
                if any([mod.use_smooth_shade]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # SMOOTH SHADING
                    if mod.use_smooth_shade:
                        test_text.extend([(" Smooth Shading ", color_setting, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# SOLIDIFY
# ---------------------------------------------------------------


def mod_solidify(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SOLIDIFY.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # THICKNESS
                test_text.extend([(" Thickness ", color_setting, text_size_normal),
                                  (str(round(mod.thickness, 3)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                # OFFSET
                test_text.extend([(" Offset ", color_setting, text_size_normal),
                                  (str(round(mod.offset, 2)), color_value, text_size_normal)])

                # CLAMP
                if mod.thickness_clamp != 0:
                    test_text.extend([(" Clamp ", color_setting, text_size_normal),
                                      (str(round(mod.thickness_clamp, 2)), color_value, text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                      (str(mod.vertex_group), color_value, text_size_normal)])

                    # THICKNESS VGROUP
                    test_text.extend([(" Clamp ", color_setting, text_size_normal),
                                      (str(round(mod.thickness_vertex_group, 2)), color_value, text_size_normal)])

                # OPTIONS LIGNE 1
                if any([mod.use_flip_normals, mod.use_even_offset, mod.use_quality_normals, mod.use_rim]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # FLIP NORMALS
                    if mod.use_flip_normals:
                        test_text.extend([(" Flip Normals ", color_setting, text_size_normal)])

                    # USE EVEN OFFSET
                    if mod.use_even_offset:
                        test_text.extend([(" Even Thickness ", color_setting, text_size_normal)])

                    # HIGH QUALITY NORMALS
                    if mod.use_quality_normals:
                        test_text.extend([(" High Quality Normals ", color_setting, text_size_normal)])

                    # USE RIM
                    if mod.use_rim:
                        test_text.extend([(" Fill Rim ", color_setting, text_size_normal)])

                        # ONLY RIM
                        if mod.use_rim_only:
                            test_text.extend([(" Only rims ", color_setting, text_size_normal)])

                # OPTIONS LIGNE 2
                if any([mod.edge_crease_inner, mod.edge_crease_outer, mod.edge_crease_rim]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # INNER
                    if mod.edge_crease_inner != 0:
                        test_text.extend([(" Inner ", color_setting, text_size_normal),
                                          (str(round(mod.edge_crease_inner, 2)), color_value, text_size_normal)])

                    # OUTER
                    if mod.edge_crease_outer != 0:
                        test_text.extend([(" Outer ", color_setting, text_size_normal),
                                          (str(round(mod.edge_crease_outer, 2)), color_value, text_size_normal)])

                    # RIM
                    if mod.edge_crease_rim != 0:
                        test_text.extend([(" Rim ", color_setting, text_size_normal),
                                          (str(round(mod.edge_crease_rim, 2)), color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# SUBSURF
# ---------------------------------------------------------------


def mod_subsurf(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SUBSURF.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # VIEW
                test_text.extend([(" View ", color_setting, text_size_normal),
                                  (str(mod.levels), color_value, text_size_normal)])

                # RENDER
                test_text.extend([(" Render ", color_setting, text_size_normal),
                                  (str(mod.render_levels), color_value, text_size_normal)])

                # OPTIONS
                # if any([mod.use_subsurf_uv, mod.show_only_control_edges, mod.use_opensubdiv]):
                if any([mod.use_subsurf_uv, mod.show_only_control_edges]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # UV's
                    if mod.use_subsurf_uv:
                        test_text.extend([(" UV's ", color_setting, text_size_normal)])

                    # OPTIMAL DISPLAY
                    if mod.show_only_control_edges:
                        test_text.extend([(" Optimal Display ", color_setting, text_size_normal)])

                    # OPEN SUBDIV
                    # if (hasattr(bpy.context.preferences.system, 'opensubdiv_compute_type')):
                    #     if mod.use_opensubdiv:
                    #         test_text.extend([(" Open Subdiv ", color_setting, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# TRIANGULATE
# ---------------------------------------------------------------


def mod_triangulate(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_TRIANGULATE.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # VIEW
                test_text.extend([("  ", color_setting, text_size_normal),
                                  (str(mod.quad_method.lower().capitalize()), color_value, text_size_normal)])

                # RENDER
                test_text.extend([("  ", color_setting, text_size_normal),
                                  (str(mod.ngon_method.lower().capitalize()), color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# WIREFRAME
# ---------------------------------------------------------------


def mod_wireframe(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_WIREFRAME.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # THICKNESS
                test_text.extend([(" Thickness ", color_setting, text_size_normal),
                                  (str(round(mod.thickness, 3)), color_value, text_size_normal)])

                # OFFSET
                test_text.extend([(" Offset ", color_setting, text_size_normal),
                                  (str(round(mod.offset, 2)), color_value, text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                      (str(mod.vertex_group), color_value, text_size_normal)])

                    # THICKNESS VERTEX GROUP
                    test_text.extend([(" Factor ", color_setting, text_size_normal),
                                      (str(round(mod.thickness_vertex_group, 2)), color_value, text_size_normal)])
                # CREASE WEIGHT
                if mod.use_crease:
                    test_text.extend([(" Crease Weight ", color_setting, text_size_normal),
                                      (str(round(mod.crease_weight, 2)), color_value, text_size_normal)])

                # OPTIONS
                if any([mod.use_even_offset, mod.use_relative_offset, mod.use_replace, mod.use_boundary, mod.material_offset]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # EVEN THICKNESS
                    if mod.use_even_offset:
                        test_text.extend([(" Even Thickness ", color_setting, text_size_normal)])

                    # RELATIVE THICKNESS
                    if mod.use_relative_offset:
                        test_text.extend([(" Relative Thickness ", color_setting, text_size_normal)])

                    # BOUNDARY
                    if mod.use_boundary:
                        test_text.extend([(" Boundary ", color_setting, text_size_normal)])

                    # REPLACE ORIGINAL
                    if mod.use_replace:
                        test_text.extend([(" Replace Original ", color_setting, text_size_normal)])

                    # MATERIAL OFFSET
                    if mod.material_offset:
                        test_text.extend([(" Material Offset ", color_setting, text_size_normal),
                                          (str(mod.material_offset), color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ----------------------------------------------------------------------------------------------------------------------
# MODIFIERS DEFORM -----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------
# ARMATURE
# ---------------------------------------------------------------


def mod_armature(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_ARMATURE.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                if mod.object:
                    # START
                    test_text.extend([(" Object ", color_setting, text_size_normal),
                                      (str(mod.object.name), color_value, text_size_normal)])
                else:
                    test_text.extend([(" No Armature Selected ", hidden, text_size_normal)])

                # VERTEX GROUP
                if mod.use_vertex_groups:
                    test_text.extend([(" VGroup ", color_setting, text_size_normal)])
                    if mod.vertex_group:
                        test_text.extend([(str(mod.vertex_group), color_value, text_size_normal)])
                    else:
                        test_text.extend([(" No Vertex Group Selected ", hidden, text_size_normal)])

                # OPTIONS
                if any([mod.use_deform_preserve_volume, mod.use_bone_envelopes, mod.use_multi_modifier]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # PRESERVE VOLUME
                    if mod.use_deform_preserve_volume:

                        test_text.extend([(" Preserve Volume ", color_setting, text_size_normal)])

                    # BONE ENVELOPES
                    if mod.use_bone_envelopes:
                        test_text.extend([(" Bone Enveloppes ", color_setting, text_size_normal)])

                    # MULTI MODIFIER
                    if mod.use_multi_modifier:
                        test_text.extend([(" Multi Modifier ", color_setting, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# CAST
# ---------------------------------------------------------------


def mod_cast(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_CAST.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # CAST TYPE
                test_text.extend([(" Type ", color_setting, text_size_normal), (str(
                    mod.cast_type.lower().capitalize()), color_value, text_size_normal)])

                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    test_text.extend([(" Axis ", color_setting, text_size_normal)])

                    if mod.use_x:
                        test_text.extend([(" X ", color_value, text_size_normal)])

                    if mod.use_y:
                        test_text.extend([(" Y ", color_value, text_size_normal)])

                    if mod.use_z:
                        test_text.extend([(" Z ", color_value, text_size_normal)])

                else:
                    test_text.extend([(" No Axis Selected ", hidden, text_size_normal)])

                # FACTOR
                test_text.extend([(" Factor ", color_setting, text_size_normal),
                                  (str(round(mod.factor, 2)), color_value, text_size_normal)])

                # RADIUS
                if mod.radius != 0:
                    test_text.extend([(" Radius ", color_setting, text_size_normal),
                                      (str(round(mod.radius, 2)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                # SIZE
                if mod.size != 0:
                    test_text.extend([(" Size ", color_setting, text_size_normal),
                                      (str(round(mod.size, 2)), color_value, text_size_normal)])

                # OPTIONS
                if any([mod.use_radius_as_size, mod.vertex_group, mod.object, mod.use_transform]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                          (mod.vertex_group, color_value, text_size_normal)])

                    # FROM RADIUS
                    if mod.use_radius_as_size:
                        test_text.extend([(" From Radius ", color_setting, text_size_normal)])

                    # OBJECT
                    if mod.object:
                        test_text.extend([(" Control Object ", color_setting, text_size_normal),
                                          (mod.object.name, color_value, text_size_normal)])

                    # USE TRANSFORM
                    if mod.use_transform:
                        test_text.extend([(" Use Transform ", color_setting, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# CORRECTIVE SMOOTH
# ---------------------------------------------------------------


def mod_corrective_smooth(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # FACTOR
                test_text.extend([(" Factor ", color_setting, text_size_normal),
                                  (str(round(mod.factor, 2)), color_value, text_size_normal)])

                # ITERATIONS
                test_text.extend([(" Repeat ", color_setting, text_size_normal),
                                  (str(mod.iterations), color_value, text_size_normal)])

                # SMOOTH TYPE
                test_text.extend([(" Smooth Type ", color_setting, text_size_normal), (str(
                    mod.smooth_type.lower().capitalize()), color_setting, text_size_normal)])

                # OPTIONS
                if any([mod.use_only_smooth, mod.vertex_group, mod.use_pin_boundary, mod.rest_source]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                          (mod.vertex_group, color_value, text_size_normal)])

                    # ONLY SMOOTH
                    if mod.use_only_smooth:
                        test_text.extend([(" Only Smooth ", color_setting, text_size_normal)])

                    # PIN BOUNDARIES
                    if mod.use_pin_boundary:
                        test_text.extend([(" Pin Boundaries ", color_setting, text_size_normal)])

                    # OBJECT
                    test_text.extend([(" Rest Sources ", color_setting, text_size_normal),
                                      (mod.rest_source.lower().capitalize(), color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# CURVE
# ---------------------------------------------------------------


def mod_curve(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_CURVE.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # OBJECT
                if mod.object:
                    test_text.extend([(" Object ", color_setting, text_size_normal),
                                      (mod.object.name, color_value, text_size_normal)])
                else:
                    test_text.extend([(" No Object Selected ", hidden, text_size_normal)])

                # DEFORM AXIS
                test_text.extend([(" Deformation Axis ", color_setting, text_size_normal)])
                if mod.deform_axis == 'POS_X':
                    test_text.extend([(" X ", color_value, text_size_normal)])

                elif mod.deform_axis == 'POS_Y':
                    test_text.extend([(" Y ", color_value, text_size_normal)])

                elif mod.deform_axis == 'POS_Z':
                    test_text.extend([(" Z ", color_value, text_size_normal)])

                elif mod.deform_axis == 'NEG_X':
                    test_text.extend([(" -X ", color_value, text_size_normal)])

                elif mod.deform_axis == 'NEG_Y':
                    test_text.extend([(" -Y ", color_value, text_size_normal)])

                elif mod.deform_axis == 'NEG_Z':
                    test_text.extend([(" -Z ", color_value, text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([CR, ("----", color_title, text_size_normal)])
                    test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                      (str(mod.vertex_group), color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# DISPLACE
# ---------------------------------------------------------------


def mod_displace(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_DISPLACE.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # MID LEVEL
                test_text.extend([(" Mid Level ", color_setting, text_size_normal),
                                  (str(round(mod.mid_level, 2)), color_value, text_size_normal)])

                # STRENGTH
                test_text.extend([(" Strength ", color_setting, text_size_normal),
                                  (str(round(mod.strength, 2)), color_value, text_size_normal)])

                # DIRECTION
                test_text.extend([(" Direction ", color_setting, text_size_normal), (str(
                    mod.direction.lower().capitalize()), color_value, text_size_normal)])
                if mod.direction in ['RGB_TO_XYZ', 'X', 'Y', 'Z']:
                    # DIRECTION
                    test_text.extend([(" Space ", color_setting, text_size_normal), (str(
                        mod.space.lower().capitalize()), color_value, text_size_normal)])

                # # OPTIONS
                # if any([mod.vertex_group]):
                #     test_text.extend([CR, ("----", color_title, text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([CR, ("----", color_title, text_size_normal)])
                    test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                      (str(mod.vertex_group), color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# HOOK
# ---------------------------------------------------------------


def mod_hook(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_HOOK.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # OBJECT
                if mod.object:
                    test_text.extend([(" Object ", color_setting, text_size_normal),
                                      (mod.object.name, color_value, text_size_normal)])
                else:
                    test_text.extend([(" No Object Selected ", hidden, text_size_normal)])

                # RADIUS
                if mod.falloff_type != 'NONE':
                    if mod.falloff_radius != 0:
                        test_text.extend([(" Radius ", color_setting, text_size_normal),
                                          (str(round(mod.falloff_radius, 2)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                # STRENGTH
                test_text.extend([(" Strength ", color_setting, text_size_normal),
                                  (str(round(mod.strength, 2)), color_value, text_size_normal)])

                # OPTIONS
                test_text.extend([CR, ("----", color_title, text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                      (mod.vertex_group, color_value, text_size_normal)])

                # FALLOF TYPE
                test_text.extend([(" Fallof Type ", color_setting, text_size_normal),
                                  (str(mod.falloff_type.upper()), color_value, text_size_normal)])

                # UNIFORM FALLOFF
                if mod.use_falloff_uniform:
                    test_text.extend([(" Uniform Falloff ", color_setting, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# LAPLACIAN DEFORMER
# ---------------------------------------------------------------


def mod_laplacian_deformer(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # ITERATIONS
                test_text.extend([(" Repeat ", color_setting, text_size_normal),
                                  (str(mod.iterations), color_value, text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                      (str(mod.vertex_group), color_value, text_size_normal)])
                else:
                    test_text.extend([(" No VGroup Selected ", hidden, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# LAPLACIAN SMOOTH
# ---------------------------------------------------------------


def mod_laplacian_smooth(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    test_text.extend([(" Axis ", color_setting, text_size_normal)])

                    if mod.use_x:
                        test_text.extend([(" X ", color_value, text_size_normal)])

                    if mod.use_y:
                        test_text.extend([(" Y ", color_value, text_size_normal)])

                    if mod.use_z:
                        test_text.extend([(" Z ", color_value, text_size_normal)])
                else:
                    test_text.extend([(" No Axis Selected ", hidden, text_size_normal)])

                # FACTOR
                test_text.extend([(" Factor ", color_setting, text_size_normal),
                                  (str(round(mod.lambda_factor, 2)), color_value, text_size_normal)])

                # BORDER
                test_text.extend([(" Border ", color_setting, text_size_normal),
                                  (str(round(mod.lambda_border, 2)), color_value, text_size_normal)])

                # OPTIONS
                if any([mod.use_volume_preserve, mod.use_normalized, mod.vertex_group]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # PRESERVE VOLUME
                    if mod.use_volume_preserve:
                        test_text.extend([(" Preserve Volume ", color_setting, text_size_normal)])

                    # NORMALIZED
                    if mod.use_normalized:
                        test_text.extend([(" Normalized ", color_setting, text_size_normal)])

                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                          (mod.vertex_group, color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# MESH DEFORM
# ---------------------------------------------------------------


def mod_mesh_deform(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # OBJECT
                if mod.object:
                    test_text.extend([(" Object ", color_setting, text_size_normal),
                                      (mod.object.name, color_value, text_size_normal)])
                else:
                    test_text.extend([(" No Object Selected ", hidden, text_size_normal)])

                # PRECISION
                test_text.extend([(" Precision ", color_setting, text_size_normal),
                                  (str(mod.precision), color_value, text_size_normal)])

                # OPTIONS
                if any([mod.use_dynamic_bind, mod.vertex_group]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                          (str(mod.vertex_group), color_value, text_size_normal)])

                    # USE DYNAMIC BIND
                    if mod.use_dynamic_bind:
                        test_text.extend([(" Dynamic ", color_setting, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# SIMPLE DEFORM
# ---------------------------------------------------------------


def mod_simple_deform(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SIMPLEDEFORM.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:

                test_text.extend([(" ", color_setting, text_size_normal),
                                  (str(mod.deform_method.upper()), color_value, text_size_normal)])

                # ORIGIN
                if mod.origin:
                    test_text.extend([(" Axis,Origin ", color_setting, text_size_normal),
                                      (str(mod.origin.name), color_value, text_size_normal)])

                # ANGLE/FACTOR
                if mod.deform_method in ['TWIST', 'BEND']:
                    # Angle
                    test_text.extend([(" Angle ", color_setting, text_size_normal),
                                      (str(round(math.degrees(mod.factor), 1)), color_value, text_size_normal),
                                      ("°", color_value, text_size_normal)])

                elif mod.deform_method in ['TAPER', 'STRETCH']:
                    test_text.extend([(" Factor ", color_setting, text_size_normal),
                                      (str(round(mod.factor, 2)), color_value, text_size_normal)])

                # OPTIONS
                test_text.extend([CR, ("----", color_title, text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                      (str(mod.vertex_group), color_value, text_size_normal)])

                # LOCK
                if mod.deform_method != 'BEND':
                    if any([mod.lock_x, mod.lock_y]):
                        test_text.extend([(" Lock ", color_setting, text_size_normal)])

                        if mod.lock_x:
                            test_text.extend([(" X ", color_value, text_size_normal)])

                        if mod.lock_y:
                            test_text.extend([(" Y ", color_value, text_size_normal)])

                # LIMIT
                test_text.extend([(" Limit ", color_setting, text_size_normal)])

                test_text.extend([(str(round(mod.limits[0], 2)), color_value, text_size_normal)])

                test_text.extend([(" ", color_setting, text_size_normal),
                                  (str(round(mod.limits[1], 2)), color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# SHRINKWRAP
# ---------------------------------------------------------------


def mod_shrinkwrap(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SHRINKWRAP.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])

        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # TARGET
                if mod.target:
                    test_text.extend([(" Target ", color_setting, text_size_normal),
                                      (str(mod.target.name), color_value, text_size_normal)])
                else:
                    test_text.extend([(" No Target Selected ", hidden, text_size_normal)])

                # OFFSET
                test_text.extend([(" Offset ", color_setting, text_size_normal),
                                  (str(round(mod.offset, 2)), color_value, text_size_normal)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                      (str(mod.vertex_group), color_value, text_size_normal)])

                test_text.extend([CR, ("----", color_title, text_size_normal)])

                # NEAREST SURFACEPOINT
                if mod.wrap_method == 'NEAREST_SURFACEPOINT':
                    # MODE
                    test_text.extend([(" Mode ", color_setting, text_size_normal),
                                      (str(mod.wrap_method.lower().capitalize()), color_value, text_size_normal)])

                    # KEEP ABOVE SURFACE
                    if mod.use_keep_above_surface:
                        test_text.extend([(" Keep Above Surface ", color_setting, text_size_normal)])

                # PROJECT
                elif mod.wrap_method == 'PROJECT':
                    # MODE
                    test_text.extend([(" Mode ", color_setting, text_size_normal),
                                      (str(mod.wrap_method.lower().capitalize()), color_value, text_size_normal)])

                    # AXIS
                    if any([mod.use_project_x, mod.use_project_y, mod.use_project_z]):
                        test_text.extend([(" Axis ", color_setting, text_size_normal)])
                        # X
                        if mod.use_project_x:
                            test_text.extend([(" X ", color_value, text_size_normal)])
                        # Y
                        if mod.use_project_y:
                            test_text.extend([(" Y ", color_value, text_size_normal)])
                        # Z
                        if mod.use_project_z:
                            test_text.extend([(" Z ", color_value, text_size_normal)])

                    # LEVELS
                    test_text.extend([(" Subsurf Levels ", color_setting, text_size_normal),
                                      (str(mod.subsurf_levels), color_value, text_size_normal)])

                    # PROJECT LIMIT
                    test_text.extend([(" Limit ", color_setting, text_size_normal),
                                      (str(round(mod.project_limit, 2)), color_value, text_size_normal)])

                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # DIRECTION
                    if mod.use_negative_direction:
                        test_text.extend([(" Negative ", color_setting, text_size_normal)])

                    if mod.use_positive_direction:
                        test_text.extend([(" Positive ", color_setting, text_size_normal)])

                    # MODE
                    test_text.extend([(" Cull Face ", color_setting, text_size_normal),
                                      (str(mod.cull_face.lower().capitalize()), color_value, text_size_normal)])
                    # AUXILIARY TARGET
                    if mod.auxiliary_target:
                        test_text.extend([(" Auxiliary Target ", color_setting, text_size_normal),
                                          (mod.auxiliary_target.name, color_value, text_size_normal)])
                else:
                    # MODE
                    test_text.extend([(" Mode ", color_setting, text_size_normal),
                                      (str(mod.wrap_method.lower().capitalize()), color_value, text_size_normal)])
        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# SMOOTH
# ---------------------------------------------------------------


def mod_smooth(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    test_text.extend([(" Axis ", color_setting, text_size_normal)])

                    if mod.use_x:
                        test_text.extend([(" X ", color_value, text_size_normal)])

                    if mod.use_y:
                        test_text.extend([(" Y ", color_value, text_size_normal)])

                    if mod.use_z:
                        test_text.extend([(" Z ", color_value, text_size_normal)])
                else:
                    test_text.extend([(" No Axis Selected ", hidden, text_size_normal)])

                # FACTOR
                test_text.extend([(" Factor ", color_setting, text_size_normal),
                                  (str(round(mod.factor, 2)), color_value, text_size_normal)])

                # ITERATIONS
                test_text.extend([(" Repeat ", color_setting, text_size_normal),
                                  (str(mod.iterations), color_value, text_size_normal)])

                # OPTIONS
                if mod.vertex_group:
                    test_text.extend([CR, ("----", color_title, text_size_normal)])
                    test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                      (mod.vertex_group, color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# SURFACE DEFORM
# ---------------------------------------------------------------


def mod_surface_deform(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # TARGET
                if mod.target:
                    test_text.extend([(" Target ", color_setting, text_size_normal),
                                      (str(mod.target.name), color_value, text_size_normal)])
                else:
                    test_text.extend([(" No Target Selected ", hidden, text_size_normal)])

                # FALLOFF
                test_text.extend([(" Interpolation Falloff ", color_setting, text_size_normal),
                                  (str(round(mod.falloff, 2)), color_value, text_size_normal)])
        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# WARP
# ---------------------------------------------------------------


def mod_warp(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_WARP.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                # FROM
                if mod.object_from:
                    test_text.extend([(" From ", color_setting, text_size_normal),
                                      (str(mod.object_from.name), color_value, text_size_normal)])

                else:
                    test_text.extend([(" No Object From ", hidden, text_size_normal)])

                # TO
                if mod.object_to:
                    test_text.extend([(" To ", color_setting, text_size_normal),
                                      (str(mod.object_to.name), color_value, text_size_normal)])
                else:
                    test_text.extend([(" No Object To ", hidden, text_size_normal)])

                # STRENGTH
                test_text.extend([(" Strength ", color_setting, text_size_normal),
                                  (str(round(mod.strength, 2)), color_value, text_size_normal)])

                # RADIUS
                if mod.falloff_type != 'NONE':
                    if mod.falloff_radius != 0:
                        test_text.extend([(" Radius ", color_setting, text_size_normal),
                                          (str(round(mod.falloff_radius, 2)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                # OPTIONS
                if any([mod.vertex_group, mod.use_volume_preserve, mod.texture_coords]):
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                          (str(mod.vertex_group), color_value, text_size_normal)])

                    # OFFSET
                    if mod.use_volume_preserve:
                        test_text.extend([(" Preserve Volume ", color_setting, text_size_normal)])

                    # TEXTURES COORD
                    test_text.extend([(" Texture Coords ", color_setting, text_size_normal),
                                      (str(mod.texture_coords.lower().capitalize()), color_value, text_size_normal)])

                    # OBJECT
                    if mod.texture_coords == "OBJECT":
                        if mod.texture_coords_object:
                            test_text.extend([(" Object ", color_setting, text_size_normal),
                                              (str(mod.texture_coords_object.name), color_value, text_size_normal)])
                        else:
                            test_text.extend([(" No Object Selected ", hidden, text_size_normal)])

                    # UVs
                    if mod.texture_coords == "UV":
                        if mod.uv_layer:
                            test_text.extend([(" UVMap ", color_setting, text_size_normal),
                                              (str(mod.uv_layer), color_value, text_size_normal)])
                        else:
                            test_text.extend([(" No UV's Selected ", hidden, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ---------------------------------------------------------------
# WAVE
# ---------------------------------------------------------------


def mod_wave(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_WAVE.png'), ("    ", color_setting, text_size_normal),
        #                   (str(mod.name.upper()), color_title, text_size_normal)])
        test_text.extend([CR, (str(mod.name.upper()), color_title, text_size_normal)])

        if mod.show_viewport:
            if not simple_text_mode:
                if any([mod.use_x, mod.use_y, mod.use_cyclic]):
                    test_text.extend([(" Motion ", color_setting, text_size_normal)])

                    if mod.use_x:
                        test_text.extend([(" X ", color_value, text_size_normal)])

                    if mod.use_y:
                        test_text.extend([(" Y ", color_value, text_size_normal)])

                    if mod.use_cyclic:
                        test_text.extend([(" Cyclic ", color_value, text_size_normal)])

                if mod.use_normal:
                    if any([mod.use_normal_x, mod.use_normal_y, mod.use_normal_z]):
                        test_text.extend([(" Normals ", color_setting, text_size_normal)])

                        if mod.use_normal_x:
                            test_text.extend([(" X ", color_value, text_size_normal)])

                        if mod.use_normal_y:
                            test_text.extend([(" Y ", color_value, text_size_normal)])

                        if mod.use_normal_z:
                            test_text.extend([(" Z ", color_value, text_size_normal)])

                # TIME
                test_text.extend([(" Time ", color_setting, text_size_normal)])

                # OFFSET
                test_text.extend([(" Offset ", color_setting, text_size_normal),
                                  (str(round(mod.time_offset, 2)), color_value, text_size_normal)])
                # LIFE
                test_text.extend([(" Life ", color_setting, text_size_normal),
                                  (str(round(mod.lifetime, 2)), color_value, text_size_normal)])
                # DAMPING
                test_text.extend([(" Damping ", color_setting, text_size_normal),
                                  (str(round(mod.damping_time, 2)), color_value, text_size_normal)])

                if any([mod.start_position_x, mod.start_position_y, mod.falloff_radius]) != 0:
                    test_text.extend([CR, ("----", color_title, text_size_normal)])
                    # TIME
                    test_text.extend([(" Position ", color_setting, text_size_normal)])

                    # POS X
                    test_text.extend([(" X ", color_setting, text_size_normal),
                                      (str(round(mod.start_position_x, 2)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                    # POS Y
                    test_text.extend([(" Y ", color_setting, text_size_normal),
                                      (str(round(mod.start_position_y, 2)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                    # FALLOFF
                    test_text.extend([(" Y ", color_setting, text_size_normal),
                                      (str(round(mod.falloff_radius, 2)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                if any([mod.start_position_object, mod.vertex_group, mod.texture_coords]) != 0:
                    test_text.extend([CR, ("----", color_title, text_size_normal)])

                    # FROM
                    if mod.start_position_object:
                        test_text.extend([(" From ", color_setting, text_size_normal),
                                          (str(mod.start_position_object.name), color_value, text_size_normal)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", color_setting, text_size_normal),
                                          (str(mod.vertex_group), color_value, text_size_normal)])

                    # TEXTURES COORD
                    test_text.extend([(" Texture Coords ", color_setting, text_size_normal),
                                      (str(mod.texture_coords.lower().capitalize()), color_value, text_size_normal)])

                    # OBJECT
                    if mod.texture_coords == "OBJECT":
                        if mod.texture_coords_object:
                            test_text.extend([(" Object ", color_setting, text_size_normal),
                                              (str(mod.texture_coords_object.name), color_value, text_size_normal)])
                        else:
                            test_text.extend([(" No Object Selected ", hidden, text_size_normal)])

                    # UVs
                    if mod.texture_coords == "UV":
                        if mod.uv_layer:
                            test_text.extend([(" UVMap ", color_setting, text_size_normal),
                                              (str(mod.uv_layer), color_value, text_size_normal)])
                        else:
                            test_text.extend([(" No UV's Selected ", hidden, text_size_normal)])

                test_text.extend([CR, ("----", color_title, text_size_normal)])

                # SPEED
                test_text.extend([(" Speed ", color_setting, text_size_normal),
                                  (str(round(mod.speed, 2)), color_value, text_size_normal)])

                # SPEED
                test_text.extend([(" Height ", color_setting, text_size_normal),
                                  (str(round(mod.height, 2)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                # SPEED
                test_text.extend([(" Width ", color_setting, text_size_normal),
                                  (str(round(mod.width, 2)), color_value, text_size_normal), (units, color_value, text_size_normal)])

                # SPEED
                test_text.extend([(" Narrowness ", color_setting, text_size_normal),
                                  (str(round(mod.narrowness, 2)), color_value, text_size_normal), (units, color_value, text_size_normal)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size_normal)])

# ----------------------------------------------------------------------------------------------------------------------
# OBJECTS --------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------
# ARMATURE
# ---------------------------------------------------------------


def armature(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space):
    obj = bpy.context.active_object
    active_bone = bpy.context.active_bone

    # BONE SELECTED
    if bpy.context.object.mode in {'POSE', 'EDIT'}:
        test_text.extend([CR, ("BONE SELECTED ", color_title, text_size_normal),
                          (active_bone.name, color_value, text_size_normal)])

# ---------------------------------------------------------------
# CAMERA
# ---------------------------------------------------------------


def camera(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space):
    obj = bpy.context.active_object

    # LENS
    test_text.extend([CR, ("LENS ", color_title, text_size_normal),
                      (str(round(obj.data.lens, 2)), color_value, text_size_normal)])
    # FOCUS
    if bpy.context.object.data.dof.use_dof and bpy.context.object.data.dof.focus_object:

        test_text.extend([CR, ("FOCUS ", color_title, text_size_normal),
                          (str(obj.dof.focus_object.name), color_value, text_size_normal)])

    else:
        test_text.extend([CR, ("DISTANCE ", color_title, text_size_normal),
                          (str(round(obj.data.dof.focus_distance, 2)), color_value, text_size_normal)])

    # RADIUS / FSTOP
    # if bpy.context.object.data.cycles.aperture_type == 'RADIUS': bpy.context.object.data.dof.focus_object = None
    #     if obj.data.cycles.aperture_size:
    #         test_text.extend([CR, ("RADIUS ", color_title, text_size_normal),
    #                       (str(round(obj.data.cycles.aperture_size, 2)), color_value,
    #                        text_size_normal)])

    if bpy.context.object.data.dof.use_dof:

        test_text.extend([CR, ("FSTOP ", color_title, text_size_normal),
                          (str(round(obj.data.cycles.aperture_fstop, 2)), color_value,
                           text_size_normal)])

# ---------------------------------------------------------------
# CURVE / FONT
# ---------------------------------------------------------------


def curve_font(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space):
    obj = bpy.context.active_object

    # PREVIEW U
    test_text.extend([CR, ("Preview U ", color_title, text_size_normal),
                      (str(obj.data.resolution_u), color_value, text_size_normal)])

    # RENDER PREVIEW U
    test_text.extend([(" Render U ", color_title, text_size_normal),
                      (str(obj.data.render_resolution_u), color_value, text_size_normal)])

    # FILL MODE
    test_text.extend([CR, ("FILL ", color_title, text_size_normal), (str(
        obj.data.fill_mode.lower().capitalize()), color_value, text_size_normal)])

    # OFFSET
    if obj.data.offset:
        test_text.extend(
            [CR, ("Offset ", color_title, text_size_normal), (str(round(obj.data.offset, 2)), color_value, text_size_normal)])

    # DEPTH
    if obj.data.bevel_depth:
        test_text.extend([CR, ("DEPTH ", color_title, text_size_normal),
                          (str(round(obj.data.bevel_depth, 2)), color_value, text_size_normal)])

    # EXTRUDE
    if obj.data.extrude:
        test_text.extend([CR, ("EXTRUDE ", color_title, text_size_normal),
                          (str(round(obj.data.extrude, 2)), color_value, text_size_normal)])

    # RESOLUTION
    if obj.data.bevel_resolution:
        test_text.extend([CR, ("RESOLUTION ", color_title, text_size_normal),
                          (str(obj.data.bevel_resolution), color_value, text_size_normal)])
    # BEVEL
    if obj.data.bevel_object:
        test_text.extend([CR, ("BEVEL ", color_title, text_size_normal),
                          (obj.data.bevel_object.name, color_value, text_size_normal)])

    # TAPER
    if obj.data.taper_object:
        test_text.extend([CR, ("TAPER ", color_title, text_size_normal),
                          (obj.data.taper_object.name, color_value, text_size_normal)])

# ---------------------------------------------------------------
# EMPTY
# ---------------------------------------------------------------


def empty(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space):
    obj = bpy.context.active_object

    # ICON_OUTLINER_OB_EMPTY
    # TYPE
    test_text.extend([("TYPE ", color_title, text_size_normal),
                      (str(obj.empty_display_type.lower().capitalize()), color_value, text_size_normal)])

    # SIZE
    test_text.extend([CR, ("SIZE ", color_title, text_size_normal),
                      (str(round(obj.empty_display_size, 2)), color_value, text_size_normal)])

# ---------------------------------------------------------------
# LATTICE
# ---------------------------------------------------------------


def text_lattice(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space):
    obj = bpy.context.active_object

# U -----------------------------------------------------------------------
    test_text.extend([CR, ("U  ", color_title, text_size_normal),
                      (str(obj.data.points_u), color_value, text_size_normal)])

    # INTERPOLATION U
    test_text.extend([("  ", color_title, text_size_normal),
                      (str(obj.data.interpolation_type_u.split("_")[-1]), color_setting, text_size_normal)])

# V -----------------------------------------------------------------------
    test_text.extend([CR, ("V  ", color_title, text_size_normal),
                      (str(obj.data.points_v), color_value, text_size_normal)])

    # INTERPOLATION V
    test_text.extend([("  ", color_title, text_size_normal), (
        str(obj.data.interpolation_type_v.split("_")[-1]), color_setting, text_size_normal)])

# W -----------------------------------------------------------------------
    test_text.extend([CR, ("W ", color_title, text_size_normal),
                      (str(obj.data.points_w), color_value,
                       text_size_normal)])

    # INTERPOLATION W
    test_text.extend([("  ", color_title, text_size_normal), (
        str(obj.data.interpolation_type_w.split("_")[-1]), color_setting, text_size_normal)])

# ---------------------------------------------------------------
# LIGHTS
# ---------------------------------------------------------------


def cycles_lights(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space):
    obj = bpy.context.active_object

    # TYPE
    if obj.data.type == 'AREA':
        test_text.extend([CR, ("TYPE: ", color_title, text_size_normal), ("AREA ", color_setting, text_size_normal)])

        # SQUARE
        if obj.data.shape == 'SQUARE':
            test_text.extend([CR, ("SQUARE ", color_title, text_size_normal)])
            test_text.extend([CR, ("SIZE ", color_title, text_size_normal),
                              (str(round(obj.data.size, 2)), color_value, text_size_normal)])
        # RECTANGLE
        elif obj.data.shape == 'RECTANGLE':
            # RECTANGLE
            test_text.extend([CR, ("RECTANGLE ", color_title, text_size_normal)])
            # SIZE
            test_text.extend([CR, ("SIZE X ", color_title, text_size_normal),
                              (str(round(obj.data.size, 2)), color_value, text_size_normal)])
            # SIZE Y
            test_text.extend([CR, ("SIZE Y ", color_title, text_size_normal),
                              (str(round(obj.data.size_y, 2)), color_value, text_size_normal)])

    # POINT
    elif obj.data.type == 'POINT':
        test_text.extend([CR, ("TYPE: ", color_title, text_size_normal), ("POINT ", color_setting, text_size_normal)])

        # SIZE
        test_text.extend([CR, ("SIZE ", color_title, text_size_normal),
                          (str(round(obj.data.shadow_soft_size, 2)), color_value, text_size_normal)])

    # SUN
    elif obj.data.type == 'SUN':
        test_text.extend([CR, ("TYPE: ", color_title, text_size_normal), ("SUN ", color_setting, text_size_normal)])

        # SIZE
        test_text.extend([CR, ("SIZE ", color_title, text_size_normal),
                          (str(round(obj.data.shadow_soft_size, 2)), color_value, text_size_normal)])

    elif obj.data.type == 'SPOT':
        test_text.extend([CR, ("TYPE: ", color_title, text_size_normal), ("SPOT ", color_setting, text_size_normal)])
        # SIZE
        test_text.extend([CR, ("SIZE ", color_title, text_size_normal),
                          (str(round(obj.data.shadow_soft_size, 2)), color_value, text_size_normal)])
        # SHAPE
        test_text.extend([CR, ("SHAPE ", color_title, text_size_normal), (
            str(round(math.degrees(obj.data.spot_size), 1)), color_value, text_size_normal),
            ("°", color_value, text_size_normal)])
        # BLEND
        test_text.extend([CR, ("SIZE ", color_title, text_size_normal),
                          (str(round(obj.data.spot_blend, 2)), color_value, text_size_normal)])

    # HEMI
    elif obj.data.type == 'HEMI':
        test_text.extend([CR, ("TYPE: ", color_title, text_size_normal), ("HEMI ", color_setting, text_size_normal)])
        # test_text.extend([("HEMI ", color_title, text_size_normal),
        #                   (str(round(bpy.data.node_groups["Shader Nodetree"].nodes["Emission"].inputs[1].default_value, 2)), color_value, text_size_normal)])

    # PORTAL
    if obj.data.cycles.is_portal:
        test_text.extend([CR, ("PORTAL", color_title, text_size_normal)])

    else:
        # CAST SHADOW
        if obj.data.cycles.cast_shadow:
            test_text.extend([CR, ("CAST SHADOW ", color_setting, text_size_normal)])
        # MULTIPLE IMPORTANCE
        if obj.data.cycles.use_multiple_importance_sampling:
            test_text.extend([CR, ("MULTIPLE IMPORTANCE", color_setting, text_size_normal)])

# ---------------------------------------------------------------
# METABALL
# ---------------------------------------------------------------


def metaball(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space):
    obj = bpy.context.active_object

    # VIEW
    test_text.extend([CR, ("VIEW ", color_title, text_size_normal),
                      (str(round(obj.data.resolution, 2)), color_value, text_size_normal)])

    # RENDER
    test_text.extend([CR, ("RENDER ", color_title, text_size_normal),
                      (str(round(obj.data.render_resolution, 2)), color_value, text_size_normal)])

    # THRESHOLD
    test_text.extend([CR, ("THRESHOLD ", color_title, text_size_normal),
                      (str(round(obj.data.threshold, 2)), color_value, text_size_normal)])

    # UPDATE
    test_text.extend([CR, ("UPDATE ", color_title, text_size_normal),
                      (obj.data.update_method.split("_")[-1], color_value, text_size_normal)])


# ---------------------------------------------------------------
# WARNING
# ---------------------------------------------------------------
def warning(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space):
    obj = bpy.context.active_object

    for mod in bpy.context.active_object.modifiers:
        if mod.type in ['BEVEL', 'SOLIDIFY']:
            if obj.scale[0] != obj.scale[2] or obj.scale[1] != obj.scale[0] or obj.scale[1] != obj.scale[2]:
                # test_text.extend(
                #     [CR,('ICON', 'ICON_ERROR.png'),("      Non-Uniform Scale will give bad results ", color_setting, text_size_normal)])
                test_text.extend(
                    [CR, ("      Non-Uniform Scale will give bad results ", color_setting, text_size_normal)])


# ----------------------------------------------------------------------------------------------------------------------
# TEXTS
# ----------------------------------------------------------------------------------------------------------------------
def infotext_key_text():
    units = ""

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

    obj = bpy.context.active_object
    wm = bpy.context.window_manager

    test_text = []
    # SHOW TEXT
    show_object_mode = get_addon_preferences().show_object_mode
    show_vert_face_tris = get_addon_preferences().show_vert_face_tris
    show_object_name = get_addon_preferences().show_object_name
    show_loc_rot_scale = get_addon_preferences().show_loc_rot_scale
    show_modifiers = get_addon_preferences().show_modifiers
    show_object_info = get_addon_preferences().show_object_info
    simple_text_mode = get_addon_preferences().simple_text_mode
    # show_keymaps = get_addon_preferences().show_keymaps
    show_blender_keymaps = get_addon_preferences().show_blender_keymaps

    # TEXT OPTIONS
    hidden = get_addon_preferences().hidden
    color_title = get_addon_preferences().text_color
    color_setting = get_addon_preferences().text_color_1
    option = get_addon_preferences().option
    color_value = get_addon_preferences().text_color_2
    text_size_max = get_addon_preferences().text_size_max
    text_size_mini = get_addon_preferences().text_size_mini

    # FIXME: Make sure the math here is sensical
    text_size_normal = min(text_size_max, max(text_size_mini, int(bpy.context.area.width / 100)))
    text_size_large = int(text_size_max * 1.5)
    space = int(text_size_normal * 2)
    CR = "Carriage return"

    # HELP
    # if show_keymaps:
    #     keymaps(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, space)

    obj = bpy.context.object
    if obj is None:
        test_text.extend([("SELECTION", color_title, "Active object not found")])
        return test_text

    # MODE
    if show_object_mode:
        mode(test_text, CR, color_title, color_setting, color_value,
             text_size_normal, hidden, option, text_size_large, space)
        # SPACE
        test_text.extend([("SPACE", color_title, space)])

    # NAME
    if show_object_name:
        name(test_text, CR, color_title, color_setting, color_value,
             text_size_normal, hidden, option, text_size_large, space)
        # SPACE
        test_text.extend([("SPACE", color_title, space)])

    # LOCATION / ROTATION / SCALE
    if show_loc_rot_scale:
        loc(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space)

    # VERT/FACES/EDGES/NGONS
    if show_vert_face_tris:
        if obj.type == 'MESH':
            ngons(test_text, CR, color_title, color_value, text_size_normal, space)
            # SPACE
            test_text.extend([("SPACE", color_title, space)])

    # MESH OPTIONS
    if show_object_info:
        # if bpy.context.object.mode in ['EDIT', 'OBJECT', 'WEIGHT_PAINT']:
        if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
            mesh_options(test_text, CR, color_title, color_setting,
                         color_value, text_size_normal, hidden, option, space)

    # SCULPT
    if bpy.context.object.type == 'MESH' and bpy.context.object.mode == 'SCULPT':
        sculpt(test_text, CR, color_title, color_setting, color_value,
               text_size_normal, hidden, option, text_size_large, units, space)
        # SPACE
        test_text.extend([("SPACE", color_title, space)])


# ----------------------------------------------------------------------------------------------------------------------
# OBJECTS --------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    # ARMATURE
    if obj.type == 'ARMATURE':
        armature(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space)
        # SPACE
        test_text.extend([("SPACE", color_title, space)])

    # CAMERA
    if obj.type == 'CAMERA':
        camera(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space)
        # SPACE
        test_text.extend([("SPACE", color_title, space)])

    # CURVES / FONT
    if obj.type in ['CURVE', 'FONT']:
        curve_font(test_text, CR, color_title, color_setting, color_value,
                   text_size_normal, hidden, option, units, space)
        if obj.modifiers:
            # SPACE
            test_text.extend([CR, ("", color_title, space)])

    # EMPTY
    if obj.type == 'EMPTY':
        # SPACE
        test_text.extend([CR, ("", color_title, text_size_normal)])
        empty(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space)
        # SPACE
        test_text.extend([("SPACE", color_title, space)])

    # LATTICE
    if obj.type == 'LATTICE':
        text_lattice(test_text, CR, color_title, color_setting, color_value,
                     text_size_normal, hidden, option, units, space)
        # SPACE
        test_text.extend([("SPACE", color_title, space)])

    # LIGHT
    if obj.type == 'LAMP':
        cycles_lights(test_text, CR, color_title, color_setting, color_value,
                      text_size_normal, hidden, option, units, space)
        # SPACE
        test_text.extend([("SPACE", color_title, space)])

    # METABALL
    if obj.type == 'META':
        metaball(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space)
        # SPACE
        test_text.extend([("SPACE", color_title, space)])

# ----------------------------------------------------------------------------------------------------------------------
# MODIFIERS ------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    wm = bpy.context.window_manager

    # from ppretty import ppretty
    # print("wm: ")
    # print(ppretty(wm, depth=1, seq_length=100))
    # index = wm.infotext.active_modifier
    # index = infotext.active_modifier

    GREEN = (0.5, 1, 0, 1)
    NOIR = (0, 0, 0, 1)
    BLANC = (1, 1, 1, 1)

    index = -1
    if hasattr(wm, 'infotext') and hasattr(wm.infotext, 'active_modifier'):
        index = wm.infotext.active_modifier

    if show_modifiers:

        # for mod in bpy.context.active_object.modifiers:
        for i, mod in enumerate(bpy.context.object.modifiers):

            color_title = BLANC
            if i == index:
                color_title = GREEN

            if mod.type not in {'BEVEL', 'ARRAY', 'SUBSURF', 'LATTICE', 'BOOLEAN', 'MIRROR', 'SOLIDIFY',
                                'DECIMATE', 'EDGE_SPLIT', 'DISPLACE', 'MULTIRES', 'BUILD', 'ARMATURE',
                                'MASK', 'REMESH', 'TRIANGULATE', 'SHRINKWRAP', 'WIREFRAME', 'SKIN', 'SCREW',
                                'CURVE', 'MESH_DEFORM', 'LAPLACIANDEFORM', 'CAST', 'CORRECTIVE_SMOOTH',
                                'HOOK', 'LAPLACIANSMOOTH', 'SIMPLE_DEFORM', 'SMOOTH', 'SURFACE_DEFORM',
                                'WARP', 'WAVE', 'WEIGHTED_NORMAL'
                                }:

                # MODIFIER STILL NOT ADDED
                if mod.show_viewport:
                    test_text.extend([CR, (str(mod.type), color_title, text_size_normal), ("  ", color_title, text_size_normal),
                                      (str(mod.name), color_value, text_size_normal)])
                else:
                    test_text.extend([CR, (str(mod.type), color_title, text_size_normal), ("  ", color_title, text_size_normal),
                                      (str(mod.name), color_value, text_size_normal)])
                    test_text.extend([(" Hidden ", hidden, text_size_normal)])

            # modifiers_list[mod]
            if mod.type == 'ARMATURE':
                mod_armature(test_text, mod, CR, color_title, color_setting, color_value,
                             text_size_normal, hidden, option, space, simple_text_mode)

            if mod.type == 'ARRAY':
                mod_array(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                          hidden, option, units, space, simple_text_mode)

            if mod.type == 'BEVEL':
                mod_bevel(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                          hidden, option, units, space, simple_text_mode)

            if mod.type == 'BOOLEAN':
                mod_boolean(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                            hidden, option, units, space, simple_text_mode)

            if mod.type == 'BUILD':
                mod_build(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                          hidden, option, units, space, simple_text_mode)

            if mod.type == 'CAST':
                mod_cast(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                         hidden, option, units, space, simple_text_mode)

            if mod.type == 'CORRECTIVE_SMOOTH':
                mod_corrective_smooth(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                                      hidden, option, units, space, simple_text_mode)

            if mod.type == 'CURVE':
                mod_curve(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                          hidden, option, units, space, simple_text_mode)

            if mod.type == 'DECIMATE':
                mod_decimate(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                             hidden, option, units, space, simple_text_mode)

            if mod.type == 'DISPLACE':
                mod_displace(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                             hidden, option, units, space, simple_text_mode)

            if mod.type == 'EDGE_SPLIT':
                mod_edge_split(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                               hidden, option, units, space, simple_text_mode)

            if mod.type == 'HOOK':
                mod_hook(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                         hidden, option, units, space, simple_text_mode)

            if mod.type == 'LAPLACIANDEFORM':
                mod_laplacian_deformer(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                                       hidden, option, units, space, simple_text_mode)

            if mod.type == 'LAPLACIANSMOOTH':
                mod_laplacian_smooth(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                                     hidden, option, units, space, simple_text_mode)

            if mod.type == 'LATTICE':
                mod_lattice(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                            hidden, option, units, space, simple_text_mode)

            if mod.type == 'MASK':
                mod_mask(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                         hidden, option, units, space, simple_text_mode)

            if mod.type == 'MESH_DEFORM':
                mod_mesh_deform(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                                hidden, option, units, space, simple_text_mode)

            if mod.type == 'MIRROR':
                mod_mirror(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                           hidden, option, units, space, simple_text_mode)

            if mod.type == 'MULTIRES':
                mod_multires(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                             hidden, option, units, space, simple_text_mode)

            if mod.type == 'REMESH':
                mod_remesh(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                           hidden, option, units, space, simple_text_mode)

            if mod.type == 'SCREW':
                mod_screw(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                          hidden, option, units, space, simple_text_mode)

            if mod.type == 'SHRINKWRAP':
                mod_shrinkwrap(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                               hidden, option, units, space, simple_text_mode)

            if mod.type == 'SIMPLE_DEFORM':
                mod_simple_deform(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                                  hidden, option, units, space, simple_text_mode)

            if mod.type == 'SKIN':
                mod_skin(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                         hidden, option, units, space, simple_text_mode)

            if mod.type == 'SMOOTH':
                mod_smooth(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                           hidden, option, units, space, simple_text_mode)

            if mod.type == 'SOLIDIFY':
                mod_solidify(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                             hidden, option, units, space, simple_text_mode)

            if mod.type == 'SUBSURF':
                mod_subsurf(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                            hidden, option, units, space, simple_text_mode)

            if mod.type == 'SURFACE_DEFORM':
                mod_surface_deform(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                                   hidden, option, units, space, simple_text_mode)

            if mod.type == 'TRIANGULATE':
                mod_triangulate(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                                hidden, option, units, space, simple_text_mode)

            if mod.type == 'WARP':
                mod_warp(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                         hidden, option, units, space, simple_text_mode)

            if mod.type == 'WAVE':
                mod_wave(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                         hidden, option, units, space, simple_text_mode)

            if mod.type == 'WIREFRAME':
                mod_wireframe(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                              hidden, option, units, space, simple_text_mode)

            if mod.type == 'WEIGHTED_NORMAL':
                mod_weighted_normals(test_text, mod, CR, color_title, color_setting, color_value, text_size_normal,
                                     hidden, option, units, space, simple_text_mode)

    # WARNING
    # SPACE
    test_text.extend([("SPACE", color_title, space)])
    warning(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, units, space)

    # Blender Keymaps
    if show_blender_keymaps:
        blender_keymaps(test_text, CR, color_title, color_setting, color_value, text_size_normal, hidden, option, space)

    # bpy.context.area.tag_redraw()
    return test_text
