import bpy

class YafarayRenderButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    COMPAT_ENGINES = ['YAFA_RENDER']

    @classmethod
    def poll(self, context):
        render = context.scene.render
        return (render.engine in self.COMPAT_ENGINES)

class YAFRENDER_PT_render(YafarayRenderButtonsPanel, bpy.types.Panel):

    bl_label = 'Render'

    def draw(self, context):

        split = self.layout.split()

        split.column().operator("RENDER_OT_render", "Render Image", "RENDER_STILL")
        
        split.column().operator("RENDER_OT_render", "Render Animation", "RENDER_ANIMATION").animation = True
        
        if context.scene.render.engine == "YAFA_RENDER":
            self.layout.row().operator("RENDER_OT_render_view", "Render 3D View", "VIEW3D")
        
        self.layout.row().prop(context.scene.render, "display_mode")

class YAFRENDER_PT_dimensions(YafarayRenderButtonsPanel, bpy.types.Panel):

    bl_label = "Dimensions"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render

        row = layout.row(align=True)
        row.menu("RENDER_MT_presets", text=bpy.types.RENDER_MT_presets.bl_label)
        row.operator("render.preset_add", text="", icon="ZOOMIN")
        row.operator("render.preset_add", text="", icon="ZOOMOUT").remove_active = True

        split = layout.split()

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Resolution:")
        sub.prop(rd, "resolution_x", text="X")
        sub.prop(rd, "resolution_y", text="Y")
        sub.prop(rd, "resolution_percentage", text="")

        row = layout.row(align=True)
        row.prop(rd, "use_border", text="Border", toggle=True)

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Frame Range:")
        sub.prop(scene, "frame_start", text="Start")
        sub.prop(scene, "frame_end", text="End")
        sub.prop(scene, "frame_step", text="Step")

from yafaray.ui import properties_yaf_general_settings
from yafaray.ui import properties_yaf_integrator
from yafaray.ui import properties_yaf_AA_settings

class YAFRENDER_PT_output(YafarayRenderButtonsPanel, bpy.types.Panel):

    bl_label = "Output Settings"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render
        file_format = rd.file_format

        layout.prop(rd, "filepath", text="")

        split = layout.split()
        col = split.column()
        col.prop(rd, "file_format", text="")

        if file_format == 'JPEG':
            split = layout.split()
            split.label("Using 8 Bit color depth, full quality")

        elif file_format == 'PNG':
            split = layout.split()
            split.label("Using 8 Bit color depth, no compression")

        elif file_format == 'TARGA':
            split = layout.split()
            split.label("Using 8 Bit color depth, no RLE")

        elif file_format == 'OPEN_EXR':
            split = layout.split()
            split.label("Using Half Float format with Z-Buffer")
            split.label("(If Z-Buffer is enabled on the render settings)")
 
        elif file_format == 'TIFF':
            split = layout.split()
            split.label("Using 8 bit depth TIFF")

        else:
            split = layout.split()
            split.label("Not supported by YafaRay")

