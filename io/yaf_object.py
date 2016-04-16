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
import yafaray_v3_interface


def multiplyMatrix4x4Vector4(matrix, vector):
    result = mathutils.Vector((0.0, 0.0, 0.0, 0.0))
    for i in range(4):
        result[i] = vector * matrix[i]  # use reverse vector multiply order, API changed with rev. 38674

    return result


class yafObject(object):
    def __init__(self, yi, mMap, preview):
        self.yi = yi
        self.materialMap = mMap
        self.is_preview = preview

    def setScene(self, scene):

        self.scene = scene

    def createCameras(self):

        yi = self.yi
        yi.printVerbose("Exporting Cameras")
    
        render = self.scene.render
        
        class CameraData:
            def __init__ (self, camera, camera_name, view_name):
                self.camera = camera
                self.camera_name = camera_name
                self.view_name = view_name
        
        cameras = []

        if bpy.types.YAFA_V3_RENDER.useViewToRender or not render.use_multiview:
            cameras.append(CameraData(self.scene.camera, "cam", ""))
        else:
            camera_base_name = self.scene.camera.name.rsplit('_',1)[0]

            for view in render.views:
                if view.use and not (render.views_format == "STEREO_3D" and view.name != "left" and view.name != "right"):
                    cameras.append(CameraData(self.scene.objects[camera_base_name+view.camera_suffix], camera_base_name+view.camera_suffix, view.name))

        for cam in cameras:
            if bpy.types.YAFA_V3_RENDER.useViewToRender and bpy.types.YAFA_V3_RENDER.viewMatrix:
                # use the view matrix to calculate the inverted transformed
                # points cam pos (0,0,0), front (0,0,1) and up (0,1,0)
                # view matrix works like the opengl view part of the
                # projection matrix, i.e. transforms everything so camera is
                # at 0,0,0 looking towards 0,0,1 (y axis being up)

                m = bpy.types.YAFA_V3_RENDER.viewMatrix
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

            yi.paramsClearAll()

            if bpy.types.YAFA_V3_RENDER.useViewToRender:
                yi.paramsSetString("type", "perspective")
                yi.paramsSetFloat("focal", 0.7)
                bpy.types.YAFA_V3_RENDER.useViewToRender = False

            else:
                camera = cam.camera.data
                camType = camera.camera_type

                yi.paramsSetString("type", camType)

                if camera.use_clipping:
                    yi.paramsSetFloat("nearClip", camera.clip_start)
                    yi.paramsSetFloat("farClip", camera.clip_end)

                if camType == "orthographic":
                    yi.paramsSetFloat("scale", camera.ortho_scale)

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

                    yi.paramsSetFloat("focal", camera.lens / (f_aspect * sensor_size))

                    # DOF params, only valid for real camera
                    # use DOF object distance if present or fixed DOF
                    if camera.dof_object is not None:
                        # use DOF object distance
                        dist = (pos.xyz - camera.dof_object.location.xyz).length
                        dof_distance = dist
                    else:
                        # use fixed DOF distance
                        dof_distance = camera.dof_distance

                    yi.paramsSetFloat("dof_distance", dof_distance)
                    yi.paramsSetFloat("aperture", camera.aperture)
                    # bokeh params
                    yi.paramsSetString("bokeh_type", camera.bokeh_type)
                    yi.paramsSetFloat("bokeh_rotation", camera.bokeh_rotation)

                elif camType == "angular":
                    yi.paramsSetBool("circular", camera.circular)
                    yi.paramsSetBool("mirrored", camera.mirrored)
                    yi.paramsSetFloat("max_angle", camera.max_angle)
                    yi.paramsSetFloat("angle", camera.angular_angle)

            yi.paramsSetInt("resx", x)
            yi.paramsSetInt("resy", y)

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

            yi.paramsSetPoint("from", pos[0], pos[1], pos[2])
            yi.paramsSetPoint("up", up[0], up[1], up[2])
            yi.paramsSetPoint("to", to[0], to[1], to[2])
            yi.paramsSetString("view_name", cam.view_name)
            yi.createCamera(cam.camera_name)


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

    def get4x4Matrix(self, matrix):

        ret = yafaray_v3_interface.matrix4x4_t()

        for i in range(4):
            for j in range(4):
                ret.setVal(i, j, matrix[i][j])

        return ret

    def writeObject(self, obj, matrix=None):

        if not matrix:
            matrix = obj.matrix_world.copy()

        if obj.vol_enable:  # Volume region
            self.writeVolumeObject(obj, matrix)

        elif obj.ml_enable:  # Meshlight
            self.writeMeshLight(obj, matrix)

        elif obj.bgp_enable:  # BGPortal Light
            self.writeBGPortal(obj, matrix)

        elif obj.particle_systems:  # Particle Hair system
            self.writeParticleStrands(obj, matrix)

        else:  # The rest of the object types
            if self.is_preview and bpy.data.scenes[0].yafaray.preview.enable:
                if "checkers" in obj.name and bpy.data.scenes[0].yafaray.preview.previewBackground == "checker":
                        self.writeMesh(obj, matrix)
                elif "checkers" not in obj.name:
                        self.writeMesh(obj, matrix)
            else:        
                self.writeMesh(obj, matrix)

    def writeInstanceBase(self, obj):

        # Generate unique object ID
        ID = self.yi.getNextFreeID()

        self.yi.printVerbose("Exporting Base Mesh: {0} with ID: {1:d}".format(obj.name, ID))

        obType = 512  # Create this geometry object as a base object for instances

        self.yi.paramsClearAll()
        self.yi.paramsSetInt("obj_pass_index", obj.pass_index)
        
        self.writeGeometry(ID, obj, None, obj.pass_index, obType)  # We want the vertices in object space

        return ID

    def writeInstance(self, oID, obj2WorldMatrix, name):

        self.yi.printVerbose("Exporting Instance of {0} [ID = {1:d}]".format(name, oID))

        mat4 = obj2WorldMatrix.to_4x4()
        # mat4.transpose() --> not needed anymore: matrix indexing changed with Blender rev.42816

        o2w = self.get4x4Matrix(mat4)

        self.yi.addInstance(oID, o2w)
        del mat4
        del o2w

    def writeMesh(self, obj, matrix):

        self.yi.printVerbose("Exporting Mesh: {0}".format(obj.name))

        # Generate unique object ID
        ID = self.yi.getNextFreeID()
        
        self.yi.paramsClearAll()
        self.yi.paramsSetInt("obj_pass_index", obj.pass_index)

        if self.is_preview and bpy.data.scenes[0].yafaray.preview.enable and "preview" in obj.name:
            ymat = self.materialMap[obj.active_material]
            
            if bpy.data.scenes[0].yafaray.preview.previewObject != "" and bpy.data.scenes[0].objects[bpy.data.scenes[0].yafaray.preview.previewObject].type=="MESH":
                    customObj = bpy.data.scenes[0].objects[bpy.data.scenes[0].yafaray.preview.previewObject]
                    previewMatrix = customObj.matrix_world.copy()
                    previewMatrix[0][3]=0
                    previewMatrix[1][3]=0
                    previewMatrix[2][3]=0
                    self.writeGeometry(ID, customObj, previewMatrix, obj.pass_index, 0, ymat)
            else:
                    previewMatrix = obj.matrix_world.copy()
                    previewMatrix[0][3]=0
                    previewMatrix[1][3]=0
                    previewMatrix[2][3]=0
                    
                    self.writeGeometry(ID, obj, previewMatrix, obj.pass_index)
        else:
            self.writeGeometry(ID, obj, matrix, obj.pass_index)  # obType in 0, default, the object is rendered

    def writeBGPortal(self, obj, matrix):

        self.yi.printVerbose("Exporting Background Portal Light: {0}".format(obj.name))

        # Generate unique object ID
        ID = self.yi.getNextFreeID()

        self.yi.paramsClearAll()
        self.yi.paramsSetInt("obj_pass_index", obj.pass_index)
        self.yi.paramsSetString("type", "bgPortalLight")
        self.yi.paramsSetFloat("power", obj.bgp_power)
        self.yi.paramsSetInt("samples", obj.bgp_samples)
        self.yi.paramsSetInt("object", ID)
        self.yi.paramsSetBool("shoot_caustics", obj.bgp_with_caustic)
        self.yi.paramsSetBool("shoot_diffuse", obj.bgp_with_diffuse)
        self.yi.paramsSetBool("photon_only", obj.bgp_photon_only)
        self.yi.createLight(obj.name)

        obType = 256  # Makes object invisible to the renderer (doesn't enter the kdtree)

        self.writeGeometry(ID, obj, matrix, obj.pass_index, obType)

    def writeMeshLight(self, obj, matrix):

        self.yi.printVerbose("Exporting Meshlight: {0}".format(obj.name))

        # Generate unique object ID
        ID = self.yi.getNextFreeID()

        ml_matname = "ML_"
        ml_matname += obj.name + "." + str(obj.__hash__())

        self.yi.paramsClearAll()
        self.yi.paramsSetInt("obj_pass_index", obj.pass_index)
        self.yi.paramsSetString("type", "light_mat")
        self.yi.paramsSetBool("double_sided", obj.ml_double_sided)
        c = obj.ml_color
        self.yi.paramsSetColor("color", c[0], c[1], c[2])
        self.yi.paramsSetFloat("power", obj.ml_power)
        ml_mat = self.yi.createMaterial(ml_matname)

        self.materialMap[ml_matname] = ml_mat

        # Export mesh light
        self.yi.paramsClearAll()
        self.yi.paramsSetInt("obj_pass_index", obj.pass_index)
        self.yi.paramsSetString("type", "meshlight")
        self.yi.paramsSetBool("double_sided", obj.ml_double_sided)
        c = obj.ml_color
        self.yi.paramsSetColor("color", c[0], c[1], c[2])
        self.yi.paramsSetFloat("power", obj.ml_power)
        self.yi.paramsSetInt("samples", obj.ml_samples)
        self.yi.paramsSetInt("object", ID)
        self.yi.createLight(obj.name)

        self.writeGeometry(ID, obj, matrix, obj.pass_index, 0, ml_mat)  # obType in 0, default, the object is rendered

    def writeVolumeObject(self, obj, matrix):

        self.yi.printVerbose("Exporting Volume Region: {0}".format(obj.name))

        yi = self.yi
        # me = obj.data  /* UNUSED */
        # me_materials = me.materials  /* UNUSED */

        yi.paramsClearAll()
        yi.paramsSetInt("obj_pass_index", obj.pass_index)

        if obj.vol_region == 'ExpDensity Volume':
            yi.paramsSetString("type", "ExpDensityVolume")
            yi.paramsSetFloat("a", obj.vol_height)
            yi.paramsSetFloat("b", obj.vol_steepness)

        elif obj.vol_region == 'Uniform Volume':
            yi.paramsSetString("type", "UniformVolume")

        elif obj.vol_region == 'Noise Volume':
            if not obj.active_material:
                yi.printError("Volume object ({0}) is missing the materials".format(obj.name))
            elif not obj.active_material.active_texture:
                yi.printError("Volume object's material ({0}) is missing the noise texture".format(obj.name))
            else:
                texture = obj.active_material.active_texture

                yi.paramsSetString("type", "NoiseVolume")
                yi.paramsSetFloat("sharpness", obj.vol_sharpness)
                yi.paramsSetFloat("cover", obj.vol_cover)
                yi.paramsSetFloat("density", obj.vol_density)
                yi.paramsSetString("texture", texture.name)

        elif obj.vol_region == 'Grid Volume':
            yi.paramsSetString("type", "GridVolume")

        yi.paramsSetFloat("sigma_a", obj.vol_absorp)
        yi.paramsSetFloat("sigma_s", obj.vol_scatter)
        yi.paramsSetInt("attgridScale", self.scene.world.v_int_attgridres)

        # Calculate BoundingBox: get the low corner (minx, miny, minz)
        # and the up corner (maxx, maxy, maxz) then apply object scale,
        # also clamp the values to min: -1e10 and max: 1e10

        mesh = obj.to_mesh(self.scene, True, 'RENDER')
        mesh.transform(matrix)

        vec = [j for v in mesh.vertices for j in v.co]

        yi.paramsSetFloat("minX", max(min(vec[0::3]), -1e10))
        yi.paramsSetFloat("minY", max(min(vec[1::3]), -1e10))
        yi.paramsSetFloat("minZ", max(min(vec[2::3]), -1e10))
        yi.paramsSetFloat("maxX", min(max(vec[0::3]), 1e10))
        yi.paramsSetFloat("maxY", min(max(vec[1::3]), 1e10))
        yi.paramsSetFloat("maxZ", min(max(vec[2::3]), 1e10))

        yi.createVolumeRegion("VR.{0}-{1}".format(obj.name, str(obj.__hash__())))
        bpy.data.meshes.remove(mesh)

    def writeGeometry(self, ID, obj, matrix, pass_index, obType=0, oMat=None):

        mesh = obj.to_mesh(self.scene, True, 'RENDER')
        isSmooth = False
        hasOrco = False
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
                bpy.data.meshes.remove(mesh)
                return
        else:
            if not mesh.faces:
                # if there are no faces, no need to write geometry, remove mesh data then...
                bpy.data.meshes.remove(mesh)
                return

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

        self.yi.paramsClearAll()
        self.yi.startGeometry()

        self.yi.startTriMesh(ID, len(mesh.vertices), len(getattr(mesh, face_attr)), hasOrco, hasUV, obType, pass_index)

        for ind, v in enumerate(mesh.vertices):
            if hasOrco:
                self.yi.addVertex(v.co[0], v.co[1], v.co[2], ov[ind][0], ov[ind][1], ov[ind][2])
            else:
                self.yi.addVertex(v.co[0], v.co[1], v.co[2])

        for index, f in enumerate(getattr(mesh, face_attr)):
            if f.use_smooth:
                isSmooth = True

            if oMat:
                ymaterial = oMat
            else:
                ymaterial = self.getFaceMaterial(mesh.materials, f.material_index, obj.material_slots)

            co = None
            if hasUV:

                if self.is_preview:
                    co = uv_texture[0].data[index].uv
                else:
                    co = uv_texture.active.data[index].uv

                uv0 = self.yi.addUV(co[0][0], co[0][1])
                uv1 = self.yi.addUV(co[1][0], co[1][1])
                uv2 = self.yi.addUV(co[2][0], co[2][1])

                self.yi.addTriangle(f.vertices[0], f.vertices[1], f.vertices[2], uv0, uv1, uv2, ymaterial)
            else:
                self.yi.addTriangle(f.vertices[0], f.vertices[1], f.vertices[2], ymaterial)

            if len(f.vertices) == 4:
                if hasUV:
                    uv3 = self.yi.addUV(co[3][0], co[3][1])
                    self.yi.addTriangle(f.vertices[0], f.vertices[2], f.vertices[3], uv0, uv2, uv3, ymaterial)
                else:
                    self.yi.addTriangle(f.vertices[0], f.vertices[2], f.vertices[3], ymaterial)

        self.yi.endTriMesh()

        if isSmooth and mesh.use_auto_smooth:
            self.yi.smoothMesh(0, math.degrees(mesh.auto_smooth_angle))
        elif isSmooth and obj.type == 'FONT':  # getting nicer result with smooth angle 60 degr. for text objects
            self.yi.smoothMesh(0, 60)
        elif isSmooth:
            self.yi.smoothMesh(0, 181)

        self.yi.endGeometry()

        bpy.data.meshes.remove(mesh)

    def getFaceMaterial(self, meshMats, matIndex, matSlots):

        ymaterial = self.materialMap["default"]

        #if self.scene.gs_clay_render:
        #    ymaterial = self.materialMap["clay"]
        if len(meshMats) and meshMats[matIndex]:
            mat = meshMats[matIndex]
            if mat in self.materialMap:
                ymaterial = self.materialMap[mat]
        else:
            for mat_slots in [ms for ms in matSlots if ms.material in self.materialMap]:
                ymaterial = self.materialMap[mat_slots.material]

        return ymaterial

    def writeParticleStrands(self, object, matrix):

        yi = self.yi
        renderEmitter = False
        if hasattr(object, 'particle_systems') == False:
            return

        # Check for hair particles:
        for pSys in object.particle_systems:
            for mod in [m for m in object.modifiers if (m is not None) and (m.type == 'PARTICLE_SYSTEM')]:
                if (pSys.settings.render_type == 'PATH') and mod.show_render and (pSys.name == mod.particle_system.name):
                    yi.printVerbose("Exporter: Creating Hair Particle System {!r}".format(pSys.name))
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

                    for particle in pSys.particles:
                        if particle.is_exist and particle.is_visible:
                            p = True
                        else:
                            p = False
                        CID = yi.getNextFreeID()
                        yi.paramsClearAll()
                        yi.startGeometry()
                        yi.startCurveMesh(CID, p)
                        for location in particle.hair_keys:
                            vertex = matrix * location.co  # use reverse vector multiply order, API changed with rev. 38674
                            yi.addVertex(vertex[0], vertex[1], vertex[2])
                        #this section will be changed after the material settings been exported
                        if self.materialMap[pmaterial]:
                            yi.endCurveMesh(self.materialMap[pmaterial], strandStart, strandEnd, strandShape)
                        else:
                            yi.endCurveMesh(self.materialMap["default"], strandStart, strandEnd, strandShape)
                    # TODO: keep object smooth
                    #yi.smoothMesh(0, 60.0)
                        yi.endGeometry()
                    yi.printVerbose("Exporter: Particle creation time: {0:.3f}".format(time.time() - tstart))

                    if pSys.settings.use_render_emitter:
                        renderEmitter = True
                else:
                    self.writeMesh(object, matrix)

        # We only need to render emitter object once
        if renderEmitter:
            # ymat = self.materialMap["default"]  /* UNUSED */
            self.writeMesh(object, matrix)
