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
import mathutils
from bpy.types import Operator


class OBJECT_OT_get_position(Operator):
    bl_label = "From( get position )"
    bl_idname = "world.get_position"
    bl_description = "Get the position of the sun from the selected lamp location"

    def execute(self, context):
        warning_message = sunPosAngle(mode="get", val="position")
        if warning_message:
            self.report({'WARNING'}, (warning_message))
            return {'CANCELLED'}
        else:
            return{'FINISHED'}


class OBJECT_OT_get_angle(Operator):
    bl_label = "From( get angle )"
    bl_idname = "world.get_angle"
    bl_description = "Get the position of the sun from selected lamp angle"

    def execute(self, context):
        warning_message = sunPosAngle(mode="get", val="angle")
        if warning_message:
            self.report({'WARNING'}, (warning_message))
            return {'CANCELLED'}
        else:
            return{'FINISHED'}


class OBJECT_OT_update_sun(Operator):
    bl_label = "From( update sun )"
    bl_idname = "world.update_sun"
    bl_description = "Update the position and angle of selected lamp in 3D View according to GUI values"

    def execute(self, context):
        warning_message = sunPosAngle(mode="update")
        if warning_message:
            self.report({'WARNING'}, (warning_message))
            return {'CANCELLED'}
        else:
            return{'FINISHED'}


def sunPosAngle(mode="get", val="position"):
    active_object = bpy.context.active_object
    scene = bpy.context.scene
    world = scene.world

    if active_object and active_object.type == "LAMP":

        if mode == "get":
            # get the position of the sun from selected lamp 'location'
            if val == "position":
                location = mathutils.Vector(active_object.location)

                if location.length:
                    point = location.normalized()
                else:
                    point = location.copy()

                world.bg_from = point
                return
            # get the position of the sun from selected lamps 'angle'
            elif val == "angle":
                matrix = mathutils.Matrix(active_object.matrix_local).copy()
                world.bg_from = (matrix[0][2], matrix[1][2], matrix[2][2])
                return

        elif mode == "update":

            # get gui from vector and normalize it
            bg_from = mathutils.Vector(world.bg_from).copy()
            if bg_from.length:
                bg_from.normalize()

            # set location
            sundist = mathutils.Vector(active_object.location).length
            active_object.location = sundist * bg_from

            # compute and set rotation
            quat = bg_from.to_track_quat("Z", "Y")
            eul = quat.to_euler()

            # update sun rotation and redraw the 3D windows
            active_object.rotation_euler = eul
            return

    else:
        return "No selected LAMP object in the scene!"


def checkSceneLights():
    scene = bpy.context.scene
    world = scene.world
    
    # expand fuction for include light from 'add sun' or 'add skylight' in sunsky or sunsky2 mode    
    haveLights = False
     # use light create with sunsky, sunsky2 or with use ibl ON
    if world.bg_add_sun or world.bg_background_light or world.bg_use_ibl:
        return True
    # if above is true, this 'for' is not used
    for sceneObj in scene.objects:
        if not sceneObj.hide_render and sceneObj.is_visible(scene): # check lamp, meshlight or portal light object
            if sceneObj.type == "LAMP" or sceneObj.ml_enable or sceneObj.bgp_enable:
                haveLights = True
                break
    #
    return haveLights

class RENDER_OT_render_view(Operator):
    bl_label = "YafaRay render view"
    bl_idname = "render.render_view"
    bl_description = "Renders using the view in the active 3d viewport"

    @classmethod
    def poll(cls, context):

        return context.scene.render.engine == 'YAFA_e2_RENDER'

    def execute(self, context):
        view3d = context.region_data
        bpy.types.YAFA_e2_RENDER.useViewToRender = True
        sceneLights = checkSceneLights()
        scene = context.scene
        # Get the 3d view under the mouse cursor
        # if the region is not a 3d view
        # then search for the first active one
        if not view3d:
            for area in [a for a in bpy.context.window.screen.areas if a.type == "VIEW_3D"]:
                view3d = area.spaces.active.region_3d
                break

        if not view3d or view3d.view_perspective == "ORTHO":
            self.report({'WARNING'}, ("The selected view is not in perspective mode or there was no 3d view available to render."))
            bpy.types.YAFA_e2_RENDER.useViewToRender = False
            return {'CANCELLED'}

        elif not sceneLights and scene.intg_light_method == "Bidirectional":
            self.report({'WARNING'}, ("No lights in the scene and lighting method is Bidirectional!"))
            bpy.types.YAFA_e2_RENDER.useViewToRender = False
            return {'CANCELLED'}

        else:
            bpy.types.YAFA_e2_RENDER.viewMatrix = view3d.view_matrix.copy()
            bpy.ops.render.render('INVOKE_DEFAULT')
            return {'FINISHED'}


class RENDER_OT_render_animation(Operator):
    bl_label = "YafaRay render animation"
    bl_idname = "render.render_animation"
    bl_description = "Render active scene"

    @classmethod
    def poll(cls, context):

        return context.scene.render.engine == 'YAFA_e2_RENDER'

    def execute(self, context):
        sceneLights = checkSceneLights()
        scene = context.scene

        if not sceneLights and scene.intg_light_method == "Bidirectional":
            self.report({'WARNING'}, ("No lights in the scene and lighting method is Bidirectional!"))
            return {'CANCELLED'}

        else:
            bpy.ops.render.render('INVOKE_DEFAULT', animation=True)
            return {'FINISHED'}


class RENDER_OT_render_still(Operator):
    bl_label = "YafaRay render still"
    bl_idname = "render.render_still"
    bl_description = "Render active scene"

    @classmethod
    def poll(cls, context):

        return context.scene.render.engine == 'YAFA_e2_RENDER'

    def execute(self, context):
        sceneLights = checkSceneLights()
        scene = context.scene

        if not sceneLights and scene.intg_light_method == "Bidirectional":
            self.report({'WARNING'}, ("No lights in the scene and lighting method is Bidirectional!"))
            return {'CANCELLED'}

        else:
            bpy.ops.render.render('INVOKE_DEFAULT')
            return {'FINISHED'}


class YAF_OT_presets_ior_list(Operator):
    bl_idname = "material.set_ior_preset"
    bl_label = "IOR presets"
    index = bpy.props.FloatProperty()
    name = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        yaf_mat = context.material
        return yaf_mat.mat_type in {"glass", "rough_glass"}

    def execute(self, context):
        yaf_mat = context.material
        bpy.types.YAF_MT_presets_ior_list.bl_label = self.name
        yaf_mat.IOR_refraction = self.index
        return {'FINISHED'}
