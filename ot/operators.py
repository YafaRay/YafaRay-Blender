# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
import mathutils
from bpy.props import (StringProperty)
# noinspection PyUnresolvedReferences
from bpy.types import Operator

from ..util.properties_annotations import replace_properties_with_annotations

if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed,
    # before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the
    # "libyafaray4_bindings" compiled module is installed on. Assuming that the YafaRay-Plugin exporter is installed
    # in a folder named "yafaray4" within the addons Blender directory
    # noinspection PyUnresolvedReferences
    from yafaray4 import global_vars
else:
    from .. import global_vars


class CreateNode(Operator):
    bl_idname = "yafaray4.new_node_tree"
    bl_label = "Create YafaRay Node Tree"
    bl_description = "Creates a new YafaRay Node Tree"

    # noinspection PyUnusedLocal
    def execute(self, context):
        bpy.ops.node.new_node_tree(type="YAFARAY4_NODE_TREE")
        return {'FINISHED'}


class NewMaterial(Operator):
    bl_idname = "yafaray4.material_new"
    bl_label = "Create New Material"
    bl_description = "Creates a new YafaRay material or clones existing selected material"

    # noinspection PyUnusedLocal
    def execute(self, context):
        if context.material is not None:
            context.active_object.active_material = context.material.copy()
            if context.material.yafaray_nodes is not None:
                context.active_object.active_material.yafaray_nodes = context.material.yafaray_nodes.copy()
                node_editor_area = None
                for area in context.window_manager.windows[-1].screen.areas:
                    if area.type == 'NODE_EDITOR':
                        node_editor_area = area
                        break
                if node_editor_area is None:
                    bpy.ops.screen.userpref_show("INVOKE_DEFAULT")
                    node_editor_area = context.window_manager.windows[-1].screen.areas[0]
                    node_editor_area.type = "NODE_EDITOR"
                node_editor_area.spaces[0].tree_type = 'YAFARAY4_NODE_TREE'
                node_editor_area.spaces[0].node_tree = bpy.data.node_groups[context.active_object.active_material.yafaray_nodes.name]
                return {'FINISHED'}
        else:
            context.active_object.active_material = bpy.data.materials.new("Material")
        return {'FINISHED'}


@replace_properties_with_annotations
class ShowNodeTreeWindow(Operator):
    bl_idname = "yafaray4.show_node_tree_window"
    bl_label = "Show Node Tree Window"
    bl_description = "Shows the YafaRay Node Tree Window for the selected Node Tree"
    shader_type = StringProperty()

    # noinspection PyUnusedLocal
    def execute(self, context):
        node_editor_area = None
        for area in context.window_manager.windows[-1].screen.areas:
            if area.type == 'NODE_EDITOR':
                node_editor_area = area
                break
        if node_editor_area is None:
            bpy.ops.screen.userpref_show("INVOKE_DEFAULT")
            node_editor_area = context.window_manager.windows[-1].screen.areas[0]
            node_editor_area.type = "NODE_EDITOR"
        node_editor_area.spaces[0].tree_type = 'ShaderNodeTree'
        node_editor_area.spaces[0].shader_type = self.shader_type
        return {'FINISHED'}


class WorldGetSunPosition(Operator):
    bl_idname = "yafaray4.world_get_position"
    bl_label = "From( get position )"
    bl_description = "Get the position of the sun from the selected light location"

    # noinspection PyUnusedLocal
    def execute(self, context):
        warning_message = sun_pos_angle(mode="get", val="position")
        if warning_message:
            self.report({'WARNING'}, warning_message)
            return {'CANCELLED'}
        else:
            return {'FINISHED'}


class WorldGetSunAngle(Operator):
    bl_idname = "yafaray4.world_get_angle"
    bl_label = "From( get angle )"
    bl_description = "Get the position of the sun from selected light angle"

    # noinspection PyUnusedLocal
    def execute(self, context):
        warning_message = sun_pos_angle(mode="get", val="angle")
        if warning_message:
            self.report({'WARNING'}, warning_message)
            return {'CANCELLED'}
        else:
            return {'FINISHED'}


class WorldUpdateSunPositionAndAngle(Operator):
    bl_idname = "yafaray4.world_update_sun"
    bl_label = "From( update sun )"
    bl_description = "Update the position and angle of selected light in 3D View according to GUI values"

    # noinspection PyUnusedLocal
    def execute(self, context):
        warning_message = sun_pos_angle(mode="update")
        if warning_message:
            self.report({'WARNING'}, warning_message)
            return {'CANCELLED'}
        else:
            return {'FINISHED'}


def sun_pos_angle(mode="get", val="position"):
    active_object = bpy.context.active_object
    scene = bpy.context.scene
    world = scene.world

    if active_object and (active_object.type == "LAMP" or active_object.type == "LIGHT"):
        if mode == "get":
            # get the position of the sun from selected light 'location'
            if val == "position":
                location = mathutils.Vector(active_object.location)

                if location.length:
                    point = location.normalized()
                else:
                    point = location.copy()

                world.bg_from = point
                return
            # get the position of the sun from selected lights 'angle'
            elif val == "angle":
                matrix = mathutils.Matrix(active_object.matrix_local).copy()
                # noinspection PyUnresolvedReferences
                world.bg_from = (matrix[0][2], matrix[1][2], matrix[2][2])
                return

        elif mode == "update":
            # get gui from vector and normalize it
            bg_from = mathutils.Vector(world.bg_from).copy()
            if bg_from.length:
                bg_from.normalize()

            # set location
            sun_dist = mathutils.Vector(active_object.location).length
            active_object.location = sun_dist * bg_from

            # compute and set rotation
            quaternion = bg_from.to_track_quat("Z", "Y")
            # noinspection PyArgumentList
            euler = quaternion.to_euler()

            # update sun rotation and redraw the 3D windows
            active_object.rotation_euler = euler
            return

    else:
        return "No selected LIGHT object in the scene!"


def check_scene_lights():
    scene = bpy.context.scene
    world = scene.world

    # expand fuction for include light from 'add sun' or 'add skylight' in sunsky or sunsky2 mode    
    have_lights = False
    # use light create with sunsky, sunsky2 or with use ibl ON
    if world.bg_add_sun or world.bg_background_light or world.bg_use_ibl:
        return True
    # if above is true, this 'for' is not used
    for sceneObj in scene.objects:
        if not sceneObj.hide_render:
            # FIXME BLENDER 2.80-3.51 visibility in Blender >= 2.80??
            if bpy.app.version >= (2, 80, 0) or sceneObj.is_visible(scene):  # check light, meshlight or portal light
                # object
                if sceneObj.type == "LAMP" or sceneObj.type == "LIGHT" or sceneObj.ml_enable or sceneObj.bgp_enable:
                    have_lights = True
                    break
    return have_lights


class RenderView(Operator):
    bl_idname = "yafaray4.render_view"
    bl_label = "YafaRay render view"
    bl_description = "Renders using the view in the active 3d viewport"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == 'YAFARAY4_RENDER'

    def execute(self, context):
        view3d = context.region_data
        global_vars.use_view_to_render = True
        scene_lights = check_scene_lights()
        scene = context.scene
        # Get the 3d view under the mouse cursor
        # if the region is not a 3d view
        # then search for the first active one
        if not view3d:
            for area in [a for a in bpy.context.window.screen.areas if a.type == "VIEW_3D"]:
                view3d = area.spaces.active.region_3d
                break

        if not view3d or view3d.view_perspective == "ORTHO":
            self.report({'WARNING'}, "The selected view is not in perspective mode or there was no 3d view available "
                                     "to render.")
            global_vars.use_view_to_render = False
            return {'CANCELLED'}

        elif not scene_lights and scene.intg_light_method == "Bidirectional":
            self.report({'WARNING'}, "No lights in the scene and lighting method is Bidirectional!")
            global_vars.use_view_to_render = False
            return {'CANCELLED'}

        else:
            global_vars.view_matrix = view3d.view_matrix.copy()
            bpy.ops.render.render('INVOKE_DEFAULT')
            return {'FINISHED'}


class RenderAnimation(Operator):
    bl_idname = "yafaray4.render_animation"
    bl_label = "YafaRay render animation"
    bl_description = "Render active scene"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == 'YAFARAY4_RENDER'

    def execute(self, context):
        scene_lights = check_scene_lights()
        scene = context.scene

        if not scene_lights and scene.intg_light_method == "Bidirectional":
            self.report({'WARNING'}, "No lights in the scene and lighting method is Bidirectional!")
            return {'CANCELLED'}

        else:
            bpy.ops.render.render('INVOKE_DEFAULT', animation=True)
            return {'FINISHED'}


class RenderStill(Operator):
    bl_idname = "yafaray4.render_still"
    bl_label = "YafaRay render still"
    bl_description = "Render active scene"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == 'YAFARAY4_RENDER'

    def execute(self, context):
        scene_lights = check_scene_lights()
        scene = context.scene

        if not scene_lights and scene.intg_light_method == "Bidirectional":
            self.report({'WARNING'}, "No lights in the scene and lighting method is Bidirectional!")
            return {'CANCELLED'}

        else:
            bpy.ops.render.render('INVOKE_DEFAULT')
            return {'FINISHED'}


class MaterialPresetsIorList(Operator):
    bl_idname = "yafaray4.material_preset_ior_list"
    bl_label = "IOR presets"
    index = bpy.props.FloatProperty()
    name = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        yaf_mat = context.material
        return yaf_mat.mat_type in {"glass", "rough_glass"}

    def execute(self, context):
        yaf_mat = context.material
        bpy.types.PresetsIorList.bl_label = self.name
        yaf_mat.IOR_refraction = self.index
        return {'FINISHED'}


class MaterialPreviewCamRotReset(bpy.types.Operator):
    """ Reset camera rotation/zoom to initial values. """
    bl_idname = "yafaray4.material_preview_camera_rotation_reset"
    bl_label = "reset camera rotation/distance values to defaults"
    country = bpy.props.StringProperty()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def execute(self, context):
        bpy.data.scenes[0].yafaray.preview.camRot = (0, 0, 1)
        bpy.data.scenes[0].yafaray.preview.camDist = 12
        return {'FINISHED'}


class MaterialPreviewCamZoomIn(bpy.types.Operator):
    """ Camera zoom in (reduces distance between camera and object) """
    bl_idname = "yafaray4.material_preview_camera_zoom_in"
    bl_label = "reset camera rotation/distance values to defaults"
    country = bpy.props.StringProperty()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def execute(self, context):
        bpy.data.scenes[0].yafaray.preview.camDist -= 0.5
        return {'FINISHED'}


class MaterialPreviewCamZoomOut(bpy.types.Operator):
    """ Camera zoom out (increases distance between camera and object) """
    bl_idname = "yafaray4.material_preview_camera_zoom_out"
    bl_label = "reset camera rotation/distance values to defaults"
    country = bpy.props.StringProperty()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def execute(self, context):
        bpy.data.scenes[0].yafaray.preview.camDist += 0.5
        return {'FINISHED'}


classes = (
    CreateNode, NewMaterial, ShowNodeTreeWindow,
    WorldGetSunPosition, WorldGetSunAngle, WorldUpdateSunPositionAndAngle,
    RenderView, RenderAnimation, RenderStill,
    MaterialPresetsIorList, MaterialPreviewCamRotReset, MaterialPreviewCamZoomIn, MaterialPreviewCamZoomOut,)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed,
    # before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the
    # "libyafaray4_bindings" compiled module is installed on
    register()
