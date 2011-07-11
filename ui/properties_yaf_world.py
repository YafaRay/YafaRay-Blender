import bpy
# import types and props ---->
from bpy.props import *
World = bpy.types.World
# TODO: check in converter for prop conversion of darktides sunsky values, improve UI Layout of sunsky


def call_world_update(self, context):
    world = context.scene.world
    world.ambient_color = world.ambient_color

World.bg_type =                 EnumProperty(
                                    items = (
                                        ('Gradient', 'Gradient', 'Gradient background'),
                                        ('Texture', 'Texture', 'Textured background'),
                                        ('Sunsky', 'Sunsky', 'Sunsky background'),
                                        ('Darktide\'s Sunsky', 'Darktide\'s sunsky', 'New model of sunsky background'),
                                        ('Single Color', 'Single Color', 'Single color background')
                                    ),
                                    default = 'Single Color',
                                    name = 'Background Type', update = call_world_update)

World.bg_color_space =          EnumProperty(
                                    items = (
                                        ('CIE (E)', 'CIE (E)', 'Select color space model'),
                                        ('CIE (D50)', 'CIE (D50)', 'Select color space model'),
                                        ('sRGB (D65)', 'sRGB (D65)', 'Select color space model'),
                                        ('sRGB (D50)', 'sRGB (D50)', 'Select color space model')
                                    ),
                                    default = 'CIE (E)',
                                    name = 'Color space', update = call_world_update)

World.bg_zenith_color =         FloatVectorProperty(
                                    description = 'Zenith color',
                                    subtype = 'COLOR',
                                    min = 0.0, max = 1.0,
                                    default = (0.57, 0.65, 1.0), update = call_world_update)
World.bg_horizon_color =        FloatVectorProperty(
                                    description = 'Horizon color',
                                    subtype = 'COLOR',
                                    min = 0.0, max = 1.0,
                                    default = (1, 1, 0.5), update = call_world_update)

World.bg_zenith_ground_color =  FloatVectorProperty(
                                    description = 'Zenith ground color',
                                    subtype = 'COLOR',
                                    min = 0.0, max = 1.0,
                                    default = (1, 0.9, 0.8), update = call_world_update)

World.bg_horizon_ground_color = FloatVectorProperty(
                                    description = 'Horizon ground color',
                                    subtype = 'COLOR',
                                    min = 0.0, max = 1.0,
                                    default = (0.8, 0.6, 0.3), update = call_world_update)

World.bg_single_color =         FloatVectorProperty(
                                    description = 'Background color',
                                    subtype = 'COLOR',
                                    min = 0.0, max = 1.0,
                                    default = (0.7, 0.7, 0.7), update = call_world_update)

World.bg_use_ibl =              BoolProperty(
                                    description = 'Use the background as the light source for your image',
                                    default = False)

World.bg_with_caustic =         BoolProperty(
                                    description = 'Allow background light to shoot caustic photons',
                                    default = True)

World.bg_with_diffuse =         BoolProperty(
                                    description = 'Allow background light to shoot diffuse photons',
                                    default = True)

World.bg_ibl_samples =          IntProperty(
                                    description = 'Number of samples for direct lighting from background',
                                    default = 16,
                                    min = 1, max = 512)

World.bg_rotation =             FloatProperty(
                                    description = 'Rotation offset of background texture',
                                    default = 0.0,
                                    min = 0, max = 360, update = call_world_update)

World.bg_turbidity =            FloatProperty(
                                    description = 'Turbidity of the atmosphere',
                                    default = 2.0,
                                    min = 1.0, max = 20.0, update = call_world_update)

World.ds_bg_turbidity =         FloatProperty(  # Darktide turbidity is different
                                    description = 'Turbidity of the atmosphere',
                                    default = 2.0,
                                    min = 2.0, max = 12.0, update = call_world_update)

World.bg_a_var =                FloatProperty(
                                    description = 'Darkening or brightening towards horizon',
                                    default = 1.0,
                                    min = 0, max =10, update = call_world_update)

World.bg_b_var =                FloatProperty(
                                    description = 'Luminance gradient near the horizon',
                                    default = 1.0,
                                    min = 0, max = 10, update = call_world_update)

World.bg_c_var =                FloatProperty(
                                    description = 'Relative intensity of circumsolar region',
                                    default = 1.0,
                                    min = 0, max =10, update = call_world_update)

World.bg_d_var =                FloatProperty(
                                    description = 'Width of circumsolar region',
                                    default = 1.0,
                                    min = 0, max = 10, update = call_world_update)

World.bg_e_var =                FloatProperty(
                                    description = 'Relative backscattered light',
                                    default = 1.0,
                                    min = 0, max = 10, update = call_world_update)

World.bg_from =                 FloatVectorProperty(
                                    description = 'Set position of the sun',
                                    default = (0.5, 0.5, 0.5), subtype = 'DIRECTION',
                                    step = 10, precision = 3,
                                    min = -1, max = 1, update = call_world_update)

World.bg_add_sun =              BoolProperty(
                                    description = 'Add a real sun light',
                                    default = False, update = call_world_update)

World.bg_sun_power =            FloatProperty(
                                    description = 'Sun power',
                                    default = 1.0,
                                    min = 0, max = 10, update = call_world_update)

World.bg_background_light =     BoolProperty(
                                    description = 'Add skylight',
                                    default = False, update = call_world_update)

World.bg_light_samples =        IntProperty(
                                    description = 'Set skylight and sunlight samples',
                                    default = 16,
                                    min = 1, max = 512, update = call_world_update)

World.bg_dsaltitude =           FloatProperty(
                                    description = 'Moves the sky dome above or below the camera position',
                                    default = 0.0,
                                    min = -1, max = 2, update = call_world_update)

World.bg_dsnight =              BoolProperty(
                                    description = 'Activate experimental night mode',
                                    default = False, update = call_world_update)

World.bg_dsbright =             FloatProperty(
                                    description = 'Brightness of the sky',
                                    default = 1.0,
                                    min = 0, max = 10, update = call_world_update)

World.bg_power =                FloatProperty(
                                    description = 'Multiplier for background color',
                                    default = 1.0,
                                    min = 0, max = 10, update = call_world_update)

World.bg_exposure =             FloatProperty(
                                    description = 'Exposure correction for the sky (0 = no correction)',
                                    default = 1.0,
                                    min = 0, max = 10, update = call_world_update)

World.bg_clamp_rgb =            BoolProperty(
                                    description = 'Clamp RGB values',
                                    default = False, update = call_world_update)

World.bg_gamma_enc =            BoolProperty(
                                    description = 'Apply gamma encoding to the sky',
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
    def poll(cls, context):
        rd = context.scene.render
        return context.world and (rd.engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout
        world = context.world

        split = layout.split()
        col = layout.column()
        col.prop(world, 'bg_type', text = 'Background')

        if world.bg_type == 'Gradient':

            split = layout.split(percentage = 0.40)
            col = split.column()
            col.label(text = 'Zenith Color:')
            col.label(text = 'Horizon Color:')
            col.label(text = 'Horizon Ground Color:')
            col.label(text = 'Zenith Ground Color:')

            col = split.column()
            col.prop(world, 'bg_zenith_color', text = '')
            col.prop(world, 'bg_horizon_color', text = '')
            col.prop(world, 'bg_horizon_ground_color', text = '')
            col.prop(world, 'bg_zenith_ground_color', text = '')

            split = layout.split(percentage = 0.40)
            col = split.column()
            col.prop(world, 'bg_use_ibl', text = 'Use IBL')
            col.label(text = ' ')

        elif world.bg_type == 'Texture':

            tex = context.scene.world.active_texture

            if tex is not None:  # and tex.type == 'IMAGE': # revised if changed to yaf_tex_type
                try:
                    layout.template_ID(context.world, 'active_texture')  # new='texture.new')
                except:
                    pass
                if  tex.type == 'IMAGE':  # it allows to change the used image
                    try:
                        layout.template_image(tex, 'image', tex.image_user, compact = True)
                    except:
                        pass
            else:
                try:
                    layout.template_ID(context.world, 'active_texture', new='texture.new')
                except:  # TODO: create only image texture? procedural not supported.. ?
                    pass
            layout.prop(world, 'bg_rotation', text = 'Rotation')

            split = layout.split(percentage = 0.33)

            col = split.column()
            col.prop(world, 'bg_use_ibl', text = 'Use IBL')
            if world.bg_use_ibl:
                row = layout.row()
                row.prop(world, 'bg_with_diffuse', text = 'Diffuse photons')
                row.prop(world, 'bg_with_caustic', text = 'Caustic photons')
            else:
                col = layout.column()
                col.label(text = ' ')
                col.label(text = ' ')

        elif world.bg_type == 'Sunsky':
            self.ibl = False
            col.prop(world, 'bg_turbidity', text = 'Turbidity')
            col.prop(world, 'bg_a_var', text = 'HorBrght')
            col.prop(world, 'bg_b_var', text = 'HorSprd')
            col.prop(world, 'bg_c_var', text = 'SunBrght')
            col.prop(world, 'bg_d_var', text = 'SunSize')
            col.prop(world, 'bg_e_var', text = 'Backlight')
            col.operator('world.get_position', text = 'Get Position')
            col.operator('world.get_angle', text = 'Get Angle')
            col.operator('world.update_sun', text = 'Update Sun')
            col.prop(world, 'bg_from', text = 'From')
            col.prop(world, 'bg_add_sun', text = 'Add Sun')
            if world.bg_add_sun:
                col.prop(world, 'bg_sun_power', text = 'Sun Power')
            col.prop(world, 'bg_background_light', text = 'Skylight')
            if world.bg_background_light:
                col.prop(world, 'bg_power', text = 'Skylight Power')
            col.prop(world, 'bg_light_samples', text = 'Samples')
        ## DarkTide Sunsky NOT  more updated? ----->
        elif world.bg_type == 'Darktide\'s Sunsky':
            self.ibl = False
            layout.separator()
            col = layout.column()
            sub = col.column(align = True)
            sub.prop(world, 'ds_bg_turbidity', text = 'Turbidity')
            sub.prop(world, 'bg_a_var', text = 'Brightness of horizon gradient')
            sub.prop(world, 'bg_b_var', text = 'Luminance of horizon')
            sub.prop(world, 'bg_c_var', text = 'Solar region intensity')
            sub.prop(world, 'bg_d_var', text = 'Width of circumsolar region')
            sub.prop(world, 'bg_e_var', text = 'Backscattered light')

            split = layout.split()
            col = split.column()
            col.label(text = 'Set sun position:')
            col.prop(world, 'bg_from', text = '')
            col.prop(world, 'bg_dsnight', text = 'Night')

            col = split.column()
            col.label(text = ' ')
            sub = col.column(align = True)
            sub.operator('world.get_position', text = 'Get Position')
            sub.operator('world.get_angle', text = 'Get Angle')
            sub.operator('world.update_sun', text = 'Update Sun')
            col.prop(world, 'bg_dsaltitude', text = 'Altitude')

            layout.separator()

            split = layout.split()
            col = split.column()
            col.prop(world, 'bg_add_sun', text = 'Add Sun')
            if world.bg_add_sun:
                col.prop(world, 'bg_sun_power', text = 'Sunlight Power')
            else:
                col.label(text = ' ')
            if world.bg_background_light:
                col.prop(world, 'bg_with_diffuse', text = 'Diffuse photons')
            else:
                col.label(text = ' ')

            col = split.column()
            col.prop(world, 'bg_background_light', text = 'Add Skylight')
            if world.bg_background_light:
                col.prop(world, 'bg_power', text = 'Skylight Power')
            else:
                col.label(text = ' ')
            if world.bg_background_light:
                col.prop(world, 'bg_with_caustic', text = 'Caustic photons')
            else:
                col.label(text = ' ')

            split = layout.split()
            col = split.column()
            col.prop(world, 'bg_exposure', text = 'Exposure')
            col = split.column()
            col.prop(world, 'bg_dsbright', text = 'Sky Brightness')

            layout.column().prop(world, 'bg_light_samples', text = 'Samples')

            split = layout.split()
            col = split.column()
            col.prop(world, 'bg_clamp_rgb', text = 'Clamp RGB')
            col = split.column()
            col.prop(world, 'bg_gamma_enc', text = 'Gamma Encoding')

            layout.column().prop(world, 'bg_color_space', text = 'Color space')

        elif world.bg_type == 'Single Color':

            split = layout.split(percentage = 0.33)

            col = split.column()
            col.label('Color:')
            col = split.column()
            col.prop(world, 'bg_single_color', text = '')

            split = layout.split(percentage = 0.33)
            col = split.column()
            col.prop(world, 'bg_use_ibl', text = 'Use IBL')
            col.label(text = ' ')

        if world.bg_use_ibl and self.ibl:  # for all options used IBL

            col = split.column()
            col.prop(world, 'bg_ibl_samples', text = 'IBL Samples')
            col.prop(world, 'bg_power', text = 'Power')

from . import properties_yaf_volume_integrator
