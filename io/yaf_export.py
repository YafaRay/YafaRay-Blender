#TODO: Use Blender enumerators if any

import bpy
import os
import time
import tempfile
import sys
import platform

import yafrayinterface
from yafaray import PLUGIN_PATH
from yafaray import YAF_ID_NAME
from yafaray.io.yaf_object import yafObject
from yafaray.io.yaf_light  import yafLight
from yafaray.io.yaf_world  import yafWorld
from yafaray.io.yaf_integrator import yafIntegrator
from yafaray.io import yaf_scene
from yafaray.io.yaf_texture import yafTexture
from yafaray.io.yaf_material import yafMaterial

class YafaRayRenderEngine(bpy.types.RenderEngine):
    bl_idname = YAF_ID_NAME
    bl_use_preview = True
    bl_label = "YafaRay Render"
    prog = 0.0
    tag = ""
    useViewToRender = False
    viewMatrix = None
    viewRenderKey = -65535

    def setInterface(self, yi):
        self.materialMap = {}
        self.materials   = set()
        self.yi = yi

        if self.preview:
            pass
            self.yi.setVerbosityMute()
        else:
            # TODO: add verbosity control in the general settings
            self.yi.setVerbosityInfo()

        self.yi.loadPlugins(PLUGIN_PATH)
        self.yaf_object     = yafObject(self.yi, self.materialMap)
        self.yaf_lamp       = yafLight(self.yi, self.preview)
        self.yaf_world      = yafWorld(self.yi)
        self.yaf_integrator = yafIntegrator(self.yi)
        self.yaf_texture    = yafTexture(self.yi)
        self.yaf_material   = yafMaterial(self.yi, self.materialMap, self.yaf_texture.loadedTextures)
        

    def exportScene(self):
        self.yaf_world.exportWorld(self.scene)
        self.exportTextures()
        self.exportMaterials()
        self.yaf_object.setScene(self.scene)
        self.yaf_object.createCamera()
        self.exportObjects()

    def exportTextures(self):
        # export textures from visible objects only. Won't work with
        # blend mat, there the textures need to be handled separately
        
        for obj in [o for o in self.scene.objects if (not o.hide_render and o.is_visible(self.scene))]:
            for mat_slot in [m for m in obj.material_slots if m.material]:
                for tex in [t for t in mat_slot.material.texture_slots if (t and t.texture)]:
                    if self.preview and tex.texture.name == "fakeshadow": continue
                    self.yaf_texture.writeTexture(self.scene, tex.texture)

    def exportObjects(self):
        self.yi.printInfo("Exporter: Processing Lamps...")

        # export only visible lamps
        for obj in [o for o in self.scene.objects if not o.hide_render and o.is_visible(self.scene) and o.type == 'LAMP']:
            if obj.is_duplicator:
                obj.create_dupli_list(self.scene)
                for obj_dupli in obj.dupli_list:
                    self.yaf_lamp.createLight(self.yi, obj_dupli.object, obj_dupli.matrix)

                if obj.dupli_list:
                    obj.free_dupli_list()
            else:
                if obj.parent and obj.parent.is_duplicator:
                    continue
                self.yaf_lamp.createLight(self.yi, obj, obj.matrix_world)
        
        self.yi.printInfo("Exporter: Processing Geometry...")
        self.yaf_object.writeObjects()

    def handleBlendMat(self, mat):
        mat1_name = mat.material1
        mat2_name = mat.material2

        if mat.name == mat1_name or mat.name == mat2_name:
            self.yi.printError("Exporter: Blend material " + mat.name + " contains itself!")
            return

        if not mat1_name in bpy.data.materials or not mat2_name in bpy.data.materials:
            self.yi.printWarning("Exporter: Problem with blend material " + mat.name + ". Could not find one of the two blended materials.")
            return

        mat1 = bpy.data.materials[mat1_name]
        mat2 = bpy.data.materials[mat2_name]

        if mat1.mat_type == 'blend':
            self.handleBlendMat(mat1)
        elif mat1 not in self.materials:
            self.materials.add(mat1)
            self.yaf_material.writeMaterial(mat1)

        if mat2.mat_type == 'blend':
            self.handleBlendMat(mat2)
        elif mat2 not in self.materials:
            self.materials.add(mat2)
            self.yaf_material.writeMaterial(mat2)

        if mat not in self.materials:
            self.materials.add(mat)
            self.yaf_material.writeMaterial(mat)


    def exportMaterials(self):
        self.yi.printInfo("Exporter: Processing Materials...")
        self.materials = set()
        self.yi.paramsClearAll()
        self.yi.paramsSetString("type", "shinydiffusemat")
        self.yi.printInfo("Exporter: Creating Material \"defaultMat\"")
        ymat = self.yi.createMaterial("defaultMat")
        self.materialMap["default"] = ymat

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
                self.yaf_material.writeMaterial(material, self.preview)


    def decideOutputFileName(self, output_path, filetype):
        if filetype == 'PNG':
            filetype = 'png'
        elif filetype == 'TARGA':
            filetype = 'tga'
        elif filetype == 'OPEN_EXR':
            filetype = 'exr'
        else:
            filetype = 'png'
        extension = '.' + filetype
        output = tempfile.mktemp(dir = output_path)
        outputFile = output + extension

        return outputFile,output,filetype

    # callback to render scene
    def render(self, scene):

        self.preview = (scene.name == "preview")
        
        self.bl_use_postprocess = False

        self.update_stats("", "Setting up render")

        if not self.preview:
            scene.frame_set(scene.frame_current)

        self.scene = scene
        r = scene.render
        
        [sizeX, sizeY, bStartX, bStartY, bsizeX, bsizeY, camDummy] = yaf_scene.getRenderCoords(scene)
        
        if r.use_border:
            x = bsizeX
            y = bsizeY
        else:
            x = sizeX
            y = sizeY
        
        self.setInterface(yafrayinterface.yafrayInterface_t())

        self.yi.setInputGamma(scene.gs_gamma_input, True)

        if scene.gs_type_render == "file":
            outputFile, output, file_type = self.decideOutputFileName(r.filepath, r.file_format)
            self.yi.paramsClearAll()
            self.yi.paramsSetString("type", file_type)
            self.yi.paramsSetBool("alpha_channel", r.color_mode == "RGBA")
            self.yi.paramsSetBool("z_channel", scene.gs_z_channel)
            self.yi.paramsSetInt("width", x + bStartX)
            self.yi.paramsSetInt("height", y + bStartY)
            ih = self.yi.createImageHandler("outFile")
            co = yafrayinterface.imageOutput_t(ih, str(outputFile), 0, 0)


        self.yi.startScene()
        self.exportScene()
        self.yaf_integrator.exportIntegrator(self.scene)
        self.yaf_integrator.exportVolumeIntegrator(self.scene)

        yaf_scene.exportRenderSettings(self.yi, self.scene) # must be called last as the params from here will be used by render()

        if scene.gs_type_render == "file":
            
            self.yi.printInfo("Exporter: Rendering to file " + outputFile)

            self.update_stats("", "Rendering to %s" % outputFile)

            self.yi.render(co)

            result = self.begin_result(bStartX, bStartY, x + bStartX, y + bStartY)

            lay = result.layers[0]
            
            if scene.gs_z_channel:
                lay.load_from_file(output + '_zbuffer.' + file_type)
            else:
                lay.load_from_file(outputFile)

            self.end_result(result)

        elif scene.gs_type_render == "into_blender":
            
            import threading


            def progressCallback(command, *args):
                if not self.test_break():
                    if command == "tag":
                        self.tag = args[0]
                    elif command == "progress":
                        self.prog = args[0]
                    self.update_stats("YafaRay Rendering... ", "%s - %.2f %%" % (self.tag, self.prog))

            def drawAreaCallback(*args):
                x, y, w, h, tile = args
                res = self.begin_result(x, y, w, h)
                try:
                    res.layers[0].rect = tile
                    #res.layers[0].passes[0].rect = tile
                except:
                    pass
                self.end_result(res)

            def flushCallback(*args):
                w, h, tile = args
                res = self.begin_result(0, 0, w, h)
                try:
                    res.layers[0].rect = tile
                    #res.layers[0].passes[0].rect = tile
                except BaseException as e:
                    pass
                self.end_result(res)

            t = threading.Thread( target=self.yi.render,
                                  args=( sizeX, sizeY, 0, 0,
                                  self.preview,
                                  drawAreaCallback,
                                  flushCallback,
                                  progressCallback )
                                 )
            t.start()

            while t.isAlive() and not self.test_break():
                time.sleep(0.2)

            if t.isAlive():
                self.update_stats("", "Aborting...")
                self.yi.abort()
                t.join()
                self.yi.clearAll()
                del self.yi
                self.update_stats("", "Render is aborted")
                self.bl_use_postprocess = True
                return

        self.update_stats("", "Done!")
        
        self.yi.clearAll()
        del self.yi

        self.bl_use_postprocess = True

