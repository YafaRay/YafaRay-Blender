# SPDX-License-Identifier: GPL-2.0-or-later

import bpy


def ui_split(ui_item, factor):
    if bpy.app.version >= (2, 80, 0):
        return ui_item.split(factor=factor)
    else:
        return ui_item.split(percentage=factor)


def material_from_context(context):
    if bpy.app.version >= (2, 80, 0):
        return context.material
    else:
        # noinspection PyUnresolvedReferences
        from bl_ui.properties_material import active_node_mat
        return active_node_mat(context.material)