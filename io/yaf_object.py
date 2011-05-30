import bpy
import time
import mathutils
import yafrayinterface


def multiplyMatrix4x4Vector4(matrix, vector):
    result = mathutils.Vector((0.0, 0.0, 0.0, 0.0))
    for i in range(4):
        result[i] = matrix[i] * vector

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
            matrix = camera.matrix_world  # get cam worldspace transformation matrix, e.g. if cam is parented local does not work
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

            if (camera.use_clipping):
                yi.paramsSetFloat("nearClip", camera.clip_start)
                yi.paramsSetFloat("farClip", camera.clip_end)

            if camType == "orthographic":
                yi.paramsSetFloat("scale", camera.ortho_scale)

            elif camType in ["perspective", "architect"]:
                f_aspect = 1.0
                if x < y:
                    f_aspect = x / y

                yi.paramsSetFloat("focal", camera.lens / (f_aspect * 32.0))

                # DOF params, only valid for real camera
                # use DOF object distance if present or fixed DOF

                if camera.dof_object:
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
        for obj in [o for o in self.scene.objects if not o.hide_render and o.is_visible(self.scene) and (o.type == 'MESH' or o.type == 'SURFACE' or o.type == 'CURVE' or o.type == 'FONT')]:
            if obj.is_duplicator:  # Exporting dupliObjects as instances

                #self.writeObject(obj)
                self.yi.printInfo("Processing duplis for: " + obj.name)

                if hasattr(obj, "create_dupli_list"):  # method name changed
                    obj.create_dupli_list(self.scene)
                else:
                    obj.dupli_list_create(self.scene)

                for obj_dupli in obj.dupli_list:

                    if obj_dupli.object.name not in dupBaseIds:
                        dupBaseIds[obj_dupli.object.name] = self.writeInstanceBase(obj_dupli.object)

                    self.writeInstance(dupBaseIds[obj_dupli.object.name], obj_dupli.matrix, obj_dupli.object.name)

                if obj.dupli_list:
                    if hasattr(obj, "free_dupli_list"):  # method name changed
                        obj.free_dupli_list()
                    else:
                        obj.dupli_list_clear()

            elif obj.data.users > 1:  # Exporting objects with shared mesh data blocks as instances

                self.yi.printInfo("Processing shared mesh data node object: " + obj.name)
                if obj.data.name not in baseIds:
                    baseIds[obj.data.name] = self.writeInstanceBase(obj)

                if obj.name not in dupBaseIds:
                    self.writeInstance(baseIds[obj.data.name], obj.matrix_world, obj.data.name)

            else:
                if obj.data.name not in baseIds and obj.name not in dupBaseIds:
                    self.writeObject(obj)

        # checking for empty objects with duplis on them also...
        for empt in [e for e in self.scene.objects if not e.hide_render and e.is_visible(self.scene) and e.type == 'EMPTY']:

            if empt.is_duplicator:
                self.yi.printInfo("Processing duplis for: " + empt.name)

                if hasattr(empt, "create_dupli_list"):  # method name changed
                    empt.create_dupli_list(self.scene)
                else:
                    empt.dupli_list_create(self.scene)

                for empt_dupli in empt.dupli_list:

                    if empt_dupli.object.name not in dupBaseIds:
                        dupBaseIds[empt_dupli.object.name] = self.writeInstanceBase(empt_dupli.object)

                    self.writeInstance(dupBaseIds[empt_dupli.object.name], empt_dupli.matrix, empt_dupli.object.name)

                if empt.dupli_list:
                    if hasattr(empt, "free_dupli_list"):  # method name changed
                        empt.free_dupli_list()
                    else:
                        empt.dupli_list_clear()

    def writeObject(self, obj, matrix = None):

        if not matrix:
            matrix = obj.matrix_world

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

        self.yi.printInfo("Exporting Base Mesh: " + obj.name + " with ID " + str(ID))

        obType = 512  # Create this geometry object as a base object for instances

        self.writeGeometry(ID, obj, None, obType)  # We want the vertices in object space

        return ID

    def writeInstance(self, oID, obj2WorldMatrix, name):

        self.yi.printInfo("Exporting Instance of " + name + " [ID = " + str(oID) + "]")

        mat4 = obj2WorldMatrix.to_4x4()
        mat4.transpose()

        o2w = self.get4x4Matrix(mat4)

        self.yi.addInstance(oID, o2w)
        del mat4
        del o2w

    def writeMesh(self, obj, matrix):

        self.yi.printInfo("Exporting Mesh: " + obj.name)

        # Generate unique object ID
        ID = self.yi.getNextFreeID()

        self.writeGeometry(ID, obj, matrix)  # obType in 0, default, the object is rendered

    def writeBGPortal(self, obj, matrix):

        self.yi.printInfo("Exporting Background Portal Light: " + obj.name)

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

        self.yi.printInfo("Exporting Meshlight: " + obj.name)

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

        self.yi.printInfo("Exporting Volume Region: " + obj.name)

        yi = self.yi
        me = obj.data
        me_materials = me.materials

        if hasattr(obj, "create_mesh"):  # method name changed
            mesh = obj.create_mesh(self.scene, True, 'RENDER')
        else:
            mesh = obj.to_mesh(self.scene, True, 'RENDER')

        if matrix:
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
            if not obj.data.materials[0]:
                yi.printError("Volume object (" + obj.name + ") is missing the material")
            elif not obj.data.materials[0].texture_slots[0].texture:
                yi.printError("Volume object's material (" + obj.name + ") is missing the noise texture")
            else:
                texture = obj.data.materials[0].texture_slots[0].texture

                yi.paramsSetString("type", "NoiseVolume")
                yi.paramsSetFloat("sharpness", obj.vol_sharpness)
                yi.paramsSetFloat("cover", obj.vol_cover)
                yi.paramsSetFloat("density", obj.vol_density)
                yi.paramsSetString("texture", texture.name)

        elif obj.vol_region == 'Grid Volume':
            yi.paramsSetString("type", "GridVolume")

#        elif obj.vol_region == 'Sky Volume':
#            yi.paramsSetString("type", "SkyVolume");

        yi.paramsSetFloat("sigma_a", obj.vol_absorp)
        yi.paramsSetFloat("sigma_s", obj.vol_scatter)
        # yi.paramsSetFloat("l_e", obj.vol_l_e)
        # yi.paramsSetFloat("g", obj.vol_g)
        yi.paramsSetInt("attgridScale", self.scene.world.v_int_attgridres)

        min = [1e10, 1e10, 1e10]
        max = [-1e10, -1e10, -1e10]
        vertLoc = []
        for v in mesh.vertices:
            #print("Scanning vertices ... ")
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

    def writeGeometry(self, ID, obj, matrix, obType = 0, oMat = None):

        if hasattr(obj, "create_mesh"):  # method name changed
            mesh = obj.create_mesh(self.scene, True, 'RENDER')
        else:
            mesh = obj.to_mesh(self.scene, True, 'RENDER')

        isSmooth = False
        hasOrco = False
        # TODO: this may not be the best way to check for uv maps
        hasUV = (len(mesh.uv_textures) > 0)

        # Check if the object has an orco mapped texture
        for mat in [mmat for mmat in mesh.materials if mmat]:
            for m in [mtex for mtex in mat.texture_slots if mtex]:
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
        if matrix:
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

            if oMat:
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

        if isSmooth == True:
            if mesh.use_auto_smooth:
                self.yi.smoothMesh(0, mesh.auto_smooth_angle)
            else:
                if obj.type == 'FONT':  # getting nicer result with smooth angle 60 degr. for text objects
                    self.yi.smoothMesh(0, 60)
                else:
                    self.yi.smoothMesh(0, 181)

        self.yi.endGeometry()

        bpy.data.meshes.remove(mesh)

    def getFaceMaterial(self, meshMats, matIndex, matSlots):

        ymaterial = self.materialMap["default"]

        if not self.scene.gs_clay_render:
            if len(meshMats) and meshMats[matIndex]:
                mat = meshMats[matIndex]

                if mat in self.materialMap:
                    ymaterial = self.materialMap[mat]
            else:
                for mat_slot in matSlots:
                    if mat_slot.material in self.materialMap:
                        ymaterial = self.materialMap[mat_slot.material]

        return ymaterial

    def writeParticlesObject(self, object, matrix):

        yi = self.yi
        renderEmitter = False
        if hasattr(object, 'particle_systems') == False:
            return

        for pSys in object.particle_systems:

            if pSys.settings.render_type == 'PATH':  # Export Hair particles
                yi.printInfo("Exporter: Creating Particle System \"" + pSys.name + "\"")
                tstart = time.time()
                # TODO: clay particles uses at least materials thikness?
                if object.active_material is not None:
                    pmaterial = object.active_material

                    if pmaterial.strand.use_blender_units:
                        strandStart = pmaterial.strand.root_size
                        strandEnd   = pmaterial.strand.tip_size
                        strandShape = pmaterial.strand.shape
                    else:  # Blender unit conversion
                        strandStart = pmaterial.strand.root_size / 100
                        strandEnd   = pmaterial.strand.tip_size / 100
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
                        vertex = location.co
                        yi.addVertex(vertex[0], vertex[1], vertex[2])
                    #this section will be changed after the material settings been exported
                    if self.materialMap[pmaterial]:
                        yi.endCurveMesh(self.materialMap[pmaterial], strandStart, strandEnd, strandShape)
                    else:
                        yi.endCurveMesh(self.materialMap["default"], strandStart, strandEnd, strandShape)
                # TODO: keep object smooth
                #yi.smoothMesh(0, 60.0)
                    yi.endGeometry()
                yi.printInfo("Exporter: Particle creation time: " + str(time.time() - tstart))

                if (pSys.settings.use_render_emitter):
                    renderEmitter = True
        # We only need to render emitter object once
        if renderEmitter:
            ymat = self.materialMap["default"]
            self.writeMesh(object, matrix)
