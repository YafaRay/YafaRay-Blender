import bpy
import os
import time
import tempfile

#from yafaray import yafrayinterface
from yafaray.yaf_object import yafObject
from yafaray.yaf_config import PLUGIN_PATH,PATH_TO_ADD
from yafaray.yaf_light  import yafLight

import sys
sys.path.append(PATH_TO_ADD)
import yafrayinterface

#this is the name of our Render
IDNAME = 'YAFA_RENDER'

class YafaRayRenderEngine(bpy.types.RenderEngine):
    bl_idname = IDNAME
    bl_label = "YafaRay Render"
    
    def setInterface(self, yi):
        self.yi = yi
        self.yi.loadPlugins(PLUGIN_PATH)
        self.yaf_object = yafObject(self.yi)
        self.yaf_lamp = yafLight(self.yi)
    
    def exportObjects(self):
        self.yaf_object.createCamera(self.yi, self.scene)
        self.yaf_object.writeMeshes(self.yi, self.scene)
        self.yaf_lamp.createLights(self.yi,self.scene)
    
    def configureRender(self, w, h):
        # Integrators
        self.yi.paramsClearAll()
        self.yi.paramsSetString("type", "directlighting")
        self.yi.createIntegrator("default")
        
        self.yi.paramsClearAll()
        self.yi.paramsSetString("type", "none")
        self.yi.createIntegrator("volintegr")
        
        #some color in the background
        worldProp = {"bg_type":"Single Color",
                     "color":[0,0,255],
                     "ibl":0,
                     "ibl_samples":16,
                     "power":1.0
                    }
        c = worldProp["color"]
        self.yi.paramsSetColor("color", c[0], c[1], c[2])
        self.yi.paramsSetBool("ibl", worldProp["ibl"])
        self.yi.paramsSetInt("paramsSetBoolibl_samples", worldProp["ibl_samples"])
        self.yi.paramsSetFloat("power", worldProp["power"])
        self.yi.paramsSetString("type", "constant")
        self.yi.createBackground("world_background")
        # Render
        self.yi.paramsClearAll()
        self.yi.paramsSetString("camera_name", "cam")
        self.yi.paramsSetString("integrator_name", "default")
        self.yi.paramsSetString("volintegrator_name", "volintegr")
        self.yi.paramsSetString("background_name", "world_background")

        self.yi.paramsSetInt("width", w)
        self.yi.paramsSetInt("height", h)

    # callback to render scene
    def render(self, scene):
        self.scene = scene
        self.setInterface(yafrayinterface.yafrayInterface_t())
        self.yi.startScene()
        self.exportObjects()

        r = scene.render

        # compute resolution
        x= int(r.resolution_x*r.resolution_percentage*0.01)
        y= int(r.resolution_y*r.resolution_percentage*0.01)

        self.configureRender(x,y)

        # get a render result to write into
        result = self.begin_result(0, 0, x, y)
        lay = result.layers[0]

        # here we export blender scene and renders using yafaray
        outputFile = tempfile.mktemp(suffix='.tga')
        co = yafrayinterface.outTga_t(x, y, outputFile)

        self.update_stats("", "Rendering to %s" % outputFile)
        print("Rendering to %s" % outputFile)
        
        self.yi.render(co) 

        lay.load_from_file(outputFile)
       
        # done
        self.end_result(result)
        self.update_stats("", "Done!")

# Use some of the existing buttons.
import properties_render
properties_render.RENDER_PT_render.COMPAT_ENGINES.add(IDNAME)
properties_render.RENDER_PT_dimensions.COMPAT_ENGINES.add(IDNAME)
properties_render.RENDER_PT_antialiasing.COMPAT_ENGINES.add(IDNAME)
properties_render.RENDER_PT_output.COMPAT_ENGINES.add(IDNAME)
del properties_render
#
## Use only a subset of the world panels
#import properties_world
#properties_world.WORLD_PT_preview.COMPAT_ENGINES.add(IDNAME)
#properties_world.WORLD_PT_context_world.COMPAT_ENGINES.add(IDNAME)
#properties_world.WORLD_PT_world.COMPAT_ENGINES.add(IDNAME)
#properties_world.WORLD_PT_mist.COMPAT_ENGINES.add(IDNAME)
#del properties_world

class YafaRayCameraPoll(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "YafaRay Poll"

    def poll(self, context):
        import properties_data_camera
        
        if context.camera and context.scene.render.engine == IDNAME:
            try:
                properties_data_camera.unregister()
                #bpy.types.unregister(properties_data_camera.DATA_PT_camera)
            except:
                pass
        else:
            try:
                properties_data_camera.register()
                #bpy.types.register(properties_data_camera.DATA_PT_camera)
            except:
                pass
                    
        return False
        
    def draw(self, context):
        pass
        
class YafaRayCameraButtonsPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "YafaRay Camera"

    def poll(self, context):
        return context.camera and context.scene.render.engine == IDNAME
        
    def draw(self, context):
        narrowui = 180
        
        layout = self.layout

        cam = context.camera
        wide_ui = context.region.width > narrowui

        if wide_ui:
            layout.prop(cam, "YF_type")
        else:
            layout.prop(cam, "YF_type", text="")

        split = layout.split()

        col = split.column()
        if cam.YF_type in ['perspective','architecture']:
            if cam.lens_unit == 'MILLIMETERS':
                col.prop(cam, "lens", text="Angle")
            elif cam.lens_unit == 'DEGREES':
                col.prop(cam, "angle")
            if wide_ui:
                col = split.column()
            col.prop(cam, "lens_unit", text="")

            layout.prop(context.camera, "YF_aperture")
            layout.prop(context.camera, "YF_bokeh_type")
            layout.prop(context.camera, "YF_bokeh_rotation", slider=True)
            
        elif cam.YF_type == 'orthografic':
            col.prop(cam, "ortho_scale")

        elif cam.YF_type == 'angular':
            col.prop(context.camera, "YF_circular")
            col.prop(context.camera, "YF_mirrored")
            layout.prop(context.camera, "YF_max_angle", slider=True)
            layout.prop(context.camera, "YF_angle", slider=True)

        split = layout.split()

#        col = split.column(align=True)
#        col.label(text="Shift:")
#        col.prop(cam, "shift_x", text="X")
#        col.prop(cam, "shift_y", text="Y")
#
#        if wide_ui:
#            col = split.column(align=True)
#        col.label(text="Clipping:")
#        col.prop(cam, "clip_start", text="Start")
#        col.prop(cam, "clip_end", text="End")
#
        layout.label(text="Depth of Field:")

        split = layout.split()

        col = split.column()
        col.prop(cam, "dof_object", text="")

        if wide_ui:
            col = split.column()
        else:
            col = col.column()
        if cam.dof_object != None:
            col.enabled = False
        col.prop(cam, "dof_distance", text="Distance")
