import bpy
from bpy.types import Panel
from bl_ui.properties_world import WorldButtonsPanel
WorldButtonsPanel.COMPAT_ENGINES = {'YAFA_RENDER'}
from bpy.props import (FloatProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty)

World = bpy.types.World

World.v_int_type = EnumProperty(
    name="Volume integrator",
    description="Set the volume integrator",
    items=(
        ('None', "None", ""),
        ('Single Scatter', "Single Scatter", "")
    ),
    default='None')

World.v_int_step_size = FloatProperty(
    name="Step size",
    description="Precision of volumetric rendering (in Blender units)",
    min=0.0, max=100.0,
    precision=3,
    default=1.000)

World.v_int_adaptive = BoolProperty(
    name="Adaptive",
    description="Optimizes stepping calculations for NoiseVolumes",
    default=False)

World.v_int_optimize = BoolProperty(
    name="Optimize",
    description="Precomputing attenuation in the entire volume at a 3d grid of points",
    default=False)

World.v_int_attgridres = IntProperty(
    name="Att. grid resolution",
    description="Optimization attenuation grid resolution",
    min=1, max=50,
    default=1)

# ??? not sure about the following properties ???
# World.v_int_scale = FloatProperty(attr = "v_int_scale")
# World.v_int_alpha =       FloatProperty(attr = "v_int_alpha")
# World.v_int_dsturbidity = FloatProperty(attr = "v_int_dsturbidity")


class YAF_PT_vol_integrator(WorldButtonsPanel, Panel):
    bl_label = "YafaRay Volume Integrator"

    def draw(self, context):

        layout = self.layout

        layout.prop(context.world, "v_int_type")
        layout.separator()

        if context.world.v_int_type == 'Single Scatter':
            layout.prop(context.world, "v_int_step_size")
            layout.prop(context.world, "v_int_adaptive")
            layout.prop(context.world, "v_int_optimize")
            if context.world.v_int_optimize:
                layout.prop(context.world, "v_int_attgridres")

del WorldButtonsPanel
