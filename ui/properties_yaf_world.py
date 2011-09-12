import bpy
# import types and props ---->
from bpy.types import Panel
from bpy.props import (EnumProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       IntProperty,
                       BoolProperty)
World = bpy.types.World


def call_world_update(self, context):
    world = context.scene.world
    world.ambient_color = world.ambient_color

World.bg_type = EnumProperty(
    name="Background",
    items=(
        ('Gradient', "Gradient", "Gradient background"),
        ('Texture', "Texture", "Textured background"),
        ('Sunsky1', "Sunsky1", "Sunsky background"),
        ('Sunsky2', "Sunsky2", "New model of Sunsky background"),
        ('Single Color', "Single Color", "Single color background")
    ),
    default="Single Color",
    update=call_world_update)

World.bg_color_space = EnumProperty(
    name="Color space",
    items=(
        ('CIE (E)', "CIE (E)", "Select color space model"),
        ('CIE (D50)', "CIE (D50)", "Select color space model"),
        ('sRGB (D65)', "sRGB (D65)", "Select color space model"),
        ('sRGB (D50)', "sRGB (D50)", "Select color space model")
    ),
    default="CIE (E)",
    update=call_world_update)

World.bg_zenith_color = FloatVectorProperty(
    name="Zenith color",
    description="Zenith color",
    subtype='COLOR',
    min=0.0, max=1.0,
    default=(0.57, 0.65, 1.0),
    update=call_world_update)

World.bg_horizon_color = FloatVectorProperty(
    name="Horizon color",
    description="Horizon color",
    subtype='COLOR',
    min=0.0, max=1.0,
    default=(1.0, 1.0, 0.5),
    update=call_world_update)

World.bg_zenith_ground_color = FloatVectorProperty(
    name="Zenith ground color",
    description="Zenith ground color",
    subtype='COLOR',
    min=0.0, max=1.0,
    default=(1.0, 0.9, 0.8),
    update=call_world_update)

World.bg_horizon_ground_color = FloatVectorProperty(
    name="Horizon ground color",
    description="Horizon ground color",
    subtype='COLOR',
    min=0.0, max=1.0,
    default=(0.8, 0.6, 0.3),
    update=call_world_update)

World.bg_single_color = FloatVectorProperty(
    name="Background color",
    description="Background color",
    subtype='COLOR',
    min=0.0, max=1.0,
    default=(0.7, 0.7, 0.7),
    update=call_world_update)

World.bg_use_ibl = BoolProperty(
    name="Use IBL",
    description="Use the background as the light source for your image",
    default=False)

World.bg_with_caustic = BoolProperty(
    name="Caustic photons",
    description="Allow background light to shoot caustic photons",
    default=True)

World.bg_with_diffuse = BoolProperty(
    name="Diffuse photons",
    description="Allow background light to shoot diffuse photons",
    default=True)

World.bg_ibl_samples = IntProperty(
    name="IBL Samples",
    description="Number of samples for direct lighting from background",
    min=1, max=512,
    default=16)

World.bg_rotation = FloatProperty(
    name="Rotation",
    description="Rotation offset of background texture",
    min=0.0, max=360.0,
    default=0.0,
    update=call_world_update)

World.bg_turbidity = FloatProperty(
    name="Turbidity",
    description="Turbidity of the atmosphere",
    min=1.0, max=20.0,
    default=2.0,
    update=call_world_update)

World.bg_ds_turbidity = FloatProperty(  # Darktides turbidity has different values
    name="Turbidity",
    description="Turbidity of the atmosphere",
    min=2.0, max=12.0,
    default=2.0,
    update=call_world_update)

World.bg_a_var = FloatProperty(
    name="Brightness of horizon gradient",
    description="Darkening or brightening towards horizon",
    min=0.0, max=10.0,
    default=1.0,
    update=call_world_update)

World.bg_b_var = FloatProperty(
    name="Luminance of horizon",
    description="Luminance gradient near the horizon",
    min=0.0, max=10.0,
    default=1.0,
    update=call_world_update)

World.bg_c_var = FloatProperty(
    name="Solar region intensity",
    description="Relative intensity of circumsolar region",
    min=0.0, max=10.0,
    default=1.0,
    update=call_world_update)

World.bg_d_var = FloatProperty(
    name="Width of circumsolor region",
    description="Width of circumsolar region",
    min=0.0, max=10.0,
    default=1.0,
    update=call_world_update)

World.bg_e_var = FloatProperty(
    name="Backscattered light",
    description="Relative backscattered light",
    min=0.0, max=10.0,
    default=1.0,
    update=call_world_update)

World.bg_from = FloatVectorProperty(
    name="Set sun position",
    description="Set the position of the sun",
    subtype='DIRECTION',
    step=10, precision=3,
    min=-1.0, max=1.0,
    default=(1.0, 1.0, 1.0),
    update=call_world_update)

World.bg_add_sun = BoolProperty(
    name="Add sun",
    description="Add a real sun light",
    default=False,
    update=call_world_update)

World.bg_sun_power = FloatProperty(
    name="Sunlight power",
    description="Sunlight power",
    min=0.0, max=10.0,
    default=1.0,
    update=call_world_update)

World.bg_background_light = BoolProperty(
    name="Add skylight",
    description="Add skylight",
    default=False,
    update=call_world_update)

World.bg_light_samples = IntProperty(
    name="Samples",
    description="Set skylight and sunlight samples",
    min=1, max=512,
    default=16,
    update=call_world_update)

World.bg_dsaltitude = FloatProperty(
    name="Altitude",
    description="Moves the sky dome above or below the camera position",
    min=-1.0, max=2.0,
    default=0.0,
    update=call_world_update)

World.bg_dsnight = BoolProperty(
    name="Night",
    description="Activate experimental night mode",
    default=False,
    update=call_world_update)

World.bg_dsbright = FloatProperty(
    name="Sky brightness",
    description="Brightness of the sky",
    min=0.0, max=10.0,
    default=1.0,
    update=call_world_update)

World.bg_power = FloatProperty(
    name="Skylight power",
    description="Multiplier for background color",
    min=0.0, max=10.0,
    default=1.0,
    update=call_world_update)

World.bg_exposure = FloatProperty(
    name="Exposure",
    description="Exposure correction for the sky (0 = no correction)",
    min=0.0, max=10.0,
    default=1.0,
    update=call_world_update)

World.bg_clamp_rgb = BoolProperty(
    name="Clamp RGB",
    description="Clamp RGB values",
    default=False)

World.bg_gamma_enc = BoolProperty(
    name="Gamma encoding",
    description="Apply gamma encoding to the sky",
    default=True,
    update=call_world_update)


class YAFWORLD_PT_preview(Panel):
    bl_label = "Background Preview"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "world"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return (context.world) and (not rd.use_game_engine) and (rd.engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        self.layout.template_preview(context.world)


class YAFWORLD_PT_world(Panel):

    bl_label = 'Background Settings'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'world'
    ibl = True
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return context.world and (rd.engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout
        world = context.world

        split = layout.split()
        col = layout.column()
        col.prop(world, 'bg_type', text="Background")

        if world.bg_type == "Gradient":

            split = layout.split(percentage=0.40)
            col = split.column()
            col.label(text="Zenith:")
            col.label(text="Horizon:")
            col.label(text="Horizon ground:")
            col.label(text="Zenith ground:")

            col = split.column()
            col.prop(world, 'bg_zenith_color', text="")
            col.prop(world, 'bg_horizon_color', text="")
            col.prop(world, 'bg_horizon_ground_color', text="")
            col.prop(world, 'bg_zenith_ground_color', text="")

            split = layout.split(percentage=0.40)
            col = split.column()
            col.prop(world, 'bg_use_ibl')
            col.label(text=" ")

        elif world.bg_type == "Texture":

            tex = context.scene.world.active_texture

            if tex is not None:  # and tex.type == 'IMAGE': # revised if changed to yaf_tex_type
                try:
                    layout.template_ID(context.world, 'active_texture')  # new='texture.new')
                except:
                    pass
                if  tex.type == "IMAGE":  # it allows to change the used image
                    try:
                        layout.template_image(tex, "image", tex.image_user, compact=True)
                    except:
                        pass
            else:
                try:
                    layout.template_ID(context.world, "active_texture", new="texture.new")
                except:  # TODO: create only image texture? procedural not supported.. ?
                    pass
            layout.prop(world, "bg_rotation")

            split = layout.split(percentage=0.33)

            col = split.column()
            col.prop(world, "bg_use_ibl")
            if world.bg_use_ibl:
                row = layout.row()
                row.prop(world, "bg_with_diffuse")
                row.prop(world, "bg_with_caustic")
            else:
                col = layout.column()
                col.label(text=" ")
                col.label(text=" ")

        elif world.bg_type == "Sunsky1":
            self.ibl = False
            layout.separator()
            sub = layout.column(align=True)
            sub.prop(world, "bg_turbidity")
            sub.prop(world, "bg_a_var")
            sub.prop(world, "bg_b_var")
            sub.prop(world, "bg_c_var")
            sub.prop(world, "bg_d_var")
            sub.prop(world, "bg_e_var")

            split = layout.split()
            col = split.column()
            col.label(text="Set sun position:")
            col.prop(world, "bg_from", text="")

            col = split.column()
            col.label(text=" ")
            sub = col.column(align=True)
            sub.operator("world.get_position", text="Get Position")
            sub.operator("world.get_angle", text="Get Angle")
            sub.operator("world.update_sun", text="Update Sun")

            layout.separator()

            split = layout.split()
            col = split.column()
            col.prop(world, "bg_add_sun")
            if world.bg_add_sun:
                col.prop(world, "bg_sun_power")
            else:
                col.label(text=" ")

            col = split.column()
            col.prop(world, "bg_background_light")
            if world.bg_background_light:
                col.prop(world, "bg_power")
            else:
                col.label(text=" ")

            layout.column().prop(world, "bg_light_samples")

        ## DarkTide Sunsky NOT more updated? ----->
        elif world.bg_type == "Sunsky2":
            self.ibl = False
            layout.separator()
            sub = layout.column(align=True)
            sub.prop(world, "bg_ds_turbidity")
            sub.prop(world, "bg_a_var")
            sub.prop(world, "bg_b_var")
            sub.prop(world, "bg_c_var")
            sub.prop(world, "bg_d_var")
            sub.prop(world, "bg_e_var")

            split = layout.split()
            col = split.column()
            col.label(text="Set sun position:")
            col.prop(world, "bg_from", text="")
            col.prop(world, "bg_dsnight")

            col = split.column()
            col.label(text=" ")
            sub = col.column(align=True)
            sub.operator("world.get_position", text="Get Position")
            sub.operator("world.get_angle", text="Get Angle")
            sub.operator("world.update_sun", text="Update Sun")
            col.prop(world, "bg_dsaltitude")

            layout.separator()

            split = layout.split()
            col = split.column()
            col.prop(world, "bg_add_sun")
            if world.bg_add_sun:
                col.prop(world, "bg_sun_power")
            else:
                col.label(text=" ")
            if world.bg_background_light:
                col.prop(world, "bg_with_diffuse")
            else:
                col.label(text=" ")

            col = split.column()
            col.prop(world, "bg_background_light")
            if world.bg_background_light:
                col.prop(world, "bg_power")
            else:
                col.label(text=" ")
            if world.bg_background_light:
                col.prop(world, "bg_with_caustic")
            else:
                col.label(text=" ")

            split = layout.split()
            col = split.column()
            col.prop(world, "bg_exposure")
            col = split.column()
            col.prop(world, "bg_dsbright")

            layout.column().prop(world, "bg_light_samples")

            split = layout.split()
            col = split.column()
            col.prop(world, "bg_clamp_rgb")
            col = split.column()
            col.prop(world, "bg_gamma_enc")

            layout.column().prop(world, "bg_color_space")

        elif world.bg_type == "Single Color":

            split = layout.split(percentage=0.33)

            col = split.column()
            col.label("Color:")
            col = split.column()
            col.prop(world, "bg_single_color", text="")

            split = layout.split(percentage=0.33)
            col = split.column()
            col.prop(world, "bg_use_ibl")
            col.label(text=" ")

        if world.bg_use_ibl and self.ibl:
            # for all options that uses IBL
            col = split.column()
            col.prop(world, "bg_ibl_samples")
            col.prop(world, "bg_power")

from . import properties_yaf_volume_integrator
