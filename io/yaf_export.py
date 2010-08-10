import bpy
import os
import time
import tempfile

import subprocess
import sys


import platform

#from yafaray import yafrayinterface
from yaf_object import yafObject
from yafaray import PLUGIN_PATH
from yaf_light  import yafLight
from yaf_world  import yafWorld
from yaf_integrator import yafIntegrator
from yaf_general_AA import yafGeneralAA
from yaf_texture import yafTexture
from yaf_material import yafMaterial

import sys
import yafrayinterface

#this is the name of our Render
IDNAME = 'YAFA_RENDER'

class YafaRayRenderEngine(bpy.types.RenderEngine):
    bl_idname = IDNAME
    bl_preview = False
    bl_label = "YafaRay Render"
    
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
        
    
    def exportObjects(self):
        self.yaf_object.createCamera(self.yi, self.scene)
        self.yaf_lamp.createLights(self.yi,self.scene)
        self.yaf_world.exportWorld(self.scene)
        self.yaf_texture.createTextures(self.yi, self.scene)
        self.exportMaterials()
        self.yaf_object.writeMeshes(self.yi, self.scene)



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

    def exportMaterial(self,material):
        if material:
            if material.mat_type == 'blend':
                # must make sure all materials used by a blend mat
                # are written before the blend mat itself
                self.handleBlendMat(material)
            else:
                self.materials.add(material)
                self.yaf_material.writeMaterial(material)
    
    def exportMaterials(self):
        self.yi.printInfo("Exporter: Processing Materials...")
        self.materials = set()
        self.yi.paramsClearAll()
        self.yi.paramsSetString("type", "shinydiffusemat")
        self.yi.printInfo("Exporter: Creating Material \"defaultMat\"")
        ymat = self.yi.createMaterial("defaultMat")
        self.materialMap["default"] = ymat
        
        for mat in bpy.data.materials:
            if mat in self.materials : continue
            self.exportMaterial(mat)
    
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
        outputFile = tempfile.mktemp(suffix = extension, dir = output_path)
        
        return outputFile,filetype


    # callback to render scene
    def render(self, scene):
        
        if scene.name != 'preview':
            
            scene.set_frame(scene.frame_current)
            self.scene = scene
        
            r = scene.render

            # compute resolution
            x= int(r.resolution_x*r.resolution_percentage*0.01)
            y= int(r.resolution_y*r.resolution_percentage*0.01)
        
            self.setInterface(yafrayinterface.yafrayInterface_t())
            
            print("the scene name is : " + scene.name )

            
            
            outputFile,file_type = self.decideOutputFileName(r.output_path, r.file_format)
                        
            self.yi.paramsClearAll()
            self.yi.paramsSetString("type", file_type)
            self.yi.paramsSetInt("width", x)
            self.yi.paramsSetInt("height", y)
            self.yi.paramsSetBool("alpha_channel", False)
            self.yi.paramsSetBool("z_channel", True)
                        
            ih = self.yi.createImageHandler("outFile")
            co = yafrayinterface.imageOutput_t(ih, outputFile)
                        
            self.yi.printInfo("Exporter: Rendering to file " + outputFile)
                
            self.yi.startScene()
            
            self.exportObjects()
            self.configureRender()
            
            # get a render result to write into
            result = self.begin_result(0, 0, x, y)
            lay = result.layers[0]
            
            # here we export blender scene and renders using yafaray
            #outputFile = tempfile.mktemp(suffix='.tga')
            #co = yafrayinterface.outTga_t(x, y, outputFile)
            
            self.update_stats("", "Rendering to %s" % outputFile)
            print("Rendering to %s" % outputFile)
            
            self.yi.render(co) 
            lay.load_from_file(outputFile)
            
            # done
            self.end_result(result)
            self.update_stats("", "Done!")
        #else:
        #    print("This is for preview")
        #    self.yi.startScene()
        #    self.exportObjects()
        #    self.configureRender(x,y)
        #    
        #    # get a render result to write into
        #    result = self.begin_result(0, 0, x, y)
        #    lay = result.layers[0]
        #    
        #    # here we export blender scene and renders using yafaray
        #    outputFile = tempfile.mktemp(suffix='.tga')
        #    co = yafrayinterface.outTga_t(x, y, outputFile)
        #    
        #    self.update_stats("", "Rendering to %s" % outputFile)
        #    print("Rendering to %s" % outputFile)
        #    
        #    self.yi.render(co) 
        #    lay.load_from_file(outputFile)
        #    
        #    # done
        #    self.end_result(result)
        #    self.update_stats("", "Done!")

        


# Use some of the existing buttons.
import properties_render
properties_render.RENDER_PT_render.COMPAT_ENGINES.add(IDNAME)
properties_render.RENDER_PT_dimensions.COMPAT_ENGINES.add(IDNAME)
#properties_render.RENDER_PT_antialiasing.COMPAT_ENGINES.add(IDNAME)
properties_render.RENDER_PT_output.COMPAT_ENGINES.add(IDNAME)
del properties_render

import properties_particle
properties_particle.PARTICLE_PT_context_particles.COMPAT_ENGINES.add(IDNAME)
properties_particle.PARTICLE_PT_emission.COMPAT_ENGINES.add(IDNAME)
properties_particle.PARTICLE_PT_hair_dynamics.COMPAT_ENGINES.add(IDNAME)
#properties_particle.PARTICLE_PT_cache.COMPAT_ENGINES.add(IDNAME)
properties_particle.PARTICLE_PT_velocity.COMPAT_ENGINES.add(IDNAME)
properties_particle.PARTICLE_PT_rotation.COMPAT_ENGINES.add(IDNAME)
properties_particle.PARTICLE_PT_physics.COMPAT_ENGINES.add(IDNAME)
properties_particle.PARTICLE_PT_boidbrain.COMPAT_ENGINES.add(IDNAME)
properties_particle.PARTICLE_PT_render.COMPAT_ENGINES.add(IDNAME)
properties_particle.PARTICLE_PT_draw.COMPAT_ENGINES.add(IDNAME)
#properties_particle.PARTICLE_PT_children.COMPAT_ENGINES.add(IDNAME)
properties_particle.PARTICLE_PT_force_fields.COMPAT_ENGINES.add(IDNAME)
#properties_particle.PARTICLE_PT_vertexgroups.COMPAT_ENGINES.add(IDNAME)
del properties_particle

