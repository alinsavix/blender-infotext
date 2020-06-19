'''
Copyright (C) 2015 Pistiwique, Pitiwazou
 
Created by Pistiwique, Pitiwazou
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
 
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import os
import bpy
import bpy.utils.previews
 
epm_icon_collections = {}
epm_icons_loaded = False
 
def load_icons():
    global epm_icon_collections
    global epm_icons_loaded
 
    if epm_icons_loaded: return epm_icon_collections["main"]
 
    custom_icons = bpy.utils.previews.new()
 
    icons_dir = os.path.join(os.path.dirname(__file__))
    

    custom_icons.load("icon_line", os.path.join(icons_dir, "line.png"), 'IMAGE')
    custom_icons.load("icon_bevel", os.path.join(icons_dir, "bevel.png"), 'IMAGE')
    custom_icons.load("icon_faces", os.path.join(icons_dir, "faces.png"), 'IMAGE')
    custom_icons.load("icon_sharp", os.path.join(icons_dir, "sharp.png"), 'IMAGE')
    custom_icons.load("icon_crease", os.path.join(icons_dir, "crease.png"), 'IMAGE')
    custom_icons.load("icon_clear", os.path.join(icons_dir, "clear.png"), 'IMAGE')
    custom_icons.load("icon_ngons", os.path.join(icons_dir, "ngons.png"), 'IMAGE')
    custom_icons.load("icon_laprelax", os.path.join(icons_dir, "laprelax.png"), 'IMAGE')
    custom_icons.load("icon_autosmooth", os.path.join(icons_dir, "autosmooth.png"), 'IMAGE')
    custom_icons.load("icon_autosmooth_off", os.path.join(icons_dir, "autosmooth_off.png"), 'IMAGE')
    custom_icons.load("icon_tubify", os.path.join(icons_dir, "tubify.png"), 'IMAGE')
    custom_icons.load("icon_bevel_1", os.path.join(icons_dir, "bevel_1.png"), 'IMAGE')
    custom_icons.load("icon_mirror", os.path.join(icons_dir, "mirror.png"), 'IMAGE')
    custom_icons.load("icon_subsurf", os.path.join(icons_dir, "subsurf.png"), 'IMAGE')
    custom_icons.load("icon_modifiers", os.path.join(icons_dir, "modifiers.png"), 'IMAGE')
    custom_icons.load("icon_vgroup", os.path.join(icons_dir, "vgroup.png"), 'IMAGE')
    custom_icons.load("icon_dym_line", os.path.join(icons_dir, "dym_line.png"), 'IMAGE')


    custom_icons.load("icon_rename", os.path.join(icons_dir, "rename.png"), 'IMAGE')
    custom_icons.load("icon_intersection", os.path.join(icons_dir, "intersection.png"), 'IMAGE')
    custom_icons.load("icon_parent", os.path.join(icons_dir, "parent.png"), 'IMAGE')
    custom_icons.load("icon_replace", os.path.join(icons_dir, "replace.png"), 'IMAGE')
    
    #Shading
    custom_icons.load("icon_solid", os.path.join(icons_dir, "solid.png"), 'IMAGE')
    custom_icons.load("icon_wire", os.path.join(icons_dir, "wire.png"), 'IMAGE')
    custom_icons.load("icon_bounds", os.path.join(icons_dir, "bounds.png"), 'IMAGE')
    custom_icons.load("icon_add_boolean", os.path.join(icons_dir, "add_boolean.png"), 'IMAGE')

    #Primitives
    custom_icons.load("icon_plane", os.path.join(icons_dir, "plane.png"), 'IMAGE')
    custom_icons.load("icon_vert", os.path.join(icons_dir, "vert.png"), 'IMAGE')
    custom_icons.load("icon_cylinder_8", os.path.join(icons_dir, "cylinder_8.png"), 'IMAGE')
    custom_icons.load("icon_cylinder_16", os.path.join(icons_dir, "cylinder_16.png"), 'IMAGE')
    custom_icons.load("icon_carver", os.path.join(icons_dir, "carver.png"), 'IMAGE')
    custom_icons.load("icon_project", os.path.join(icons_dir, "project.png"), 'IMAGE')
    custom_icons.load("draw_text", os.path.join(icons_dir, "draw_text.png"), 'IMAGE')

    custom_icons.load("cube_round", os.path.join(icons_dir, "cube_round.png"), 'IMAGE')
    custom_icons.load("cube_rounded_cut", os.path.join(icons_dir, "cube_rounded_cut.png"), 'IMAGE')
    custom_icons.load("long_cylinder", os.path.join(icons_dir, "long_cylinder.png"), 'IMAGE')
    custom_icons.load("rounded_cube", os.path.join(icons_dir, "rounded_cube.png"), 'IMAGE')
    custom_icons.load("rounded_cross", os.path.join(icons_dir, "rounded_cross.png"), 'IMAGE')
    custom_icons.load("cross", os.path.join(icons_dir, "cross.png"), 'IMAGE')


    custom_icons.load("prim_screw_2", os.path.join(icons_dir, "prim_screw_2.png"), 'IMAGE')
    custom_icons.load("prim_screw_3", os.path.join(icons_dir, "prim_screw_3.png"), 'IMAGE')
    custom_icons.load("prim_screw_4", os.path.join(icons_dir, "prim_screw_4.png"), 'IMAGE')
    custom_icons.load("prim_screw_5", os.path.join(icons_dir, "prim_screw_5.png"), 'IMAGE')

    custom_icons.load("prim_cross", os.path.join(icons_dir, "prim_cross.png"), 'IMAGE')
    custom_icons.load("prim_cross_rounded", os.path.join(icons_dir, "prim_cross_rounded.png"), 'IMAGE')

    
    #Curves
    custom_icons.load("icon_radius", os.path.join(icons_dir, "radius.png"), 'IMAGE')
    custom_icons.load("icon_close", os.path.join(icons_dir, "close.png"), 'IMAGE')
    custom_icons.load("icon_free", os.path.join(icons_dir, "free.png"), 'IMAGE')
    custom_icons.load("icon_vector", os.path.join(icons_dir, "vector.png"), 'IMAGE')
    custom_icons.load("icon_auto", os.path.join(icons_dir, "auto.png"), 'IMAGE')
    custom_icons.load("icon_align", os.path.join(icons_dir, "align.png"), 'IMAGE')
    custom_icons.load("icon_hide_normals", os.path.join(icons_dir, "hide_normals.png"), 'IMAGE')
    custom_icons.load("icon_show_normals", os.path.join(icons_dir, "show_normals.png"), 'IMAGE')
    custom_icons.load("icon_switch_direction", os.path.join(icons_dir, "switch_direction.png"), 'IMAGE')
    custom_icons.load("icon_poly", os.path.join(icons_dir, "poly.png"), 'IMAGE')
    custom_icons.load("icon_bezier", os.path.join(icons_dir, "bezier.png"), 'IMAGE')
    custom_icons.load("icon_recalc_normals", os.path.join(icons_dir, "recalc_normals.png"), 'IMAGE')

    #Colors
    custom_icons.load("red", os.path.join(icons_dir, "red.png"), 'IMAGE')
    custom_icons.load("orange", os.path.join(icons_dir, "orange.png"), 'IMAGE')
    custom_icons.load("yellow", os.path.join(icons_dir, "yellow.png"), 'IMAGE')
    custom_icons.load("green", os.path.join(icons_dir, "green.png"), 'IMAGE')
    custom_icons.load("cian", os.path.join(icons_dir, "cian.png"), 'IMAGE')
    custom_icons.load("blue", os.path.join(icons_dir, "blue.png"), 'IMAGE')
    custom_icons.load("purple", os.path.join(icons_dir, "purple.png"), 'IMAGE')
    custom_icons.load("pink", os.path.join(icons_dir, "pink.png"), 'IMAGE')

    custom_icons.load("nb_1", os.path.join(icons_dir, "nb_1.png"), 'IMAGE')
    custom_icons.load("nb_2", os.path.join(icons_dir, "nb_2.png"), 'IMAGE')
    custom_icons.load("nb_3", os.path.join(icons_dir, "nb_3.png"), 'IMAGE')
    custom_icons.load("nb_4", os.path.join(icons_dir, "nb_4.png"), 'IMAGE')
    custom_icons.load("nb_5", os.path.join(icons_dir, "nb_5.png"), 'IMAGE')
    custom_icons.load("nb_6", os.path.join(icons_dir, "nb_6.png"), 'IMAGE')
    custom_icons.load("nb_7", os.path.join(icons_dir, "nb_7.png"), 'IMAGE')
    custom_icons.load("nb_8", os.path.join(icons_dir, "nb_8.png"), 'IMAGE')

    custom_icons.load("icon_market", os.path.join(icons_dir, "market.png"), 'IMAGE')
    custom_icons.load("icon_artstation", os.path.join(icons_dir, "artstation.png"), 'IMAGE')
    custom_icons.load("icon_gumroad", os.path.join(icons_dir, "gumroad.png"), 'IMAGE')
    custom_icons.load("icon_youtube", os.path.join(icons_dir, "youtube.png"), 'IMAGE')
    custom_icons.load("icon_tutocom", os.path.join(icons_dir, "tutocom.png"), 'IMAGE')
    custom_icons.load("icon_discord", os.path.join(icons_dir, "discord.png"), 'IMAGE')

    custom_icons.load("icon_fluent", os.path.join(icons_dir, "fluent.png"), 'IMAGE')

    epm_icon_collections["main"] = custom_icons
    epm_icons_loaded = True
 
    return epm_icon_collections["main"]
 
def speedflow_clear_icons():
    global epm_icons_loaded
    for icon in epm_icon_collections.values():
        bpy.utils.previews.remove(icon)
    epm_icon_collections.clear()
    epm_icons_loaded = False
