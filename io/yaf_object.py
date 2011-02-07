import bpy
import time
import mathutils

def multiplyMatrix4x4Vector4(matrix, vector):
    result = mathutils.Vector((0.0, 0.0, 0.0, 0.0))
    for i in range(4):
        result[i] = matrix[i] * vector

    return result

class yafObject(object):
    def __init__(self, yi, mMap):
        self.yi = yi
        self.materialMap = mMap

    def createCamera(self, yi, scene, useView = False):
        
        self.yi.printInfo("Exporting Camera")

        camera = scene.camera
        render = scene.render

        if bpy.types.YAFA_RENDER.useViewToRender and bpy.types.YAFA_RENDER.viewMatrix:
            # use the view matrix to calculate the inverted transformed
            # points cam pos (0,0,0), front (0,0,1) and up (0,1,0)
            # view matrix works like the opengl view part of the
            # projection matrix, i.e. transforms everything so camera is
            # at 0,0,0 looking towards 0,0,1 (y axis being up)

            m = bpy.types.YAFA_RENDER.viewMatrix

            m.transpose()
            inv = m.invert()

            pos = multiplyMatrix4x4Vector4(inv, mathutils.Vector((0, 0, 0, 1)))
            aboveCam = multiplyMatrix4x4Vector4(inv, mathutils.Vector((0, 1, 0, 1)))
            frontCam = multiplyMatrix4x4Vector4(inv, mathutils.Vector((0, 0, 1, 1)))

            dir = frontCam - pos
            up = aboveCam

        else:
            matrix = camera.matrix_local # this change is recent
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

            yi.paramsSetString("type", camType);

            if camType == "orthographic":
                yi.paramsSetFloat("scale", camera.ortho_scale)

            elif camType in ["perspective", "architect"]:
                f_aspect = 1.0;
                if x < y:
                    f_aspect= x / y

                yi.paramsSetFloat("focal", camera.lens/(f_aspect*32.0))

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
        bb = object.bound_box   #look bpy.types.Object if there is any problem

        min = [1e10, 1e10, 1e10]
        max = [-1e10, -1e10, -1e10]
    
        for corner in bb:
            for i in range(3):
                if corner[i] < min[i]:
                    min[i] = corner[i]
                if corner[i] > max[i]:
                    max[i] = corner[i]

        return min, max



    #extracts data from all the meshes of a scene    
    def writeMesh(self,yi,scene, ID, obj, matrix, ymat = None, isSmooth = False):

        #matrix = obj.matrix_local #recent change
        me = obj.data
        me_materials = me.materials
        mesh = obj.create_mesh(scene, True, 'RENDER') # mesh is created for an object here.
            
        hasOrco = False
        # TODO: this may not be the best way to check for uv maps
        hasUV   = (len(mesh.uv_textures) > 0)

        # Check if the object has an orco mapped texture
        for mat in mesh.materials:
            if mat == None: continue
            for m in mat.texture_slots:
                if m is None:
                    continue
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
                if delta[i] < 0.0001: delta[i] = 1

            # use untransformed mesh's vertices
            for v in mesh.vertices:
                normCo = []
                for i in range(3):
                    normCo.append(2 * (v.co[i] - bbMin[i]) / delta[i] - 1)

                ov.append([normCo[0], normCo[1], normCo[2]])

        # only transform the mesh after orcos have been stored
        if matrix:
            mesh.transform(matrix)
        else:
            return
        
        self.yi.paramsClearAll()
        self.yi.startGeometry()
        
        obType = 0
            
        #ID = self.yi.getNextFreeID()

        self.yi.startTriMesh(ID, len(mesh.vertices), len(mesh.faces), hasOrco, hasUV, obType)
        #print("The name of id is : " + str(ID) )
            
        for ind, v in enumerate(mesh.vertices):
            if hasOrco:
                self.yi.addVertex(v.co[0], v.co[1], v.co[2], ov[ind][0], ov[ind][1], ov[ind][2])
            else:
                self.yi.addVertex(v.co[0], v.co[1], v.co[2])

        for index, f in enumerate(mesh.faces):
            if f.use_smooth == True:
                isSmooth = True
                
            fmat = self.materialMap["default"] # fallback is always the default mat
            
            # get the face material if none is provided to override
            if scene.gs_clay_render:
                fmat = self.materialMap["default"]
            elif len(mesh.materials):
                mat = mesh.materials[f.material_index]
                if mat in self.materialMap:
                    fmat = self.materialMap[mat]
                elif ymat:
                    fmat = ymat
            elif ymat:
                fmat = ymat

            co = None
            if hasUV:
                co = mesh.uv_textures.active.data[index]
            
            if hasUV:
                uv0 = yi.addUV(co.uv1[0], co.uv1[1])
                uv1 = yi.addUV(co.uv2[0], co.uv2[1])
                uv2 = yi.addUV(co.uv3[0], co.uv3[1])
                yi.addTriangle(f.vertices[0], f.vertices[1], f.vertices[2], uv0, uv1, uv2, fmat)
            else:
                self.yi.addTriangle(f.vertices[0], f.vertices[1], f.vertices[2], fmat)
                
            #print("trying to locate error " + str(index))
        
            if len(f.vertices) == 4:
                if hasUV:
                    uv3 = yi.addUV(co.uv4[0], co.uv4[1])
                    yi.addTriangle(f.vertices[2], f.vertices[3], f.vertices[0], uv2, uv3, uv0, fmat)
                else:
                    self.yi.addTriangle(f.vertices[2], f.vertices[3], f.vertices[0], fmat)
                    
        self.yi.endTriMesh()
        
        if isSmooth == True:
            self.yi.smoothMesh(0, mesh.auto_smooth_angle)
        
        self.yi.endGeometry()
        bpy.data.meshes.remove(mesh)


    # write the object using the given transformation matrix (for duplis)
    # if no matrix is given (usual case) use the object's matrix
    
    def writeObject(self, yi, scene, obj, matrix = None):
        
        yi.printInfo("Exporting Object: " + obj.name)
        
        #create a default material
        self.yi.paramsClearAll()
        ymat = self.materialMap["default"]

        # Generate unique object ID
        ID = self.yi.getNextFreeID()

        isMeshlight = obj.ml_enable
        isVolume = obj.vol_enable
        isBGPL = obj.bgp_enable
        
        #more codes can be added in this part later
        if isMeshlight:
            
            ml_matname = "ML_"
            ml_matname += obj.name + "." + str(obj.__hash__())
            
            yi.paramsClearAll();
            yi.paramsSetString("type", "light_mat");
            yi.paramsSetBool("double_sided", obj.ml_double_sided)
            c = obj.ml_color
            yi.paramsSetColor("color", c[0], c[1], c[2])
            yi.paramsSetFloat("power", obj.ml_power)
            ml_mat = yi.createMaterial(ml_matname);
            
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
        
        # Export BGPortalLight DT
        if isBGPL:
            self.yi.paramsClearAll()
            self.yi.paramsSetString("type", "bgPortalLight")
            self.yi.paramsSetFloat("power", obj.bgp_power)
            self.yi.paramsSetInt("samples", obj.bgp_samples)
            self.yi.paramsSetInt("object", ID)
            self.yi.paramsSetBool("with_caustic", obj.bgp_with_caustic)
            self.yi.paramsSetBool("with_diffuse", obj.bgp_with_diffuse)
            self.yi.paramsSetBool("photon_only", obj.bgp_photon_only)
            self.yi.createLight(obj.name)
        
        # Object Material

        ymaterial = None

        if isMeshlight:
            ymaterial = ml_mat
        else:
            if scene.gs_clay_render:
                ymaterial = ymat
            elif obj.type == 'CURVE':
                curve = obj.data
                if len(curve.materials) > 0:
                    mat = curve.materials[0]
                    ymaterial = self.materialMap[mat]
                else:
                    ymaterial = self.materialMap["default"]
            else:
                if len(obj.data.materials) and obj.data.materials[0]:
                    mat = obj.data.materials[0]
                    
                    if mat in self.materialMap:
                        ymaterial = self.materialMap[mat]
                    else:
                        ymaterial = self.materialMap["default"]
                else:
                    for mat_slot in obj.material_slots:
                        if mat_slot.material in self.materialMap:
                            ymaterial = self.materialMap[mat_slot.material]
                        else:
                            ymaterial = self.materialMap["default"]
                            
                    if not ymaterial:
                        yi.printWarning("Object \"" + obj.name + "\" has no material asigned.")
                        ymaterial = self.materialMap["default"]
        
        if isBGPL:
            self.writeMesh(yi, scene, ID, obj, matrix, ymaterial)
        
        elif isVolume:
            self.writeVolumeObject(yi, scene, obj, ID, ymaterial)
            
        elif type(obj.particle_systems)==bpy.types.ParticleSystems:
            self.writeParticlesObject(yi, scene, obj, ID)
            
        else:
            self.writeMesh(yi, scene, ID, obj, matrix, ymaterial)

    def writeParticlesObject(self, yi, scene, object, ID):
        
        renderEmitter = False
        
        if hasattr(object,'particle_systems') == False:
            return

        for pSys in object.particle_systems:
            
            if (pSys.settings.ren_as == 'PATH'):
                # Export particles
                #yi.printInfo("Exporter: Creating Particle System \"" + pSys.getName() + "\"")
                tstart = time.time()
                
                # get particles material (keeps particles thikness too)
                # TODO: clay particles uses at least materials thikness?
                if object.active_material is not None:
                    pmaterial = object.active_material
                    
                    if pmaterial.strand.blender_units :
                        strandStart = pmaterial.strand.root_size
                        strandEnd   = pmaterial.strand.tip_size
                        strandShape = pmaterial.strand.shape
                    else:
                        # Blender unit conversion
                        strandStart = pmaterial.strand.root_size/100
                        strandEnd   = pmaterial.strand.tip_size/100
                        strandShape = pmaterial.strand.shape
                else:
                    # No material assigned in blender, use default one
                    pmaterial = "default"
                    strandStart = 0.01
                    strandEnd = 0.01
                    strandShape = 0.0
                    
                # Workaround to API bug, getLoc() is empty for particles system > 1
                # (object has more than one particle system assigned)
                #pSys.getLoc()
                # Workaround end
                CID = yi.getNextFreeID()
                yi.paramsClearAll()
                yi.startGeometry()
                yi.startCurveMesh(CID, len(pSys.particles))
                for particle in pSys.particles:
                    #for vertex in path:
                    location = particle.location
                    yi.addVertex(location[0], location[1], location[2])
                    #this section will be changed after the material settings been exported
                if self.materialMap[pmaterial]:
                    yi.endCurveMesh(self.materialMap[pmaterial], strandStart, strandEnd, strandShape)
                else:
                    yi.endCurveMesh(self.materialMap["default"], strandStart, strandEnd, strandShape)
                # TODO: keep object smooth
                #yi.smoothMesh(0, 60.0)
                yi.endGeometry()
                yi.printInfo("Exporter: Particle creation time: " + str(time.time()-tstart))
                
                if (pSys.settings.emitter):
                    renderEmitter = True
        # We only need to render emitter object once
        if renderEmitter:
            ymat = self.materialMap["default"]
            self.writeMesh(yi, scene, ID, object, None, ymat)

    def writeVolumeObject(self, yi, scene, obj, ID, ymaterial = None):

        
        matrix = obj.matrix_local #recent change
        me = obj.data
        me_materials = me.materials
        
        if scene is None:
            yi.printError("scene is None ...")
        else:
            yi.printInfo(str(scene))
        mesh = obj.create_mesh(scene,True, 'RENDER')   #mesh is created for an object here.
        
            
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
            yi.paramsSetString("type", "UniformVolume");
        
        elif obj.vol_region == 'Noise Volume':
            if not obj.data.materials[0]:
                yi.printError("Volume object (" + obj.name + ") is missing the material")
            elif not obj.data.materials[0].texture_slots[0].texture:
                yi.printError("Volume object's material (" + obj.name + ") is missing the noise texture")#
            else:
                texture = obj.data.materials[0].texture_slots[0].texture

                yi.paramsSetString("type", "NoiseVolume");
                yi.paramsSetFloat("sharpness", obj.vol_sharpness)
                yi.paramsSetFloat("cover", obj.vol_cover)
                yi.paramsSetFloat("density", obj.vol_density)
                yi.paramsSetString("texture", texture.name)
        
        elif obj.vol_region == 'Grid Volume':
            yi.paramsSetString("type", "GridVolume");
        
#        elif obj.vol_region == 'Sky Volume':
#            yi.paramsSetString("type", "SkyVolume");
        
        yi.paramsSetFloat("sigma_a", obj.vol_absorp)
        yi.paramsSetFloat("sigma_s", obj.vol_scatter)
        # yi.paramsSetFloat("l_e", obj.vol_l_e)
        # yi.paramsSetFloat("g", obj.vol_g)
        yi.paramsSetInt("attgridScale", scene.world.v_int_attgridres)
        
        
        min = [1e10, 1e10, 1e10]
        max = [-1e10, -1e10, -1e10]
        vertLoc =[]
        for v in mesh.vertices:
            #print("Scanning vertices ... ")
            vertLoc.append(v.co[0])
            vertLoc.append(v.co[1])
            vertLoc.append(v.co[2])
            
            if vertLoc[0] < min[0]: min[0] = vertLoc[0]
            if vertLoc[1] < min[1]: min[1] = vertLoc[1]
            if vertLoc[2] < min[2]: min[2] = vertLoc[2]
            if vertLoc[0] > max[0]: max[0] = vertLoc[0]
            if vertLoc[1] > max[1]: max[1] = vertLoc[1]
            if vertLoc[2] > max[2]: max[2] = vertLoc[2]
            
            vertLoc = []
                
        yi.paramsSetFloat("minX", min[0])
        yi.paramsSetFloat("minY", min[1])
        yi.paramsSetFloat("minZ", min[2])
        yi.paramsSetFloat("maxX", max[0])
        yi.paramsSetFloat("maxY", max[1])
        yi.paramsSetFloat("maxZ", max[2])
        
        yi.createVolumeRegion(obj.name + "." + str(obj.__hash__()) + "." + str(ID))
        return

