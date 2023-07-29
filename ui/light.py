# SPDX-License-Identifier: GPL-2.0-or-later

# noinspection PyUnresolvedReferences
from bpy.types import Panel
import bpy

# Inherit Light data block
if bpy.app.version >= (2, 80, 0):
    from bl_ui.properties_data_light import DataButtonsPanel
    from bl_ui.properties_data_light import DATA_PT_context_light
    DATA_PT_context_light.COMPAT_ENGINES.add('YAFARAY4_RENDER')
    del DATA_PT_context_light
else:
    # noinspection PyUnresolvedReferences
    from bl_ui.properties_data_lamp import DataButtonsPanel
    # noinspection PyUnresolvedReferences
    from bl_ui.properties_data_lamp import DATA_PT_context_lamp
    DATA_PT_context_lamp.COMPAT_ENGINES.add('YAFARAY4_RENDER')
    del DATA_PT_context_lamp

if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed, 
    # before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the 
    # "libyafaray4_bindings" compiled module is installed on. Assuming that the YafaRay-Plugin exporter is installed 
    # in a folder named "yafaray4" within the addons Blender directory
    # noinspection PyUnresolvedReferences
    import yafaray4.prop.light
    yafaray4.prop.light.register()


def light_from_context(context):
    if bpy.app.version >= (2, 80, 0):
        return context.light
    else:
        return context.lamp


class Preview(Panel):
    bl_idname = "YAFARAY4_PT_light_preview"
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


class Light(DataButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_light"
    bl_label = "Light"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        layout = self.layout

        light = light_from_context(context)

        layout.prop(light, "lamp_type", expand=True)
        layout.prop(light, "light_enabled")

        if light.lamp_type == "area":
            layout.prop(light, "color")
            layout.prop(light, "yaf_energy", text="Power")
            layout.prop(light, "yaf_samples")
            layout.prop(light, "create_geometry")

        elif light.lamp_type == "spot":
            layout.prop(light, "color")
            layout.prop(light, "yaf_energy", text="Power")
            layout.prop(light, "spot_soft_shadows", toggle=True)

            if light.spot_soft_shadows:
                box = layout.box()
                box.prop(light, "yaf_samples")
                box.prop(light, "shadow_fuzzyness")

        elif light.lamp_type == "sun":
            layout.prop(light, "color")
            layout.prop(light, "yaf_energy", text="Power")
            layout.prop(light, "yaf_samples")
            layout.prop(light, "angle")

        elif light.lamp_type == "directional":
            layout.prop(light, "color")
            layout.prop(light, "yaf_energy", text="Power")
            layout.prop(light, "infinite")
            if not light.infinite:
                layout.prop(light, "shadow_soft_size", text="Radius of directional cone")

        elif light.lamp_type == "point":
            layout.prop(light, "color")
            layout.prop(light, "yaf_energy", text="Power")
            if hasattr(light, "use_sphere"):
                layout.prop(light, "use_sphere", toggle=True)
                if light.use_sphere:
                    box = layout.box()
                    box.prop(light, "yaf_sphere_radius")
                    box.prop(light, "yaf_samples")
                    box.prop(light, "create_geometry")

        elif light.lamp_type == "ies":
            layout.prop(light, "color")
            layout.prop(light, "yaf_energy", text="Power")
            layout.prop(light, "ies_file")
            layout.prop(light, "ies_soft_shadows", toggle=True)
            if light.ies_soft_shadows:
                layout.box().prop(light, "yaf_samples")


class Area(DataButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_light_area"
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


class Spot(DataButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_light_spot"
    bl_label = "Spot Shape"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):
        light = light_from_context(context)
        engine = context.scene.render.engine
        return (light and light.lamp_type == "spot") and (engine in cls.COMPAT_ENGINES)

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


class LightAdvanced(DataButtonsPanel, Panel):
    bl_idname = "YAFARAY4_PT_light_advanced"
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
    Preview,
    Light,
    Area,
    Spot,
    LightAdvanced,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed, 
    # before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the 
    # "libyafaray4_bindings" compiled module is installed on
    register()
