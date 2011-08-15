import bpy
import math
import mathutils
from bpy.types import Operator
from bpy.props import FloatProperty, StringProperty


class OBJECT_OT_get_position(Operator):
    bl_label = 'From( get position )'
    bl_idname = 'world.get_position'
    bl_description = 'Get position from selected sun lamp'

    def execute(self, context):
        warning_message = sunPosAngle(mode = 'get', val = 'position')
        if warning_message:
            self.report({'WARNING'}, (warning_message))
            return {'CANCELLED'}
        else:
            return{'FINISHED'}


class OBJECT_OT_get_angle(Operator):
    bl_label = 'From( get angle )'
    bl_idname = 'world.get_angle'
    bl_description = 'Get angle from selected sun lamp'

    def execute(self, context):
        warning_message = sunPosAngle(mode = 'get', val = 'angle')
        if warning_message:
            self.report({'WARNING'}, (warning_message))
            return {'CANCELLED'}
        else:
            return{'FINISHED'}


class OBJECT_OT_update_sun(Operator):
    bl_label = 'From( update sun )'
    bl_idname = 'world.update_sun'
    bl_description = 'Update position and angle of selected sun lamp according to GUI values'

    def execute(self, context):
        warning_message = sunPosAngle(mode = 'update')
        if warning_message:
            self.report({'WARNING'}, (warning_message))
            return {'CANCELLED'}
        else:
            return{'FINISHED'}


def sunPosAngle(mode = 'get', val = 'position'):
    active_object = bpy.context.active_object
    scene = bpy.context.scene
    world = scene.world
    warning_message = ''

    if active_object and active_object.type == 'LAMP' and active_object.data.type == 'SUN':

        if mode == 'get':
            if val == 'position':
                location = mathutils.Vector(active_object.location)

                if location.length:
                    point = location.normalized()
                else:
                    point = location.copy()

                world.bg_from = point
                return

            elif val == 'angle':
                inv_matrix = mathutils.Matrix(active_object.matrix_local).copy().inverted()
                world.bg_from = (inv_matrix[0][2], inv_matrix[1][2], inv_matrix[2][2])
                return

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
            return

    else:
        return "No selected Sun lamp object in the scene!"


def checkSceneLights():
    scene = bpy.context.scene

    for l in scene.objects:
        if not l.hide_render and l.is_visible(scene) and l.type == 'LAMP':
            sceneLights = True
            break
        else:
            sceneLights = False
    return sceneLights


class RENDER_OT_render_view(Operator):
    bl_label = 'YafaRay render view'
    bl_idname = 'render.render_view'
    bl_description = 'Renders using the view in the active 3d viewport'

    @classmethod
    def poll(self, context):

        return context.scene.render.engine == 'YAFA_RENDER'

    def execute(self, context):
        view3d = context.region_data
        bpy.types.YAFA_RENDER.useViewToRender = True
        sceneLights = checkSceneLights()
        scene = context.scene
        # Get the 3d view under the mouse cursor
        # if the region is not a 3d view
        # then search for the first active one
        if not view3d:
            for area in [a for a in bpy.context.window.screen.areas if a.type == 'VIEW_3D']:
                view3d = area.spaces.active.region_3d
                break

        if not view3d or view3d.view_perspective == 'ORTHO':
            self.report({'WARNING'}, ("The selected view is not in perspective mode or there was no 3d view available to render."))
            bpy.types.YAFA_RENDER.useViewToRender = False
            return {'CANCELLED'}

        elif not sceneLights and scene.intg_light_method == 'Bidirectional':
            self.report({'WARNING'}, ("No lights in the scene and lighting method is bidirectional!"))
            bpy.types.YAFA_RENDER.useViewToRender = False
            return {'CANCELLED'}

        elif scene.render.use_border:
            self.report({'WARNING'}, ("Border render not yet supported in YafaRay!"))
            # turn off border render
            scene.render.use_border = False
            return {'CANCELLED'}

        else:
            bpy.types.YAFA_RENDER.viewMatrix = view3d.view_matrix.copy()
            bpy.ops.render.render('INVOKE_DEFAULT')
            return {'FINISHED'}


class RENDER_OT_render_animation(Operator):
    bl_label = 'YafaRay render animation'
    bl_idname = 'render.render_animation'
    bl_description = 'Render active scene'

    @classmethod
    def poll(self, context):

        return context.scene.render.engine == 'YAFA_RENDER'

    def execute(self, context):
        sceneLights = checkSceneLights()
        scene = context.scene

        if not sceneLights and scene.intg_light_method == 'Bidirectional':
            self.report({'WARNING'}, ("No lights in the scene and lighting method is bidirectional!"))
            return {'CANCELLED'}

        elif scene.render.use_border:
            self.report({'WARNING'}, ("Border render not yet supported in YafaRay!"))
            # turn off border render
            scene.render.use_border = False
            return {'CANCELLED'}

        else:
            bpy.ops.render.render('INVOKE_DEFAULT', animation = True)
            return {'FINISHED'}


class RENDER_OT_render_still(Operator):
    bl_label = 'YafaRay render still'
    bl_idname = 'render.render_still'
    bl_description = 'Render active scene'

    @classmethod
    def poll(self, context):
        # remove shortcut F12 for blenders render operator, we use our own ;)
        krm = context.window_manager.keyconfigs.active.keymaps['Screen']
        for kren in krm.keymap_items:
            if kren.idname == 'render.render':
                krm.keymap_items.remove(kren)
                break
        # turn off Blenders color management for correct YafaRay render results
        if context.scene.render.use_color_management:
            context.scene.render.use_color_management = False
        return context.scene.render.engine == 'YAFA_RENDER'

    def execute(self, context):
        sceneLights = checkSceneLights()
        scene = context.scene

        if not sceneLights and scene.intg_light_method == 'Bidirectional':
            self.report({'WARNING'}, ("No lights in the scene and lighting method is bidirectional!"))
            return {'CANCELLED'}

        elif scene.render.use_border:
            self.report({'WARNING'}, ("Border render not yet supported in YafaRay!"))
            # turn off border render
            scene.render.use_border = False
            return {'CANCELLED'}
           
        else:
            bpy.ops.render.render('INVOKE_DEFAULT')
            return {'FINISHED'}


class YAF_OT_presets_ior_list(Operator):
    bl_idname = 'material.set_ior_preset'
    bl_label = 'IOR presets'
    index = bpy.props.FloatProperty()
    name = bpy.props.StringProperty()

    @classmethod
    def poll(self, context):
        yaf_mat = context.material
        return yaf_mat.mat_type == 'glass' or yaf_mat.mat_type == 'rough_glass'

    def execute(self, context):
        yaf_mat = context.material
        bpy.types.YAF_MT_presets_ior_list.bl_label = self.name
        yaf_mat.IOR_refraction = self.index
        return {'FINISHED'}
