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
import mathutils
import libyafaray4_bindings
from ..util.math import multiply_matrix4x4_vector4


class Film:
    def __init__(self, yaf_film, yaf_logger, is_preview):
        self.yaf_film = yaf_film
        self.yaf_logger = yaf_logger
        self.is_preview = is_preview

    def define_camera(self, bl_camera, res_x, res_y, res_percentage, use_view_to_render, view_matrix):
        if use_view_to_render and view_matrix:
            # use the view matrix to calculate the inverted transformed
            # points cam pos (0,0,0), front (0,0,1) and up (0,1,0)
            # view matrix works like the opengl view part of the
            # projection matrix, i.e. transforms everything so camera is
            # at 0,0,0 looking towards 0,0,1 (y axis being up)
            inv = view_matrix.inverted()

            pos = multiply_matrix4x4_vector4(inv, mathutils.Vector((0, 0, 0, 1)))
            above_cam = multiply_matrix4x4_vector4(inv, mathutils.Vector((0, 1, 0, 1)))
            front_cam = multiply_matrix4x4_vector4(inv, mathutils.Vector((0, 0, 1, 1)))

            direction = front_cam - pos
            up = above_cam

        else:
            # get cam worldspace transformation matrix, e.g. if cam is parented matrix_local does not work
            matrix = bl_camera.matrix_world.copy()
            # matrix indexing (row, colums) changed in Blender rev.42816, for explanation see also:
            # http://wiki.blender.org/index.php/User:TrumanBlending/Matrix_Indexing
            pos = matrix.col[3]
            direction = matrix.col[2]
            up = pos + matrix.col[1]

        to = pos - direction

        x = int(res_x * res_percentage * 0.01)
        y = int(res_y * res_percentage * 0.01)

        yaf_param_map = libyafaray4_bindings.ParamMap()

        if use_view_to_render:
            yaf_param_map.setString("type", "perspective")
            yaf_param_map.setFloat("focal", 0.7)

        else:
            cam_type = bl_camera.camera_type

            yaf_param_map.setString("type", cam_type)

            if bl_camera.use_clipping:
                yaf_param_map.setFloat("nearClip", bl_camera.clip_start)
                yaf_param_map.setFloat("farClip", bl_camera.clip_end)

            if cam_type == "orthographic":
                yaf_param_map.setFloat("scale", bl_camera.ortho_scale)

            elif cam_type in {"perspective", "architect"}:
                # Blenders GSOC 2011 project "tomato branch" merged into trunk.
                # Check for sensor settings and use them in yafaray exporter also.
                if bl_camera.sensor_fit == 'AUTO':
                    horizontal_fit = (x > y)
                    sensor_size = bl_camera.sensor_width
                elif bl_camera.sensor_fit == 'HORIZONTAL':
                    horizontal_fit = True
                    sensor_size = bl_camera.sensor_width
                else:
                    horizontal_fit = False
                    sensor_size = bl_camera.sensor_height

                if horizontal_fit:
                    f_aspect = 1.0
                else:
                    f_aspect = x / y

                yaf_param_map.setFloat("focal", bl_camera.lens / (f_aspect * sensor_size))

                # DOF params, only valid for real camera
                # use DOF object distance if present or fixed DOF
                if bpy.app.version >= (2, 80, 0):
                    pass  # FIXME BLENDER 2.80-3.00
                else:
                    if bl_camera.dof_object is not None:
                        # use DOF object distance
                        dist = (pos.xyz - bl_camera.dof_object.location.xyz).length
                        dof_distance = dist
                    else:
                        # use fixed DOF distance
                        dof_distance = bl_camera.dof_distance
                    yaf_param_map.setFloat("dof_distance", dof_distance)

                yaf_param_map.setFloat("aperture", bl_camera.aperture)
                # bokeh params
                yaf_param_map.setString("bokeh_type", bl_camera.bokeh_type)
                yaf_param_map.setFloat("bokeh_rotation", bl_camera.bokeh_rotation)

            elif cam_type == "angular":
                yaf_param_map.setBool("circular", bl_camera.circular)
                yaf_param_map.setBool("mirrored", bl_camera.mirrored)
                yaf_param_map.setString("projection", bl_camera.angular_projection)
                yaf_param_map.setFloat("max_angle", bl_camera.max_angle)
                yaf_param_map.setFloat("angle", bl_camera.angular_angle)

        yaf_param_map.setInt("resx", x)
        yaf_param_map.setInt("resy", y)

        if self.is_preview and bpy.data.scenes[0].yafaray.is_preview.enable:

                #incl = bpy.data.scenes[0].yafaray.preview.camRotIncl
                #azi = bpy.data.scenes[0].yafaray.preview.camRotAzi
                rot = bpy.data.scenes[0].yafaray.is_preview.camRot
                dist = bpy.data.scenes[0].yafaray.is_preview.camDist

                #pos = (dist*math.sin(incl)*math.cos(azi), dist*math.sin(incl)*math.sin(azi), dist*math.cos(incl))
                #up = (math.sin(rotZ), 0, math.cos(rotZ))
                pos = (-dist*rot[0], -dist*rot[2], -dist*rot[1])
                up = (0,0,1)
                to = (0,0,0)

        yaf_param_map.setVector("from", pos[0], pos[1], pos[2])
        yaf_param_map.setVector("up", up[0], up[1], up[2])
        yaf_param_map.setVector("to", to[0], to[1], to[2])
        self.yaf_film.defineCamera(yaf_param_map)

