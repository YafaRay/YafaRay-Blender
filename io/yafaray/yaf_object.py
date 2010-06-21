import bpy
from yafaray.yaf_properties import *

class yafObject(object):
    def __init__(self, yi):
        self.yi = yi

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

        yi.paramsClearAll()


        if useView:
            yi.paramsSetString("type", "perspective");
        else:
            #camProp = camObj.properties["YafRay"]
            fdist = 1 # only changes for ortho


            camType = scene.camera_type

            if camType == "orthographic":
                yi.paramsSetString("type", "orthographic");
                yi.paramsSetFloat("scale", camera.data.ortho_scale)

            elif camType == "perspective" or camType == "architect":
                
                yi.paramsSetString("type", camType);
                f_aspect = 1.0;
                if (x * x) <= (y * y):
                    f_aspect=(x * x) / (y * y)

                #print "f_aspect: ", f_aspect
                yi.paramsSetFloat("focal", camera.data.lens/(f_aspect*32.0))
                                
                # DOF params, only valid for real camera
                # use DOF object distance if present or fixed DOF
                
                if (camera.data.dof_object):
                    # use DOF object distance
                    dof_distance = camera.data.dof_object.location.length
                else:
                    # use fixed DOF distance
                    dof_distance = camera.data.dof_distance

                yi.paramsSetFloat("dof_distance", dof_distance)
                yi.paramsSetFloat("aperture", scene.aperture)
                # bokeh params
                yi.paramsSetString("bokeh_type", scene.bokeh_type)
                yi.paramsSetFloat("bokeh_rotation",scene.bokeh_rotation)
            
            elif camType == "angular":
                yi.paramsSetString("type", "angular");
                yi.paramsSetBool("circular", scene.circular)
                yi.paramsSetBool("mirrored", scene.mirrored)
                yi.paramsSetFloat("max_angle",scene.max_angle)
                yi.paramsSetFloat("angle", camera.data.lens)
        
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
    def writeMeshes(self,yi,scene,isSmooth = False):
        
        num_ob = 0
        objects = scene.objects
        
        print('I have come to this point')
        
        #scene = bpy.data.scenes[0]
        yi.paramsSetString("type", "shinydiffusemat")
        ymat = yi.createMaterial("defaultMat")
        
        for obj in objects:
            if obj.type in ('LAMP', 'CAMERA', 'EMPTY', 'META', 'ARMATURE'):
                continue
        
            matrix = obj.matrix
            me = obj.data
            me_materials = me.materials
            mesh = obj.create_mesh(True, 'RENDER')   #mesh is created for an object here.
            #mesh_backup = mesh
        
            if matrix:
                mesh.transform(matrix)
            else:
                continue
        
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
        
            yi.paramsClearAll()
            print('number of vertices ' + str(len(mesh.verts)) )
            yi.startGeometry()
            
            print('problem solved')
            
            obType = 0
            
            ID = yi.getNextFreeID()
            
            ''' count triangles '''
            count = 0
            for face in mesh.faces:
                if len(face.verts) == 4:
                    count += 2
                else:
                    count += 1
            
            print("count is : " + str(count) + "number of faces : " + str( len(mesh.faces) ) )
            
            
            yi.startTriMesh(ID, len(mesh.verts), len(mesh.faces) , hasOrco, hasUV, obType)
            print("The name of id is : " + str(ID) )
            
            ind = 0
            for v in mesh.verts:
                if hasOrco:
                    yi.addVertex(v.co[0], v.co[1], v.co[2],ov[ind][0], ov[ind][1], ov[ind][2] )
                    ind +=  1
                else:
                    yi.addVertex(v.co[0], v.co[1], v.co[2])
        
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
                yi.addTriangle(f.verts[0], f.verts[1], f.verts[2],ymat)
                print("without uv case 1")
                
                #print("trying to locate error " + str(index))
        
                if len(f.verts) == 4:
                    #if hasUV == True and (co is not None):
                    #    uv3 = yi.addUV(co.uv4[0], co.uv4[1])
                    #    yi.addTriangle(f.verts[2], f.verts[3], f.verts[0], uv2, uv3, uv0, ymat)
                    #    print("with uv case 2")
                    #else:
                    yi.addTriangle(f.verts[2], f.verts[3], f.verts[0],ymat)
                    print("without uv case 2")
                    
            yi.endTriMesh()
        
            if isSmooth == True:
                yi.smoothMesh(0, mesh.autosmooth_angle)
        
            yi.endGeometry()
            print("work is completed")
            bpy.data.meshes.remove(mesh)
        #del mesh