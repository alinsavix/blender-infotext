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
    "description": "Better text handling for Blender informational text",
    "author": "TDV Alinsa",
    "version": (0, 1, 0),
    "blender": (2, 90, 0),
    "location": "View3D",
    "warning": "Work In Progress - Might be unstable or slow",
    # "wiki_url": "",
    "category": "Tools"
}

import os
import sys

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

from . import infotext
from . import functions
from . import prefs
# from . import ui

from typing import Callable, Dict, List, Optional, Any, Union, Tuple, TYPE_CHECKING

# FIXME: There's probably a better way to do this.
# main_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(main_dir)

# from .infotext import infotext_text_Handle
# from .functions import get_addon_preferences
# from .icon.icons import load_icons
# import .prefs

# from . import infotext


# Property Group
class INFOTEXT_OT_property_group(bpy.types.PropertyGroup):
    face_type_count: Dict[str, int] = {}
    # previous_mesh = []   # FIXME: What was this used for?
    # previous_mode: StringProperty()


##################################
# Register
##################################

CLASSES = [
    # INFOTEXT_OT_Reset_Prefs,
    # InfotextAddonPrefs,
    INFOTEXT_OT_property_group,
]

def register():
    # Preferences and shared state must exist before the draw callback can run.
    prefs.register()

    for cls in CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.infotext = bpy.props.PointerProperty(
        type=INFOTEXT_OT_property_group)

    # Install the draw handler last.
    infotext.register()

    # Check the addon version on Github
    # context = bpy.context
    # prefs = context.preferences.addons[__name__].preferences
    # check_for_update(prefs, context)

    # # Add Text
    # if infotext_text_Handle:
    #     bpy.types.SpaceView3D.draw_handler_remove(
    #         infotext_text_Handle[0], 'WINDOW')
    # infotext_text_Handle[:] = [
    #     bpy.types.SpaceView3D.draw_handler_add(infotext_draw_text_callback, (), 'WINDOW', 'POST_PIXEL')]


# Unregister
def unregister():
    # Stop drawing before preferences or shared state are removed.
    infotext.unregister()

    del bpy.types.WindowManager.infotext

    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)

    prefs.unregister()

    # # Remove Text
    # if infotext_text_Handle:
    #     bpy.types.SpaceView3D.draw_handler_remove(
    #         infotext_text_Handle[0], 'WINDOW')
    #     infotext_text_Handle[:] = []
