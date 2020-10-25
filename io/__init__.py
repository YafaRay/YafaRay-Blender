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

import yafaray4
from . import yaf_export
from . import yaf_world
from . import yaf_integrator
from . import yaf_texture
from . import yaf_object
from . import yaf_light
from . import yaf_material

modules = (
    yaf_export,
    #yaf_world,
    #yaf_integrator,
    #yaf_texture,
    #yaf_object,
    #yaf_light,
    #yaf_material,
)

def register():
    for module in modules:
        module.register()

def unregister():
    for module in reversed(modules):
        module.unregister()


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
