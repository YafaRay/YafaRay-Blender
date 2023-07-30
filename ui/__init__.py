# SPDX-License-Identifier: GPL-2.0-or-later

import bpy

from . import camera
from . import light
from . import material
from . import object
from . import render
from . import scene
from . import strand
from . import texture
from . import world

if bpy.app.version >= (2, 80, 0):
    from . import layer_passes
    pass  # FIXME BLENDER >= v2.80
else:
    from . import layer_passes

modules = (
    render,
    layer_passes,
    camera,
    material,
    texture,
    world,
    strand,
    object,
    light,
    scene
)


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()


if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed, 
    # before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the 
    # "libyafaray4_bindings" compiled module is installed on
    register()

from bl_ui import properties_object as properties_object

for member in dir(properties_object):  # add all "object" panels from blender
    subclass = getattr(properties_object, member)
    # noinspection PyBroadException
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except Exception:
        pass
del properties_object

from bl_ui import properties_particle as properties_particle

for member in dir(properties_particle):  # add all "particle" panels from blender
    subclass = getattr(properties_particle, member)
    # noinspection PyBroadException
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except Exception:
        pass
del properties_particle

from bl_ui import properties_data_mesh as properties_data_mesh

for member in dir(properties_data_mesh):  # add all "object data" panels from blender
    subclass = getattr(properties_data_mesh, member)
    # noinspection PyBroadException
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except Exception:
        pass
del properties_data_mesh

from bl_ui import properties_data_speaker as properties_data_speaker

for member in dir(properties_data_speaker):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_data_speaker, member)
    # noinspection PyBroadException
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except Exception:
        pass
del properties_data_speaker

from bl_ui import properties_scene as properties_scene

for member in dir(properties_scene):

    if member != "SCENE_PT_color_management":  # YafaRay Color management panel is customized in scene.
        # FIXME: The customized YafaRay panel appears at the end of the Blender scene tab panels, I don't know how to
        #  rearrange the panels to keep YafaRay color management in the same place as Blender Color Management panel
        #  was.

        subclass = getattr(properties_scene, member)
        # noinspection PyBroadException
        try:
            if hasattr(subclass, 'COMPAT_ENGINES'):
                subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
            else:
                subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
        except Exception:
            pass

del properties_scene

from bl_ui import properties_physics_cloth as properties_physics_cloth

for member in dir(properties_physics_cloth):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_cloth, member)
    # noinspection PyBroadException
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except Exception:
        pass
del properties_physics_cloth

from bl_ui import properties_physics_common as properties_physics_common

for member in dir(properties_physics_common):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_common, member)
    # noinspection PyBroadException
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except Exception:
        pass
del properties_physics_common

from bl_ui import properties_physics_dynamicpaint as properties_physics_dynamicpaint

for member in dir(properties_physics_dynamicpaint):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_dynamicpaint, member)
    # noinspection PyBroadException
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except Exception:
        pass
del properties_physics_dynamicpaint

from bl_ui import properties_physics_field as properties_physics_field

for member in dir(properties_physics_field):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_field, member)
    # noinspection PyBroadException
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except Exception:
        pass
del properties_physics_field

from bl_ui import properties_physics_fluid as properties_physics_fluid

for member in dir(properties_physics_fluid):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_fluid, member)
    # noinspection PyBroadException
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except Exception:
        pass
del properties_physics_fluid

from bl_ui import properties_physics_rigidbody as properties_physics_rigidbody

for member in dir(properties_physics_rigidbody):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_rigidbody, member)
    # noinspection PyBroadException
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except Exception:
        pass
del properties_physics_rigidbody

from bl_ui import properties_physics_rigidbody_constraint as properties_physics_rigidbody_constraint

for member in dir(
        properties_physics_rigidbody_constraint):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_rigidbody_constraint, member)
    # noinspection PyBroadException
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except Exception:
        pass
del properties_physics_rigidbody_constraint

if bpy.app.version >= (2, 80, 0):
    pass  # FIXME BLENDER >= v2.80
else:
    # noinspection PyUnresolvedReferences
    from bl_ui import properties_physics_smoke as properties_physics_smoke

    for member in dir(properties_physics_smoke):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
        subclass = getattr(properties_physics_smoke, member)
        # noinspection PyBroadException
        try:
            if hasattr(subclass, 'COMPAT_ENGINES'):
                subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
            else:
                subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
        except Exception:
            pass
    del properties_physics_smoke

from bl_ui import properties_physics_softbody as properties_physics_softbody

for member in dir(properties_physics_softbody):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_softbody, member)
    # noinspection PyBroadException
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except Exception:
        pass
del properties_physics_softbody
