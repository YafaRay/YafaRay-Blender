import bpy
from bl_ui.properties_material import active_node_mat
#import types and props ---->
from bpy.props import *
Texture = bpy.types.Texture

Texture.yaf_tex_type =          EnumProperty(
                                    items = (
                                        ("NONE", "None", ""),
                                        ("BLEND", "Blend", ""),
                                        ("CLOUDS", "Clouds", ""),
                                        ("WOOD", "Wood", ""),
                                        ("MARBLE", "Marble", ""),
                                        ("VORONOI", "Voronoi", ""),
                                        ("MUSGRAVE", "Musgrave", ""),
                                        ("DISTORTED_NOISE", "Distorted Noise", ""),
                                        ("IMAGE", "Image", "")),
                                    default = "NONE",
                                    name = "Texture Type")
    
Texture.yaf_tex_interpolate =   EnumProperty(
                                    items = (
                                        ("bilinear", "Bilinear", ""),
                                        ("bicubic", "Bicubic", ""),
                                        ("none", "None", "")),
                                    default = "bilinear",
                                    name = "Interpolation type")

Texture.tex_file_name =         StringProperty(attr='tex_file_name', subtype = 'FILE_PATH')
Texture.yaf_is_normal_map =     BoolProperty(default = False, name = "Normal map")

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
    if idblock:
        return idblock

    if context.particle_system:
        idblock = context.particle_system.settings

    return idblock


class YAF_TextureButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "texture"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):
        tex = context.texture
        return tex and (tex.type != 'NONE' or tex.use_nodes) and (context.scene.render.engine in cls.COMPAT_ENGINES)


class YAF_TEXTURE_PT_context_texture(YAF_TextureButtonsPanel, bpy.types.Panel):
    bl_label = "YafaRay Textures"
    bl_options = {'HIDE_HEADER'}
    # bl_show_header = True
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        if not hasattr(context, "texture_slot"):
            return False

        return ((context.material or context.world or context.lamp or context.brush or context.texture \
        or context.particle_system or isinstance(context.space_data.pin_id, bpy.types.ParticleSettings)) \
        and (engine in cls.COMPAT_ENGINES))

    def draw(self, context):
        layout = self.layout
        slot = context.texture_slot
        node = context.texture_node
        space = context.space_data
        tex = context.texture
        idblock = context_tex_datablock(context)
        pin_id = space.pin_id

        if space.use_pin_id and not isinstance(pin_id, bpy.types.Texture):
            idblock = pin_id
            pin_id = None

        if not space.use_pin_id:
            layout.prop(space, "texture_context", expand=True)

        tex_collection = (pin_id is None) and (node is None) and (not isinstance(idblock, bpy.types.Brush))

        if tex_collection:
            row = layout.row()

            row.template_list(idblock, "texture_slots", idblock, "active_texture_index", rows=2)

            col = row.column(align=True)
            col.operator("texture.slot_move", text="", icon='TRIA_UP').type = 'UP'
            col.operator("texture.slot_move", text="", icon='TRIA_DOWN').type = 'DOWN'
            col.menu("TEXTURE_MT_specials", icon='DOWNARROW_HLT', text="")

        split = layout.split(percentage=0.65)
        col = split.column()

        if tex_collection:
            col.template_ID(idblock, "active_texture", new="texture.new")
        elif node:
            col.template_ID(node, "texture", new="texture.new")
        elif idblock:
            col.template_ID(idblock, "texture", new="texture.new")

        if pin_id:
            col.template_ID(space, "pin_id")

        col = split.column()

        if tex:
            split = layout.split(percentage=0.2)

            if tex.use_nodes:

                if slot:
                    split.label(text="Output:")
                    split.prop(slot, "output_node", text="")

            else:
                split.label(text="Type:")
                split.prop(tex, "type", text="")


class YAF_TEXTURE_PT_preview(YAF_TextureButtonsPanel, bpy.types.Panel):
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


class YAF_TextureSlotPanel(YAF_TextureButtonsPanel):
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):
        if not hasattr(context, "texture_slot"):
            return False

        engine = context.scene.render.engine
        return YAF_TextureButtonsPanel.poll(self, context) and (engine in cls.COMPAT_ENGINES)


class YAF_TextureTypePanel(YAF_TextureButtonsPanel):

    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):
        tex = context.texture
        engine = context.scene.render.engine
        return tex and ((tex.type == cls.tex_type and not tex.use_nodes) and (engine in cls.COMPAT_ENGINES))


class YAF_TEXTURE_PT_clouds(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Clouds"
    tex_type = 'CLOUDS'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        layout.prop(tex, "cloud_type", expand=True)
        layout.label(text="Noise:")
        layout.prop(tex, "noise_type", text="Type", expand=True)
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")
        split.prop(tex, "noise_depth", text="Depth")


class YAF_TEXTURE_PT_wood(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Wood"
    tex_type = 'WOOD'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        layout.prop(tex, "noise_basis_2", expand=True)
        layout.prop(tex, "wood_type", expand=True)

        col = layout.column()
        col.active = tex.wood_type in {'RINGNOISE', 'BANDNOISE'}
        col.label(text="Noise:")
        col.row().prop(tex, "noise_type", text="Type", expand=True)
        col.row().prop(tex, "noise_basis", text="Basis")

        split = layout.split()
        split.active = tex.wood_type in {'RINGNOISE', 'BANDNOISE'}

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")
        split.prop(tex, "turbulence")


class YAF_TEXTURE_PT_marble(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Marble"
    tex_type = 'MARBLE'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        layout.prop(tex, "marble_type", expand=True)
        layout.prop(tex, "noise_basis_2", expand=True)
        layout.label(text="Noise:")
        layout.prop(tex, "noise_type", text="Type", expand=True)
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")
        col.prop(tex, "noise_depth", text="Depth")
        split.prop(tex, "turbulence")


class YAF_TEXTURE_PT_blend(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Blend"
    tex_type = 'BLEND'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture
        layout.prop(tex, "progression")
        if tex.progression != 'LINEAR':  # TODO: remove this if other progression types are supported
            layout.label(text='Not yet supported in YafaRay')
        else:
            layout.label(text=' ')


class YAF_TEXTURE_PT_image(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Map Image"
    tex_type = 'IMAGE'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture
        layout.template_image(tex, "image", tex.image_user)


class YAF_TEXTURE_PT_image_sampling(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Image Sampling"
    bl_options = {'DEFAULT_CLOSED'}
    tex_type = 'IMAGE'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        idblock = context_tex_datablock(context)
        tex = context.texture

        split = layout.split()

        col = split.column()
        col.label(text="Image:")
        col.prop(tex, "use_alpha", text="Use Alpha")
        col.prop(tex, "use_calculate_alpha", text="Calculate Alpha")
        col.prop(tex, "use_flip_axis", text="Flip X/Y Axis") 

        col = split.column()
        col.label(text = "Interpolation:")
        col.prop(tex, "yaf_tex_interpolate", text = "")


class YAF_TEXTURE_PT_image_mapping(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Image Mapping"
    bl_options = {'DEFAULT_CLOSED'}
    tex_type = 'IMAGE'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        layout.prop(tex, "extension")

        split = layout.split()

        if tex.extension == 'REPEAT':
            row = layout.row(align = True)
            row.prop(tex, "repeat_x", text="X Repeat")
            row.prop(tex, "repeat_y", text="Y Repeat")

            layout.separator()

        elif tex.extension == 'CHECKER':
            col = split.column(align=True)
            row = col.row()
            row.prop(tex, "use_checker_even", text="Even")
            row.prop(tex, "use_checker_odd", text="Odd")

            col = split.column()
            col.prop(tex, "checker_distance", text="Distance")

            layout.separator()

        split = layout.split()

        col = split.column(align=True)
        col.label(text="Crop Minimum:")
        col.prop(tex, "crop_min_x", text="X")
        col.prop(tex, "crop_min_y", text="Y")

        col = split.column(align=True)
        col.label(text="Crop Maximum:")
        col.prop(tex, "crop_max_x", text="X")
        col.prop(tex, "crop_max_y", text="Y")


class YAF_TEXTURE_PT_musgrave(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Musgrave"
    tex_type = 'MUSGRAVE'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        layout.prop(tex, "musgrave_type")

        split = layout.split()

        col = split.column()
        col.prop(tex, "dimension_max", text="Dimension")
        col.prop(tex, "lacunarity")
        col.prop(tex, "octaves")

        musgrave_type = tex.musgrave_type
        col = split.column()
        if musgrave_type in {'HETERO_TERRAIN', 'RIDGED_MULTIFRACTAL', 'HYBRID_MULTIFRACTAL'}:
            col.prop(tex, "offset")
        if musgrave_type in {'MULTIFRACTAL', 'RIDGED_MULTIFRACTAL', 'HYBRID_MULTIFRACTAL'}:
            col.prop(tex, "noise_intensity", text="Intensity")
        if musgrave_type in {'RIDGED_MULTIFRACTAL', 'HYBRID_MULTIFRACTAL'}:
            col.prop(tex, "gain")

        layout.label(text="Noise:")

        layout.prop(tex, "noise_basis", text="Basis")

        row = layout.row()
        row.prop(tex, "noise_scale", text="Size")


class YAF_TEXTURE_PT_voronoi(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Voronoi"
    tex_type = 'VORONOI'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        split = layout.split()

        col = split.column()
        col.label(text="Distance Metric:")
        col.prop(tex, "distance_metric", text="")
        sub = col.column()
        sub.active = tex.distance_metric == 'MINKOVSKY'
        sub.prop(tex, "minkovsky_exponent", text="Exponent")
        col.label(text="Coloring:")
        col.prop(tex, "color_mode", text="")
        col.prop(tex, "noise_intensity", text="Intensity")

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Feature Weights:")
        sub.prop(tex, "weight_1", text="1", slider=True)
        sub.prop(tex, "weight_2", text="2", slider=True)
        sub.prop(tex, "weight_3", text="3", slider=True)
        sub.prop(tex, "weight_4", text="4", slider=True)

        layout.label(text="Noise:")
        row = layout.row()
        row.prop(tex, "noise_scale", text="Size")


class YAF_TEXTURE_PT_distortednoise(YAF_TextureTypePanel, bpy.types.Panel):
    bl_label = "Distorted Noise"
    tex_type = 'DISTORTED_NOISE'
    COMPAT_ENGINES = {'YAFA_RENDER'}

    def draw(self, context):
        layout = self.layout

        tex = context.texture

        layout.prop(tex, "noise_distortion")
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "distortion", text="Distortion")
        split.prop(tex, "noise_scale", text="Size")


class YAF_TEXTURE_PT_mapping(YAF_TextureSlotPanel, bpy.types.Panel):
    bl_label = "YafaRay Mapping (Map Input)"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):
        idblock = context_tex_datablock(context)
        if isinstance(idblock, bpy.types.Brush) and not context.sculpt_object:
            return False

        if not getattr(context, "texture_slot", None):
            return False

        engine = context.scene.render.engine
        return (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        idblock = context_tex_datablock(context)

        tex = context.texture_slot
        # textype = context.texture

        if not isinstance(idblock, bpy.types.Brush):
            split = layout.split(percentage=0.3)
            col = split.column()
            col.label(text="Coordinates:")
            col = split.column()
            col.prop(tex, "texture_coords", text="")

            if tex.texture_coords == 'UV':
                split = layout.split(percentage=0.3)
                split.label(text="Layer:")
                ob = context.object
                if ob and ob.type == 'MESH':
                    split.prop_search(tex, "uv_layer", ob.data, "uv_textures", text="")
                else:
                    split.prop(tex, "uv_layer", text="")

            elif tex.texture_coords == 'OBJECT':
                split = layout.split(percentage=0.3)
                split.label(text="Object:")
                split.prop(tex, "object", text="")

        if isinstance(idblock, bpy.types.Brush):
            if context.sculpt_object:
                layout.label(text="Brush Mapping:")
                layout.prop(tex, "map_mode", expand=True)

                row = layout.row()
                row.active = tex.map_mode in {'FIXED', 'TILED'}
                row.prop(tex, "angle")
        else:
            if isinstance(idblock, bpy.types.Material):
                split = layout.split(percentage=0.3)
                split.label(text="Projection:")
                split.prop(tex, "mapping", text="")

                split = layout.split()

                col = split.column()
                if tex.texture_coords in {'ORCO', 'UV'}:
                    col.prop(tex, "use_from_dupli")
                elif tex.texture_coords == 'OBJECT':
                    col.prop(tex, "use_from_original")
                else:
                    col.label()

                col = split.column()
                row = col.row()
                row.prop(tex, "mapping_x", text="")
                row.prop(tex, "mapping_y", text="")
                row.prop(tex, "mapping_z", text="")

        row = layout.row()
        row.column().prop(tex, "offset")
        row.column().prop(tex, "scale") 


class YAF_TEXTURE_PT_influence(YAF_TextureSlotPanel, bpy.types.Panel):
    bl_label = "YafaRay Influence (Map To)"
    COMPAT_ENGINES = {'YAFA_RENDER'}

    @classmethod
    def poll(cls, context):
        idblock = context_tex_datablock(context)
        if isinstance(idblock, bpy.types.Brush):
            return False

        if not getattr(context, "texture_slot", None):
            return False

        engine = context.scene.render.engine
        return (engine in cls.COMPAT_ENGINES)

    def factor_but(self, tex, layout, toggle, factor, name):
        row = layout.row(align = True)
        row.prop(tex, toggle, text = "")
        sub = row.row()
        sub.enabled = getattr(tex, toggle)
        sub.prop(tex, factor, text = name, slider = True)
        return sub  # XXX, temp. use_map_normal needs to override.

    def draw(self, context):

        layout = self.layout

        idblock = context_tex_datablock(context)

        tex_slot = context.texture_slot
        texture = context.texture

        shaderNodes = dict()
        shaderNodes["Bump"]         = ["use_map_normal", "normal_factor", "Bump"]
        shaderNodes["MirrorAmount"] = ["use_map_raymir", "raymir_factor", "Mirror Amount"]
        shaderNodes["MirrorColor"]  = ["use_map_mirror", "mirror_factor", "Mirror Color"]
        shaderNodes["DiffuseColor"] = ["use_map_color_diffuse", "diffuse_color_factor", "Diffuse Color"]
        shaderNodes["GlossyColor"]  = ["use_map_color_spec", "specular_color_factor", "Glossy Color"]
        shaderNodes["GlossyAmount"] = ["use_map_specular", "specular_factor", "Glossy Amount"]
        shaderNodes["Transparency"] = ["use_map_alpha", "alpha_factor", "Transparency"]
        shaderNodes["Translucency"] = ["use_map_translucency", "translucency_factor", "Translucency"]
        shaderNodes["BlendAmount"]  = ["use_map_diffuse", "diffuse_factor", "Blending Amount"]

        materialShaderNodes = dict()
        materialShaderNodes["glass"]           = ["Bump", "MirrorColor"]
        materialShaderNodes["rough_glass"]     = ["Bump", "MirrorColor"]
        materialShaderNodes["glossy"]          = ["DiffuseColor", "GlossyColor", "GlossyAmount", "Bump"]
        materialShaderNodes["coated_glossy"]   = ["DiffuseColor", "GlossyColor", "GlossyAmount", "Bump"]
        materialShaderNodes["shinydiffusemat"] = ["DiffuseColor", "MirrorAmount", "MirrorColor", "Transparency", "Translucency", "Bump"]
        materialShaderNodes["blend"]           = ["BlendAmount"]

        if isinstance(idblock, bpy.types.Material):
            material = context.material
            materialType = material.mat_type

            nodes = materialShaderNodes[materialType]

            col = layout.column()

            for node in nodes:
                value = shaderNodes[node]
                self.factor_but(tex_slot, col, value[0], value[1], value[2])
                if node == "Bump" and getattr(tex_slot, "use_map_normal") and texture.type == "IMAGE":
                    col.prop(texture, "yaf_is_normal_map", "Use map as normal map")

        elif isinstance(idblock, bpy.types.World):  # for setup world texture
            split = layout.split()

            col = split.column()
            self.factor_but(tex_slot, col, "use_map_blend", "blend_factor", "Blend")
            self.factor_but(tex_slot, col, "use_map_horizon", "horizon_factor", "Horizon")
            col = split.column()
            self.factor_but(tex_slot, col, "use_map_zenith_up", "zenith_up_factor", "Zenith Up")
            self.factor_but(tex_slot, col, "use_map_zenith_down", "zenith_down_factor", "Zenith Down")

        layout.separator()

        if not isinstance(idblock, bpy.types.ParticleSettings) and not isinstance(idblock, bpy.types.World):
            split = layout.split()

            col = split.column()
            col.prop(tex_slot, "blend_type", text="Blend")
            col.prop(tex_slot, "use_rgb_to_intensity")
            col.prop(tex_slot, "color", text="")

            col = split.column()
            col.prop(tex_slot, "invert", text="Negative")
            col.prop(tex_slot, "use_stencil")

        if isinstance(idblock, bpy.types.Material) or isinstance(idblock, bpy.types.World):
            col.prop(tex_slot, "default_value", text="Default Value", slider=True)
