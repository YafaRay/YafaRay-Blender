# SPDX-License-Identifier: GPL-2.0-or-later

import platform

import bpy
import libyafaray4_bindings

from .light_exporter import export_light
from .materials_exporter import export_material
from .object_exporter import export_object, export_mesh, export_instance, export_instance_base, add_instance_matrix
from .texture_exporter import export_texture
from .world_exporter import export_world
from .. import YAFARAY_BLENDER_VERSION
from ..util.io import scene_from_depsgraph


class SceneExporter:
    def __init__(self, is_preview, depsgraph, scene_yafaray, logger):
        self.logger = logger
        self.is_preview = is_preview
        self.depsgraph = depsgraph
        self.scene_blender = scene_from_depsgraph(depsgraph)
        self.scene_yafaray = scene_yafaray
        self.material_set = set()

        if self.is_preview:
            self.logger.set_console_verbosity_level(self.logger.log_level_from_string("debug"))
            self.logger.set_log_verbosity_level(self.logger.log_level_from_string("debug"))
            self.scene_blender.bg_transp = False  # to correct alpha problems in preview roughglass
            self.scene_blender.bg_transp_refract = False  # to correct alpha problems in preview roughglass
        else:
            self.logger.enable_print_date_time(self.scene_blender.yafaray4.logging.log_print_date_time)
            # self.logger.set_console_verbosity_level(self.logger.log_level_from_string(self.scene_blender.yafaray4.logging.console_verbosity))
            self.logger.set_console_verbosity_level(self.logger.log_level_from_string("debug"))
            self.logger.set_log_verbosity_level(
                self.logger.log_level_from_string(self.scene_blender.yafaray4.logging.log_verbosity))
            self.logger.print_info("YafaRay-Blender (v" + YAFARAY_BLENDER_VERSION + ")")
            self.logger.print_info(
                "Exporter: Blender version " + bpy.app.version_string + "  Build information: " + bpy.app.build_platform.decode(
                    "utf-8") + ", " + bpy.app.build_type.decode("utf-8") + ", branch: " + bpy.app.build_branch.decode(
                    "utf-8") + ", hash: " + bpy.app.build_hash.decode("utf-8"))
            self.logger.print_info(
                "Exporter: System information: " + platform.processor() + ", " + platform.platform())

    def export_scene(self):
        if bpy.app.version >= (2, 80, 0):
            for inst in self.depsgraph.object_instances:
                obj = inst.object
                self.export_texture(obj)
        else:
            for obj in self.scene_blender.objects:
                self.export_texture(obj)
        self.export_materials()
        self.export_objects()

        if self.is_preview and bpy.data.scenes[0].yafaray4.preview.enable \
                and bpy.data.scenes[0].yafaray4.preview.preview_background == "world":
            export_world(bpy.data.scenes[0], self.scene_yafaray, self.logger, self.is_preview)
        else:
            export_world(self.scene_blender, self.scene_yafaray, self.logger, self.is_preview)

    def export_texture(self, obj):
        # First export the textures of the materials type 'blend'
        for mat_slot in [m for m in obj.material_slots if m.material is not None]:
            if mat_slot.material.mat_type == 'blend':
                mat_error = False
                # noinspection PyBroadException
                try:
                    mat1 = bpy.data.materials[mat_slot.material.material1name]
                except Exception:
                    self.logger.printWarning(
                        "Exporter: Problem with blend material:\"{0}\". "
                        "Could not find the first material:\"{1}\"".format(
                            mat_slot.material.name, mat_slot.material.material1name))
                    mat_error = True
                # noinspection PyBroadException
                try:
                    mat2 = bpy.data.materials[mat_slot.material.material2name]
                except Exception:
                    self.logger.printWarning(
                        "Exporter: Problem with blend material:\"{0}\". "
                        "Could not find the second material:\"{1}\"".format(
                            mat_slot.material.name, mat_slot.material.material2name))
                    mat_error = True
                if mat_error:
                    continue
                for bm in [mat1, mat2]:
                    for blendtex in [bt for bt in bm.texture_slots if (bt and bt.texture and bt.use)]:
                        if self.is_preview and blendtex.texture.name == 'fakeshadow':
                            continue
                        export_texture(self.scene_blender, blendtex.texture, self.scene_yafaray, self.logger)
            else:
                continue

        for mat_slot in [m for m in obj.material_slots if m.material is not None]:
            for tex in [t for t in mat_slot.material.yafaray4.texture_slots if (t and t.texture and t.use)]:
                if self.is_preview and tex.texture.name == "fakeshadow":
                    continue
                export_texture(self.scene_blender, tex.texture, self.scene_yafaray, self.logger)

    def object_on_visible_layer(self, obj):
        if bpy.app.version >= (2, 80, 0):
            return None  # FIXME BLENDER >= v2.80
        obj_visible = False
        for layer_visible in [object_layers and scene_layers for object_layers, scene_layers in
                              zip(obj.layers, self.scene_blender.layers)]:
            obj_visible |= layer_visible
        return obj_visible

    def export_objects(self):
        self.logger.print_info("Exporter: Processing Lights...")

        # export only visible lights
        if bpy.app.version >= (2, 80, 0):
            visible_lights = [o.object for o in self.depsgraph.object_instances if not (
                    o.object.hide_get() or o.object.hide_render or o.object.hide_viewport) and o.object.type == 'LIGHT']
        else:
            visible_lights = [o for o in self.scene_blender.objects if
                              not o.hide_render and o.is_visible(self.scene_blender) and o.type == 'LAMP']
        for obj in visible_lights:
            if bpy.app.version >= (2, 80, 0):
                obj_is_instancer = obj.is_instancer
            else:
                obj_is_instancer = obj.is_duplicator
            if obj_is_instancer:
                obj.create_dupli_list(self.scene_blender)
                for obj_dupli in obj.dupli_list:
                    matrix = obj_dupli.matrix.copy()
                    export_light(obj_dupli.object, self.scene_yafaray, self.logger, self.is_preview, matrix)

                if obj.dupli_list:
                    obj.free_dupli_list()
            else:
                if obj.parent:
                    if bpy.app.version >= (2, 80, 0):
                        obj_parent_is_instancer = obj.parent.is_instancer
                    else:
                        obj_parent_is_instancer = obj.parent.is_duplicator
                    if obj_parent_is_instancer:
                        continue
                export_light(obj, self.scene_yafaray, self.logger, self.is_preview, obj.matrix_world)

        self.logger.print_info("Exporter: Processing Geometry...")

        # export only visible objects
        base_names = set()
        dup_base_names = set()

        if bpy.app.version >= (2, 80, 0):
            visible_objects = [o.object for o in self.depsgraph.object_instances if not (
                    o.object.hide_get() or o.object.hide_render or o.object.hide_viewport) and o.object.type in {
                                   'MESH', 'SURFACE', 'CURVE', 'FONT', 'EMPTY'}]
        else:
            visible_objects = [o for o in self.scene_blender.objects if not o.hide_render and (
                    o.is_visible(self.scene_blender) or o.hide) and self.object_on_visible_layer(o) and (
                                       o.type in {'MESH', 'SURFACE', 'CURVE', 'FONT', 'EMPTY'})]
        for obj in visible_objects:
            # Exporting dupliObjects as instances, also check for dupliObject
            # type 'EMPTY' and don't export them as geometry
            if bpy.app.version >= (2, 80, 0):
                obj_is_instancer = obj.is_instancer
            else:
                obj_is_instancer = obj.is_duplicator
            if obj_is_instancer:
                self.logger.printVerbose("Processing duplis for: {0}".format(obj.name))
                frame_current = self.scene_blender.frame_current
                if self.scene_blender.use_instances:
                    time_steps = 3
                else:
                    time_steps = 1
                instance_ids = []
                for time_step in range(0, time_steps):
                    self.scene_blender.frame_set(frame_current, 0.5 * time_step)
                    obj.dupli_list_create(self.scene_blender)
                    idx = 0
                    for obj_dupli in [od for od in obj.dupli_list if not od.object.type == 'EMPTY']:
                        self.export_texture(obj_dupli.object)
                        for mat_slot in obj_dupli.object.material_slots:
                            if mat_slot.material not in self.material_set:
                                export_material(mat_slot.material, self.material_set, self.scene_blender,
                                                self.scene_yafaray, self.logger, self.is_preview)

                        if not self.scene_blender.use_instances:
                            matrix = obj_dupli.matrix.copy()
                            export_mesh(self.depsgraph, self.scene_yafaray, self.logger, self.is_preview,
                                        obj_dupli.object, matrix,
                                        obj_dupli.object.name + "_" + str(idx))
                        else:
                            if obj_dupli.object.name not in dup_base_names:
                                dup_base_names.add(obj_dupli.object.name)
                                export_instance_base(self.depsgraph, self.scene_yafaray, self.logger, self.is_preview,
                                                     obj_dupli.object)
                            matrix = obj_dupli.matrix.copy()
                            if time_step == 0:
                                instance_id = export_instance(self.scene_yafaray, self.logger, matrix,
                                                              obj_dupli.object.name)
                                instance_ids.append(instance_id)
                            elif obj.motion_blur_bezier:
                                add_instance_matrix(self.scene_yafaray, self.logger, instance_ids[idx],
                                                    matrix, 0.5 * time_step)
                                idx += 1

                    if obj.dupli_list is not None:
                        obj.dupli_list_clear()

                self.scene_blender.frame_set(frame_current, 0.0)

                # check if object has particle system and uses the option for 'render emitter'
                if hasattr(obj, 'particle_systems'):
                    for pSys in obj.particle_systems:
                        check_rendertype = pSys.settings.render_type in {'OBJECT', 'GROUP'}
                        if check_rendertype and pSys.settings.use_render_emitter:
                            matrix = obj.matrix_world.copy()
                            export_mesh(self.depsgraph, self.scene_yafaray, self.logger, self.is_preview, obj, matrix)

            # no need to write empty object from here on, so continue with next object in loop
            elif obj.type == 'EMPTY':
                continue

            # Exporting objects with shared mesh data blocks as instances
            elif obj.data.users > 1 and self.scene_blender.use_instances:
                self.logger.printVerbose("Processing shared mesh data node object: {0}".format(obj.name))
                if obj.data.name not in base_names:
                    base_names.add(obj.data.name)
                    export_instance_base(self.depsgraph, self.scene_yafaray, self.logger, self.is_preview, obj)

                if obj.name not in dup_base_names:
                    matrix = obj.matrix_world.copy()
                    instance_id = export_instance(self.scene_yafaray, self.logger, matrix, obj.data.name)
                    if obj.motion_blur_bezier:
                        frame_current = self.scene_blender.frame_current
                        self.scene_blender.frame_set(frame_current, 0.5)
                        matrix = obj.matrix_world.copy()
                        add_instance_matrix(self.scene_yafaray, self.logger, instance_id, matrix, 0.5)
                        self.scene_blender.frame_set(frame_current, 1.0)
                        matrix = obj.matrix_world.copy()
                        add_instance_matrix(self.scene_yafaray, self.logger, instance_id, matrix, 1.0)
                        self.scene_blender.frame_set(frame_current, 0.0)

            elif obj.data.name not in base_names and obj.name not in dup_base_names:
                export_object(self.depsgraph, self.scene_yafaray, self.logger, self.is_preview, obj)

    def export_materials(self):
        self.logger.print_info("Exporter: Processing Materials...")
        self.material_set = set()

        # create a default shiny diffuse material -> it will be assigned, if object has no material(s)
        param_map = libyafaray4_bindings.ParamMap()
        param_map_list = libyafaray4_bindings.ParamMapList()
        param_map.set_string("type", "shinydiffusemat")
        if self.scene_blender.gs_clay_render:
            c_col = self.scene_blender.gs_clay_col
        else:
            c_col = (0.8, 0.8, 0.8)
        param_map.set_color("color", c_col[0], c_col[1], c_col[2])
        self.logger.print_info("Exporter: Creating Material \"defaultMat\"")
        self.scene_yafaray.create_material("defaultMat", param_map, param_map_list)

        for obj in self.scene_blender.objects:
            for mat_slot in obj.material_slots:
                if mat_slot.material not in self.material_set:
                    export_material(mat_slot.material, self.material_set, self.scene_blender, self.scene_yafaray,
                                    self.logger, self.is_preview)

    def export_volume_integrator(self):
        param_map = libyafaray4_bindings.ParamMap()
        world = self.scene_blender.world
        if world:
            vint_type = world.v_int_type
            self.logger.print_info("Exporting Volume Integrator: {0}".format(vint_type))

            if vint_type == 'Single Scatter':
                param_map.set_string("type", "SingleScatterIntegrator")
                param_map.set_float("stepSize", world.v_int_step_size)
                param_map.set_bool("adaptive", world.v_int_adaptive)
                param_map.set_bool("optimize", world.v_int_optimize)

            elif vint_type == 'Sky':
                param_map.set_string("type", "SkyIntegrator")
                param_map.set_float("turbidity", world.v_int_dsturbidity)
                param_map.set_float("stepSize", world.v_int_step_size)
                param_map.set_float("alpha", world.v_int_alpha)
                param_map.set_float("sigma_t", world.v_int_scale)

            else:
                param_map.set_string("type", "none")
        else:
            param_map.set_string("type", "none")

        self.scene_yafaray.defineVolumeIntegrator(self.scene_yafaray, param_map)
        return True
