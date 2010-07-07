import bpy
from yafaray.yaf_properties import *

class yafObject(object):
    def __init__(self, yi):
        self.yi = yi
        self.materialMap = {}

    def createCamera(self,yi,scene,useView = False):
        
        print("INFO: Exporting Camera")

        camera = scene.camera
        matrix = camera.matrix
        render = scene.render
        
        #renderData = scene.getRenderingContext()
        #
        #if not useView:
        #    camObj = scene.objects.camera
        #    camera = camObj.getData()
        #
        if useView:
            # use the view matrix to calculate the inverted transformed
            # points cam pos (0,0,0), front (0,0,1) and up (0,1,0)
            # view matrix works like the opengl view part of the
            # projection matrix, i.e. transforms everything so camera is
            # at 0,0,0 looking towards 0,0,1 (y axis being up)
        
            m = matrix.copy()
            m.transpose()
            inv = m.invert()
            pos = inv * mathutils.Vector(0, 0, 0, 1)
            aboveCam = inv * mathutils.Vector(0, 1, 0, 1)
            frontCam = inv * mathutils.Vector(0, 0, 1, 1)
            dir = frontCam - pos
            up = aboveCam - pos

        else:

            pos = matrix[3]
            dir = matrix[2]
            up = matrix[1]

        to = [pos[0] - dir[0], pos[1] - dir[1], pos[2] - dir[2]]
        
        x = int(render.resolution_x * render.resolution_percentage * 0.01)
        y = int(render.resolution_y * render.resolution_percentage * 0.01)
        
        #print("I am in the camera creation code")

        yi.paramsClearAll()


        if useView:
            yi.paramsSetString("type", "perspective");
        else:
            #camProp = camObj.properties["YafRay"]
            fdist = 1 # only changes for ortho

            camera = camera.data
            camType = camera.camera_type

            if camType == "orthographic":
                yi.paramsSetString("type", "orthographic");
                yi.paramsSetFloat("scale", camera.ortho_scale)

            elif camType == "perspective" or camType == "architect":
                
                yi.paramsSetString("type", camType);
                f_aspect = 1.0;
                if (x * x) <= (y * y):
                    f_aspect=(x * x) / (y * y)

                #print "f_aspect: ", f_aspect
                yi.paramsSetFloat("focal", camera.lens/(f_aspect*32.0))
                                
                # DOF params, only valid for real camera
                # use DOF object distance if present or fixed DOF
                
                if (camera.dof_object):
                    # use DOF object distance
                    dof_distance = camera.dof_object.location.length
                else:
                    # use fixed DOF distance
                    dof_distance = camera.dof_distance

                yi.paramsSetFloat("dof_distance", dof_distance)
                yi.paramsSetFloat("aperture", camera.aperture)
                # bokeh params
                yi.paramsSetString("bokeh_type", camera.bokeh_type)
                yi.paramsSetFloat("bokeh_rotation",camera.bokeh_rotation)
            
            elif camType == "angular":
                yi.paramsSetString("type", "angular");
                yi.paramsSetBool("circular", camera.circular)
                yi.paramsSetBool("mirrored", camera.mirrored)
                yi.paramsSetFloat("max_angle",camera.max_angle)
                yi.paramsSetFloat("angle", camera.lens)
        
        yi.paramsSetInt("resx", x)
        yi.paramsSetInt("resy", y)

        yi.paramsSetPoint("from", pos[0], pos[1], pos[2])
        yi.paramsSetPoint("up", pos[0] + up[0], pos[1] + up[1], pos[2] + up[2])
        yi.paramsSetPoint("to", to[0], to[1], to[2])
        yi.createCamera("cam")


    def getBBCorners(self,object):
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
    def writeMesh(self,yi,scene,obj,ID,ymat = None,isSmooth = False):
        
        #num_ob = 0
        #objects = scene.objects
        #
        #print('I have come to this point')
        
        #scene = bpy.data.scenes[0]
        #if ymat is None :
        #    self.yi.paramsSetString("type", "shinydiffusemat")
        #    ymat = self.yi.createMaterial("defaultMat")
        
        #for obj in objects:
        #    if obj.type in ('LAMP', 'CAMERA', 'EMPTY', 'META', 'ARMATURE'):
        #        continue
        print("The id is : " + str(ID))
            
        matrix = obj.matrix
        me = obj.data
        me_materials = me.materials
        mesh = obj.create_mesh(scene,True, 'RENDER')   #mesh is created for an object here.
        #mesh_backup = mesh
            
        #self.writeObject(yi, obj, scene, matrix)
            
            
        
        if matrix:
            mesh.transform(matrix)
        else:
            return
        
        hasOrco = False
        hasUV   = False
            
        # Check if the object has an orco mapped texture
        for mat in mesh.materials:
            if mat == None: continue
            for m in mat.texture_slots:
                if m is None:
                    continue
                if m.texture_coordinates == 'ORCO':
                    hasOrco = True
                    break
            if hasOrco:
                break

        vert_count = 0
        if hasOrco:
            # Keep a copy of the untransformed vertex and bring them
            # into a (-1 -1 -1) (1 1 1) bounding box
            ov = []
            bbMin, bbMax = self.getBBCorners(obj)
            # print bbMin, bbMax
        
            delta = []
                
            for i in range(3):
                delta.append(bbMax[i] - bbMin[i])
                if delta[i] < 0.0001: delta[i] = 1
                # print "delta", delta
            for v in mesh.verts:
                normCo = []
                vert_count = vert_count + 1
                print('I am here')
                for i in range(3):
                    #print(v)
                    normCo.append(2 * (v.co[i] - bbMin[i]) / delta[i] - 1)
                ov.append([normCo[0], normCo[1], normCo[2]])
        
        self.yi.paramsClearAll()
        print('number of vertices ' + str(len(mesh.verts)) )
        self.yi.startGeometry()
            
        print('problem solved')
            
        obType = 0
            
        #ID = self.yi.getNextFreeID()
            
        ''' count triangles '''
        count = 0
        for face in mesh.faces:
            if len(face.verts) == 4:
                count += 2
            else:
                count += 1
            
        print("count is : " + str(count) + "number of faces : " + str( len(mesh.faces) ) )
            
            
        self.yi.startTriMesh(ID, len(mesh.verts), len(mesh.faces) , hasOrco, hasUV, obType)
        print("The name of id is : " + str(ID) )
            
        ind = 0
        for v in mesh.verts:
            if hasOrco:
                self.yi.addVertex(v.co[0], v.co[1], v.co[2],ov[ind][0], ov[ind][1], ov[ind][2] )
                ind +=  1
            else:
                self.yi.addVertex(v.co[0], v.co[1], v.co[2])
        
        #print("before creating material ....")
        ##dummy material     
        #yi.paramsClearAll()
        ##end of dummy material
        #print("after creating material ...")
        co = None
        #ymat = None

        for index,f in enumerate(mesh.faces):
            if f.smooth == True:
                isSmooth = True
                
                
            if mesh.active_uv_texture is not None :
                co = mesh.active_uv_texture.data[index]
                hasUV = True
            #
            #if hasUV == True and (co is not None) :
            #    uv0 = yi.addUV(co.uv1[0], co.uv1[1])
            #    uv1 = yi.addUV(co.uv2[0], co.uv2[1])
            #    uv2 = yi.addUV(co.uv3[0], co.uv3[1])
            #    yi.addTriangle(f.verts[0], f.verts[1], f.verts[2], uv0, uv1, uv2, ymat)
            #    print("with uv case 1")
            #
            #else:
            self.yi.addTriangle(f.verts[0], f.verts[1], f.verts[2],ymat)
            print("without uv case 1")
                
            #print("trying to locate error " + str(index))
        
            if len(f.verts) == 4:
                #if hasUV == True and (co is not None):
                #    uv3 = yi.addUV(co.uv4[0], co.uv4[1])
                #    yi.addTriangle(f.verts[2], f.verts[3], f.verts[0], uv2, uv3, uv0, ymat)
                #    print("with uv case 2")
                #else:
                self.yi.addTriangle(f.verts[2], f.verts[3], f.verts[0],ymat)
                print("without uv case 2")
                    
        self.yi.endTriMesh()
        
        if isSmooth == True:
            self.yi.smoothMesh(0, mesh.autosmooth_angle)
        
        self.yi.endGeometry()
        print("work is completed")
        bpy.data.meshes.remove(mesh)
        #del mesh


    # write the object using the given transformation matrix (for duplis)
    # if no matrix is given (usual case) use the object's matrix
    
    def writeObject(self, yi, scene, obj):
        
        print("INFO: Exporting Object: " + obj.name)
        
        materialMap = {}
        
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
            
            #ml_matname = "ML_"
            #ml_matname += obj.name + "." + str(obj.__hash__())
            #
            #yi.paramsClearAll();
            #yi.paramsSetString("type", "light_mat");
            #yi.paramsSetBool("double_sided", scene.ml_double_sided)
            #c = scene.ml_color
            #yi.paramsSetColor("color", c[0], c[1], c[2])
            #yi.paramsSetFloat("power", scene.ml_power)
            #ml_mat = yi.createMaterial(ml_matname);
            #
            #materialMap[ml_matname] = ml_mat
            
            
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
        #if isMeshlight:
        #    ymaterial = ml_mat
        #else:
        #    if scene.gs_clay_render == True:
        #        ymaterial = materialMap["default"]
        #    elif obj.type == 'CURVE':
        #        curve = obj.data
        #        if len(curve.materials) != 0:
        #            mat = curve.materials[0]
        #            ymaterial = self.materialMap[mat]
        #        else:
        #            ymaterial = self.materialMap["default"]
        #    else:
        #        if obj.getData().getMaterials():
        #            ymaterial = None
        #        else:
        #            ymaterial = self.materialMap["default"]

        
        if isBGPL:
            self.writeMesh(yi, scene, obj, ID, ymat)
        else:
            self.writeMesh(yi, scene, obj, ID, ymat)
    
    
    def writeMeshes(self,yi,scene,isSmooth = False):
        
        objects = scene.objects
        self.yi.paramsClearAll()
        self.yi.paramsSetString("type", "shinydiffusemat")
        
        ymat = self.yi.createMaterial("defaultMat")
        self.materialMap["default"] = ymat
        
        for obj in objects:
            if obj.type in ('LAMP', 'CAMERA', 'EMPTY', 'META', 'ARMATURE'):
                continue
            else:
                self.writeObject(yi,scene,obj)
        
