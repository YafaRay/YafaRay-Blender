import bpy

class YAF_PT_convert(bpy.types.Panel):
    bl_label = 'Convert old YafaRay Settings'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    COMPAT_ENGINES =['YAFA_RENDER']

    @classmethod
    def poll(self, context):
        engine = context.scene.render.engine
        return (True and (engine in self.COMPAT_ENGINES) ) 

    def draw(self, context):
        layout = self.layout
        layout.column().operator("data.convert_yafaray_properties", "Convert data form 2.4x")

