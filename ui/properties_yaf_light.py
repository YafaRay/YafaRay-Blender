import bpy
#import types and props ---->
from bpy.props import *
Lamp = bpy.types.Lamp
# TODO: check params in yafaray source and ../yaf_light.py, improve UI Layout


def call_lighttype_update(self, context):
        lamp = context.scene.objects.active
        if lamp.type == 'LAMP':
            switchLampType = {'area': 'AREA', 'spot': 'SPOT', 'sun': 'SUN', 'point': 'POINT', 'ies': 'SPOT'}
            lamp.data.type = switchLampType.get(lamp.data.lamp_type)

Lamp.lamp_type =            EnumProperty(
                                items = (
                                    ("point", "Point", ""),
                                    ("sun", "Sun", ""),
                                    ("spot", "Spot", ""),
                                    ("ies", "IES", ""),
                                    ("area", "Area", "")),
                                default="point",
                                name = "Light Type", update = call_lighttype_update)

Lamp.directional =          BoolProperty(
                                description = "",
                                default = False)


Lamp.create_geometry =      BoolProperty(
                                description = "Creates a visible geometry in the dimensions of the light during the render",
                                default = False)

Lamp.infinite =             BoolProperty(
                                description = "Determines if light is infinite or filling a semi-infinite cylinder",
                                default = True)

Lamp.size =                 FloatProperty(attr = "size",  # size = size value in Blender -> do we need this prop? TODO: check
                                description = "",
                                default = 2)

Lamp.size_y =               FloatProperty(attr = "size_y",  # do we need this prop, TODO: check
                                description = "",
                                default = 2)

Lamp.spot_blend =           FloatProperty(attr = "spot_blend",  # do we need this prop? TODO: check
                                description = "")

Lamp.spot_size =            FloatProperty(attr = "spot_size",  # do we need this prop? TODO: check
                                description = "",
                                default = 45)

Lamp.use_sphere =           BoolProperty(  # do we need this prop? TODO: check
                                description = "",
                                default = False)

Lamp.spot_soft_shadows =    BoolProperty(
                                description = "Use soft shadows",
                                default = False)

Lamp.shadow_fuzzyness =     FloatProperty(
                                description = "Fuzzyness of the soft shadows (0 - hard shadow, 1 - fuzzy shadow)",
                                min = 0.0, max = 1.0,
                                default = 1.0)

Lamp.photon_only =          BoolProperty(
                                description = "This spot will only throw photons not direct light",
                                default = False)

Lamp.angle =                FloatProperty(
                                description = "Angle of the cone in degrees (shadow softness)",
                                min = 0.0, max = 80.0,
                                default = 0.5)

Lamp.ies_file =             StringProperty(attr = "ies_file", subtype = 'FILE_PATH')

Lamp.yaf_samples =          IntProperty(
                                description = "Number of samples to be taken for direct lighting",
                                min = 0, max = 512,
                                default = 16)

Lamp.ies_cone_angle =       FloatProperty(attr = "spot_size", default = 45)
Lamp.ies_soft_shadows =     BoolProperty(attr = "ies_soft_shadows")


class YAF_PT_lamp(bpy.types.Panel):

    bl_label = 'Lamp'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'

    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(cls, context):

        engine = context.scene.render.engine
        return (context.lamp and  (engine in cls.COMPAT_ENGINES))

    def draw(self, context):
        layout = self.layout

        ob = context.object
        lamp = context.lamp
        space = context.space_data

        layout.template_preview(context.lamp)
        layout.prop(lamp, "lamp_type", expand = True, text = "Light Type")

        row = layout.row()
        col = row.column()

        if lamp.lamp_type == 'area':
            col.prop(lamp, "yaf_samples", text = "Samples")
            col.prop(lamp, "create_geometry", text= "Create Geometry")

        elif lamp.lamp_type == 'spot':
            col.prop(lamp, "spot_size", text = "Cone Angle")
            col.prop(lamp, "spot_blend", text = "Cone Edge Softness")
            col.prop(lamp, "spot_soft_shadows", text= "Soft Shadow", toggle = True)

            if lamp.spot_soft_shadows:
                box = col.box()
                box.prop(lamp, "yaf_samples", text = "Samples")
                box.prop(lamp, "shadow_fuzzyness", text= "Shadow Fuzzyness")

            col.prop(lamp, "photon_only", text= "Photon Only")

        elif lamp.lamp_type == 'sun':
            col.prop(lamp, "angle", text = "Angle")
            col.prop(lamp, "yaf_samples", text= "Samples")
            col.prop(lamp, "directional", text= "Directional", toggle = True)
            if lamp.directional:
                box = col.box()
                box.prop(lamp, "shadow_soft_size", text = "Radius")
                box.prop(lamp, "infinite", text= "Infinite")

        elif lamp.lamp_type == 'point':
            col.prop(lamp, "use_sphere", text = "Use sphere", toggle = True)
            if lamp.use_sphere:
                box = col.box()
                box.prop(lamp, "shadow_soft_size", text= "Radius")
                box.prop(lamp, "yaf_samples", text = "Samples")
                box.prop(lamp, "create_geometry", text = "Create Geometry")

        elif lamp.lamp_type == 'ies':
            col.label("YafaRay Light type IES")
            col.prop(lamp, "ies_file", text = "IES File")
            col.prop(lamp, "ies_soft_shadows", text = "IES Soft Shadows", toggle = True)
            if lamp.ies_soft_shadows:
                box = col.box()
                box.prop(lamp, "yaf_samples", text = "IES Samples")

        col.prop(lamp, "color", text= "Color")
        col.prop(lamp, "energy", text= "Power")
