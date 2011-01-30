import bpy

# import types and props ---->
from bpy.props import *
World = bpy.types.World
#TODO: Update default values, edit description


World.bg_type = EnumProperty(attr="bg_type",
    items = (
        ("Yafaray Background", "Yafaray Background", ""),
        ("Gradient", "Gradient", ""),
        ("Texture", "Texture", ""),
        ("Sunsky", "Sunsky", ""),
        ("Darktide's Sunsky", "Darktide's Sunsky", ""),
        ("Single Color", "Single Color", ""),
), default="Single Color")
World.bg_zenith_ground_color =  FloatVectorProperty(
                                            description = "Color Settings", subtype = "COLOR",
                                            min = 0.0, max = 1.0,
                                            default = (1, 1, 1), step = 1,
                                            precision = 2,
                                            soft_min = 0.0, soft_max = 1.0)
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
                                            min = 0, max = 360)
World.bg_turbidity =        FloatProperty(
                                            description = "",
                                            default = 2.0,
                                            min = 1.0, max = 20.0)
World.bg_a_var =            FloatProperty(
                                            description = "",
                                            default = 1.0,
                                            min = 0, max =10)
World.bg_b_var =            FloatProperty(
                                            default = 1.0,
                                            min = 0, max = 10)
World.bg_c_var =            FloatProperty(
                                            description = "",
                                            default = 1.0,
                                            min = 0, max =10)
World.bg_d_var =            FloatProperty(
                                            description = "",
                                            default = 1.0,
                                            min = 0, max = 10)
World.bg_e_var =            FloatProperty(
                                            description = "",
                                            default = 1.0,
                                            min = 0, max = 10)
World.bg_from =             FloatVectorProperty(
                                            description = "Point Info", subtype = "XYZ",
                                            default = (0.5, 0.5, 0.5),
                                            step = 10, precision = 3,
                                            min = -1, max = 1)
World.bg_add_sun =          BoolProperty()
World.bg_sun_power =        FloatProperty(
                                            description = "",
                                            default = 1.0,
                                            min = 0, max = 10)
World.bg_background_light = BoolProperty(
                                            description = "",
                                            default = False)
World.bg_light_samples =    IntProperty(
                                            description = "",
                                            default = 16,
                                            min = 1, max = 512)
World.bg_dsaltitude =       FloatProperty(
                                            description = "",
                                            default = 0.0,
                                            min = -1, max = 2)
World.bg_dsnight =          BoolProperty(
                                            description = "",
                                            default = False)
World.bg_dsbright =         FloatProperty(
                                            description = "",
                                            default = 1.0,
                                            min = 0, max = 10)
World.bg_power =            FloatProperty(
                                            description = "Multiplier for Background Color",
                                            default = 1.0,
                                            min = 0, max = 10)

World.bg_exposure =         FloatProperty(
                                            description = "",
                                            default = 1.0,
                                            min = 0, max = 10)
World.bg_clamp_rgb =        BoolProperty(
                                            description = "",
                                            default = False)
World.bg_gamma_enc =        BoolProperty(
                                            description = "",
                                            default = True)

#World.use_image = BoolProperty(attr="use_image", default = False)


class YAF_PT_world(bpy.types.Panel):

    bl_label = 'YafaRay Background'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'world'
    COMPAT_ENGINES =['YAFA_RENDER']

    @classmethod
    def poll(self, context):

        engine = context.scene.render.engine

        import properties_world


        import properties_texture

        if (context.world  and  (engine in self.COMPAT_ENGINES) ) :
            try :
                properties_world.unregister()
            except:
                pass
        else:
            try:
                properties_world.register()
            except:
                pass
        if (context.texture and  (engine in self.COMPAT_ENGINES) ) :
            try :
                properties_texture.unregister()
            except:
                pass
        else:
            try:
                properties_texture.register()
            except:
                pass
        return (context.texture  or context.world and  (engine in self.COMPAT_ENGINES) )


    def draw(self, context):

        layout = self.layout
        split = layout.split()
        col = split.column()

        col.prop(context.world, "bg_type", text= "Yafaray Background")

        if context.world.bg_type == 'Gradient':
            col.prop(context.world, "horizon_color", text= "Horizon Color")
            col.prop(context.world, "ambient_color", text= "Horizon Ground Color")
            col.prop(context.world, "zenith_color", text= "Zenith Color")
            col.prop(context.world, "bg_zenith_ground_color", text= "Zenith Ground Color")
            col.prop(context.world, "bg_use_ibl", text= "Use IBL")

        elif context.world.bg_type == 'Texture':
            col.prop(context.world, "bg_use_ibl", text= "Use IBL")
            col.prop(context.world, "bg_rotation", text= "Rotation")

            tex = context.scene.world.active_texture

            if tex is not None: # and tex.type == 'IMAGE': # revised if changed to yaf_tex_type
                try:
                    col.template_ID(context.world, "active_texture")#, new="texture.new")
                except:
                    pass
                if  tex.type == 'IMAGE': # it allows to change the used image
                    try:
                        col.template_image(tex, "image", tex.image_user, compact=True)
                    except:
                        pass
            else:
                try:
                    col.template_ID(context.world, "active_texture", new="texture.new")
                except: # TODO: create only image texture? procedural not supported.. ?
                    pass
#

            # more code ?, yes, is need

        elif context.world.bg_type == 'Sunsky':
            col.prop(context.world, "bg_turbidity", text= "Turbidity")
            col.prop(context.world, "bg_a_var", text= "HorBrght")
            col.prop(context.world, "bg_b_var", text= "HorSprd")
            col.prop(context.world, "bg_c_var", text= "SunBrght")
            col.prop(context.world, "bg_d_var", text= "SunSize")
            col.prop(context.world, "bg_e_var", text= "Backlight")
            col.operator("world.get_position", text = "Get Position")
            col.operator("world.get_angle", text = "Get Angle")
            col.operator("world.update_sun", text = "Update Sun")
            col.prop(context.world, "bg_from", text= "From")
            col.prop(context.world, "bg_add_sun", text= "Add Sun")
            if context.world.bg_add_sun :
                col.prop(context.world, "bg_sun_power", text= "Sun Power")

            col.prop(context.world, "bg_background_light", text= "Skylight")
            col.prop(context.world, "bg_light_samples", text= "Samples")
## DarkTide Sunsky NOT  more updated? ----->
        elif context.world.bg_type == 'Darktide\'s Sunsky':
            col.prop(context.world, "bg_turbidity", text= "Turbidity")
            col.prop(context.world, "bg_a_var", text= "Brightness of horizon gradient")
            col.prop(context.world, "bg_b_var", text= "Luminance of horizon")
            col.prop(context.world, "bg_c_var", text= "Solar region intensity")
            col.prop(context.world, "bg_d_var", text= "Width of circumsolar region")
            col.prop(context.world, "bg_e_var", text= "Backscattered light")

            col.operator("world.get_position", text = "Get Position")
            col.operator("world.get_angle", text = "Get Angle")
            col.operator("world.update_sun", text = "Update Sun")

            col.prop(context.world, "bg_from", text= "From")
            col.prop(context.world, "bg_dsaltitude", text= "Altitude")
            col.prop(context.world, "bg_add_sun", text= "Add Sun")

            col.prop(context.world, "bg_sun_power", text= "Sun Power")
            col.prop(context.world, "bg_background_light", text= "Add Skylight")

            col.prop(context.world, "bg_dsnight", text= "Night")

            col.prop(context.world, "bg_dsbright", text= "Sky Brightness")
            col.prop(context.world, "bg_light_samples", text= "Samples")
            col.prop(context.world, "bg_exposure", text= "Exposure")
            col.prop(context.world, "bg_clamp_rgb", text= "Clamp RGB")
            col.prop(context.world, "bg_gamma_enc", text= "Gamma Encoding")

        elif context.world.bg_type == 'Single Color':
            col.prop(context.world, "horizon_color", text= "Color")
            col.prop(context.world, "bg_use_ibl", text= "Use IBL")

        if context.world.bg_use_ibl: # for all options used IBL
            col.prop(context.world, "bg_ibl_samples", text= "IBL Samples")
            col.prop(context.world, "bg_power", text= "Power")

# re-use modules from Blender

import properties_world

properties_world.WORLD_PT_preview.COMPAT_ENGINES.add('YAFA_RENDER')
properties_world.WORLD_PT_context_world.COMPAT_ENGINES.add('YAFA_RENDER')

del properties_world

