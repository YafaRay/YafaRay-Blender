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
import yafrayinterface


def multiplyMatrix4x4Vector4(matrix, vector):
    result = mathutils.Vector((0.0, 0.0, 0.0, 0.0))
    for i in range(4):
        result[i] = vector * matrix[i]  # use reverse vector multiply order, API changed with rev. 38674

    return result


class yafObject(object):
    def __init__(self, yi, mMap):
        self.yi = yi
        self.materialMap = mMap

    def setScene(self, scene):

        self.scene = scene

    def createCamera(self):

        yi = self.yi
        yi.printInfo("Exporting Camera")

        camera = self.scene.camera
        render = self.scene.render

        if bpy.types.YAFA_RENDER.useViewToRender and bpy.types.YAFA_RENDER.viewMatrix:
            # use the view matrix to calculate the inverted transformed
            # points cam pos (0,0,0), front (0,0,1) and up (0,1,0)
            # view matrix works like the opengl view part of the
            # projection matrix, i.e. transforms everything so camera is
            # at 0,0,0 looking towards 0,0,1 (y axis being up)

            m = bpy.types.YAFA_RENDER.viewMatrix

            m.transpose()
            inv = m.inverted()

            pos = multiplyMatrix4x4Vector4(inv, mathutils.Vector((0, 0, 0, 1)))
            aboveCam = multiplyMatrix4x4Vector4(inv, mathutils.Vector((0, 1, 0, 1)))
            frontCam = multiplyMatrix4x4Vector4(inv, mathutils.Vector((0, 0, 1, 1)))

            dir = frontCam - pos
            up = aboveCam

        else:
            matrix = camera.matrix_world.copy()  # get cam worldspace transformation matrix, e.g. if cam is parented local does not work
            pos = matrix[3]
            dir = matrix[2]
            up = pos + matrix[1]

        to = pos - dir

        x = int(render.resolution_x * render.resolution_percentage * 0.01)
        y = int(render.resolution_y * render.resolution_percentage * 0.01)

        yi.paramsClearAll()

        if bpy.types.YAFA_RENDER.useViewToRender:
            yi.paramsSetString("type", "perspective")
            yi.paramsSetFloat("focal", 0.7)
            bpy.types.YAFA_RENDER.useViewToRender = False

        else:
            camera = camera.data
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

        yi.paramsSetPoint("from", pos[0], pos[1], pos[2])
        yi.paramsSetPoint("up", up[0], up[1], up[2])
        yi.paramsSetPoint("to", to[0], to[1], to[2])
        yi.createCamera("cam")

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

        ret = yafrayinterface.matrix4x4_t()

        for i in range(4):
            for j in range(4):
                ret.setVal(i, j, matrix[i][j])

        return ret

    def writeObjects(self):

        baseIds = {}
        dupBaseIds = {}
        # export only visible objects
        for obj in [o for o in self.scene.objects if not o.hide_render and o.is_visible(self.scene) \
        and (o.type in {'MESH', 'SURFACE', 'CURVE', 'FONT', 'EMPTY'})]:
            # Exporting dupliObjects as instances: disabled exporting instances when global
            # option "transp. shadows" is on -> crashes yafaray render engine
            if obj.is_duplicator:
                self.yi.printInfo("Processing duplis for: {0}".format(obj.name))
                obj.dupli_list_create(self.scene)

                for obj_dupli in obj.dupli_list:
                    if self.scene.gs_transp_shad:
                        matrix = obj_dupli.matrix.copy()
                        self.writeMesh(obj_dupli.object, matrix)
                    else:
                        if obj_dupli.object.name not in dupBaseIds:
                            dupBaseIds[obj_dupli.object.name] = self.writeInstanceBase(obj_dupli.object)
                        matrix = obj_dupli.matrix.copy()
                        self.writeInstance(dupBaseIds[obj_dupli.object.name], matrix, obj_dupli.object.name)

                if obj.dupli_list is not None:
                    obj.dupli_list_clear()

                # check if object has particle system and uses the option for 'render emitter'
                if hasattr(obj, 'particle_systems'):
                    for pSys in obj.particle_systems:
                        check_rendertype = pSys.settings.render_type in {'OBJECT', 'GROUP'}
                        if check_rendertype and pSys.settings.use_render_emitter:
                            matrix = obj.matrix_world.copy()
                            self.writeMesh(obj, matrix)

            # no need to write empty object from here on, so continue with next object in loop
            elif obj.type == 'EMPTY':
                continue

            # Exporting objects with shared mesh data blocks as instances: disabled exporting instances when global
            # option "transparent shadows" is on -> crashes yafaray render engine
            elif obj.data.users > 1 and not self.scene.gs_transp_shad:
                has_orco = False
                # check materials and textures of object for 'ORCO' texture coordinates
                # if so: do not export them as instances -> gives weird rendering results!
                for mat_slot in [m for m in obj.material_slots if m.material is not None]:
                    for tex in [t for t in mat_slot.material.texture_slots if (t and t.texture and t.use)]:
                        if tex.texture_coords == 'ORCO':
                            has_orco = True
                            break  # break tex loop
                    if has_orco:
                        break  # break mat_slot loop
                if has_orco:
                    self.writeObject(obj)
                else:
                    self.yi.printInfo("Processing shared mesh data node object: {0}".format(obj.name))
                    if obj.data.name not in baseIds:
                        baseIds[obj.data.name] = self.writeInstanceBase(obj)

                    if obj.name not in dupBaseIds:
                        matrix = obj.matrix_world.copy()
                        self.writeInstance(baseIds[obj.data.name], matrix, obj.data.name)

            else:
                if obj.data.name not in baseIds and obj.name not in dupBaseIds:
                    self.writeObject(obj)

    def writeObject(self, obj, matrix=None):

        if not matrix:
            matrix = obj.matrix_world.copy()

        if obj.vol_enable:  # Volume region
            self.writeVolumeObject(obj, matrix)

        elif obj.ml_enable:  # Meshlight
            self.writeMeshLight(obj, matrix)

        elif obj.bgp_enable:  # BGPortal Light
            self.writeBGPortal(obj, matrix)

        elif obj.particle_systems:  # Particle system
            self.writeParticlesObject(obj, matrix)

        else:  # The rest of the object types
            self.writeMesh(obj, matrix)

    def writeInstanceBase(self, obj):

        # Generate unique object ID
        ID = self.yi.getNextFreeID()

        self.yi.printInfo("Exporting Base Mesh: {0} with ID: {1:d}".format(obj.name, ID))

        obType = 512  # Create this geometry object as a base object for instances

        self.writeGeometry(ID, obj, None, obType)  # We want the vertices in object space

        return ID

    def writeInstance(self, oID, obj2WorldMatrix, name):

        self.yi.printInfo("Exporting Instance of {0} [ID = {1:d}]".format(name, oID))

        mat4 = obj2WorldMatrix.to_4x4()
        mat4.transpose()

        o2w = self.get4x4Matrix(mat4)

        self.yi.addInstance(oID, o2w)
        del mat4
        del o2w

    def writeMesh(self, obj, matrix):

        self.yi.printInfo("Exporting Mesh: {0}".format(obj.name))

        # Generate unique object ID
        ID = self.yi.getNextFreeID()

        self.writeGeometry(ID, obj, matrix)  # obType in 0, default, the object is rendered

    def writeBGPortal(self, obj, matrix):

        self.yi.printInfo("Exporting Background Portal Light: {0}".format(obj.name))

        # Generate unique object ID
        ID = self.yi.getNextFreeID()

        self.yi.paramsClearAll()
        self.yi.paramsSetString("type", "bgPortalLight")
        self.yi.paramsSetFloat("power", obj.bgp_power)
        self.yi.paramsSetInt("samples", obj.bgp_samples)
        self.yi.paramsSetInt("object", ID)
        self.yi.paramsSetBool("with_caustic", obj.bgp_with_caustic)
        self.yi.paramsSetBool("with_diffuse", obj.bgp_with_diffuse)
        self.yi.paramsSetBool("photon_only", obj.bgp_photon_only)
        self.yi.createLight(obj.name)

        obType = 256  # Makes object invisible to the renderer (doesn't enter the kdtree)

        self.writeGeometry(ID, obj, matrix, obType)

    def writeMeshLight(self, obj, matrix):

        self.yi.printInfo("Exporting Meshlight: {0}".format(obj.name))

        # Generate unique object ID
        ID = self.yi.getNextFreeID()

        ml_matname = "ML_"
        ml_matname += obj.name + "." + str(obj.__hash__())

        self.yi.paramsClearAll()
        self.yi.paramsSetString("type", "light_mat")
        self.yi.paramsSetBool("double_sided", obj.ml_double_sided)
        c = obj.ml_color
        self.yi.paramsSetColor("color", c[0], c[1], c[2])
        self.yi.paramsSetFloat("power", obj.ml_power)
        ml_mat = self.yi.createMaterial(ml_matname)

        self.materialMap[ml_matname] = ml_mat

        # Export mesh light
        self.yi.paramsClearAll()
        self.yi.paramsSetString("type", "meshlight")
        self.yi.paramsSetBool("double_sided", obj.ml_double_sided)
        c = obj.ml_color
        self.yi.paramsSetColor("color", c[0], c[1], c[2])
        self.yi.paramsSetFloat("power", obj.ml_power)
        self.yi.paramsSetInt("samples", obj.ml_samples)
        self.yi.paramsSetInt("object", ID)
        self.yi.createLight(obj.name)

        self.writeGeometry(ID, obj, matrix, 0, ml_mat)  # obType in 0, default, the object is rendered

    def writeVolumeObject(self, obj, matrix):

        self.yi.printInfo("Exporting Volume Region: {0}".format(obj.name))

        yi = self.yi
        # me = obj.data  /* UNUSED */
        # me_materials = me.materials  /* UNUSED */

        mesh = obj.to_mesh(self.scene, True, 'RENDER')

        if matrix is not None:
            mesh.transform(matrix)
        else:
            return

        yi.paramsClearAll()

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

        min = [1e10, 1e10, 1e10]
        max = [-1e10, -1e10, -1e10]
        vertLoc = []
        for v in mesh.vertices:
            vertLoc.append(v.co[0])
            vertLoc.append(v.co[1])
            vertLoc.append(v.co[2])

            if vertLoc[0] < min[0]:
                min[0] = vertLoc[0]
            if vertLoc[1] < min[1]:
                min[1] = vertLoc[1]
            if vertLoc[2] < min[2]:
                min[2] = vertLoc[2]
            if vertLoc[0] > max[0]:
                max[0] = vertLoc[0]
            if vertLoc[1] > max[1]:
                max[1] = vertLoc[1]
            if vertLoc[2] > max[2]:
                max[2] = vertLoc[2]

            vertLoc = []

        yi.paramsSetFloat("minX", min[0])
        yi.paramsSetFloat("minY", min[1])
        yi.paramsSetFloat("minZ", min[2])
        yi.paramsSetFloat("maxX", max[0])
        yi.paramsSetFloat("maxY", max[1])
        yi.paramsSetFloat("maxZ", max[2])

        yi.createVolumeRegion("VR_" + obj.name + "." + str(obj.__hash__()))

    def writeGeometry(self, ID, obj, matrix, obType=0, oMat=None):

        mesh = obj.to_mesh(self.scene, True, 'RENDER')
        isSmooth = False
        hasOrco = False
        hasUV = mesh.uv_textures

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

        self.yi.paramsClearAll()
        self.yi.startGeometry()

        self.yi.startTriMesh(ID, len(mesh.vertices), len(mesh.faces), hasOrco, hasUV, obType)

        for ind, v in enumerate(mesh.vertices):
            if hasOrco:
                self.yi.addVertex(v.co[0], v.co[1], v.co[2], ov[ind][0], ov[ind][1], ov[ind][2])
            else:
                self.yi.addVertex(v.co[0], v.co[1], v.co[2])

        for index, f in enumerate(mesh.faces):
            if f.use_smooth:
                isSmooth = True

            if oMat is not None:
                ymaterial = oMat
            else:
                ymaterial = self.getFaceMaterial(mesh.materials, f.material_index, obj.material_slots)

            co = None
            if hasUV:
                co = mesh.uv_textures.active.data[index]
                uv0 = self.yi.addUV(co.uv1[0], co.uv1[1])
                uv1 = self.yi.addUV(co.uv2[0], co.uv2[1])
                uv2 = self.yi.addUV(co.uv3[0], co.uv3[1])
                self.yi.addTriangle(f.vertices[0], f.vertices[1], f.vertices[2], uv0, uv1, uv2, ymaterial)
            else:
                self.yi.addTriangle(f.vertices[0], f.vertices[1], f.vertices[2], ymaterial)

            if len(f.vertices) == 4:
                if hasUV:
                    uv3 = self.yi.addUV(co.uv4[0], co.uv4[1])
                    self.yi.addTriangle(f.vertices[2], f.vertices[3], f.vertices[0], uv2, uv3, uv0, ymaterial)
                else:
                    self.yi.addTriangle(f.vertices[2], f.vertices[3], f.vertices[0], ymaterial)

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

        if self.scene.gs_clay_render:
            ymaterial = self.materialMap["clay"]
        elif len(meshMats) and meshMats[matIndex]:
            mat = meshMats[matIndex]
            if mat in self.materialMap:
                ymaterial = self.materialMap[mat]
        else:
            for mat_slot in [ms for ms in matSlots if ms.material in self.materialMap]:
                ymaterial = self.materialMap[mat_slot.material]

        return ymaterial

    def writeParticlesObject(self, object, matrix):

        yi = self.yi
        renderEmitter = False
        if hasattr(object, 'particle_systems') == False:
            return

        # Check for hair particles:
        for pSys in object.particle_systems:
            for mod in [m for m in object.modifiers if (m is not None) and (m.type == 'PARTICLE_SYSTEM')]:
                if (pSys.settings.render_type == 'PATH') and mod.show_render and (pSys.name == mod.particle_system.name):
                    yi.printInfo("Exporter: Creating Particle System {!r}".format(pSys.name))
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
                    yi.printInfo("Exporter: Particle creation time: {0:.3f}".format(time.time() - tstart))

                    if pSys.settings.use_render_emitter:
                        renderEmitter = True
                else:
                    self.writeMesh(object, matrix)

        # We only need to render emitter object once
        if renderEmitter:
            # ymat = self.materialMap["default"]  /* UNUSED */
            self.writeMesh(object, matrix)
