import bpy
# import al files for register all classes

from yafaray.io import yaf_export
from yafaray.io import yaf_world
from yafaray.io import yaf_general_AA
from yafaray.io import yaf_integrator
from yafaray.io import yaf_texture
from yafaray.io import yaf_object
from yafaray.io import yaf_light
from yafaray.io import yaf_material
import yafrayinterface

classes = [
    yaf_export.YafaRayRenderEngine,
    yaf_world.yafWorld,
    yaf_general_AA.yafGeneralAA,
    yaf_integrator.yafIntegrator,
    yaf_texture.yafTexture,
    yaf_object.yafObject,
    yaf_light.yafLight,
    yaf_material.yafMaterial,

    ]


def register():

    register = bpy.types.register
    for cls in classes:
        register(cls)

def unregister():
    unregister = bpy.types.unregister
    for cls in classes:
        unregister(cls)


