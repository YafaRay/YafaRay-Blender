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

#TODO: Use Blender enumerators if any
import bpy
import os
import threading
import time
import libyafaray4_bindings
import traceback
import datetime
import platform
import tempfile

from .. import YAF_ID_NAME
from .. import YAFARAY_BLENDER_VERSION
from .yaf_object import yafObject
from .yaf_light import yafLight
from .yaf_world import yafWorld
from .yaf_integrator import yafIntegrator
from . import yaf_scene
from .yaf_texture import yafTexture
from .yaf_material import yafMaterial
from ..ot import yafaray_presets
# from pprint import pprint
# from pprint import pformat
from ..util.io_utils import scene_from_depsgraph
from .. import yaf_global_vars

class YafaRay4RenderEngine(bpy.types.RenderEngine):
    bl_idname = YAF_ID_NAME
    bl_use_preview = True
    bl_label = "YafaRay v4 Render"
    prog = 0.0
    tag = ""
    yaf_global_vars.useViewToRender = False
    yaf_global_vars.viewMatrix = None

    def setInterface(self, yi):
        self.materials = set()
        self.yi = yi

        if self.is_preview:
            self.yi.setConsoleVerbosityLevel(yi.logLevelFromString("mute"))
            self.yi.setLogVerbosityLevel(yi.logLevelFromString("mute"))

        yi.paramsSetString("type", self.scene.adv_scene_type)
        self.yi.createScene()
        self.yi.paramsClearAll()

        if self.is_preview:
            self.yi.setConsoleVerbosityLevel(yi.logLevelFromString("mute"))
            self.yi.setLogVerbosityLevel(yi.logLevelFromString("mute"))
            self.scene.bg_transp = False  #to correct alpha problems in preview roughglass
            self.scene.bg_transp_refract = False  #to correct alpha problems in preview roughglass
        else:
            self.yi.enablePrintDateTime(self.scene.yafaray.logging.logPrintDateTime)
            self.yi.setConsoleVerbosityLevel(yi.logLevelFromString(self.scene.yafaray.logging.consoleVerbosity))
            self.yi.setLogVerbosityLevel(yi.logLevelFromString(self.scene.yafaray.logging.logVerbosity))
            self.yi.printInfo("YafaRay-Blender (" + YAFARAY_BLENDER_VERSION + ")")
            self.yi.printInfo("Exporter: Blender version " + str(bpy.app.version[0]) + "." + str(bpy.app.version[1]) + "." + str(bpy.app.version[2]) + "." + bpy.app.version_char + "  Build information: " + bpy.app.build_platform.decode("utf-8") + ", " + bpy.app.build_type.decode("utf-8") + ", branch: " + bpy.app.build_branch.decode("utf-8") + ", hash: " + bpy.app.build_hash.decode("utf-8"))
            self.yi.printInfo("Exporter: System information: " + platform.processor() + ", " + platform.platform())

        self.yaf_object = yafObject(self.yi, self.is_preview)
        self.yaf_light = yafLight(self.yi, self.is_preview)
        self.yaf_world = yafWorld(self.yi)
        self.yaf_integrator = yafIntegrator(self.yi)
        self.yaf_texture = yafTexture(self.yi)
        self.yaf_material = yafMaterial(self.yi, self.yaf_texture.loadedTextures)

    def exportScene(self):
        if bpy.app.version >= (2, 80, 0):
            for inst in self.depsgraph.object_instances:
                obj = inst.object
                self.exportTexture(obj)
        else:
            for obj in self.scene.objects:
                self.exportTexture(obj)
        self.exportMaterials()
        self.yaf_object.setDepsgraph(self.depsgraph)
        self.exportObjects()
        self.yaf_object.createCameras()
        
        if self.is_preview and bpy.data.scenes[0].yafaray.preview.enable and bpy.data.scenes[0].yafaray.preview.previewBackground == "world":
            self.yaf_world.exportWorld(bpy.data.scenes[0], self.is_preview)
        else:
            self.yaf_world.exportWorld(self.scene, self.is_preview)

    def exportTexture(self, obj):
        if bpy.app.version >= (2, 80, 0):
            return None   # FIXME BLENDER 2.80-3.00
        # First export the textures of the materials type 'blend'
        for mat_slot in [m for m in obj.material_slots if m.material is not None]:
            if mat_slot.material.mat_type == 'blend':
                blendmat_error = False
                try:
                    mat1 = bpy.data.materials[mat_slot.material.material1name]
                except:
                    self.yi.printWarning("Exporter: Problem with blend material:\"{0}\". Could not find the first material:\"{1}\"".format(mat_slot.material.name, mat_slot.material.material1name))
                    blendmat_error = True
                try:
                    mat2 = bpy.data.materials[mat_slot.material.material2name]
                except:
                    self.yi.printWarning("Exporter: Problem with blend material:\"{0}\". Could not find the second material:\"{1}\"".format(mat_slot.material.name, mat_slot.material.material2name))
                    blendmat_error = True
                if blendmat_error:
                    continue
                for bm in [mat1, mat2]:
                    for blendtex in [bt for bt in bm.texture_slots if (bt and bt.texture and bt.use)]:
                        if self.is_preview and blendtex.texture.name == 'fakeshadow':
                            continue
                        self.yaf_texture.writeTexture(self.scene, blendtex.texture)
            else:
                continue

        for mat_slot in [m for m in obj.material_slots if m.material is not None]:
            for tex in [t for t in mat_slot.material.texture_slots if (t and t.texture and t.use)]:
                if self.is_preview and tex.texture.name == "fakeshadow":
                    continue
                self.yaf_texture.writeTexture(self.scene, tex.texture)

    def object_on_visible_layer(self, obj):
        if bpy.app.version >= (2, 80, 0):
            return None   # FIXME BLENDER 2.80-3.00
        obj_visible = False
        for layer_visible in [object_layers and scene_layers for object_layers, scene_layers in zip(obj.layers, self.scene.layers)]:
            obj_visible |= layer_visible
        return obj_visible

    def exportObjects(self):
        self.yi.printInfo("Exporter: Processing Lights...")

        # export only visible lights
        if bpy.app.version >= (2, 80, 0):
            visible_lights = [o.object for o in self.depsgraph.object_instances if not (o.object.hide_get() or o.object.hide_render or o.object.hide_viewport) and o.object.type == 'LIGHT']
        else:
            visible_lights = [o for o in self.scene.objects if not o.hide_render and o.is_visible(self.scene) and o.type == 'LAMP']
        for obj in visible_lights:
            if bpy.app.version >= (2, 80, 0):
                obj_is_instancer = obj.is_instancer
            else:
                obj_is_instancer = obj.is_duplicator
            if obj_is_instancer:
                obj.create_dupli_list(self.scene)
                for obj_dupli in obj.dupli_list:
                    matrix = obj_dupli.matrix.copy()
                    self.yaf_light.createLight(self.yi, obj_dupli.object, matrix)

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
                self.yaf_light.createLight(self.yi, obj, obj.matrix_world)

        self.yi.printInfo("Exporter: Processing Geometry...")

        # export only visible objects
        baseIds = {}
        dupBaseIds = {}

        if bpy.app.version >= (2, 80, 0):
            visible_objects = [o.object for o in self.depsgraph.object_instances if not (o.object.hide_get() or o.object.hide_render or o.object.hide_viewport) and o.object.type in {'MESH', 'SURFACE', 'CURVE', 'FONT', 'EMPTY'}]
        else:
            visible_objects = [o for o in self.scene.objects if not o.hide_render and (o.is_visible(self.scene) or o.hide) and self.object_on_visible_layer(o) and (o.type in {'MESH', 'SURFACE', 'CURVE', 'FONT', 'EMPTY'})]
        for obj in visible_objects:
            # Exporting dupliObjects as instances, also check for dupliObject type 'EMPTY' and don't export them as geometry
            if bpy.app.version >= (2, 80, 0):
                obj_is_instancer = obj.is_instancer
            else:
                obj_is_instancer = obj.is_duplicator
            if obj_is_instancer:
                self.yi.printVerbose("Processing duplis for: {0}".format(obj.name))
                frame_current = self.scene.frame_current
                if self.scene.render.use_instances:
                    time_steps = 3
                else:
                    time_steps = 1
                instance_ids = []
                for time_step in range(0, time_steps):
                    self.scene.frame_set(frame_current, 0.5 * time_step)
                    obj.dupli_list_create(self.scene)
                    idx = 0
                    for obj_dupli in [od for od in obj.dupli_list if not od.object.type == 'EMPTY']:
                        self.exportTexture(obj_dupli.object)
                        for mat_slot in obj_dupli.object.material_slots:
                            if mat_slot.material not in self.materials:
                                self.exportMaterial(mat_slot.material)

                        if not self.scene.render.use_instances:
                            matrix = obj_dupli.matrix.copy()
                            self.yaf_object.writeMesh(obj_dupli.object, matrix, obj_dupli.object.name + "_" + str(self.yi.getNextFreeId()))
                        else:
                            if obj_dupli.object.name not in dupBaseIds:
                                dupBaseIds[obj_dupli.object.name] = self.yaf_object.writeInstanceBase(obj_dupli.object.name, obj_dupli.object)
                            matrix = obj_dupli.matrix.copy()
                            if time_step == 0:
                                instance_id = self.yaf_object.writeInstance(dupBaseIds[obj_dupli.object.name], matrix, obj_dupli.object.name)
                                instance_ids.append(instance_id)
                            elif obj.motion_blur_bezier:
                                self.yaf_object.addInstanceMatrix(instance_ids[idx], matrix, 0.5 * time_step)
                                idx += 1

                    if obj.dupli_list is not None:
                        obj.dupli_list_clear()

                self.scene.frame_set(frame_current, 0.0)

                # check if object has particle system and uses the option for 'render emitter'
                if hasattr(obj, 'particle_systems'):
                    for pSys in obj.particle_systems:
                        check_rendertype = pSys.settings.render_type in {'OBJECT', 'GROUP'}
                        if check_rendertype and pSys.settings.use_render_emitter:
                            matrix = obj.matrix_world.copy()
                            self.yaf_object.writeMesh(obj, matrix)

            # no need to write empty object from here on, so continue with next object in loop
            elif obj.type == 'EMPTY':
                continue

            # Exporting objects with shared mesh data blocks as instances
            elif obj.data.users > 1 and self.scene.render.use_instances:
                self.yi.printVerbose("Processing shared mesh data node object: {0}".format(obj.name))
                if obj.data.name not in baseIds:
                    baseIds[obj.data.name] = self.yaf_object.writeInstanceBase(obj.data.name, obj)

                if obj.name not in dupBaseIds:
                    matrix = obj.matrix_world.copy()
                    instance_id = self.yaf_object.writeInstance(obj.name, matrix, baseIds[obj.data.name])
                    if obj.motion_blur_bezier:
                        frame_current = self.scene.frame_current
                        self.scene.frame_set(frame_current, 0.5)
                        matrix = obj.matrix_world.copy()
                        self.yaf_object.addInstanceMatrix(instance_id, matrix, 0.5)
                        self.scene.frame_set(frame_current, 1.0)
                        matrix = obj.matrix_world.copy()
                        self.yaf_object.addInstanceMatrix(instance_id, matrix, 1.0)
                        self.scene.frame_set(frame_current, 0.0)

            elif obj.data.name not in baseIds and obj.name not in dupBaseIds:
                self.yaf_object.writeObject(obj)

    def handleBlendMat(self, mat):
        blendmat_error = False
        try:
            mat1 = bpy.data.materials[mat.material1name]
        except:
            self.yi.printWarning("Exporter: Problem with blend material:\"{0}\". Could not find the first material:\"{1}\"".format(mat.name, mat.material1name))
            blendmat_error = True
        try:
            mat2 = bpy.data.materials[mat.material2name]
        except:
            self.yi.printWarning("Exporter: Problem with blend material:\"{0}\". Could not find the second material:\"{1}\"".format(mat.name, mat.material2name))
            blendmat_error = True
        if blendmat_error:
            return blendmat_error
        if mat1.name == mat2.name:
            self.yi.printWarning("Exporter: Problem with blend material \"{0}\". \"{1}\" and \"{2}\" to blend are the same materials".format(mat.name, mat1.name, mat2.name))

        if mat1.mat_type == 'blend':
            blendmat_error = self.handleBlendMat(mat1)
            if blendmat_error:
                return

        elif mat1 not in self.materials:
            self.materials.add(mat1)
            self.yaf_material.writeMaterial(mat1, self.scene)

        if mat2.mat_type == 'blend':
            blendmat_error = self.handleBlendMat(mat2)
            if blendmat_error:
                return

        elif mat2 not in self.materials:
            self.materials.add(mat2)
            self.yaf_material.writeMaterial(mat2, self.scene)

        if mat not in self.materials:
            self.materials.add(mat)
            self.yaf_material.writeMaterial(mat, self.scene)

    def exportMaterials(self):
        self.yi.printInfo("Exporter: Processing Materials...")
        self.materials = set()

        # create a default shiny diffuse material -> it will be assigned, if object has no material(s)
        self.yi.paramsClearAll()
        self.yi.paramsSetString("type", "shinydiffusemat")
        if self.scene.gs_clay_render:    
            cCol = self.scene.gs_clay_col
        else:
            cCol = (0.8, 0.8, 0.8)
        self.yi.paramsSetColor("color", cCol[0], cCol[1], cCol[2])
        self.yi.printInfo("Exporter: Creating Material \"defaultMat\"")
        self.yi.createMaterial("defaultMat")

        for obj in self.scene.objects:
            for mat_slot in obj.material_slots:
                if mat_slot.material not in self.materials:
                    self.exportMaterial(mat_slot.material)

    def exportMaterial(self, material):
        if material:
            if material.mat_type == 'blend':
                # must make sure all materials used by a blend mat
                # are written before the blend mat itself
                self.handleBlendMat(material)
            else:
                self.materials.add(material)
                self.yaf_material.writeMaterial(material, self.scene, self.is_preview)

    def decideOutputFileName(self, output_path, filetype):

        switchFileType = {
            'PNG': 'png',
            'TARGA': 'tga',
            'TIFF': 'tif',
            'JPEG': 'jpg',
            'HDR': 'hdr',
            'OPEN_EXR': 'exr',
            'xml': 'xml',
            'c': 'c',
            'python': 'py',
        }
        filetype = switchFileType.get(filetype, 'png')
        # write image or XML-File with filename from framenumber
        frame_numb_str = "{:0" + str(len(str(self.scene.frame_end))) + "d}"
        
        filebasename = ""
        if self.scene.img_add_blend_name:
            if bpy.data.filepath == "":
                filebasename += "temp"
            filebasename += os.path.splitext(os.path.basename(bpy.data.filepath))[0]+" - "
            
        filebasename += frame_numb_str.format(self.scene.frame_current)

        if self.scene.img_add_datetime:
            filebasename += " ("+datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S")+")"
        
        output = os.path.join(output_path, filebasename)
        # try to create dir if it not exists...
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
            except:
                print("Unable to create directory...")
                import traceback
                traceback.print_exc()
                output = ""
        outputFile = output + "." + filetype

        return outputFile, output, filetype

    def defineImageOutput(self, output_name, fp, scene, render, color_space, gamma, alpha_premultiply):
        self.outputFile, self.output, self.file_type = self.decideOutputFileName(fp, scene.img_output)
        self.yi.paramsClearAll()
        self.yi.paramsSetString("image_path", str(self.outputFile))
        self.yi.paramsSetString("color_space", color_space)
        self.yi.paramsSetFloat("gamma", gamma)
        self.yi.paramsSetBool("alpha_premultiply", alpha_premultiply)
        self.yi.paramsSetBool("multi_layer", scene.img_multilayer)
        self.yi.paramsSetBool("denoise_enabled", scene.img_denoise)
        self.yi.paramsSetInt("denoise_h_lum", scene.img_denoiseHLum)
        self.yi.paramsSetInt("denoise_h_col", scene.img_denoiseHCol)
        self.yi.paramsSetFloat("denoise_mix", scene.img_denoiseMix)
        print(render.image_settings.color_mode)
        self.yi.paramsSetBool("alpha_channel", render.image_settings.color_mode == "RGBA")
        yaf_scene.setLoggingAndBadgeSettings(self.yi, self.scene)
        self.co = self.yi.createOutput(output_name)

    # callback to export the scene
    def update(self, data, depsgraph):
        self.depsgraph = depsgraph
        scene = scene_from_depsgraph(depsgraph)
        self.update_stats("", "Setting up render")
        if not self.is_preview:
            scene.frame_set(scene.frame_current)

        self.scene = scene
        render = scene.render

        if bpy.data.filepath == "":
            render_filename = "render"
            render_path = tempfile.gettempdir() + "/temp_render/"
        else:
            render_filename = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
            render_path = "//" + render_filename + "_render/"

        render_filename += " - " + str(self.scene.frame_current)

        if scene.img_save_with_blend_file:
            render.filepath = render_path
            render_path = bpy.path.abspath(render_path)
        else:
            render_path = bpy.path.abspath(render.filepath)

        render_path = os.path.realpath(render_path)
        render_path = os.path.normpath(render_path)

        if not os.path.exists(render_path):
            os.mkdir(render_path)

        [self.sizeX, self.sizeY, self.bStartX, self.bStartY, self.bsizeX, self.bsizeY, camDummy] = yaf_scene.getRenderCoords(scene)

        if render.use_border:
            self.resX = self.bsizeX
            self.resY = self.bsizeY
        else:
            self.resX = self.sizeX
            self.resY = self.sizeY

        color_space = yaf_scene.calcColorSpace(scene)
        gamma = yaf_scene.calcGamma(scene)
        alpha_premultiply = yaf_scene.calcAlphaPremultiply(scene)

        if scene.gs_type_render == "file":
            self.setInterface(libyafaray4_bindings.Interface())
            self.yi.setInputColorSpace("LinearRGB", 1.0)    #When rendering into Blender, color picker floating point data is already linear (linearized by Blender)
            self.defineImageOutput("blender_file_output", render_path, scene, render, color_space.blender, gamma.blender, alpha_premultiply.blender)
            if scene.yafaray.logging.savePreset:
                yafaray_presets.YAF_AddPresetBase.export_to_file(yafaray_presets.YAFARAY_OT_presets_renderset, self.outputFile)

        elif scene.gs_type_render == "xml" or scene.gs_type_render == "c" or scene.gs_type_render == "python":
            self.outputFile, self.output, self.file_type = self.decideOutputFileName(render_path, scene.gs_type_render)
            self.setInterface(libyafaray4_bindings.Interface(self.outputFile))

            input_color_values_color_space = "sRGB"
            input_color_values_gamma = 1.0

            if scene.display_settings.display_device == "sRGB":
                input_color_values_color_space = "sRGB"
                
            elif scene.display_settings.display_device == "XYZ":
                input_color_values_color_space = "XYZ"
                
            elif scene.display_settings.display_device == "None":
                input_color_values_color_space = "Raw_Manual_Gamma"
                input_color_values_gamma = scene.gs_gamma  #We only use the selected gamma if the output device is set to "None"
            
            self.yi.setInputColorSpace("LinearRGB", 1.0)    #Values from Blender, color picker floating point data are already linear (linearized by Blender)
            self.defineImageOutput("xml_file_output", render_path, scene, render, color_space.blender, gamma.blender, alpha_premultiply.blender)
            #FIXME! self.yi.setXmlColorSpace(input_color_values_color_space, input_color_values_gamma)  #To set the XML interface to write the XML values with the correction included for the selected color space (and gamma if applicable)

        else:
            self.setInterface(libyafaray4_bindings.Interface())
            self.yi.setInputColorSpace("LinearRGB", 1.0)    #When rendering into Blender, color picker floating point data is already linear (linearized by Blender)
            if scene.gs_secondary_file_output and not self.is_preview:
                self.defineImageOutput("blender_secondary_output", render_path, scene, render, color_space.secondary_output, gamma.secondary_output, alpha_premultiply.secondary_output)
                if scene.yafaray.logging.savePreset:
                    yafaray_presets.YAF_AddPresetBase.export_to_file(yafaray_presets.YAFARAY_OT_presets_renderset, self.outputFile)

        self.exportScene()
        self.yaf_integrator.exportIntegrator(self.scene)
        self.yaf_integrator.exportVolumeIntegrator(self.scene)
        yaf_scene.defineLayers(self.yi, self.depsgraph)
        yaf_scene.exportRenderSettings(self.yi, self.depsgraph, render_path, render_filename)
        self.yi.setupRender()

    # callback to render scene
    def render(self, depsgraph):
        self.depsgraph = depsgraph
        scene = scene_from_depsgraph(depsgraph)
        self.bl_use_postprocess = False
        self.scene = scene

        if scene.gs_type_render == "file":
            self.yi.printInfo("Exporter: Rendering to file {0}".format(self.outputFile))
            self.update_stats("YafaRay Rendering:", "Rendering to {0}".format(self.outputFile))
            self.yi.render(0, 0)
            result = self.begin_result(0, 0, self.resX, self.resY)
            result.layers[0].load_from_file(self.outputFile)
            #lay.passes["Depth"].load_from_file("{0} (Depth).{1}".format(self.output, self.file_type)) #FIXME? Unfortunately I cannot find a way to load the exported images back to the appropiate passes in Blender. Blender probably needs to improve their API to allow per-pass loading of files. Also, Blender does not allow opening multi layer EXR files with this function.
            self.end_result(result)

        elif scene.gs_type_render == "xml":
            self.yi.printInfo("Exporter: Writing XML to file {0}".format(self.outputFile))
            self.yi.render(0, 0)

        else:
            def progressCallback(*args):
                steps_total, steps_done, tag = args
                self.update_stats("YafaRay Render: ", "{0}".format(tag))
                # Now, Blender use same range to YafaRay
                if steps_total > 0:
                    self.update_progress(steps_done / steps_total)
                else:
                    self.update_progress(0.0)

            def updateBlenderResult(x, y, w, h, view_name, tiles, callback_name):
                if scene.render.use_multiview:
                    blender_result_buffers = self.begin_result(x, y, w, h, "", view_name)
                else:
                    blender_result_buffers = self.begin_result(x, y, w, h)
                for tile in tiles:
                    tile_name, tile_bitmap = tile
                    try:
                        blender_result_buffers.layers[0].passes[tile_name].rect = tile_bitmap
                    except:
                        print("Exporter: Exception while rendering in " + callback_name + " function:")
                        traceback.print_exc()
                self.end_result(blender_result_buffers)

            def highlightCallback(*args):
                view_name, area_id, x_0, y_0, x_1, y_1, tiles = args
                w = x_1 - x_0
                h = y_1 - y_0
                if view_name == "":  # In case we use Render 3D viewport with Views enabled, it will copy the result to all views
                    for view in scene.render.views:
                        updateBlenderResult(x_0, y_0, w, h, view.name, tiles, "highlightCallback")
                else:  # Normal rendering
                    updateBlenderResult(x_0, y_0, w, h, view_name, tiles, "highlightCallback")

            def flushAreaCallback(*args):
                view_name, area_id, x_0, y_0, x_1, y_1, tiles = args
                w = x_1 - x_0
                h = y_1 - y_0
                if view_name == "":  # In case we use Render 3D viewport with Views enabled, it will copy the result to all views
                    for view in scene.render.views:
                        updateBlenderResult(x_0, y_0, w, h, view.name, tiles, "flushAreaCallback")
                else:  # Normal rendering
                    updateBlenderResult(x_0, y_0, w, h, view_name, tiles, "flushAreaCallback")

            def flushCallback(*args):
                view_name, w, h, tiles = args
                if view_name == "":  # In case we use Render 3D viewport with Views enabled, it will copy the result to all views
                    for view in scene.render.views:
                        updateBlenderResult(0, 0, w, h, view.name, tiles, "flushCallback")
                else:  # Normal rendering
                    updateBlenderResult(0, 0, w, h, view_name, tiles, "flushCallback")

            self.yi.setRenderFlushAreaCallback(flushAreaCallback)
            self.yi.setRenderFlushCallback(flushCallback)
            self.yi.setRenderHighlightAreaCallback(highlightCallback)
            t = threading.Thread(target=self.yi.render, args=(self.bStartX, self.bStartY, progressCallback,))
            t.start()

            while t.is_alive() and not self.test_break():
                time.sleep(0.2)

            if t.is_alive():
                self.update_stats("", "Aborting, please wait for all pending tasks to complete (progress in console log)...")
                self.yi.cancelRendering()
                t.join()

        self.yi.clearAll()
        self.yi.clearOutputs()
        del self.yi
        self.update_stats("", "Done!")
        self.bl_use_postprocess = True


classes = (
    YafaRay4RenderEngine,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
