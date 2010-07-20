import bpy
import os
import time
import tempfile

import subprocess
import sys


import platform

#from yafaray import yafrayinterface
from yafaray.yaf_object import yafObject
from yafaray.yaf_config import PLUGIN_PATH,PATH_TO_ADD
from yafaray.yaf_light  import yafLight
from yafaray.yaf_world  import yafWorld
from yafaray.yaf_integrator import yafIntegrator
from yafaray.yaf_general_AA import yafGeneralAA

import sys
sys.path.append(PATH_TO_ADD)
import yafrayinterface

#this is the name of our Render
IDNAME = 'YAFA_RENDER'

class YafaRayRenderEngine(bpy.types.RenderEngine):
    bl_idname = IDNAME
    bl_preview = False
    bl_label = "YafaRay Render"
    
    def setInterface(self, yi):
        self.yi = yi
        self.yi.loadPlugins(PLUGIN_PATH)
        self.yaf_object  = yafObject(self.yi)
        self.yaf_lamp    = yafLight(self.yi)
        self.yaf_world   = yafWorld(self.yi)
        self.yaf_integrator = yafIntegrator(self.yi)
        self.yaf_general_aa = yafGeneralAA(self.yi)
    
    def exportObjects(self):
        self.yaf_object.createCamera(self.yi, self.scene)
        self.yaf_object.writeMeshes(self.yi, self.scene)
        self.yaf_lamp.createLights(self.yi,self.scene)
        self.yaf_world.exportWorld(self.scene)
    
    #    , w, h
    def configureRender(self):
        # Integrators
        self.yi.paramsClearAll()
        #self.yi.paramsSetString("type", "directlighting")
        #self.yi.createIntegrator("default")
        self.yaf_integrator.exportIntegrator(self.scene)
        self.yaf_general_aa.exportGeneralAA(self.scene)
        
        #self.yi.paramsClearAll()
        #self.yi.paramsSetString("type", "none")
        #self.yi.createIntegrator("volintegr")
        
        #some color in the background
        #worldProp = {"bg_type":"Single Color",
        #             "color":[0,0,255],
        #             "ibl":0,
        #             "ibl_samples":16,
        #             "power":1.0
        #            }
        #c = worldProp["color"]
        #self.yi.paramsSetColor("color", c[0], c[1], c[2])
        #self.yi.paramsSetBool("ibl", worldProp["ibl"])
        #self.yi.paramsSetInt("paramsSetBoolibl_samples", worldProp["ibl_samples"])
        #self.yi.paramsSetFloat("power", worldProp["power"])
        #self.yi.paramsSetString("type", "constant")
        #self.yi.createBackground("world_background")
        
        
        # Render
        #self.yi.paramsClearAll()
        #self.yi.paramsSetString("camera_name", "cam")
        #self.yi.paramsSetString("integrator_name", "default")
        #self.yi.paramsSetString("volintegrator_name", "volintegr")
        #self.yi.paramsSetString("background_name", "world_background")
        #
        #self.yi.paramsSetInt("width", w)
        #self.yi.paramsSetInt("height", h)

    # callback to render scene
    def render(self, scene):
        
        if scene.name != 'preview':
            
            self.scene = scene
        
            r = scene.render

            # compute resolution
            x= int(r.resolution_x*r.resolution_percentage*0.01)
            y= int(r.resolution_y*r.resolution_percentage*0.01)
        
            self.setInterface(yafrayinterface.yafrayInterface_t())
            
            print("the scene name is : " + scene.name )
            #print("the background type is : " + scene.bg_type)
            
            #newly added part
            #outputFile = self.getOutputFilename(frameNumber)
                        
            #format = self.yi.getImageFormatFromFullName(self.scene.properties["YafRay"]["Renderer"]["file_type"])
            #outputFile += '.' + format
            outputFile = tempfile.mktemp(suffix='.png')
                        
            self.yi.paramsClearAll()
            self.yi.paramsSetString("type", 'png')
            self.yi.paramsSetInt("width", x)
            self.yi.paramsSetInt("height", y)
            self.yi.paramsSetBool("alpha_channel", False)
            self.yi.paramsSetBool("z_channel", True)
                        
            ih = self.yi.createImageHandler("outFile")
            co = yafrayinterface.imageOutput_t(ih, outputFile)
                        
            self.yi.printInfo("Exporter: Rendering to file " + outputFile)
                
            self.yi.startScene()
            #end of added part
                
            #[co, outputFile]
            #self.yi.startScene()
            
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

