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

# <pep8 compliant>

import bpy
from bpy.types import Panel
from bl_ui.properties_render_layer import RenderLayerButtonsPanel

RenderLayerButtonsPanel.COMPAT_ENGINES = {'YAFA_RENDER'}

class ViewsLightGroupList_UL_List(bpy.types.UIList):
    COMPAT_ENGINES = {'YAFA_RENDER'}
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
 
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "view_number")

            if item.view_number < len(context.scene.render.views):
                    layout.label("", icon = 'SCENE')
                    layout.label(context.scene.render.views[item.view_number].name)
                    layout.label("", icon = 'LAMP')
                    layout.prop(item, "light_group")
            else:
                    layout.label("", icon = 'ERROR')
                    layout.label("View not defined, skipping.")
 
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label("", icon = custom_icon)
            
bpy.utils.register_class(ViewsLightGroupList_UL_List)    # ( inside register() )  FIXME DAVID??

class ViewsLightGroupList_OT_NewItem(bpy.types.Operator):
    bl_idname = "views_lightgroup_list.new_item"
    bl_label = "Add a new View-Light Group Filter assignment"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def execute(self, context):
        context.scene.yafaray.passes.views_lightgroup_list.add()
 
        return{'FINISHED'}

bpy.utils.register_class(ViewsLightGroupList_OT_NewItem)    # ( inside register() )  FIXME DAVID??

class ViewsLightGroupList_OT_DeleteItem(bpy.types.Operator):
    bl_idname = "views_lightgroup_list.delete_item"
    bl_label = "Delete a View-Light Group Filter assignment"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(self, context):
        return len(context.scene.yafaray.passes.views_lightgroup_list) > 0

    def execute(self, context):
        list = context.scene.yafaray.passes.views_lightgroup_list
        index = context.scene.yafaray.passes.views_lightgroup_list_index

        list.remove(index)

        if index > 0:
            index = index - 1

        return{'FINISHED'}

bpy.utils.register_class(ViewsLightGroupList_OT_DeleteItem)    # ( inside register() )  FIXME DAVID??

class YAFRENDER_PT_layers(RenderLayerButtonsPanel, Panel):
    bl_label = "Layers"
    COMPAT_ENGINES = {'YAFA_RENDER'}
#    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render

        row = layout.row()
        if bpy.app.version < (2, 65, 3 ):
            row.template_list(rd, "layers", rd.layers, "active_index", rows=2)
        else:
            row.template_list("RENDERLAYER_UL_renderlayers", "", rd, "layers", rd.layers, "active_index", rows=2)

        col = row.column(align=True)
        col.operator("scene.render_layer_add", icon='ZOOMIN', text="")
        col.operator("scene.render_layer_remove", icon='ZOOMOUT', text="")

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

class YAFRENDER_PT_layer_passes(RenderLayerButtonsPanel, Panel):
    bl_label = "Render Passes"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw_header(self, context):
        scene = context.scene
        self.layout.prop(scene.yafaray.passes, "pass_enable", text="")

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render
        rl = rd.layers.active

        #row = layout.row(align=True)
        #row.alignment = 'LEFT'

        #row.prop(scene.yafaray.passes, "pass_enable", toggle=True) #, "optional extended description")
        if scene.yafaray.passes.pass_enable:

                row = layout.row() #(align=True)
                #row.alignment = 'LEFT'
                ##row.prop(rl, "use_pass_combined")
                ##if scene.render.layers[0].use_pass_combined:
                ##        sub = row.column(align=True)
                ##        sub.prop(scene.yafaray.passes, "pass_combined", "")
                
                row = layout.row() #(align=True)
                #row.alignment = 'LEFT'
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

                row = layout.row()
                row.prop(scene.yafaray.passes, "pass_mask_obj_index")
                
                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_mask_mat_index")
                
                row = layout.row()
                row.prop(scene.yafaray.passes, "pass_mask_invert")                        

                sub = row.column(align=True)
                sub.prop(scene.yafaray.passes, "pass_mask_only")                        


class YAFRENDER_PT_views(RenderLayerButtonsPanel, Panel):
    bl_label = "Views"
    COMPAT_ENGINES = {'YAFA_RENDER'}
    
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
                    col.operator("scene.render_view_add", icon='ZOOMIN', text="")
                    col.operator("scene.render_view_remove", icon='ZOOMOUT', text="")

                    row = layout.row()
                    row.label(text="Camera Suffix:")
                    row.prop(rv, "camera_suffix", text="")

                row = layout.row()
                row.label(text="Views - Light Group filters:")
                if len(scene.yafaray.passes.views_lightgroup_list) == 0:
                        row = layout.row()
                        row.label(icon="INFO", text="No views/light group filters defined.")
                        row = layout.row()
                        row.label(icon="INFO", text="By default all views will be rendered with all lights.")
                row = layout.row()
                row.template_list("ViewsLightGroupList_UL_List", "ViewsLightGroupList", scene.yafaray.passes, "views_lightgroup_list", scene.yafaray.passes, "views_lightgroup_list_index", rows=2)
                col = row.column(align=True)
                col.operator('views_lightgroup_list.new_item', icon='ZOOMIN', text="")
                col.operator('views_lightgroup_list.delete_item', icon='ZOOMOUT', text="")
                if len(scene.yafaray.passes.views_lightgroup_list) > 0:
                        row = layout.row()
                        row.label(icon="INFO", text="Only the selected views with the assigned light groups will be rendered")
                        row = layout.row()
                        row.label(icon="INFO", text="If several light groups are assigned to the same view, ONLY THE LAST ONE will be imported into Blender.")
        

if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
