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

Lamp.lamp_type = EnumProperty(attr="type",
    items = (
        ("","Light Type",""),
        ("POINT","Point",""),
        ("SUN","Sun",""),
        #("Directional","Directional",""), # integrate into Sun
        #("MeshLight","MeshLight",""),
        #("Sphere","Sphere",""), # integrate in Pointlight
        ("SPOT","Spot",""),
        ("IES","IES",""),
        ("AREA","Area",""),
),default="POINT")
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

        layout.prop(context.lamp,"type", expand=True, text= "Light Type")

        split = layout.split(percentage = 0.65)
        row = layout.row()

        col = row.column() # row.column = org
        sub = col.column()

        #context.lamp.shadow_ray_samples = 16

        if context.lamp.type == 'AREA':

            col.prop(context.lamp,"yaf_samples", text= "Samples")
            col.prop(context.lamp,"size", text= "SizeX")
            col.prop(context.lamp,"size_y", text= "SizeY")
            col.prop(context.lamp,"create_geometry", text= "Create Geometry") # crash in render


        elif context.lamp.type == 'SPOT':

            col.prop(context.lamp,"spot_size", text= "Cone Angle")
            col.prop(context.lamp,"spot_soft_shadows", text= "Soft Shadow")

            if context.lamp.spot_soft_shadows:
                col.prop(context.lamp,"yaf_samples", text= "Samples")
                col.prop(context.lamp,"shadow_fuzzyness", text= "Shadow Fuzzyness")

            col.prop(context.lamp,"spot_blend", text= "Blend")
            col.prop(context.lamp,"distance", text= "Distance")
            #col = split.column()
            col.prop(context.lamp,"photon_only", text= "Photon Only")


        elif context.lamp.type == 'SUN':

            col.prop(context.lamp,"angle", text= "Angle")
            col.prop(context.lamp,"yaf_samples", text= "Samples")
            col.prop(context.lamp,"directional", text= "Directional")
            if context.lamp.directional:
                col.prop(context.lamp,"shadow_soft_size", text= "Radius")
                col.prop(context.lamp,"infinite", text= "Infinite")

        elif context.lamp.type == 'POINT':

            col.prop(context.lamp,"use_sphere",text= "Use sphere")
            if context.lamp.use_sphere:
                col.prop(context.lamp,"shadow_soft_size", text= "Radius")
                col.prop(context.lamp,"yaf_samples", text= "Samples")
                col.prop(context.lamp,"distance", text= "Distance")
                col.prop(context.lamp,"create_geometry", text= "Create Geometry")


        elif context.lamp.type == 'HEMI':

            col.label("YafaRay Light type IES")
            col.prop(context.lamp,"ies_file",text = "IES File")
            #col.prop(context.lamp,"spot_size",text = "IES Cone Angle")
            col.prop(context.lamp,"ies_soft_shadows",text = "IES Soft Shadows")
            if context.lamp.ies_soft_shadows:
                col.prop(context.lamp,"yaf_samples",text = "IES Samples")

        col.prop(context.lamp,"color", text= "Color")
        col.prop(context.lamp,"energy", text= "Power")



classes = [
    YAF_PT_lamp,
]

def register():

    register = bpy.types.register
    for cls in classes:
        register(cls)


def unregister():

    unregister = bpy.types.unregister
    for cls in classes:
        unregister(cls)


if __name__ == "__main__":
    register()

