import bpy
from bpy.props import *

bpy.types.Scene.useViewToRender = BoolProperty(attr = "useViewToRender")
bpy.types.Scene.viewMatrix = FloatVectorProperty(attr = "viewMatrix", size = 16)


class RENDER_PT_render(bpy.types.Panel):

    bl_label = 'Render'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    COMPAT_ENGINES = ['YAFA_RENDER']
    
    @classmethod
    def poll(self, context):
        return (context.scene.render.engine in self.COMPAT_ENGINES)

    def draw(self, context):

        split = self.layout.split()

        split.column().operator("RENDER_OT_render", "Render Image", "RENDER_STILL")
        
        props = split.column().operator("RENDER_OT_render", "Render Animation", "RENDER_ANIMATION")
        props.animation = True
        
        if context.scene.render.engine == "YAFA_RENDER":
            self.layout.row().operator("RENDER_OT_render_view", "Render 3D View", "VIEW3D")
        
        self.layout.row().prop(context.scene.render, "display_mode")

