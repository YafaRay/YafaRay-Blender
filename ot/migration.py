# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.app.handlers import persistent


@persistent
def migration(_dummy):
    for tex in bpy.data.textures:
        if tex is not None:
            # set the correct texture type on file load....
            # converts old files, where property yaf_tex_type wasn't defined
            print("Load Handler: Convert Yafaray texture \"{0}\" with texture type: \"{1}\" to \"{2}\""
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
    # convert image output file type setting from blender to yafaray's file type setting on file load, so that both
    # are the same...
    if bpy.context.scene.render.image_settings.file_format is not bpy.context.scene.img_output:
        bpy.context.scene.img_output = bpy.context.scene.render.image_settings.file_format
