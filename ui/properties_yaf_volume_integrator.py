import bpy
#import types and props ---->
from bpy.props import *
World = bpy.types.World

World.v_int_type = EnumProperty(
    items = (
            ("None", "None", ""),
            ("Single Scatter", "Single Scatter", "")),
    default = "None",
    name = "Volume Integrator")
World.v_int_step_size =   FloatProperty(attr = "v_int_step_size", precision = 3)
World.v_int_adaptive =    BoolProperty(attr = "v_int_adaptive")
World.v_int_optimize =    BoolProperty(attr = "v_int_optimize")
World.v_int_attgridres =  IntProperty(attr = "v_int_attgridres")
World.v_int_scale =       FloatProperty(attr = "v_int_scale")
World.v_int_alpha =       FloatProperty(attr = "v_int_alpha")
World.v_int_dsturbidity = FloatProperty(attr = "v_int_dsturbidity")


class YAF_PT_vol_integrator(bpy.types.Panel):

    bl_label = 'YafaRay Volume Integrator'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'world'
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(cls, context):

        engine = context.scene.render.engine
        return (context.world and (engine in cls.COMPAT_ENGINES))

    def draw(self, context):

        layout = self.layout
        split = layout.split()
        col = split.column()
        col.prop(context.world, "v_int_type", text = "Volume Integrator")
        if context.world.v_int_type == 'Single Scatter':
            col.prop(context.world, "v_int_step_size", text = "Step Size")
            col.prop(context.world, "v_int_attgridres", text = "Att. grid resolution")
            row = layout.row()
            row.prop(context.world, "v_int_adaptive", text = "Adaptive")
            row.prop(context.world, "v_int_optimize", text = "Optimize")
