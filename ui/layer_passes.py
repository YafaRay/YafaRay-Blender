# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

from bpy.types import Panel
from bl_ui.properties_render_layer import RenderLayerButtonsPanel


class YAFARAY4_PT_layers(RenderLayerButtonsPanel, Panel):
    bl_label = "Layers"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
#    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render

        row = layout.row()
        row.template_list("RENDERLAYER_UL_renderlayers", "", rd, "layers", rd.layers, "active_index", rows=2)

        col = row.column(align=True)
        col.operator("scene.render_layer_add", icon="ADD" if bpy.app.version >= (2, 80, 0) else "ZOOMIN", text="")
        col.operator("scene.render_layer_remove", icon="REMOVE" if bpy.app.version >= (2, 80, 0) else "ZOOMOUT", text="")

        row = layout.row()
        rl = rd.layers.active
        row.prop(rl, "name")
        row.prop(rd, "use_single_layer", text="", icon_only=True)

        split = layout.split()

        col = split.column()
        col.prop(scene, "layers", text="Scene")
        # TODO: Implement material override
        #col.prop(rl, "material_override", text="Material")

        col = split.column()
        # TODO: Implement render layers
        #col.prop(rl, "layers", text="Layer")

class YAFARAY4_PT_layer_passes(RenderLayerButtonsPanel, Panel):
    bl_label = "Render Passes"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw_header(self, context):
        scene = context.scene
        self.layout.prop(scene.yafaray.passes, "pass_enable", text="")

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render
        rl = rd.layers.active

        if scene.yafaray.passes.pass_enable:

                row = layout.row() #(align=True)
                row = layout.row() #(align=True)
                row.prop(rl, "use_pass_z") #, "Z-depth")
                if scene.render.layers[0].use_pass_z:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_Depth", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_vector")
                if scene.render.layers[0].use_pass_vector:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_Vector", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_normal")
                if scene.render.layers[0].use_pass_normal:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_Normal", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_uv")
                if scene.render.layers[0].use_pass_uv:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_UV", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_color")
                if scene.render.layers[0].use_pass_color:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_Color", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_emit")
                if scene.render.layers[0].use_pass_emit:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_Emit", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_mist")
                if scene.render.layers[0].use_pass_mist:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_Mist", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_diffuse")
                if scene.render.layers[0].use_pass_diffuse:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_Diffuse", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_specular")
                if scene.render.layers[0].use_pass_specular:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_Spec", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_ambient_occlusion")
                if scene.render.layers[0].use_pass_ambient_occlusion:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_AO", "")
                        row = layout.row()
                        col = row.column()
                        col.prop(scene, "intg_AO_color")
                        col.prop(scene, "intg_AO_samples")
                        col.prop(scene, "intg_AO_distance")
                
                row = layout.row()
                row.prop(rl, "use_pass_environment")
                if scene.render.layers[0].use_pass_environment:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_Env", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_indirect")
                if scene.render.layers[0].use_pass_indirect:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_Indirect", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_shadow")
                if scene.render.layers[0].use_pass_shadow:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_Shadow", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_reflection")
                if scene.render.layers[0].use_pass_reflection:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_Reflect", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_refraction")
                if scene.render.layers[0].use_pass_refraction:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_Refract", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_object_index")
                if scene.render.layers[0].use_pass_object_index:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_IndexOB", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_material_index")
                if scene.render.layers[0].use_pass_material_index:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_IndexMA", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_diffuse_direct")
                if scene.render.layers[0].use_pass_diffuse_direct:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_DiffDir", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_diffuse_indirect")
                if scene.render.layers[0].use_pass_diffuse_indirect:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_DiffInd", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_diffuse_color")
                if scene.render.layers[0].use_pass_diffuse_color:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_DiffCol", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_glossy_direct")
                if scene.render.layers[0].use_pass_glossy_direct:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_GlossDir", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_glossy_indirect")
                if scene.render.layers[0].use_pass_glossy_indirect:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_GlossInd", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_glossy_color")
                if scene.render.layers[0].use_pass_glossy_color:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_GlossCol", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_transmission_direct")
                if scene.render.layers[0].use_pass_transmission_direct:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_TransDir", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_transmission_indirect")
                if scene.render.layers[0].use_pass_transmission_indirect:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_TransInd", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_transmission_color")
                if scene.render.layers[0].use_pass_transmission_color:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_TransCol", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_subsurface_direct")
                if scene.render.layers[0].use_pass_subsurface_direct:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_SubsurfaceDir", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_subsurface_indirect")
                if scene.render.layers[0].use_pass_subsurface_indirect:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_SubsurfaceInd", "")
                
                row = layout.row()
                row.prop(rl, "use_pass_subsurface_color")
                if scene.render.layers[0].use_pass_subsurface_color:
                        sub = row.column(align=True)
                        sub.prop(scene.yafaray.passes, "pass_SubsurfaceCol", "")


                box = layout.box()
                box.label(text="Masking Passes settings:")

                row = box.row()
                row.prop(scene.yafaray.passes, "pass_mask_obj_index")
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_mask_mat_index")

                row = box.row()
                row.prop(scene.yafaray.passes, "pass_mask_invert")                        
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_mask_only")                        


                box = layout.box()
                box.label(text="Toon and Object Edge Passes settings:")

                row = box.row()
                row.prop(scene.yafaray.passes, "objectEdgeThickness")                        
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "toonEdgeColor", text = "")                        
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "objectEdgeSmoothness")                        
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "objectEdgeThreshold")                        

                row = box.row()
                row.prop(scene.yafaray.passes, "toonPreSmooth")                        
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "toonQuantization")                        
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "toonPostSmooth")  

                box = layout.box()
                box.label(text="Faces Edge Pass settings:")

                row = box.row()
                row.prop(scene.yafaray.passes, "facesEdgeThickness")
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "facesEdgeSmoothness")                        
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "facesEdgeThreshold")                        


class YAFARAY4_PT_views(RenderLayerButtonsPanel, Panel):
    bl_label = "Views"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}
    
    def draw_header(self, context):
        rd = context.scene.render
        self.layout.prop(rd, "use_multiview", text="")

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render
        rv = rd.views.active

        if rd.use_multiview:
                layout.active = rd.use_multiview
                basic_stereo = rd.views_format == 'STEREO_3D'

                row = layout.row()
                row.prop(rd, "views_format", expand=True)

                if basic_stereo:
                    row = layout.row()
                    row.template_list("RENDERLAYER_UL_renderviews", "name", rd, "stereo_views", rd.views, "active_index", rows=2)

                    row = layout.row()
                    row.label(text="File Suffix:")
                    row.prop(rv, "file_suffix", text="")

                else:
                    row = layout.row()
                    row.template_list("RENDERLAYER_UL_renderviews", "name", rd, "views", rd.views, "active_index", rows=2)

                    col = row.column(align=True)
                    col.operator("scene.render_view_add", icon="ADD" if bpy.app.version >= (2, 80, 0) else "ZOOMIN", text="")
                    col.operator("scene.render_view_remove", icon="REMOVE" if bpy.app.version >= (2, 80, 0) else "ZOOMOUT", text="")

                    row = layout.row()
                    row.label(text="Camera Suffix:")
                    row.prop(rv, "camera_suffix", text="")


classes = (
    YAFARAY4_PT_layers,
    YAFARAY4_PT_layer_passes,
    YAFARAY4_PT_views,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed, before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the "libyafaray4_bindings" compiled module is installed on
    register()
