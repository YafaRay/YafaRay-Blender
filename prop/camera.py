# SPDX-License-Identifier: GPL-2.0-or-later

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
            ('equirectangular', "Equirectangular", ""),
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

    Camera.angular_projection = EnumProperty(
        name="Angular projection",
        items=(
            ('equidistant', "Equidistant (default)", ""),
            ('orthographic', "Orthographic (angle should be 90º or less)", ""),
            ('stereographic', "Stereographic (angle should be less than 180º)", ""),
            ('equisolid_angle', "Equisolid Angle", ""),
            ('rectilinear', "Rectilinear (angle should be less than 90º)", ""),
        ),
        default='equidistant')

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
    del Camera.camera_type
    del Camera.angular_angle
    del Camera.max_angle
    del Camera.mirrored
    del Camera.circular
    del Camera.angular_projection
    del Camera.use_clipping
    del Camera.bokeh_type
    del Camera.aperture
    del Camera.bokeh_rotation
    del Camera.bokeh_bias
