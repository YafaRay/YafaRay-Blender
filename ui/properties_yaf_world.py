import bpy
# import types and props ---->
from bpy.props import *
World = bpy.types.World
#TODO: Update default values, edit description

def call_world_update(self, context):
    wrld = context.scene.world
    wrld.ambient_color = wrld.ambient_color

World.bg_type = EnumProperty(
    items = (
        ("Gradient", "Gradient", ""),
        ("Texture", "Texture", ""),
        ("Sunsky", "Sunsky", ""),
        ("Darktide's Sunsky", "Darktide's Sunsky", ""),
        ("Single Color", "Single Color", "")
    ),
    default = "Single Color",
    name = "Background Type", update = call_world_update)

World.bg_zenith_ground_color = FloatVectorProperty(
                                            subtype = "COLOR",
                                            min = 0.0, max = 1.0,
                                            default = (1, 0.9, 0.8), update = call_world_update)

World.bg_horizon_ground_color = FloatVectorProperty(
                                            subtype = "COLOR",
                                            min = 0.0, max = 1.0,
                                            default = (0.8, 0.6, 0.3), update = call_world_update)

World.bg_single_color =     FloatVectorProperty(description = "Background color",
                                            subtype = 'COLOR',
                                            min = 0.0, max = 1.0,
                                            default = (0.7, 0.7, 0.7), update = call_world_update)

World.bg_use_ibl =          BoolProperty(
                                            description = "Use IBL",
                                            default = False)
World.bg_ibl_samples =      IntProperty(
                                            description = "Amount of samples",
                                            default = 16,
                                            min = 1, max = 512)
World.bg_rotation =         FloatProperty(
                                            description = "",
                                            default = 0.0,
                                            min = 0, max = 360, update = call_world_update)
World.bg_turbidity =        FloatProperty(
                                            description = "",
                                            default = 2.0,
                                            min = 1.0, max = 20.0, update = call_world_update)
World.bg_a_var =            FloatProperty(
                                            description = "",
                                            default = 1.0,
                                            min = 0, max =10, update = call_world_update)
World.bg_b_var =            FloatProperty(
                                            default = 1.0,
                                            min = 0, max = 10, update = call_world_update)
World.bg_c_var =            FloatProperty(
                                            description = "",
                                            default = 1.0,
                                            min = 0, max =10, update = call_world_update)
World.bg_d_var =            FloatProperty(
                                            description = "",
                                            default = 1.0,
                                            min = 0, max = 10, update = call_world_update)
World.bg_e_var =            FloatProperty(
                                            description = "",
                                            default = 1.0,
                                            min = 0, max = 10, update = call_world_update)
World.bg_from =             FloatVectorProperty(
                                            description = "Point Info", subtype = "DIRECTION",
                                            default = (0.5, 0.5, 0.5),
                                            step = 10, precision = 3,
                                            min = -1, max = 1, update = call_world_update)
World.bg_add_sun =          BoolProperty(default = False, update = call_world_update)
World.bg_sun_power =        FloatProperty(
                                            description = "",
                                            default = 1.0,
                                            min = 0, max = 10, update = call_world_update)
World.bg_background_light = BoolProperty(
                                            description = "",
                                            default = False, update = call_world_update)
World.bg_light_samples =    IntProperty(
                                            description = "",
                                            default = 16,
                                            min = 1, max = 512, update = call_world_update)
World.bg_dsaltitude =       FloatProperty(
                                            description = "",
                                            default = 0.0,
                                            min = -1, max = 2, update = call_world_update)
World.bg_dsnight =          BoolProperty(
                                            description = "",
                                            default = False, update = call_world_update)
World.bg_dsbright =         FloatProperty(
                                            description = "",
                                            default = 1.0,
                                            min = 0, max = 10, update = call_world_update)
World.bg_power =            FloatProperty(
                                            description = "Multiplier for Background Color",
                                            default = 1.0,
                                            min = 0, max = 10, update = call_world_update)

World.bg_exposure =         FloatProperty(
                                            description = "",
                                            default = 1.0,
                                            min = 0, max = 10, update = call_world_update)
World.bg_clamp_rgb =        BoolProperty(
                                            description = "",
                                            default = False, update = call_world_update)
World.bg_gamma_enc =        BoolProperty(
                                            description = "",
                                            default = True, update = call_world_update)


class YAFWORLD_PT_preview(bpy.types.Panel):
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


class YAFWORLD_PT_world(bpy.types.Panel):

    bl_label = 'Background Settings'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'world'
    ibl = True
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(self, context):

        return context.world and (context.scene.render.engine in self.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        world = context.world

        split = layout.split()

        col = layout.column()
        col.prop(world, "bg_type", text = "Background")

        if world.bg_type == 'Gradient':

            split = layout.split(percentage = 0.40)

            col = split.column()
            col.label(text = "Zenith Color:")
            col.label(text = "Horizon Color:")
            col.label(text = "Horizon Ground Color:")
            col.label(text = "Zenith Ground Color:")

            col = split.column()
            col.prop(world, "zenith_color", text = "")
            col.prop(world, "horizon_color", text = "")
            col.prop(world, "bg_horizon_ground_color", text = "")
            col.prop(world, "bg_zenith_ground_color", text = "")

            split = layout.split(percentage = 0.40)

            col = split.column(align = True)
            col.prop(world, "bg_use_ibl", text = "Use IBL")
            col.label(text = " ")

        elif world.bg_type == 'Texture':

            tex = context.scene.world.active_texture

            if tex is not None:  # and tex.type == 'IMAGE': # revised if changed to yaf_tex_type
                try:
                    layout.template_ID(context.world, "active_texture")  # new="texture.new")
                except:
                    pass
                if  tex.type == 'IMAGE':  # it allows to change the used image
                    try:
                        layout.template_image(tex, "image", tex.image_user, compact = True)
                    except:
                        pass
            else:
                try:
                    layout.template_ID(context.world, "active_texture", new="texture.new")
                except:  # TODO: create only image texture? procedural not supported.. ?
                    pass
            layout.prop(world, "bg_rotation", text = "Rotation")

            split = layout.split(percentage = 0.33)

            col = split.column(align = True)
            col.prop(world, "bg_use_ibl", text = "Use IBL")
            col.label(text = " ")

        elif world.bg_type == 'Sunsky':
            self.ibl = False
            col.prop(world, "bg_turbidity", text = "Turbidity")
            col.prop(world, "bg_a_var", text = "HorBrght")
            col.prop(world, "bg_b_var", text = "HorSprd")
            col.prop(world, "bg_c_var", text = "SunBrght")
            col.prop(world, "bg_d_var", text = "SunSize")
            col.prop(world, "bg_e_var", text = "Backlight")
            col.operator("world.get_position", text = "Get Position")
            col.operator("world.get_angle", text = "Get Angle")
            col.operator("world.update_sun", text = "Update Sun")
            col.prop(world, "bg_from", text = "From")
            col.prop(world, "bg_add_sun", text = "Add Sun")
            if world.bg_add_sun:
                col.prop(world, "bg_sun_power", text = "Sun Power")

            col.prop(world, "bg_background_light", text = "Skylight")
            col.prop(world, "bg_light_samples", text = "Samples")
        ## DarkTide Sunsky NOT  more updated? ----->
        elif world.bg_type == 'Darktide\'s Sunsky':
            self.ibl = False
            col.prop(world, "bg_turbidity", text = "Turbidity")
            col.prop(world, "bg_a_var", text = "Brightness of horizon gradient")
            col.prop(world, "bg_b_var", text = "Luminance of horizon")
            col.prop(world, "bg_c_var", text = "Solar region intensity")
            col.prop(world, "bg_d_var", text = "Width of circumsolar region")
            col.prop(world, "bg_e_var", text = "Backscattered light")

            col.operator("world.get_position", text = "Get Position")
            col.operator("world.get_angle", text = "Get Angle")
            col.operator("world.update_sun", text = "Update Sun")

            col.prop(world, "bg_from", text = "From", icon='VIEW3D_VEC')
            col.prop(world, "bg_dsaltitude", text = "Altitude")
            col.prop(world, "bg_add_sun", text = "Add Sun")

            col.prop(world, "bg_sun_power", text = "Sun Power")
            col.prop(world, "bg_background_light", text = "Add Skylight")

            col.prop(world, "bg_dsnight", text = "Night")

            col.prop(world, "bg_dsbright", text = "Sky Brightness")
            col.prop(world, "bg_light_samples", text = "Samples")
            col.prop(world, "bg_exposure", text = "Exposure")
            col.prop(world, "bg_clamp_rgb", text = "Clamp RGB")
            col.prop(world, "bg_gamma_enc", text = "Gamma Encoding")

        elif world.bg_type == 'Single Color':

            split = layout.split(percentage = 0.33)

            col = split.column()
            col.label("Color:")
            col = split.column()
            col.prop(world, "bg_single_color", text = "")

            split = layout.split(percentage = 0.33)
            col = split.column(align = True)
            col.prop(world, "bg_use_ibl", text = "Use IBL")
            col.label(text = " ")

        if world.bg_use_ibl and self.ibl:  # for all options used IBL

            col = split.column(align = True)
            col.prop(world, "bg_ibl_samples", text = "IBL Samples")
            col.prop(world, "bg_power", text = "Power")

from yafaray.ui import properties_yaf_volume_integrator
