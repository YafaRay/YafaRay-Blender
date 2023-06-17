# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import bpy
from . import render
from . import camera
from . import material
from . import texture
from . import world
from . import strand
from . import object
from . import light
from . import scene
from . import general_settings
from . import integrator
from . import aa_settings

if bpy.app.version >= (2, 80, 0):
    pass   # FIXME BLENDER 2.80-3.00
else:
    from . import layer_passes

modules = (
    general_settings,
    aa_settings,
    integrator,
    render,
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
    if bpy.app.version >= (2, 80, 0):
        pass  # FIXME BLENDER 2.80-3.00
    else:
        layer_passes.register()


def unregister():
    if bpy.app.version >= (2, 80, 0):
        pass  # FIXME BLENDER 2.80-3.00
    else:
        layer_passes.unregister()
    for module in reversed(modules):
        module.unregister()


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)


from bl_ui import properties_object as properties_object
for member in dir(properties_object):  # add all "object" panels from blender
    subclass = getattr(properties_object, member)
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except:
        pass
del properties_object

from bl_ui import properties_particle as properties_particle
for member in dir(properties_particle):  # add all "particle" panels from blender
    subclass = getattr(properties_particle, member)
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except:
        pass
del properties_particle

from bl_ui import properties_data_mesh as properties_data_mesh
for member in dir(properties_data_mesh):  # add all "object data" panels from blender
    subclass = getattr(properties_data_mesh, member)
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except:
        pass
del properties_data_mesh

from bl_ui import properties_data_speaker as properties_data_speaker
for member in dir(properties_data_speaker):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_data_speaker, member)
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except:
        pass
del properties_data_speaker

from bl_ui import properties_scene as properties_scene
for member in dir(properties_scene):

    if member != "SCENE_PT_color_management":   #YafaRay Color management panel is customized in scene.
        #FIXME: The customized YafaRay panel appears at the end of the Blender scene tab panels, I don't know how to rearrange the panels to keep YafaRay color management in the same place as Blender Color Management panel was.

            subclass = getattr(properties_scene, member)
            try:
                if hasattr(subclass, 'COMPAT_ENGINES'):
                    subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
                else:
                    subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
            except:
                pass

del properties_scene

from bl_ui import properties_physics_cloth as properties_physics_cloth
for member in dir(properties_physics_cloth):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_cloth, member)
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except:
        pass
del properties_physics_cloth

from bl_ui import properties_physics_common as properties_physics_common
for member in dir(properties_physics_common):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_common, member)
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except:
        pass
del properties_physics_common

from bl_ui import properties_physics_dynamicpaint as properties_physics_dynamicpaint
for member in dir(properties_physics_dynamicpaint):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_dynamicpaint, member)
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except:
        pass
del properties_physics_dynamicpaint

from bl_ui import properties_physics_field as properties_physics_field
for member in dir(properties_physics_field):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_field, member)
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except:
        pass
del properties_physics_field

from bl_ui import properties_physics_fluid as properties_physics_fluid
for member in dir(properties_physics_fluid):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_fluid, member)
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except:
        pass
del properties_physics_fluid

from bl_ui import properties_physics_rigidbody as properties_physics_rigidbody
for member in dir(properties_physics_rigidbody):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_rigidbody, member)
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except:
        pass
del properties_physics_rigidbody

from bl_ui import properties_physics_rigidbody_constraint as properties_physics_rigidbody_constraint
for member in dir(properties_physics_rigidbody_constraint):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_rigidbody_constraint, member)
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except:
        pass
del properties_physics_rigidbody_constraint

if bpy.app.version >= (2, 80, 0):
    pass  # FIXME BLENDER 2.80-3.00
else:
    from bl_ui import properties_physics_smoke as properties_physics_smoke
    for member in dir(properties_physics_smoke):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
        subclass = getattr(properties_physics_smoke, member)
        try:
            if hasattr(subclass, 'COMPAT_ENGINES'):
                subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
            else:
                subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
        except:
            pass
    del properties_physics_smoke

from bl_ui import properties_physics_softbody as properties_physics_softbody
for member in dir(properties_physics_softbody):  # add all "speaker (SOC 2011, pepper branch)" panels from blender
    subclass = getattr(properties_physics_softbody, member)
    try:
        if hasattr(subclass, 'COMPAT_ENGINES'):
            subclass.COMPAT_ENGINES.add('YAFARAY4_RENDER')
        else:
            subclass.COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    except:
        pass
del properties_physics_softbody

