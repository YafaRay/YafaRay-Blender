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
import yafrayinterface
from yafaray import PLUGIN_PATH
from yafaray import YAF_ID_NAME
from .yaf_object import yafObject
from .yaf_light  import yafLight
from .yaf_world  import yafWorld
from .yaf_integrator import yafIntegrator
from . import yaf_scene
from .yaf_texture import yafTexture
from .yaf_material import yafMaterial


class YafaRayRenderEngine(bpy.types.RenderEngine):
    bl_idname = YAF_ID_NAME
    bl_use_preview = True
    bl_label = "YafaRay Render"
    prog = 0.0
    tag = ""
    useViewToRender = False
    viewMatrix = None
    # boolean variable to check for texture preview
    is_texPrev = False

    def setInterface(self, yi):
        self.materialMap = {}
        self.materials = set()
        self.yi = yi

        if self.is_preview:
            self.yi.setVerbosityMute()
        elif self.scene.gs_verbose:
            self.yi.setVerbosityInfo()
        else:
            self.yi.setVerbosityMute()

        self.yi.loadPlugins(PLUGIN_PATH)
        self.yaf_object = yafObject(self.yi, self.materialMap)
        self.yaf_lamp = yafLight(self.yi, self.is_preview)
        self.yaf_world = yafWorld(self.yi)
        self.yaf_integrator = yafIntegrator(self.yi)
        self.yaf_texture = yafTexture(self.yi)
        self.yaf_material = yafMaterial(self.yi, self.materialMap, self.yaf_texture.loadedTextures)

    def exportScene(self):
        self.exportTextures()
        self.exportMaterials()
        self.yaf_object.setScene(self.scene)
        self.exportObjects()
        self.yaf_object.createCamera()
        self.yaf_world.exportWorld(self.scene)

    def exportTextures(self):
        # First export the textures of the materials type 'blend'
        for obj in self.scene.objects:
            for mat_slot in [m for m in obj.material_slots if m.material is not None]:
                if mat_slot.material.mat_type == 'blend':
                    mat1 = bpy.data.materials[mat_slot.material.material1]
                    mat2 = bpy.data.materials[mat_slot.material.material2]
                    for bm in [mat1, mat2]:
                        for blendtex in [bt for bt in bm.texture_slots if (bt and bt.texture and bt.use)]:
                            if self.is_preview and blendtex.texture.name == 'fakeshadow':
                                continue
                            self.yaf_texture.writeTexture(self.scene, blendtex.texture)
                else:
                    continue

        for obj in self.scene.objects:
            for mat_slot in [m for m in obj.material_slots if m.material is not None]:
                for tex in [t for t in mat_slot.material.texture_slots if (t and t.texture and t.use)]:
                    if self.is_preview and tex.texture.name == "fakeshadow":
                        continue
                    # stretched plane needs to be fixed for texture preview
                    if self.is_preview and obj.name == 'texture':
                        bpy.types.YAFA_RENDER.is_texPrev = True
                    else:
                        bpy.types.YAFA_RENDER.is_texPrev = False
                    self.yaf_texture.writeTexture(self.scene, tex.texture)

    def exportObjects(self):
        self.yi.printInfo("Exporter: Processing Lamps...")

        # export only visible lamps
        for obj in [o for o in self.scene.objects if not o.hide_render and o.is_visible(self.scene) and o.type == 'LAMP']:
            if obj.is_duplicator:
                obj.create_dupli_list(self.scene)
                for obj_dupli in obj.dupli_list:
                    matrix = obj_dupli.matrix.copy()
                    self.yaf_lamp.createLight(self.yi, obj_dupli.object, matrix)

                if obj.dupli_list:
                    obj.free_dupli_list()
            else:
                if obj.parent and obj.parent.is_duplicator:
                    continue
                self.yaf_lamp.createLight(self.yi, obj, obj.matrix_world)

        self.yi.printInfo("Exporter: Processing Geometry...")
        self.yaf_object.writeObjects()

    def handleBlendMat(self, mat):
        if mat.name == mat.material1:
            self.yi.printError("Exporter: Blend material " + mat.name + " contains itself!")
            return
        elif mat.name == mat.material2:
            self.yi.printError("Exporter: Blend material " + mat.name + " contains itself!")
            return
        elif mat.material1 == mat.material2:
            self.yi.printError("Exporter: Blend material " + mat.material1 + " and " + mat.material2 + " are the same!")
            return
        elif not (mat.material1 and mat.material2 in bpy.data.materials):
            self.yi.printWarning("Exporter: Problem with blend material " + mat.name + ". Could not find one of the two blended materials.")
            return
        else:
            mat1 = bpy.data.materials[mat.material1]
            mat2 = bpy.data.materials[mat.material2]

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

        # create a default shiny diffuse material -> it will be assigned, if object has no material(s)
        self.yi.paramsClearAll()
        self.yi.paramsSetString("type", "shinydiffusemat")
        self.yi.paramsSetColor("color", 0.8, 0.8, 0.8)
        self.yi.printInfo("Exporter: Creating Material \"defaultMat\"")
        ymat = self.yi.createMaterial("defaultMat")
        self.materialMap["default"] = ymat

        # create a shiny diffuse material for "Clay Render" option in general settings
        self.yi.paramsClearAll()
        self.yi.paramsSetString("type", "shinydiffusemat")
        cCol = self.scene.gs_clay_col
        self.yi.paramsSetColor("color", cCol[0], cCol[1], cCol[2])
        self.yi.printInfo("Exporter: Creating Material \"clayMat\"")
        cmat = self.yi.createMaterial("clayMat")
        self.materialMap["clay"] = cmat

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
                self.yaf_material.writeMaterial(material, self.is_preview)

    def decideOutputFileName(self, output_path, filetype):

        switchFileType = {
            'PNG': 'png',
            'TARGA': 'tga',
            'TIFF': 'tif',
            'JPEG': 'jpg',
            'HDR': 'hdr',
            'OPEN_EXR': 'exr',
            'XML': 'xml',
        }
        filetype = switchFileType.get(filetype, 'png')
        # write image or XML-File with filename from framenumber
        frame_numb_str = "{:0" + str(len(str(self.scene.frame_end))) + "d}"
        output = os.path.join(output_path, frame_numb_str.format(self.scene.frame_current))
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


    # callback to export the scene
    def update(self, data, scene):
        self.update_stats("", "Setting up render")
        if not self.is_preview:
            scene.frame_set(scene.frame_current)

        self.scene = scene
        render = scene.render

        fp = bpy.path.abspath(render.filepath)
        fp = os.path.realpath(fp)
        fp = os.path.normpath(fp)

        [self.sizeX, self.sizeY, self.bStartX, self.bStartY, self.bsizeX, self.bsizeY, camDummy] = yaf_scene.getRenderCoords(scene)

        if render.use_border:
            self.x = self.bsizeX
            self.y = self.bsizeY
        else:
            self.x = self.sizeX
            self.y = self.sizeY        

        if scene.gs_type_render == "file":
            self.setInterface(yafrayinterface.yafrayInterface_t())
            self.yi.setInputGamma(scene.gs_gamma_input, True)
            self.outputFile, self.output, self.file_type = self.decideOutputFileName(fp, scene.img_output)
            self.yi.paramsClearAll()
            self.yi.paramsSetString("type", self.file_type)
            self.yi.paramsSetBool("alpha_channel", render.image_settings.color_mode == "RGBA")
            self.yi.paramsSetBool("z_channel", scene.gs_z_channel)
            self.yi.paramsSetInt("width", self.x + self.bStartX)
            self.yi.paramsSetInt("height", self.y + self.bStartY)
            self.ih = self.yi.createImageHandler("outFile")
            self.co = yafrayinterface.imageOutput_t(self.ih, str(self.outputFile), 0, 0)

        elif scene.gs_type_render == "xml":
            self.setInterface(yafrayinterface.xmlInterface_t())
            self.yi.setInputGamma(scene.gs_gamma_input, True)
            self.outputFile, self.output, self.file_type = self.decideOutputFileName(fp, 'XML')
            self.yi.paramsClearAll()
            self.co = yafrayinterface.imageOutput_t()
            self.yi.setOutfile(self.outputFile)

        else:
            self.setInterface(yafrayinterface.yafrayInterface_t())
            self.yi.setInputGamma(scene.gs_gamma_input, True)

        self.yi.startScene()
        self.exportScene()
        self.yaf_integrator.exportIntegrator(self.scene)
        self.yaf_integrator.exportVolumeIntegrator(self.scene)

        # must be called last as the params from here will be used by render()
        yaf_scene.exportRenderSettings(self.yi, self.scene)

    # callback to render scene
    def render(self, scene):
        self.bl_use_postprocess = False

        if scene.gs_type_render == "file":
            self.yi.printInfo("Exporter: Rendering to file {0}".format(self.outputFile))
            self.update_stats("YafaRay Rendering:", "Rendering to {0}".format(self.outputFile))
            self.yi.render(self.co)
            result = self.begin_result(self.bStartX, self.bStartY, self.x + self.bStartX, self.y + self.bStartY)
            lay = result.layers[0]

            # exr format has z-buffer included, so no need to load '_zbuffer' - file
            if scene.gs_z_channel and not scene.img_output == 'OPEN_EXR':
                lay.load_from_file(self.output + '_zbuffer.' + self.file_type)
            else:
                lay.load_from_file(self.outputFile)

            self.end_result(result)

        elif scene.gs_type_render == "xml":
            self.yi.printInfo("Exporter: Writing XML to file {0}".format(self.outputFile))
            self.yi.render(self.co)

        else:

            def progressCallback(command, *args):
                if not self.test_break():
                    if command == "tag":
                        self.tag = args[0]
                    elif command == "progress":
                        self.prog = args[0]
                    self.update_stats("YafaRay Rendering... ", "{0}".format(self.tag))
                    # use blender's progress bar in the header to show progress of render
                    # update_progress needs float range 0.0 to 1.0, yafaray returns 0.0 to 100.0
                    self.update_progress(self.prog / 100)

            def drawAreaCallback(*args):
                x, y, w, h, tile = args
                res = self.begin_result(x, y, w, h)
                try:
                    res.layers[0].rect = tile
                except:
                    pass
                self.end_result(res)

            def flushCallback(*args):
                w, h, tile = args
                res = self.begin_result(0, 0, w, h)
                try:
                    res.layers[0].rect = tile
                except BaseException as e:
                    pass
                self.end_result(res)

            t = threading.Thread(
                                    target=self.yi.render,
                                    args=(self.sizeX, self.sizeY, 0, 0,
                                    self.is_preview,
                                    drawAreaCallback,
                                    flushCallback,
                                    progressCallback)
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

        self.yi.clearAll()
        del self.yi
        self.update_stats("", "Done!")
        self.bl_use_postprocess = True
