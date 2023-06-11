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
import time
import math
import mathutils
import libyafaray4_bindings
from ..util.io_utils import scene_from_depsgraph
from .. import yaf_global_vars

def multiplyMatrix4x4Vector4(matrix, vector):
    result = mathutils.Vector((0.0, 0.0, 0.0, 0.0))
    if bpy.app.version >= (2, 80, 0):
        for i in range(4):
            result[i] = vector @ matrix[i]  # use reverse vector multiply order, API changed with rev. 38674
    else:
        for i in range(4):
            result[i] = vector * matrix[i]  # use reverse vector multiply order, API changed with rev. 38674

    return result


class yafObject(object):
    def __init__(self, scene, logger, preview):
        self.yaf_scene = scene
        self.logger = logger
        self.is_preview = preview

    def setDepsgraph(self, depsgraph):
        self.depsgraph = depsgraph
        self.scene = scene_from_depsgraph(depsgraph)

    def createCameras(self):

        
        self.logger.printInfo("Exporting Cameras")
    
        render = self.scene.render
        
        class CameraData:
            def __init__ (self, camera, camera_name, view_name):
                self.camera = camera
                self.camera_name = camera_name
                self.view_name = view_name
        
        cameras = []

        render_use_multiview = render.use_multiview

        if yaf_global_vars.useViewToRender or not render_use_multiview:
            cameras.append(CameraData(self.scene.camera, self.scene.camera.name, ""))
        else:
            camera_base_name = self.scene.camera.name.rsplit('_',1)[0]

            for view in render.views:
                if view.use and not (render.views_format == "STEREO_3D" and view.name != "left" and view.name != "right"):
                    cameras.append(CameraData(self.scene.objects[camera_base_name+view.camera_suffix], camera_base_name+view.camera_suffix, view.name))

        for cam in cameras:
            if yaf_global_vars.useViewToRender and yaf_global_vars.viewMatrix:
                # use the view matrix to calculate the inverted transformed
                # points cam pos (0,0,0), front (0,0,1) and up (0,1,0)
                # view matrix works like the opengl view part of the
                # projection matrix, i.e. transforms everything so camera is
                # at 0,0,0 looking towards 0,0,1 (y axis being up)

                m = yaf_global_vars.viewMatrix
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

            param_map = libyafaray4_bindings.ParamMap()

            if yaf_global_vars.useViewToRender:
                param_map.setString("type", "perspective")
                param_map.setFloat("focal", 0.7)
                yaf_global_vars.useViewToRender = False

            else:
                camera = cam.camera.data
                camType = camera.camera_type

                param_map.setString("type", camType)

                if camera.use_clipping:
                    param_map.setFloat("nearClip", camera.clip_start)
                    param_map.setFloat("farClip", camera.clip_end)

                if camType == "orthographic":
                    param_map.setFloat("scale", camera.ortho_scale)

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

                    param_map.setFloat("focal", camera.lens / (f_aspect * sensor_size))

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
                        param_map.setFloat("dof_distance", dof_distance)

                    param_map.setFloat("aperture", camera.aperture)
                    # bokeh params
                    param_map.setString("bokeh_type", camera.bokeh_type)
                    param_map.setFloat("bokeh_rotation", camera.bokeh_rotation)

                elif camType == "angular":
                    param_map.setBool("circular", camera.circular)
                    param_map.setBool("mirrored", camera.mirrored)
                    param_map.setString("projection", camera.angular_projection)
                    param_map.setFloat("max_angle", camera.max_angle)
                    param_map.setFloat("angle", camera.angular_angle)

            param_map.setInt("resx", x)
            param_map.setInt("resy", y)

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

            param_map.setVector("from", pos[0], pos[1], pos[2])
            param_map.setVector("up", up[0], up[1], up[2])
            param_map.setVector("to", to[0], to[1], to[2])
            self.film.defineCamera(param_map)


    def getBBCorners(self, object):
        bb = object.bound_box   # look bpy.types.Object if there is any problem

        min = [1e10, 1e10, 1e10]
        max = [-1e10, -1e10, -1e10]

        for corner in bb:
            for i in range(3):
                if corner[i] < min[i]:
                    min[i] = corner[i]
                if corner[i] > max[i]:
                    max[i] = corner[i]

        return min, max

    def writeObject(self, obj):

        if obj.vol_enable:  # Volume region
            self.writeVolumeObject(obj)

        elif obj.ml_enable:  # Meshlight
            self.writeMeshLight(obj)

        elif obj.bgp_enable:  # BGPortal Light
            self.writeBGPortal(obj)

        elif obj.particle_systems:  # Particle Hair system
            self.writeParticleStrands(obj)

        else:  # The rest of the object types
            matrix = obj.matrix_world.copy()
            if self.is_preview and bpy.data.scenes[0].yafaray.preview.enable:
                if "checkers" in obj.name and bpy.data.scenes[0].yafaray.preview.previewBackground == "checker":
                        self.writeMesh(obj, matrix)
                elif "checkers" not in obj.name:
                        self.writeMesh(obj, matrix)
            else:        
                self.writeMesh(obj, matrix)

    def writeInstanceBase(self, ID, obj):
        self.logger.printInfo("Exporting Base Mesh: {0} with ID: {1}".format(obj.name, ID))
        # Create this geometry object as a base object for instances
        self.writeGeometry(ID, obj, None, obj.pass_index, None, "normal", True)  # We want the vertices in object space
        return ID

    def writeInstance(self, oID, obj2WorldMatrix, base_obj_name):
        obj_to_world = obj2WorldMatrix.to_4x4()
        # mat4.transpose() --> not needed anymore: matrix indexing changed with Blender rev.42816
        #o2w = self.get4x4Matrix(mat4)
        #self.yi.addInstance(base_obj_name, o2w)
        instance_id = self.yaf_scene.createInstance()
        object_id = self.yaf_scene.getObjectId(base_obj_name)
        self.logger.printVerbose("Exporting Instance ID={0} of {1} [ID = {2}]".format(instance_id, base_obj_name, object_id))
        self.yaf_scene.addInstanceObject(instance_id, object_id)
        self.addInstanceMatrix(instance_id, obj_to_world, 0.0)
        return instance_id

    def addInstanceMatrix(self, instance_id, obj2WorldMatrix, time):
        self.logger.printVerbose("Adding matrix to Instance ID={0} at time {1}".format(instance_id, time))
        #print(obj2WorldMatrix)
        obj_to_world = obj2WorldMatrix.to_4x4()
        self.yaf_scene.addInstanceMatrix(instance_id,
                                         obj_to_world[0][0], obj_to_world[0][1], obj_to_world[0][2], obj_to_world[0][3],
                                         obj_to_world[1][0], obj_to_world[1][1], obj_to_world[1][2], obj_to_world[1][3],
                                         obj_to_world[2][0], obj_to_world[2][1], obj_to_world[2][2], obj_to_world[2][3],
                                         obj_to_world[3][0], obj_to_world[3][1], obj_to_world[3][2], obj_to_world[3][3],
                                         time)
        del obj_to_world

    def writeMesh(self, obj, matrix, ID=None):

        if ID is None:
            # Generate unique object ID
            ID = obj.name
        
        self.logger.printInfo("Exporting Mesh: {0}".format(ID))

        if self.is_preview and bpy.data.scenes[0].yafaray.preview.enable and "preview" in obj.name:
            ymat = obj.active_material.name
            
            if bpy.data.scenes[0].yafaray.preview.previewObject != "" and bpy.data.scenes[0].objects[bpy.data.scenes[0].yafaray.preview.previewObject].type=="MESH":
                    customObj = bpy.data.scenes[0].objects[bpy.data.scenes[0].yafaray.preview.previewObject]
                    previewMatrix = customObj.matrix_world.copy()
                    previewMatrix[0][3]=0
                    previewMatrix[1][3]=0
                    previewMatrix[2][3]=0
                    self.writeGeometry(ID, customObj, previewMatrix, obj.pass_index, ymat)
            else:
                    previewMatrix = obj.matrix_world.copy()
                    previewMatrix[0][3]=0
                    previewMatrix[1][3]=0
                    previewMatrix[2][3]=0
                    
                    self.writeGeometry(ID, obj, previewMatrix, obj.pass_index)
        else:
            self.writeGeometry(ID, obj, matrix, obj.pass_index)

    def writeBGPortal(self, obj):
        self.logger.printInfo("Exporting Background Portal Light: {0}".format(obj.name))
        param_map = libyafaray4_bindings.ParamMap()
        param_map.setInt("obj_pass_index", obj.pass_index)
        param_map.setString("type", "bgPortalLight")
        param_map.setFloat("power", obj.bgp_power)
        param_map.setInt("samples", obj.bgp_samples)
        param_map.setString("object_name", obj.name)
        param_map.setBool("with_caustic", obj.bgp_with_caustic)
        param_map.setBool("with_diffuse", obj.bgp_with_diffuse)
        param_map.setBool("photon_only", obj.bgp_photon_only)
        self.yaf_scene.createLight(obj.name)
        matrix = obj.matrix_world.copy()
        # Makes object invisible to the renderer (doesn't enter the kdtree)
        self.writeGeometry(obj.name, obj, matrix, obj.pass_index, None, "invisible")

    def writeMeshLight(self, obj):

        self.logger.printInfo("Exporting Meshlight: {0}".format(obj.name))
        ml_matname = "ML_"
        ml_matname += obj.name + "." + str(obj.__hash__())

        param_map = libyafaray4_bindings.ParamMap()
        param_map.setInt("obj_pass_index", obj.pass_index)
        param_map.setString("type", "light_mat")
        param_map.setBool("double_sided", obj.ml_double_sided)
        c = obj.ml_color
        param_map.setColor("color", c[0], c[1], c[2])
        param_map.setFloat("power", obj.ml_power)
        self.yaf_scene.createMaterial(ml_matname)

        # Export mesh light
        param_map = libyafaray4_bindings.ParamMap()
        param_map.setInt("obj_pass_index", obj.pass_index)
        param_map.setString("type", "objectlight")
        param_map.setBool("double_sided", obj.ml_double_sided)
        c = obj.ml_color
        param_map.setColor("color", c[0], c[1], c[2])
        param_map.setFloat("power", obj.ml_power)
        param_map.setInt("samples", obj.ml_samples)
        param_map.setString("object_name", obj.name)
        self.yaf_scene.createLight(obj.name)

        matrix = obj.matrix_world.copy()
        self.writeGeometry(obj.name, obj, matrix, obj.pass_index, ml_matname)

    def writeVolumeObject(self, obj):

        self.logger.printInfo("Exporting Volume Region: {0}".format(obj.name))

        
        # me = obj.data  /* UNUSED */
        # me_materials = me.materials  /* UNUSED */

        param_map = libyafaray4_bindings.ParamMap()
        param_map.setInt("obj_pass_index", obj.pass_index)

        if obj.vol_region == 'ExpDensity Volume':
            param_map.setString("type", "ExpDensityVolume")
            param_map.setFloat("a", obj.vol_height)
            param_map.setFloat("b", obj.vol_steepness)

        elif obj.vol_region == 'Uniform Volume':
            param_map.setString("type", "UniformVolume")

        elif obj.vol_region == 'Noise Volume':
            if not obj.active_material:
                self.logger.printError("Volume object ({0}) is missing the materials".format(obj.name))
            elif not obj.active_material.active_texture:
                self.logger.printError("Volume object's material ({0}) is missing the noise texture".format(obj.name))
            else:
                texture = obj.active_material.active_texture

                param_map.setString("type", "NoiseVolume")
                param_map.setFloat("sharpness", obj.vol_sharpness)
                param_map.setFloat("cover", obj.vol_cover)
                param_map.setFloat("density", obj.vol_density)
                param_map.setString("texture", texture.name)

        elif obj.vol_region == 'Grid Volume':
            param_map.setString("type", "GridVolume")

        param_map.setFloat("sigma_a", obj.vol_absorp)
        param_map.setFloat("sigma_s", obj.vol_scatter)
        param_map.setInt("attgridScale", self.scene.world.v_int_attgridres)

        # Calculate BoundingBox: get the low corner (minx, miny, minz)
        # and the up corner (maxx, maxy, maxz) then apply object scale,
        # also clamp the values to min: -1e10 and max: 1e10

        if bpy.app.version >= (2, 80, 0):
            mesh = obj.to_mesh(preserve_all_data_layers=True, depsgraph=self.depsgraph)
        else:
            mesh = obj.to_mesh(self.scene, True, 'RENDER')
        matrix = obj.matrix_world.copy()
        mesh.transform(matrix)

        vec = [j for v in mesh.vertices for j in v.co]

        param_map.setFloat("minX", max(min(vec[0::3]), -1e10))
        param_map.setFloat("minY", max(min(vec[1::3]), -1e10))
        param_map.setFloat("minZ", max(min(vec[2::3]), -1e10))
        param_map.setFloat("maxX", min(max(vec[0::3]), 1e10))
        param_map.setFloat("maxY", min(max(vec[1::3]), 1e10))
        param_map.setFloat("maxZ", min(max(vec[2::3]), 1e10))

        self.yaf_scene.createVolumeRegion("VR.{0}-{1}".format(obj.name, str(obj.__hash__())))
        if bpy.app.version >= (2, 80, 0):
            pass  # FIXME BLENDER 2.80-3.00
        else:
            bpy.data.meshes.remove(mesh, do_unlink=False)

    def writeGeometry(self, ID, obj, matrix, pass_index, oMat=None, visibility="normal", is_base_object=False):
        isSmooth = False
        hasOrco = False

        if bpy.app.version >= (2, 80, 0):
            mesh = obj.to_mesh(preserve_all_data_layers=True, depsgraph=self.depsgraph)
            # test for UV Map after BMesh API changes
            uv_texture = mesh.uv_layers if 'uv_layers' in dir(mesh) else mesh.uv_textures
            # test for faces after BMesh API changes
            face_attr = 'polygons' if 'polygons' in dir(mesh) else 'loop_triangles'
            hasUV = False  # FIXME BLENDER 2.80-3.00 #len(uv_texture) > 0  # check for UV's

            if face_attr == 'loop_triangles':
                if not mesh.loop_triangles and mesh.polygons:
                    # BMesh API update, check for tessellated faces, if needed calculate them...
                    mesh.update(calc_edges=False, calc_edges_loose=False, calc_loop_triangles=True)

                if not mesh.loop_triangles:
                    # if there are no faces, no need to write geometry, remove mesh data then...
                    bpy.data.meshes.remove(mesh, do_unlink=False)
                    return
            else:
                if not mesh.polygons:
                    # if there are no faces, no need to write geometry, remove mesh data then...
                    bpy.data.meshes.remove(mesh, do_unlink=False)
                    return
        else:
            mesh = obj.to_mesh(self.scene, True, 'RENDER')
            # test for UV Map after BMesh API changes
            uv_texture = mesh.tessface_uv_textures if 'tessface_uv_textures' in dir(mesh) else mesh.uv_textures
            # test for faces after BMesh API changes
            face_attr = 'faces' if 'faces' in dir(mesh) else 'tessfaces'
            hasUV = len(uv_texture) > 0  # check for UV's

            if face_attr == 'tessfaces':
                if not mesh.tessfaces and mesh.polygons:
                    # BMesh API update, check for tessellated faces, if needed calculate them...
                    mesh.update(calc_tessface=True)

                if not mesh.tessfaces:
                    # if there are no faces, no need to write geometry, remove mesh data then...
                    bpy.data.meshes.remove(mesh, do_unlink=False)
                    return
            else:
                if not mesh.faces:
                    # if there are no faces, no need to write geometry, remove mesh data then...
                    bpy.data.meshes.remove(mesh, do_unlink=False)
                    return

        if bpy.app.version >= (2, 80, 0):
            pass  # FIXME BLENDER 2.80-3.00
        else:
            # Check if the object has an orco mapped texture
            for mat in [mmat for mmat in mesh.materials if mmat is not None]:
                for m in [mtex for mtex in mat.texture_slots if mtex is not None]:
                    if m.texture_coords == 'ORCO':
                        hasOrco = True
                        break
                if hasOrco:
                    break

        # normalized vertex positions for orco mapping
        ov = []

        if hasOrco:
            # Keep a copy of the untransformed vertex and bring them
            # into a (-1 -1 -1) (1 1 1) bounding box
            bbMin, bbMax = self.getBBCorners(obj)

            delta = []

            for i in range(3):
                delta.append(bbMax[i] - bbMin[i])
                if delta[i] < 0.0001:
                    delta[i] = 1

            # use untransformed mesh's vertices
            for v in mesh.vertices:
                normCo = []
                for i in range(3):
                    normCo.append(2 * (v.co[i] - bbMin[i]) / delta[i] - 1)

                ov.append([normCo[0], normCo[1], normCo[2]])

        # Transform the mesh after orcos have been stored and only if matrix exists
        if matrix is not None:
            mesh.transform(matrix)
            
        if self.is_preview:
            if("checker" in obj.name):
                matrix2 = mathutils.Matrix.Scale(4, 4)
                mesh.transform(matrix2)
            elif bpy.data.scenes[0].yafaray.preview.enable:
                matrix2 = mathutils.Matrix.Scale(bpy.data.scenes[0].yafaray.preview.objScale, 4)
                mesh.transform(matrix2)
                matrix2 = mathutils.Matrix.Rotation(bpy.data.scenes[0].yafaray.preview.rotZ, 4, 'Z')
                mesh.transform(matrix2)
            pass

        param_map = libyafaray4_bindings.ParamMap()

        param_map.setString("type", "mesh")
        param_map.setInt("num_vertices", len(mesh.vertices))
        param_map.setInt("num_faces", len(getattr(mesh, face_attr)))
        param_map.setBool("has_orco", hasOrco)
        param_map.setBool("has_uv", hasUV)
        param_map.setBool("is_base_object", is_base_object)
        param_map.setString("visibility", visibility)
        param_map.setInt("object_index", pass_index)
        param_map.setBool("motion_blur_bezier", obj.motion_blur_bezier)
        object_id = self.yaf_scene.createObject(str(ID), param_map)

        for ind, v in enumerate(mesh.vertices):
            if hasOrco:
                self.yaf_scene.addVertexWithOrco(object_id, v.co[0], v.co[1], v.co[2], ov[ind][0], ov[ind][1], ov[ind][2])
            else:
                self.yaf_scene.addVertex(object_id, v.co[0], v.co[1], v.co[2])

        if self.scene.adv_scene_mesh_tesselation == "triangles_only":
            triangles_only = True
        else:
            triangles_only = False

        for index, f in enumerate(getattr(mesh, face_attr)):
            if f.use_smooth:
                isSmooth = True

            if oMat:
                ymaterial = oMat
            else:
                ymaterial = self.getFaceMaterial(mesh.materials, f.material_index, obj.material_slots)
            material_id = self.yaf_scene.getMaterialId(ymaterial)
            co = None
            if hasUV:
                if self.is_preview:
                    co = uv_texture[0].data[index].uv
                else:
                    co = uv_texture.active.data[index].uv

                uv0 = self.yaf_scene.addUv(object_id, co[0][0], co[0][1])
                uv1 = self.yaf_scene.addUv(object_id, co[1][0], co[1][1])
                uv2 = self.yaf_scene.addUv(object_id, co[2][0], co[2][1])

                if len(f.vertices) == 4:
                    uv3 = self.yaf_scene.addUv(object_id, co[3][0], co[3][1])
                    if triangles_only:
                        self.yaf_scene.addTriangleWithUv(object_id, f.vertices[0], f.vertices[1], f.vertices[2], uv0, uv1, uv2, material_id)
                        self.yaf_scene.addTriangleWithUv(object_id, f.vertices[0], f.vertices[2], f.vertices[3], uv0, uv2, uv3, material_id)
                    else:
                        self.yaf_scene.addQuadWithUv(object_id, f.vertices[0], f.vertices[1], f.vertices[2], f.vertices[3], uv0, uv1, uv2, uv3, material_id)
                else:
                    self.yaf_scene.addTriangleWithUv(object_id, f.vertices[0], f.vertices[1], f.vertices[2], uv0, uv1, uv2, material_id)
            else:
                if len(f.vertices) == 4:
                    if triangles_only:
                        self.yaf_scene.addTriangle(object_id, f.vertices[0], f.vertices[1], f.vertices[2], material_id)
                        self.yaf_scene.addTriangle(object_id, f.vertices[0], f.vertices[2], f.vertices[3], material_id)
                    else:
                        self.yaf_scene.addQuad(object_id, f.vertices[0], f.vertices[1], f.vertices[2], f.vertices[3], material_id)
                else:
                    self.yaf_scene.addTriangle(object_id, f.vertices[0], f.vertices[1], f.vertices[2], material_id)

        auto_smooth_enabled = mesh.use_auto_smooth
        auto_smooth_angle = mesh.auto_smooth_angle

        if bpy.app.version >= (2, 80, 0):
            pass  # FIXME BLENDER 2.80-3.00
        else:
            bpy.data.meshes.remove(mesh, do_unlink=False)

        if obj.motion_blur_bezier:
            frame_current = self.scene.frame_current
            for time_step in range(1, 3):
                self.scene.frame_set(frame_current, 0.5 * time_step)
                mesh = self.scene.objects[obj.name].to_mesh(self.scene, True, 'RENDER')
                mesh.update(calc_tessface=True)
                if obj.matrix_world is not None:
                    mesh.transform(obj.matrix_world)
                for ind, v in enumerate(mesh.vertices):
                    if hasOrco:
                        self.yaf_scene.addVertexWithOrcoTimeStep(object_id, v.co[0], v.co[1], v.co[2], ov[ind][0], ov[ind][1], ov[ind][2], time_step)
                    else:
                        self.yaf_scene.addVertexTimeStep(object_id, v.co[0], v.co[1], v.co[2], time_step)
                if bpy.app.version >= (2, 80, 0):
                    pass  # FIXME BLENDER 2.80-3.00
                else:
                    bpy.data.meshes.remove(mesh, do_unlink=False)
            self.scene.frame_set(frame_current, 0.0)
        self.yaf_scene.initObject(object_id, 0)

        if isSmooth and auto_smooth_enabled:
            self.yaf_scene.smoothObjectMesh(object_id, math.degrees(auto_smooth_angle))
        elif isSmooth and obj.type == 'FONT':  # getting nicer result with smooth angle 60 degr. for text objects
            self.yaf_scene.smoothObjectMesh(object_id, 60)
        elif isSmooth:
            self.yaf_scene.smoothObjectMesh(object_id, 181)


    def getFaceMaterial(self, meshMats, matIndex, matSlots):

        ymaterial = "defaultMat"

        #if self.scene.gs_clay_render:
        #    ymaterial = self.materialMap["clay"]
        if len(meshMats) and meshMats[matIndex]:
            mat = meshMats[matIndex]
            ymaterial = mat.name
        else:
            for mat_slots in [ms for ms in matSlots]:
                if mat_slots.material is not None:
                    ymaterial = mat_slots.material.name

        return ymaterial

    def writeParticleStrands(self, object):

        
        renderEmitter = False
        if hasattr(object, 'particle_systems') == False:
            return

        # Check for hair particles:
        for pSys in object.particle_systems:
            if bpy.app.version >= (2, 80, 0):
                continue  # FIXME BLENDER 2.80-3.00
            for mod in [m for m in object.modifiers if (m is not None) and (m.type == 'PARTICLE_SYSTEM')]:
                if (pSys.settings.render_type == 'PATH') and mod.show_render and (pSys.name == mod.particle_system.name):
                    self.logger.printInfo("Exporter: Creating Hair Particle System {!r}".format(pSys.name))
                    tstart = time.time()
                    # TODO: clay particles uses at least materials thikness?
                    if object.active_material is not None:
                        pmaterial = object.active_material

                        if pmaterial.strand.use_blender_units:
                            strandStart = pmaterial.strand.root_size
                            strandEnd = pmaterial.strand.tip_size
                            strandShape = pmaterial.strand.shape
                        else:  # Blender unit conversion
                            strandStart = pmaterial.strand.root_size / 100
                            strandEnd = pmaterial.strand.tip_size / 100
                            strandShape = pmaterial.strand.shape
                    else:
                        pmaterial = "default"  # No material assigned in blender, use default one
                        strandStart = 0.01
                        strandEnd = 0.01
                        strandShape = 0.0

                    matrix = object.matrix_world.copy()
                    for particle in pSys.particles:
                        param_map = libyafaray4_bindings.ParamMap()
                        yi.setCurrentMaterial(pmaterial.name)
                        param_map.setString("type", "curve")
                        param_map.setFloat("strand_start", strandStart)
                        param_map.setFloat("strand_end", strandEnd)
                        param_map.setFloat("strand_shape", strandShape)
                        param_map.setInt("num_vertices", len(particle.hair_keys))
                        param_map.setBool("motion_blur_bezier", object.motion_blur_bezier)
                        self.yaf_scene.createObject(object.name + "_strand_" + str(yi.getNextFreeId()))
                        for location in particle.hair_keys:
                            vertex = matrix * location.co  # use reverse vector multiply order, API changed with rev. 38674
                            yi.addVertex(vertex[0], vertex[1], vertex[2])

                        if object.motion_blur_bezier:
                            frame_current = self.scene.frame_current
                            for time_step in range(1, 3):
                                self.scene.frame_set(frame_current, 0.5 * time_step)
                                matrix = object.matrix_world.copy()
                                for particle in pSys.particles:
                                    for location in particle.hair_keys:
                                        vertex = matrix * location.co  # use reverse vector multiply order, API changed with rev. 38674
                                        yi.addVertexTimeStep(vertex[0], vertex[1], vertex[2], time_step)
                            self.scene.frame_set(frame_current, 0.0)

                        yi.endObject()
                    # TODO: keep object smooth
                    #yi.smoothMesh(0, 60.0)
                    self.logger.printInfo("Exporter: Particle creation time: {0:.3f}".format(time.time() - tstart))

                    if pSys.settings.use_render_emitter:
                        renderEmitter = True
                else:
                    self.writeMesh(object, object.matrix_world.copy())

        # We only need to render emitter object once
        if renderEmitter:
            # ymat = self.materialMap["default"]  /* UNUSED */
            self.writeMesh(object, object.matrix_world.copy())
