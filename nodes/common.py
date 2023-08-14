# SPDX-License-Identifier: GPL-2.0-or-later

from nodeitems_utils import NodeCategory as BlenderNodeCategory


class NodeCategory(BlenderNodeCategory):
    bl_idname = "YafaRay4NodeCategory"

    @classmethod
    def poll(cls, context):
        # return context.space_data.tree_type == "YAFARAY4_NODE_TREE"
        return context.scene.render.engine == "YAFARAY4_RENDER" and context.space_data.tree_type == 'ShaderNodeTree'
