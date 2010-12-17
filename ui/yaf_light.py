"""
This file is part of Yafaray Exporter
"""
import bpy
narrowui = 300

#import types and props ---->
from bpy.props import *
Lamp = bpy.types.Lamp

Lamp.lamp_type = EnumProperty(attr="lamp_type",
    items = (
        ("Light Type","Light Type",""),
        ("Area","Area",""),
        ("Directional","Directional",""),
        #("MeshLight","MeshLight",""),
        ("Point","Point",""),
        ("Sphere","Sphere",""),
        ("Spot","Spot",""),
        ("Sun","Sun",""),
        ("IES","IES",""),
),default="Sun")
Lamp.directional = BoolProperty(attr="directional",
                                    default = False)
Lamp.infinite = BoolProperty(attr="infinite",
                                    description = "Determines if light is infinite or filling a semi-infinite cylinder",
                                    default = True)
Lamp.directional_radius = FloatProperty(attr="directional_radius",
                                    description = "Radius of semi-infinit cylinder (only applies if infinite=false)",
                                    min = 0.0, max = 10000.0,
                                    default = 1.0)
Lamp.create_geometry = BoolProperty(attr="create_geometry",
                                    description = "Creates a visible geometry in the dimensions of the light during the render",
                                    default = False)
Lamp.spot_soft_shadows = BoolProperty(attr="spot_soft_shadows",
                                    description = "Use soft shadows",
                                    default = False)
Lamp.shadow_fuzzyness = FloatProperty(attr="shadow_fuzzyness",
                                    description = "Fuzzyness of the soft shadows (0 - hard shadow, 1 - fuzzy shadow)",
                                    min = 0.0, max = 1.0,
                                    default = 1.0)
Lamp.photon_only = BoolProperty(attr="photon_only",
                                    description = "This spot will only throw photons not direct light",
                                    default = False)
Lamp.angle = FloatProperty(attr="angle",
                                    description = "Angle of the cone in degrees (shadow softness)",
                                    min = 0.0, max = 80.0,
                                    default = 0.5)
Lamp.ies_file = StringProperty(attr="ies_file",subtype = 'FILE_PATH')
Lamp.yaf_samples = IntProperty(attr="yaf_samples",
                                    description = "Number of samples to be taken for direct lighting",
                                    min = 0, max = 512,
                                    default = 16)
Lamp.ies_cone_angle = FloatProperty(attr="ies_cone_angle", default = 10.0)
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

        import properties_data_lamp

        if (context.lamp and  (engine in self.COMPAT_ENGINES) ) :
            try :
                properties_data_lamp.unregister()
            except: 
                pass
        else:
            try:
                properties_data_lamp.register()
            except: 
                pass
        return (context.lamp and  (engine in self.COMPAT_ENGINES) ) 


    def draw(self, context):

        layout = self.layout
        split = layout.split()
        col = split.column()

        col.prop(context.lamp,"type", text= "Light Type")
        row = layout.row()
        split = row.split()
        col = split.column() # row.column = org

        #context.lamp.shadow_ray_samples = 16

        if context.lamp.type == 'AREA':

            col.prop(context.lamp,"yaf_samples", text= "Samples")
            if context.lamp.type != 'AREA':
                context.lamp.type = 'AREA'
            col.prop(context.lamp,"size", text= "SizeX")
            col.prop(context.lamp,"size_y", text= "SizeY")
            col.prop(context.lamp,"create_geometry", text= "Create Geometry")


#        elif context.lamp.type == 'Directional':
#            if context.lamp.type != 'SUN':
#                context.lamp.type = 'SUN'
#            row.prop(context.lamp,"shadow_soft_size", text= "Radius")
#            row.prop(context.lamp,"infinite", text= "Infinite")

#       elif context.lamp.type == 'Sphere':
#           if context.lamp.type != 'POINT':
#               context.lamp.type = 'POINT'
#           col.prop(context.lamp,"shadow_soft_size", text= "Radius")
#           col.prop(context.lamp,"yaf_samples", text= "Samples")
#           col.prop(context.lamp,"create_geometry", text= "Create Geometry")


        elif context.lamp.type == 'SPOT':

            if context.lamp.type != 'SPOT':
                context.lamp.type = 'SPOT'

            col.prop(context.lamp,"spot_size", text= "Cone Angle")
            col.prop(context.lamp,"spot_soft_shadows", text= "Soft Shadow")

            if context.lamp.spot_soft_shadows:
                col.prop(context.lamp,"yaf_samples", text= "Samples")
                col.prop(context.lamp,"shadow_fuzzyness", text= "Shadow Fuzzyness")
            col.prop(context.lamp,"spot_blend", text= "Blend")
            col.prop(context.lamp,"distance", text= "Distance")
            col.prop(context.lamp,"photon_only", text= "Photon Only")


        elif context.lamp.type == 'SUN':
            col.prop(context.lamp,"directional", text="directional")
            if context.lamp.directional:
                col.prop(context.lamp,"infinite", text= "Infinite")
                if not context.lamp.infinite:
                    col.prop(context.lamp,"directional_radius", text= "Radius")
            else:
                col.prop(context.lamp,"angle", text= "Angle")
                col.prop(context.lamp,"yaf_samples", text= "Samples")
            if context.lamp.type != 'SUN':
                context.lamp.type = 'SUN'


        elif context.lamp.type == 'POINT':
            col.prop(context.lamp, "use_sphere")
            if context.lamp.use_sphere:
                col.prop(context.lamp,"shadow_soft_size", text= "Radius")
                col.prop(context.lamp,"yaf_samples", text= "Samples")
                col.prop(context.lamp,"create_geometry", text= "Create Geometry")           
            if context.lamp.type != 'POINT':
                context.lamp.type = 'POINT'


        elif context.lamp.type == 'IES':
            col.prop(context.lamp,"ies_file",text = "IES File")
            if context.lamp.ies_soft_shadows:
                col.prop(context.lamp,"yaf_samples",text = "IES Samples")
            col.prop(context.lamp,"ies_cone_angle",text = "IES Cone Angle")
            col.prop(context.lamp,"ies_soft_shadows",text = "IES Soft Shadows")




        col.prop(context.lamp,"color", text= "Color")
        col.prop(context.lamp,"energy", text= "Power")


from properties_data_lamp import DATA_PT_preview
from properties_data_lamp import DATA_PT_context_lamp

classes = [
    YAF_PT_lamp,
]

def register():
    YAF_PT_lamp.prepend( DATA_PT_preview.draw )
    YAF_PT_lamp.prepend( DATA_PT_context_lamp.draw )
    register = bpy.types.register
    for cls in classes:
        register(cls)


def unregister():
    bpy.types.YAF_PT_lamp.remove( DATA_PT_preview.draw )
    bpy.types.YAF_PT_lamp.remove( DATA_PT_context_lamp.draw )
    unregister = bpy.types.unregister
    for cls in classes:
        unregister(cls)


if __name__ == "__main__":
    register()

