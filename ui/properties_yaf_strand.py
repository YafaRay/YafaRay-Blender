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

from bpy.types import Panel


class YAF_PT_strand_settings(Panel):
    bl_label = "Strand Settings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "particle"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):

        psys = context.object.particle_systems
        engine = context.scene.render.engine
        return (psys and (engine in cls.COMPAT_ENGINES))

    def draw(self, context):
        layout = self.layout

        yaf_mat = context.object.active_material
        if yaf_mat:
            tan = yaf_mat.strand

            split = layout.split()

            col = split.column()
            sub = col.column(align=True)
            sub.label(text="Size:")
            sub.prop(tan, "root_size", text="Root")
            sub.prop(tan, "tip_size", text="Tip")
            sub = col.column()
            col.prop(tan, "shape")
            col.prop(tan, "use_blender_units")

            col = split.column()
            col.label(text="Shading:")
            col.prop(tan, "width_fade")
            ob = context.object
            if ob and ob.type == 'MESH':
                col.prop_search(tan, "uv_layer", ob.data, "uv_textures", text="")
            else:
                col.prop(tan, "uv_layer", text="")


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
