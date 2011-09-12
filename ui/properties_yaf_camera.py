import bpy
#import types and props ---->
from bpy.props import FloatProperty, EnumProperty, BoolProperty
from bpy.types import Panel
from bl_ui import properties_data_camera
Camera = bpy.types.Camera


def call_camera_update(self, context):
    camera = context.camera
    if camera is not None:
        if camera.camera_type == 'orthographic':
            camera.type = 'ORTHO'
        else:
            camera.type = 'PERSP'

Camera.camera_type = EnumProperty(
    name="Camera Type",
    items=(
        ('perspective', "Perspective", ""),
        ('architect', "Architect", ""),
        ('angular', "Angular", ""),
        ('orthographic', "Ortho", "")
    ),
    update=call_camera_update,
    default='perspective')

Camera.angular_angle = FloatProperty(
    name="Angle",
    min=0.0, max=180.0, precision=3,
    default=90.0)

Camera.max_angle = FloatProperty(
    name="Max Angle",
    min=0.0, max=180.0, precision=3,
    default=90.0)

Camera.mirrored = BoolProperty(
    name="Mirrored",
    default=False)

Camera.circular = BoolProperty(
    name="Circular",
    default=False)

Camera.use_clipping = BoolProperty(
    name="Use clipping",
    default=False)

Camera.bokeh_type = EnumProperty(
    name="Bokeh type",
    items=(
        ('disk1', "Disk1", ""),
        ('disk2', "Disk2", ""),
        ('triangle', "Triangle", ""),
        ('square', "Square", ""),
        ('pentagon', "Pentagon", ""),
        ('hexagon', "Hexagon", ""),
        ('ring', "Ring", "")
    ),
    default='disk1')

Camera.aperture = FloatProperty(
    name="Aperture",
    min=0.0, max=20.0, precision=5,
    default=0.0)

Camera.bokeh_rotation = FloatProperty(
    name="Bokeh rotation",
    min=0.0, max=180, precision=3,
    default=0.0)

Camera.bokeh_bias = EnumProperty(
    name="Bokeh bias",
    items=(
        ('uniform', "Uniform", ""),
        ('center', "Center", ""),
        ('edge', "Edge", "")
    ),
    default='uniform')


class YAF_PT_camera(Panel):
    bl_label = "Camera"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.camera and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        camera = context.camera

        layout.prop(camera, 'camera_type', expand=True)

        layout.separator()

        if camera.camera_type == 'angular':
            layout.prop(camera, 'angular_angle')
            layout.prop(camera, 'max_angle')
            layout.prop(camera, 'mirrored')
            layout.prop(camera, 'circular')

        elif camera.camera_type == 'orthographic':
            layout.prop(camera, 'ortho_scale')

        elif camera.camera_type in {'perspective', 'architect'}:
            layout.prop(camera, 'lens')

            layout.separator()

            layout.label("Depth of Field:")
            layout.prop(camera, 'aperture')
            split = layout.split()
            split.prop(camera, 'dof_object', text="")
            col = split.column()
            if camera.dof_object is not None:
                col.enabled = False
            col.prop(camera, 'dof_distance', text="Distance")

            layout.prop(camera, 'bokeh_type')
            layout.prop(camera, 'bokeh_bias')
            layout.prop(camera, 'bokeh_rotation')


class YAF_PT_camera_display(Panel):
    bl_label = "Display"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.camera and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        camera = context.camera

        split = layout.split()

        col = split.column()
        col.prop(camera, 'show_limits')
        col.prop(camera, 'show_title_safe')
        col.prop(camera, 'show_name')

        col = split.column()
        col.prop(camera, 'draw_size', text="Size")
        col.prop(camera, 'show_passepartout', text="Passepartout")
        sub = col.column()
        sub.active = camera.show_passepartout
        sub.prop(camera, 'passepartout_alpha', text="Alpha", slider=True)

        layout.separator()
        layout.prop(camera, 'use_clipping')

        split = layout.split()
        col = split.column(align=True)
        clip = col.column()
        clip.active = camera.use_clipping
        clip.prop(camera, 'clip_start', text="Start")
        clip.prop(camera, 'clip_end', text="End")

        col = split.column()
        col.prop_menu_enum(camera, 'show_guide')
