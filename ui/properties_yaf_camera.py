import bpy

#import types and props ---->
from bpy.props import *


bpy.types.Scene.useViewToRender = BoolProperty(attr = "useViewToRender")

Camera = bpy.types.Camera

Camera.camera_type = EnumProperty(attr = "camera_type",
    items = (
        ("Yafaray Camera", "Yafaray Camera", ""),
        ("angular", "Angular", ""),
        ("orthographic", "Orthographic", ""),
        ("perspective", "Perspective", ""),
        ("architect", "Architect", "")),
    default = "perspective")
Camera.angular_angle =      FloatProperty(attr = "angular_angle", max = 360.0)
Camera.max_angle     =      FloatProperty(attr = "max_angle", max = 360.0)
Camera.mirrored      =      BoolProperty(attr = "mirrored")
Camera.circular      =      BoolProperty(attr = "circular")
Camera.bokeh_type    =      EnumProperty(attr = "bokeh_type",
    items = (
        ("Bokeh Type", "Bokeh Type", ""),
        ("disk1", "Disk1", ""),
        ("disk2", "Disk2", ""),
        ("triangle", "Triangle", ""),
        ("square", "Square", ""),
        ("pentagon", "Pentagon", ""),
        ("hexagon", "Hexagon", ""),
        ("ring", "Ring", "")
    ),
    default="disk1")
Camera.aperture =       FloatProperty(attr = "aperture", min = 0.0, max = 1.0)
Camera.bokeh_rotation = FloatProperty(attr = "bokeh_rotation")
Camera.bokeh_bias =     EnumProperty(attr = "bokeh_bias",
    items = (
        ("Bokeh Bias", "Bokeh Bias", ""),
        ("uniform", "Uniform", ""),
        ("center", "Center", ""),
        ("edge", "Edge", "")),
    default = "uniform")
Camera.color_data =     FloatVectorProperty(attr = "color_data",
                                        description = "Point Info",
                                        subtype = "XYZ",
                                        step = 10,
                                        precision = 3)


class UpdateCameraTypeOperator(bpy.types.Operator):
    bl_idname = "yafaray.cameratypeop"
    bl_label = ""

    def execute(self, context):
        if context.camera.camera_type == 'orthographic':
            context.camera.type = 'ORTHO'
        else:
            context.camera.type = 'PERSP'
        return {'FINISHED'}

class RenderFromView(bpy.types.Operator):
    bl_idname = "yafaray.render_from_view"
    bl_label = ""

    def execute(self, context):
        context.scene.useViewToRender = True
        #bpy.ops.render.view_show()
        context.scene.gs_type_render = "into_blender"
        bpy.ops.render.render()
        context.scene.useViewToRender = False
        return {'FINISHED'}


class YAF_PT_camera(bpy.types.Panel):

    bl_label = 'Camera'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(self, context):

        engine = context.scene.render.engine

        import properties_data_camera

        if (context.camera and (engine in self.COMPAT_ENGINES)):
            try:
                properties_data_camera.unregister()
            except:
                pass
        else:
            try:
                properties_data_camera.register()
            except:
                pass
        return (context.camera and (engine in self.COMPAT_ENGINES))


    def draw(self, context):

        layout = self.layout
        split = layout.split()
        col = split.column()

        camera = context.camera


        #col.prop(bpy.data,"cameras",text = "Available cameras")
        col.prop(context.camera, "camera_type", text = "Yafaray Camera")
        col.operator("yafaray.cameratypeop", text = "Update 3D View Camera")
        col.operator("yafaray.render_from_view", text = "Render From View")
        col.separator()

        if context.camera.camera_type == 'angular':
            col.prop(context.camera, "angular_angle", text = "Angle")
            col.prop(context.camera, "max_angle", text = "Max Angle")
            col.prop(context.camera, "mirrored", text = "Mirrored")
            col.prop(context.camera, "circular", text = "Circular")

        elif camera.camera_type == 'orthographic':
            col.prop(context.camera, "ortho_scale", text = "Scale")

        elif camera.camera_type in ['perspective', 'architect']:
            col.prop(context.camera, "lens", text = "Focal Length")

            col.label("Depth of Field")
            col.prop(context.camera, "aperture", text = "Aperture")
            col.prop(context.camera, "dof_object", text = "DOF object")
            if camera.dof_object == None:
                col.prop(context.camera, "dof_distance", text = "DOF distance")

            col.prop(context.camera, "bokeh_type", text = "Bokeh Type")
            col.prop(context.camera, "bokeh_bias", text = "Bokeh Bias")
            col.prop(context.camera, "bokeh_rotation", text = "Bokeh Rotation")


        # col.prop(context.camera, "color_data", text = "Yafaray Camera Point")


#properties_data_camera.DATA_PT_context_camera.(COMPAT_ENGINES).add

classes = [
    YAF_PT_camera,
]

def register():
    #YAF_PT_camera.prepend( DATA_PT_context_camera.draw )
    register = bpy.types.register
    for cls in classes:
        register(cls)


def unregister():
    #bpy.types.YAF_PT_camera.remove( DATA_PT_context_camera.draw )
    unregister = bpy.types.unregister
    for cls in classes:
        unregister(cls)


if __name__ == "__main__":
    register()
