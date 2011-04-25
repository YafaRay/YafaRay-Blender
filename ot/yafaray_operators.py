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

        if hasattr(check_kitems, "keymap_items"):  # check for api changes in Blender 2.56 rev. 35764
            kitems = check_kitems.keymap_items
        else:
            kitems = check_kitems.items

        if not kitems.from_id(bpy.types.YAFA_RENDER.viewRenderKey):
            bpy.types.YAFA_RENDER.viewRenderKey = kitems.new("RENDER_OT_render_view", 'F12', 'RELEASE', False, False, False, True).id

        return context.scene.render.engine  == 'YAFA_RENDER'

    def draw(self, context):

        split = self.layout.split().column()

        split.label("The selected view is not on perspective mode", icon='ERROR')
        split.label("or there was no 3d view available to render.")

        split.separator()

        split.label("Rendering 3d views in orthographic mode", icon='INFO')
        split.label("is not supported yet.")

    def invoke(self, context, event):

        bpy.types.YAFA_RENDER.useViewToRender = True

        # Get the 3d view unde the mouse cursor
        # if the region is not a 3d view
        # then search for the first active one

        view3d = context.region_data

        if not view3d:
            for area in [a for a in bpy.context.window.screen.areas if a.type == "VIEW_3D"]:
                view3d = area.active_space.region_3d
                break

        if not view3d or view3d.view_perspective == "ORTHO":
            context.window_manager.invoke_popup(self)
            return {'CANCELLED'}

        bpy.types.YAFA_RENDER.viewMatrix = view3d.view_matrix.copy()

        bpy.ops.render.render('INVOKE_DEFAULT')

        return {'FINISHED'}


class RENDER_OT_render_animation(bpy.types.Operator):  # own operator for rendering and to check if render animation was invoked
    bl_label = "Render Active Scene"
    bl_idname = "render.render_animation"
    bl_description = "Render active scene"
    animation = bpy.props.BoolProperty()

    @classmethod
    def poll(self, context):

        check_kitems = context.window_manager.keyconfigs.active.keymaps["Screen"]

        if hasattr(check_kitems, "keymap_items"):  # check for api changes in Blender 2.56 rev. 35764
            kitems = check_kitems.keymap_items
        else:
            kitems = check_kitems.items

        if not kitems.from_id(bpy.types.YAFA_RENDER.renderAnimationKey):
            if self.animation:
                bpy.types.YAFA_RENDER.renderAnimationKey = kitems.new("RENDER_OT_render_animation", 'F12', 'RELEASE', False, False, True, False).id
            else:
                bpy.types.YAFA_RENDER.renderStillKey = kitems.new("RENDER_OT_render_animation", 'F12', 'RELEASE', False, False, False, False).id

        return context.scene.render.engine  == 'YAFA_RENDER'


    def invoke(self, context, event):

        if self.animation:
            bpy.types.YAFA_RENDER.render_Animation = True  # set propertie, so exporter could recognize that render animation was invoked
            bpy.ops.render.render('INVOKE_DEFAULT', animation = True)
        else:
            bpy.types.YAFA_RENDER.render_Animation = False  # set propertie, so exporter could recognize that render animation was invoked
            bpy.ops.render.render('INVOKE_DEFAULT')

        return {'FINISHED'}


class RENDER_OT_refresh_preview(bpy.types.Operator):
    bl_label = "Render View"
    bl_idname = "render.refresh_preview"
    bl_description = "Refreshes the material preview"

    def invoke(self, context, event):
        mat = context.scene.objects.active.active_material
        mat.preview_render_type = mat.preview_render_type
        return {'FINISHED'}


class WORLD_OT_refresh_preview(bpy.types.Operator):
    bl_label = "Refresh World Preview"
    bl_idname = "world.refresh_preview"
    bl_description = "Refreshes the world preview"

    def invoke(self, context, event):
        wrld = context.scene.world
        wrld.ambient_color = wrld.ambient_color
        return {'FINISHED'}


class LAMP_OT_sync_3dview(bpy.types.Operator):
    bl_label = "Sync type with 3D view"
    bl_idname = "lamp.sync_3dview"
    bl_description = "Sets the lamp type on the 3d view"

    def invoke(self, context, event):
        lamp = context.scene.objects.active

        if lamp.type == 'LAMP':
            lampTypeMap = {'area': 'AREA', 'spot': 'SPOT', 'sun': 'SUN', 'point': 'POINT', 'ies': 'SPOT'}
            lamp.data.type = lampTypeMap[lamp.data.lamp_type]

        return {'FINISHED'}
