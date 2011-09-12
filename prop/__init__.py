from . import yaf_object
from . import yaf_material
from . import yaf_light


def register():
    yaf_object.register()
    yaf_material.register()
    yaf_light.register()


def unregister():
    yaf_object.unregister()
    yaf_material.unregister()
    yaf_light.unregister()
