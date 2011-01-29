import bpy
import math
import mathutils
import time

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
            
            if mode == 'get' :
                if val == 'position' :
                    location = mathutils.Vector(active_object.location)
                    if location.length:
                        point = location.copy().normalize()
                    print(str(point))
                    world.bg_from = point.copy()
                
                elif val == 'angle' :
                    inv_matrix    = mathutils.Matrix(active_object.matrix_local).copy().invert()
                    world.bg_from = (inv_matrix[0][2],inv_matrix[1][2],inv_matrix[2][2])
            
            elif mode == 'update' :
                
                # get gui from vector and normalize it
                bg_from = mathutils.Vector(world.bg_from)
                if bg_from.length:
                    bg_from.normalize()
            
                # set location -----------------------------------
                sundist = mathutils.Vector(active_object.location).length
                active_object.location = sundist * bg_from
            
                # compute and set rotation -----------------------
                # initialize rotation angle
                ang = 0.0
            
                # set reference vector for angle to -z
                vtrack = mathutils.Vector((0, 0, -1))
            
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
                quat = mathutils.Quaternion(axis, ang)
                eul = quat.to_euler().unique()
                
                eulrad = []
                for i in eul:
                    eulrad.append(math.radians(i))

                # update sun rotation and redraw the 3D windows
                print(str(eulrad))
                active_object.rotation_euler = eulrad


    else :
        print('There is no active Sun Lamp object in the scene')

class RENDER_OT_render_view(bpy.types.Operator):
    bl_label = "Render View"
    bl_idname = "render.render_view"
    bl_description = "Renders using the view in the active 3d viewport"
    
    def invoke(self, context, event):
        context.scene.useViewToRender = True

        # pretty much get the first best 3d view and use its view
        # matrix, store it serialized in the scene
        views3d = [s for s in bpy.context.window.screen.areas if s.type == "VIEW_3D"]

        if len(views3d) == 0:
            print("No 3d view found")
            return

        m = views3d[0].spaces[0].region_3d.view_matrix.copy()

        mSerial = [0 for o in range(16)]
        for row in range(4):
            for column in range(4):
                mSerial[column + row * 4] = m[row][column]

        context.scene.viewMatrix = mSerial

        bpy.ops.render.render('INVOKE_DEFAULT')
        return 'FINISHED'


class OBJECT_OT_UpdateCameraType(bpy.types.Operator):
    bl_idname = "object.update_camera_type"
    bl_label = ""

    def execute(self, context):
        if context.camera.camera_type == 'orthographic':
            context.camera.type = 'ORTHO'
        else:
            context.camera.type = 'PERSP'
        return {'FINISHED'}



def register():
    bpy.types.register(OBJECT_OT_get_position)
    bpy.types.register(OBJECT_OT_get_angle)
    bpy.types.register(OBJECT_OT_update_sun)
    bpy.types.register(RENDER_OT_render_view)
    bpy.types.register(OBJECT_OT_UpdateCameraType)

def unregister():
    bpy.types.unregister(OBJECT_OT_get_position)
    bpy.types.unregister(OBJECT_OT_get_angle)
    bpy.types.unregister(OBJECT_OT_update_sun)
    bpy.types.unregister(RENDER_OT_render_view)
    bpy.types.register(OBJECT_OT_UpdateCameraType)

