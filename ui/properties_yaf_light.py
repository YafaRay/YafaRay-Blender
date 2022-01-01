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
import bpy
from ..util.ui_utils import light_from_context

# Inherit Light data block
if bpy.app.version >= (2, 80, 0):
    from bl_ui.properties_data_light import DataButtonsPanel
    from bl_ui.properties_data_light import DATA_PT_context_light
    DATA_PT_context_light.COMPAT_ENGINES.add('YAFARAY4_RENDER')
    del DATA_PT_context_light
else:
    from bl_ui.properties_data_lamp import DataButtonsPanel
    from bl_ui.properties_data_lamp import DATA_PT_context_lamp
    DATA_PT_context_lamp.COMPAT_ENGINES.add('YAFARAY4_RENDER')
    del DATA_PT_context_lamp

class YAFARAY4_PT_preview(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "Preview"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        light = light_from_context(context)
        return light and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        light = light_from_context(context)
        self.layout.template_preview(light)


class YAFARAY4_PT_light(DataButtonsPanel, Panel):
    bl_label = "Light"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout

        light = light_from_context(context)

        layout.prop(light, "light_type", expand=True)
        layout.prop(light, "light_enabled")

        if light.light_type == "area":
            layout.prop(light, "color")
            layout.prop(light, "yaf_energy", text="Power")
            layout.prop(light, "yaf_samples")
            layout.prop(light, "create_geometry")

        elif light.light_type == "spot":
            layout.prop(light, "color")
            layout.prop(light, "yaf_energy", text="Power")
            layout.prop(light, "spot_soft_shadows", toggle=True)

            if light.spot_soft_shadows:
                box = layout.box()
                box.prop(light, "yaf_samples")
                box.prop(light, "shadow_fuzzyness")

        elif light.light_type == "sun":
            layout.prop(light, "color")
            layout.prop(light, "yaf_energy", text="Power")
            layout.prop(light, "yaf_samples")
            layout.prop(light, "angle")

        elif light.light_type == "directional":
            layout.prop(light, "color")
            layout.prop(light, "yaf_energy", text="Power")
            layout.prop(light, "infinite")
            if not light.infinite:
                layout.prop(light, "shadow_soft_size", text="Radius of directional cone")

        elif light.light_type == "point":
            layout.prop(light, "color")
            layout.prop(light, "yaf_energy", text="Power")
            if hasattr(light, "use_sphere"):
                layout.prop(light, "use_sphere", toggle=True)
                if light.use_sphere:
                    box = layout.box()
                    box.prop(light, "yaf_sphere_radius")
                    box.prop(light, "yaf_samples")
                    box.prop(light, "create_geometry")

        elif light.light_type == "ies":
            layout.prop(light, "color")
            layout.prop(light, "yaf_energy", text="Power")
            layout.prop(light, "ies_file")
            layout.prop(light, "ies_soft_shadows", toggle=True)
            if light.ies_soft_shadows:
                layout.box().prop(light, "yaf_samples")

# povman test
class YAFARAY4_PT_area(DataButtonsPanel, Panel):
    bl_label = "Area Shape"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):
        light = light_from_context(context)
        engine = context.scene.render.engine
        return (light and light.type == 'AREA') and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout
        light = light_from_context(context)

        col = layout.column()
        col.row().prop(light, "shape", expand=True)
        sub = col.row(align=True)

        if light.shape == 'SQUARE':
            sub.prop(light, "size")
        elif light.shape == 'RECTANGLE':
            sub.prop(light, "size", text="Size X")
            sub.prop(light, "size_y", text="Size Y")
# end

class YAFARAY4_PT_spot(DataButtonsPanel, Panel):
    bl_label = "Spot Shape"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):
        light = light_from_context(context)
        engine = context.scene.render.engine
        return (light and light.light_type == "spot") and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout
        light = light_from_context(context)

        split = layout.split()
        col = split.column()
        col.prop(light, "spot_size", text="Size")
        col.prop(light, "yaf_show_dist_clip")
        if light.yaf_show_dist_clip:
            col.prop(light, "distance")
            col.prop(light, "shadow_buffer_clip_start", text="Clip Start")

        col = split.column()

        col.prop(light, "spot_blend", text="Blend", slider=True)
        col.prop(light, "show_cone")
        if light.yaf_show_dist_clip:
            col.label(text="")
            col.prop(light, "shadow_buffer_clip_end", text=" Clip End")

class YAFARAY4_PT_light_advanced(DataButtonsPanel, Panel):
    bl_label = "Advanced settings"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    
    def draw(self, context):
        layout = self.layout
        light = light_from_context(context)

        split = layout.split()
        col = split.column()
        col.row().prop(light, "cast_shadows")
        col = split.column()
        col.row().prop(light, "photon_only")

        split = layout.split()
        col = split.column()
        col.row().prop(light, "caustic_photons")
        col = split.column()
        col.row().prop(light, "diffuse_photons")


classes = (
    YAFARAY4_PT_preview,
    YAFARAY4_PT_light,
    YAFARAY4_PT_area,
    YAFARAY4_PT_spot,
    YAFARAY4_PT_light_advanced,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
