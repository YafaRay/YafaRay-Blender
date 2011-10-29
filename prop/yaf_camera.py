# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import bpy
from bpy.props import (FloatProperty,
                       EnumProperty,
                       BoolProperty)

Camera = bpy.types.Camera


def call_camera_update(self, context):
    camera = context.camera
    if camera is not None:
        if camera.camera_type == 'orthographic':
            camera.type = 'ORTHO'
        else:
            camera.type = 'PERSP'


def register():
    Camera.camera_type = EnumProperty(
        name="Camera Type",
        items=(
            ('perspective', "Perspective", ""),
            ('architect', "Architect", ""),
            ('angular', "Angular", ""),
            ('orthographic', "Ortho", "")
        ),
        update=call_camera_update,
        default='perspective')

    Camera.angular_angle = FloatProperty(
        name="Angle",
        min=0.0, max=180.0, precision=3,
        default=90.0)

    Camera.max_angle = FloatProperty(
        name="Max Angle",
        min=0.0, max=180.0, precision=3,
        default=90.0)

    Camera.mirrored = BoolProperty(
        name="Mirrored",
        default=False)

    Camera.circular = BoolProperty(
        name="Circular",
        default=False)

    Camera.use_clipping = BoolProperty(
        name="Use clipping",
        default=False)

    Camera.bokeh_type = EnumProperty(
        name="Bokeh type",
        items=(
            ('disk1', "Disk1", ""),
            ('disk2', "Disk2", ""),
            ('triangle', "Triangle", ""),
            ('square', "Square", ""),
            ('pentagon', "Pentagon", ""),
            ('hexagon', "Hexagon", ""),
            ('ring', "Ring", "")
        ),
        default='disk1')

    Camera.aperture = FloatProperty(
        name="Aperture",
        min=0.0, max=20.0, precision=5,
        default=0.0)

    Camera.bokeh_rotation = FloatProperty(
        name="Bokeh rotation",
        min=0.0, max=180, precision=3,
        default=0.0)

    Camera.bokeh_bias = EnumProperty(
        name="Bokeh bias",
        items=(
            ('uniform', "Uniform", ""),
            ('center', "Center", ""),
            ('edge', "Edge", "")
        ),
        default='uniform')


def unregister():
    Camera.camera_type
    Camera.angular_angle
    Camera.max_angle
    Camera.mirrored
    Camera.circular
    Camera.use_clipping
    Camera.bokeh_type
    Camera.aperture
    Camera.bokeh_rotation
    Camera.bokeh_bias
