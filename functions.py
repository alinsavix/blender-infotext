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
from bpy.props import (StringProperty,
                       BoolProperty,
                       FloatVectorProperty,
                       FloatProperty,
                       EnumProperty,
                       IntProperty,
                       PointerProperty)

from bpy.types import PropertyGroup

# from bpy.app.handlers import persistent


def get_addon_preferences():
    addon_key = __package__.split(".")[0]

    return bpy.context.preferences.addons[addon_key].preferences


def get_face_type_count(infotext, obj):
    if obj.type == 'MESH':
        tris = 0
        ngons = 0
        if obj.data.is_editmode:
            obj.update_from_editmode()
        for f in obj.data.polygons:
            vert_count = len(f.vertices)
            if vert_count == 3:
                tris += 1
            elif vert_count == 4:
                tris += 2
            else:
                ngons += 1
                tris += vert_count - 2

        infotext.face_type_count['TRIS'] = tris
        infotext.face_type_count['NGONS'] = ngons


# Property Group
class infotext(PropertyGroup):
    # active_modifier: IntProperty(default=-1)
    pass


def register():
    try:
        bpy.utils.register_class(infotext)
    except:
        print("infotext already registred")

    bpy.types.WindowManager.infotext = PointerProperty(type=infotext)


def unregister():
    bpy.utils.unregister_class(infotext)
    del bpy.types.WindowManager.infotext


# @persistent
# def infotext_update_mesh_info_values(dummy):
#     addon_prefs = get_addon_preferences()
#     if addon_prefs.show_infotext:
#         infotext_properties = bpy.context.window_manager.infotext_properties
#         if bpy.context.object is not None:
#             ob = bpy.context.scene.objects.active
#             mode = ob.mode
#
#             if not infotext_properties.previous_mode:
#                 infotext_properties.previous_mode = mode
#
#             if mode == 'EDIT':
#                 if infotext_properties.previous_mode != 'EDIT':
#                     infotext_properties.previous_mode = mode
#                     get_face_type_count(infotext_properties, ob)
#
#                 else:
#                     if ob.data.is_updated_data:
#                         get_face_type_count(infotext_properties, ob)
#
#             elif mode == 'OBJECT':
#                 if infotext_properties.previous_mode != 'OBJECT':
#                     infotext_properties.previous_mode = mode
#                     get_face_type_count(infotext_properties, ob)
#
#
#                 if bpy.context.selected_objects not in infotext_properties.previous_mesh:
#                     infotext_properties.previous_mesh[:] = []
#                     infotext_properties.previous_mesh.append(bpy.context.selected_objects)
#                     get_face_type_count(infotext_properties, ob)
#
#
# bpy.app.handlers.scene_update_post.append(infotext_update_mesh_info_values)
