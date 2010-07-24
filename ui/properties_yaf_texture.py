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
from rna_prop_ui import PropertyPanel

narrowui = bpy.context.user_preferences.view.properties_width_check

FloatProperty = bpy.types.Texture.FloatProperty
IntProperty = bpy.types.Texture.IntProperty
BoolProperty = bpy.types.Texture.BoolProperty
CollectionProperty = bpy.types.Texture.CollectionProperty
EnumProperty = bpy.types.Texture.EnumProperty
FloatVectorProperty = bpy.types.Texture.FloatVectorProperty
StringProperty = bpy.types.Texture.StringProperty
IntVectorProperty = bpy.types.Texture.IntVectorProperty

EnumProperty(attr="yaf_tex_type",
        items = (
                ("BLEND","Blend",""),
                ("CLOUDS","Clouds",""),
                ("WOOD","Wood",""),
                ("MARBLE","Marble",""),
                ("VORONOI","Voronoi",""),
                ("MUSGRAVE","Musgrave",""),
                ("DISTORTED_NOISE","Distorted Noise",""),
                ("IMAGE","Image",""),
),default="CLOUDS")


from properties_material import active_node_mat


def context_tex_datablock(context):
    idblock = context.material
    if idblock:
        return active_node_mat(idblock)

    idblock = context.lamp
    if idblock:
        return idblock

    idblock = context.world
    if idblock:
        return idblock

    idblock = context.brush
    return idblock

class YAF_TextureButtonsPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "texture"

    def poll(self, context):
        tex = context.texture
        if not tex:
            return False
        engine = context.scene.render.engine
        var =  (engine in self.COMPAT_ENGINES)
        
        if var:
                import properties_texture
                
                try :
                        properties_world.unregister()
                except: 
                        pass
                del properties_texture
        return var


class YAF_TEXTURE_PT_preview(YAF_TextureButtonsPanel):
    bl_label = "Preview"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture
        slot = getattr(context, "texture_slot", None)
        idblock = context_tex_datablock(context)

        if idblock:
            layout.template_preview(tex, parent=idblock, slot=slot)
        else:
            layout.template_preview(tex, slot=slot)


class YAF_TEXTURE_PT_context_texture(YAF_TextureButtonsPanel):
    bl_label = ""
    bl_show_header = False
    COMPAT_ENGINES = {'YAFA_RENDER'}
    count = 0

    def poll(self, context):
        engine = context.scene.render.engine
        if not hasattr(context, "texture_slot"):
            return False
        return ((context.material or context.world or context.lamp or context.brush or context.texture)
            and (engine in self.COMPAT_ENGINES))


    def draw(self, context):
        
        #import properties_texture
        #
        #try :
        #        properties_world.unregister()
        #except: 
        #        pass
        #del properties_texture
        
        layout = self.layout
        slot = context.texture_slot
        node = context.texture_node
        space = context.space_data
        tex = context.texture
        wide_ui = context.region.width > narrowui
        idblock = context_tex_datablock(context)
        tex_collection = space.pin_id == None and type(idblock) != bpy.types.Brush and not node

        if tex_collection:
            row = layout.row()

            row.template_list(idblock, "texture_slots", idblock, "active_texture_index", rows=2)

            #col = row.column(align=True)
            #col.operator("texture.slot_move", text="", icon='TRIA_UP').type = 'UP'
            #col.operator("texture.slot_move", text="", icon='TRIA_DOWN').type = 'DOWN'
            #col.menu("TEXTURE_MT_specials", icon='DOWNARROW_HLT', text="")

        if wide_ui:
            split = layout.split(percentage=0.65)
            col = split.column()
        else:
            col = layout.column()

        if tex_collection:
            col.template_ID(idblock, "active_texture", new="texture.new")
        elif node:
            col.template_ID(node, "texture", new="texture.new")
        elif idblock:
            col.template_ID(idblock, "texture", new="texture.new")

        if space.pin_id:
            col.template_ID(space, "pin_id")

        if wide_ui:
            col = split.column()

        if not space.pin_id:
            col.prop(space, "brush_texture", text="Brush", toggle=True)

        if tex:
            split = layout.split(percentage=0.2)

            if tex.use_nodes:

                if slot:
                    split.label(text="Output:")
                    split.prop(slot, "output_node", text="")

            else:
                if wide_ui:
                    split.label(text="Type:")
                    split.prop(tex, "yaf_tex_type", text="")
                    #tex.type = tex.yaf_tex_type
                else:
                    layout.prop(tex, "yaf_tex_type", text="")
                    #tex.type = tex.yaf_tex_type


classes = [
    #TEXTURE_MT_specials,
    #TEXTURE_MT_envmap_specials,

    YAF_TEXTURE_PT_context_texture,
    YAF_TEXTURE_PT_preview,

    #YAF_TEXTURE_PT_clouds, # Texture Type Panels
    #YAF_TEXTURE_PT_wood,
    #YAF_TEXTURE_PT_marble,
    ##TEXTURE_PT_magic,
    #YAF_TEXTURE_PT_blend,
    ##YAF_TEXTURE_PT_stucci,
    #YAF_TEXTURE_PT_image,
    #YAF_TEXTURE_PT_image_sampling,
    #YAF_TEXTURE_PT_image_mapping,
    ##YAF_TEXTURE_PT_plugin,
    ##YAF_TEXTURE_PT_envmap,
    ##TEXTURE_PT_envmap_sampling,
    #YAF_TEXTURE_PT_musgrave,
    #YAF_TEXTURE_PT_voronoi,
    #YAF_TEXTURE_PT_distortednoise,
    ##TEXTURE_PT_voxeldata,
    ##TEXTURE_PT_pointdensity,
    ##TEXTURE_PT_pointdensity_turbulence,
    #
    #YAF_TEXTURE_PT_colors,
    #YAF_TEXTURE_PT_mapping,
    #YAF_TEXTURE_PT_influence,

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