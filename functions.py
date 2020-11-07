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
from typing import Tuple

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


def fmt_unit(category: str, value: float, precision: int) -> Tuple[str, float, str]:
    # FIXME: Should the unit system be passed in instead?
    units_system = str(bpy.context.scene.unit_settings.system)

    s = bpy.utils.units.to_string(units_system, category, value, precision)

    # Split the output so we can render it separately. janky... is there
    # a better way to accomplish this while not writing our own code for it?
    (v, u) = s.split()
    return (s, float(v), u)


def fmt_length(value: float, precision: int = 6) -> str:
    return fmt_unit('LENGTH', value, precision)[0]


def fmt_area(value: float, precision: int = 6) -> str:
    return fmt_unit('AREA', value, precision)[0]


def fmt_vol(value: float, precision: int = 6) -> str:
    return fmt_unit('VOLUME', value, precision)[0]


def fmt_mass(value: float, precision: int = 6) -> str:
    return fmt_unit('MASS', value, precision)[0]


def fmt_rot(value: float, precision: int = 6) -> str:
    return fmt_unit('ROTATION', value, precision)[0]

# same as rotation


def fmt_angle(value: float, precision: int = 6) -> str:
    return fmt_unit('ROTATION', value, precision)[0]


def fmt_time(value: float, precision: int = 6) -> str:
    return fmt_unit('TIME', value, precision)[0]


def fmt_vel(value: float, precision: int = 6) -> str:
    return fmt_unit('VELOCITY', value, precision)[0]


def fmt_accel(value: float, precision: int = 6) -> str:
    return fmt_unit('ACCELERATION', value, precision)[0]


def fmt_camera(value: float, precision: int = 6) -> str:
    return fmt_unit('CAMERA', value, precision)[0]


def fmt_pct(value: float, precision: int = 2) -> str:
    s = f'{value:.{precision}f}'

    return(s + '%')


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
