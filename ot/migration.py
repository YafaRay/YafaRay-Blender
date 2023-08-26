# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.app.handlers import persistent

from .. import bl_info


def copy_attributes(source, destination, mapping):
    print("Copying attributes from", source, "to", destination)
    attributes = [a for a in dir(source) if not a.startswith("__")]
    for attr in attributes:
        if attr in mapping:
            if mapping[attr] is None:
                continue
            else:
                attr_v4 = mapping[attr]
        else:
            attr_v4 = attr
        if hasattr(source, attr):
            attr_value = getattr(source, attr)
            print("  Copying attribute:", attr, "with value:", attr_value, "to attribute v4:", attr_v4)
            setattr(destination, attr_v4, attr_value)


@persistent
def migration(_dummy):
    scene = bpy.context.scene
    print("scene.world.texture", scene.world.texture, "scene.world.texture", scene.world.texture)
    for tex in bpy.data.textures:
        if tex is not None:
            # set the correct texture type on file load....
            # converts old files, where property yaf_tex_type wasn't defined
            print(bl_info["name"], "Handler: Convert Yafaray texture \"{0}\" with texture type: \"{1}\" to \"{2}\""
                  .format(tex.name, tex.yaf_tex_type, tex.type))
            tex.yaf_tex_type = tex.type
    for mat in bpy.data.materials:
        if mat is not None:
            # from old scenes, convert old blend material Enum properties into the new string properties
            if mat.mat_type == "blend":
                if not mat.is_property_set("material1name") or not mat.material1name:
                    mat.material1name = mat.material1
                if not mat.is_property_set("material2name") or not mat.material2name:
                    mat.material2name = mat.material2
    # convert image output file type setting from blender to YafaRay's file type setting on file load, so that both
    # are the same...
    if scene.render.image_settings.file_format is not scene.img_output:
        scene.img_output = scene.render.image_settings.file_format

    # convert old world texture slot to dedicated YafaRay world texture parameter
    if (bpy.app.version < (2, 80, 0)
            and not scene.yafaray4.migration.migrated_to_v4
            and scene.world.active_texture is not None):
        print(bl_info["name"], "Handler: Initial 'one-off' migration from Yafaray v3 parameters")
        scene.world.texture = scene.world.active_texture
        scene.yafaray4.migration.migrated_to_v4 = True
        if hasattr(scene, "yafaray"):
            mapping = {
                "name": None,
                "bl_rna": None,
                "rna_type": None,
                "verbosityLevels": None,
            }
            copy_attributes(scene.yafaray.logging, scene.yafaray4.logging, mapping)
            mapping = {
                "name": None,
                "bl_rna": None,
                "rna_type": None,
            }
            copy_attributes(scene.yafaray.noise_control, scene.yafaray4.noise_control, mapping)
            mapping = {
                "name": None,
                "bl_rna": None,
                "rna_type": None,
                "OBJECT_OT_CamRotReset": None,
                "OBJECT_OT_CamZoomIn": None,
                "OBJECT_OT_CamZoomOut": None,
            }
            copy_attributes(scene.yafaray.preview, scene.yafaray4.preview, mapping)
            mapping = {
                "name": None,
                "bl_rna": None,
                "rna_type": None,
                "renderPassItemsBasic": None,
                "renderInternalPassAdvanced": None,
                "renderPassAllItems": None,
                "renderPassItemsAO": None,
                "renderPassItemsDisabled": None,
                "renderPassItemsIndex": None,
                "renderPassItemsDebug": None,
                "renderPassItemsDepth": None,
            }
            copy_attributes(scene.yafaray.passes, scene.yafaray4.passes, mapping)
