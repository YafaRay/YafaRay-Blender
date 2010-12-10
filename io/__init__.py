import bpy
#//----/ added path complete.. in one line??/------>
from yafaray.io import yaf_export, yaf_object


# register engine and panels
classes = [
    yaf_export.YafaRayRenderEngine,
    yaf_texture.yafTexture, #more classes....?
    yaf_light.yafLight,
    yaf_material.yafMaterial,
    #yaf_export.YafaRayCameraPoll,
    #yaf_export.YafaRayCameraButtonsPanel
    ]

def register():
    register = bpy.types.register
    for cls in classes:
        register(cls)

def unregister():    
    unregister = bpy.types.unregister
    for cls in classes:
        unregister(cls)

#yaf_properties.yaf_register_camera_types()
        
if __name__ == '__main__':
    register()