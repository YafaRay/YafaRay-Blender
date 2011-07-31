import bpy
import math
import mathutils
import time
from bpy.props import *


class OBJECT_OT_get_position(bpy.types.Operator):
    bl_label = "From( get position )"
    bl_idname = "world.get_position"
    bl_description = "Get position from selected sun lamp"

    def invoke(self, context, event):
        sunPosAngle(mode = 'get', val = 'position')
        return{'FINISHED'}


class OBJECT_OT_get_angle(bpy.types.Operator):
    bl_label = "From( get angle )"
    bl_idname = "world.get_angle"
    bl_description = "Get angle from selected sun lamp"

    def invoke(self, context, event):
        sunPosAngle(mode = 'get', val = 'angle')
        return{'FINISHED'}


class OBJECT_OT_update_sun(bpy.types.Operator):
    bl_label = "From( update sun )"
    bl_idname = "world.update_sun"
    bl_description = "Update position and angle of selected sun lamp according to GUI values"

    def invoke(self, context, event):
        sunPosAngle(mode = 'update')
        return{'FINISHED'}


def sunPosAngle(mode = "get", val = "position"):

    warningMessage = True
    active_object  = bpy.context.active_object
    world          = bpy.context.scene.world
    scene          = bpy.context.scene

    if active_object:

        if active_object.type == 'LAMP' and active_object.data.type == 'SUN':  # the second condition may also be bpy.context.scene.lamp_type
            warningMessage = False

            if mode == 'get':
                if val == 'position':
                    location = mathutils.Vector(active_object.location)

                    if location.length:
                        point = location.normalized()
                    else:
                        point = location.copy()

                    world.bg_from = point

                elif val == 'angle':
                    inv_matrix    = mathutils.Matrix(active_object.matrix_local).copy().inverted()
                    world.bg_from = (inv_matrix[0][2], inv_matrix[1][2], inv_matrix[2][2])

            elif mode == 'update':

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
                    vray.negate()
                    vray.normalize()

                # get angle between sun ray and reference vector
                if vtrack.length and vray.length:
                    ang = vtrack.angle(vray, 0.0)  # 0.0 is the falloff value
                else:
                    print("Zero length input vector - sun angle set to 0")

                # get rotation axis
                axis = vtrack.cross(vray).normalized()

                # get quaternion representing rotation and get corresponding euler angles
                quat = mathutils.Quaternion(axis, ang)
                eul = quat.to_euler()

                # update sun rotation and redraw the 3D windows
                active_object.rotation_euler = eul

    else:
        print('There is no active Sun Lamp object in the scene')


class RENDER_OT_render_view(bpy.types.Operator):
    bl_label = "Render View"
    bl_idname = "render.render_view"
    bl_description = "Renders using the view in the active 3d viewport"

    @classmethod
    def poll(self, context):

        check_kitems = context.window_manager.keyconfigs.active.keymaps["Screen"]
        kitems = check_kitems.keymap_items

        if not kitems.from_id(bpy.types.YAFA_RENDER.viewRenderKey):
            bpy.types.YAFA_RENDER.viewRenderKey = kitems.new("RENDER_OT_render_view", 'F12', 'RELEASE', False, False, False, True).id
        return context.scene.render.engine  == 'YAFA_RENDER'

    def execute(self, context):

        bpy.types.YAFA_RENDER.useViewToRender = True

        # Get the 3d view under the mouse cursor
        # if the region is not a 3d view
        # then search for the first active one

        view3d = context.region_data

        if not view3d:
            for area in [a for a in bpy.context.window.screen.areas if a.type == "VIEW_3D"]:
                view3d = area.spaces.active.region_3d
                break

        if not view3d or view3d.view_perspective == "ORTHO":
            self.report({'WARNING'}, ("The selected view is not in perspective mode or there was no 3d view available to render."))
            return {"CANCELLED"}

        else:
            bpy.types.YAFA_RENDER.viewMatrix = view3d.view_matrix.copy()
            bpy.ops.render.render('INVOKE_DEFAULT')
            return {'FINISHED'}


class YAF_OT_presets_ior_list(bpy.types.Operator):
    bl_idname = 'material.set_ior_preset'
    bl_label = 'IOR presets'
    index = bpy.props.FloatProperty()
    name = bpy.props.StringProperty()

    @classmethod
    def poll(self, context):
        yaf_mat = context.material
        return yaf_mat

    def execute(self, context):
        yaf_mat = context.material
        bpy.types.YAF_MT_presets_ior_list.bl_label = self.name
        yaf_mat.IOR_refraction = self.index
        return {'FINISHED'}
