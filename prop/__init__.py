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

from . import yaf_object
from . import yaf_material
from . import yaf_light
from . import yaf_scene
from . import yaf_camera
from . import yaf_texture
from . import yaf_world


def register():
    yaf_object.register()
    yaf_material.register()
    yaf_light.register()
    yaf_scene.register()
    yaf_camera.register()
    yaf_texture.register()
    yaf_world.register()


def unregister():
    yaf_object.unregister()
    yaf_material.unregister()
    yaf_light.unregister()
    yaf_scene.unregister()
    yaf_camera.unregister()
    yaf_texture.unregister()
    yaf_world.unregister()
