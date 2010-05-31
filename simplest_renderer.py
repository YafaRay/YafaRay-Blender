import bpy

class DummyRenderEngine(bpy.types.RenderEngine):
      
    bl_idname = 'YAF_RENDER_ENGINE'
    bl_label = "YafaRay"
    
    def render(self, scene):
       self.scene = scene
       print("yafaray renderer is called")
       

classes = [DummyRenderEngine]

def register():
    register = bpy.types.register
    for cls in classes:
        register(cls)


def unregister():
    unregister = bpy.types.unregister
    for cls in classes:
        unregister(cls)

if __name__ == "__main__":
    register()
