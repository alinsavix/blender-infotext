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
print(__name__ + "1")
from math import degrees
print(__name__ + "2")
# from .functions import get_addon_preferences, infotext_update_mesh_info_values
from .functions import *
print(__name__ + "3")
import bmesh
# from .icon.icons import load_icons
print(__name__ + "4")
from os.path import dirname, join
from . import png
print(__name__ + "::5")

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
def blender_keymaps(test_text, CR, title_var, setting, value, text_size, hidden, option, space):
    test_text.extend([CR, ("BLENDER KEYMAPS:", value, text_size)])
    test_text.extend([CR, ("", title_var, text_size)])
    test_text.extend([CR, ("G: ", title_var, text_size), ("Move", setting, text_size)])
    test_text.extend([CR, ("R: ", title_var, text_size), ("Rotate", setting, text_size)])
    test_text.extend([CR, ("S: ", title_var, text_size), ("Scale", setting, text_size)])
    test_text.extend([CR, (" ", title_var, text_size)])
    test_text.extend([CR, ("SHFT+D: ", title_var, text_size), ("Duplicate", setting, text_size)])
    test_text.extend([CR, ("ALT+D: ", title_var, text_size), ("Duplicate Instance", setting, text_size)])
    test_text.extend([CR, ("", title_var, text_size)])
    test_text.extend([CR, ("H: ", title_var, text_size), ("Hide Selection", setting, text_size)])
    test_text.extend([CR, ("ALT+H: ", title_var, text_size), ("Unhide Everything", setting, text_size)])
    test_text.extend([CR, ("M: ", title_var, text_size), ("Collections", setting, text_size)])
    test_text.extend([CR, ("CTRL+A: ", title_var, text_size), ("Apply Transforms", setting, text_size)])
    test_text.extend([CR, ("", value, text_size)])

    # if bpy.context.object.mode == "OBJECT":

    if bpy.context.object.mode == "EDIT":
        if tuple(bpy.context.tool_settings.mesh_select_mode) == (True, False, False):
            test_text.extend([CR, ("VERTEX MODE: ", value, text_size)])
            test_text.extend([CR, ("", value, text_size)])
            test_text.extend([CR, ("CTRL+V: ", title_var, text_size), ("Vertex Menu", setting, text_size)])
            test_text.extend([CR, ("ALT+M: ", title_var, text_size), ("Merge MEnu", setting, text_size)])
            test_text.extend([CR, ("E: ", title_var, text_size), ("Extrude Vertex", setting, text_size)])
            test_text.extend([CR, ("F: ", title_var, text_size), ("New Face", setting, text_size)])
            test_text.extend([CR, ("K: ", title_var, text_size), ("Knife", setting, text_size)])
            test_text.extend([CR, ("P: ", title_var, text_size), ("Separate", setting, text_size)])
            test_text.extend([CR, ("X: ", title_var, text_size), ("Delete", setting, text_size)])
            test_text.extend([CR, ("Y: ", title_var, text_size), ("Split", setting, text_size)])
            test_text.extend([CR, ("CTRL+SHIT+B: ", title_var, text_size), ("Bevel Vertices", setting, text_size)])
            test_text.extend([CR, ("ALT+D: ", title_var, text_size), ("Extand Vertex", setting, text_size)])
            test_text.extend([CR, ("ALT+S: ", title_var, text_size), ("Shrink Fatten", setting, text_size)])

        elif tuple(bpy.context.tool_settings.mesh_select_mode) == (False, True, False):
            test_text.extend([CR, ("EDGE MODE: ", value, text_size)])
            test_text.extend([CR, ("", value, text_size)])
            test_text.extend([CR, ("CTRL+E: ", title_var, text_size), ("Edge Menu", setting, text_size)])
            test_text.extend([CR, ("ALT+M: ", title_var, text_size), ("Merge MEnu", setting, text_size)])
            test_text.extend([CR, ("E: ", title_var, text_size), ("Extrude Edge", setting, text_size)])
            test_text.extend([CR, ("F: ", title_var, text_size), ("New Face", setting, text_size)])
            test_text.extend([CR, ("K: ", title_var, text_size), ("Knife", setting, text_size)])
            test_text.extend([CR, ("P: ", title_var, text_size), ("Separate", setting, text_size)])
            test_text.extend([CR, ("X: ", title_var, text_size), ("Delete", setting, text_size)])
            test_text.extend([CR, ("Y: ", title_var, text_size), ("Split", setting, text_size)])
            test_text.extend([CR, ("CTRL+B: ", title_var, text_size), ("Bevel Edge", setting, text_size)])
            test_text.extend([CR, ("ALT+F: ", title_var, text_size), ("Fill", setting, text_size)])
            test_text.extend([CR, ("ALT+S: ", title_var, text_size), ("Shrink Fatten", setting, text_size)])

        elif tuple(bpy.context.tool_settings.mesh_select_mode) == (False, False, True):
            test_text.extend([CR, ("FACE MODE: ", value, text_size)])
            test_text.extend([CR, ("", value, text_size)])
            test_text.extend([CR, ("CTRL+F: ", title_var, text_size), ("Face Menu", setting, text_size)])
            test_text.extend([CR, ("ALT+M: ", title_var, text_size), ("Merge MEnu", setting, text_size)])
            test_text.extend([CR, ("ALT+N: ", title_var, text_size), ("Normal Menu", setting, text_size)])
            test_text.extend([CR, ("E: ", title_var, text_size), ("Extrude Face", setting, text_size)])
            test_text.extend([CR, ("F: ", title_var, text_size), ("New Face", setting, text_size)])
            test_text.extend([CR, ("I: ", title_var, text_size), ("Inset", setting, text_size)])
            test_text.extend([CR, ("K: ", title_var, text_size), ("Knife", setting, text_size)])
            test_text.extend([CR, ("P: ", title_var, text_size), ("Separate", setting, text_size)])
            test_text.extend([CR, ("X: ", title_var, text_size), ("Delete", setting, text_size)])
            test_text.extend([CR, ("Y: ", title_var, text_size), ("Split", setting, text_size)])
            test_text.extend([CR, ("CTRL+T: ", title_var, text_size), ("Triangulate", setting, text_size)])
            test_text.extend([CR, ("ALT+J: ", title_var, text_size), ("Tri To Quad", setting, text_size)])
            test_text.extend([CR, ("ALT+S: ", title_var, text_size), ("Shrink Fatten", setting, text_size)])


# ---------------------------------------------------------------
# KEYMAPS
# ---------------------------------------------------------------
def keymaps(test_text, CR, title_var, setting, value, text_size, hidden, option, space):
    test_text.extend([CR, ("KEYMAPS:", value, text_size)])
    test_text.extend([CR, ("SPEEDFLOW: ", title_var, text_size), ("SPACEBAR", setting, text_size)])
    test_text.extend([CR, ("COMPANION: ", title_var, text_size), ("SHIFT + Q", setting, text_size)])
    test_text.extend([CR, ("Note: ", title_var, text_size),
                      ("You can change the keymaps in the add-ons preferences", value, text_size)])
    test_text.extend([CR, ("Note: ", title_var, text_size),
                      ("Hide this text in the add-ons preferences", value, text_size)])
    test_text.extend([CR, ("", title_var, text_size)])

# ---------------------------------------------------------------
# MODE
# ---------------------------------------------------------------


def mode(test_text, CR, title_var, setting, value, text_size, hidden, option, text_size_deux, space):
    obj = bpy.context.active_object

    mode = obj.mode

    if bpy.context.object.mode == "OBJECT":
        # test_text.extend([CR, ('ICON', 'ICON_OBJECT_DATAMODE.png'), ("   OBJECT MODE", title_var, text_size_deux)])
        test_text.extend([CR, ("OBJECT MODE", title_var, text_size_deux)])

    elif bpy.context.object.mode == "EDIT":
        # test_text.extend([CR, ('ICON', 'ICON_EDITMODE_HLT.png'), ("   EDIT MODE", title_var, text_size_deux)])
        test_text.extend([CR, ("EDIT MODE", title_var, text_size_deux)])

    elif bpy.context.object.mode == "SCULPT":
        # test_text.extend([CR, ('ICON', 'ICON_SCULPTMODE_HLT.png'), ("   SCULPT MODE", title_var, text_size_deux)])
        test_text.extend([CR, ("SCULPT MODE", title_var, text_size_deux)])

    elif bpy.context.object.mode == "VERTEX_PAINT":
        # test_text.extend([CR, ('ICON', 'ICON_VPAINT_HLT.png'), ("    VERTEX PAINT MODE", title_var, text_size_deux)])
        test_text.extend([CR, ("VERTEX PAINT MODE", title_var, text_size_deux)])

    elif bpy.context.object.mode == "WEIGHT_PAINT":
        # test_text.extend([CR, ('ICON', 'ICON_WPAINT_HLT.png'), ("    WEIGHT PAINT MODE", title_var, text_size_deux)])
        test_text.extend([CR, ("WEIGHT PAINT MODE", title_var, text_size_deux)])

    elif bpy.context.object.mode == "TEXTURE_PAINT":
        # test_text.extend([CR, ('ICON', 'ICON_TPAINT_HLT.png'), ("    TEXTURE PAINT MODE", title_var, text_size_deux)])
        test_text.extend([CR, ("TEXTURE PAINT MODE", title_var, text_size_deux)])

    # elif bpy.context.object.mode == "PARTICLE":
    #     test_text.extend([CR, ('ICON', 'ICON_PARTICLEMODE.png'), ("    PARTICLES EDIT MODE", title_var, text_size_deux)])

    elif bpy.context.object.mode == "POSE":
        # test_text.extend([CR, ('ICON', 'ICON_POSE_HLT.png'), ("    POSE MODE", title_var, text_size_deux)])
        test_text.extend([CR, ("POSE MODE", title_var, text_size_deux)])

    # test_text.extend(
    #     [CR, ('ICON', 'ICON_OBJECT_DATAMODE.png'), ("    ", setting, text_size)])

    # if "_" in mode:
    #     text_mode = mode.replace("_", " ")
    #     test_text.extend([CR,('ICON', 'ICON_OBJECT_DATAMODE.png'), ("    ", setting, text_size), (text_mode, title_var, text_size_deux)])
    # else:
    #     test_text.extend([CR, ("{} MODE".format(mode), title_var, text_size_deux)])

# ---------------------------------------------------------------
# NAME
# ---------------------------------------------------------------


def name(test_text, CR, title_var, setting, value, text_size, hidden, option, space):
    obj = bpy.context.active_object

    # if obj.type =='MESH':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_MESH.png'), ("    ", setting, text_size)])
    #     test_text.extend([CR, ("Name: ", setting, text_size), (obj.name, value, text_size)])
    # elif obj.type == 'CURVE':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_CURVE.png'), ("    ", setting, text_size)])
    #     test_text.extend([CR, ("    ", setting, text_size), (obj.name, value, text_size)])
    # elif obj.type == 'EMPTY':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_EMPTY.png'), ("    ", setting, text_size)])
    #     test_text.extend([CR, ("    ", setting, text_size), (obj.name, value, text_size)])
    #
    # elif obj.type == 'CAMERA':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_CAMERA.png'), ("     ", setting, text_size)])
    #     test_text.extend([CR, ("     ", setting, text_size), (obj.name, value, text_size)])
    #
    # elif obj.type == 'LATTICE':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_LATTICE.png'), ("     ", setting, text_size)])
    #     test_text.extend([CR, ("     ", setting, text_size), (obj.name, value, text_size)])
    #
    # elif obj.type == 'META':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_META.png'), ("    ", setting, text_size)])
    #     test_text.extend([CR, ("    ", setting, text_size), (obj.name, value, text_size)])
    #
    # elif obj.type == 'ARMATURE':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_ARMATURE.png'), ("    ", setting, text_size)])
    #     test_text.extend([CR, ("    ", setting, text_size), (obj.name, value, text_size)])
    #
    # elif obj.type == 'FONT':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_FONT.png'), ("     ", setting, text_size)])
    #     test_text.extend([CR, ("     ", setting, text_size), (obj.name, value, text_size)])
    #
    # elif obj.type == 'LATTICE':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_LATTICE.png'), ("    ", setting, text_size)])
    #     test_text.extend([CR, ("    ", setting, text_size), (obj.name, value, text_size)])
    #
    # elif obj.type == 'LAMP':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_LAMP.png'), ("    ", setting, text_size)])
    #     test_text.extend([CR, ("    ", setting, text_size), (obj.name, value, text_size)])
    #
    # elif obj.type == 'SURFACE':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_SURFACE.png'), ("    ", setting, text_size)])
    #     test_text.extend([CR, ("    ", setting, text_size), (obj.name, value, text_size)])
    #
    # elif obj.type == 'SPEAKER':
    #     # test_text.extend([CR, ('ICON', 'ICON_OUTLINER_OB_SPEAKER.png'), ("    ", setting, text_size)])
    #     test_text.extend([CR, ("    ", setting, text_size), (obj.name, value, text_size)])

    # MESH NAME
    # test_text.extend([CR, (obj.type, title_var, text_size)])
    test_text.extend([CR, ("Name: ", title_var, text_size), (obj.name, value, text_size)])

# ---------------------------------------------------------------
# LOCATION / ROTATION / SCALE
# ---------------------------------------------------------------


def loc(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space):
    obj = bpy.context.active_object

    axis_list = (" X ", " Y ", " Z ")
    # LOCATION
    if tuple(obj.location) != (0.0, 0.0, 0.0):
        # test_text.extend([CR,("LOCATION ", title_var, text_size),
        #                   ("  %s" % round(obj.location[0], 2), value, text_size), (units, value, text_size),
        #                   ("  %s" % round(obj.location[1], 2), value, text_size), (units, value, text_size),
        #                   ("  %s" % round(obj.location[2], 2), value, text_size), (units, value, text_size)])

        # test_text.extend([CR, ('ICON', 'ICON_MAN_TRANS.png'), ("    ", title_var, text_size)])
        test_text.extend([CR, ("L: ", title_var, text_size)])

        for idx, axis in enumerate(axis_list):
            test_text.extend([(axis, setting, text_size),
                              (str(round(obj.location[idx], 2)), value, text_size),
                              (units, value, text_size)])

    # ROTATION
    if tuple(obj.rotation_euler) != (0.0, 0.0, 0.0):
        # test_text.extend([CR, ('ICON', 'ICON_MAN_ROT.png'), ("    ", title_var, text_size)])
        test_text.extend([CR, ("R: ", title_var, text_size)])

        for idx, axis in enumerate(axis_list):
            test_text.extend([(axis, setting, text_size),
                              (str(round(math.degrees(obj.rotation_euler[idx]), 2)), value, text_size), ("°", value, text_size)])

    # SCALE
    if tuple(obj.scale) != (1, 1, 1):
        # test_text.extend([CR, ('ICON', 'ICON_MAN_SCALE.png'), ("    ", title_var, text_size)])
        test_text.extend([CR, ("S: ", title_var, text_size)])

        for idx, axis in enumerate(axis_list):
            test_text.extend([(axis, setting, text_size),
                              (str(round(obj.scale[idx], 2)), value, text_size)])

    if any([tuple(obj.location) != (0.0, 0.0, 0.0), tuple(obj.rotation_euler) != (0.0, 0.0, 0.0), tuple(obj.scale) != (1, 1, 1)]):
        # SPACE
        test_text.extend([("SPACE", title_var, space)])

# ---------------------------------------------------------------
# NGONS
# ---------------------------------------------------------------


def ngons(test_text, CR, title_var, value, text_size, space):
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
    # test_text.extend([CR, ('ICON', 'vert.png'), ("    ", title_var, text_size),
    #                   (str(vcount), value, text_size)])
    test_text.extend([CR, ("V: ", title_var, text_size),
                      (str(vcount), value, text_size)])

    # EDGES
    # test_text.extend([("  ", title_var, text_size), ('ICON', 'edge.png'), ("    ", title_var, text_size),
    #                   (str(ecount), value, text_size)])
    test_text.extend([("  E: ", title_var, text_size), (" ", title_var, text_size),
                      (str(ecount), value, text_size)])

    # FACES
    # test_text.extend([("  ", title_var, text_size), ('ICON', 'face.png'), ("    ", title_var, text_size),
    #                   (str(fcount), value, text_size)])
    test_text.extend([("  F: ", title_var, text_size), (" ", title_var, text_size),
                      (str(fcount), value, text_size)])

    if not bpy.context.object.mode == 'SCULPT':
        tcount = infotext.face_type_count['TRIS']
        ncount = infotext.face_type_count['NGONS']
        # TRIS
        if tcount:
            # test_text.extend([("  ", title_var, text_size), ('ICON', 'triangle.png'), ("    ", title_var, text_size),
            #                   (str(tcount), value, text_size)])

            test_text.extend([("  T: ", title_var, text_size), (" ", title_var, text_size),
                              (str(tcount), value, text_size)])

        # NGONS ICON_OBJECT_DATA
        if ncount:
            # test_text.extend([(" ", title_var, text_size), ('ICON', 'ngons.png'),
            #                   ("     ", title_var, text_size), (str(ncount), value, text_size)])

            test_text.extend([("  N: ", title_var, text_size),
                              (" ", title_var, text_size), (str(ncount), value, text_size)])

# ---------------------------------------------------------------
# MESH OPTIONS
# ---------------------------------------------------------------


def mesh_options(test_text, CR, title_var, setting, value, text_size, hidden, option, space):
    obj = bpy.context.active_object

    # MATERIALS
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        if obj.material_slots:
            if obj.active_material:
                # test_text.extend([CR, ('ICON', 'ICON_SMOOTH.png'),("     ", title_var, text_size)])
                test_text.extend([CR, ("MATERIAL: ", title_var, text_size)])
                test_text.extend([(str(len(obj.material_slots)), setting, text_size), (" ", title_var,
                                                                                       text_size), (str(obj.active_material.name), value, text_size)])

                if obj.active_material.users >= 2:
                    test_text.extend([(" ", setting, text_size), (str(obj.active_material.users),
                                                                  setting, text_size), (" users", setting, text_size)])
                if obj.active_material.use_fake_user:
                    test_text.extend([(" ,FAKE USER ", setting, text_size)])
            else:
                test_text.extend([CR, ("SLOT ONLY", title_var, text_size)])

            # SPACE
            test_text.extend([("SPACE", title_var, space)])

    if obj.type == 'MESH':
        # AUTOSMOOTH
        if obj.data.use_auto_smooth:
            test_text.extend([CR, ("AUTOSMOOTH ", title_var, text_size)])
            # ANGLE
            test_text.extend([(" ANGLE ", setting, text_size), (
                str(round(math.degrees(obj.data.auto_smooth_angle), 1)), value, text_size),
                ("°", value, text_size)])

    if obj.type in ['MESH', 'LATTICE']:
        # VERTEX GROUPS
        if obj.vertex_groups:
            test_text.extend([CR, ("VERTEX GROUPS", title_var, text_size)])
            test_text.extend([(" ", title_var, text_size),
                              (str(len(obj.vertex_groups)), setting, text_size)])
            test_text.extend([(" ", title_var, text_size),
                              (str(obj.vertex_groups[int(obj.vertex_groups.active_index)].name), value, text_size)])

    if obj.type in ['CURVE', 'MESH', 'LATTICE']:
        # SHAPE KEYS
        if obj.data.shape_keys:
            test_text.extend([CR, ("SHAPE KEYS", title_var, text_size)])
            test_text.extend([(" ", title_var, text_size),
                              (str(len(obj.data.shape_keys.key_blocks)), setting, text_size)])
            test_text.extend([(" ", title_var, text_size),
                              (str(obj.data.shape_keys.key_blocks[int(bpy.context.object.active_shape_key_index)].name), value, text_size)])

            if bpy.context.object.mode == 'OBJECT':
                test_text.extend([(" VALUE ", setting, text_size),
                                  (str(round(obj.data.shape_keys.key_blocks[int(bpy.context.object.active_shape_key_index)].value, 3)),
                                   value, text_size)])

    if obj.type == 'MESH':
        # UV's
        if obj.data.uv_layers:
            test_text.extend([CR, ("UV's", title_var, text_size)])
            test_text.extend([(" ", title_var, text_size), (str(len(obj.data.uv_layers)), setting, text_size)])
            test_text.extend([(" ", title_var, text_size), (str(
                obj.data.uv_layers[int(obj.data.uv_layers.active_index)].name), value, text_size)])

        # VERTEX COLORS
        if obj.data.vertex_colors:
            test_text.extend([CR, ("VERTEX COLORS", title_var, text_size)])
            test_text.extend([(" ", title_var, text_size),
                              (str(len(obj.data.vertex_colors)), setting, text_size)])
            test_text.extend([(" ", title_var, text_size),
                              (str(obj.data.vertex_colors[int(obj.data.vertex_colors.active_index)].name), value, text_size)])

    if obj.type == 'LATTICE':
        if any([obj.vertex_groups, obj.data.shape_keys]):
            # SPACE
            test_text.extend([("SPACE", title_var, space)])

    if obj.type in ['CURVE', 'FONT']:
        if any([obj.vertex_groups, obj.data.shape_keys]):
            # SPACE
            test_text.extend([("SPACE", title_var, space)])

    if obj.type == 'MESH':
        if any([obj.data.use_auto_smooth, obj.vertex_groups, obj.data.shape_keys, obj.data.uv_layers, obj.data.vertex_colors]):
            # SPACE
            test_text.extend([("SPACE", title_var, space)])

# ---------------------------------------------------------------
# SCULPT
# ---------------------------------------------------------------


def sculpt(test_text, CR, title_var, setting, value, text_size, hidden, option, text_size_deux, units, space):
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
    test_text.extend([("SPACE", title_var, space)])

    # if bpy.types.Brush == 'GRAB':
    # test_text.extend([CR, ('ICON', 'grab.png'), ("    ", setting, text_size)])

    test_text.extend([CR, (str(brush.name.upper()), title_var, text_size_deux)])

    # SPACE
    test_text.extend([("SPACE", title_var, space)])

    # RADIUS
    test_text.extend([CR, ("RADIUS ", setting, text_size),
                      (str(round(ups.size, 2)), value, text_size), (" px", value, text_size)])
    # STRENGTH
    test_text.extend([CR, ("STRENGTH ", setting, text_size),
                      (str(round(brush.strength, 3)), value, text_size)])

    # STRENGTH
    brush_autosmooth = bpy.data.brushes[brush.name].auto_smooth_factor
    if brush_autosmooth:
        test_text.extend([CR, ("AUTOSMOOTH ", setting, text_size),
                          (str(round(brush_autosmooth, 3)), value, text_size)])

    brush_use_frontface = bpy.data.brushes[brush.name].use_frontface
    if bpy.data.brushes[brush.name].use_frontface:
        test_text.extend([CR, ("FRONT FACE ", setting, text_size),
                          (str(brush_use_frontface), value, text_size)])

    # brush_stroke_method = bpy.data.brushes[brush.name].stroke_method
    # if brush_stroke_method == 'SPACE':
    #     test_text.extend([CR, ("STROKE METHOD ", setting, text_size)])
    #     test_text.extend([("SPACE", value, text_size)])
    # else:
    #     test_text.extend([CR, ("STROKE METHOD ", setting, text_size),
    #                       (str(brush_stroke_method), value, text_size)])

    # SPACE
    test_text.extend([("SPACE", title_var, space)])

    if bpy.context.sculpt_object.use_dynamic_topology_sculpting:
        # SPACE
        test_text.extend([("SPACE", title_var, space)])

        # DYNTOPO
        test_text.extend([CR, ("DYNTOPO ", title_var, text_size_deux)])
        # SPACE
        test_text.extend([("SPACE", title_var, space)])

        if context_tool.detail_type_method == 'CONSTANT':

            test_text.extend([CR, ("CONSTANT DETAIL ", setting, text_size),
                              (str(round(context_tool.constant_detail_resolution, 2)), value, text_size)])

        elif context_tool.detail_type_method == 'RELATIVE':
            test_text.extend([CR, ("RELATIVE DETAIL ", setting, text_size),
                              (str(round(context_tool.detail_size, 2)), value,
                               text_size), (" px", value, text_size)])
        else:
            test_text.extend([CR, ("BRUSH DETAIL ", setting, text_size),
                              (str(round(context_tool.detail_percent, 2)), value,
                               text_size), ("%", value, text_size)])

        # SUBDIV METHOD

        # SUBDIVIDE_COLLAPSE
        if context_tool.detail_refine_method == 'SUBDIVIDE_COLLAPSE':
            test_text.extend([CR, (str("SUBDIVIDE COLLAPSE"), setting, text_size)])

        # COLLAPSE
        elif context_tool.detail_refine_method == 'COLLAPSE':
            test_text.extend([CR, (str("COLLAPSE"), setting, text_size)])

        # SUBDIVIDE
        else:
            test_text.extend([CR, (str("SUBDIVIDE"), setting, text_size)])

        # SMOOTH SHADING
        if context_tool.use_smooth_shading:
            test_text.extend([CR, (str("SMOOTH SHADING"), value, text_size)])

        # SYMMETRIZE DIRECTION
        test_text.extend([CR, (str("SYMMETRIZE "), setting, text_size),
                          (str(context_tool.symmetrize_direction.lower().capitalize()), value, text_size)])

        # SPACE
        test_text.extend([("SPACE", title_var, space)])

    # SYMMETRIZE
    if any([context_tool.use_symmetry_x, context_tool.use_symmetry_y, context_tool.use_symmetry_z]):
        test_text.extend([CR, (str("MIRROR"), setting, text_size)])
        if context_tool.use_symmetry_x:
            test_text.extend([(str(" X "), value, text_size)])
        if context_tool.use_symmetry_y:
            test_text.extend([(str(" Y "), value, text_size)])
        if context_tool.use_symmetry_z:
            test_text.extend([(str(" Z "), value, text_size)])

    if context_tool.use_symmetry_feather:
        test_text.extend([CR, (str("FEATHER "), title_var, text_size)])

    # LOCK
    if any([context_tool.lock_x, context_tool.lock_y, context_tool.lock_z]):
        test_text.extend([CR, (str("LOCK  "), setting, text_size)])
        if context_tool.lock_x:
            test_text.extend([(str(" X "), value, text_size)])
        if context_tool.lock_y:
            test_text.extend([(str(" Y "), value, text_size)])
        if context_tool.lock_z:
            test_text.extend([(str(" Z "), value, text_size)])

    # TILE
    if any([context_tool.tile_x, context_tool.tile_y, context_tool.tile_z]):
        test_text.extend([CR, (str("TILE    "), setting, text_size)])
        if context_tool.tile_x:
            test_text.extend([(str(" X "), value, text_size)])
        if context_tool.tile_y:
            test_text.extend([(str(" Y "), value, text_size)])
        if context_tool.tile_z:
            test_text.extend([(str(" Z "), value, text_size)])

# ----------------------------------------------------------------------------------------------------------------------
# MODIFIERS ------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------
# ARRAY
# ---------------------------------------------------------------


def mod_array(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR,('ICON', 'ICON_MOD_ARRAY.png'),("    ", setting, text_size), (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:

                # FIT MODE
                if mod.fit_type == 'FIXED_COUNT':
                    test_text.extend([(" Count ", setting, text_size), (str(mod.count), value, text_size)])

                elif mod.fit_type == 'FIT_CURVE':
                    if mod.curve:
                        # Object
                        test_text.extend([(" Curve ", setting, text_size),
                                          (mod.curve.name, value, text_size)])
                    else:
                        test_text.extend([(" No Curve Selected", hidden, text_size)])

                else:
                    test_text.extend([(" Length ", setting, text_size),
                                      (str(round(mod.fit_length, 2)), value, text_size)])

                # CONSTANT
                if mod.use_constant_offset:
                    # test_text.extend([(" Constant ", setting, text_size),
                    #                   ("%s" %round(mod.constant_offset_displace[0], 1),value, text_size),
                    #                   ("  %s" %round(mod.constant_offset_displace[1], 1),value, text_size),
                    #                   ("  %s" %round(mod.constant_offset_displace[2], 1),value, text_size)])

                    test_text.extend([(" Constant ", setting, text_size)])

                    # X
                    if mod.constant_offset_displace[0] != 0:
                        test_text.extend(
                            [(" X ", setting, text_size), (str(round(mod.constant_offset_displace[0], 1)), value, text_size), (units, value, text_size)])

                    # Y
                    if mod.constant_offset_displace[1] != 0:
                        test_text.extend(
                            [(" Y ", setting, text_size), (str(round(mod.constant_offset_displace[1], 1)), value, text_size), (units, value, text_size)])

                    # Z
                    if mod.constant_offset_displace[2] != 0:
                        test_text.extend(
                            [(" Z ", setting, text_size), (str(round(mod.constant_offset_displace[2], 1)), value, text_size), (units, value, text_size)])

                # RELATIVE
                elif mod.use_relative_offset:
                    test_text.extend([(" Relative ", setting, text_size)])

                    # X
                    if mod.relative_offset_displace[0] != 0:
                        test_text.extend([(" X ", setting, text_size), (str(
                            round(mod.relative_offset_displace[0], 1)), value, text_size)])

                    # Y
                    if mod.relative_offset_displace[1] != 0:
                        test_text.extend([(" Y ", setting, text_size), (str(
                            round(mod.relative_offset_displace[1], 1)), value, text_size)])

                    # Z
                    if mod.relative_offset_displace[2] != 0:
                        test_text.extend([(" Z ", setting, text_size), (str(
                            round(mod.relative_offset_displace[2], 1)), value, text_size)])

                # MERGE
                if mod.use_merge_vertices:
                    test_text.extend([(" Merge ", setting, text_size),
                                      (str(round(mod.merge_threshold, 3)), value, text_size)])

                    if mod.use_merge_vertices_cap:
                        test_text.extend([(" First Last ", setting, text_size)])

                # OPTIONS
                if any([mod.use_object_offset, mod.start_cap, mod.end_cap]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # OBJECT OFFSET
                    if mod.use_object_offset:
                        if mod.offset_object:
                            test_text.extend([(" Object Offset ", setting, text_size),
                                              (mod.offset_object.name, value, text_size)])
                        else:
                            test_text.extend([(" No Object Selected", hidden, text_size)])

                    # STAR CAP
                    if mod.start_cap:
                        test_text.extend([(" Start Cap ", setting, text_size),
                                          (mod.start_cap.name, value, text_size)])

                    # END CAP
                    if mod.end_cap:
                        test_text.extend([(" End Cap ", setting, text_size),
                                          (mod.end_cap.name, value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])


# ---------------------------------------------------------------
# BEVEL
# ---------------------------------------------------------------
def mod_bevel(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    wm = bpy.context.window_manager
    obj = bpy.context.active_object

    if obj.type in {'MESH', 'CURVE', 'FONT'}:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_BEVEL.png'), ("     ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])

        # if self.active_mod:
        #     test_text.extend([CR, (str(mod.name.upper()), hidden, text_size)])
        # else:
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # WIDTH
                test_text.extend([(" Width ", setting, text_size), (str(round(mod.width, 2)),
                                                                    value, text_size), (units, value, text_size)])

                # SEGMENTS
                test_text.extend([(" Segments ", setting, text_size),
                                  (str(mod.segments), value, text_size)])

                # PROFILE
                test_text.extend([(" Profile ", setting, text_size),
                                  (str(round(mod.profile, 2)), value, text_size)])

                # LIMIT METHOD
                test_text.extend([(" ", setting, text_size),
                                  (str(mod.limit_method.lower().capitalize()), setting, text_size)])

                # ANGLE
                if mod.limit_method == 'ANGLE':
                    test_text.extend([("  ", setting, text_size),
                                      (str(round(math.degrees(mod.angle_limit), 2)), value, text_size),
                                      ("°", value, text_size)])
                # VERTEX GROUP
                elif mod.limit_method == 'VGROUP':

                    if mod.vertex_group:
                        test_text.extend([("  ", setting, text_size),
                                          (str(mod.vertex_group), value, text_size)])
                    else:
                        test_text.extend([(" No Vertex Group Selected ", hidden, text_size)])

                # SPEEDFLOW
                if obj.get('SpeedFlow') and 'Bevel' in obj['SpeedFlow']:
                    if obj['SpeedFlow']['Bevel']:
                        test_text.extend([(" SUBDIV ", value, text_size)])
                    else:
                        test_text.extend([(" NO-SUBDIV ", value, text_size)])

                # OPTIONS
                if any([mod.use_clamp_overlap, mod.loop_slide, mod.use_only_vertices, mod.offset_type]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # LOOP SLIDE
                    if mod.loop_slide:
                        test_text.extend([(" Loop Slide ", setting, text_size)])

                    # CLAMP
                    if mod.use_clamp_overlap:
                        test_text.extend([(" Clamp ", setting, text_size)])

                    # ONLY VERTICES
                    if mod.use_only_vertices:
                        test_text.extend([(" Only Vertices ", setting, text_size)])

                    # OFFSET TYPE
                    test_text.extend([(" Width Method ", setting, text_size),
                                      (str(mod.offset_type.lower().capitalize()), value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# BOOLEAN
# ---------------------------------------------------------------


def mod_boolean(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_BOOLEAN.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # OPERATION
                test_text.extend([(" ", title_var, text_size),
                                  (str(mod.operation), value, text_size)])
                if mod.object:
                    # Object
                    test_text.extend([(" Object ", setting, text_size),
                                      (mod.object.name, value, text_size)])
                else:
                    test_text.extend([(" No object Selected", hidden, text_size)])

                # SOLVER
                # if (hasattr(bpy.context.preferences.system, 'opensubdiv_compute_type')):
                # if bpy.app.version == (2, 79, 0):
                #     test_text.extend([(" ", title_var, text_size),
                #                           (str(mod.solver.upper()), value, text_size)])

                # OVERLAP THRESHOLD
                # if mod.solver == 'BMESH':
                #     if mod.double_threshold > 0 :
                #         test_text.extend([(" Overlap Threshold ", setting, text_size),
                #                           (str(round(mod.double_threshold,2)), value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# BUILD
# ---------------------------------------------------------------


def mod_build(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_BUILD.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # START
                test_text.extend([(" Start ", setting, text_size),
                                  (str(round(mod.frame_start, 2)), value, text_size)])

                # LENGTH
                test_text.extend([(" Length ", setting, text_size),
                                  (str(round(mod.frame_duration, 2)), value, text_size)])

                # SEED
                if mod.use_random_order:
                    test_text.extend([(" Seed ", setting, text_size),
                                      (str(mod.seed), value, text_size)])

                if mod.use_reverse:
                    test_text.extend([(" Reversed ", setting, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# DECIMATE
# ---------------------------------------------------------------


def mod_decimate(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_DECIM.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # COLLAPSE
                if mod.decimate_type == 'COLLAPSE':
                    test_text.extend([(" Collapse ", setting, text_size)])
                    test_text.extend([(" Ratio ", setting, text_size),
                                      (str(round(mod.ratio, 2)), value, text_size)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", setting, text_size),
                                          (str(mod.vertex_group), value, text_size)])

                        # FACTOR
                        test_text.extend([(" Factor ", setting, text_size),
                                          (str(round(mod.vertex_group_factor, 2)), value, text_size)])
                    # OPTIONS
                    if any([mod.use_collapse_triangulate, mod.use_symmetry]):
                        test_text.extend([CR, ("----", title_var, text_size)])

                        # TRIANGULATE
                        if mod.use_collapse_triangulate:
                            test_text.extend([(" Triangulate ", setting, text_size)])

                        # SYMMETRY
                        if mod.use_symmetry:
                            test_text.extend([(" Symmetry ", setting, text_size),
                                              (str(mod.symmetry_axis), value, text_size)])

                # UN-SUBDIVDE
                elif mod.decimate_type == 'UNSUBDIV':
                    test_text.extend([(" Un-subdivide ", setting, text_size)])
                    test_text.extend([(" Iteration ", setting, text_size),
                                      (str(round(mod.iterations, 2)), value, text_size)])
                # PLANAR
                else:
                    test_text.extend([(" Planar ", setting, text_size)])
                    test_text.extend([(" Angle Limit ", setting, text_size), (
                        str(round(math.degrees(mod.angle_limit), 1)), value, text_size),
                        ("°", value, text_size)])

                    # OPTIONS
                    if any([mod.use_dissolve_boundaries, mod.delimit]):
                        test_text.extend([CR, ("----", title_var, text_size)])

                        # ALL BOUNDARIES
                        if mod.use_dissolve_boundaries:
                            test_text.extend([(" All Boundaries ", setting, text_size)])

                        # DELIMIT
                        if mod.delimit:
                            test_text.extend([(" Delimit ", setting, text_size)])
                            if mod.delimit == {'NORMAL'}:
                                test_text.extend([(" NORMAL ", value, text_size)])
                            elif mod.delimit == {'MATERIAL'}:
                                test_text.extend([(" MATERIAL ", value, text_size)])
                            elif mod.delimit == {'SEAM'}:
                                test_text.extend([(" SEAM ", value, text_size)])
                            elif mod.delimit == {'SHARP'}:
                                test_text.extend([(" SHARP ", value, text_size)])
                            elif mod.delimit == {'UV'}:
                                test_text.extend([(" UV ", value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# EDGE SPLIT
# ---------------------------------------------------------------


def mod_edge_split(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_EDGESPLIT.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # EDGE ANGLE
                if mod.use_edge_angle:
                    test_text.extend([(" Edges angle ", setting, text_size), (
                        str(round(math.degrees(mod.split_angle), 1)), value, text_size),
                        ("°", value, text_size)])

                # SHARP EDGES
                if mod.use_edge_sharp:
                    test_text.extend([(" Sharp Edges ", setting, text_size)])
        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# WEIGHTED NORMALS
# ---------------------------------------------------------------


def mod_weighted_normals(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_EDGESPLIT.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # Mode
                # test_text.extend([(" Mode", setting, text_size), (str(mod.mode.lower().capitalize()), setting, text_size)])
                test_text.extend([(" Mode ", setting, text_size), (str(
                    mod.mode.lower().capitalize()), value, text_size)])

                # Weight
                test_text.extend([(" Weight ", setting, text_size),
                                  (str(round(mod.weight, 2)), value, text_size)])

                # STRENGTH
                test_text.extend([(" Strength ", setting, text_size),
                                  (str(round(mod.weight, 2)), value, text_size)])

                # THRESHOLD
                test_text.extend([(" Threshold ", setting, text_size),
                                  (str(round(mod.thresh, 2)), value, text_size)])

                if any([mod.keep_sharp, mod.face_influence, mod.vertex_group]):
                    test_text.extend([CR, ("----", title_var, text_size)])
                    # KEEP SHARP
                    if mod.keep_sharp:
                        test_text.extend([(" Keep Sharp ", setting, text_size)])

                    # KEEP SHARP
                    if mod.face_influence:
                        test_text.extend([(" Face Influence ", setting, text_size)])

                    if mod.vertex_group:
                        test_text.extend([(" Vgroup ", setting, text_size),
                                          (str(mod.vertex_group), value, text_size)])
                    else:
                        test_text.extend([(" No Vertex Group Selected ", hidden, text_size)])
        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# LATTICE
# ---------------------------------------------------------------


def mod_lattice(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_LATTICE.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                if mod.object:
                    # OBJECT
                    test_text.extend([(" Object ", setting, text_size),
                                      (mod.object.name, value, text_size)])
                else:
                    test_text.extend([(" No Object Selected ", hidden, text_size)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([(" VGroup ", setting, text_size),
                                      (str(mod.vertex_group), value, text_size)])

                # STRENGTH
                test_text.extend([(" Strength ", setting, text_size),
                                  (str(round(mod.strength, 2)), value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# MASK
# ---------------------------------------------------------------


def mod_mask(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_MASK.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # ARMATURE
                if mod.mode == 'ARMATURE':
                    if mod.armature:
                        test_text.extend([(" Armature ", setting, text_size),
                                          (str(mod.armature.name), value, text_size)])
                    else:
                        test_text.extend([(" No Armature Selected ", hidden, text_size)])

                # VERTEX GROUP
                elif mod.mode == 'VERTEX_GROUP':
                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", setting, text_size),
                                          (str(mod.vertex_group), value, text_size)])
                    else:
                        test_text.extend([(" No Vertex Group Selected ", hidden, text_size)])
        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# MIRROR
# ---------------------------------------------------------------


def mod_mirror(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_MIRROR.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                if any([mod.use_axis[0], mod.use_axis[1], mod.use_axis[2]]):
                    test_text.extend([(" Axis ", setting, text_size)])
                    # X
                    if mod.use_axis[0]:
                        test_text.extend([(" X ", value, text_size)])

                    # Y
                    if mod.use_axis[1]:
                        test_text.extend([(" Y ", value, text_size)])

                    # Z
                    if mod.use_axis[2]:
                        test_text.extend([(" Z ", value, text_size)])

                # OBJECT
                if mod.mirror_object:
                    test_text.extend([(" Object ", setting, text_size),
                                      (mod.mirror_object.name, value, text_size)])

                # MERGE
                if mod.use_mirror_merge:
                    test_text.extend([(" Merge ", setting, text_size),
                                      (str(round(mod.merge_threshold, 3)), value, text_size), (units, value, text_size)])

                # OPTIONS
                if any([mod.use_clip, mod.use_mirror_vertex_groups, mod.use_mirror_u, mod.use_mirror_v]):
                    test_text.extend([CR, ("----", title_var, text_size)])
                    # CLIPPING
                    if mod.use_clip:
                        test_text.extend([(" Clipping ", setting, text_size)])

                    # VERTEX GROUP
                    if mod.use_mirror_vertex_groups:
                        test_text.extend([(" VGroup ", setting, text_size)])

                    # TEXTURES
                    if any([mod.use_mirror_u, mod.use_mirror_v]):
                        test_text.extend([(" Textures ", setting, text_size)])

                    # TEXTURE U
                    if mod.use_mirror_u:
                        test_text.extend([(" U ", setting, text_size),
                                          (str(round(mod.mirror_offset_u, 3)), value, text_size), (units, value, text_size)])

                    # TEXTURE V
                    if mod.use_mirror_v:
                        test_text.extend([(" V ", setting, text_size),
                                          (str(round(mod.mirror_offset_v, 3)), value, text_size), (units, value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# MULTIRES
# ---------------------------------------------------------------


def mod_multires(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_MULTIRES.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])

        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # SUBDIVISION TYPE
                if mod.subdivision_type == 'SIMPLE':
                    test_text.extend([(" Simple ", setting, text_size)])
                else:
                    test_text.extend([(" Catmull Clark ", setting, text_size)])

                if mod.levels >= 1:
                    # LEVELS
                    test_text.extend([(" Levels ", setting, text_size),
                                      (str(mod.levels), value, text_size)])

                    # RENDER
                    test_text.extend([(" Render ", setting, text_size),
                                      (str(mod.render_levels), value, text_size)])

                    # SCULPT
                    test_text.extend([(" Sculpt ", setting, text_size),
                                      (str(mod.sculpt_levels), value, text_size)])

                # OPTIONS
                if any([mod.use_subsurf_uv, mod.show_only_control_edges]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # UV's
                    if mod.use_subsurf_uv:
                        test_text.extend([(" UV's ", setting, text_size)])

                    # OPTIMAL DISPLAY
                    if mod.show_only_control_edges:
                        test_text.extend([(" Optimal Display ", setting, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# REMESH
# ---------------------------------------------------------------


def mod_remesh(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_REMESH.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                test_text.extend([(" ", title_var, text_size), (str(mod.mode), value, text_size)])

                # OCTREE DEPTH
                test_text.extend([(" Octree Depth ", setting, text_size),
                                  (str(mod.octree_depth), value, text_size)])

                # SCALE
                test_text.extend([(" Scale ", setting, text_size),
                                  (str(round(mod.scale, 2)), value, text_size)])

                # SHARPNESS
                if mod.mode == 'SHARP':
                    test_text.extend([(" Sharpness ", setting, text_size),
                                      (str(round(mod.sharpness, 2)), value, text_size)])

                # OPTIONS
                if any([mod.use_smooth_shade, mod.use_remove_disconnected]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # SMOOTH SHADING
                    if mod.use_smooth_shade:
                        test_text.extend([(" Smooth Shading ", setting, text_size)])

                    # REMOVE DISCONNECTED
                    if mod.use_remove_disconnected:
                        test_text.extend([(" Remove Disconnected Pieces ", setting, text_size),
                                          (str(round(mod.threshold, 2)), value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# SCREW
# ---------------------------------------------------------------


def mod_screw(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SCREW.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # AXIS
                test_text.extend([(" Axis ", setting, text_size),
                                  (str(mod.axis), value, text_size)])

                # AXIS OBJECT
                if mod.object:
                    test_text.extend([(" Axis Object ", setting, text_size),
                                      (str(mod.object.name), value, text_size)])

                # SCREW
                test_text.extend([(" Screw ", setting, text_size),
                                  (str(round(mod.screw_offset, 2)), value, text_size), (units, value, text_size)])

                # ITERATIONS
                test_text.extend([(" Iterations ", setting, text_size),
                                  (str(round(mod.iterations, 2)), value, text_size)])

                # Angle
                test_text.extend([(" Angle ", setting, text_size),
                                  (str(round(math.degrees(mod.angle), 1)), value, text_size),
                                  ("°", value, text_size)])

                # STEPS
                test_text.extend([(" Steps ", setting, text_size),
                                  (str(round(mod.steps, 2)), value, text_size)])

                # OPTIONS LINE 1
                if any([mod.use_normal_flip, mod.use_smooth_shade, mod.use_object_screw_offset,
                        mod.use_normal_calculate]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # USE FLIP
                    if mod.use_normal_flip:
                        test_text.extend([(" Flip ", setting, text_size)])

                    # USE SMOOTH SHADE
                    if mod.use_smooth_shade:
                        test_text.extend([(" Smooth Shading ", setting, text_size)])

                    # USE OBJECT SCREW OFFSET
                    # if mod.object:
                    if mod.use_object_screw_offset:
                        test_text.extend([(" Object Screw ", setting, text_size)])

                    # CALC ORDER
                    if mod.use_normal_calculate:
                        test_text.extend([(" Calc Order ", setting, text_size)])

                # OPTIONS LINE 2
                if any([mod.use_merge_vertices, mod.use_stretch_u, mod.use_stretch_v]):
                    test_text.extend([CR, ("----", title_var, text_size)])
                    # USE MERGE VERTICES
                    if mod.use_merge_vertices:
                        test_text.extend([(" Merge Vertices ", setting, text_size),
                                          (str(round(mod.merge_threshold, 2)), value, text_size), (units, value, text_size)])

                    # STRETCH U
                    if mod.use_stretch_u:
                        test_text.extend([(" Stretch U ", setting, text_size)])

                    # STRETCH V
                    if mod.use_stretch_v:
                        test_text.extend([(" Stretch V ", setting, text_size)])
        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# SKIN
# ---------------------------------------------------------------


def mod_skin(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SKIN.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # BRANCH SMOOTHING
                if mod.branch_smoothing != 0:
                    test_text.extend([(" Branch Smoothing ", setting, text_size),
                                      (str(round(mod.branch_smoothing, 3)), value, text_size)])

                if any([mod.use_x_symmetry, mod.use_y_symmetry, mod.use_z_symmetry]):
                    # SYMMETRY
                    test_text.extend([(" Symmetry ", setting, text_size)])

                    # X
                    if mod.use_x_symmetry:
                        test_text.extend([(" X ", value, text_size)])

                    # Y
                    if mod.use_y_symmetry:
                        test_text.extend([(" Y ", value, text_size)])

                    # Z
                    if mod.use_z_symmetry:
                        test_text.extend([(" Z ", value, text_size)])

                # OPTIONS
                if any([mod.use_smooth_shade]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # SMOOTH SHADING
                    if mod.use_smooth_shade:
                        test_text.extend([(" Smooth Shading ", setting, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# SOLIDIFY
# ---------------------------------------------------------------


def mod_solidify(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SOLIDIFY.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # THICKNESS
                test_text.extend([(" Thickness ", setting, text_size),
                                  (str(round(mod.thickness, 3)), value, text_size), (units, value, text_size)])

                # OFFSET
                test_text.extend([(" Offset ", setting, text_size),
                                  (str(round(mod.offset, 2)), value, text_size)])

                # CLAMP
                if mod.thickness_clamp != 0:
                    test_text.extend([(" Clamp ", setting, text_size),
                                      (str(round(mod.thickness_clamp, 2)), value, text_size)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([(" VGroup ", setting, text_size),
                                      (str(mod.vertex_group), value, text_size)])

                    # THICKNESS VGROUP
                    test_text.extend([(" Clamp ", setting, text_size),
                                      (str(round(mod.thickness_vertex_group, 2)), value, text_size)])

                # OPTIONS LIGNE 1
                if any([mod.use_flip_normals, mod.use_even_offset, mod.use_quality_normals, mod.use_rim]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # FLIP NORMALS
                    if mod.use_flip_normals:
                        test_text.extend([(" Flip Normals ", setting, text_size)])

                    # USE EVEN OFFSET
                    if mod.use_even_offset:
                        test_text.extend([(" Even Thickness ", setting, text_size)])

                    # HIGH QUALITY NORMALS
                    if mod.use_quality_normals:
                        test_text.extend([(" High Quality Normals ", setting, text_size)])

                    # USE RIM
                    if mod.use_rim:
                        test_text.extend([(" Fill Rim ", setting, text_size)])

                        # ONLY RIM
                        if mod.use_rim_only:
                            test_text.extend([(" Only rims ", setting, text_size)])

                # OPTIONS LIGNE 2
                if any([mod.edge_crease_inner, mod.edge_crease_outer, mod.edge_crease_rim]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # INNER
                    if mod.edge_crease_inner != 0:
                        test_text.extend([(" Inner ", setting, text_size),
                                          (str(round(mod.edge_crease_inner, 2)), value, text_size)])

                    # OUTER
                    if mod.edge_crease_outer != 0:
                        test_text.extend([(" Outer ", setting, text_size),
                                          (str(round(mod.edge_crease_outer, 2)), value, text_size)])

                    # RIM
                    if mod.edge_crease_rim != 0:
                        test_text.extend([(" Rim ", setting, text_size),
                                          (str(round(mod.edge_crease_rim, 2)), value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# SUBSURF
# ---------------------------------------------------------------


def mod_subsurf(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SUBSURF.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # VIEW
                test_text.extend([(" View ", setting, text_size),
                                  (str(mod.levels), value, text_size)])

                # RENDER
                test_text.extend([(" Render ", setting, text_size),
                                  (str(mod.render_levels), value, text_size)])

                # OPTIONS
                # if any([mod.use_subsurf_uv, mod.show_only_control_edges, mod.use_opensubdiv]):
                if any([mod.use_subsurf_uv, mod.show_only_control_edges]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # UV's
                    if mod.use_subsurf_uv:
                        test_text.extend([(" UV's ", setting, text_size)])

                    # OPTIMAL DISPLAY
                    if mod.show_only_control_edges:
                        test_text.extend([(" Optimal Display ", setting, text_size)])

                    # OPEN SUBDIV
                    # if (hasattr(bpy.context.preferences.system, 'opensubdiv_compute_type')):
                    #     if mod.use_opensubdiv:
                    #         test_text.extend([(" Open Subdiv ", setting, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# TRIANGULATE
# ---------------------------------------------------------------


def mod_triangulate(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_TRIANGULATE.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # VIEW
                test_text.extend([("  ", setting, text_size),
                                  (str(mod.quad_method.lower().capitalize()), value, text_size)])

                # RENDER
                test_text.extend([("  ", setting, text_size),
                                  (str(mod.ngon_method.lower().capitalize()), value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# WIREFRAME
# ---------------------------------------------------------------


def mod_wireframe(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_WIREFRAME.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # THICKNESS
                test_text.extend([(" Thickness ", setting, text_size),
                                  (str(round(mod.thickness, 3)), value, text_size)])

                # OFFSET
                test_text.extend([(" Offset ", setting, text_size),
                                  (str(round(mod.offset, 2)), value, text_size)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([(" VGroup ", setting, text_size),
                                      (str(mod.vertex_group), value, text_size)])

                    # THICKNESS VERTEX GROUP
                    test_text.extend([(" Factor ", setting, text_size),
                                      (str(round(mod.thickness_vertex_group, 2)), value, text_size)])
                # CREASE WEIGHT
                if mod.use_crease:
                    test_text.extend([(" Crease Weight ", setting, text_size),
                                      (str(round(mod.crease_weight, 2)), value, text_size)])

                # OPTIONS
                if any([mod.use_even_offset, mod.use_relative_offset, mod.use_replace, mod.use_boundary, mod.material_offset]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # EVEN THICKNESS
                    if mod.use_even_offset:
                        test_text.extend([(" Even Thickness ", setting, text_size)])

                    # RELATIVE THICKNESS
                    if mod.use_relative_offset:
                        test_text.extend([(" Relative Thickness ", setting, text_size)])

                    # BOUNDARY
                    if mod.use_boundary:
                        test_text.extend([(" Boundary ", setting, text_size)])

                    # REPLACE ORIGINAL
                    if mod.use_replace:
                        test_text.extend([(" Replace Original ", setting, text_size)])

                    # MATERIAL OFFSET
                    if mod.material_offset:
                        test_text.extend([(" Material Offset ", setting, text_size),
                                          (str(mod.material_offset), value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ----------------------------------------------------------------------------------------------------------------------
# MODIFIERS DEFORM -----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------
# ARMATURE
# ---------------------------------------------------------------


def mod_armature(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_ARMATURE.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                if mod.object:
                    # START
                    test_text.extend([(" Object ", setting, text_size),
                                      (str(mod.object.name), value, text_size)])
                else:
                    test_text.extend([(" No Armature Selected ", hidden, text_size)])

                # VERTEX GROUP
                if mod.use_vertex_groups:
                    test_text.extend([(" VGroup ", setting, text_size)])
                    if mod.vertex_group:
                        test_text.extend([(str(mod.vertex_group), value, text_size)])
                    else:
                        test_text.extend([(" No Vertex Group Selected ", hidden, text_size)])

                # OPTIONS
                if any([mod.use_deform_preserve_volume, mod.use_bone_envelopes, mod.use_multi_modifier]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # PRESERVE VOLUME
                    if mod.use_deform_preserve_volume:

                        test_text.extend([(" Preserve Volume ", setting, text_size)])

                    # BONE ENVELOPES
                    if mod.use_bone_envelopes:
                        test_text.extend([(" Bone Enveloppes ", setting, text_size)])

                    # MULTI MODIFIER
                    if mod.use_multi_modifier:
                        test_text.extend([(" Multi Modifier ", setting, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# CAST
# ---------------------------------------------------------------


def mod_cast(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_CAST.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # CAST TYPE
                test_text.extend([(" Type ", setting, text_size), (str(
                    mod.cast_type.lower().capitalize()), value, text_size)])

                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    test_text.extend([(" Axis ", setting, text_size)])

                    if mod.use_x:
                        test_text.extend([(" X ", value, text_size)])

                    if mod.use_y:
                        test_text.extend([(" Y ", value, text_size)])

                    if mod.use_z:
                        test_text.extend([(" Z ", value, text_size)])

                else:
                    test_text.extend([(" No Axis Selected ", hidden, text_size)])

                # FACTOR
                test_text.extend([(" Factor ", setting, text_size),
                                  (str(round(mod.factor, 2)), value, text_size)])

                # RADIUS
                if mod.radius != 0:
                    test_text.extend([(" Radius ", setting, text_size),
                                      (str(round(mod.radius, 2)), value, text_size), (units, value, text_size)])

                # SIZE
                if mod.size != 0:
                    test_text.extend([(" Size ", setting, text_size),
                                      (str(round(mod.size, 2)), value, text_size)])

                # OPTIONS
                if any([mod.use_radius_as_size, mod.vertex_group, mod.object, mod.use_transform]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", setting, text_size),
                                          (mod.vertex_group, value, text_size)])

                    # FROM RADIUS
                    if mod.use_radius_as_size:
                        test_text.extend([(" From Radius ", setting, text_size)])

                    # OBJECT
                    if mod.object:
                        test_text.extend([(" Control Object ", setting, text_size),
                                          (mod.object.name, value, text_size)])

                    # USE TRANSFORM
                    if mod.use_transform:
                        test_text.extend([(" Use Transform ", setting, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# CORRECTIVE SMOOTH
# ---------------------------------------------------------------


def mod_corrective_smooth(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # FACTOR
                test_text.extend([(" Factor ", setting, text_size),
                                  (str(round(mod.factor, 2)), value, text_size)])

                # ITERATIONS
                test_text.extend([(" Repeat ", setting, text_size),
                                  (str(mod.iterations), value, text_size)])

                # SMOOTH TYPE
                test_text.extend([(" Smooth Type ", setting, text_size), (str(
                    mod.smooth_type.lower().capitalize()), setting, text_size)])

                # OPTIONS
                if any([mod.use_only_smooth, mod.vertex_group, mod.use_pin_boundary, mod.rest_source]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", setting, text_size),
                                          (mod.vertex_group, value, text_size)])

                    # ONLY SMOOTH
                    if mod.use_only_smooth:
                        test_text.extend([(" Only Smooth ", setting, text_size)])

                    # PIN BOUNDARIES
                    if mod.use_pin_boundary:
                        test_text.extend([(" Pin Boundaries ", setting, text_size)])

                    # OBJECT
                    test_text.extend([(" Rest Sources ", setting, text_size),
                                      (mod.rest_source.lower().capitalize(), value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# CURVE
# ---------------------------------------------------------------


def mod_curve(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_CURVE.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # OBJECT
                if mod.object:
                    test_text.extend([(" Object ", setting, text_size),
                                      (mod.object.name, value, text_size)])
                else:
                    test_text.extend([(" No Object Selected ", hidden, text_size)])

                # DEFORM AXIS
                test_text.extend([(" Deformation Axis ", setting, text_size)])
                if mod.deform_axis == 'POS_X':
                    test_text.extend([(" X ", value, text_size)])

                elif mod.deform_axis == 'POS_Y':
                    test_text.extend([(" Y ", value, text_size)])

                elif mod.deform_axis == 'POS_Z':
                    test_text.extend([(" Z ", value, text_size)])

                elif mod.deform_axis == 'NEG_X':
                    test_text.extend([(" -X ", value, text_size)])

                elif mod.deform_axis == 'NEG_Y':
                    test_text.extend([(" -Y ", value, text_size)])

                elif mod.deform_axis == 'NEG_Z':
                    test_text.extend([(" -Z ", value, text_size)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([CR, ("----", title_var, text_size)])
                    test_text.extend([(" VGroup ", setting, text_size),
                                      (str(mod.vertex_group), value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# DISPLACE
# ---------------------------------------------------------------


def mod_displace(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_DISPLACE.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # MID LEVEL
                test_text.extend([(" Mid Level ", setting, text_size),
                                  (str(round(mod.mid_level, 2)), value, text_size)])

                # STRENGTH
                test_text.extend([(" Strength ", setting, text_size),
                                  (str(round(mod.strength, 2)), value, text_size)])

                # DIRECTION
                test_text.extend([(" Direction ", setting, text_size), (str(
                    mod.direction.lower().capitalize()), value, text_size)])
                if mod.direction in ['RGB_TO_XYZ', 'X', 'Y', 'Z']:
                    # DIRECTION
                    test_text.extend([(" Space ", setting, text_size), (str(
                        mod.space.lower().capitalize()), value, text_size)])

                # # OPTIONS
                # if any([mod.vertex_group]):
                #     test_text.extend([CR, ("----", title_var, text_size)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([CR, ("----", title_var, text_size)])
                    test_text.extend([(" VGroup ", setting, text_size),
                                      (str(mod.vertex_group), value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# HOOK
# ---------------------------------------------------------------


def mod_hook(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_HOOK.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # OBJECT
                if mod.object:
                    test_text.extend([(" Object ", setting, text_size),
                                      (mod.object.name, value, text_size)])
                else:
                    test_text.extend([(" No Object Selected ", hidden, text_size)])

                # RADIUS
                if mod.falloff_type != 'NONE':
                    if mod.falloff_radius != 0:
                        test_text.extend([(" Radius ", setting, text_size),
                                          (str(round(mod.falloff_radius, 2)), value, text_size), (units, value, text_size)])

                # STRENGTH
                test_text.extend([(" Strength ", setting, text_size),
                                  (str(round(mod.strength, 2)), value, text_size)])

                # OPTIONS
                test_text.extend([CR, ("----", title_var, text_size)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([(" VGroup ", setting, text_size),
                                      (mod.vertex_group, value, text_size)])

                # FALLOF TYPE
                test_text.extend([(" Fallof Type ", setting, text_size),
                                  (str(mod.falloff_type.upper()), value, text_size)])

                # UNIFORM FALLOFF
                if mod.use_falloff_uniform:
                    test_text.extend([(" Uniform Falloff ", setting, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# LAPLACIAN DEFORMER
# ---------------------------------------------------------------


def mod_laplacian_deformer(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # ITERATIONS
                test_text.extend([(" Repeat ", setting, text_size),
                                  (str(mod.iterations), value, text_size)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([(" VGroup ", setting, text_size),
                                      (str(mod.vertex_group), value, text_size)])
                else:
                    test_text.extend([(" No VGroup Selected ", hidden, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# LAPLACIAN SMOOTH
# ---------------------------------------------------------------


def mod_laplacian_smooth(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    test_text.extend([(" Axis ", setting, text_size)])

                    if mod.use_x:
                        test_text.extend([(" X ", value, text_size)])

                    if mod.use_y:
                        test_text.extend([(" Y ", value, text_size)])

                    if mod.use_z:
                        test_text.extend([(" Z ", value, text_size)])
                else:
                    test_text.extend([(" No Axis Selected ", hidden, text_size)])

                # FACTOR
                test_text.extend([(" Factor ", setting, text_size),
                                  (str(round(mod.lambda_factor, 2)), value, text_size)])

                # BORDER
                test_text.extend([(" Border ", setting, text_size),
                                  (str(round(mod.lambda_border, 2)), value, text_size)])

                # OPTIONS
                if any([mod.use_volume_preserve, mod.use_normalized, mod.vertex_group]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # PRESERVE VOLUME
                    if mod.use_volume_preserve:
                        test_text.extend([(" Preserve Volume ", setting, text_size)])

                    # NORMALIZED
                    if mod.use_normalized:
                        test_text.extend([(" Normalized ", setting, text_size)])

                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", setting, text_size),
                                          (mod.vertex_group, value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# MESH DEFORM
# ---------------------------------------------------------------


def mod_mesh_deform(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # OBJECT
                if mod.object:
                    test_text.extend([(" Object ", setting, text_size),
                                      (mod.object.name, value, text_size)])
                else:
                    test_text.extend([(" No Object Selected ", hidden, text_size)])

                # PRECISION
                test_text.extend([(" Precision ", setting, text_size),
                                  (str(mod.precision), value, text_size)])

                # OPTIONS
                if any([mod.use_dynamic_bind, mod.vertex_group]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", setting, text_size),
                                          (str(mod.vertex_group), value, text_size)])

                    # USE DYNAMIC BIND
                    if mod.use_dynamic_bind:
                        test_text.extend([(" Dynamic ", setting, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# SIMPLE DEFORM
# ---------------------------------------------------------------


def mod_simple_deform(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SIMPLEDEFORM.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:

                test_text.extend([(" ", setting, text_size), (str(mod.deform_method.upper()), value, text_size)])

                # ORIGIN
                if mod.origin:
                    test_text.extend([(" Axis,Origin ", setting, text_size),
                                      (str(mod.origin.name), value, text_size)])

                # ANGLE/FACTOR
                if mod.deform_method in ['TWIST', 'BEND']:
                    # Angle
                    test_text.extend([(" Angle ", setting, text_size),
                                      (str(round(math.degrees(mod.factor), 1)), value, text_size),
                                      ("°", value, text_size)])

                elif mod.deform_method in ['TAPER', 'STRETCH']:
                    test_text.extend([(" Factor ", setting, text_size),
                                      (str(round(mod.factor, 2)), value, text_size)])

                # OPTIONS
                test_text.extend([CR, ("----", title_var, text_size)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([(" VGroup ", setting, text_size),
                                      (str(mod.vertex_group), value, text_size)])

                # LOCK
                if mod.deform_method != 'BEND':
                    if any([mod.lock_x, mod.lock_y]):
                        test_text.extend([(" Lock ", setting, text_size)])

                        if mod.lock_x:
                            test_text.extend([(" X ", value, text_size)])

                        if mod.lock_y:
                            test_text.extend([(" Y ", value, text_size)])

                # LIMIT
                test_text.extend([(" Limit ", setting, text_size)])

                test_text.extend([(str(round(mod.limits[0], 2)), value, text_size)])

                test_text.extend([(" ", setting, text_size), (str(round(mod.limits[1], 2)), value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# SHRINKWRAP
# ---------------------------------------------------------------


def mod_shrinkwrap(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SHRINKWRAP.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])

        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # TARGET
                if mod.target:
                    test_text.extend([(" Target ", setting, text_size),
                                      (str(mod.target.name), value, text_size)])
                else:
                    test_text.extend([(" No Target Selected ", hidden, text_size)])

                # OFFSET
                test_text.extend([(" Offset ", setting, text_size),
                                  (str(round(mod.offset, 2)), value, text_size)])

                # VERTEX GROUP
                if mod.vertex_group:
                    test_text.extend([(" VGroup ", setting, text_size),
                                      (str(mod.vertex_group), value, text_size)])

                test_text.extend([CR, ("----", title_var, text_size)])

                # NEAREST SURFACEPOINT
                if mod.wrap_method == 'NEAREST_SURFACEPOINT':
                    # MODE
                    test_text.extend([(" Mode ", setting, text_size),
                                      (str(mod.wrap_method.lower().capitalize()), value, text_size)])

                    # KEEP ABOVE SURFACE
                    if mod.use_keep_above_surface:
                        test_text.extend([(" Keep Above Surface ", setting, text_size)])

                # PROJECT
                elif mod.wrap_method == 'PROJECT':
                    # MODE
                    test_text.extend([(" Mode ", setting, text_size),
                                      (str(mod.wrap_method.lower().capitalize()), value, text_size)])

                    # AXIS
                    if any([mod.use_project_x, mod.use_project_y, mod.use_project_z]):
                        test_text.extend([(" Axis ", setting, text_size)])
                        # X
                        if mod.use_project_x:
                            test_text.extend([(" X ", value, text_size)])
                        # Y
                        if mod.use_project_y:
                            test_text.extend([(" Y ", value, text_size)])
                        # Z
                        if mod.use_project_z:
                            test_text.extend([(" Z ", value, text_size)])

                    # LEVELS
                    test_text.extend([(" Subsurf Levels ", setting, text_size),
                                      (str(mod.subsurf_levels), value, text_size)])

                    # PROJECT LIMIT
                    test_text.extend([(" Limit ", setting, text_size),
                                      (str(round(mod.project_limit, 2)), value, text_size)])

                    test_text.extend([CR, ("----", title_var, text_size)])

                    # DIRECTION
                    if mod.use_negative_direction:
                        test_text.extend([(" Negative ", setting, text_size)])

                    if mod.use_positive_direction:
                        test_text.extend([(" Positive ", setting, text_size)])

                    # MODE
                    test_text.extend([(" Cull Face ", setting, text_size),
                                      (str(mod.cull_face.lower().capitalize()), value, text_size)])
                    # AUXILIARY TARGET
                    if mod.auxiliary_target:
                        test_text.extend([(" Auxiliary Target ", setting, text_size),
                                          (mod.auxiliary_target.name, value, text_size)])
                else:
                    # MODE
                    test_text.extend([(" Mode ", setting, text_size),
                                      (str(mod.wrap_method.lower().capitalize()), value, text_size)])
        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# SMOOTH
# ---------------------------------------------------------------


def mod_smooth(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_SMOOTH.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # TYPE
                if any([mod.use_x, mod.use_y, mod.use_z]):
                    test_text.extend([(" Axis ", setting, text_size)])

                    if mod.use_x:
                        test_text.extend([(" X ", value, text_size)])

                    if mod.use_y:
                        test_text.extend([(" Y ", value, text_size)])

                    if mod.use_z:
                        test_text.extend([(" Z ", value, text_size)])
                else:
                    test_text.extend([(" No Axis Selected ", hidden, text_size)])

                # FACTOR
                test_text.extend([(" Factor ", setting, text_size),
                                  (str(round(mod.factor, 2)), value, text_size)])

                # ITERATIONS
                test_text.extend([(" Repeat ", setting, text_size),
                                  (str(mod.iterations), value, text_size)])

                # OPTIONS
                if mod.vertex_group:
                    test_text.extend([CR, ("----", title_var, text_size)])
                    test_text.extend([(" VGroup ", setting, text_size),
                                      (mod.vertex_group, value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# SURFACE DEFORM
# ---------------------------------------------------------------


def mod_surface_deform(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_MESHDEFORM.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # TARGET
                if mod.target:
                    test_text.extend([(" Target ", setting, text_size),
                                      (str(mod.target.name), value, text_size)])
                else:
                    test_text.extend([(" No Target Selected ", hidden, text_size)])

                # FALLOFF
                test_text.extend([(" Interpolation Falloff ", setting, text_size),
                                  (str(round(mod.falloff, 2)), value, text_size)])
        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# WARP
# ---------------------------------------------------------------


def mod_warp(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_WARP.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                # FROM
                if mod.object_from:
                    test_text.extend([(" From ", setting, text_size),
                                      (str(mod.object_from.name), value, text_size)])

                else:
                    test_text.extend([(" No Object From ", hidden, text_size)])

                # TO
                if mod.object_to:
                    test_text.extend([(" To ", setting, text_size),
                                      (str(mod.object_to.name), value, text_size)])
                else:
                    test_text.extend([(" No Object To ", hidden, text_size)])

                # STRENGTH
                test_text.extend([(" Strength ", setting, text_size),
                                  (str(round(mod.strength, 2)), value, text_size)])

                # RADIUS
                if mod.falloff_type != 'NONE':
                    if mod.falloff_radius != 0:
                        test_text.extend([(" Radius ", setting, text_size),
                                          (str(round(mod.falloff_radius, 2)), value, text_size), (units, value, text_size)])

                # OPTIONS
                if any([mod.vertex_group, mod.use_volume_preserve, mod.texture_coords]):
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", setting, text_size),
                                          (str(mod.vertex_group), value, text_size)])

                    # OFFSET
                    if mod.use_volume_preserve:
                        test_text.extend([(" Preserve Volume ", setting, text_size)])

                    # TEXTURES COORD
                    test_text.extend([(" Texture Coords ", setting, text_size),
                                      (str(mod.texture_coords.lower().capitalize()), value, text_size)])

                    # OBJECT
                    if mod.texture_coords == "OBJECT":
                        if mod.texture_coords_object:
                            test_text.extend([(" Object ", setting, text_size),
                                              (str(mod.texture_coords_object.name), value, text_size)])
                        else:
                            test_text.extend([(" No Object Selected ", hidden, text_size)])

                    # UVs
                    if mod.texture_coords == "UV":
                        if mod.uv_layer:
                            test_text.extend([(" UVMap ", setting, text_size),
                                              (str(mod.uv_layer), value, text_size)])
                        else:
                            test_text.extend([(" No UV's Selected ", hidden, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ---------------------------------------------------------------
# WAVE
# ---------------------------------------------------------------


def mod_wave(test_text, mod, CR, title_var, setting, value, text_size, hidden, option, units, space, simple_text_mode):
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        # NAME
        # test_text.extend([CR, ('ICON', 'ICON_MOD_WAVE.png'), ("    ", setting, text_size),
        #                   (str(mod.name.upper()), title_var, text_size)])
        test_text.extend([CR, (str(mod.name.upper()), title_var, text_size)])

        if mod.show_viewport:
            if not simple_text_mode:
                if any([mod.use_x, mod.use_y, mod.use_cyclic]):
                    test_text.extend([(" Motion ", setting, text_size)])

                    if mod.use_x:
                        test_text.extend([(" X ", value, text_size)])

                    if mod.use_y:
                        test_text.extend([(" Y ", value, text_size)])

                    if mod.use_cyclic:
                        test_text.extend([(" Cyclic ", value, text_size)])

                if mod.use_normal:
                    if any([mod.use_normal_x, mod.use_normal_y, mod.use_normal_z]):
                        test_text.extend([(" Normals ", setting, text_size)])

                        if mod.use_normal_x:
                            test_text.extend([(" X ", value, text_size)])

                        if mod.use_normal_y:
                            test_text.extend([(" Y ", value, text_size)])

                        if mod.use_normal_z:
                            test_text.extend([(" Z ", value, text_size)])

                # TIME
                test_text.extend([(" Time ", setting, text_size)])

                # OFFSET
                test_text.extend([(" Offset ", setting, text_size),
                                  (str(round(mod.time_offset, 2)), value, text_size)])
                # LIFE
                test_text.extend([(" Life ", setting, text_size),
                                  (str(round(mod.lifetime, 2)), value, text_size)])
                # DAMPING
                test_text.extend([(" Damping ", setting, text_size),
                                  (str(round(mod.damping_time, 2)), value, text_size)])

                if any([mod.start_position_x, mod.start_position_y, mod.falloff_radius]) != 0:
                    test_text.extend([CR, ("----", title_var, text_size)])
                    # TIME
                    test_text.extend([(" Position ", setting, text_size)])

                    # POS X
                    test_text.extend([(" X ", setting, text_size),
                                      (str(round(mod.start_position_x, 2)), value, text_size), (units, value, text_size)])

                    # POS Y
                    test_text.extend([(" Y ", setting, text_size),
                                      (str(round(mod.start_position_y, 2)), value, text_size), (units, value, text_size)])

                    # FALLOFF
                    test_text.extend([(" Y ", setting, text_size),
                                      (str(round(mod.falloff_radius, 2)), value, text_size), (units, value, text_size)])

                if any([mod.start_position_object, mod.vertex_group, mod.texture_coords]) != 0:
                    test_text.extend([CR, ("----", title_var, text_size)])

                    # FROM
                    if mod.start_position_object:
                        test_text.extend([(" From ", setting, text_size),
                                          (str(mod.start_position_object.name), value, text_size)])

                    # VERTEX GROUP
                    if mod.vertex_group:
                        test_text.extend([(" VGroup ", setting, text_size),
                                          (str(mod.vertex_group), value, text_size)])

                    # TEXTURES COORD
                    test_text.extend([(" Texture Coords ", setting, text_size),
                                      (str(mod.texture_coords.lower().capitalize()), value, text_size)])

                    # OBJECT
                    if mod.texture_coords == "OBJECT":
                        if mod.texture_coords_object:
                            test_text.extend([(" Object ", setting, text_size),
                                              (str(mod.texture_coords_object.name), value, text_size)])
                        else:
                            test_text.extend([(" No Object Selected ", hidden, text_size)])

                    # UVs
                    if mod.texture_coords == "UV":
                        if mod.uv_layer:
                            test_text.extend([(" UVMap ", setting, text_size),
                                              (str(mod.uv_layer), value, text_size)])
                        else:
                            test_text.extend([(" No UV's Selected ", hidden, text_size)])

                test_text.extend([CR, ("----", title_var, text_size)])

                # SPEED
                test_text.extend([(" Speed ", setting, text_size),
                                  (str(round(mod.speed, 2)), value, text_size)])

                # SPEED
                test_text.extend([(" Height ", setting, text_size),
                                  (str(round(mod.height, 2)), value, text_size), (units, value, text_size)])

                # SPEED
                test_text.extend([(" Width ", setting, text_size),
                                  (str(round(mod.width, 2)), value, text_size), (units, value, text_size)])

                # SPEED
                test_text.extend([(" Narrowness ", setting, text_size),
                                  (str(round(mod.narrowness, 2)), value, text_size), (units, value, text_size)])

        else:
            test_text.extend([(" Hidden ", hidden, text_size)])

# ----------------------------------------------------------------------------------------------------------------------
# OBJECTS --------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------
# ARMATURE
# ---------------------------------------------------------------


def armature(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space):
    obj = bpy.context.active_object
    active_bone = bpy.context.active_bone

    # BONE SELECTED
    if bpy.context.object.mode in {'POSE', 'EDIT'}:
        test_text.extend([CR, ("BONE SELECTED ", title_var, text_size), (active_bone.name, value, text_size)])

# ---------------------------------------------------------------
# CAMERA
# ---------------------------------------------------------------


def camera(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space):
    obj = bpy.context.active_object

    # LENS
    test_text.extend([CR, ("LENS ", title_var, text_size),
                      (str(round(obj.data.lens, 2)), value, text_size)])
    # FOCUS
    if bpy.context.object.data.dof.use_dof and bpy.context.object.data.dof.focus_object:

        test_text.extend([CR, ("FOCUS ", title_var, text_size),
                          (str(obj.dof.focus_object.name), value, text_size)])

    else:
        test_text.extend([CR, ("DISTANCE ", title_var, text_size),
                          (str(round(obj.data.dof.focus_distance, 2)), value, text_size)])

    # RADIUS / FSTOP
    # if bpy.context.object.data.cycles.aperture_type == 'RADIUS': bpy.context.object.data.dof.focus_object = None
    #     if obj.data.cycles.aperture_size:
    #         test_text.extend([CR, ("RADIUS ", title_var, text_size),
    #                       (str(round(obj.data.cycles.aperture_size, 2)), value,
    #                        text_size)])

    if bpy.context.object.data.dof.use_dof:

        test_text.extend([CR, ("FSTOP ", title_var, text_size),
                          (str(round(obj.data.cycles.aperture_fstop, 2)), value,
                           text_size)])

# ---------------------------------------------------------------
# CURVE / FONT
# ---------------------------------------------------------------


def curve_font(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space):
    obj = bpy.context.active_object

    # PREVIEW U
    test_text.extend([CR, ("Preview U ", title_var, text_size), (str(obj.data.resolution_u), value, text_size)])

    # RENDER PREVIEW U
    test_text.extend([(" Render U ", title_var, text_size), (str(obj.data.render_resolution_u), value, text_size)])

    # FILL MODE
    test_text.extend([CR, ("FILL ", title_var, text_size), (str(
        obj.data.fill_mode.lower().capitalize()), value, text_size)])

    # OFFSET
    if obj.data.offset:
        test_text.extend(
            [CR, ("Offset ", title_var, text_size), (str(round(obj.data.offset, 2)), value, text_size)])

    # DEPTH
    if obj.data.bevel_depth:
        test_text.extend([CR, ("DEPTH ", title_var, text_size),
                          (str(round(obj.data.bevel_depth, 2)), value, text_size)])

    # EXTRUDE
    if obj.data.extrude:
        test_text.extend([CR, ("EXTRUDE ", title_var, text_size),
                          (str(round(obj.data.extrude, 2)), value, text_size)])

    # RESOLUTION
    if obj.data.bevel_resolution:
        test_text.extend([CR, ("RESOLUTION ", title_var, text_size),
                          (str(obj.data.bevel_resolution), value, text_size)])
    # BEVEL
    if obj.data.bevel_object:
        test_text.extend([CR, ("BEVEL ", title_var, text_size),
                          (obj.data.bevel_object.name, value, text_size)])

    # TAPER
    if obj.data.taper_object:
        test_text.extend([CR, ("TAPER ", title_var, text_size),
                          (obj.data.taper_object.name, value, text_size)])

# ---------------------------------------------------------------
# EMPTY
# ---------------------------------------------------------------


def empty(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space):
    obj = bpy.context.active_object

    # ICON_OUTLINER_OB_EMPTY
    # TYPE
    test_text.extend([("TYPE ", title_var, text_size),
                      (str(obj.empty_display_type.lower().capitalize()), value, text_size)])

    # SIZE
    test_text.extend([CR, ("SIZE ", title_var, text_size), (str(round(obj.empty_display_size, 2)), value, text_size)])

# ---------------------------------------------------------------
# LATTICE
# ---------------------------------------------------------------


def text_lattice(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space):
    obj = bpy.context.active_object

# U -----------------------------------------------------------------------
    test_text.extend([CR, ("U  ", title_var, text_size),
                      (str(obj.data.points_u), value, text_size)])

    # INTERPOLATION U
    test_text.extend([("  ", title_var, text_size),
                      (str(obj.data.interpolation_type_u.split("_")[-1]), setting, text_size)])

# V -----------------------------------------------------------------------
    test_text.extend([CR, ("V  ", title_var, text_size),
                      (str(obj.data.points_v), value, text_size)])

    # INTERPOLATION V
    test_text.extend([("  ", title_var, text_size), (
        str(obj.data.interpolation_type_v.split("_")[-1]), setting, text_size)])

# W -----------------------------------------------------------------------
    test_text.extend([CR, ("W ", title_var, text_size),
                      (str(obj.data.points_w), value,
                       text_size)])

    # INTERPOLATION W
    test_text.extend([("  ", title_var, text_size), (
        str(obj.data.interpolation_type_w.split("_")[-1]), setting, text_size)])

# ---------------------------------------------------------------
# LIGHTS
# ---------------------------------------------------------------


def cycles_lights(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space):
    obj = bpy.context.active_object

    # TYPE
    if obj.data.type == 'AREA':
        test_text.extend([CR, ("TYPE: ", title_var, text_size), ("AREA ", setting, text_size)])

        # SQUARE
        if obj.data.shape == 'SQUARE':
            test_text.extend([CR, ("SQUARE ", title_var, text_size)])
            test_text.extend([CR, ("SIZE ", title_var, text_size),
                              (str(round(obj.data.size, 2)), value, text_size)])
        # RECTANGLE
        elif obj.data.shape == 'RECTANGLE':
            # RECTANGLE
            test_text.extend([CR, ("RECTANGLE ", title_var, text_size)])
            # SIZE
            test_text.extend([CR, ("SIZE X ", title_var, text_size),
                              (str(round(obj.data.size, 2)), value, text_size)])
            # SIZE Y
            test_text.extend([CR, ("SIZE Y ", title_var, text_size),
                              (str(round(obj.data.size_y, 2)), value, text_size)])

    # POINT
    elif obj.data.type == 'POINT':
        test_text.extend([CR, ("TYPE: ", title_var, text_size), ("POINT ", setting, text_size)])

        # SIZE
        test_text.extend([CR, ("SIZE ", title_var, text_size),
                          (str(round(obj.data.shadow_soft_size, 2)), value, text_size)])

    # SUN
    elif obj.data.type == 'SUN':
        test_text.extend([CR, ("TYPE: ", title_var, text_size), ("SUN ", setting, text_size)])

        # SIZE
        test_text.extend([CR, ("SIZE ", title_var, text_size),
                          (str(round(obj.data.shadow_soft_size, 2)), value, text_size)])

    elif obj.data.type == 'SPOT':
        test_text.extend([CR, ("TYPE: ", title_var, text_size), ("SPOT ", setting, text_size)])
        # SIZE
        test_text.extend([CR, ("SIZE ", title_var, text_size),
                          (str(round(obj.data.shadow_soft_size, 2)), value, text_size)])
        # SHAPE
        test_text.extend([CR, ("SHAPE ", title_var, text_size), (
            str(round(math.degrees(obj.data.spot_size), 1)), value, text_size),
            ("°", value, text_size)])
        # BLEND
        test_text.extend([CR, ("SIZE ", title_var, text_size),
                          (str(round(obj.data.spot_blend, 2)), value, text_size)])

    # HEMI
    elif obj.data.type == 'HEMI':
        test_text.extend([CR, ("TYPE: ", title_var, text_size), ("HEMI ", setting, text_size)])
        # test_text.extend([("HEMI ", title_var, text_size),
        #                   (str(round(bpy.data.node_groups["Shader Nodetree"].nodes["Emission"].inputs[1].default_value, 2)), value, text_size)])

    # PORTAL
    if obj.data.cycles.is_portal:
        test_text.extend([CR, ("PORTAL", title_var, text_size)])

    else:
        # CAST SHADOW
        if obj.data.cycles.cast_shadow:
            test_text.extend([CR, ("CAST SHADOW ", setting, text_size)])
        # MULTIPLE IMPORTANCE
        if obj.data.cycles.use_multiple_importance_sampling:
            test_text.extend([CR, ("MULTIPLE IMPORTANCE", setting, text_size)])

# ---------------------------------------------------------------
# METABALL
# ---------------------------------------------------------------


def metaball(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space):
    obj = bpy.context.active_object

    # VIEW
    test_text.extend([CR, ("VIEW ", title_var, text_size), (str(round(obj.data.resolution, 2)), value, text_size)])

    # RENDER
    test_text.extend([CR, ("RENDER ", title_var, text_size),
                      (str(round(obj.data.render_resolution, 2)), value, text_size)])

    # THRESHOLD
    test_text.extend([CR, ("THRESHOLD ", title_var, text_size),
                      (str(round(obj.data.threshold, 2)), value, text_size)])

    # UPDATE
    test_text.extend([CR, ("UPDATE ", title_var, text_size),
                      (obj.data.update_method.split("_")[-1], value, text_size)])


# ---------------------------------------------------------------
# WARNING
# ---------------------------------------------------------------
def warning(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space):
    obj = bpy.context.active_object

    for mod in bpy.context.active_object.modifiers:
        if mod.type in ['BEVEL', 'SOLIDIFY']:
            if obj.scale[0] != obj.scale[2] or obj.scale[1] != obj.scale[0] or obj.scale[1] != obj.scale[2]:
                # test_text.extend(
                #     [CR,('ICON', 'ICON_ERROR.png'),("      Non-Uniform Scale will give bad results ", setting, text_size)])
                test_text.extend(
                    [CR, ("      Non-Uniform Scale will give bad results ", setting, text_size)])


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
    # show_object_name = get_addon_preferences().show_object_name
    show_loc_rot_scale = get_addon_preferences().show_loc_rot_scale
    show_modifiers = get_addon_preferences().show_modifiers
    show_object_info = get_addon_preferences().show_object_info
    simple_text_mode = get_addon_preferences().simple_text_mode
    # show_keymaps = get_addon_preferences().show_keymaps
    show_blender_keymaps = get_addon_preferences().show_blender_keymaps

    # TEXT OPTIONS
    hidden = get_addon_preferences().hidden
    title_var = get_addon_preferences().text_color
    setting = get_addon_preferences().text_color_1
    option = get_addon_preferences().option
    value = get_addon_preferences().text_color_2
    text_size_max = get_addon_preferences().text_size_max
    text_size_mini = get_addon_preferences().text_size_mini
    text_size = min(text_size_max, max(text_size_mini, int(bpy.context.area.width / 100)))
    text_size_deux = int(text_size_max * 1.5)
    space = int(text_size * 2)
    CR = "Carriage return"

    # HELP
    # if show_keymaps:
    #     keymaps(test_text, CR, title_var, setting, value, text_size, hidden, option, space)

    obj = bpy.context.object
    if obj is None:
        test_text.extend([("SELECTION", title_var, "Active object not found")])
        return test_text

    # MODE
    if show_object_mode:
        mode(test_text, CR, title_var, setting, value, text_size, hidden, option, text_size_deux, space)
        # SPACE
        test_text.extend([("SPACE", title_var, space)])

    # NAME
    # if show_object_name:
    #     name(test_text, CR, title_var, setting, value, text_size, hidden, option, space)
    #     # SPACE
    #     test_text.extend([("SPACE", title_var, space)])

    # LOCATION / ROTATION / SCALE
    if show_loc_rot_scale:
        loc(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space)

    # VERT/FACES/EDGES/NGONS
    if show_vert_face_tris:
        if obj.type == 'MESH':
            ngons(test_text, CR, title_var, value, text_size, space)
            # SPACE
            test_text.extend([("SPACE", title_var, space)])

    # MESH OPTIONS
    if show_object_info:
        # if bpy.context.object.mode in ['EDIT', 'OBJECT', 'WEIGHT_PAINT']:
        if obj.type in ['MESH', 'CURVE', 'FONT', 'LATTICE']:
            mesh_options(test_text, CR, title_var, setting, value, text_size, hidden, option, space)

    # SCULPT
    if bpy.context.object.type == 'MESH' and bpy.context.object.mode == 'SCULPT':
        sculpt(test_text, CR, title_var, setting, value, text_size, hidden, option, text_size_deux, units, space)
        # SPACE
        test_text.extend([("SPACE", title_var, space)])


# ----------------------------------------------------------------------------------------------------------------------
# OBJECTS --------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    # ARMATURE
    if obj.type == 'ARMATURE':
        armature(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space)
        # SPACE
        test_text.extend([("SPACE", title_var, space)])

    # CAMERA
    if obj.type == 'CAMERA':
        camera(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space)
        # SPACE
        test_text.extend([("SPACE", title_var, space)])

    # CURVES / FONT
    if obj.type in ['CURVE', 'FONT']:
        curve_font(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space)
        if obj.modifiers:
            # SPACE
            test_text.extend([CR, ("", title_var, space)])

    # EMPTY
    if obj.type == 'EMPTY':
        # SPACE
        test_text.extend([CR, ("", title_var, text_size)])
        empty(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space)
        # SPACE
        test_text.extend([("SPACE", title_var, space)])

    # LATTICE
    if obj.type == 'LATTICE':
        text_lattice(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space)
        # SPACE
        test_text.extend([("SPACE", title_var, space)])

    # LIGHT
    if obj.type == 'LAMP':
        cycles_lights(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space)
        # SPACE
        test_text.extend([("SPACE", title_var, space)])

    # METABALL
    if obj.type == 'META':
        metaball(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space)
        # SPACE
        test_text.extend([("SPACE", title_var, space)])

# ----------------------------------------------------------------------------------------------------------------------
# MODIFIERS ------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    wm = bpy.context.window_manager
    index = wm.sf_companion.active_modifier
    # index = infotext.active_modifier

    GREEN = (0.5, 1, 0, 1)
    NOIR = (0, 0, 0, 1)
    BLANC = (1, 1, 1, 1)

    index = -1
    if hasattr(wm, 'sf_companion') and hasattr(wm.sf_companion, 'active_modifier'):
        index = wm.sf_companion.active_modifier

    if show_modifiers:

        # for mod in bpy.context.active_object.modifiers:
        for i, mod in enumerate(bpy.context.object.modifiers):

            title_var = BLANC
            if i == index:
                title_var = GREEN

            if mod.type not in {'BEVEL', 'ARRAY', 'SUBSURF', 'LATTICE', 'BOOLEAN', 'MIRROR', 'SOLIDIFY',
                                'DECIMATE', 'EDGE_SPLIT', 'DISPLACE', 'MULTIRES', 'BUILD', 'ARMATURE',
                                'MASK', 'REMESH', 'TRIANGULATE', 'SHRINKWRAP', 'WIREFRAME', 'SKIN', 'SCREW',
                                'CURVE', 'MESH_DEFORM', 'LAPLACIANDEFORM', 'CAST', 'CORRECTIVE_SMOOTH',
                                'HOOK', 'LAPLACIANSMOOTH', 'SIMPLE_DEFORM', 'SMOOTH', 'SURFACE_DEFORM',
                                'WARP', 'WAVE', 'WEIGHTED_NORMAL'
                                }:

                # MODIFIER STILL NOT ADDED
                if mod.show_viewport:
                    test_text.extend([CR, (str(mod.type), title_var, text_size), ("  ", title_var, text_size),
                                      (str(mod.name), value, text_size)])
                else:
                    test_text.extend([CR, (str(mod.type), title_var, text_size), ("  ", title_var, text_size),
                                      (str(mod.name), value, text_size)])
                    test_text.extend([(" Hidden ", hidden, text_size)])

            # modifiers_list[mod]
            if mod.type == 'ARMATURE':
                mod_armature(test_text, mod, CR, title_var, setting, value,
                             text_size, hidden, option, space, simple_text_mode)

            if mod.type == 'ARRAY':
                mod_array(test_text, mod, CR, title_var, setting, value, text_size,
                          hidden, option, units, space, simple_text_mode)

            if mod.type == 'BEVEL':
                mod_bevel(test_text, mod, CR, title_var, setting, value, text_size,
                          hidden, option, units, space, simple_text_mode)

            if mod.type == 'BOOLEAN':
                mod_boolean(test_text, mod, CR, title_var, setting, value, text_size,
                            hidden, option, units, space, simple_text_mode)

            if mod.type == 'BUILD':
                mod_build(test_text, mod, CR, title_var, setting, value, text_size,
                          hidden, option, units, space, simple_text_mode)

            if mod.type == 'CAST':
                mod_cast(test_text, mod, CR, title_var, setting, value, text_size,
                         hidden, option, units, space, simple_text_mode)

            if mod.type == 'CORRECTIVE_SMOOTH':
                mod_corrective_smooth(test_text, mod, CR, title_var, setting, value, text_size,
                                      hidden, option, units, space, simple_text_mode)

            if mod.type == 'CURVE':
                mod_curve(test_text, mod, CR, title_var, setting, value, text_size,
                          hidden, option, units, space, simple_text_mode)

            if mod.type == 'DECIMATE':
                mod_decimate(test_text, mod, CR, title_var, setting, value, text_size,
                             hidden, option, units, space, simple_text_mode)

            if mod.type == 'DISPLACE':
                mod_displace(test_text, mod, CR, title_var, setting, value, text_size,
                             hidden, option, units, space, simple_text_mode)

            if mod.type == 'EDGE_SPLIT':
                mod_edge_split(test_text, mod, CR, title_var, setting, value, text_size,
                               hidden, option, units, space, simple_text_mode)

            if mod.type == 'HOOK':
                mod_hook(test_text, mod, CR, title_var, setting, value, text_size,
                         hidden, option, units, space, simple_text_mode)

            if mod.type == 'LAPLACIANDEFORM':
                mod_laplacian_deformer(test_text, mod, CR, title_var, setting, value, text_size,
                                       hidden, option, units, space, simple_text_mode)

            if mod.type == 'LAPLACIANSMOOTH':
                mod_laplacian_smooth(test_text, mod, CR, title_var, setting, value, text_size,
                                     hidden, option, units, space, simple_text_mode)

            if mod.type == 'LATTICE':
                mod_lattice(test_text, mod, CR, title_var, setting, value, text_size,
                            hidden, option, units, space, simple_text_mode)

            if mod.type == 'MASK':
                mod_mask(test_text, mod, CR, title_var, setting, value, text_size,
                         hidden, option, units, space, simple_text_mode)

            if mod.type == 'MESH_DEFORM':
                mod_mesh_deform(test_text, mod, CR, title_var, setting, value, text_size,
                                hidden, option, units, space, simple_text_mode)

            if mod.type == 'MIRROR':
                mod_mirror(test_text, mod, CR, title_var, setting, value, text_size,
                           hidden, option, units, space, simple_text_mode)

            if mod.type == 'MULTIRES':
                mod_multires(test_text, mod, CR, title_var, setting, value, text_size,
                             hidden, option, units, space, simple_text_mode)

            if mod.type == 'REMESH':
                mod_remesh(test_text, mod, CR, title_var, setting, value, text_size,
                           hidden, option, units, space, simple_text_mode)

            if mod.type == 'SCREW':
                mod_screw(test_text, mod, CR, title_var, setting, value, text_size,
                          hidden, option, units, space, simple_text_mode)

            if mod.type == 'SHRINKWRAP':
                mod_shrinkwrap(test_text, mod, CR, title_var, setting, value, text_size,
                               hidden, option, units, space, simple_text_mode)

            if mod.type == 'SIMPLE_DEFORM':
                mod_simple_deform(test_text, mod, CR, title_var, setting, value, text_size,
                                  hidden, option, units, space, simple_text_mode)

            if mod.type == 'SKIN':
                mod_skin(test_text, mod, CR, title_var, setting, value, text_size,
                         hidden, option, units, space, simple_text_mode)

            if mod.type == 'SMOOTH':
                mod_smooth(test_text, mod, CR, title_var, setting, value, text_size,
                           hidden, option, units, space, simple_text_mode)

            if mod.type == 'SOLIDIFY':
                mod_solidify(test_text, mod, CR, title_var, setting, value, text_size,
                             hidden, option, units, space, simple_text_mode)

            if mod.type == 'SUBSURF':
                mod_subsurf(test_text, mod, CR, title_var, setting, value, text_size,
                            hidden, option, units, space, simple_text_mode)

            if mod.type == 'SURFACE_DEFORM':
                mod_surface_deform(test_text, mod, CR, title_var, setting, value, text_size,
                                   hidden, option, units, space, simple_text_mode)

            if mod.type == 'TRIANGULATE':
                mod_triangulate(test_text, mod, CR, title_var, setting, value, text_size,
                                hidden, option, units, space, simple_text_mode)

            if mod.type == 'WARP':
                mod_warp(test_text, mod, CR, title_var, setting, value, text_size,
                         hidden, option, units, space, simple_text_mode)

            if mod.type == 'WAVE':
                mod_wave(test_text, mod, CR, title_var, setting, value, text_size,
                         hidden, option, units, space, simple_text_mode)

            if mod.type == 'WIREFRAME':
                mod_wireframe(test_text, mod, CR, title_var, setting, value, text_size,
                              hidden, option, units, space, simple_text_mode)

            if mod.type == 'WEIGHTED_NORMAL':
                mod_weighted_normals(test_text, mod, CR, title_var, setting, value, text_size,
                                     hidden, option, units, space, simple_text_mode)

    # WARNING
    # SPACE
    test_text.extend([("SPACE", title_var, space)])
    warning(test_text, CR, title_var, setting, value, text_size, hidden, option, units, space)

    # Blender Keymaps
    if show_blender_keymaps:
        blender_keymaps(test_text, CR, title_var, setting, value, text_size, hidden, option, space)

    # bpy.context.area.tag_redraw()
    return test_text
