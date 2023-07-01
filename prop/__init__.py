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

if bpy.app.version >= (2, 80, 0):
    from . import preferences
else:
    from . import preferences_279
# from . import object
# from . import material
# from . import light
# from . import scene
# from . import camera
# from . import texture
# from . import world

if bpy.app.version >= (2, 80, 0):
    modules = (
        preferences,
        #object,
        #material,
        #light,
        #scene,
        #camera,
        #texture,
        #world,
    )
else:
    modules = (
        preferences_279,
        #object,
        #material,
        #light,
        #scene,
        #camera,
        #texture,
        #world,
    )

def register():
    for module in modules:
        module.register()

def unregister():
    for module in reversed(modules):
        module.unregister()