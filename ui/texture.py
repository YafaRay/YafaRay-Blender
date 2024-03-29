# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
# noinspection PyUnresolvedReferences
from bpy.types import (Panel,
                       Texture,
                       Material,
                       World,
                       ParticleSettings)

from .common import ui_split
from bl_ui.properties_texture import context_tex_datablock


def get_texture_from_context(context):
    if context.scene.yafaray4.texture_edition_panel == 'MATERIAL':
        material_properties = context.active_object.active_material.yafaray4
        return material_properties.texture_slots[material_properties.active_texture_index].texture
    elif context.scene.yafaray4.texture_edition_panel == 'WORLD':
        return context.scene.world.background_texture
    elif context.scene.yafaray4.texture_edition_panel == 'TEXTURE':
        return context.scene.yafaray4.texture_properties_edition.texture_selected
    else:
        return None


class TextureButtons:
    bl_idname = "YAFARAY4_PT_texture_buttons"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "texture"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return

        return tex and (tex.yaf_tex_type not in 'NONE' or tex.use_nodes) and (
                context.scene.render.engine in cls.COMPAT_ENGINES)


class OBJECT_UL_List(bpy.types.UIList):
    bl_idname = "OBJECT_UL_List"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if item.texture is not None:
                layout.label(text=item.name, icon_value=layout.icon(item.texture))
                layout.prop(item, "use", text="")
                # layout.prop(item, "texture", text="Slot", icon_value=layout.icon(item.texture))
            else:
                layout.label(text=" ", icon='TEXTURE')
                # layout.prop(item, "texture", text="Slot")


class Context(TextureButtons, Panel):
    bl_idname = "YAFARAY4_PT_texture_context"
    bl_label = "YafaRay Textures"
    bl_options = {'HIDE_HEADER'}
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.space_data.context == 'TEXTURE' and engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        if bpy.app.version >= (2, 80, 0):
            col = row.column()
            col.label(text="YafaRay **only** uses the panels below, ignore the 'Brush' and texture fields above", icon='INFO')
        row = layout.row()
        row.operator("yafaray4.select_texture_edition_panel_material", text="", icon='MATERIAL',
                     emboss=context.scene.yafaray4.texture_edition_panel == 'MATERIAL')
        row.operator("yafaray4.select_texture_edition_panel_world", text="", text_ctxt="", translate=True,
                     icon='WORLD', emboss=context.scene.yafaray4.texture_edition_panel == 'WORLD', icon_value=0)
        row.operator("yafaray4.select_texture_edition_panel_texture", text="", text_ctxt="", translate=True,
                     icon='TEXTURE', emboss=context.scene.yafaray4.texture_edition_panel == 'TEXTURE', icon_value=0)
        row = layout.row()
        tex = None
        if context.scene.yafaray4.texture_edition_panel == 'MATERIAL':
            material = context.active_object.active_material
            if hasattr(material.yafaray4, "texture_slots"):
                # row.prop(context.scene.yafaray4, "migrated_to_v4")
                # row = layout.row()
                row.template_list("OBJECT_UL_List", "test_coll", material.yafaray4, "texture_slots", material.yafaray4,
                                  "active_texture_index")
                col = row.column(align=True)
                col.operator("texture.slot_move", text="", icon='TRIA_UP').type = 'UP'
                col.operator("texture.slot_move", text="", icon='TRIA_DOWN').type = 'DOWN'
            row = layout.row()
            material_properties = context.active_object.active_material.yafaray4
            row.template_ID(material_properties.texture_slots[material_properties.active_texture_index], "texture", new="texture.new")
            tex = material_properties.texture_slots[material_properties.active_texture_index].texture

        elif context.scene.yafaray4.texture_edition_panel == 'WORLD':
            layout.template_ID(context.scene.world, "background_texture", new="texture.new")
            tex = context.scene.world.background_texture

        elif context.scene.yafaray4.texture_edition_panel == 'TEXTURE':
            texture_properties_edition = context.scene.yafaray4.texture_properties_edition
            col = row.column(align=True)
            col.label(text="Generic YafaRay Texture Editor")
            col.label(text="This editor allows to edit any textures from the scene or create new textures, "
                           "not associated to any objects")
            split = ui_split(layout, 0.25)
            col = split.column()
            col.label(text="Texture to edit:")
            col = split.column()
            col.template_ID(texture_properties_edition, "texture_selected", new="texture.new")
            tex = texture_properties_edition.texture_selected

        if tex is not None:
            split = ui_split(layout, 0.2)
            split.label(text="Type:")
            split.prop(tex, "yaf_tex_type", text="")


class Preview(TextureButtons, Panel):
    bl_idname = "YAFARAY4_PT_texture_preview"
    bl_label = "Preview"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return
        layout = self.layout
        idblock = context_tex_datablock(context)
        if idblock:
            layout.template_preview(tex, parent=idblock)
        else:
            layout.template_preview(tex)


class PreviewControls(TextureButtons, Panel):
    bl_idname = "YAFARAY4_PT_texture_preview_controls"
    bl_label = "Preview Controls"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    # bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.prop(context.scene.yafaray4.preview, "enable", text="")

    def draw(self, context):
        if context.scene.yafaray4.preview.enable:
            layout = self.layout
            split = layout.split()
            col = split.column()
            col.label(text="Preview dynamic rotation/zoom")
            split = layout.split()
            col = split.column()
            col.prop(context.scene.yafaray4.preview, "cam_rot", text="")
            col = split.column()
            row = col.row()
            row.operator("yafaray4.material_preview_camera_zoom_out", text='Zoom Out', icon='ZOOM_OUT')
            col2 = row.column()
            col2.operator("yafaray4.material_preview_camera_zoom_in", text='Zoom In', icon='ZOOM_IN')
            row = col.row()
            row.label(text="")
            row = col.row()
            row.operator("yafaray4.material_preview_camera_rotation_reset", text='Reset dynamic rotation/zoom')
            split = layout.split()
            col = split.column()
            col.label(text="Preview object control")
            split = layout.split()
            col = split.column()
            col.prop(context.scene.yafaray4.preview, "obj_scale", text="Scale")
            col = split.column()
            col.prop(context.scene.yafaray4.preview, "rot_z", text="Z Rotation")
            col = split.column()
            col.prop_search(context.scene.yafaray4.preview, "preview_object", bpy.data, "objects", text="")
            split = layout.split()
            col = split.column()
            col.label(text="Preview lights control")
            col = split.column()
            col.prop(context.scene.yafaray4.preview, "light_rot_z", text="lights Z Rotation")
            split = layout.split()
            col = split.column()
            col.label(text="Key light:")
            col = split.column()
            col.prop(context.scene.yafaray4.preview, "key_light_power_factor", text="Power factor")
            col = split.column()
            col.prop(context.scene.yafaray4.preview, "key_light_color", text="")
            split = layout.split()
            col = split.column()
            col.label(text="Fill lights:")
            col = split.column()
            col.prop(context.scene.yafaray4.preview, "fill_light_power_factor", text="Power factor")
            col = split.column()
            col.prop(context.scene.yafaray4.preview, "fill_light_color", text="")
            split = layout.split()
            col = split.column()
            col.label(text="Preview scene control")
            split = layout.split()
            col = split.column()
            col.prop(context.scene.yafaray4.preview, "preview_ray_depth", text="Ray Depth")
            col = split.column()
            col.prop(context.scene.yafaray4.preview, "preview_aa_passes", text="AA samples")
            col = split.column()
            col.prop(context.scene.yafaray4.preview, "preview_background", text="")


class Colors(TextureButtons, Panel):
    bl_idname = "YAFARAY4_PT_texture_colors"
    bl_label = "Colors"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return

        layout = self.layout
        layout.prop(tex, "use_color_ramp", text="Ramp")
        if tex.use_color_ramp:
            if tex.yaf_tex_type == "IMAGE":
                split = layout.split()
                row = split.row()
                row.label(text="Color ramp is ignored by YafaRay when using image textures", icon="INFO")

            if tex.color_ramp.color_mode == "RGB" and tex.color_ramp.interpolation != "CONSTANT" \
                    and tex.color_ramp.interpolation != "LINEAR":
                split = layout.split()
                row = split.row()
                row.label(
                    text="The ramp interpolation '" + tex.color_ramp.interpolation
                         + "' is not supported. Using Linear instead",
                    icon="ERROR")

            layout.template_color_ramp(tex, "color_ramp", expand=True)

        split = layout.split()

        col = split.column()
        col.label(text="RGB Multiply:")
        sub = col.column(align=True)
        sub.prop(tex, "factor_red", text="R")
        sub.prop(tex, "factor_green", text="G")
        sub.prop(tex, "factor_blue", text="B")

        col = split.column()
        col.label(text="Adjust:")
        col.prop(tex, "intensity")
        col.prop(tex, "contrast")

        split = layout.split()
        col = split.column()
        col.prop(tex, "yaf_adj_hue")
        col = split.column()
        col.prop(tex, "saturation")

        col = layout.column()
        col.prop(tex, "use_clamp", text="Clamp")


class Slot(TextureButtons):
    bl_idname = "YAFARAY4_PT_texture_slot"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):
        if not hasattr(context, "texture_slot"):
            return False

        engine = context.scene.render.engine
        return TextureButtons.poll(cls, context) and (engine in cls.COMPAT_ENGINES)


class Type(TextureButtons):
    bl_idname = "YAFARAY4_PT_texture_type"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return

        engine = context.scene.render.engine
        return tex and ((tex.yaf_tex_type == cls.tex_type and not tex.use_nodes) and (engine in cls.COMPAT_ENGINES))


# --- YafaRay's own Texture Type Panels --- #
class TypeClouds(Type, Panel):
    bl_idname = "YAFARAY4_PT_texture_type_clouds"
    bl_label = "Clouds"
    tex_type = 'CLOUDS'
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return
        layout = self.layout

        layout.prop(tex, "cloud_type", expand=True)
        layout.label(text="Noise:")
        layout.prop(tex, "noise_type", text="Type", expand=True)
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "noise_scale", text="Size")
        split.prop(tex, "noise_depth", text="Depth")


class TypeWood(Type, Panel):
    bl_idname = "YAFARAY4_PT_texture_type_wood"
    bl_label = "Wood"
    tex_type = 'WOOD'
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return
        layout = self.layout

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


class TypeMarble(Type, Panel):
    bl_idname = "YAFARAY4_PT_texture_type_marble"
    bl_label = "Marble"
    tex_type = 'MARBLE'
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return
        layout = self.layout

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


class TypeBlend(Type, Panel):
    bl_idname = "YAFARAY4_PT_texture_type_blend"
    bl_label = "Blend"
    tex_type = 'BLEND'
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return
        layout = self.layout

        layout.prop(tex, "progression")

        sub = layout.row()

        sub.active = (tex.progression in {'LINEAR', 'QUADRATIC', 'EASING', 'RADIAL'})
        sub.prop(tex, "use_flip_axis", expand=True)


class TypeImage(Type, Panel):
    bl_idname = "YAFARAY4_PT_texture_type_image"
    bl_label = "Map Image"
    tex_type = 'IMAGE'
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return
        layout = self.layout

        layout.template_image(tex, "image", tex.image_user)

        if hasattr(tex.image, "colorspace_settings"):
            if tex.image.colorspace_settings.name == "sRGB" or tex.image.colorspace_settings.name == "Linear" \
                    or tex.image.colorspace_settings.name == "Non-Color":
                pass

            elif tex.image.colorspace_settings.name == "XYZ":
                row = layout.row(align=True)
                row.label(text="YafaRay 'XYZ' support is experimental and may not give the expected results",
                          icon="ERROR")

            elif tex.image.colorspace_settings.name == "Linear ACES":
                row = layout.row(align=True)
                row.label(
                    text="YafaRay doesn't support '" + tex.image.colorspace_settings.name + "', assuming linear RGB",
                    icon="ERROR")

            elif tex.image.colorspace_settings.name == "Raw":
                row = layout.row(align=True)
                row.prop(tex, "yaf_gamma_input", text="Texture gamma input correction")

            else:
                row = layout.row(align=True)
                row.label(text="YafaRay doesn't support '" + tex.image.colorspace_settings.name + "', assuming sRGB",
                          icon="ERROR")

        row = layout.row(align=True)
        row.label(text="Note: for bump/normal maps, textures are always considered Linear", icon="INFO")


class TypeImageSampling(Type, Panel):
    bl_idname = "YAFARAY4_PT_texture_type_image_sampling"
    bl_label = "Image Sampling"
    bl_options = {'DEFAULT_CLOSED'}
    tex_type = 'IMAGE'
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return
        layout = self.layout

        layout.label(text="Image:")
        row = layout.row(align=True)
        if context.scene.yafaray4.texture_edition_panel != 'WORLD':
            '''povman: change layout to row for save space
                and show only options in each context
            '''
            row.prop(tex, "yaf_use_alpha", text="Use Alpha")
            row.prop(tex, "use_calculate_alpha", text="Calculate Alpha")
            layout.prop(tex, "use_flip_axis", text="Flip X/Y Axis")
            layout.prop(tex, "yaf_tex_interpolate")
            if tex.yaf_tex_interpolate == "mipmap_ewa":
                layout.prop(tex, "yaf_ewa_max_anisotropy")
            elif tex.yaf_tex_interpolate == "mipmap_trilinear":
                layout.prop(tex, "yaf_trilinear_level_bias")
        else:
            row.prop(tex, "use_interpolation", text="Use image background interpolation")
            # row.prop(tex, "use_calculate_alpha", text="Calculate Alpha")
        layout.prop(tex, "yaf_tex_optimization")
        layout.prop(tex, "yaf_img_grayscale", text="Use as Grayscale")


class TypeImageMapping(Type, Panel):
    bl_idname = "YAFARAY4_PT_texture_type_image_mapping"
    bl_label = "Image Mapping"
    bl_options = {'DEFAULT_CLOSED'}
    tex_type = 'IMAGE'
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return
        layout = self.layout

        layout.prop(tex, "extension")

        split = layout.split()

        if tex.extension == 'REPEAT':
            col = split.column(align=True)
            col.label(text="Repeat:")
            col.prop(tex, "repeat_x", text="X")
            col.prop(tex, "repeat_y", text="Y")

            col = split.column(align=True)
            col.label(text="Mirror:")
            row = col.row(align=True)
            row.prop(tex, "use_mirror_x", text="X")
            row = col.row(align=True)
            row.prop(tex, "use_mirror_y", text="Y")

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


class TypeMusgrave(Type, Panel):
    bl_idname = "YAFARAY4_PT_texture_type_musgrave"
    bl_label = "Musgrave"
    tex_type = 'MUSGRAVE'
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return
        layout = self.layout

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


class TypeVoronoi(Type, Panel):
    bl_idname = "YAFARAY4_PT_texture_type_voronoi"
    bl_label = "Voronoi"
    tex_type = 'VORONOI'
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return
        layout = self.layout
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


class TypeDistortedNoise(Type, Panel):
    bl_idname = "YAFARAY4_PT_texture_type_distorted_noise"
    bl_label = "Distorted Noise"
    tex_type = 'DISTORTED_NOISE'
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return
        layout = self.layout

        layout.prop(tex, "noise_distortion")
        layout.prop(tex, "noise_basis", text="Basis")

        split = layout.split()

        col = split.column()
        col.prop(tex, "distortion", text="Distortion")
        split.prop(tex, "noise_scale", text="Size")


class TypeOcean(Type, Panel):
    bl_idname = "YAFARAY4_PT_texture_type_ocean"
    bl_label = "Ocean"
    tex_type = 'OCEAN'
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    def draw(self, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return
        layout = self.layout

        ot = tex.ocean

        col = layout.column()
        col.prop(ot, "ocean_object")
        col.prop(ot, "output")


class SlotMapping(Slot, Panel):
    bl_idname = "YAFARAY4_PT_texture_slot_mapping"
    bl_label = "YafaRay Mapping (Map Input)"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):
        tex = get_texture_from_context(context)
        if tex is None:
            return
        engine = context.scene.render.engine
        return engine in cls.COMPAT_ENGINES and context.scene.yafaray4.texture_edition_panel != 'TEXTURE'

    def draw(self, context):
        layout = self.layout
        if context.scene.yafaray4.texture_edition_panel == 'WORLD':
            split = ui_split(layout, 0.3)
            col = split.column()
            world = context.scene.world
            col.label(text="Coordinates:")
            col = split.column()
            col.prop(world, "yaf_mapworld_type", text="")
        else:
            material_properties = context.active_object.active_material.yafaray4
            tex = material_properties.texture_slots[material_properties.active_texture_index]
            if tex is None:
                return
            split = ui_split(layout, 0.3)
            col = split.column()
            col.label(text="Coordinates:")
            col = split.column()
            col.prop(tex, "texture_coords", text="")

            if tex.texture_coords == 'UV':
                pass
                # UV layers not supported in yafaray engine
                """
                split = ui_split(layout, 0.3)
                split.label(text="Layer:")
                ob = context.object
                if ob and ob.type == 'MESH':
                    split.prop_search(tex, "uv_layer", ob.data, "uv_textures", text="")
                else:
                    split.prop(tex, "uv_layer", text="")
                """

            elif tex.texture_coords == 'OBJECT':
                split = ui_split(layout, 0.3)
                split.label(text="Object:")
                split.prop(tex, "object", text="")

            split = ui_split(layout, 0.3)
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


class SlotInfluence(Slot, Panel):
    bl_idname = "YAFARAY4_PT_texture_slot_influence"
    bl_label = "YafaRay Influence (Map To)"
    COMPAT_ENGINES = {'YAFARAY4_RENDER'}

    @classmethod
    def poll(cls, context):
        tex = get_texture_from_context(context)
        if tex is None or context.scene.yafaray4.texture_edition_panel != 'MATERIAL':
            return
        engine = context.scene.render.engine
        return engine in cls.COMPAT_ENGINES

    def draw(self, context):
        material = context.active_object.active_material
        texture_slot = material.yafaray4.texture_slots[material.yafaray4.active_texture_index]
        texture = texture_slot.texture

        def factor_but(layout, toggle, factor, name):
            row = layout.row(align=True)
            row.prop(texture_slot, toggle, text="")
            sub = row.row()
            sub.active = getattr(texture_slot, toggle)
            sub.prop(texture_slot, factor, text=name, slider=True)
            return sub  # XXX, temp. use_map_normal needs to override.

        shader_nodes = dict()
        shader_nodes["Bump"] = ["use_map_normal", "normal_factor", "Bump"]
        shader_nodes["MirrorAmount"] = ["use_map_raymir", "raymir_factor", "Mirror Amount"]
        shader_nodes["SigmaOren"] = ["use_map_hardness", "hardness_factor", "Sigma Amount for Oren Nayar"]
        shader_nodes["MirrorColor"] = ["use_map_mirror", "mirror_factor", "Mirror Color"]
        shader_nodes["DiffuseColor"] = ["use_map_color_diffuse", "diffuse_color_factor", "Diffuse Color"]
        shader_nodes["GlossyColor"] = ["use_map_color_spec", "specular_color_factor", "Glossy Color"]
        shader_nodes["GlossyAmount"] = ["use_map_specular", "specular_factor", "Glossy Amount"]
        shader_nodes["Transparency"] = ["use_map_alpha", "alpha_factor", "Transparency"]
        shader_nodes["Translucency"] = ["use_map_translucency", "translucency_factor", "Translucency"]
        shader_nodes["BlendAmount"] = ["use_map_diffuse", "diffuse_factor", "Blending Amount"]
        shader_nodes["DiffuseReflection"] = ["use_map_diffuse", "diffuse_factor", "Diffuse reflection Amount"]
        shader_nodes["FilterColor"] = ["use_map_color_reflection", "reflection_color_factor", "Filter Color Amount"]
        shader_nodes["IORAmount"] = ["use_map_warp", "warp_factor", "IOR Amount (added to material IOR)"]
        shader_nodes["RoughnessAmount"] = ["use_map_hardness", "hardness_factor", "Roughness amount"]
        shader_nodes["ExponentAmount"] = ["use_map_ambient", "ambient_factor", "Glossy Exponent amount"]
        shader_nodes["Wireframe"] = ["use_map_displacement", "displacement_factor", "Wireframe Amount"]

        material_shader_nodes = dict()
        material_shader_nodes["glass"] = ["FilterColor", "MirrorColor", "IORAmount", "Bump", "Wireframe"]
        material_shader_nodes["rough_glass"] = ["RoughnessAmount", "FilterColor", "MirrorColor", "IORAmount", "Bump",
                                                "Wireframe"]
        material_shader_nodes["glossy"] = ["DiffuseColor", "DiffuseReflection", "SigmaOren", "GlossyColor",
                                           "GlossyAmount", "ExponentAmount", "Bump", "Wireframe"]
        material_shader_nodes["coated_glossy"] = ["DiffuseColor", "DiffuseReflection", "SigmaOren", "GlossyColor",
                                                  "GlossyAmount", "ExponentAmount", "MirrorAmount", "MirrorColor",
                                                  "IORAmount", "Bump", "Wireframe"]
        material_shader_nodes["shinydiffusemat"] = ["DiffuseColor", "DiffuseReflection", "SigmaOren", "MirrorAmount",
                                                    "MirrorColor", "IORAmount", "Transparency", "Translucency", "Bump",
                                                    "Wireframe"]
        material_shader_nodes["blend"] = ["BlendAmount"]

        if context.scene.yafaray4.texture_edition_panel == 'MATERIAL':
            nodes = material_shader_nodes[material.mat_type]
            col = self.layout.column()

            for node in nodes:
                value = shader_nodes[node]
                factor_but(col, value[0], value[1], value[2])
                if node == "Bump" and getattr(texture_slot, "use_map_normal") and texture.yaf_tex_type == 'IMAGE':
                    col.prop(texture, "yaf_is_normal_map", "Use map as normal map")

        elif context.scene.yafaray4.texture_edition_panel == 'WORLD':  # for setup world texture
            split = self.layout.split()

            col = split.column()
            factor_but(col, "use_map_blend", "blend_factor", "Blend")
            factor_but(col, "use_map_horizon", "horizon_factor", "Horizon")

            col = split.column()
            factor_but(col, "use_map_zenith_up", "zenith_up_factor", "Zenith Up")
            factor_but(col, "use_map_zenith_down", "zenith_down_factor", "Zenith Down")

        if context.scene.yafaray4.texture_edition_panel != 'WORLD':
            split = self.layout.split()

            col = split.column()
            col.prop(texture_slot, "blend_type", text="Blend")
            col.prop(texture_slot, "use_rgb_to_intensity", text="No RGB")
            col.prop(texture_slot, "color", text="")

            col = split.column()
            col.prop(texture_slot, "invert", text="Negative")
            col.prop(texture_slot, "use_stencil")

        if context.scene.yafaray4.texture_edition_panel == 'MATERIAL' or context.scene.yafaray4.texture_edition_panel == 'WORLD':
            self.layout.separator()
            self.layout.row().prop(texture_slot, "default_value", text="Default Value", slider=True)


classes = (
    OBJECT_UL_List,
    Context,
    Preview,
    PreviewControls,
    Colors,
    TypeClouds,
    TypeWood,
    TypeMarble,
    TypeBlend,
    TypeImage,
    TypeImageSampling,
    TypeImageMapping,
    TypeMusgrave,
    TypeVoronoi,
    TypeDistortedNoise,
    TypeOcean,
    SlotMapping,
    SlotInfluence,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":  # Only used when editing and testing "live" within Blender Text Editor. If needed, 
    # before running Blender set the environment variable "PYTHONPATH" with the path to the directory where the 
    # "libyafaray4_bindings" compiled module is installed on
    register()
