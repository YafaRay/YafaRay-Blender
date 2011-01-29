#TODO: Use Blender enumerators if any

import bpy
import os
import time
import tempfile
import sys
import platform

import yafrayinterface
from yafaray.io.yaf_object import yafObject
from yafaray import PLUGIN_PATH
from yafaray.io.yaf_light  import yafLight
from yafaray.io.yaf_world  import yafWorld
from yafaray.io.yaf_integrator import yafIntegrator
from yafaray.io.yaf_general_AA import yafGeneralAA
from yafaray.io.yaf_texture import yafTexture
from yafaray.io.yaf_material import yafMaterial

#import yafrayinterface

#this is the name of our Render
IDNAME = 'YAFA_RENDER'

class YafaRayRenderEngine(bpy.types.RenderEngine):
    bl_idname = IDNAME
    bl_use_preview = True
    bl_label = "YafaRay Render"
    progress = 0.0
    tag = ""

    def setInterface(self, yi):
        self.materialMap = {}
        self.materials   = set()
        self.yi = yi
        self.yi.loadPlugins(PLUGIN_PATH)
        self.yaf_object     = yafObject(self.yi, self.materialMap)
        self.yaf_lamp       = yafLight(self.yi)
        self.yaf_world      = yafWorld(self.yi)
        self.yaf_integrator = yafIntegrator(self.yi)
        self.yaf_general_aa = yafGeneralAA(self.yi)
        self.yaf_texture    = yafTexture(self.yi)
        self.yaf_material   = yafMaterial(self.yi, self.materialMap)

    def exportScene(self):
        self.yaf_world.exportWorld(self.scene)
        self.exportTextures()
        self.exportMaterials()
        self.yaf_object.createCamera(self.yi, self.scene)
        self.exportObjects()

    def exportTextures(self):
        # export textures from visible objects only. Won't work with
        # blend mat, there the textures need to be handled separately
        for obj in [o for o in self.scene.objects if (not o.hide_render and o.is_visible(self.scene))]:
            for mat_slot in [m for m in obj.material_slots if m.material]:
                for tex in [t for t in mat_slot.material.texture_slots if (t and t.texture)]:
                    self.yaf_texture.writeTexture(self.scene, tex.texture)

    def exportObjects(self):
        self.yi.printInfo("Exporter: Processing Objects...")

        idx=0      #TODO: REMOVE

        # export only visible objects
        for obj in [o for o in self.scene.objects if not o.hide_render and o.is_visible(self.scene)]:
            # if ob.is_duplicator and len(ob.particle_systems) < 1:
            if obj.is_duplicator:
                if obj.particle_systems:
                    # Check if we need to render emitter, if so do it
                    for psys in obj.particle_systems:
                        if psys.settings.use_render_emitter:
                            self.exportObject(obj, obj.matrix_local)
                            break
                obj.create_dupli_list(self.scene)
                for obj_dupli in obj.dupli_list:
                    #print ("Exporting INSTANCE OBJECT:",obj.object,obj.object.type)
                    self.exportObject(obj_dupli.object, obj_dupli.matrix, idx)    #TODO: Please kill that idx
                    idx += 1    #TODO: REMOVE

                if obj.dupli_list:
                    obj.free_dupli_list()
            else:
                if obj.parent and obj.parent.is_duplicator:
                    # this is an instanced object
                    continue
                #print ("Exporting REAL OBJECT:",o,o.type)
                self.exportObject(obj)


    def exportObject(self, obj, matrix=None, idx=None):
        # obj can be any object, even EMPTY or CAMERA

        # TODO: set a proper matrix if none?
        if matrix == None:
            matrix = obj.matrix_local #this change is at 18.7.10

        if obj.type == "MESH" or obj.type == "CURVE" or obj.type == "SURFACE":
                self.yaf_object.writeObject(self.yi, self.scene, obj, matrix)
        if obj.type == "LAMP":
                self.yaf_lamp.createLight(self.yi, obj, matrix, idx, (self.scene.name == "preview"))


    def handleBlendMat(self, mat):
        try:
            mat1_name =  mat.mat_material_one
            mat1      =  bpy.data.materials[mat1_name]

            mat2_name =  mat.mat_material_two
            mat2      =  bpy.data.materials[mat2_name]
        except:
            self.yi.printWarning("Exporter: Problem with blend material" + mat.name + ". Could not find one of the two blended materials.")
            return

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
                self.yaf_material.writeMaterial(material)


    #    , w, h
    def configureRender(self):
        # Integrators
        self.yi.paramsClearAll()
        self.yaf_integrator.exportIntegrator(self.scene)
        self.yaf_general_aa.exportGeneralAA(self.scene)

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

    def dummy(self):
        return self.yaf_general_aa.getRenderCoords(self.scene)

    # callback to render scene
    def render(self, scene):
        self.update_stats("", "Setting up render")

        if scene.name != "preview":
            scene.frame_set(scene.frame_current)
        self.scene = scene
        r = scene.render
        
        # compute resolution
        x= int(r.resolution_x*r.resolution_percentage*0.01)
        y= int(r.resolution_y*r.resolution_percentage*0.01)

        self.setInterface(yafrayinterface.yafrayInterface_t())

        outputFile,output,file_type = self.decideOutputFileName(r.filepath, r.file_format)

        self.yi.paramsClearAll()
        self.yi.paramsSetString("type", file_type)
        self.yi.paramsSetInt("width", x)
        self.yi.paramsSetInt("height", y)
        self.yi.paramsSetBool("alpha_channel", False)
        self.yi.paramsSetBool("z_channel", scene.gs_z_channel)

        self.yi.startScene()
        self.exportScene()
        self.configureRender()

        def prog_callback(command, *args):
            if not self.test_break():
                if command == "tag":
                    self.tag = args[0]
                elif command == "progress":
                    self.progress = args[0]
                self.update_stats("", "%s - %.2f %%" % (self.tag, self.progress))

        def tile_callback(command, *args):
            if command == "highliteArea":
                x0, y0, x1, y1, tile = args
                res = self.begin_result(x0, y0, x1-x0, y1-y0)
                try:
                    res.layers[0].rect = tile
                except BaseException as e:
                    print("Exception in tile callback with command ", command, ": ", e)
                    print(args, len(tile))
                self.update_result(res)
            elif command == "flushArea":
                x0, y0, x1, y1, tile = args
                res = self.begin_result(x0, y0, x1-x0, y1-y0)
                try:
                    res.layers[0].rect = tile
                except BaseException as e:
                    print("Exception in tile callback with command ", command, ": ", e)
                    print(args, len(tile))
                self.end_result(res)
            elif command == "flush":
                w, h, tile = args
                res = self.begin_result(0, 0, w, h)
                try:
                    res.layers[0].rect = tile
                except BaseException as e:
                    print("Exception in flush callback: ", e)
                    print(args, len(tile))
                self.update_result(res)

        if scene.gs_type_render == "file":
            self.yi.paramsSetString("type", file_type)
            ih = self.yi.createImageHandler("outFile")
            co = yafrayinterface.imageOutput_t(ih, str(outputFile), 0, 0)

            self.yi.printInfo("Exporter: Rendering to file " + outputFile)

            self.update_stats("", "Rendering to %s" % outputFile)

            self.yi.render(co)

            result = self.begin_result(0, 0, x, y)
            lay = result.layers[0]

            if scene.gs_z_channel:
                lay.load_from_file(output + '_zbuffer.' + file_type)
            else:
                lay.load_from_file(outputFile)

            self.end_result(result)

        if scene.gs_type_render == "into_blender":
            import threading
            t = threading.Thread(target=self.yi.render, args=(x, y, tile_callback, prog_callback))
            t.start()

            while t.isAlive() and not self.test_break():
                time.sleep(0.2)

            if t.isAlive():
                self.update_stats("", "Aborting...")
                self.yi.abort()
                t.join()
                self.update_stats("", "Render is aborted")
                return

        self.update_stats("", "Done!")

# Use some of the existing buttons.
# moved to /ui/__init__.py
"""
import properties_render, properties_particle

for panel in [properties_render.RENDER_PT_render,
              properties_render.RENDER_PT_dimensions,
              properties_render.RENDER_PT_output,
              properties_render.RENDER_PT_shading,
              properties_particle.PARTICLE_PT_context_particles,
              properties_particle.PARTICLE_PT_emission,
              properties_particle.PARTICLE_PT_hair_dynamics,
              properties_particle.PARTICLE_PT_velocity,
              properties_particle.PARTICLE_PT_rotation,
              properties_particle.PARTICLE_PT_physics,
              properties_particle.PARTICLE_PT_boidbrain,
              properties_particle.PARTICLE_PT_render,
              properties_particle.PARTICLE_PT_draw,
              properties_particle.PARTICLE_PT_force_fields]:
    panel.COMPAT_ENGINES.add(IDNAME)

del properties_render, properties_particle
"""
