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
import libyafaray4_bindings
from .. import global_vars
import mathutils

def multiplyMatrix4x4Vector4(matrix, vector):
    result = mathutils.Vector((0.0, 0.0, 0.0, 0.0))
    if bpy.app.version >= (2, 80, 0):
        for i in range(4):
            result[i] = vector @ matrix[i]  # use reverse vector multiply order, API changed with rev. 38674
    else:
        for i in range(4):
            result[i] = vector * matrix[i]  # use reverse vector multiply order, API changed with rev. 38674

    return result

class Film:
    def __init__(self, yaf_film, yaf_logger, is_preview):
        self.yaf_film = yaf_film
        self.yaf_logger = yaf_logger
        self.is_preview = is_preview

    def createCameras(self, scene):

        self.yaf_logger.printInfo("Exporting Cameras")
    
        render = scene.render
        
        class CameraData:
            def __init__ (self, camera, camera_name, view_name):
                self.camera = camera
                self.camera_name = camera_name
                self.view_name = view_name
        
        cameras = []

        render_use_multiview = render.use_multiview

        if global_vars.useViewToRender or not render_use_multiview:
            cameras.append(CameraData(scene.camera, scene.camera.name, ""))
        else:
            camera_base_name = scene.camera.name.rsplit('_',1)[0]

            for view in render.views:
                if view.use and not (render.views_format == "STEREO_3D" and view.name != "left" and view.name != "right"):
                    cameras.append(CameraData(scene.objects[camera_base_name+view.camera_suffix], camera_base_name+view.camera_suffix, view.name))

        for cam in cameras:
            if global_vars.useViewToRender and global_vars.viewMatrix:
                # use the view matrix to calculate the inverted transformed
                # points cam pos (0,0,0), front (0,0,1) and up (0,1,0)
                # view matrix works like the opengl view part of the
                # projection matrix, i.e. transforms everything so camera is
                # at 0,0,0 looking towards 0,0,1 (y axis being up)

                m = global_vars.viewMatrix
                # m.transpose() --> not needed anymore: matrix indexing changed with Blender rev.42816
                inv = m.inverted()

                pos = multiplyMatrix4x4Vector4(inv, mathutils.Vector((0, 0, 0, 1)))
                aboveCam = multiplyMatrix4x4Vector4(inv, mathutils.Vector((0, 1, 0, 1)))
                frontCam = multiplyMatrix4x4Vector4(inv, mathutils.Vector((0, 0, 1, 1)))

                dir = frontCam - pos
                up = aboveCam

            else:
                # get cam worldspace transformation matrix, e.g. if cam is parented matrix_local does not work
                matrix = cam.camera.matrix_world.copy()
                # matrix indexing (row, colums) changed in Blender rev.42816, for explanation see also:
                # http://wiki.blender.org/index.php/User:TrumanBlending/Matrix_Indexing
                pos = matrix.col[3]
                dir = matrix.col[2]
                up = pos + matrix.col[1]

            to = pos - dir

            x = int(render.resolution_x * render.resolution_percentage * 0.01)
            y = int(render.resolution_y * render.resolution_percentage * 0.01)

            yaf_param_map = libyafaray4_bindings.ParamMap()

            if global_vars.useViewToRender:
                yaf_param_map.setString("type", "perspective")
                yaf_param_map.setFloat("focal", 0.7)
                global_vars.useViewToRender = False

            else:
                camera = cam.camera.data
                camType = camera.camera_type

                yaf_param_map.setString("type", camType)

                if camera.use_clipping:
                    yaf_param_map.setFloat("nearClip", camera.clip_start)
                    yaf_param_map.setFloat("farClip", camera.clip_end)

                if camType == "orthographic":
                    yaf_param_map.setFloat("scale", camera.ortho_scale)

                elif camType in {"perspective", "architect"}:
                    # Blenders GSOC 2011 project "tomato branch" merged into trunk.
                    # Check for sensor settings and use them in yafaray exporter also.
                    if camera.sensor_fit == 'AUTO':
                        horizontal_fit = (x > y)
                        sensor_size = camera.sensor_width
                    elif camera.sensor_fit == 'HORIZONTAL':
                        horizontal_fit = True
                        sensor_size = camera.sensor_width
                    else:
                        horizontal_fit = False
                        sensor_size = camera.sensor_height

                    if horizontal_fit:
                        f_aspect = 1.0
                    else:
                        f_aspect = x / y

                    yaf_param_map.setFloat("focal", camera.lens / (f_aspect * sensor_size))

                    # DOF params, only valid for real camera
                    # use DOF object distance if present or fixed DOF
                    if bpy.app.version >= (2, 80, 0):
                        pass  # FIXME BLENDER 2.80-3.00
                    else:
                        if camera.dof_object is not None:
                            # use DOF object distance
                            dist = (pos.xyz - camera.dof_object.location.xyz).length
                            dof_distance = dist
                        else:
                            # use fixed DOF distance
                            dof_distance = camera.dof_distance
                        yaf_param_map.setFloat("dof_distance", dof_distance)

                    yaf_param_map.setFloat("aperture", camera.aperture)
                    # bokeh params
                    yaf_param_map.setString("bokeh_type", camera.bokeh_type)
                    yaf_param_map.setFloat("bokeh_rotation", camera.bokeh_rotation)

                elif camType == "angular":
                    yaf_param_map.setBool("circular", camera.circular)
                    yaf_param_map.setBool("mirrored", camera.mirrored)
                    yaf_param_map.setString("projection", camera.angular_projection)
                    yaf_param_map.setFloat("max_angle", camera.max_angle)
                    yaf_param_map.setFloat("angle", camera.angular_angle)

            yaf_param_map.setInt("resx", x)
            yaf_param_map.setInt("resy", y)

            if self.is_preview and bpy.data.scenes[0].yafaray.preview.enable:

                    #incl = bpy.data.scenes[0].yafaray.preview.camRotIncl
                    #azi = bpy.data.scenes[0].yafaray.preview.camRotAzi
                    rot = bpy.data.scenes[0].yafaray.preview.camRot
                    dist = bpy.data.scenes[0].yafaray.preview.camDist

                    #pos = (dist*math.sin(incl)*math.cos(azi), dist*math.sin(incl)*math.sin(azi), dist*math.cos(incl))
                    #up = (math.sin(rotZ), 0, math.cos(rotZ))
                    pos = (-dist*rot[0], -dist*rot[2], -dist*rot[1])
                    up = (0,0,1)
                    to = (0,0,0)

            yaf_param_map.setVector("from", pos[0], pos[1], pos[2])
            yaf_param_map.setVector("up", up[0], up[1], up[2])
            yaf_param_map.setVector("to", to[0], to[1], to[2])
            self.yaf_film.defineCamera(yaf_param_map)

