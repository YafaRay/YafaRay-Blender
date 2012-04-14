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

# Inherit Lamp data block
from bl_ui.properties_data_lamp import DATA_PT_context_lamp
DATA_PT_context_lamp.COMPAT_ENGINES.add('YAFA_RENDER')
del DATA_PT_context_lamp

class LampButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        lamp = context.lamp
        switchLampType = {'area': 'AREA', 'spot': 'SPOT', 'sun': 'SUN', 'point': 'POINT', 'ies': 'SPOT', 'directional': "SUN"}
        return lamp and ((lamp.lamp_type == cls.lamp_type) and (lamp.type == switchLampType.get(lamp.lamp_type, None)) and (engine in cls.COMPAT_ENGINES))


class YAF_PT_preview(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "Preview"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.lamp and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        self.layout.template_preview(context.lamp)


class YAF_PT_lamp_type(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "Lamp type"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.lamp and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout
        lamp = context.lamp

        layout.prop(lamp, "lamp_type", expand=True)


class YAF_PT_lamp_area(LampButtonsPanel, Panel):
    bl_label = "Area lamp settings"
    lamp_type = 'area'

    def draw(self, context):
        layout = self.layout
        lamp = context.lamp

        layout.prop(lamp, "color")
        layout.prop(lamp, "yaf_energy", text="Power")
        layout.prop(lamp, "yaf_samples")
        layout.prop(lamp, "create_geometry")


class YAF_PT_lamp_spot(LampButtonsPanel, Panel):
    bl_label = "Spot lamp settings"
    lamp_type = 'spot'

    def draw(self, context):
        layout = self.layout
        lamp = context.lamp

        layout.prop(lamp, "color")
        layout.prop(lamp, "yaf_energy", text="Power")
        layout.prop(lamp, "spot_soft_shadows", toggle=True)

        if lamp.spot_soft_shadows:
            box = layout.box()
            box.prop(lamp, "yaf_samples")
            box.prop(lamp, "shadow_fuzzyness")

        layout.prop(lamp, "photon_only")


class YAF_PT_spotshape(LampButtonsPanel, Panel):
    bl_label = "Spot shape settings"
    lamp_type = 'spot'

    def draw(self, context):
        layout = self.layout
        lamp = context.lamp

        split = layout.split()

        col = split.column()
        col.prop(lamp, "spot_size", text="Size")
        col.prop(lamp, "yaf_show_dist_clip")
        if lamp.yaf_show_dist_clip:
            col.prop(lamp, "distance")
            col.prop(lamp, "shadow_buffer_clip_start", text="Clip Start")

        col = split.column()

        col.prop(lamp, "spot_blend", text="Blend", slider=True)
        col.prop(lamp, "show_cone")
        if lamp.yaf_show_dist_clip:
            col.label(text="")
            col.prop(lamp, "shadow_buffer_clip_end", text=" Clip End")


class YAF_PT_lamp_sun(LampButtonsPanel, Panel):
    bl_label = "Sun lamp settings"
    lamp_type = 'sun'

    def draw(self, context):
        layout = self.layout
        lamp = context.lamp

        layout.prop(lamp, "color")
        layout.prop(lamp, "yaf_energy", text="Power")
        layout.prop(lamp, "yaf_samples")
        layout.prop(lamp, "angle")


class YAF_PT_lamp_directional(LampButtonsPanel, Panel):
    bl_label = "Directional lamp settings"
    lamp_type = 'directional'

    def draw(self, context):
        layout = self.layout
        lamp = context.lamp

        layout.prop(lamp, "color")
        layout.prop(lamp, "yaf_energy", text="Power")
        layout.prop(lamp, "infinite")
        if not lamp.infinite:
            layout.prop(lamp, "shadow_soft_size", text="Radius of directional cone")


class YAF_PT_lamp_point(LampButtonsPanel, Panel):
    bl_label = "Point lamp settings"
    lamp_type = 'point'

    def draw(self, context):
        layout = self.layout
        lamp = context.lamp

        layout.prop(lamp, "color")
        layout.prop(lamp, "yaf_energy", text="Power")
        if hasattr(lamp, "use_sphere"):
            layout.prop(lamp, "use_sphere", toggle=True)
            if lamp.use_sphere:
                box = layout.box()
                box.prop(lamp, "distance", text="Radius of sphere light")
                box.prop(lamp, "yaf_samples")
                box.prop(lamp, "create_geometry")


class YAF_PT_lamp_ies(LampButtonsPanel, Panel):
    bl_label = "IES lamp settings"
    lamp_type = 'ies'

    def draw(self, context):
        layout = self.layout
        lamp = context.lamp

        layout.prop(lamp, "color")
        layout.prop(lamp, "yaf_energy", text="Power")
        layout.prop(lamp, "ies_file")
        layout.prop(lamp, "ies_soft_shadows", toggle=True)
        if lamp.ies_soft_shadows:
            layout.box().prop(lamp, "yaf_samples")


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
