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
from bl_ui.properties_data_lamp import DataButtonsPanel

# Inherit Lamp data block
from bl_ui.properties_data_lamp import DATA_PT_context_lamp
DATA_PT_context_lamp.COMPAT_ENGINES.add('YAFA_E3_RENDER')
del DATA_PT_context_lamp    

class YAFA_E3_PT_preview(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "Preview"
    COMPAT_ENGINES = {'YAFA_E3_RENDER'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.lamp and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        self.layout.template_preview(context.lamp)


class YAFA_E3_PT_lamp(DataButtonsPanel, Panel):
    bl_label = "Lamp"
    COMPAT_ENGINES = {'YAFA_E3_RENDER'}

    def draw(self, context):
        layout = self.layout

        lamp = context.lamp

        layout.prop(lamp, "lamp_type", expand=True)
        layout.prop(lamp, "light_enabled")

        if lamp.lamp_type == "area":
            layout.prop(lamp, "color")
            layout.prop(lamp, "yaf_energy", text="Power")
            layout.prop(lamp, "yaf_samples")
            layout.prop(lamp, "create_geometry")

        elif lamp.lamp_type == "spot":
            layout.prop(lamp, "color")
            layout.prop(lamp, "yaf_energy", text="Power")
            layout.prop(lamp, "spot_soft_shadows", toggle=True)

            if lamp.spot_soft_shadows:
                box = layout.box()
                box.prop(lamp, "yaf_samples")
                box.prop(lamp, "shadow_fuzzyness")

        elif lamp.lamp_type == "sun":
            layout.prop(lamp, "color")
            layout.prop(lamp, "yaf_energy", text="Power")
            layout.prop(lamp, "yaf_samples")
            layout.prop(lamp, "angle")

        elif lamp.lamp_type == "directional":
            layout.prop(lamp, "color")
            layout.prop(lamp, "yaf_energy", text="Power")
            layout.prop(lamp, "infinite")
            if not lamp.infinite:
                layout.prop(lamp, "shadow_soft_size", text="Radius of directional cone")

        elif lamp.lamp_type == "point":
            layout.prop(lamp, "color")
            layout.prop(lamp, "yaf_energy", text="Power")
            if hasattr(lamp, "use_sphere"):
                layout.prop(lamp, "use_sphere", toggle=True)
                if lamp.use_sphere:
                    box = layout.box()
                    box.prop(lamp, "yaf_sphere_radius")
                    box.prop(lamp, "yaf_samples")
                    box.prop(lamp, "create_geometry")

        elif lamp.lamp_type == "ies":
            layout.prop(lamp, "color")
            layout.prop(lamp, "yaf_energy", text="Power")
            layout.prop(lamp, "ies_file")
            layout.prop(lamp, "ies_soft_shadows", toggle=True)
            if lamp.ies_soft_shadows:
                layout.box().prop(lamp, "yaf_samples")

# povman test
class YAFA_E3_PT_area(DataButtonsPanel, Panel):
    bl_label = "Area Shape"
    COMPAT_ENGINES = {'YAFA_E3_RENDER'}

    @classmethod
    def poll(cls, context):
        lamp = context.lamp
        engine = context.scene.render.engine
        return (lamp and lamp.type == 'AREA') and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        lamp = context.lamp

        col = layout.column()
        col.row().prop(lamp, "shape", expand=True)
        sub = col.row(align=True)

        if lamp.shape == 'SQUARE':
            sub.prop(lamp, "size")
        elif lamp.shape == 'RECTANGLE':
            sub.prop(lamp, "size", text="Size X")
            sub.prop(lamp, "size_y", text="Size Y")
# end

class YAFA_E3_PT_spot(DataButtonsPanel, Panel):
    bl_label = "Spot Shape"
    COMPAT_ENGINES = {'YAFA_E3_RENDER'}

    @classmethod
    def poll(cls, context):
        lamp = context.lamp
        engine = context.scene.render.engine
        return (lamp and lamp.lamp_type == "spot") and (engine in cls.COMPAT_ENGINES)

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

class YAFA_E3_PT_lamp_advanced(DataButtonsPanel, Panel):
    bl_label = "Advanced settings"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'YAFA_E3_RENDER'}
    
    def draw(self, context):
        layout = self.layout
        lamp = context.lamp

        split = layout.split()
        col = split.column()
        col.row().prop(lamp, "cast_shadows")
        col = split.column()
        col.row().prop(lamp, "photon_only")

        split = layout.split()
        col = split.column()
        col.row().prop(lamp, "caustic_photons")
        col = split.column()
        col.row().prop(lamp, "diffuse_photons")


if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
