import bpy
import Mathutils

class OBJECT_OT_get_position(bpy.types.Operator):
    bl_label = "From( get position )"
    bl_idname = "world.get_position"
    bl_description = "Get position from selected sun lamp"

    def invoke(self, context, event):
        sunPosAngle(mode= 'get', val = 'position')
        return{'FINISHED'}

class OBJECT_OT_get_angle(bpy.types.Operator):
    bl_label = "From( get angle )"
    bl_idname = "world.get_angle"
    bl_description = "Get angle from selected sun lamp"

    def invoke(self, context, event):
        sunPosAngle(mode= 'get', val = 'angle')
        return{'FINISHED'}

class OBJECT_OT_update_sun(bpy.types.Operator):
    bl_label = "From( update sun )"
    bl_idname = "world.update_sun"
    bl_description = "Update position and angle of selected sun lamp according to GUI values"

    def invoke(self, context, event):
        sunPosAngle(mode= 'update')
        return{'FINISHED'}


def sunPosAngle(mode="get", val="position"):
    
    warningMessage = True
    active_object  = bpy.context.active_object
    world          = bpy.context.scene.world
    scene          = bpy.context.scene
    
    if active_object :
        if active_object.type == 'LAMP' and active_object.data.type == 'SUN':  #the second condition may also be bpy.context.scene.lamp_type
            warningMessage = False
            print('Come to the main clause')
            if mode == 'get' :
                if val == 'position' :
                    location = Mathutils.Vector(active_object.location)
                    if location.length:
                        point = location.copy().normalize()
                    scene.bg_from = point.copy()
                
                elif val == 'angle' :
                    inv_matrix    = Mathutils.Matrix(active_object.matrix).copy().invert()
                    scene.bg_from = (inv_matrix[0][2],inv_matrix[1][2],inv_matrix[2][2])
            
            elif mode == 'update' :
                
                # get gui from vector and normalize it
                bg_from = Mathutils.Vector(scene.bg_from)
                if bg_from.length:
                    bg_from.normalize()
            
                # set location -----------------------------------
                sundist = Mathutils.Vector(active_object.location).length
                active_object.location = sundist * bg_from
            
                # compute and set rotation -----------------------
                # initialize rotation angle
                ang = 0.0
            
                # set reference vector for angle to -z
                vtrack = Mathutils.Vector(0, 0, -1)
            
                # compute sun ray direction from position
                vray = bg_from.copy()
                if bg_from.length:
                    vray.negate().normalize()
                
                # get angle between sun ray and reference vector
                if vtrack.length and vray.length:
                    ang = vtrack.angle(vray,0.0) #0.0 is the falloff value
                else:
                    print("Zero length input vector - sun angle set to 0")
            
                # get rotation axis
                axis = vtrack.cross(vray).normalize()
            
                # get quaternion representing rotation and get corresponding euler angles
                quat = Mathutils.Quaternion(axis, ang)
                eul = quat.to_euler().unique()
                
                eulrad = []
                for i in eul:
                    eulrad.append(math.radians(i))

                # update sun rotation and redraw the 3D windows
                print(str(eulrad))
                active_object.rotation_euler = eulrad


    else :
        print('There is no active Sun Lamp object in the scene')


def register():
    bpy.types.register(OBJECT_OT_get_position)
    bpy.types.register(OBJECT_OT_get_angle)
    bpy.types.register(OBJECT_OT_update_sun)

def unregister():
    bpy.types.unregister(OBJECT_OT_get_position)
    bpy.types.unregister(OBJECT_OT_get_angle)
    bpy.types.unregister(OBJECT_OT_update_sun)