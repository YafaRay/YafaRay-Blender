"""
This file is part of Yafaray Exporter
"""
import bpy
narrowui = 300

#import types and props ---->
from bpy.props import *
Lamp = bpy.types.Lamp

from rna_prop_ui import PropertyPanel


# only create proprerty if not exist in Blender
# if exist, but not apropiate parameter for Yafaray

Lamp.lamp_type = EnumProperty(
    items = (
        ("", "Light Type", ""),
        ("point", "Point", ""),
        ("sun", "Sun", ""),
        ("spot", "Spot", ""),
        ("ies", "IES", ""),
        ("area", "Area", "")),
    default="point")
Lamp.directional =      BoolProperty(attr="directional",
                                    description = "",
                                    default = False)
Lamp.size =             FloatProperty(attr="size", # size = size value in Blender
                                    description = "",
                                    default = 2)
Lamp.size_y =           FloatProperty(attr="size_y",
                                    description = "",
                                    default = 2)
Lamp.spot_blend =       FloatProperty(attr="spot_blend",
                                    description = "")
Lamp.spot_size =        FloatProperty(attr="spot_size",
                                    description = "",
                                    default = 45)
Lamp.use_sphere =       BoolProperty(attr="use_sphere",
                                    description = "",
                                    default = False)
Lamp.create_geometry =  BoolProperty(attr="create_geometry",
                                    description = "Creates a visible geometry in the dimensions of the light during the render",
                                    default = False)
Lamp.infinite =         BoolProperty(attr="infinite",
                                    description = "Determines if light is infinite or filling a semi-infinite cylinder",
                                    default = True)
#Lamp.shadow_soft_size = FloatProperty(attr="shadow_soft_size",
#                                    description = "",
#                                    min = 1.0, max = 100,
#                                    default = 1.0)
Lamp.spot_soft_shadows = BoolProperty(attr="spot_soft_shadows",
                                    description = "Use soft shadows",
                                    default = False)
Lamp.shadow_fuzzyness = FloatProperty(attr="shadow_fuzzyness",
                                    description = "Fuzzyness of the soft shadows (0 - hard shadow, 1 - fuzzy shadow)",
                                    min = 0.0, max = 1.0,
                                    default = 1.0)
Lamp.photon_only =      BoolProperty(attr="photon_only",
                                    description = "This spot will only throw photons not direct light",
                                    default = False)
Lamp.angle =            FloatProperty(attr="angle",
                                    description = "Angle of the cone in degrees (shadow softness)",
                                    min = 0.0, max = 80.0,
                                    default = 0.5)
Lamp.ies_file =         StringProperty(attr="ies_file",subtype = 'FILE_PATH')
Lamp.yaf_samples =      IntProperty(attr="yaf_samples",
                                    description = "Number of samples to be taken for direct lighting",
                                    min = 0, max = 512,
                                    default = 16)
Lamp.ies_cone_angle =   FloatProperty(attr="spot_size", default = 45)
Lamp.ies_soft_shadows = BoolProperty(attr="ies_soft_shadows")

class YAF_PT_lamp(bpy.types.Panel):

    bl_label = 'Lamp'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'

    COMPAT_ENGINES =['YAFA_RENDER']


    @classmethod
    def poll(self, context):

        engine = context.scene.render.engine
        """
        import properties_data_lamp

        if (context.lamp and  (engine in self.COMPAT_ENGINES) ) :
            try :
                properties_data_lamp.unregister() # not blender properties, use Yafaray properties
            except:
                pass
        else:
            try:
                properties_data_lamp.register() # use Blender properties
            except:
                pass
        """
        return (context.lamp and  (engine in self.COMPAT_ENGINES))


    def draw(self, context):
        layout = self.layout
        # test insert context.lamp here, for no import module
        ob = context.object
        lamp = context.lamp
        space = context.space_data
        lamp_type = context.lamp.type

        split = layout.split(percentage=0.65)

        texture_count = len(lamp.texture_slots.keys())

        if ob:
            split.template_ID(ob, "data")
        elif lamp:
            split.template_ID(space, "pin_id")

        if texture_count != 0:
            split.label(text=str(texture_count), icon='TEXTURE')
        # end insert

        # draw preview? easy...
        layout.template_preview(context.lamp)

        layout.prop(lamp, "lamp_type", expand=True, text= "Light Type")
        # layout.prop(context.lamp, "type", expand=True, text= "Light Type")

        split = layout.split(percentage = 0.65)
        row = layout.row()

        col = row.column()
        sub = col.column()

        if lamp.lamp_type == 'area':
            if not lamp.type == "AREA":
                bpy.ops.wm.context_set_enum("EXEC_DEFAULT", data_path="lamp.type", value="AREA")

            col.prop(lamp, "yaf_samples", text= "Samples")
            # col.prop(lamp, "size", text= "SizeX")
            # col.prop(lamp, "size_y", text= "SizeY")
            col.prop(lamp, "create_geometry", text= "Create Geometry")

        elif lamp.lamp_type == 'spot':
            if not lamp.type == "SPOT":
                bpy.ops.wm.context_set_enum("EXEC_DEFAULT", data_path="lamp.type", value="SPOT")

            col.prop(lamp, "spot_size", text= "Cone Angle")
            col.prop(lamp, "spot_blend", text= "Cone Edge Softness")

            col.prop(lamp, "spot_soft_shadows", text= "Soft Shadow", toggle = True)

            if lamp.spot_soft_shadows:
                box = col.box()
                box.prop(lamp, "yaf_samples", text= "Samples")
                box.prop(lamp, "shadow_fuzzyness", text= "Shadow Fuzzyness")

            col.prop(lamp, "photon_only", text= "Photon Only")

        elif lamp.lamp_type == 'sun':
            if not lamp.type == "SUN":
                bpy.ops.wm.context_set_enum("EXEC_DEFAULT", data_path="lamp.type", value="SUN")

            col.prop(lamp, "angle", text= "Angle")
            col.prop(lamp, "yaf_samples", text= "Samples")
            col.prop(lamp, "directional", text= "Directional", toggle = True)
            if lamp.directional:
                box = col.box()
                box.prop(lamp, "shadow_soft_size", text= "Radius")
                box.prop(lamp, "infinite", text= "Infinite")

        elif lamp.lamp_type == 'point':
            if not lamp.type == "POINT":
                bpy.ops.wm.context_set_enum("EXEC_DEFAULT", data_path="lamp.type", value="POINT")

            col.prop(lamp, "use_sphere",text= "Use sphere", toggle = True)
            if lamp.use_sphere:
                box = col.box()
                box.prop(lamp, "shadow_soft_size", text= "Radius")
                box.prop(lamp, "yaf_samples", text= "Samples")
                box.prop(lamp, "create_geometry", text= "Create Geometry")

        elif lamp.lamp_type == 'ies':
            if not lamp.type == "SPOT":
                bpy.ops.wm.context_set_enum("EXEC_DEFAULT", data_path="lamp.type", value="SPOT")

            col.label("YafaRay Light type IES")
            col.prop(lamp, "ies_file",text = "IES File")
            col.prop(lamp, "ies_soft_shadows",text = "IES Soft Shadows", toggle = True)
            if lamp.ies_soft_shadows:
                box = col.box()
                box.prop(lamp, "yaf_samples",text = "IES Samples")

        col.prop(lamp, "color", text= "Color")
        col.prop(lamp, "energy", text= "Power")

